# 07 — Users, Organizations, and Tenancy

| Field | Value |
|-------|-------|
| Spec ID | `BE-07` |
| Source | `backend.md` — §7.3 User and Organization Management, §10.2–10.3, org settings APIs |
| Related architecture | structure.md multi-tenant readiness |
| Priority order | 07 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Organizations, users, teams, roles, permissions, invitations, service accounts, API keys association.
- User lifecycle statuses (active, invited, disabled).
- Organization settings endpoints as provided by backend.

### 1.2 Out of scope
- Full HR identity directory sync.
- Billing calculations.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-07-01 | Org admins | Manage users and invitations. |
| STK-07-02 | Security | Disable users and rotate access. |
| STK-07-03 | Platform | Tenant isolation fields always present. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-07-01 | The backend shall support organization records with status active or disabled. |
| FR-07-02 | The backend shall support user records linked to an organization with status active, invited, or disabled. |
| FR-07-03 | The backend shall support assigning roles/permissions to users within an organization. |
| FR-07-04 | Where invitations are enabled, the backend shall support creating invitations for new users. |
| FR-07-05 | The backend shall support service accounts as non-human principals within an organization. |
| FR-07-06 | The backend shall associate API keys with a principal and organization. |
| FR-07-07 | When a user is disabled, the backend shall reject new authenticated API access for that user. |
| FR-07-08 | The backend shall expose user and organization management endpoints required by the ops console (list/get/update as implemented). |
| FR-07-09 | If the deployment is single-tenant, then the backend shall still persist organization_id on tenant-scoped rows. |
| FR-07-10 | When listing users, the backend shall enforce admin/owner (or equivalent) authorization. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-07-01 | User list for a typical org (<1k users) shall return within 500ms p95 local. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-07-02 | User list endpoints shall not return password hashes or full API key secrets. |
| NFR-07-03 | Only privileged roles may invite users or create service accounts. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-07-01 | Seed organizations and users load after bootstrap. |
| AC-07-02 | Disabled user cannot call protected APIs. |
| AC-07-03 | organization_id present on user entity. |
| AC-07-04 | Non-admin cannot list all users. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-05, BE-06 | All tenant-scoped resources |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-07-01 | Unit: user status transitions. | Automated |
| TV-07-02 | Authz: admin vs operator on user admin routes. | Automated |
| TV-07-03 | Seed credentials login for documented roles. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.3 User/Org | FR-07-01 … FR-07-06 |
| backend.md §10.2–10.3 | FR-07-01 … FR-07-02 |
