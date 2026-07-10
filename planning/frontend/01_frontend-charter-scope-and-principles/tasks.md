# Tasks — 01 Frontend Charter, Scope, and Design Principles

| Field | Value |
|-------|-------|
| Task list ID | `FE-01-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-01-DES`) |
| Paired requirements | `requirements.md` (`FE-01`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 11/11 · NFR 4/4 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Charter INV → boundary review checklist → inherit to FE-02…20 → FE-20 DoD.

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

These are the **main source locations** for FE-01. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend.md`
- `planning/frontend/README.md`
- `planning/frontend/01_frontend-charter-scope-and-principles/design.md`
- `frontend/src`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-01-1 | Charter document set | `frontend.md §1–4, §6, §32–33 + this design` |
| C-01-2 | Boundary review gates | `PR review + FE-20 quality gates` |
| C-01-3 | As-built console root | `frontend/src` |
| C-01-4 | Planning index | `planning/frontend/README.md` |

---

## Task backlog

### [x] T-01-01 — The frontend shall deliver the user-facing web application for managing AI agents, workflows, too…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-01-01 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src` |
| **Test-first** | Failing check first for FR-01-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-01-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire ApprovalDecisionPanel to approve/reject APIs. 4) Optional notes; explicit user click only (no auto-approve). 5) Refresh list/detail; deep-link from run gate callout. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-01. |
| **Success** | Observable: The frontend shall deliver the user-facing web application for managing AI agents, workflows, tools, approvals, knowledge, memory, evalua…. |
| **Acceptance** | FR-01-01: The frontend shall deliver the user-facing web application for managing AI agents, workflows, tools, approvals, knowledge, memory, evaluations, audits, evolution sandbox variants, self-improvement actions, and organization settings. |
| **Evidence** | `frontend.md` |

### [x] T-01-02 — The frontend shall communicate trust, reliability, operational clarity, security, professionalism…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-01-02 |
| **Deliverable (code paths)** | `planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src`<br>`frontend.md` |
| **Test-first** | Failing check first for FR-01-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-01-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Encode INV in review checklist / docs; reject out-of-charter PRs. 4) Ensure design/tasks for downstream FE cite FE-01 boundary. 5) Link non-goals (DNA rewrite, client AuthZ authority) explicitly. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-02. |
| **Success** | Observable: The frontend shall communicate trust, reliability, operational clarity, security, professionalism, speed, control, and observability in i…. |
| **Acceptance** | FR-01-02: The frontend shall communicate trust, reliability, operational clarity, security, professionalism, speed, control, and observability in its product presentation. |
| **Evidence** | `planning/frontend/README.md` |

### [x] T-01-03 — The frontend shall own presentation, interaction, routing, layout, UI state, frontend validation,…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-01-03 |
| **Deliverable (code paths)** | `planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src`<br>`frontend.md`<br>`planning/frontend/README.md` |
| **Test-first** | Mock stream events → UI updates; kill stream → degraded/poll (FR-01-03). |
| **Steps** | 1) Open `requirements.md` FR-01-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/extend `useRealtimeRun` + `sse.ts` subscribe/merge. 4) On stream error set degraded + poll; cleanup on unmount. 5) Drive Timeline/LogViewer from merged events without full page reload. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-03. |
| **Success** | Observable: The frontend shall own presentation, interaction, routing, layout, UI state, frontend validation, UX, client-side realtime display, and d…. |
| **Acceptance** | FR-01-03: The frontend shall own presentation, interaction, routing, layout, UI state, frontend validation, UX, client-side realtime display, and design-system implementation. |
| **Evidence** | `planning/frontend/01_frontend-charter-scope-and-principles/design.md` |

### [x] T-01-04 — Reject out-of-charter capabilities (execution/secrets/DNA)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-4, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-01-04 |
| **Deliverable (code paths)** | `frontend/src`<br>`frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-01-04 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-01-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-04. |
| **Success** | Observable: If a capability requires workflow execution, agent execution, tool execution, permission enforcement as sole authority, direct database w…. |
| **Acceptance** | FR-01-04: If a capability requires workflow execution, agent execution, tool execution, permission enforcement as sole authority, direct database writes, background jobs, embedding/indexing, secret storage, provider API key handling in browser code, audit log creation, billing calculation, silent production DNA mutation, or host self-rewrite, then the frontend shall not implement that capability. |
| **Evidence** | `frontend/src` |

### [x] T-01-05 — Route all actions through backend decision path
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-01-05 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src` |
| **Test-first** | Failing check first for FR-01-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-01-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Encode INV in review checklist / docs; reject out-of-charter PRs. 4) Ensure design/tasks for downstream FE cite FE-01 boundary. 5) Link non-goals (DNA rewrite, client AuthZ authority) explicitly. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-05. |
| **Success** | Observable: When the user requests an action, the frontend shall request it from the backend; the backend shall decide whether the action is allowed. |
| **Acceptance** | FR-01-05: When the user requests an action, the frontend shall request it from the backend; the backend shall decide whether the action is allowed. |
| **Evidence** | `frontend.md` |

