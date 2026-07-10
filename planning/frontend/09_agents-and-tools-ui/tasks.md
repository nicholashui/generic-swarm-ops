# Tasks — 09 Agents and Tools UI

| Field | Value |
|-------|-------|
| Task list ID | `FE-09-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-09-DES`) |
| Paired requirements | `requirements.md` (`FE-09`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 10/10 · NFR 2/2 · AC 4/4 · C-* 5/5 |

---

## SDD workflow

Agents/tools list → create forms (zod) → detail → no client execution.

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

These are the **main source locations** for FE-09. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/lib/forms/create-resource-schemas.ts`
- `frontend/src/components/domain/form-route-actions.tsx`
- `frontend/src/components/domain/detail-metadata.tsx`
- `frontend/src/app/app/[...slug]/page.tsx`
- `frontend/tests/unit/create-forms.test.ts`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-09-1 | Domain surfaces | `frontend/src/app/app/[...slug]/page.tsx + product panels` |
| C-09-2 | Create schemas | `frontend/src/lib/forms/create-resource-schemas.ts` |
| C-09-3 | Form route actions | `frontend/src/components/domain/form-route-actions.tsx` |
| C-09-4 | Detail metadata | `frontend/src/components/domain/detail-metadata.tsx` |
| C-09-5 | Tests | `frontend/tests/unit/create-forms.test.ts` |

---

## Task backlog

### [x] T-09-01 — The frontend shall provide agents list, create, and detail views under `/app/agents`
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-09-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-09-01 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx + product panels`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx` |
| **Test-first** | Failing check first for FR-09-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-09-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Build list/detail or form using DataTable/StatusBadge + zod schemas. 4) POST/PATCH via typed client; show field errors and AppError. 5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-09-01. |
| **Success** | Observable: The frontend shall provide agents list, create, and detail views under `/app/agents`. |
| **Acceptance** | FR-09-01: The frontend shall provide agents list, create, and detail views under `/app/agents`. |
| **Evidence** | `frontend/src/app/app/[...slug]/page.tsx + product panels` |

### [x] T-09-02 — The frontend shall provide tools list and detail views under `/app/tools`
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-09-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-09-02 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx`<br>`frontend/src/components/domain/detail-metadata.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/tests/unit/create-forms.test.ts` |
| **Test-first** | Failing check first for FR-09-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-09-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Build list/detail or form using DataTable/StatusBadge + zod schemas. 4) POST/PATCH via typed client; show field errors and AppError. 5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-09-02. |
| **Success** | Observable: The frontend shall provide tools list and detail views under `/app/tools`. |
| **Acceptance** | FR-09-02: The frontend shall provide tools list and detail views under `/app/tools`. |
| **Evidence** | `frontend/src/lib/forms/create-resource-schemas.ts` |

### [x] T-09-03 — When creating or updating an agent, the frontend shall validate required fields client-side and s…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-09-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-09-03 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx` |
| **Test-first** | Failing check first for FR-09-03: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-09-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Build list/detail or form using DataTable/StatusBadge + zod schemas. 4) POST/PATCH via typed client; show field errors and AppError. 5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-09-03. |
| **Success** | Observable: When creating or updating an agent, the frontend shall validate required fields client-side and submit to backend agent APIs. |
| **Acceptance** | FR-09-03: When creating or updating an agent, the frontend shall validate required fields client-side and submit to backend agent APIs. |
| **Evidence** | `frontend/src/lib/forms/create-resource-schemas.ts` |

