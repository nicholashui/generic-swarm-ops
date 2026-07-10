# Knowledge And Memory

The knowledge layer separates rules, best practices, tacit knowledge, and provenance from episodic, semantic, procedural, decision, and evaluation memory.

## Retrieval tiers (structure.md §3.4)

See also: `business/knowledge-base/provenance/retrieval-tier-policy.md`.

| Tier | Behavior | When used |
|------|----------|-----------|
| **0 (default)** | Keyword search; every hit includes `source_refs` + `provenance.retrieval_tier` | Always |
| **1 (lite)** | Entity-link multi-hop expansion (shared workflow/policy/path entities) | Relational queries or `multi_hop=true` |
| **2** | Hierarchical summaries | Deferred |

### API

```http
GET  /api/v1/knowledge?query=billing+gate
GET  /api/v1/knowledge?query=which+policy+is+related&multi_hop=true
POST /api/v1/knowledge/search
     { "query": "...", "multi_hop": true, "limit": 10 }
```

Index builds `entity_links` for Tier-1 edges:

```http
POST /api/v1/knowledge/documents/{id}/index
```

### Evaluation

- Unit: `test_retrieval.py` (provenance + multi-hop).
- Fixtures: `business/evals/retrieval/tier0-provenance.json`, `tier1-multi-hop-entity.json`.

### Memory

Workflow execution enforces `allowed_memory_scopes` on read/write (seed agents union
`organization_memory` for flagship onboarding paths). Memory items carry provenance
independently of knowledge retrieval. Lessons from auto-reflect are written to
`organization_memory` and `improvement_lessons`.

### Graph orchestration (K1-lite)

- Index/extract: entities, claims, relations with evidence spans
- Operators: seed resolve (O1), lineage (O2), gaps (O5)
- Federation: `POST /api/v1/knowledge/graph/federate` → Cypher + GraphAnything-compatible JSON