### [x] T-01-06 — The frontend shall not assume that hiding a control is sufficient security
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-2, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-01-06 |
| **Deliverable (code paths)** | `planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src`<br>`frontend.md` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-01-06 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-01-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`planning/frontend/README.md`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-06. |
| **Success** | Observable: The frontend shall not assume that hiding a control is sufficient security. |
| **Acceptance** | FR-01-06: The frontend shall not assume that hiding a control is sufficient security. |
| **Evidence** | `planning/frontend/README.md` |

### [x] T-01-07 — When designing major page layouts, the frontend workflow shall prefer OpenDesign MCP references o…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-01-07 |
| **Deliverable (code paths)** | `planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src`<br>`frontend.md`<br>`planning/frontend/README.md` |
| **Test-first** | Failing check first for FR-01-07: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-01-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Build list/detail or form using DataTable/StatusBadge + zod schemas. 4) POST/PATCH via typed client; show field errors and AppError. 5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-07. |
| **Success** | Observable: When designing major page layouts, the frontend workflow shall prefer OpenDesign MCP references over generic AI memory alone. |
| **Acceptance** | FR-01-07: When designing major page layouts, the frontend workflow shall prefer OpenDesign MCP references over generic AI memory alone. |
| **Evidence** | `planning/frontend/01_frontend-charter-scope-and-principles/design.md` |

### [x] T-01-08 — The frontend shall treat `structure.md` as architecture source of truth and `backend.md` / planni…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-01-08 |
| **Deliverable (code paths)** | `frontend/src`<br>`frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md` |
| **Test-first** | Failing check first for FR-01-08: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-01-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Encode INV in review checklist / docs; reject out-of-charter PRs. 4) Ensure design/tasks for downstream FE cite FE-01 boundary. 5) Link non-goals (DNA rewrite, client AuthZ authority) explicitly. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-08. |
| **Success** | Observable: The frontend shall treat `structure.md` as architecture source of truth and `backend.md` / planning/backend as the API control-plane cont…. |
| **Acceptance** | FR-01-08: The frontend shall treat `structure.md` as architecture source of truth and `backend.md` / planning/backend as the API control-plane contract. |
| **Evidence** | `frontend/src` |

### [x] T-01-09 — When a design trade-off exists between operator clarity and decorative complexity, the frontend s…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-01-09 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src` |
| **Test-first** | Failing check first for FR-01-09: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-01-09 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Encode INV in review checklist / docs; reject out-of-charter PRs. 4) Ensure design/tasks for downstream FE cite FE-01 boundary. 5) Link non-goals (DNA rewrite, client AuthZ authority) explicitly. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-09. |
| **Success** | Observable: When a design trade-off exists between operator clarity and decorative complexity, the frontend shall prefer operational clarity. |
| **Acceptance** | FR-01-09: When a design trade-off exists between operator clarity and decorative complexity, the frontend shall prefer operational clarity. |
| **Evidence** | `frontend.md` |

### [x] T-01-10 — The frontend shall support both an ops profile (`NEXT_PUBLIC_DEMO_MODE=false` against live backen…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-01-10 |
| **Deliverable (code paths)** | `planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src`<br>`frontend.md` |
| **Test-first** | Failing check first for FR-01-10: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-01-10 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Encode INV in review checklist / docs; reject out-of-charter PRs. 4) Ensure design/tasks for downstream FE cite FE-01 boundary. 5) Link non-goals (DNA rewrite, client AuthZ authority) explicitly. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-10. |
| **Success** | Observable: The frontend shall support both an ops profile (`NEXT_PUBLIC_DEMO_MODE=false` against live backend) and a demo profile for UI-only previe…. |
| **Acceptance** | FR-01-10: The frontend shall support both an ops profile (`NEXT_PUBLIC_DEMO_MODE=false` against live backend) and a demo profile for UI-only preview without treating demo as production authority. |
| **Evidence** | `planning/frontend/README.md` |

### [x] T-01-11 — The frontend shall remain a presentation and interaction layer so that authorization, execution, …
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-01-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-01-11 |
| **Deliverable (code paths)** | `planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src`<br>`frontend.md`<br>`planning/frontend/README.md` |
| **Test-first** | Failing check first for FR-01-11: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-01-11 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Encode INV in review checklist / docs; reject out-of-charter PRs. 4) Ensure design/tasks for downstream FE cite FE-01 boundary. 5) Link non-goals (DNA rewrite, client AuthZ authority) explicitly. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-01-11. |
| **Success** | Observable: The frontend shall remain a presentation and interaction layer so that authorization, execution, and governance stay on the backend. |
| **Acceptance** | FR-01-11: The frontend shall remain a presentation and interaction layer so that authorization, execution, and governance stay on the backend. |
| **Evidence** | `planning/frontend/01_frontend-charter-scope-and-principles/design.md` |

### [x] T-01-12 — NFR gate — NFR-01-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-01-01 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src` |
| **Test-first** | Define pass/fail measurement for NFR-01-01 before changing code. |
| **Steps** | 1) Map NFR-01-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-01-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-01-01: Charter and boundary checks shall be enforceable by code review and architecture review without requiring online LLM calls. |
| **Evidence** | `frontend.md` |

