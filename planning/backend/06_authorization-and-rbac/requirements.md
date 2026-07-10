# 06 — Authorization and RBAC

| Field | Value |
|-------|-------|
| Spec ID | `BE-06` |
| Source | `backend.md` — §7.2 Authorization, permission groups, future ABAC notes |
| Related architecture | structure.md §6–7 permission scopes |
| Priority order | 06 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Role-based access control roles: Owner, Admin, Manager, Operator, Reviewer, Viewer, ServiceAccount.
- Permission strings for agents, workflows, runs, knowledge, memory, governance, approvals, audit, evaluations, settings.
- Enforcement on every protected resource.
- Design readiness for future ABAC rules.

### 1.2 Out of scope
- Full ABAC policy language product.
- Frontend permission matrix UI.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-06-01 | Admins | Assign roles with least privilege. |
| STK-06-02 | Auditors | Permission checks are consistent and logged on failures. |
| STK-06-03 | Developers | Declarative permission dependencies on routes. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-06-01 | The backend shall implement role-based access control for protected operations. |
| FR-06-02 | The backend shall support roles including Owner, Admin, Manager, Operator, Reviewer, Viewer, and ServiceAccount (or equivalent mapped set). |
| FR-06-03 | When a caller lacks a required permission, the backend shall deny the operation with an authorization error. |
| FR-06-04 | The backend shall enforce permissions for agents:read/create/update/delete as applicable to agent routes. |
| FR-06-05 | The backend shall enforce permissions for workflows:read/create/update/run as applicable to workflow routes. |
| FR-06-06 | The backend shall enforce permissions for workflow_runs:read/cancel as applicable to run routes. |
| FR-06-07 | The backend shall enforce permissions for knowledge:read/write, memory:read/write, governance:read/update, approvals:read/approve/reject, audit:read, evaluations:read, and settings:update on corresponding resources. |
| FR-06-08 | While ABAC is not fully required for product bar, the authorization design shall allow future rules such as organization match and max risk level. |
| FR-06-09 | When authorization fails, the backend shall not leak whether a resource exists beyond what policy allows. |
| FR-06-10 | Service accounts and API keys shall be constrained by the same permission model as interactive users. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-06-01 | Permission checks shall be deterministic and not require external network calls. |
| NFR-06-02 | Permission evaluation p95 shall remain under 5ms local for in-memory role maps. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-06-03 | Authorization shall be enforced server-side on every protected resource; client claims alone are insufficient. |
| NFR-06-04 | Privilege escalation paths (self-assign Owner) shall be restricted to appropriately privileged roles. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-06-01 | Viewer cannot create workflows when permission matrix forbids it. |
| AC-06-02 | Operator can run workflows if granted workflows:run. |
| AC-06-03 | Reviewer can approve when granted approvals:approve. |
| AC-06-04 | Cross-role matrix unit tests cover deny paths. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-05 | All resource APIs |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-06-01 | Unit: permission matrix table-driven tests. | Automated |
| TV-06-02 | Integration: role tokens against sample routes. | Automated |
| TV-06-03 | Negative: missing permission → 403. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.2 Authorization | FR-06-01 … FR-06-08 |
| backend.md §6.2 Secure by Default | FR-06-03, NFR-06-03 |
