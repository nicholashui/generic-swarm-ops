# 13 — Human Approval Gates

| Field | Value |
|-------|-------|
| Spec ID | `BE-13` |
| Source | `backend.md` — §6.4 HITL, §7.9 approvals, §11.8 Approval Endpoints |
| Related architecture | structure.md §4 human gates; STRUCT-12 |
| Priority order | 13 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Approval request entity and statuses pending/approved/rejected/expired/cancelled.
- Approve/reject/reassign/decision endpoints.
- Integration with run waiting_for_approval state.
- Decision reason capture.

### 1.2 Out of scope
- Email notification productization (optional).
- Frontend approval inbox UX details.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-13-01 | Reviewers | Clear queue of pending approvals. |
| STK-13-02 | Operators | Runs resume only after decision. |
| STK-13-03 | Auditors | Decisions and reasons retained. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-13-01 | When human approval is required, the backend shall create an approval request linked to workflow_run and step when applicable. |
| FR-13-02 | Approval requests shall store approval ID, run ID, step ID, requested action, risk level, requester, assigned reviewer, decision, decision reason, created_at, and decided_at. |
| FR-13-03 | The backend shall support approval statuses pending, approved, rejected, expired, and cancelled. |
| FR-13-04 | When a reviewer approves, the backend shall record decision reason and allow the run to continue if still valid. |
| FR-13-05 | When a reviewer rejects, the backend shall record decision reason and stop or fail the gated action according to policy. |
| FR-13-06 | The backend shall support reassigning reviewers when permitted. |
| FR-13-07 | The backend shall expose list/get/approve/reject/reassign/decision endpoints. |
| FR-13-08 | While an approval is pending for a required gate, the backend shall not execute the gated irreversible action. |
| FR-13-09 | Only principals with approvals:approve or approvals:reject (or equivalent) may decide approvals. |
| FR-13-10 | Approval decisions shall generate audit events. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-13-01 | Approval decision API p95 under 300ms local excluding resume execution time. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-13-02 | Users shall not approve their own requests when policy forbids self-approval. |
| NFR-13-03 | Approval tokens or IDs shall not grant access outside assigned org. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-13-01 | Gated flagship run creates pending approval. |
| AC-13-02 | Approve resumes run path. |
| AC-13-03 | Reject prevents completion of gated action. |
| AC-13-04 | Decision reason required/stored. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-12, BE-11 | BE-14, BE-24 E1 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-13-01 | Integration: approve path. | Automated |
| TV-13-02 | Integration: reject path. | Automated |
| TV-13-03 | E1: human gate segment. | E2E |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §6.4 HITL | FR-13-01, FR-13-08 |
| backend.md §7.9 Approvals | FR-13-02 … FR-13-06 |
| backend.md §11.8 | FR-13-07 |
