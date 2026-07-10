# 05 — Authentication and Session UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-05` |
| Source | `frontend.md` — §16.1–16.3a Public/Login/Register/Accept-invite, Phase 4 Authentication and Session UI, §20 API Integration auth |
| Related architecture | backend BE-05 auth APIs |
| Priority order | 05 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Public root behavior.
- Login page (credentials → backend auth).
- Register page (if enabled).
- Forgot/reset password pages (if backend supports).
- Accept-invite page (`/accept-invite`) calling backend invitation accept API.
- Session storage strategy for tokens/cookies as designed with backend.
- Logout and session expiry UX.
- Display of backend auth errors with `request_id` when present.

### 1.2 Out of scope
- Backend JWT/session validation implementation (BE-05).
- Full user admin (FE-16).
- RBAC matrix UI (FE-06).

### 1.3 System under specification
Authentication and session lifecycle UI.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-05-01 | End users | Sign in and start operating the console. |
| STK-05-02 | Invited users | Accept org invite and join. |
| STK-05-03 | Security | No client-side final auth authority; secure transport. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-05-01 | The frontend shall provide a login page that submits credentials to the backend authentication API. |
| FR-05-02 | On successful login, the frontend shall establish a session usable by subsequent `/api/v1` calls and route the user into `/app`. |
| FR-05-03 | On authentication failure, the frontend shall display the backend error message and `request_id` when provided, without inventing success. |
| FR-05-04 | When registration is enabled, the frontend shall provide a register page that calls the backend register endpoint. |
| FR-05-05 | The frontend shall provide an accept-invite page at `/accept-invite` that calls `POST /users/invitations/accept` (or documented equivalent). |
| FR-05-06 | When the user logs out, the frontend shall clear client session state and call backend logout when available. |
| FR-05-07 | If the session is expired or refresh fails, the frontend shall redirect to login and preserve a safe return path when appropriate. |
| FR-05-08 | The frontend shall not perform final authentication verification as the sole authority; backend remains authoritative. |
| FR-05-09 | Forgot-password and reset-password routes shall exist when backend supports them; otherwise they shall be documented as deferred. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-05-01 | Login submit shall show pending state and disable double-submit. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-05-02 | Passwords shall not be logged to console or analytics. |
| NFR-05-03 | Tokens shall not be placed in query strings or localStorage if httpOnly cookie strategy is selected; follow backend contract. |
| NFR-05-04 | Accept-invite shall not accept tokens solely from untrusted client mutation without backend validation. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-05-01 | Login against live backend succeeds for valid user (ops profile). |
| AC-05-02 | Invalid credentials show error UI. |
| AC-05-03 | Accept-invite form posts to invitation accept API. |
| AC-05-04 | Logout clears session and blocks `/app` until re-login. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-02, FE-07 | FE-04, FE-06, all protected routes |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-05-01 | E1 operator path: login step. | E2E / manual |
| TV-05-02 | Unit: form validation rejects empty credentials. | Unit |
| TV-05-03 | Negative: forged client “authenticated” flag without token still fails API calls. | Integration |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.1–16.3a Auth pages | FR-05-01 … FR-05-05, FR-05-09 |
| §6.2–6.3 Boundary | FR-05-08 |
| §33.3a Auth/invite APIs | FR-05-05, AC-05-03 |
| Phase 4 | AC-05-* |


