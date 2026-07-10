# 14 — Evaluations and Processes UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-14` |
| Source | `frontend.md` — §16.20–16.22 Evaluations/Processes pages, Phase 12 |
| Related architecture | backend BE-17, BE-18 |
| Priority order | 14 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Evaluations list/detail and evaluation run views.
- Processes list/detail for process intelligence artifacts.
- Display of quality metrics and PI summaries returned by backend.
- Links from quality nav group.

### 1.2 Out of scope
- Running eval engines in the browser.
- Full process mining product beyond backend artifacts.

### 1.3 System under specification
Evaluations and process intelligence UI.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-14-01 | Quality operators | Inspect evaluation outcomes. |
| STK-14-02 | Process owners | View process intelligence summaries. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-14-01 | The frontend shall provide evaluations list and detail routes under `/app/evaluations`. |
| FR-14-02 | The frontend shall provide processes list and detail routes under `/app/processes`. |
| FR-14-03 | Evaluation views shall display scores, statuses, and artifacts metadata returned by backend. |
| FR-14-04 | Process views shall display PI summaries/artifacts/events as returned by backend. |
| FR-14-05 | When starting an evaluation is supported, the frontend shall call backend evaluation APIs rather than computing scores locally. |
| FR-14-06 | The frontend shall not claim eval pass/fail without backend results. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-14-01 | Large eval result payloads shall be paginated or truncated in UI with expand options. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-14-02 | Eval/process views shall respect permission-aware access. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-14-01 | Evaluations and processes pages accessible from Quality nav. |
| AC-14-02 | Detail pages render backend payloads or empty states. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-04, FE-06, FE-07 | Quality nav group |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-14-01 | Manual: navigate Quality group. | Manual |
| TV-14-02 | Unit: empty state components. | Unit |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.20–16.22 Evals/Processes | FR-14-01 … FR-14-06 |
| Phase 12 | AC-14-* |