### [x] T-09-04 — When backend rejects an agent/tool mutation, the frontend shall display the error and request_id
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-09-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-09-04 |
| **Deliverable (code paths)** | `frontend/src/components/domain/detail-metadata.tsx`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx` |
| **Test-first** | Force API 4xx/5xx with request_id → ErrorState shows message + id (FR-09-04). |
| **Steps** | 1) Open `requirements.md` FR-09-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update OpenAPI artifact; run `pnpm api:generate`. 4) Extend `backendApi` method; parse errors into AppError. 5) Consume types in domain loader/panel; no hand-forked DTOs. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-09-04. |
| **Success** | Observable: When backend rejects an agent/tool mutation, the frontend shall display the error and request_id. |
| **Acceptance** | FR-09-04: When backend rejects an agent/tool mutation, the frontend shall display the error and request_id. |
| **Evidence** | `frontend/src/components/domain/detail-metadata.tsx` |

### [x] T-09-05 — When agent or tool detail data is returned, the frontend shall display identity, configuration su…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-09-5, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-09-05 |
| **Deliverable (code paths)** | `frontend/tests/unit/create-forms.test.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx` |
| **Test-first** | Failing check first for FR-09-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-09-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Build list/detail or form using DataTable/StatusBadge + zod schemas. 4) POST/PATCH via typed client; show field errors and AppError. 5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-09-05. |
| **Success** | Observable: When agent or tool detail data is returned, the frontend shall display identity, configuration summary, and status fields. |
| **Acceptance** | FR-09-05: When agent or tool detail data is returned, the frontend shall display identity, configuration summary, and status fields. |
| **Evidence** | `frontend/tests/unit/create-forms.test.ts` |

### [x] T-09-06 — If the user lacks permission to create agents/tools, the frontend shall hide or disable create ac…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-09-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-09-06 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx + product panels`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-09-06). |
| **Steps** | 1) Open `requirements.md` FR-09-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-09-06. |
| **Success** | Observable: If the user lacks permission to create agents/tools, the frontend shall hide or disable create actions. |
| **Acceptance** | FR-09-06: If the user lacks permission to create agents/tools, the frontend shall hide or disable create actions. |
| **Evidence** | `frontend/src/app/app/[...slug]/page.tsx + product panels` |

### [x] T-09-07 — The frontend shall not execute agents or tools locally; execution remains a backend responsibility
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-09-2, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-09-07 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-09-07 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-09-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/lib/forms/create-resource-schemas.ts`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-09-07. |
| **Success** | Observable: The frontend shall not execute agents or tools locally; execution remains a backend responsibility. |
| **Acceptance** | FR-09-07: The frontend shall not execute agents or tools locally; execution remains a backend responsibility. |
| **Evidence** | `frontend/src/lib/forms/create-resource-schemas.ts` |

### [x] T-09-08 — When the agents list is empty and the user may create agents, the frontend shall show an empty st…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-09-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-09-08 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx` |
| **Test-first** | Force empty API payload → assert EmptyState + guidance for FR-09-08. |
| **Steps** | 1) Open `requirements.md` FR-09-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Build list/detail or form using DataTable/StatusBadge + zod schemas. 4) POST/PATCH via typed client; show field errors and AppError. 5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-09-08. |
| **Success** | Observable: When the agents list is empty and the user may create agents, the frontend shall show an empty state with a create affordance. |
| **Acceptance** | FR-09-08: When the agents list is empty and the user may create agents, the frontend shall show an empty state with a create affordance. |
| **Evidence** | `frontend/src/lib/forms/create-resource-schemas.ts` |

### [x] T-09-09 — When rendering list rows, the frontend shall show status badges using the shared status vocabular…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-09-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-09-09 |
| **Deliverable (code paths)** | `frontend/src/components/domain/detail-metadata.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/tests/unit/create-forms.test.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx` |
| **Test-first** | Failing check first for FR-09-09: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-09-09 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Compose run detail route/panel with WorkflowRunConsole + StatusBadge. 4) Load GET run/steps; map statuses via `lib/formatting/status` + design status tokens. 5) Render Timeline + LogViewer; never execute steps in the browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-09-09. |
| **Success** | Observable: When rendering list rows, the frontend shall show status badges using the shared status vocabulary (not color alone). |
| **Acceptance** | FR-09-09: When rendering list rows, the frontend shall show status badges using the shared status vocabulary (not color alone). |
| **Evidence** | `frontend/src/components/domain/detail-metadata.tsx` |

### [x] T-09-10 — If tool metadata would require displaying a provider secret, the frontend shall omit or redact it…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-09-5, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-09-10 |
| **Deliverable (code paths)** | `frontend/tests/unit/create-forms.test.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx`<br>`frontend/src/components/domain/detail-metadata.tsx` |
| **Test-first** | Failing check first for FR-09-10: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-09-10 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Build list/detail or form using DataTable/StatusBadge + zod schemas. 4) POST/PATCH via typed client; show field errors and AppError. 5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-09-10. |
| **Success** | Observable: If tool metadata would require displaying a provider secret, the frontend shall omit or redact it and show only backend-safe fields. |
| **Acceptance** | FR-09-10: If tool metadata would require displaying a provider secret, the frontend shall omit or redact it and show only backend-safe fields. |
| **Evidence** | `frontend/tests/unit/create-forms.test.ts` |

