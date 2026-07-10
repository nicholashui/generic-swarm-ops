# 13 — Knowledge and Memory UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-13` |
| Source | `frontend.md` — §16.16–16.19 Knowledge/Memory pages, Phase 11 |
| Related architecture | backend BE-15, BE-16 |
| Priority order | 13 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Knowledge overview, sources, documents, and search pages.
- Memory list/detail inspection pages.
- Read-oriented ops UX over backend knowledge/memory APIs.
- Source connection forms only insofar as backend supports (no live CRM requirement for product bar).

### 1.2 Out of scope
- Embedding/indexing engines (backend).
- Full commercial LightRAG/Neo4j explorer product (§33.5 non-goal).
- Direct vector DB access from browser.

### 1.3 System under specification
Knowledge and memory operator UI.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-13-01 | Operators | See what knowledge sources and memories exist. |
| STK-13-02 | Reviewers | Inspect provenance fields when backend returns them. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-13-01 | The frontend shall provide knowledge routes for overview, sources, documents, and search. |
| FR-13-02 | The frontend shall provide memory list and detail routes under `/app/memory`. |
| FR-13-03 | Knowledge/memory views shall render backend-returned metadata and shall not invent index contents. |
| FR-13-04 | When search is invoked, the frontend shall call backend retrieval APIs and display results with available provenance. |
| FR-13-05 | The frontend shall not perform embedding or indexing in the browser. |
| FR-13-06 | Mutations (add source, delete memory) shall only occur through backend APIs when exposed and permitted. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-13-01 | Search UI shall debounce queries to avoid request storms. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-13-02 | Knowledge UI shall not exfiltrate full corpora beyond what backend returns to the caller. |
| NFR-13-03 | Memory detail shall respect permission UX for sensitive records. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-13-01 | Knowledge and memory pages render in app shell. |
| AC-13-02 | Search calls backend and shows results or empty state. |
| AC-13-03 | No client-side vector store dependency. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-04, FE-06, FE-07 | Shadow-learning / data ops surfaces |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-13-01 | Manual: open knowledge/memory sections. | Manual |
| TV-13-02 | Unit: search debounce. | Unit |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.16–16.19 Knowledge/Memory | FR-13-01 … FR-13-04 |
| §4.2 no embedding | FR-13-05 |
| Phase 11 | AC-13-* |


