# 17 — Evaluation System

| Field | Value |
|-------|-------|
| Spec ID | `BE-17` |
| Source | `backend.md` — §7.12, §11.12, evaluation design links |
| Related architecture | structure.md §8 evaluation harness |
| Priority order | 17 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Evaluation types: schema, business rules, policy, hallucination risk, completeness, formatting, safety, cost, human review.
- Result statuses passed/failed/warning/requires_review.
- Linkage to runs/steps/outputs.
- Manual run evaluation endpoints and corpus evaluation for evolution.

### 1.2 Out of scope
- External public leaderboard hosting.
- Replacing governance deny with soft eval warnings only.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-17-01 | Quality owners | Block unsafe outputs. |
| STK-17-02 | Evolution | Corpus scores for variants. |
| STK-17-03 | Operators | See eval results on runs. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-17-01 | The backend shall evaluate important outputs before returning or releasing them when evaluation policy requires. |
| FR-17-02 | The backend shall support evaluation types including schema validation, business rule validation, policy compliance, hallucination risk check, completeness check, formatting check, safety check, cost check, and human review. |
| FR-17-03 | Evaluation results shall use statuses passed, failed, warning, and requires_review. |
| FR-17-04 | Evaluation results shall link to workflow run, step, agent output, and/or final output as applicable. |
| FR-17-05 | The backend shall expose list/get evaluations, run evaluation manually, and get evaluations for a workflow run. |
| FR-17-06 | If a required evaluation fails, then the backend shall block release/promotion paths that depend on that evaluation. |
| FR-17-07 | The backend shall support corpus evaluation used by evolution sandbox fitness scoring. |
| FR-17-08 | Evaluation runs shall be persisted for auditability and comparison. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-17-01 | Schema/business rule evals shall complete under 200ms local for typical payloads. |
| NFR-17-02 | Corpus evaluation may be asynchronous for large sets but shall report status. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-17-03 | Evaluation configuration shall not be mutable by unauthorized roles. |
| NFR-17-04 | Eval results shall not expose secrets from fixtures. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-17-01 | Manual evaluation endpoint returns persisted result. |
| AC-17-02 | Failed required eval blocks unsafe release path in tests. |
| AC-17-03 | Run-linked evaluations queryable by run id. |
| AC-17-04 | Corpus eval callable for a sandbox variant. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-11 | BE-20 promote gates, BE-21 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-17-01 | Unit: schema eval pass/fail. | Automated |
| TV-17-02 | Integration: evaluations on run. | Automated |
| TV-17-03 | Corpus eval smoke for evolution. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.12 Evaluation | FR-17-01 … FR-17-06 |
| backend.md §11.12 | FR-17-05 |
| backend.md §24.3 Evolution corpus | FR-17-07 |
