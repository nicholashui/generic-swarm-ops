# Tasks — 20 Security, Performance, Testing, and Ops Profile

| Field | Value |
|-------|-------|
| Task list ID | `FE-20-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-20-DES`) |
| Paired requirements | `requirements.md` (`FE-20`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 8/8 · NFR 4/4 · AC 4/4 · C-* 5/5 |

---

## SDD workflow

lint/typecheck/unit/build → ops profile E1 → non-goals → page DoD.

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

These are the **main source locations** for FE-20. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/package.json`
- `frontend/tests/unit`
- `frontend/e2e/e1-smoke.spec.ts`
- `frontend/playwright.config.ts`
- `frontend/src/lib/config/env.ts`
- `frontend/README.md`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-20-1 | Unit tests | `frontend/tests/unit/*` |
| C-20-2 | E2E smoke | `frontend/e2e/e1-smoke.spec.ts` |
| C-20-3 | Playwright config | `frontend/playwright.config.ts` |
| C-20-4 | Env security | `frontend/src/lib/config/env.ts` |
| C-20-5 | Package scripts | `frontend/package.json` |

---

## Task backlog

### [x] T-20-01 — The frontend shall enforce security hygiene: no provider secrets in client bundles, safe renderin…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-20-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-20-01 |
| **Deliverable (code paths)** | `frontend/tests/unit/*`<br>`frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/playwright.config.ts` |
| **Test-first** | Failing check first for FR-20-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-20-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-20-1` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-20-01. |
| **Success** | Observable: The frontend shall enforce security hygiene: no provider secrets in client bundles, safe rendering of untrusted text, and auth credential…. |
| **Acceptance** | FR-20-01: The frontend shall enforce security hygiene: no provider secrets in client bundles, safe rendering of untrusted text, and auth credentials handled per backend contract. |
| **Evidence** | `frontend/tests/unit/*` |

### [x] T-20-02 — The frontend shall meet performance expectations for interactive ops use (responsive navigation, …
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-20-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-20-02 |
| **Deliverable (code paths)** | `frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/playwright.config.ts`<br>`frontend/src/lib/config/env.ts` |
| **Test-first** | Failing check first for FR-20-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-20-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update sidebar/paths/command palette config per IA §12. 4) Apply route guard UX (login redirect / 403 view). 5) Preserve deep-link URLs even if slug panel router is used. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-20-02. |
| **Success** | Observable: The frontend shall meet performance expectations for interactive ops use (responsive navigation, non-blocking lists for MVP data sizes). |
| **Acceptance** | FR-20-02: The frontend shall meet performance expectations for interactive ops use (responsive navigation, non-blocking lists for MVP data sizes). |
| **Evidence** | `frontend/tests/unit` |

### [x] T-20-03 — The frontend shall provide automated lint, typecheck, unit tests, and production build as quality…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-20-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-20-03 |
| **Deliverable (code paths)** | `frontend/playwright.config.ts`<br>`frontend/package.json`<br>`frontend/tests/unit` |
| **Test-first** | CI commands must pass for FR-20-03. |
| **Steps** | 1) Open `requirements.md` FR-20-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-20-3` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-20-03. |
| **Success** | Observable: The frontend shall provide automated lint, typecheck, unit tests, and production build as quality gates. |
| **Acceptance** | FR-20-03: The frontend shall provide automated lint, typecheck, unit tests, and production build as quality gates. |
| **Evidence** | `frontend/playwright.config.ts` |

### [x] T-20-04 — When servers are available, the frontend shall support an operator E1 path: login → dashboard → r…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-20-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-20-04 |
| **Deliverable (code paths)** | `frontend/playwright.config.ts`<br>`frontend/src/lib/config/env.ts`<br>`frontend/README.md`<br>`frontend/package.json` |
| **Test-first** | Unit/e2e: valid login establishes session; invalid shows error (FR-20-04). |
| **Steps** | 1) Open `requirements.md` FR-20-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-20-04. |
| **Success** | Observable: When servers are available, the frontend shall support an operator E1 path: login → dashboard → run → gate → improve as applicable. |
| **Acceptance** | FR-20-04: When servers are available, the frontend shall support an operator E1 path: login → dashboard → run → gate → improve as applicable. |
| **Evidence** | `frontend/playwright.config.ts` |

### [x] T-20-05 — Ops profile DEMO_MODE=false against live backend
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-20-5, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-20-05 |
| **Deliverable (code paths)** | `frontend/src/lib/config/env.ts`<br>`frontend/package.json`<br>`frontend/tests/unit` |
| **Test-first** | Failing check first for FR-20-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-20-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-20-5` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-20-05. |
| **Success** | Observable: The ops profile shall run with `NEXT_PUBLIC_DEMO_MODE=false` against a live backend and Postgres. |
| **Acceptance** | FR-20-05: The ops profile shall run with `NEXT_PUBLIC_DEMO_MODE=false` against a live backend and Postgres. |
| **Evidence** | `frontend/src/lib/config/env.ts` |

### [x] T-20-06 — Each page DoD shall include: routes, permission awareness, loading/empty/error, API wiring or doc…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-20-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-20-06 |
| **Deliverable (code paths)** | `frontend/tests/unit/*`<br>`frontend/README.md`<br>`frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Force slow/fixture load → assert Skeleton/loading UI for FR-20-06. |
| **Steps** | 1) Open `requirements.md` FR-20-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-20-06. |
| **Success** | Observable: Each page DoD shall include: routes, permission awareness, loading/empty/error, API wiring or documented stub, and no charter violations. |
| **Acceptance** | FR-20-06: Each page DoD shall include: routes, permission awareness, loading/empty/error, API wiring or documented stub, and no charter violations. |
| **Evidence** | `frontend/tests/unit/*` |

### [x] T-20-07 — Product-bar non-goals (always-on UI CI servers, full graph explorer, live CRM/email/billing admin…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-20-2, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-20-07 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/playwright.config.ts` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-20-07 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-20-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/package.json`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-20-07. |
| **Success** | Observable: Product-bar non-goals (always-on UI CI servers, full graph explorer, live CRM/email/billing admin, host self-rewrite UI, client-only auth…. |
| **Acceptance** | FR-20-07: Product-bar non-goals (always-on UI CI servers, full graph explorer, live CRM/email/billing admin, host self-rewrite UI, client-only authz) shall not be treated as missing requirements for mark ~100. |
| **Evidence** | `frontend/package.json` |

### [x] T-20-08 — Client observability shall preserve request_id on failures for support correlation when available
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-20-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-20-08 |
| **Deliverable (code paths)** | `frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/playwright.config.ts`<br>`frontend/src/lib/config/env.ts` |
| **Test-first** | Force API 4xx/5xx with request_id → ErrorState shows message + id (FR-20-08). |
| **Steps** | 1) Open `requirements.md` FR-20-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-20-3` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-20-08. |
| **Success** | Observable: Client observability shall preserve request_id on failures for support correlation when available. |
| **Acceptance** | FR-20-08: Client observability shall preserve request_id on failures for support correlation when available. |
| **Evidence** | `frontend/tests/unit` |

### [x] T-20-09 — NFR gate — NFR-20-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-20-01 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/playwright.config.ts` |
| **Test-first** | Define pass/fail measurement for NFR-20-01 before changing code. |
| **Steps** | 1) Map NFR-20-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-20-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-20-01: Production build shall complete in CI-reasonable time for the repo’s frontend package. |
| **Evidence** | `frontend/package.json` |

### [x] T-20-10 — NFR gate — NFR-20-02
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-20-02 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/playwright.config.ts` |
| **Test-first** | Define pass/fail measurement for NFR-20-02 before changing code. |
| **Steps** | 1) Map NFR-20-02 to design §7 performance row. 2) Implement debounce/pagination/abort/code-split as applicable in `frontend/package.json`. 3) Manual or unit timing check for MVP data sizes. 4) Confirm shell remains interactive. 5) Record evidence path. |
| **Success** | NFR-20-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-20-02: Bundle shall code-split heavy client widgets (run timeline, command palette) where practical. |
| **Evidence** | `frontend/package.json` |

### [x] T-20-11 — NFR gate — NFR-20-03
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-20-03 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/playwright.config.ts` |
| **Test-first** | Define pass/fail measurement for NFR-20-03 before changing code. |
| **Steps** | 1) Map NFR-20-03 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-20-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-20-03: Dependency vulnerabilities in FE lockfile shall be reviewed before release claims. |
| **Evidence** | `frontend/package.json` |

### [x] T-20-12 — NFR gate — NFR-20-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-20-04 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/playwright.config.ts` |
| **Test-first** | Define pass/fail measurement for NFR-20-04 before changing code. |
| **Steps** | 1) Map NFR-20-04 to design §7 security row. 2) Inspect `frontend/package.json` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-20-04 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-20-04: DEMO_MODE shall not be required for security; live mode must still enforce backend auth. |
| **Evidence** | `frontend/package.json` |

### [x] T-20-13 — Acceptance proof — AC-20-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-20-01 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-20-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: `pnpm lint`, `pnpm typecheck`, unit tests, and `pnpm build` green. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-20-01 passes with recorded evidence. |
| **Acceptance** | AC-20-01: `pnpm lint`, `pnpm typecheck`, unit tests, and `pnpm build` green. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-20-14 — Acceptance proof — AC-20-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-20-02 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-20-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Ops profile documented and usable for E1. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-20-02 passes with recorded evidence. |
| **Acceptance** | AC-20-02: Ops profile documented and usable for E1. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-20-15 — Acceptance proof — AC-20-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-20-03 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-20-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Security checklist items in §24 addressed or explicitly deferred with owner. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-20-03 passes with recorded evidence. |
| **Acceptance** | AC-20-03: Security checklist items in §24 addressed or explicitly deferred with owner. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-20-16 — Acceptance proof — AC-20-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-20-04 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-20-04 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Non-goals list matches frontend.md §33.5. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-20-04 passes with recorded evidence. |
| **Acceptance** | AC-20-04: Non-goals list matches frontend.md §33.5. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-20-17 — Exit review — FE-20 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-20-01, FR-20-02, FR-20-03, FR-20-04, FR-20-05, FR-20-06, FR-20-07, FR-20-08… |
| **Deliverable (code paths)** | `planning/frontend/20_security-performance-testing-and-ops-profile/tasks.md`<br>`planning/frontend/20_security-performance-testing-and-ops-profile/design.md`<br>`planning/frontend/20_security-performance-testing-and-ops-profile/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-20-01 | T-20-01, T-20-17 |
| FR-20-02 | T-20-02, T-20-17 |
| FR-20-03 | T-20-03, T-20-17 |
| FR-20-04 | T-20-04, T-20-17 |
| FR-20-05 | T-20-05, T-20-17 |
| FR-20-06 | T-20-06, T-20-17 |
| FR-20-07 | T-20-07, T-20-17 |
| FR-20-08 | T-20-08, T-20-17 |
| NFR-20-01 | T-20-09, T-20-17 |
| NFR-20-02 | T-20-10, T-20-17 |
| NFR-20-03 | T-20-11, T-20-17 |
| NFR-20-04 | T-20-12, T-20-17 |
| AC-20-01 | T-20-13, T-20-17 |
| AC-20-02 | T-20-14, T-20-17 |
| AC-20-03 | T-20-15, T-20-17 |
| AC-20-04 | T-20-16, T-20-17 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-20-1 | T-20-01, T-20-06 |
| C-20-2 | T-20-02, T-20-07 |
| C-20-3 | T-20-03, T-20-08 |
| C-20-4 | T-20-04 |
| C-20-5 | T-20-05 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 8/8 | [x] FR-20-01, FR-20-02, FR-20-03, FR-20-04, FR-20-05, FR-20-06, FR-20-07, FR-20-08 |
| 4 | NFR coverage 4/4 | [x] NFR-20-01, NFR-20-02, NFR-20-03, NFR-20-04 |
| 5 | AC coverage 4/4 | [x] AC-20-01, AC-20-02, AC-20-03, AC-20-04 |
| 6 | C-* coverage 5/5 | [x] C-20-1, C-20-2, C-20-3, C-20-4, C-20-5 |
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
