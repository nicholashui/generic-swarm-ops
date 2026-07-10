"""Graph federation export (Neo4j Cypher / GraphAnything-friendly JSON).

Does not require Neo4j installed — always writes export artifacts; optionally
pushes via bolt if NEO4J_* env is set and driver available.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


def export_cypher(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> str:
    lines = ["// Generic Swarm knowledge graph export", f"// generated_at: {_now()}", ""]
    for node in nodes:
        nid = str(node.get("id") or "").replace("'", "")
        label = str(node.get("label") or "").replace("'", "\\'")
        kind = str(node.get("kind") or "Entity").replace(" ", "_")
        lines.append(
            f"MERGE (n:`{kind}` {{id: '{nid}'}}) "
            f"SET n.label = '{label}', n.module = '{node.get('module')}', "
            f"n.document_id = '{node.get('document_id')}', n.source_refs = {json.dumps(node.get('source_refs') or [])};"
        )
    for edge in edges:
        hid = str(edge.get("head") or "").replace("'", "")
        tid = str(edge.get("tail") or "").replace("'", "")
        rel = str(edge.get("relation") or "RELATED").replace(" ", "_")
        lines.append(
            f"MATCH (a {{id: '{hid}'}}), (b {{id: '{tid}'}}) "
            f"MERGE (a)-[r:`{rel}`]->(b) "
            f"SET r.evidence = '{str(edge.get('evidence_span') or '')[:120].replace(chr(39), '')}';"
        )
    return "\n".join(lines) + "\n"


def export_graphanything_json(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "agents_k1_lite_v1",
        "format": "graphanything_compatible",
        "generated_at": _now(),
        "nodes": [
            {
                "id": n.get("id"),
                "label": n.get("label"),
                "type": n.get("kind"),
                "module": n.get("module"),
                "source_file": (n.get("source_refs") or [None])[0],
                "evidence": n.get("evidence_span"),
            }
            for n in nodes
        ],
        "edges": [
            {
                "id": e.get("id"),
                "source": e.get("head"),
                "target": e.get("tail"),
                "relation": e.get("relation"),
                "evidence": e.get("evidence_span"),
            }
            for e in edges
        ],
    }


def write_federation_artifacts(
    repo_root: Path,
    *,
    organization_id: str,
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, Any]:
    out_dir = repo_root / "business" / "knowledge-base" / "provenance" / "federation"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    cypher_path = out_dir / f"graph_{organization_id}_{stamp}.cypher"
    json_path = out_dir / f"graph_{organization_id}_{stamp}.json"
    cypher_path.write_text(export_cypher(nodes, edges), encoding="utf-8")
    payload = export_graphanything_json(nodes, edges)
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    # Always refresh "latest" pointers
    (out_dir / "latest.cypher").write_text(cypher_path.read_text(encoding="utf-8"), encoding="utf-8")
    (out_dir / "latest.json").write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")
    return {
        "cypher_path": str(cypher_path.as_posix()),
        "json_path": str(json_path.as_posix()),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "latest_cypher": str((out_dir / "latest.cypher").as_posix()),
        "latest_json": str((out_dir / "latest.json").as_posix()),
    }


def try_push_neo4j(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], settings: Any) -> dict[str, Any]:
    """Optional bolt push if neo4j driver + NEO4J_URI configured."""
    uri = getattr(settings, "neo4j_uri", None)
    if not uri:
        return {"pushed": False, "reason": "neo4j_uri_not_set"}
    try:
        from neo4j import GraphDatabase  # type: ignore
    except ImportError:
        return {"pushed": False, "reason": "neo4j_driver_not_installed"}
    user = getattr(settings, "neo4j_user", None) or "neo4j"
    password = getattr(settings, "neo4j_password", None) or ""
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        cypher_nodes = export_cypher(nodes, edges)
        with driver.session() as session:
            # Execute statements one by one (simple federation)
            for stmt in cypher_nodes.split(";"):
                s = stmt.strip()
                if s and not s.startswith("//"):
                    session.run(s)
        driver.close()
        return {"pushed": True, "uri": uri, "nodes": len(nodes), "edges": len(edges)}
    except Exception as exc:  # noqa: BLE001
        return {"pushed": False, "reason": str(exc)}
