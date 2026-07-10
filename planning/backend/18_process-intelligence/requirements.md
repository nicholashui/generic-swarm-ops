# 18 — Process Intelligence

| Field | Value |
|-------|-------|
| Spec ID | `BE-18` |
| Source | `backend.md` — §7.14, §11.14, PI disk artifacts |
| Related architecture | structure.md §2.3 PI layer |
| Priority order | 18 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Process intelligence APIs: metrics, workflow performance, bottlenecks, costs, failures, approval delays.
- Aggregation from workflow run data.
- Disk artifacts under business/process-intelligence/.

### 1.2 Out of scope
- Five independent always-on LLM PI agents.
- Full commercial process mining suite.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-18-01 | Ops leads | See bottlenecks and failure patterns. |
| STK-18-02 | Architects | Empirical traces not only opinions. |
| STK-18-03 | Evolution | Signals for improvement opportunities. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-18-01 | The backend shall expose process intelligence APIs for workflow performance analytics, bottleneck detection, failure patterns, average duration, approval delays, agent performance, cost by workflow/department, task success rate, and automation opportunities as data allows. |
| FR-18-02 | Initial process APIs may aggregate workflow run data without requiring external process mining clusters. |
| FR-18-03 | When events are ingested or runs complete, the backend shall be able to write process-intelligence disk artifacts under business/process-intelligence/. |
| FR-18-04 | The backend shall expose endpoints for metrics, workflow-performance, bottlenecks, costs, and failures (and related summaries as implemented). |
| FR-18-05 | Process intelligence services shall not directly mutate production workflow DNA. |
| FR-18-06 | Access to process intelligence summaries shall require appropriate authorization. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-18-01 | Aggregate metrics for small histories shall return under 1s p95 local. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-18-02 | PI APIs shall not leak cross-organization run details. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-18-01 | Metrics endpoint returns structured summary. |
| AC-18-02 | Bottlenecks/failures endpoints respond for seeded data. |
| AC-18-03 | PI artifacts directory receives outputs on ingest/run paths as implemented. |
| AC-18-04 | Unauthorized access denied. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-11, BE-14 | Ops analytics, evolution signals |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-18-01 | API smoke for processes routes. | Automated |
| TV-18-02 | Artifact write path unit/integration. | Automated |
| TV-18-03 | Authz negative test. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.14 Process Intelligence | FR-18-01 … FR-18-05 |
| backend.md §11.14 | FR-18-04 |
| backend.md §24.3 PI | FR-18-03 |
