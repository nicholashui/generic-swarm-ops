# 10 — Workflows Definition UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-10` |
| Source | `frontend.md` — §16.10–16.12 Workflows list/create/detail, Phase 8 Workflows |
| Related architecture | backend BE-10 |
| Priority order | 10 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Workflows list, create workflow, workflow detail pages.
- Run-now entry points from workflow surfaces.
- Display of workflow versions/definitions metadata from backend.
- Frontend validation of create/edit forms.

### 1.2 Out of scope
- Workflow execution engine (BE-11).
- Realtime run timeline (FE-11).
- DNA mutation outside backend sandbox APIs.

### 1.3 System under specification
Workflow definition management UI.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-10-01 | Operators | Create and inspect workflow definitions. |
| STK-10-02 | Developers | Configure workflow structure via backend-supported fields. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-10-01 | The frontend shall provide workflows list, create, and detail views under `/app/workflows`. |
| FR-10-02 | When creating a workflow, the frontend shall validate input and POST to backend workflow APIs. |
| FR-10-03 | Workflow detail shall show definition metadata, version information, and available actions returned/allowed by backend. |
| FR-10-04 | When the user triggers Run Now, the frontend shall request run creation from the backend with a valid payload. |
| FR-10-05 | If run creation fails, the frontend shall show backend errors without claiming a run started. |
| FR-10-06 | The frontend shall not implement workflow execution logic in the browser. |
| FR-10-07 | Permission-aware controls shall gate create/run actions as UX only. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-10-01 | Workflow list load shall not block the entire app shell. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-10-02 | Workflow payloads shall not include secrets; references only as backend allows. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-10-01 | Create workflow form works in ops profile. |
| AC-10-02 | Run now creates a backend run and navigates to run detail when successful. |
| AC-10-03 | Lists show backend workflows. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-04, FE-06, FE-07, FE-09 | FE-11 run detail |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-10-01 | Unit: create form validation. | Unit |
| TV-10-02 | E1: run-now path from workflow. | E2E / manual |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.10–16.12 Workflows | FR-10-01 … FR-10-05 |
| §4.2 no execution logic | FR-10-06 |
| Phase 8 | AC-10-* |


