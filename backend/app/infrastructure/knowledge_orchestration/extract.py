"""K1-lite extraction: entities, claims, relations with evidence spans.

Rule/heuristic based (no 4B model) — agent-native graph spirit of Agents-K1
without external extractors.
"""
from __future__ import annotations

import re
import uuid
from typing import Any

from app.infrastructure.knowledge.retrieval import extract_entity_links

_CLAIM_PATTERNS = [
    re.compile(r"(?P<span>[^.!?]{10,200}\b(?:requires?|must|shall|should)\b[^.!?]{5,120}[.!?])", re.I),
    re.compile(r"(?P<span>[^.!?]{10,200}\b(?:governed by|depends on|builds on)\b[^.!?]{5,120}[.!?])", re.I),
]

_RELATION_CUES = [
    (re.compile(r"\b(?:builds? on|extends?|derived from)\b", re.I), "BUILDS_ON"),
    (re.compile(r"\b(?:requires?|depends on|needs)\b", re.I), "REQUIRES"),
    (re.compile(r"\b(?:governed by|under policy)\b", re.I), "GOVERNED_BY"),
    (re.compile(r"\b(?:uses?|via|through)\b", re.I), "USES"),
    (re.compile(r"\b(?:alternative to|instead of)\b", re.I), "ALTERNATIVE_TO"),
]


def _node_id(kind: str, key: str) -> str:
    clean = re.sub(r"[^a-z0-9_]+", "_", key.lower()).strip("_")[:48]
    return f"kn_{kind}_{clean or uuid.uuid4().hex[:8]}"


def extract_document_graph(document: dict[str, Any]) -> dict[str, Any]:
    """Return nodes + edges for one knowledge document (Modules B/C/E lite)."""
    doc_id = str(document.get("id") or "unknown")
    title = str(document.get("title") or "")
    content = str(document.get("content") or "")
    source = str(document.get("source") or document.get("path") or f"knowledge:{doc_id}")
    blob = f"{title}\n{content}"

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    seen_nodes: set[str] = set()

    def add_node(kind: str, label: str, evidence: str, module: str) -> str:
        nid = _node_id(kind, label)
        if nid not in seen_nodes:
            seen_nodes.add(nid)
            nodes.append(
                {
                    "id": nid,
                    "kind": kind,
                    "label": label,
                    "module": module,  # A/B/C/E lite tags
                    "document_id": doc_id,
                    "evidence_span": evidence[:240],
                    "confidence": 0.7,
                    "source_refs": [source],
                }
            )
        return nid

    # Document structure node (Module A-lite)
    add_node("document", title or doc_id, title[:120] or doc_id, "A")

    # Module B: mentioned entities from entity link extractor
    for link in extract_entity_links(blob, source=source):
        entity = link.get("entity") or ""
        kind = link.get("kind") or "entity"
        add_node(kind, entity, entity, "B")

    # Module C: claims / obligations
    for pattern in _CLAIM_PATTERNS:
        for match in pattern.finditer(blob):
            span = match.group("span").strip()
            add_node("claim", span[:80], span, "C")

    # Module E: relations between co-occurring entities in a sentence
    sentences = re.split(r"(?<=[.!?])\s+", blob)
    entity_labels = [n["label"] for n in nodes if n.get("module") == "B"]
    for sentence in sentences:
        present = [e for e in entity_labels if e.lower() in sentence.lower()]
        if len(present) < 2:
            # still try relation cue with one entity + claim words
            pass
        rel = None
        for cue, rel_name in _RELATION_CUES:
            if cue.search(sentence):
                rel = rel_name
                break
        if not rel or len(present) < 2:
            continue
        head = present[0]
        tail = present[1]
        hid = _node_id(next((n["kind"] for n in nodes if n["label"] == head), "entity"), head)
        tid = _node_id(next((n["kind"] for n in nodes if n["label"] == tail), "entity"), tail)
        edges.append(
            {
                "id": f"ke_{uuid.uuid4().hex[:10]}",
                "head": hid,
                "relation": rel,
                "tail": tid,
                "document_id": doc_id,
                "evidence_span": sentence[:240],
                "confidence": 0.65,
                "source_refs": [source],
                "module": "E",
            }
        )

    return {
        "document_id": doc_id,
        "nodes": nodes,
        "edges": edges,
        "schema": "agents_k1_lite_v1",
        "modules_present": sorted({n.get("module") for n in nodes} | {e.get("module") for e in edges}),
    }
