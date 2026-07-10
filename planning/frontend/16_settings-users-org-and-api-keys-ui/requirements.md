# 16 — Settings, Users, Organization, and API Keys UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-16` |
| Source | `frontend.md` — §16.24–16.28 Settings suite, Phase 13 Settings, §33.3a users/orgs/invitations |
| Related architecture | backend BE-07 |
| Priority order | 16 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Settings hub and subpages: organization, users, roles (as supported), billing placeholder, API keys, security, integrations, profile.
- User management list/invite/disable UX calling BE-07 APIs.
- Organization settings GET/PATCH.
- API key management UI via backend key endpoints.
- Security settings presentation.
- Accept-invite linkage for invitations created from settings.

### 1.2 Out of scope
- Billing calculation engines.
- Backend tenancy enforcement (BE-07).
- Live external billing SaaS admin consoles (§33.5 non-goal).

### 1.3 System under specification
Organization administration and settings UI.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-16-01 | Org admins | Manage users, org profile, API keys. |
| STK-16-02 | Billing managers | See billing placeholder or backend-supported billing page. |
| STK-16-03 | Security admins | View/configure security settings exposed by backend. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-16-01 | The frontend shall provide a settings hub under `/app/settings` with sub-routes for organization, users, roles, billing, API keys, security, integrations, and profile as specified. |
| FR-16-02 | User management UI shall list users via backend and support invite/disable/update actions through BE-07 APIs when permitted. |
| FR-16-03 | Organization settings UI shall load and save organization fields via GET/PATCH organization APIs. |
| FR-16-04 | API keys UI shall create/list/revoke keys only through backend auth/API key endpoints. |
| FR-16-05 | Billing page may be a placeholder if backend lacks billing; it shall not invent charges. |
| FR-16-06 | Security settings UI shall display backend-provided security configuration and not store secrets in browser code. |
| FR-16-07 | Invitation creation from settings shall use backend invitation APIs; accept flow remains on `/accept-invite` (FE-05). |
| FR-16-08 | Permission-aware UI shall restrict admin settings to authorized roles. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-16-01 | Settings forms shall avoid full app remounts on save success. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-16-02 | Newly created API key secrets shall be shown once (if backend returns plaintext once) and not re-fetchable from FE cache. |
| NFR-16-03 | User disable/invite actions require confirmation where destructive. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-16-01 | Settings nav links resolve to settings surfaces. |
| AC-16-02 | Users invite/list wired to backend invitations/users APIs (or documented gap). |
| AC-16-03 | Organization save calls PATCH when implemented. |
| AC-16-04 | API keys page uses backend endpoints. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-04, FE-05, FE-06, FE-07 | Admin lifecycle UX |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-16-01 | Manual: admin opens settings users/org. | Manual |
| TV-16-02 | Integration: invite POST path. | Integration |
| TV-16-03 | Review: no billing math in FE. | Review |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.24–16.28 Settings suite | FR-16-01 … FR-16-08 |
| §33.3a Users/Orgs/Invitations | FR-16-02 … FR-16-03, FR-16-07 |
| Phase 13 Settings | AC-16-* |


