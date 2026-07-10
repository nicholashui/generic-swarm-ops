# 12 — Approvals and Human Gates UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-12` |
| Source | `frontend.md` — §16.14–16.15 Approvals list/detail, Phase 10 Approvals, human gates §33 |
| Related architecture | backend BE-13; structure §4/§10 |
| Priority order | 12 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Approvals list and approval detail pages.
- Approve / reject (and decision notes) actions via backend.
- Human-gate surfaces on run detail linkage.
- Queue prioritization UX for items needing attention.

### 1.2 Out of scope
- Backend policy engine (BE-12/13).
- Silent auto-approve in the client.

### 1.3 System under specification
Human approval gates UI.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-12-01 | Reviewers / operators | Clear approve/reject with context. |
| STK-12-02 | Compliance | Evidence of human decision stays on backend audit. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-12-01 | The frontend shall provide approvals list and detail routes under `/app/approvals`. |
| FR-12-02 | When approval data is loaded, the frontend shall show request context, risk/tier hints when provided, and related run/workflow references. |
| FR-12-03 | When the user explicitly approves or rejects, the frontend shall call backend approval APIs and refresh state. |
| FR-12-04 | If the backend denies the decision, the frontend shall display the error and leave local state consistent with server. |
| FR-12-05 | The frontend shall not auto-approve high-risk actions without an explicit user action. |
| FR-12-06 | When a run has a pending gate, run detail shall deep-link or embed gate actions for that approval. |
| FR-12-07 | If the user lacks approve/reject permission, the frontend shall hide or disable decision controls. |
| FR-12-08 | When the user submits a decision, the frontend shall allow optional decision notes if the backend accepts them. |
| FR-12-09 | If decision submission is in progress, the frontend shall disable double-submit on approve/reject controls. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-12-01 | Approvals list shall load pending items preferentially. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-12-02 | Approval decisions shall require authenticated session and backend authorization. |
| NFR-12-03 | Client shall not forge approval records offline as authoritative. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-12-01 | Pending approval appears in list when backend has one. |
| AC-12-02 | Approve/reject updates status via API. |
| AC-12-03 | No silent auto-approve path in UI. |
| AC-12-04 | In-progress decision disables double-submit. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-06, FE-07, FE-11 | Operator gate completion path |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-12-01 | E1: human gate approve/reject. | E2E / manual |
| TV-12-02 | Unit: decision form requires explicit action. | Unit |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.14–16.15 Approvals | FR-12-01 … FR-12-04, FR-12-07 |
| §33.3 Human gates | FR-12-05 … FR-12-06 |
| Phase 10 | AC-12-* |


