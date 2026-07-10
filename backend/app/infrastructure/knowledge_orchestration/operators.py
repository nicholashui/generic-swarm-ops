"""Typed graph operators (Agents-K1 O1/O2/O5 lite)."""
from __future__ import annotations

from typing import Any


def resolve_seed(nodes: list[dict[str, Any]], mention: str) -> list[dict[str, Any]]:
    """O1 — Seed resolution by label / id substring."""
    q = (mention or "").lower().strip()
    if not q:
        return []
    hits = []
    for node in nodes:
        label = str(node.get("label") or "").lower()
        nid = str(node.get("id") or "").lower()
        if q in label or q in nid or label in q:
            hits.append(node)
    # Prefer higher degree later; for now stable sort by label length
    hits.sort(key=lambda n: len(str(n.get("label") or "")))
    return hits


def lineage(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    seed_id: str,
    *,
    max_hops: int = 3,
) -> list[dict[str, Any]]:
    """O2 — Follow BUILDS_ON / REQUIRES / GOVERNED_BY edges from seed."""
    allowed = {"BUILDS_ON", "REQUIRES", "GOVERNED_BY", "USES", "ALTERNATIVE_TO"}
    node_by_id = {n["id"]: n for n in nodes if n.get("id")}
    frontier = [seed_id]
    seen = {seed_id}
    path: list[dict[str, Any]] = []
    if seed_id in node_by_id:
        path.append({"hop": 0, "node": node_by_id[seed_id], "via": None})
    for hop in range(1, max_hops + 1):
        nxt: list[str] = []
        for edge in edges:
            if edge.get("relation") not in allowed:
                continue
            head, tail = edge.get("head"), edge.get("tail")
            for a, b in ((head, tail), (tail, head)):
                if a in frontier and b not in seen and b in node_by_id:
                    seen.add(b)
                    nxt.append(b)
                    path.append({"hop": hop, "node": node_by_id[b], "via": edge})
        frontier = nxt
        if not frontier:
            break
    return path


def detect_gaps(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """O5 — Gap detection: orphan entities, claim without relation, singleton docs."""
    gaps: list[dict[str, Any]] = []
    connected: set[str] = set()
    for edge in edges:
        if edge.get("head"):
            connected.add(edge["head"])
        if edge.get("tail"):
            connected.add(edge["tail"])

    for node in nodes:
        if node.get("module") == "B" and node.get("id") not in connected:
            gaps.append(
                {
                    "type": "orphan_entity",
                    "node_id": node.get("id"),
                    "label": node.get("label"),
                    "message": "Entity has no typed relations",
                }
            )
        if node.get("module") == "C" and node.get("id") not in connected:
            gaps.append(
                {
                    "type": "ungrounded_claim",
                    "node_id": node.get("id"),
                    "label": node.get("label"),
                    "message": "Claim has no linking relations to entities",
                }
            )

    by_doc: dict[str, int] = {}
    for node in nodes:
        did = str(node.get("document_id") or "unknown")
        by_doc[did] = by_doc.get(did, 0) + 1
    for did, count in by_doc.items():
        if count <= 1:
            gaps.append(
                {
                    "type": "sparse_document",
                    "document_id": did,
                    "message": "Document produced only one graph node — extraction thin",
                }
            )
    return gaps
