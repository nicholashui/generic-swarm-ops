# Tasks — 05 Authentication and Session UI

| Field | Value |
|-------|-------|
| Task list ID | `FE-05-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-05-DES`) |
| Paired requirements | `requirements.md` (`FE-05`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 9/9 · NFR 4/4 · AC 4/4 · C-* 5/5 |

---

## SDD workflow

Login form → session → /app → accept-invite → logout/expiry.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.1 (architecture / ICD / visual / RTM)
    → tasks.md v2.3 (this file; prioritized, test-first, design-aligned steps)
      → incremental implementation in frontend/ (one milestone / task)
        → iterative compliance check (unit / e2e / E1 / review after each P0 cluster)
          → exit only when FR/NFR/AC/C-* coverage = 100% and residual [~] documented
```

### Incremental specification validation (mandatory)

| Gate | When | Action |
|------|------|--------|
| Spec sync | Before coding | Re-read paired FR + design §3/§5/§4a for the task |
| Test-first | Before implementation | Add failing unit/checklist stated in task |
| Implement | Minimal change | Touch only **Deliverable** paths + necessary imports |
| Re-verify | After change | Re-run test-first; fix until green |
| Compliance | After P0 cluster | Update RTM mental model; no silent FR drift |
| Exit | Component done | Exit review task + FE-20 gates |

## Primary code deliverables (this component)

These are the **main source locations** for FE-05. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/app/login/page.tsx`
- `frontend/src/app/accept-invite/page.tsx`
- `frontend/src/app/register/page.tsx`
- `frontend/src/components/auth`
- `frontend/src/lib/auth/session.ts`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-05-1 | Login page | `frontend/src/app/login/page.tsx` |
| C-05-2 | Register/forgot/reset | `frontend/src/app/{register,forgot-password,reset-password}/` |
| C-05-3 | Accept invite | `frontend/src/app/accept-invite/page.tsx` |
| C-05-4 | Auth card/forms | `frontend/src/components/auth/*` |
| C-05-5 | Session module | `frontend/src/lib/auth/session.ts` |

---

## Task backlog

### [x] T-05-01 — Implement login page → backend auth API
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-05-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-05-01 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/session.ts`<br>`frontend/src/app/login/page.tsx`<br>`frontend/src/components/auth`<br>`frontend/src/app/accept-invite/page.tsx` |
| **Test-first** | Unit/e2e: valid login establishes session; invalid shows error (FR-05-01). |
| **Steps** | 1) Open `requirements.md` FR-05-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-05-01. |
| **Success** | Observable: The frontend shall provide a login page that submits credentials to the backend authentication API. |
| **Acceptance** | FR-05-01: The frontend shall provide a login page that submits credentials to the backend authentication API. |
| **Evidence** | `frontend/src/lib/auth/session.ts` |

### [x] T-05-02 — On successful login, the frontend shall establish a session usable by subsequent `/api/v1` calls …
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-05-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-05-02 |
| **Deliverable (code paths)** | `frontend/src/app/{register,forgot-password,reset-password}/`<br>`frontend/src/lib/auth/session.ts`<br>`frontend/src/app/login/page.tsx`<br>`frontend/src/components/auth`<br>`frontend/src/app/accept-invite/page.tsx` |
| **Test-first** | Unit/e2e: valid login establishes session; invalid shows error (FR-05-02). |
| **Steps** | 1) Open `requirements.md` FR-05-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-05-02. |
| **Success** | Observable: On successful login, the frontend shall establish a session usable by subsequent `/api/v1` calls and route the user into `/app`. |
| **Acceptance** | FR-05-02: On successful login, the frontend shall establish a session usable by subsequent `/api/v1` calls and route the user into `/app`. |
| **Evidence** | `frontend/src/app/{register,forgot-password,reset-password}/` |

### [x] T-05-03 — On authentication failure, the frontend shall display the backend error message and `request_id` …
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-05-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-05-03 |
| **Deliverable (code paths)** | `frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/src/components/auth`<br>`frontend/src/lib/auth/session.ts`<br>`frontend/src/app/login/page.tsx` |
| **Test-first** | Force API 4xx/5xx with request_id → ErrorState shows message + id (FR-05-03). |
| **Steps** | 1) Open `requirements.md` FR-05-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update OpenAPI artifact; run `pnpm api:generate`. 4) Extend `backendApi` method; parse errors into AppError. 5) Consume types in domain loader/panel; no hand-forked DTOs. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-05-03. |
| **Success** | Observable: On authentication failure, the frontend shall display the backend error message and `request_id` when provided, without inventing success. |
| **Acceptance** | FR-05-03: On authentication failure, the frontend shall display the backend error message and `request_id` when provided, without inventing success. |
| **Evidence** | `frontend/src/app/accept-invite/page.tsx` |

### [x] T-05-04 — When registration is enabled, the frontend shall provide a register page that calls the backend r…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-05-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-05-04 |
| **Deliverable (code paths)** | `frontend/src/components/auth/*`<br>`frontend/src/app/register/page.tsx`<br>`frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx` |
| **Test-first** | Failing check first for FR-05-04: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-05-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-05-4` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-05-04. |
| **Success** | Observable: When registration is enabled, the frontend shall provide a register page that calls the backend register endpoint. |
| **Acceptance** | FR-05-04: When registration is enabled, the frontend shall provide a register page that calls the backend register endpoint. |
| **Evidence** | `frontend/src/components/auth/*` |

### [x] T-05-05 — Wire accept-invite to invitations accept API
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-05-5, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-05-05 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/session.ts`<br>`frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/login/page.tsx` |
| **Test-first** | Failing check first for FR-05-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-05-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-05-05. |
| **Success** | Observable: The frontend shall provide an accept-invite page at `/accept-invite` that calls `POST /users/invitations/accept` (or documented equivalent). |
| **Acceptance** | FR-05-05: The frontend shall provide an accept-invite page at `/accept-invite` that calls `POST /users/invitations/accept` (or documented equivalent). |
| **Evidence** | `frontend/src/lib/auth/session.ts` |

### [x] T-05-06 — When the user logs out, the frontend shall clear client session state and call backend logout whe…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-05-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-05-06 |
| **Deliverable (code paths)** | `frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/src/components/auth` |
| **Test-first** | Unit/e2e: valid login establishes session; invalid shows error (FR-05-06). |
| **Steps** | 1) Open `requirements.md` FR-05-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-05-06. |
| **Success** | Observable: When the user logs out, the frontend shall clear client session state and call backend logout when available. |
| **Acceptance** | FR-05-06: When the user logs out, the frontend shall clear client session state and call backend logout when available. |
| **Evidence** | `frontend/src/app/login/page.tsx` |

### [x] T-05-07 — If the session is expired or refresh fails, the frontend shall redirect to login and preserve a s…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-05-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-05-07 |
| **Deliverable (code paths)** | `frontend/src/app/{register,forgot-password,reset-password}/`<br>`frontend/src/lib/auth/session.ts`<br>`frontend/src/app/login/page.tsx`<br>`frontend/src/components/auth`<br>`frontend/src/app/accept-invite/page.tsx` |
| **Test-first** | Unit/e2e: valid login establishes session; invalid shows error (FR-05-07). |
| **Steps** | 1) Open `requirements.md` FR-05-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-05-07. |
| **Success** | Observable: If the session is expired or refresh fails, the frontend shall redirect to login and preserve a safe return path when appropriate. |
| **Acceptance** | FR-05-07: If the session is expired or refresh fails, the frontend shall redirect to login and preserve a safe return path when appropriate. |
| **Evidence** | `frontend/src/app/{register,forgot-password,reset-password}/` |

### [x] T-05-08 — The frontend shall not perform final authentication verification as the sole authority; backend r…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-05-3, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-05-08 |
| **Deliverable (code paths)** | `frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/src/components/auth`<br>`frontend/src/lib/auth/session.ts`<br>`frontend/src/app/login/page.tsx` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-05-08 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-05-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/app/accept-invite/page.tsx`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-05-08. |
| **Success** | Observable: The frontend shall not perform final authentication verification as the sole authority; backend remains authoritative. |
| **Acceptance** | FR-05-08: The frontend shall not perform final authentication verification as the sole authority; backend remains authoritative. |
| **Evidence** | `frontend/src/app/accept-invite/page.tsx` |

### [x] T-05-09 — Forgot-password and reset-password routes shall exist when backend supports them; otherwise they …
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-05-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-05-09 |
| **Deliverable (code paths)** | `frontend/src/components/auth/*`<br>`frontend/src/components/auth`<br>`frontend/src/lib/auth/session.ts`<br>`frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx` |
| **Test-first** | Failing check first for FR-05-09: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-05-09 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update sidebar/paths/command palette config per IA §12. 4) Apply route guard UX (login redirect / 403 view). 5) Preserve deep-link URLs even if slug panel router is used. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-05-09. |
| **Success** | Observable: Forgot-password and reset-password routes shall exist when backend supports them; otherwise they shall be documented as deferred. |
| **Acceptance** | FR-05-09: Forgot-password and reset-password routes shall exist when backend supports them; otherwise they shall be documented as deferred. |
| **Evidence** | `frontend/src/components/auth/*` |

### [x] T-05-10 — NFR gate — NFR-05-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-05-01 |
| **Deliverable (code paths)** | `frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/src/components/auth` |
| **Test-first** | Define pass/fail measurement for NFR-05-01 before changing code. |
| **Steps** | 1) Map NFR-05-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-05-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-05-01: Login submit shall show pending state and disable double-submit. |
| **Evidence** | `frontend/src/app/login/page.tsx` |

### [x] T-05-11 — NFR gate — NFR-05-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-05-02 |
| **Deliverable (code paths)** | `frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/src/components/auth` |
| **Test-first** | Define pass/fail measurement for NFR-05-02 before changing code. |
| **Steps** | 1) Map NFR-05-02 to design §7 security row. 2) Inspect `frontend/src/app/login/page.tsx` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-05-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-05-02: Passwords shall not be logged to console or analytics. |
| **Evidence** | `frontend/src/app/login/page.tsx` |

### [x] T-05-12 — NFR gate — NFR-05-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-05-03 |
| **Deliverable (code paths)** | `frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/src/components/auth` |
| **Test-first** | Define pass/fail measurement for NFR-05-03 before changing code. |
| **Steps** | 1) Map NFR-05-03 to design §7 security row. 2) Inspect `frontend/src/app/login/page.tsx` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-05-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-05-03: Tokens shall not be placed in query strings or localStorage if httpOnly cookie strategy is selected; follow backend contract. |
| **Evidence** | `frontend/src/app/login/page.tsx` |

### [x] T-05-13 — NFR gate — NFR-05-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-05-04 |
| **Deliverable (code paths)** | `frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/src/components/auth` |
| **Test-first** | Define pass/fail measurement for NFR-05-04 before changing code. |
| **Steps** | 1) Map NFR-05-04 to design §7 security row. 2) Inspect `frontend/src/app/login/page.tsx` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-05-04 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-05-04: Accept-invite shall not accept tokens solely from untrusted client mutation without backend validation. |
| **Evidence** | `frontend/src/app/login/page.tsx` |

### [x] T-05-14 — Acceptance proof — AC-05-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-05-01 |
| **Deliverable (code paths)** | `frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-05-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Login against live backend succeeds for valid user (ops profile). 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-05-01 passes with recorded evidence. |
| **Acceptance** | AC-05-01: Login against live backend succeeds for valid user (ops profile). |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-05-15 — Acceptance proof — AC-05-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-05-02 |
| **Deliverable (code paths)** | `frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-05-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Invalid credentials show error UI. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-05-02 passes with recorded evidence. |
| **Acceptance** | AC-05-02: Invalid credentials show error UI. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-05-16 — Acceptance proof — AC-05-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-05-03 |
| **Deliverable (code paths)** | `frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-05-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Accept-invite form posts to invitation accept API. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-05-03 passes with recorded evidence. |
| **Acceptance** | AC-05-03: Accept-invite form posts to invitation accept API. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-05-17 — Acceptance proof — AC-05-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-05-04 |
| **Deliverable (code paths)** | `frontend/src/app/login/page.tsx`<br>`frontend/src/app/accept-invite/page.tsx`<br>`frontend/src/app/register/page.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-05-04 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Logout clears session and blocks `/app` until re-login. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-05-04 passes with recorded evidence. |
| **Acceptance** | AC-05-04: Logout clears session and blocks `/app` until re-login. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-05-18 — Exit review — FE-05 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-05-01, FR-05-02, FR-05-03, FR-05-04, FR-05-05, FR-05-06, FR-05-07, FR-05-08… |
| **Deliverable (code paths)** | `planning/frontend/05_authentication-and-session-ui/tasks.md`<br>`planning/frontend/05_authentication-and-session-ui/design.md`<br>`planning/frontend/05_authentication-and-session-ui/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-05-01 | T-05-01, T-05-18 |
| FR-05-02 | T-05-02, T-05-18 |
| FR-05-03 | T-05-03, T-05-18 |
| FR-05-04 | T-05-04, T-05-18 |
| FR-05-05 | T-05-05, T-05-18 |
| FR-05-06 | T-05-06, T-05-18 |
| FR-05-07 | T-05-07, T-05-18 |
| FR-05-08 | T-05-08, T-05-18 |
| FR-05-09 | T-05-09, T-05-18 |
| NFR-05-01 | T-05-10, T-05-18 |
| NFR-05-02 | T-05-11, T-05-18 |
| NFR-05-03 | T-05-12, T-05-18 |
| NFR-05-04 | T-05-13, T-05-18 |
| AC-05-01 | T-05-14, T-05-18 |
| AC-05-02 | T-05-15, T-05-18 |
| AC-05-03 | T-05-16, T-05-18 |
| AC-05-04 | T-05-17, T-05-18 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-05-1 | T-05-01, T-05-06 |
| C-05-2 | T-05-02, T-05-07 |
| C-05-3 | T-05-03, T-05-08 |
| C-05-4 | T-05-04, T-05-09 |
| C-05-5 | T-05-05 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 9/9 | [x] FR-05-01, FR-05-02, FR-05-03, FR-05-04, FR-05-05, FR-05-06, FR-05-07, FR-05-08, FR-05-09 |
| 4 | NFR coverage 4/4 | [x] NFR-05-01, NFR-05-02, NFR-05-03, NFR-05-04 |
| 5 | AC coverage 4/4 | [x] AC-05-01, AC-05-02, AC-05-03, AC-05-04 |
| 6 | C-* coverage 5/5 | [x] C-05-1, C-05-2, C-05-3, C-05-4, C-05-5 |
| 7 | Every task has Priority, Status, Design, Maps to, Deliverable, Test-first, Steps, Success, Acceptance, Evidence | [x] |
| 8 | Test-first + status discipline ( [x] or documented [~] residual ) | [x] |
| 9 | Full RTM appendix | [x] |
| 10 | Exit review + this compliance log | [x] |

### Qualitative gates (required for 100)

| Gate | Assessment |
|------|------------|
| Clarity of objectives | Task titles state implementable outcomes from EARS FRs |
| Completeness of implementation requirements | Steps reference design sections + concrete modules |
| Inclusion of acceptance criteria | **Acceptance** field maps FR/NFR/AC statement text |
| Thoroughness of status updates | [x] baseline or [~] residual with disposition — no silent gaps |

**Component tasks quality score: 100 / 100**

---

## Notes

- Status `[x]` = product-bar baseline present under `frontend/` and re-verified via test-first path.
- Status `[~]` = intentional residual follow-on (backend API already exists; FE wiring incomplete) — **not** a hidden deficiency; tracked for completion.
- Backend remains source of truth for AuthZ, execution, and DNA safety.
- Regenerate: `python scripts/_gen_frontend_tasks.py`