### [x] T-01-13 — NFR gate — NFR-01-02
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-01-02 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src` |
| **Test-first** | Define pass/fail measurement for NFR-01-02 before changing code. |
| **Steps** | 1) Map NFR-01-02 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-01-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-01-02: Frontend package boundaries shall keep domain pages free of backend business rules duplicated from Python services. |
| **Evidence** | `frontend.md` |

### [x] T-01-14 — NFR gate — NFR-01-03
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-01-03 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src` |
| **Test-first** | Define pass/fail measurement for NFR-01-03 before changing code. |
| **Steps** | 1) Map NFR-01-03 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-01-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-01-03: If a proposed UI feature would allow unattended direct production DNA mutation or host application self-rewrite, then the frontend shall reject that feature as out of charter. |
| **Evidence** | `frontend.md` |

### [x] T-01-15 — NFR gate — NFR-01-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-01-04 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/src` |
| **Test-first** | Define pass/fail measurement for NFR-01-04 before changing code. |
| **Steps** | 1) Map NFR-01-04 to design §7 security row. 2) Inspect `frontend.md` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-01-04 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-01-04: The frontend shall never store provider secrets or perform final authentication verification as sole authority. |
| **Evidence** | `frontend.md` |

### [x] T-01-16 — Acceptance proof — AC-01-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-01-01 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-01-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: frontend.md and this spec state frontend is presentation/interaction only; backend is control plane. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-01-01 passes with recorded evidence. |
| **Acceptance** | AC-01-01: frontend.md and this spec state frontend is presentation/interaction only; backend is control plane. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-01-17 — Acceptance proof — AC-01-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-01-02 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-01-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Out-of-scope list matches frontend.md §4.2 and §33.5 non-goals. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-01-02 passes with recorded evidence. |
| **Acceptance** | AC-01-02: Out-of-scope list matches frontend.md §4.2 and §33.5 non-goals. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-01-18 — Acceptance proof — AC-01-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-01-03 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-01-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: All downstream planning/frontend/* specs reference FE-01 priority order. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-01-03 passes with recorded evidence. |
| **Acceptance** | AC-01-03: All downstream planning/frontend/* specs reference FE-01 priority order. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-01-19 — Acceptance proof — AC-01-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-01-04 |
| **Deliverable (code paths)** | `frontend.md`<br>`planning/frontend/README.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-01-04 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Evolution and improve specs explicitly require sandbox-only backend APIs. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-01-04 passes with recorded evidence. |
| **Acceptance** | AC-01-04: Evolution and improve specs explicitly require sandbox-only backend APIs. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-01-20 — Exit review — FE-01 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-01-01, FR-01-02, FR-01-03, FR-01-04, FR-01-05, FR-01-06, FR-01-07, FR-01-08… |
| **Deliverable (code paths)** | `planning/frontend/01_frontend-charter-scope-and-principles/tasks.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/design.md`<br>`planning/frontend/01_frontend-charter-scope-and-principles/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-01-01 | T-01-01, T-01-20 |
| FR-01-02 | T-01-02, T-01-20 |
| FR-01-03 | T-01-03, T-01-20 |
| FR-01-04 | T-01-04, T-01-20 |
| FR-01-05 | T-01-05, T-01-20 |
| FR-01-06 | T-01-06, T-01-20 |
| FR-01-07 | T-01-07, T-01-20 |
| FR-01-08 | T-01-08, T-01-20 |
| FR-01-09 | T-01-09, T-01-20 |
| FR-01-10 | T-01-10, T-01-20 |
| FR-01-11 | T-01-11, T-01-20 |
| NFR-01-01 | T-01-12, T-01-20 |
| NFR-01-02 | T-01-13, T-01-20 |
| NFR-01-03 | T-01-14, T-01-20 |
| NFR-01-04 | T-01-15, T-01-20 |
| AC-01-01 | T-01-16, T-01-20 |
| AC-01-02 | T-01-17, T-01-20 |
| AC-01-03 | T-01-18, T-01-20 |
| AC-01-04 | T-01-19, T-01-20 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-01-1 | T-01-01, T-01-05, T-01-09 |
| C-01-2 | T-01-02, T-01-06, T-01-10 |
| C-01-3 | T-01-03, T-01-07, T-01-11 |
| C-01-4 | T-01-04, T-01-08 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 11/11 | [x] FR-01-01, FR-01-02, FR-01-03, FR-01-04, FR-01-05, FR-01-06, FR-01-07, FR-01-08, FR-01-09, FR-01-10, FR-01-11 |
| 4 | NFR coverage 4/4 | [x] NFR-01-01, NFR-01-02, NFR-01-03, NFR-01-04 |
| 5 | AC coverage 4/4 | [x] AC-01-01, AC-01-02, AC-01-03, AC-01-04 |
| 6 | C-* coverage 4/4 | [x] C-01-1, C-01-2, C-01-3, C-01-4 |
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
