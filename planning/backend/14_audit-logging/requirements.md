# 14 — Audit Logging

| Field | Value |
|-------|-------|
| Spec ID | `BE-14` |
| Source | `backend.md` — §6.5 Audit Everything, §7.13, §10.14, §11.13 |
| Related architecture | structure.md audit log path |
| Priority order | 14 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Audit events for important actions listed in backend.md §7.13.
- Audit fields and read-only query APIs.
- Correlation with request_id and actor metadata.

### 1.2 Out of scope
- Long-term SIEM product integration (optional).
- Immutable WORM storage vendor specifics.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-14-01 | Auditors | Who did what, when, on which resource. |
| STK-14-02 | Security | Forensics after incidents. |
| STK-14-03 | Operators | Trace failed runs and approvals. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-14-01 | The backend shall generate audit logs for important actions including login, workflow create/update, run start/complete/fail, approval request/decision, knowledge upload/delete, memory access/update, governance rule change, agent tool use, API key create, and permission change. |
| FR-14-02 | Each audit log shall store audit ID, organization ID, actor user ID, actor type, action, resource type, resource ID, request ID, IP address, user agent, before/after state when applicable, metadata, status, and created_at. |
| FR-14-03 | Audit logs shall be read-only through the API (no client update/delete of audit history). |
| FR-14-04 | The backend shall expose search/list and get audit endpoints restricted by audit:read. |
| FR-14-05 | When an important action succeeds or fails, the backend shall write audit status accordingly. |
| FR-14-06 | Audit writes shall not be skippable by clients via request parameters. |
| FR-14-07 | Sensitive audit metadata shall avoid storing secrets and raw credentials. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-14-01 | Audit write shall not add more than 50ms p95 local to critical path under normal load. |
| NFR-14-02 | Audit search shall support filtering by time, actor, action, and resource. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-14-03 | Only authorized roles may read audit logs. |
| NFR-14-04 | Audit storage integrity shall be protected from ordinary user APIs. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-14-01 | Starting a run creates audit event. |
| AC-14-02 | Approval decision creates audit event. |
| AC-14-03 | Audit update/delete endpoints are absent or forbidden. |
| AC-14-04 | Viewer without audit:read cannot list audits. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-03, BE-05 | Compliance, FE audit views |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-14-01 | Integration: action → audit present. | Automated |
| TV-14-02 | Authz on audit read. | Automated |
| TV-14-03 | Review: no secrets in audit samples. | Review |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §6.5 / §7.13 | FR-14-01 … FR-14-02 |
| backend.md §11.13 | FR-14-03 … FR-14-04 |
