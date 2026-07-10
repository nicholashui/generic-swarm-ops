# 05 — Authentication and Identity

| Field | Value |
|-------|-------|
| Spec ID | `BE-05` |
| Source | `backend.md` — §7.1 Authentication, §11.4 Authentication Endpoints, §16 security auth |
| Related architecture | structure.md security layer |
| Priority order | 05 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Login, logout, token refresh, me profile.
- Password reset when password auth is used.
- API key create/list/revoke for machine clients.
- JWT access/refresh model; optional SSO/OAuth readiness.
- Auth rate limiting on sensitive endpoints.

### 1.2 Out of scope
- Full enterprise IdP productization (optional later).
- Frontend login page UI.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-05-01 | End users | Secure login and session lifecycle. |
| STK-05-02 | Integrations | API keys for machine access. |
| STK-05-03 | Security | Token hygiene and rate limits. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-05-01 | The backend shall support authenticated users via login issuing access credentials. |
| FR-05-02 | When a user logs in with valid credentials, the backend shall return access token material suitable for subsequent API calls. |
| FR-05-03 | When a user logs out, the backend shall invalidate or reject further use of the session/refresh material according to the chosen token strategy. |
| FR-05-04 | When a valid refresh token is presented, the backend shall issue a new access token. |
| FR-05-05 | Where password authentication is used, the backend shall support password reset flows. |
| FR-05-06 | The backend shall support API key creation, listing, and revocation for machine clients. |
| FR-05-07 | When an API key is used, the backend shall authenticate the caller as the associated principal with constrained permissions. |
| FR-05-08 | The backend shall expose a current-user endpoint (e.g. GET /auth/me) returning identity and role claims needed by clients. |
| FR-05-09 | If authentication credentials are invalid or expired, then the backend shall reject the request with an authentication error. |
| FR-05-10 | While SSO/OAuth is optional, the backend design shall not preclude OAuth2/OIDC compatibility. |
| FR-05-11 | When sensitive auth endpoints are called repeatedly, the backend shall apply rate limiting. |
| FR-05-12 | Passwords shall be stored only as secure hashes, never as plaintext. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-05-01 | Login handler p95 shall remain under 500ms excluding external IdP latency. |
| NFR-05-02 | Token validation on protected routes shall add minimal overhead (target under 10ms local). |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-05-03 | JWT secrets and API key secrets shall not be logged. |
| NFR-05-04 | API keys shall be shown in full only at creation time and masked thereafter. |
| NFR-05-05 | Auth endpoints shall be rate limited to reduce credential stuffing risk. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-05-01 | POST login with seed users returns usable token. |
| AC-05-02 | Protected route without token returns 401. |
| AC-05-03 | API key can be created and used, then revoked. |
| AC-05-04 | Password hashes are not returned by /me. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-03, BE-04 | BE-06, BE-07, all protected APIs |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-05-01 | Unit/e2e: login → /me. | Automated |
| TV-05-02 | Negative: bad password → 401. | Automated |
| TV-05-03 | API key revoke blocks subsequent use. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.1 Authentication | FR-05-01 … FR-05-10 |
| backend.md §11.4 Auth endpoints | FR-05-01 … FR-05-08 |
| backend.md §8.1 / rate limit | FR-05-11, NFR-05-05 |
