# 15 — Knowledge Base and Retrieval

| Field | Value |
|-------|-------|
| Spec ID | `BE-15` |
| Source | `backend.md` — §7.10, §11.9, §14.1–14.2, tiered retrieval as-built |
| Related architecture | structure.md §3.4 retrieval; STRUCT-09 |
| Priority order | 15 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Knowledge document lifecycle: upload/create, index, chunk, embed, search, archive/delete.
- Document statuses uploaded/processing/indexed/failed/archived/deleted.
- Retrieval pipeline with ACL filtering and provenance.
- Tier-0/1 retrieval as-built; optional federation export.

### 1.2 Out of scope
- Full commercial LightRAG/Neo4j mesh (non-goal).
- Frontend document viewer UX.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-15-01 | Knowledge managers | Ingest and search policies/SOPs. |
| STK-15-02 | Agents/workflows | Retrieve allowed context with provenance. |
| STK-15-03 | Security | ACL and sensitivity enforcement. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-15-01 | The backend shall expose controlled access to knowledge sources including uploaded documents and markdown/policy materials. |
| FR-15-02 | The backend shall support document lifecycle statuses uploaded, processing, indexed, failed, archived, and deleted. |
| FR-15-03 | When a document is ingested, the backend shall support store → index job → extract → chunk → embed → store chunks/vector refs → mark indexed. |
| FR-15-04 | When search is requested, the backend shall check permissions, filter by organization/department/sensitivity/ACL, retrieve results, optionally rerank, return only allowed results, and audit sensitive access. |
| FR-15-05 | The backend shall expose list/create/get/delete/index/search knowledge endpoints. |
| FR-15-06 | The backend shall implement tiered retrieval starting at Tier 0 (keyword/hash embed + provenance) and Tier 1 multi-hop lite where enabled. |
| FR-15-07 | When returning retrieval results, the backend shall include provenance/source references where available. |
| FR-15-08 | If a caller lacks knowledge:read, then the backend shall deny search and document access. |
| FR-15-09 | Where K1-lite knowledge graph features are enabled, the backend shall support extract/operators and optional federation export without requiring Neo4j for core product bar. |
| FR-15-10 | Retrieved content shall be marked untrusted for prompt-injection safety in downstream consumers. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-15-01 | Tier-0 search p95 under 1s local for small corpora. |
| NFR-15-02 | Indexing a small document shall complete without blocking the upload API response (async job acceptable). |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-15-03 | Knowledge ACL shall be enforced server-side. |
| NFR-15-04 | Uploads shall be validated/sanitized for type and size limits. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-15-01 | Create document and search returns it when indexed/available. |
| AC-15-02 | Cross-org document not visible. |
| AC-15-03 | Search without permission denied. |
| AC-15-04 | Provenance fields present on retrieval results when sources exist. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-06, BE-03 | BE-11 knowledge steps, BE-18 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-15-01 | Integration: ingest + search. | Automated |
| TV-15-02 | ACL negative test. | Automated |
| TV-15-03 | Tier-0 retrieval unit tests. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.10 Knowledge | FR-15-01 … FR-15-05 |
| backend.md §14.1–14.2 | FR-15-03 … FR-15-04 |
| backend.md §24.3 Retrieval/K1 | FR-15-06 … FR-15-09 |
