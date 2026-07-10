"""Tiered hybrid retrieval (structure.md §3.4 spirit).

Default is **Tier 0** keyword search with mandatory provenance.
**Tier 1** is a minimal entity-link expansion (LightRAG-lite) for multi-hop
queries — no external graph vendor required.

Tier 2 (RAPTOR-style hierarchical summaries) is intentionally out of scope.
"""
from __future__ import annotations

import re
from typing import Any

RETRIEVAL_TIER_NOTE = {
    "default_tier": 0,
    "tier_0": "keyword_search_with_mandatory_provenance",
    "tier_1": "entity_link_multi_hop_lite",
    "tier_2": "deferred_raptor_optional",
    "escalation": "tier0_then_tier1_on_relational_queries",
    "non_goals": ["full_lightrag_vendor", "cloud_vector_lock_in"],
}

# Relational / multi-hop cues (structure.md escalation rule)
_TIER1_CUES = re.compile(
    r"\b(related|linked|which policy|who owns|depends on|governed by|"
    r"refers to|connection|multi[- ]?hop|relationship|associated)\b",
    re.I,
)

_ENTITY_PATTERNS = [
    re.compile(r"\b(wf_[a-z0-9_]+)\b", re.I),
    re.compile(r"\b(pol_[a-z0-9_]+)\b", re.I),
    re.compile(r"\b(agent_[a-z0-9_]+|[a-z_]+_agent)\b", re.I),
    re.compile(r"\b(business/[a-z0-9_./-]+\.(?:md|json))\b", re.I),
    re.compile(r"\b(tier_[0-5]_[a-z_]+)\b", re.I),
]


def extract_entity_links(text: str, *, source: str | None = None) -> list[dict[str, str]]:
    """Extract lightweight entity mentions for Tier-1 graph edges."""
    blob = text or ""
    found: dict[str, dict[str, str]] = {}
    for pattern in _ENTITY_PATTERNS:
        for match in pattern.findall(blob):
            value = match if isinstance(match, str) else match[0]
            key = value.lower()
            if key not in found:
                found[key] = {"entity": value, "kind": _entity_kind(value)}
    if source:
        sk = source.lower()
        if sk not in found:
            found[sk] = {"entity": source, "kind": "source_path"}
    return list(found.values())


def _entity_kind(value: str) -> str:
    v = value.lower()
    if v.startswith("wf_"):
        return "workflow"
    if v.startswith("pol_"):
        return "policy"
    if "agent" in v:
        return "agent"
    if v.startswith("business/") or v.endswith((".md", ".json")):
        return "document_path"
    if v.startswith("tier_"):
        return "risk_tier"
    return "entity"


def score_keyword_hit(query: str, title: str, content: str) -> float:
    """Simple term overlap score for Tier 0 ranking."""
    q_terms = {t for t in re.split(r"\W+", (query or "").lower()) if len(t) > 2}
    if not q_terms:
        return 0.0
    blob = f"{title or ''} {content or ''}".lower()
    hits = sum(1 for t in q_terms if t in blob)
    return round(hits / max(len(q_terms), 1), 4)


def should_escalate_to_tier1(query: str | None, *, force: bool = False) -> bool:
    if force:
        return True
    if not query:
        return False
    return bool(_TIER1_CUES.search(query))


def documents_share_entity(a_links: list[dict[str, str]], b_links: list[dict[str, str]]) -> list[str]:
    a_set = {item.get("entity", "").lower() for item in a_links if item.get("entity")}
    b_set = {item.get("entity", "").lower() for item in b_links if item.get("entity")}
    return sorted(a_set & b_set)


def expand_multi_hop(
    seed_hits: list[dict[str, Any]],
    corpus: list[dict[str, Any]],
    *,
    max_extra: int = 5,
) -> list[dict[str, Any]]:
    """Tier-1 lite: pull related docs that share entity links with Tier-0 hits."""
    seed_ids = {h.get("id") for h in seed_hits}
    shared_edges: list[tuple[dict[str, Any], list[str], dict[str, Any]]] = []
    for seed in seed_hits:
        seed_links = seed.get("entity_links") or extract_entity_links(
            f"{seed.get('title', '')} {seed.get('content', '')}",
            source=seed.get("source"),
        )
        for doc in corpus:
            if doc.get("id") in seed_ids:
                continue
            doc_links = doc.get("entity_links") or extract_entity_links(
                f"{doc.get('title', '')} {doc.get('content', '')}",
                source=doc.get("source"),
            )
            shared = documents_share_entity(seed_links, doc_links)
            if shared:
                shared_edges.append((doc, shared, seed))
    extras: list[dict[str, Any]] = []
    seen: set[str] = set()
    for doc, shared, seed in shared_edges:
        did = str(doc.get("id"))
        if did in seen:
            continue
        seen.add(did)
        item = dict(doc)
        item["retrieval_hop"] = 1
        item["linked_from"] = seed.get("id")
        item["shared_entities"] = shared
        extras.append(item)
        if len(extras) >= max_extra:
            break
    return extras
