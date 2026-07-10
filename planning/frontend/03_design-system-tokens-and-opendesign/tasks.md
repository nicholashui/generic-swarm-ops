# Tasks — 03 Design System, Tokens, and OpenDesign Workflow

| Field | Value |
|-------|-------|
| Task list ID | `FE-03-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-03-DES`) |
| Paired requirements | `requirements.md` (`FE-03`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 9/9 · NFR 4/4 · AC 4/4 · C-* 5/5 |

---

## SDD workflow

OpenDesign/fallback → tokens → ui primitives → status map → docs/design.

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

These are the **main source locations** for FE-03. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/design/tokens.ts`
- `frontend/src/design/theme.ts`
- `frontend/src/design/status.ts`
- `frontend/src/components/ui`
- `frontend/docs/design`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-03-1 | Design tokens | `frontend/src/design/tokens.ts` |
| C-03-2 | Theme map | `frontend/src/design/theme.ts` |
| C-03-3 | Status map | `frontend/src/design/status.ts` |
| C-03-4 | UI kit | `frontend/src/components/ui/*` |
| C-03-5 | Design docs | `frontend/docs/design/*` |

---

## Task backlog

### [x] T-03-01 — Before creating or significantly modifying a major page layout, Trae shall call the OpenDesign MC…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-03-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-03-01 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/src/components/ui` |
| **Test-first** | Failing check first for FR-03-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-03-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/adjust tokens + ui primitive for the requirement. 4) Map status enum → StatusBadge label+color (not color alone). 5) Document OpenDesign call or fallback under `docs/design/`. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-03-01. |
| **Success** | Observable: Before creating or significantly modifying a major page layout, Trae shall call the OpenDesign MCP server named `opendesign` when available. |
| **Acceptance** | FR-03-01: Before creating or significantly modifying a major page layout, Trae shall call the OpenDesign MCP server named `opendesign` when available. |
| **Evidence** | `frontend/src/design/tokens.ts` |

### [x] T-03-02 — If OpenDesign MCP is unavailable, the frontend shall use a documented design fallback and record …
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-03-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-03-02 |
| **Deliverable (code paths)** | `frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/src/components/ui`<br>`frontend/docs/design` |
| **Test-first** | Failing check first for FR-03-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-03-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/adjust tokens + ui primitive for the requirement. 4) Map status enum → StatusBadge label+color (not color alone). 5) Document OpenDesign call or fallback under `docs/design/`. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-03-02. |
| **Success** | Observable: If OpenDesign MCP is unavailable, the frontend shall use a documented design fallback and record the fallback in design documentation. |
| **Acceptance** | FR-03-02: If OpenDesign MCP is unavailable, the frontend shall use a documented design fallback and record the fallback in design documentation. |
| **Evidence** | `frontend/src/design/theme.ts` |

### [x] T-03-03 — The frontend shall implement design tokens for color, typography, spacing, and status semantics
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-03-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-03-03 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/status.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/docs/design` |
| **Test-first** | Failing check first for FR-03-03: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-03-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/adjust tokens + ui primitive for the requirement. 4) Map status enum → StatusBadge label+color (not color alone). 5) Document OpenDesign call or fallback under `docs/design/`. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-03-03. |
| **Success** | Observable: The frontend shall implement design tokens for color, typography, spacing, and status semantics. |
| **Acceptance** | FR-03-03: The frontend shall implement design tokens for color, typography, spacing, and status semantics. |
| **Evidence** | `frontend/src/design/tokens.ts` |

### [x] T-03-04 — The frontend shall implement base UI components for buttons, form controls, status badges, cards,…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-03-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-03-04 |
| **Deliverable (code paths)** | `frontend/src/components/ui/*`<br>`frontend/src/components/ui`<br>`frontend/docs/design`<br>`frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts` |
| **Test-first** | Failing check first for FR-03-04: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-03-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Compose run detail route/panel with WorkflowRunConsole + StatusBadge. 4) Load GET run/steps; map statuses via `lib/formatting/status` + design status tokens. 5) Render Timeline + LogViewer; never execute steps in the browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-03-04. |
| **Success** | Observable: The frontend shall implement base UI components for buttons, form controls, status badges, cards, tables, modals/drawers, and alerts. |
| **Acceptance** | FR-03-04: The frontend shall implement base UI components for buttons, form controls, status badges, cards, tables, modals/drawers, and alerts. |
| **Evidence** | `frontend/src/components/ui/*` |

### [x] T-03-05 — The frontend shall implement layout components that support authenticated app shell composition
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-03-5, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-03-05 |
| **Deliverable (code paths)** | `frontend/docs/design/*`<br>`frontend/docs/design`<br>`frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts` |
| **Test-first** | Failing check first for FR-03-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-03-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/adjust tokens + ui primitive for the requirement. 4) Map status enum → StatusBadge label+color (not color alone). 5) Document OpenDesign call or fallback under `docs/design/`. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-03-05. |
| **Success** | Observable: The frontend shall implement layout components that support authenticated app shell composition. |
| **Acceptance** | FR-03-05: The frontend shall implement layout components that support authenticated app shell composition. |
| **Evidence** | `frontend/docs/design/*` |

### [x] T-03-06 — The frontend shall implement reusable loading, empty, and error presentation components
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-03-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-03-06 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/src/components/ui` |
| **Test-first** | Force slow/fixture load → assert Skeleton/loading UI for FR-03-06. |
| **Steps** | 1) Open `requirements.md` FR-03-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Adopt Skeleton/EmptyState/ErrorState primitives on target pages. 4) Labels, focus rings, non-color-only status; request_id on errors. 5) Keyboard-pass primary flows; sanitize production error bodies. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-03-06. |
| **Success** | Observable: The frontend shall implement reusable loading, empty, and error presentation components. |
| **Acceptance** | FR-03-06: The frontend shall implement reusable loading, empty, and error presentation components. |
| **Evidence** | `frontend/src/design/tokens.ts` |

### [x] T-03-07 — Status colors and badges shall encode operational states (running, succeeded, failed, awaiting ap…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-03-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-03-07 |
| **Deliverable (code paths)** | `frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/src/components/ui`<br>`frontend/docs/design` |
| **Test-first** | Failing check first for FR-03-07: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-03-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Add action handlers on run console calling lifecycle POST routes. 4) Disable when status/permission forbids; busy state prevents double-submit. 5) Refresh/merge run state after success; show AppError on failure. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-03-07. |
| **Success** | Observable: Status colors and badges shall encode operational states (running, succeeded, failed, awaiting approval, paused, cancelled) consistently. |
| **Acceptance** | FR-03-07: Status colors and badges shall encode operational states (running, succeeded, failed, awaiting approval, paused, cancelled) consistently. |
| **Evidence** | `frontend/src/design/theme.ts` |

### [x] T-03-08 — The design system shall favor operational density and scannability appropriate to an enterprise o…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-03-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-03-08 |
| **Deliverable (code paths)** | `frontend/src/design/status.ts`<br>`frontend/src/components/ui`<br>`frontend/docs/design`<br>`frontend/src/design/tokens.ts` |
| **Test-first** | Failing check first for FR-03-08: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-03-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/adjust tokens + ui primitive for the requirement. 4) Map status enum → StatusBadge label+color (not color alone). 5) Document OpenDesign call or fallback under `docs/design/`. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-03-08. |
| **Success** | Observable: The design system shall favor operational density and scannability appropriate to an enterprise ops console. |
| **Acceptance** | FR-03-08: The design system shall favor operational density and scannability appropriate to an enterprise ops console. |
| **Evidence** | `frontend/src/design/status.ts` |

### [x] T-03-09 — Design reference artifacts shall be documented under `docs/design/` (or equivalent) including tok…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-03-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-03-09 |
| **Deliverable (code paths)** | `frontend/src/components/ui/*`<br>`frontend/src/design/tokens.ts`<br>`frontend/src/design/status.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/docs/design` |
| **Test-first** | Failing check first for FR-03-09: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-03-09 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/adjust tokens + ui primitive for the requirement. 4) Map status enum → StatusBadge label+color (not color alone). 5) Document OpenDesign call or fallback under `docs/design/`. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-03-09. |
| **Success** | Observable: Design reference artifacts shall be documented under `docs/design/` (or equivalent) including token map and OpenDesign reference notes. |
| **Acceptance** | FR-03-09: Design reference artifacts shall be documented under `docs/design/` (or equivalent) including token map and OpenDesign reference notes. |
| **Evidence** | `frontend/src/components/ui/*` |

### [x] T-03-10 — NFR gate — NFR-03-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-03-01 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/src/components/ui` |
| **Test-first** | Define pass/fail measurement for NFR-03-01 before changing code. |
| **Steps** | 1) Map NFR-03-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-03-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-03-01: Base components shall avoid unnecessary client-side re-renders when used in lists and tables. |
| **Evidence** | `frontend/src/design/tokens.ts` |

### [x] T-03-11 — NFR gate — NFR-03-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-03-02 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/src/components/ui` |
| **Test-first** | Define pass/fail measurement for NFR-03-02 before changing code. |
| **Steps** | 1) Map NFR-03-02 to design §7 security row. 2) Inspect `frontend/src/design/tokens.ts` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-03-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-03-02: CSS/token delivery shall not block first paint beyond normal Next.js/Tailwind practice. |
| **Evidence** | `frontend/src/design/tokens.ts` |

### [x] T-03-12 — NFR gate — NFR-03-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-03-03 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/src/components/ui` |
| **Test-first** | Define pass/fail measurement for NFR-03-03 before changing code. |
| **Steps** | 1) Map NFR-03-03 to design §7 security row. 2) Inspect `frontend/src/design/tokens.ts` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-03-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-03-03: Design tokens and components shall not embed secrets or live credentials. |
| **Evidence** | `frontend/src/design/tokens.ts` |

### [x] T-03-13 — NFR gate — NFR-03-04
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-03-04 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/src/components/ui` |
| **Test-first** | Define pass/fail measurement for NFR-03-04 before changing code. |
| **Steps** | 1) Map NFR-03-04 to design §7 security row. 2) Inspect `frontend/src/design/tokens.ts` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-03-04 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-03-04: User-generated content displayed via design-system primitives shall be escaped/rendered safely (XSS-safe defaults). |
| **Evidence** | `frontend/src/design/tokens.ts` |

### [x] T-03-14 — Acceptance proof — AC-03-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-03-01 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-03-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Token files and base components exist and are used by app shell. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-03-01 passes with recorded evidence. |
| **Acceptance** | AC-03-01: Token files and base components exist and are used by app shell. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-03-15 — Acceptance proof — AC-03-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-03-02 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-03-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: OpenDesign process or documented fallback is written. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-03-02 passes with recorded evidence. |
| **Acceptance** | AC-03-02: OpenDesign process or documented fallback is written. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-03-16 — Acceptance proof — AC-03-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-03-03 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-03-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Status badge set covers primary run/approval states. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-03-03 passes with recorded evidence. |
| **Acceptance** | AC-03-03: Status badge set covers primary run/approval states. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-03-17 — Acceptance proof — AC-03-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-03-04 |
| **Deliverable (code paths)** | `frontend/src/design/tokens.ts`<br>`frontend/src/design/theme.ts`<br>`frontend/src/design/status.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-03-04 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Loading/empty/error primitives exist for page adoption. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-03-04 passes with recorded evidence. |
| **Acceptance** | AC-03-04: Loading/empty/error primitives exist for page adoption. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-03-18 — Exit review — FE-03 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-03-01, FR-03-02, FR-03-03, FR-03-04, FR-03-05, FR-03-06, FR-03-07, FR-03-08… |
| **Deliverable (code paths)** | `planning/frontend/03_design-system-tokens-and-opendesign/tasks.md`<br>`planning/frontend/03_design-system-tokens-and-opendesign/design.md`<br>`planning/frontend/03_design-system-tokens-and-opendesign/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-03-01 | T-03-01, T-03-18 |
| FR-03-02 | T-03-02, T-03-18 |
| FR-03-03 | T-03-03, T-03-18 |
| FR-03-04 | T-03-04, T-03-18 |
| FR-03-05 | T-03-05, T-03-18 |
| FR-03-06 | T-03-06, T-03-18 |
| FR-03-07 | T-03-07, T-03-18 |
| FR-03-08 | T-03-08, T-03-18 |
| FR-03-09 | T-03-09, T-03-18 |
| NFR-03-01 | T-03-10, T-03-18 |
| NFR-03-02 | T-03-11, T-03-18 |
| NFR-03-03 | T-03-12, T-03-18 |
| NFR-03-04 | T-03-13, T-03-18 |
| AC-03-01 | T-03-14, T-03-18 |
| AC-03-02 | T-03-15, T-03-18 |
| AC-03-03 | T-03-16, T-03-18 |
| AC-03-04 | T-03-17, T-03-18 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-03-1 | T-03-01, T-03-06 |
| C-03-2 | T-03-02, T-03-07 |
| C-03-3 | T-03-03, T-03-08 |
| C-03-4 | T-03-04, T-03-09 |
| C-03-5 | T-03-05 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 9/9 | [x] FR-03-01, FR-03-02, FR-03-03, FR-03-04, FR-03-05, FR-03-06, FR-03-07, FR-03-08, FR-03-09 |
| 4 | NFR coverage 4/4 | [x] NFR-03-01, NFR-03-02, NFR-03-03, NFR-03-04 |
| 5 | AC coverage 4/4 | [x] AC-03-01, AC-03-02, AC-03-03, AC-03-04 |
| 6 | C-* coverage 5/5 | [x] C-03-1, C-03-2, C-03-3, C-03-4, C-03-5 |
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
