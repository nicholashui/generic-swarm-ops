# 20 — Security, Performance, Testing, and Ops Profile

| Field | Value |
|-------|-------|
| Spec ID | `FE-20` |
| Source | `frontend.md` — §24 Security, §25 Performance, §26 Observability, §27 Testing, §28 Phase 14, §30–31 Acceptance/DoD, §33 non-goals & ops profile |
| Related architecture | E1 path; mark ~100 evidence |
| Priority order | 20 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Frontend security requirements (§24): XSS hygiene, no secrets in client, CSRF/credentials per design, dependency hygiene notes.
- Performance requirements (§25) for navigation and list responsiveness.
- Observability hooks (§26): client error reporting hooks if present; correlation with request_id.
- Testing requirements (§27): unit, lint, typecheck, build; E2E smoke/E1 path as practical.
- Phase 14 quality/security/release gates.
- Acceptance criteria and definition of done for pages (§30–31).
- Ops profile proof: `NEXT_PUBLIC_DEMO_MODE=false` + live backend + Postgres.
- Explicit non-goals for product bar (§33.5).

### 1.2 Out of scope
- Always-on Playwright CI with permanent servers (non-goal if servers down).
- Backend security hardening (BE-23).
- Full load test suite.

### 1.3 System under specification
Cross-cutting quality, security, testing, and operator-path proof for the frontend.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-20-01 | Release managers | Clear DoD for frontend ship. |
| STK-20-02 | Security | Client-side threat mitigations documented and tested at smoke level. |
| STK-20-03 | Operators | E1 path works on ops profile. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-20-01 | The frontend shall enforce security hygiene: no provider secrets in client bundles, safe rendering of untrusted text, and auth credentials handled per backend contract. |
| FR-20-02 | The frontend shall meet performance expectations for interactive ops use (responsive navigation, non-blocking lists for MVP data sizes). |
| FR-20-03 | The frontend shall provide automated lint, typecheck, unit tests, and production build as quality gates. |
| FR-20-04 | When servers are available, the frontend shall support an operator E1 path: login → dashboard → run → gate → improve as applicable. |
| FR-20-05 | The ops profile shall run with `NEXT_PUBLIC_DEMO_MODE=false` against a live backend and Postgres. |
| FR-20-06 | Each page DoD shall include: routes, permission awareness, loading/empty/error, API wiring or documented stub, and no charter violations. |
| FR-20-07 | Product-bar non-goals (always-on UI CI servers, full graph explorer, live CRM/email/billing admin, host self-rewrite UI, client-only authz) shall not be treated as missing requirements for mark ~100. |
| FR-20-08 | Client observability shall preserve request_id on failures for support correlation when available. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-20-01 | Production build shall complete in CI-reasonable time for the repo’s frontend package. |
| NFR-20-02 | Bundle shall code-split heavy client widgets (run timeline, command palette) where practical. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-20-03 | Dependency vulnerabilities in FE lockfile shall be reviewed before release claims. |
| NFR-20-04 | DEMO_MODE shall not be required for security; live mode must still enforce backend auth. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-20-01 | `pnpm lint`, `pnpm typecheck`, unit tests, and `pnpm build` green. |
| AC-20-02 | Ops profile documented and usable for E1. |
| AC-20-03 | Security checklist items in §24 addressed or explicitly deferred with owner. |
| AC-20-04 | Non-goals list matches frontend.md §33.5. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-01–FE-19 | Release gate / product-bar proof |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-20-01 | CI: lint + typecheck + unit + build. | Automated |
| TV-20-02 | Manual/E2E: E1 operator path when stack up. | E2E |
| TV-20-03 | Review: secrets scan on frontend env samples. | Review |
| TV-20-04 | Document review: §30–31 acceptance mapped to FE specs. | Traceability |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §24 Security | FR-20-01, NFR-20-03 … NFR-20-04 |
| §25 Performance | FR-20-02, NFR-20-01 … NFR-20-02 |
| §26 Observability | FR-20-08 |
| §27 Testing | FR-20-03 |
| §28 Phase 14 / §30–31 | FR-20-06, AC-20-* |
| §33.5–33.7 | FR-20-04 … FR-20-05, FR-20-07 |


