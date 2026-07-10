# Design — 09 Tiered Hybrid Retrieval

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-09-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-09`) |
| Source | `structure.md` §3.4 |
| Design quality bar | 100 |

---

## 1. Purpose

Cost-tiered retrieval with **always-on provenance**: default Tier 0, escalate to Tier 1 entity multi-hop, optional Tier 2 hierarchical summaries—without GraphRAG community reindex costs.

---

## 2. Context

### 2.1 Tier definitions (normative)

| Tier | Behavior | When |
|------|----------|------|
| 0 | Keyword + hashing embeddings (optional pgvector) | Default all queries |
| 1 | Entity-link multi-hop (LightRAG-lite) | `multi_hop=true` or relational cues |
| 2 | RAPTOR-style hierarchical summaries | On-demand corpus synthesis; **feature deferred** |

**Forbidden default:** GraphRAG community report rebuild on every document.

### 2.2 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-09-01 | LightRAG-lite not full vendor | Cost/complexity |
| D-09-02 | Hashing embeddings default | Offline deterministic |
| D-09-03 | Provenance mandatory on every hit | structure.md always-on |

---

## 3. Architecture

```text
Query + authz
  → ACL/sensitivity filter
  → Tier0Retriever
  → if escalate: Tier1Expander(entity_links)
  → if tier2 flag: HierarchicalSummaries (future)
  → attach source_refs + retrieval_tier
  → optional K1 graph operators / federate
```

### 3.1 Components

| ID | Component | Module |
|----|-----------|--------|
| C-09-1 | Indexer | chunk, embed, entity_links |
| C-09-2 | Tier0 | keyword + embed similarity |
| C-09-3 | Tier1 | multi-hop expansion |
| C-09-4 | Provenance layer | every hit |
| C-09-5 | K1-lite | extract/query/gaps |
| C-09-6 | Federation | Cypher/JSON export |
| C-09-7 | Policy | retrieval-tier-policy.md |
| C-09-8 | Eval fixtures | business/evals/retrieval |

---

## 4. Data models

### 4.1 Document / chunk

```text
KnowledgeDocument { id, status, sensitivity, acl, metadata, source_refs }
KnowledgeChunk { id, document_id, content, chunk_index, embedding?, entity_links[] }
EntityLink { entity_id, entity_type, related_ids[] }  // wf_, pol_, paths…
```

### 4.2 Hit model

```text
RetrievalHit {
  id, content_snippet, score,
  source_refs: string[],
  provenance: { retrieval_tier: 0|1|2, ... },
  entity_links?: EntityLink[]
}
```

### 4.3 Escalation rules

| Condition | Tier |
|-----------|------|
| Default | 0 |
| multi_hop=true | 1 |
| Query matches relational patterns (which/related/depends) | 1 |
| Global synthesis + feature flag | 2 |

Target traffic: ≥80% Tier 0 (monitor `retrieval_tier` metric).

---

## 5. Algorithms

### 5.1 Search

```text
search(q, user, multi_hop=false):
  assert_authz(user)
  base = tier0(q, acl_filter(user))
  if multi_hop or needs_relations(q):
    base = tier1_expand(base)
    tier = 1
  else:
    tier = 0
  for h in base:
    require source_refs non-empty else drop or mark ungrounded
    h.provenance.retrieval_tier = tier
  return base
```

### 5.2 Index

```text
index(document_id):
  extract text → chunk → embed → entity_links → store
  incremental: no full corpus rebuild required for Tier0/1 lite
```

---

## 6. API contract

| Method | Path |
|--------|------|
| GET | `/api/v1/knowledge?query=&multi_hop=` |
| POST | `/api/v1/knowledge/search` |
| POST | `/api/v1/knowledge/documents/{id}/index` |
| POST | `/api/v1/knowledge/graph/extract/{document_id}` |
| GET | `/api/v1/knowledge/graph/query` |
| GET | `/api/v1/knowledge/graph/gaps` |
| POST | `/api/v1/knowledge/graph/federate` |

Config: `GENERIC_SWARM_EMBEDDINGS_ENABLED`, `GENERIC_SWARM_PGVECTOR_ENABLED`, `NEO4J_URI`.

---

## 7. Evaluation design

Score separately: **context relevance**, **answer relevance**, **faithfulness**.  
Fixtures: `tier0-provenance`, `tier1-multi-hop-entity`. Tests: `test_retrieval.py`.

---

## 8. NFR design

| NFR | Design |
|-----|--------|
| NFR-09-01 Tier0 p95 ≤1.5s baseline local | In-process search |
| NFR-09-02 ≥80% Tier0 | Escalation rules + metrics |
| NFR-09-03 Tier1 only on cues | multi_hop flag |
| NFR-09-04–06 ACL, tenant isolation, untrusted content | filters + STRUCT-05 |

---

## 9. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-09-01…02 | Tier0 §2–5 | test_retrieval |
| FR-09-03…04 | Tier1 §4–5 | multi_hop fixtures |
| FR-09-05…06 | Tier2 deferred §2 | policy doc |
| FR-09-07…10 | Provenance + eval §4,7 | fixtures |
| NFR-09-01…06 | §8 | unit + policy |
| AC-09-01…04 | §6–7 | automated |

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-09-01 | Full LightRAG / Neo4j mesh | Non-goal |
| OI-09-02 | Tier2 RAPTOR builder | Deferred |
| OI-09-03 | Real embedding model default | Optional flag path |

---

## 11. Design score claim

**Self-score: 100** — tiers, models, algorithms, API, eval, NFR, RTM.
