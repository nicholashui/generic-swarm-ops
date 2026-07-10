# 06 — Permission-Aware Navigation and UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-06` |
| Source | `frontend.md` — §13 User Roles and Permissions, §6.3 Boundary Rule, permission-aware navigation in §4.1 |
| Related architecture | backend BE-06 RBAC |
| Priority order | 06 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Role-aware UI for suggested roles (Owner, Admin, Developer, Operator, Reviewer, Viewer, Billing Manager, Security Auditor).
- Permission-aware navigation (hide/disable items lacking permission).
- Page-level 403 Access Denied presentation.
- Action-level gating (e.g., Run Workflow, Approve, Invite) as UX only.
- Consumption of backend `/auth/me` (or equivalent) permission payload.

### 1.2 Out of scope
- Server-side RBAC enforcement (BE-06).
- ABAC engine UI beyond displaying backend decisions.
- Implementing permissions in localStorage as authority.

### 1.3 System under specification
Client permission presentation and navigation filtering.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-06-01 | Operators with limited roles | Only see actions they can use; clear denial otherwise. |
| STK-06-02 | Security auditors | UI does not pretend client checks are enforcement. |
| STK-06-03 | Admins | Consistent mapping of backend permissions to controls. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-06-01 | The frontend shall load the authenticated user’s roles and permissions from the backend. |
| FR-06-02 | When the user lacks permission for a navigation item, the frontend shall hide or disable that item according to product rules. |
| FR-06-03 | When the user navigates to a route they cannot access, the frontend shall show Access Denied (403) UX. |
| FR-06-04 | When the user lacks permission for a mutating action, the frontend shall disable or hide the action control. |
| FR-06-05 | If the backend returns 403 for an action the UI allowed, the frontend shall surface the backend denial and not claim success. |
| FR-06-06 | The frontend shall treat permission-aware UI as UX-level only; backend authorization remains final. |
| FR-06-07 | Role labels displayed in UI shall match backend-provided role names without inventing elevated privileges. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-06-01 | Permission payload shall be cached for the session and refreshed on login/org switch. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-06-02 | Client-side permission caches shall not be writable by untrusted page scripts as a means to elevate access. |
| NFR-06-03 | Permission checks in UI shall fail closed (deny/hide) when permission data is missing. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-06-01 | Viewer-like role cannot see admin-only nav items (given backend payload). |
| AC-06-02 | 403 from API shows error state on attempted mutation. |
| AC-06-03 | Documentation states client gates are non-authoritative. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-05 | All domain pages (UX gates only) |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-06-01 | Fixture: mock /auth/me without admin → admin links hidden. | Unit |
| TV-06-02 | Integration: API 403 path displays denial. | Integration |
| TV-06-03 | Review: no “permission enforced only in FE” claims. | Review |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §13 Roles and Permissions | FR-06-01 … FR-06-04, FR-06-07 |
| §6.3 Boundary Rule | FR-06-05 … FR-06-06 |
| §4.1 Permission-aware navigation | FR-06-02 |


