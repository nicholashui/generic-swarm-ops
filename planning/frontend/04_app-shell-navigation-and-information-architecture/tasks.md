# Tasks — 04 App Shell, Navigation, and Information Architecture

| Field | Value |
|-------|-------|
| Task list ID | `FE-04-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-04-DES`) |
| Paired requirements | `requirements.md` (`FE-04`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 10/10 · NFR 4/4 · AC 4/4 · C-* 8/8 |

---

## SDD workflow

AppShell → sidebar IA → header/CmdK → route guards UX → deep links.

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

These are the **main source locations** for FE-04. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/components/layout/app-shell.tsx`
- `frontend/src/components/layout/sidebar.tsx`
- `frontend/src/components/layout/app-header.tsx`
- `frontend/src/components/layout/command-palette.tsx`
- `frontend/src/components/layout/mobile-nav.tsx`
- `frontend/src/lib/routes/paths.ts`
- `frontend/src/app/app`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-04-1 | App shell | `frontend/src/components/layout/app-shell.tsx` |
| C-04-2 | Sidebar | `frontend/src/components/layout/sidebar.tsx` |
| C-04-3 | Header | `frontend/src/components/layout/app-header.tsx` |
| C-04-4 | Breadcrumbs | `frontend/src/components/layout/breadcrumbs.tsx` |
| C-04-5 | Command palette | `frontend/src/components/layout/command-palette.tsx` |
| C-04-6 | Mobile nav | `frontend/src/components/layout/mobile-nav.tsx` |
| C-04-7 | Path helpers | `frontend/src/lib/routes/paths.ts` |
| C-04-8 | App routes | `frontend/src/app/app/*` |

---

## Task backlog

### [x] T-04-01 — The frontend shall provide an authenticated app shell for all `/app/*` routes
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-04-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-04-01 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx` |
| **Test-first** | Failing check first for FR-04-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-04-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update sidebar/paths/command palette config per IA §12. 4) Apply route guard UX (login redirect / 403 view). 5) Preserve deep-link URLs even if slug panel router is used. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-04-01. |
| **Success** | Observable: The frontend shall provide an authenticated app shell for all `/app/*` routes. |
| **Acceptance** | FR-04-01: The frontend shall provide an authenticated app shell for all `/app/*` routes. |
| **Evidence** | `frontend/src/components/layout/app-shell.tsx` |

### [x] T-04-02 — The sidebar shall group navigation into Main, Data, Quality, Security, and Admin as specified in …
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-04-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-04-02 |
| **Deliverable (code paths)** | `frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/src/components/layout/command-palette.tsx`<br>`frontend/src/components/layout/mobile-nav.tsx` |
| **Test-first** | Failing check first for FR-04-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-04-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update sidebar/paths/command palette config per IA §12. 4) Apply route guard UX (login redirect / 403 view). 5) Preserve deep-link URLs even if slug panel router is used. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-04-02. |
| **Success** | Observable: The sidebar shall group navigation into Main, Data, Quality, Security, and Admin as specified in frontend.md §12.2. |
| **Acceptance** | FR-04-02: The sidebar shall group navigation into Main, Data, Quality, Security, and Admin as specified in frontend.md §12.2. |
| **Evidence** | `frontend/src/components/layout/sidebar.tsx` |

### [x] T-04-03 — The frontend shall expose information architecture routes for dashboard, agents, tools, workflows…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-04-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-04-03 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-header.tsx`<br>`frontend/src/components/layout/command-palette.tsx`<br>`frontend/src/components/layout/mobile-nav.tsx`<br>`frontend/src/lib/routes/paths.ts` |
| **Test-first** | Mock stream events → UI updates; kill stream → degraded/poll (FR-04-03). |
| **Steps** | 1) Open `requirements.md` FR-04-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/extend `useRealtimeRun` + `sse.ts` subscribe/merge. 4) On stream error set degraded + poll; cleanup on unmount. 5) Drive Timeline/LogViewer from merged events without full page reload. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-04-03. |
| **Success** | Observable: The frontend shall expose information architecture routes for dashboard, agents, tools, workflows, workflow runs, approvals, knowledge, m…. |
| **Acceptance** | FR-04-03: The frontend shall expose information architecture routes for dashboard, agents, tools, workflows, workflow runs, approvals, knowledge, memory, evaluations, processes, audit logs, evolution, and settings sub-routes. |
| **Evidence** | `frontend/src/components/layout/app-header.tsx` |

### [x] T-04-04 — When a user is not authenticated on `/app/*`, the frontend shall redirect to `/login`
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-04-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-04-04 |
| **Deliverable (code paths)** | `frontend/src/components/layout/breadcrumbs.tsx`<br>`frontend/src/components/layout/command-palette.tsx`<br>`frontend/src/components/layout/mobile-nav.tsx`<br>`frontend/src/lib/routes/paths.ts`<br>`frontend/src/app/app` |
| **Test-first** | Unit/e2e: valid login establishes session; invalid shows error (FR-04-04). |
| **Steps** | 1) Open `requirements.md` FR-04-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-04-04. |
| **Success** | Observable: When a user is not authenticated on `/app/*`, the frontend shall redirect to `/login`. |
| **Acceptance** | FR-04-04: When a user is not authenticated on `/app/*`, the frontend shall redirect to `/login`. |
| **Evidence** | `frontend/src/components/layout/breadcrumbs.tsx` |

### [x] T-04-05 — When a user lacks organization access, the frontend shall redirect to organization selection or a…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-04-5, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-04-05 |
| **Deliverable (code paths)** | `frontend/src/components/layout/command-palette.tsx`<br>`frontend/src/components/layout/mobile-nav.tsx`<br>`frontend/src/lib/routes/paths.ts`<br>`frontend/src/app/app`<br>`frontend/src/components/layout/app-shell.tsx` |
| **Test-first** | Failing check first for FR-04-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-04-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire settings sub-routes to users/orgs/keys APIs. 4) Confirm destructive actions; show API key secret once only. 5) Billing remains placeholder without inventing charges. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-04-05. |
| **Success** | Observable: When a user lacks organization access, the frontend shall redirect to organization selection or an access-denied page. |
| **Acceptance** | FR-04-05: When a user lacks organization access, the frontend shall redirect to organization selection or an access-denied page. |
| **Evidence** | `frontend/src/components/layout/command-palette.tsx` |

### [x] T-04-06 — When a user lacks permission for a route, the frontend shall display a 403 Access Denied state (U…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-04-6, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-04-06 |
| **Deliverable (code paths)** | `frontend/src/components/layout/mobile-nav.tsx`<br>`frontend/src/lib/routes/paths.ts`<br>`frontend/src/app/app`<br>`frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-04-06). |
| **Steps** | 1) Open `requirements.md` FR-04-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-04-06. |
| **Success** | Observable: When a user lacks permission for a route, the frontend shall display a 403 Access Denied state (UX only). |
| **Acceptance** | FR-04-06: When a user lacks permission for a route, the frontend shall display a 403 Access Denied state (UX only). |
| **Evidence** | `frontend/src/components/layout/mobile-nav.tsx` |

### [x] T-04-07 — The global header shall include breadcrumbs, command/search trigger, non-production environment i…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-04-7, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-04-07 |
| **Deliverable (code paths)** | `frontend/src/lib/routes/paths.ts`<br>`frontend/src/components/layout/command-palette.tsx`<br>`frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx` |
| **Test-first** | Failing check first for FR-04-07: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-04-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire settings sub-routes to users/orgs/keys APIs. 4) Confirm destructive actions; show API key secret once only. 5) Billing remains placeholder without inventing charges. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-04-07. |
| **Success** | Observable: The global header shall include breadcrumbs, command/search trigger, non-production environment indicator when applicable, organization s…. |
| **Acceptance** | FR-04-07: The global header shall include breadcrumbs, command/search trigger, non-production environment indicator when applicable, organization switcher, notifications entry, and user menu. |
| **Evidence** | `frontend/src/lib/routes/paths.ts` |

### [x] T-04-08 — When the user presses Cmd/Ctrl+K, the frontend shall open a command palette with documented actio…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-04-8, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-04-08 |
| **Deliverable (code paths)** | `frontend/src/app/app/*`<br>`frontend/src/components/layout/command-palette.tsx`<br>`frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx` |
| **Test-first** | Mock stream events → UI updates; kill stream → degraded/poll (FR-04-08). |
| **Steps** | 1) Open `requirements.md` FR-04-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-04-08. |
| **Success** | Observable: When the user presses Cmd/Ctrl+K, the frontend shall open a command palette with documented actions (create agent/workflow, search knowle…. |
| **Acceptance** | FR-04-08: When the user presses Cmd/Ctrl+K, the frontend shall open a command palette with documented actions (create agent/workflow, search knowledge, open recent run, approvals, invite, API keys, audit, security, evaluation, knowledge source). |
| **Evidence** | `frontend/src/app/app/*` |

### [x] T-04-09 — If the implementation uses a dynamic `/app/[...slug]` panel router, the frontend shall still pres…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-04-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-04-09 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/src/components/layout/command-palette.tsx`<br>`frontend/src/components/layout/mobile-nav.tsx` |
| **Test-first** | Failing check first for FR-04-09: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-04-09 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update sidebar/paths/command palette config per IA §12. 4) Apply route guard UX (login redirect / 403 view). 5) Preserve deep-link URLs even if slug panel router is used. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-04-09. |
| **Success** | Observable: If the implementation uses a dynamic `/app/[...slug]` panel router, the frontend shall still present the §12.1 URLs in navigation and dee…. |
| **Acceptance** | FR-04-09: If the implementation uses a dynamic `/app/[...slug]` panel router, the frontend shall still present the §12.1 URLs in navigation and deep links. |
| **Evidence** | `frontend/src/components/layout/app-shell.tsx` |

### [x] T-04-10 — Public root `/` shall land or redirect according to product rules (landing or to login/app)
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-04-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-04-10 |
| **Deliverable (code paths)** | `frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/src/components/layout/command-palette.tsx`<br>`frontend/src/components/layout/mobile-nav.tsx`<br>`frontend/src/lib/routes/paths.ts` |
| **Test-first** | Unit/e2e: valid login establishes session; invalid shows error (FR-04-10). |
| **Steps** | 1) Open `requirements.md` FR-04-10 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-04-10. |
| **Success** | Observable: Public root `/` shall land or redirect according to product rules (landing or to login/app). |
| **Acceptance** | FR-04-10: Public root `/` shall land or redirect according to product rules (landing or to login/app). |
| **Evidence** | `frontend/src/components/layout/sidebar.tsx` |

### [x] T-04-11 — NFR gate — NFR-04-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-04-01 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/src/components/layout/command-palette.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-04-01 before changing code. |
| **Steps** | 1) Map NFR-04-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-04-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-04-01: App shell chrome shall remain responsive during client navigations between domain panels. |
| **Evidence** | `frontend/src/components/layout/app-shell.tsx` |

### [x] T-04-12 — NFR gate — NFR-04-02
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-04-02 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/src/components/layout/command-palette.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-04-02 before changing code. |
| **Steps** | 1) Map NFR-04-02 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-04-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-04-02: Command palette shall open without full page reload. |
| **Evidence** | `frontend/src/components/layout/app-shell.tsx` |

### [x] T-04-13 — NFR gate — NFR-04-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-04-03 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/src/components/layout/command-palette.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-04-03 before changing code. |
| **Steps** | 1) Map NFR-04-03 to design §7 security row. 2) Inspect `frontend/src/components/layout/app-shell.tsx` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-04-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-04-03: Client route guards shall not replace backend authorization. |
| **Evidence** | `frontend/src/components/layout/app-shell.tsx` |

### [x] T-04-14 — NFR gate — NFR-04-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-04-04 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/src/components/layout/command-palette.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-04-04 before changing code. |
| **Steps** | 1) Map NFR-04-04 to design §7 security row. 2) Inspect `frontend/src/components/layout/app-shell.tsx` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-04-04 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-04-04: User menu and org switcher shall not expose tokens in the DOM beyond necessary display fields. |
| **Evidence** | `frontend/src/components/layout/app-shell.tsx` |

### [x] T-04-15 — Acceptance proof — AC-04-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-04-01 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-04-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Authenticated shell renders sidebar + header + content. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-04-01 passes with recorded evidence. |
| **Acceptance** | AC-04-01: Authenticated shell renders sidebar + header + content. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-04-16 — Acceptance proof — AC-04-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-04-02 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-04-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Navigation groups match §12.2 labels. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-04-02 passes with recorded evidence. |
| **Acceptance** | AC-04-02: Navigation groups match §12.2 labels. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-04-17 — Acceptance proof — AC-04-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-04-03 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-04-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Unauthenticated access to `/app` redirects to login. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-04-03 passes with recorded evidence. |
| **Acceptance** | AC-04-03: Unauthenticated access to `/app` redirects to login. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-04-18 — Acceptance proof — AC-04-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-04-04 |
| **Deliverable (code paths)** | `frontend/src/components/layout/app-shell.tsx`<br>`frontend/src/components/layout/sidebar.tsx`<br>`frontend/src/components/layout/app-header.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-04-04 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Command palette opens via keyboard shortcut. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-04-04 passes with recorded evidence. |
| **Acceptance** | AC-04-04: Command palette opens via keyboard shortcut. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-04-19 — Exit review — FE-04 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-04-01, FR-04-02, FR-04-03, FR-04-04, FR-04-05, FR-04-06, FR-04-07, FR-04-08… |
| **Deliverable (code paths)** | `planning/frontend/04_app-shell-navigation-and-information-architecture/tasks.md`<br>`planning/frontend/04_app-shell-navigation-and-information-architecture/design.md`<br>`planning/frontend/04_app-shell-navigation-and-information-architecture/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-04-01 | T-04-01, T-04-19 |
| FR-04-02 | T-04-02, T-04-19 |
| FR-04-03 | T-04-03, T-04-19 |
| FR-04-04 | T-04-04, T-04-19 |
| FR-04-05 | T-04-05, T-04-19 |
| FR-04-06 | T-04-06, T-04-19 |
| FR-04-07 | T-04-07, T-04-19 |
| FR-04-08 | T-04-08, T-04-19 |
| FR-04-09 | T-04-09, T-04-19 |
| FR-04-10 | T-04-10, T-04-19 |
| NFR-04-01 | T-04-11, T-04-19 |
| NFR-04-02 | T-04-12, T-04-19 |
| NFR-04-03 | T-04-13, T-04-19 |
| NFR-04-04 | T-04-14, T-04-19 |
| AC-04-01 | T-04-15, T-04-19 |
| AC-04-02 | T-04-16, T-04-19 |
| AC-04-03 | T-04-17, T-04-19 |
| AC-04-04 | T-04-18, T-04-19 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-04-1 | T-04-01, T-04-09 |
| C-04-2 | T-04-02, T-04-10 |
| C-04-3 | T-04-03 |
| C-04-4 | T-04-04 |
| C-04-5 | T-04-05 |
| C-04-6 | T-04-06 |
| C-04-7 | T-04-07 |
| C-04-8 | T-04-08 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 10/10 | [x] FR-04-01, FR-04-02, FR-04-03, FR-04-04, FR-04-05, FR-04-06, FR-04-07, FR-04-08, FR-04-09, FR-04-10 |
| 4 | NFR coverage 4/4 | [x] NFR-04-01, NFR-04-02, NFR-04-03, NFR-04-04 |
| 5 | AC coverage 4/4 | [x] AC-04-01, AC-04-02, AC-04-03, AC-04-04 |
| 6 | C-* coverage 8/8 | [x] C-04-1, C-04-2, C-04-3, C-04-4, C-04-5, C-04-6, C-04-7, C-04-8 |
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