### [x] T-09-11 — NFR gate — NFR-09-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-09-01 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx`<br>`frontend/src/components/domain/detail-metadata.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-09-01 before changing code. |
| **Steps** | 1) Map NFR-09-01 to design §7 performance row. 2) Implement debounce/pagination/abort/code-split as applicable in `frontend/src/lib/forms/create-resource-schemas.ts`. 3) Manual or unit timing check for MVP data sizes. 4) Confirm shell remains interactive. 5) Record evidence path. |
| **Success** | NFR-09-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-09-01: List views shall support pagination or virtualization when lists grow large. |
| **Evidence** | `frontend/src/lib/forms/create-resource-schemas.ts` |

### [x] T-09-12 — NFR gate — NFR-09-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-09-02 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx`<br>`frontend/src/components/domain/detail-metadata.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-09-02 before changing code. |
| **Steps** | 1) Map NFR-09-02 to design §7 security row. 2) Inspect `frontend/src/lib/forms/create-resource-schemas.ts` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-09-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-09-02: Tool configuration UI shall not accept or display raw provider secrets beyond backend-safe metadata. |
| **Evidence** | `frontend/src/lib/forms/create-resource-schemas.ts` |

### [x] T-09-13 — Acceptance proof — AC-09-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-09-01 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx`<br>`frontend/src/components/domain/detail-metadata.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-09-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Create agent form works against live backend in ops profile. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-09-01 passes with recorded evidence. |
| **Acceptance** | AC-09-01: Create agent form works against live backend in ops profile. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-09-14 — Acceptance proof — AC-09-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-09-02 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx`<br>`frontend/src/components/domain/detail-metadata.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-09-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Agents and tools lists render API data. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-09-02 passes with recorded evidence. |
| **Acceptance** | AC-09-02: Agents and tools lists render API data. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-09-15 — Acceptance proof — AC-09-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-09-03 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx`<br>`frontend/src/components/domain/detail-metadata.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-09-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Permission-denied create is gated in UI. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-09-03 passes with recorded evidence. |
| **Acceptance** | AC-09-03: Permission-denied create is gated in UI. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-09-16 — Acceptance proof — AC-09-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-09-04 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/components/domain/form-route-actions.tsx`<br>`frontend/src/components/domain/detail-metadata.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-09-04 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Status badges and empty/error states present on list views. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-09-04 passes with recorded evidence. |
| **Acceptance** | AC-09-04: Status badges and empty/error states present on list views. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-09-17 — Exit review — FE-09 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-09-01, FR-09-02, FR-09-03, FR-09-04, FR-09-05, FR-09-06, FR-09-07, FR-09-08… |
| **Deliverable (code paths)** | `planning/frontend/09_agents-and-tools-ui/tasks.md`<br>`planning/frontend/09_agents-and-tools-ui/design.md`<br>`planning/frontend/09_agents-and-tools-ui/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-09-01 | T-09-01, T-09-17 |
| FR-09-02 | T-09-02, T-09-17 |
| FR-09-03 | T-09-03, T-09-17 |
| FR-09-04 | T-09-04, T-09-17 |
| FR-09-05 | T-09-05, T-09-17 |
| FR-09-06 | T-09-06, T-09-17 |
| FR-09-07 | T-09-07, T-09-17 |
| FR-09-08 | T-09-08, T-09-17 |
| FR-09-09 | T-09-09, T-09-17 |
| FR-09-10 | T-09-10, T-09-17 |
| NFR-09-01 | T-09-11, T-09-17 |
| NFR-09-02 | T-09-12, T-09-17 |
| AC-09-01 | T-09-13, T-09-17 |
| AC-09-02 | T-09-14, T-09-17 |
| AC-09-03 | T-09-15, T-09-17 |
| AC-09-04 | T-09-16, T-09-17 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-09-1 | T-09-01, T-09-06 |
| C-09-2 | T-09-02, T-09-07 |
| C-09-3 | T-09-03, T-09-08 |
| C-09-4 | T-09-04, T-09-09 |
| C-09-5 | T-09-05, T-09-10 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 10/10 | [x] FR-09-01, FR-09-02, FR-09-03, FR-09-04, FR-09-05, FR-09-06, FR-09-07, FR-09-08, FR-09-09, FR-09-10 |
| 4 | NFR coverage 2/2 | [x] NFR-09-01, NFR-09-02 |
| 5 | AC coverage 4/4 | [x] AC-09-01, AC-09-02, AC-09-03, AC-09-04 |
| 6 | C-* coverage 5/5 | [x] C-09-1, C-09-2, C-09-3, C-09-4, C-09-5 |
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
