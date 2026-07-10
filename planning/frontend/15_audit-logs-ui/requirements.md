# 15 — Audit Logs UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-15` |
| Source | `frontend.md` — §16.23 Audit Logs Page, Phase 13 (audit portion) |
| Related architecture | backend BE-14 |
| Priority order | 15 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Audit logs list page with filters (time, actor, action, resource) as backend supports.
- Read-only presentation of audit events.
- Deep links to related entities when IDs are present.

### 1.2 Out of scope
- Creating audit events in the frontend (backend only).
- Tamper-evident store implementation.

### 1.3 System under specification
Audit log review UI.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-15-01 | Security auditors | Review who did what. |
| STK-15-02 | Operators | Diagnose recent sensitive actions. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-15-01 | The frontend shall provide an audit logs page under `/app/audit-logs`. |
| FR-15-02 | Audit logs UI shall fetch events from backend audit APIs. |
| FR-15-03 | When filters are provided by the product, the frontend shall pass filter query params to the backend. |
| FR-15-04 | The frontend shall not create, edit, or delete audit events client-side as system of record. |
| FR-15-05 | Each event row shall display actor, action, timestamp, and resource identifiers when returned. |
| FR-15-06 | Permission-aware UI shall restrict audit access for roles without permission. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-15-01 | Audit list shall paginate. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-15-02 | Audit UI shall not allow clients to forge historical events. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-15-01 | Audit page lists backend events or empty state. |
| AC-15-02 | No client write path for audit records. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-04, FE-06, FE-07 | Security / compliance review UX |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-15-01 | Manual: open audit logs as permitted user. | Manual |
| TV-15-02 | Review: no POST audit from FE client modules. | Review |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.23 Audit Logs | FR-15-01 … FR-15-06 |
| §4.2 no audit creation | FR-15-04 |
| Phase 13 (audit) | AC-15-* |


