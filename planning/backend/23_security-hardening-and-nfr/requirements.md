# 23 — Security Hardening and Cross-Cutting NFRs

| Field | Value |
|-------|-------|
| Spec ID | `BE-23` |
| Source | `backend.md` — §8 Non-Functional Requirements, §16 Security Design, rate limits, injection |
| Related architecture | structure.md §7 security controls |
| Priority order | 23 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Cross-cutting security NFRs: authn/z on protected routes, validation, upload sanitization, secrets, rate limits.
- Prompt injection protections.
- Data access control rules.
- Reliability/scalability/observability maintainability NFRs from §8.

### 1.2 Out of scope
- Full red-team program operations (process), though tests may exist.
- External WAF vendor configuration.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-23-01 | Security team | Defense in depth beyond model alignment. |
| STK-23-02 | Ops | Rate limits and reliability basics. |
| STK-23-03 | All API consumers | Safe defaults. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-23-01 | The backend shall require authentication for protected routes and enforce authorization on every protected resource. |
| FR-23-02 | The backend shall validate all request bodies and sanitize file uploads. |
| FR-23-03 | The backend shall protect secrets and never commit them to source or return them in APIs. |
| FR-23-04 | The backend shall rate limit sensitive endpoints including auth and workflow-write paths. |
| FR-23-05 | When handling retrieved or user content for LLMs, the backend shall treat content as untrusted data, separate instructions from data, and limit blast radius. |
| FR-23-06 | The backend shall assume prompt injection remains possible and shall enforce security outside the LLM with deterministic controls. |
| FR-23-07 | The backend shall apply data access control so users only access authorized org/department resources. |
| FR-23-08 | The backend shall meet reliability expectations for graceful error handling and non-corrupt state on failures. |
| FR-23-09 | The backend shall support horizontal scaling of stateless API processes when shared durable state is in Postgres. |
| FR-23-10 | The backend shall maintain layered architecture for maintainability (routes → services → domain → infrastructure). |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-23-01 | Rate limiter shall not add more than 5ms p95 local overhead when enabled. |
| NFR-23-02 | p95 API latency targets for simple CRUD remain under 300ms local excluding external LLM calls. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-23-03 | Security headers shall be applied on API responses. |
| NFR-23-04 | Dependency and secret scanning are recommended in CI; secrets must not be hardcoded. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-23-01 | Protected route without auth → 401. |
| AC-23-02 | Rate limit triggers on abusive auth attempts in tests or documented behaviour. |
| AC-23-03 | Upload validation rejects disallowed types/sizes where implemented. |
| AC-23-04 | Prompt/tool path treats retrieved content as untrusted in design tests. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-05–BE-06, BE-09 | All endpoints |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-23-01 | Security unit tests: authz, validation. | Automated |
| TV-23-02 | Rate limit tests for sensitive routes. | Automated |
| TV-23-03 | Injection-oriented negative tests for tool/knowledge path. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §8 NFRs | FR-23-01 … FR-23-10 |
| backend.md §16 Security Design | FR-23-05 … FR-23-07 |
