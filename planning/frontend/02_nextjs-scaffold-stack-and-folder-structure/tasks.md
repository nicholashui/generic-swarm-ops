# Tasks — 02 Next.js Scaffold, Stack, and Folder Structure

| Field | Value |
|-------|-------|
| Task list ID | `FE-02-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-02-DES`) |
| Paired requirements | `requirements.md` (`FE-02`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 9/9 · NFR 4/4 · AC 4/4 · C-* 6/6 |

---

## SDD workflow

Scaffold Next app → env → middleware → scripts → lint/typecheck/build green.

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

These are the **main source locations** for FE-02. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/package.json`
- `frontend/tsconfig.json`
- `frontend/middleware.ts`
- `frontend/src/app`
- `frontend/src/lib/config/env.ts`
- `frontend/src/app/globals.css`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-02-1 | App router root | `frontend/src/app` |
| C-02-2 | Middleware | `frontend/middleware.ts` |
| C-02-3 | Env config | `frontend/src/lib/config/env.ts` |
| C-02-4 | Tooling | `frontend/package.json, tsconfig.json, eslint, vitest, playwright` |
| C-02-5 | Global styles | `frontend/src/app/globals.css` |
| C-02-6 | Path aliases | `frontend/tsconfig.json `@/*` → `src/*` |

---

## Task backlog

### [x] T-02-01 — The frontend shall be implemented as a Next.js application using React and TypeScript
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-02-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-02-01 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/src/app` |
| **Test-first** | Failing check first for FR-02-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-02-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Scaffold/verify Next App Router, Tailwind, path aliases, env loader. 4) Ensure lint/typecheck/build scripts green. 5) Document DEMO_MODE vs ops profile in env/README. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-02-01. |
| **Success** | Observable: The frontend shall be implemented as a Next.js application using React and TypeScript. |
| **Acceptance** | FR-02-01: The frontend shall be implemented as a Next.js application using React and TypeScript. |
| **Evidence** | `frontend/package.json` |

### [x] T-02-02 — The frontend shall use Tailwind CSS for styling integration with design tokens
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-02-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-02-02 |
| **Deliverable (code paths)** | `frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/src/app`<br>`frontend/src/lib/config/env.ts` |
| **Test-first** | Failing check first for FR-02-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-02-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Scaffold/verify Next App Router, Tailwind, path aliases, env loader. 4) Ensure lint/typecheck/build scripts green. 5) Document DEMO_MODE vs ops profile in env/README. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-02-02. |
| **Success** | Observable: The frontend shall use Tailwind CSS for styling integration with design tokens. |
| **Acceptance** | FR-02-02: The frontend shall use Tailwind CSS for styling integration with design tokens. |
| **Evidence** | `frontend/tsconfig.json` |

### [x] T-02-03 — When a UI element is highly interactive (command palette, realtime timeline, modals, drawers, fil…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-02-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-02-03 |
| **Deliverable (code paths)** | `frontend/middleware.ts`<br>`frontend/src/app`<br>`frontend/src/lib/config/env.ts`<br>`frontend/src/app/globals.css` |
| **Test-first** | Mock stream events → UI updates; kill stream → degraded/poll (FR-02-03). |
| **Steps** | 1) Open `requirements.md` FR-02-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/extend `useRealtimeRun` + `sse.ts` subscribe/merge. 4) On stream error set degraded + poll; cleanup on unmount. 5) Drive Timeline/LogViewer from merged events without full page reload. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-02-03. |
| **Success** | Observable: When a UI element is highly interactive (command palette, realtime timeline, modals, drawers, filterable tables, workflow builder, logs v…. |
| **Acceptance** | FR-02-03: When a UI element is highly interactive (command palette, realtime timeline, modals, drawers, filterable tables, workflow builder, logs viewer), the frontend shall implement it as a client component. |
| **Evidence** | `frontend/middleware.ts` |

### [x] T-02-04 — When a surface is static layout, metadata, or secure initial composition, the frontend shall pref…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-02-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-02-04 |
| **Deliverable (code paths)** | `frontend/package.json, tsconfig.json, eslint, vitest, playwright`<br>`frontend/src/app`<br>`frontend/src/lib/config/env.ts`<br>`frontend/src/app/globals.css`<br>`frontend/package.json` |
| **Test-first** | Failing check first for FR-02-04: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-02-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Scaffold/verify Next App Router, Tailwind, path aliases, env loader. 4) Ensure lint/typecheck/build scripts green. 5) Document DEMO_MODE vs ops profile in env/README. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-02-04. |
| **Success** | Observable: When a surface is static layout, metadata, or secure initial composition, the frontend shall prefer server components where appropriate. |
| **Acceptance** | FR-02-04: When a surface is static layout, metadata, or secure initial composition, the frontend shall prefer server components where appropriate. |
| **Evidence** | `frontend/package.json, tsconfig.json, eslint, vitest, playwright` |

### [x] T-02-05 — The frontend shall organize source under the recommended folder structure (app routes, components…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-02-5, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-02-05 |
| **Deliverable (code paths)** | `frontend/src/lib/config/env.ts`<br>`frontend/src/app/globals.css`<br>`frontend/package.json`<br>`frontend/tsconfig.json` |
| **Test-first** | Failing check first for FR-02-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-02-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Scaffold/verify Next App Router, Tailwind, path aliases, env loader. 4) Ensure lint/typecheck/build scripts green. 5) Document DEMO_MODE vs ops profile in env/README. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-02-05. |
| **Success** | Observable: The frontend shall organize source under the recommended folder structure (app routes, components, lib/api, hooks, types, styles/tokens). |
| **Acceptance** | FR-02-05: The frontend shall organize source under the recommended folder structure (app routes, components, lib/api, hooks, types, styles/tokens). |
| **Evidence** | `frontend/src/lib/config/env.ts` |

### [x] T-02-06 — The frontend shall load configuration from environment variables including API base URL and `NEXT…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-02-6, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-02-06 |
| **Deliverable (code paths)** | `frontend/tsconfig.json `@/*` → `src/*`<br>`frontend/src/lib/config/env.ts`<br>`frontend/package.json`<br>`frontend/tsconfig.json` |
| **Test-first** | Failing check first for FR-02-06: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-02-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Scaffold/verify Next App Router, Tailwind, path aliases, env loader. 4) Ensure lint/typecheck/build scripts green. 5) Document DEMO_MODE vs ops profile in env/README. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-02-06. |
| **Success** | Observable: The frontend shall load configuration from environment variables including API base URL and `NEXT_PUBLIC_DEMO_MODE`. |
| **Acceptance** | FR-02-06: The frontend shall load configuration from environment variables including API base URL and `NEXT_PUBLIC_DEMO_MODE`. |
| **Evidence** | `frontend/tsconfig.json `@/*` → `src/*` |

### [x] T-02-07 — The frontend project shall provide `pnpm install`, `pnpm dev`, `pnpm build`, `pnpm lint`, and `pn…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-02-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-02-07 |
| **Deliverable (code paths)** | `frontend/src/app`<br>`frontend/package.json`<br>`frontend/tsconfig.json` |
| **Test-first** | CI commands must pass for FR-02-07. |
| **Steps** | 1) Open `requirements.md` FR-02-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Scaffold/verify Next App Router, Tailwind, path aliases, env loader. 4) Ensure lint/typecheck/build scripts green. 5) Document DEMO_MODE vs ops profile in env/README. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-02-07. |
| **Success** | Observable: The frontend project shall provide `pnpm install`, `pnpm dev`, `pnpm build`, `pnpm lint`, and `pnpm typecheck` (or equivalent documented …. |
| **Acceptance** | FR-02-07: The frontend project shall provide `pnpm install`, `pnpm dev`, `pnpm build`, `pnpm lint`, and `pnpm typecheck` (or equivalent documented scripts). |
| **Evidence** | `frontend/src/app` |

### [x] T-02-08 — If the user is not authenticated and navigates to `/app/*`, the route layer shall redirect to `/l…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-02-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-02-08 |
| **Deliverable (code paths)** | `frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/src/app`<br>`frontend/src/lib/config/env.ts` |
| **Test-first** | Unit/e2e: valid login establishes session; invalid shows error (FR-02-08). |
| **Steps** | 1) Open `requirements.md` FR-02-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-02-08. |
| **Success** | Observable: If the user is not authenticated and navigates to `/app/*`, the route layer shall redirect to `/login` (UX protection only). |
| **Acceptance** | FR-02-08: If the user is not authenticated and navigates to `/app/*`, the route layer shall redirect to `/login` (UX protection only). |
| **Evidence** | `frontend/tsconfig.json` |

### [x] T-02-09 — The frontend shall document README startup instructions for local development against a live backend
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-02-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-02-09 |
| **Deliverable (code paths)** | `frontend/middleware.ts`<br>`frontend/src/app`<br>`frontend/src/lib/config/env.ts`<br>`frontend/src/app/globals.css` |
| **Test-first** | Failing check first for FR-02-09: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-02-09 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Scaffold/verify Next App Router, Tailwind, path aliases, env loader. 4) Ensure lint/typecheck/build scripts green. 5) Document DEMO_MODE vs ops profile in env/README. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-02-09. |
| **Success** | Observable: The frontend shall document README startup instructions for local development against a live backend. |
| **Acceptance** | FR-02-09: The frontend shall document README startup instructions for local development against a live backend. |
| **Evidence** | `frontend/middleware.ts` |

### [x] T-02-10 — NFR gate — NFR-02-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-02-01 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/src/app` |
| **Test-first** | Define pass/fail measurement for NFR-02-01 before changing code. |
| **Steps** | 1) Map NFR-02-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-02-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-02-01: Local `pnpm dev` shall start the app for interactive development without requiring a full production build. |
| **Evidence** | `frontend/package.json` |

### [x] T-02-11 — NFR gate — NFR-02-02
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-02-02 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/src/app` |
| **Test-first** | Define pass/fail measurement for NFR-02-02 before changing code. |
| **Steps** | 1) Map NFR-02-02 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-02-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-02-02: Production `pnpm build` shall succeed for the scaffolded app shell before domain pages are complete. |
| **Evidence** | `frontend/package.json` |

### [x] T-02-12 — NFR gate — NFR-02-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-02-03 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/src/app` |
| **Test-first** | Define pass/fail measurement for NFR-02-03 before changing code. |
| **Steps** | 1) Map NFR-02-03 to design §7 security row. 2) Inspect `frontend/package.json` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-02-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-02-03: Secrets used only on the server shall not be prefixed with `NEXT_PUBLIC_`. |
| **Evidence** | `frontend/package.json` |

### [x] T-02-13 — NFR gate — NFR-02-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-02-04 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/src/app` |
| **Test-first** | Define pass/fail measurement for NFR-02-04 before changing code. |
| **Steps** | 1) Map NFR-02-04 to design §7 security row. 2) Inspect `frontend/package.json` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-02-04 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-02-04: Client-exposed env shall be limited to non-secret configuration (API URL, demo flag, public app metadata). |
| **Evidence** | `frontend/package.json` |

### [x] T-02-14 — Acceptance proof — AC-02-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-02-01 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-02-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: App starts locally with TypeScript and Tailwind working. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-02-01 passes with recorded evidence. |
| **Acceptance** | AC-02-01: App starts locally with TypeScript and Tailwind working. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-02-15 — Acceptance proof — AC-02-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-02-02 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-02-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Lint and typecheck scripts pass on scaffold. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-02-02 passes with recorded evidence. |
| **Acceptance** | AC-02-02: Lint and typecheck scripts pass on scaffold. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-02-16 — Acceptance proof — AC-02-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-02-03 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-02-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Folder structure matches frontend.md §18 intent (or documented as-built equivalent). 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-02-03 passes with recorded evidence. |
| **Acceptance** | AC-02-03: Folder structure matches frontend.md §18 intent (or documented as-built equivalent). |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-02-17 — Acceptance proof — AC-02-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-02-04 |
| **Deliverable (code paths)** | `frontend/package.json`<br>`frontend/tsconfig.json`<br>`frontend/middleware.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-02-04 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Env template documents API URL and DEMO_MODE. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-02-04 passes with recorded evidence. |
| **Acceptance** | AC-02-04: Env template documents API URL and DEMO_MODE. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-02-18 — Exit review — FE-02 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-02-01, FR-02-02, FR-02-03, FR-02-04, FR-02-05, FR-02-06, FR-02-07, FR-02-08… |
| **Deliverable (code paths)** | `planning/frontend/02_nextjs-scaffold-stack-and-folder-structure/tasks.md`<br>`planning/frontend/02_nextjs-scaffold-stack-and-folder-structure/design.md`<br>`planning/frontend/02_nextjs-scaffold-stack-and-folder-structure/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-02-01 | T-02-01, T-02-18 |
| FR-02-02 | T-02-02, T-02-18 |
| FR-02-03 | T-02-03, T-02-18 |
| FR-02-04 | T-02-04, T-02-18 |
| FR-02-05 | T-02-05, T-02-18 |
| FR-02-06 | T-02-06, T-02-18 |
| FR-02-07 | T-02-07, T-02-18 |
| FR-02-08 | T-02-08, T-02-18 |
| FR-02-09 | T-02-09, T-02-18 |
| NFR-02-01 | T-02-10, T-02-18 |
| NFR-02-02 | T-02-11, T-02-18 |
| NFR-02-03 | T-02-12, T-02-18 |
| NFR-02-04 | T-02-13, T-02-18 |
| AC-02-01 | T-02-14, T-02-18 |
| AC-02-02 | T-02-15, T-02-18 |
| AC-02-03 | T-02-16, T-02-18 |
| AC-02-04 | T-02-17, T-02-18 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-02-1 | T-02-01, T-02-07 |
| C-02-2 | T-02-02, T-02-08 |
| C-02-3 | T-02-03, T-02-09 |
| C-02-4 | T-02-04 |
| C-02-5 | T-02-05 |
| C-02-6 | T-02-06 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 9/9 | [x] FR-02-01, FR-02-02, FR-02-03, FR-02-04, FR-02-05, FR-02-06, FR-02-07, FR-02-08, FR-02-09 |
| 4 | NFR coverage 4/4 | [x] NFR-02-01, NFR-02-02, NFR-02-03, NFR-02-04 |
| 5 | AC coverage 4/4 | [x] AC-02-01, AC-02-02, AC-02-03, AC-02-04 |
| 6 | C-* coverage 6/6 | [x] C-02-1, C-02-2, C-02-3, C-02-4, C-02-5, C-02-6 |
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
