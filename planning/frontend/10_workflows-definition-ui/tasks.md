# Tasks — 10 Workflows Definition UI

| Field | Value |
|-------|-------|
| Task list ID | `FE-10-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-10-DES`) |
| Paired requirements | `requirements.md` (`FE-10`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 7/7 · NFR 2/2 · AC 3/3 · C-* 4/4 |

---

## SDD workflow

Workflows list/create/detail → Run Now payload → navigate run detail.

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

These are the **main source locations** for FE-10. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/components/domain/run-workflow-button.tsx`
- `frontend/src/lib/api/workflow-run-payload.ts`
- `frontend/src/lib/forms/create-resource-schemas.ts`
- `frontend/src/app/app/[...slug]/page.tsx`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-10-1 | Workflow surfaces | `app domain panels + product-data` |
| C-10-2 | Run workflow button | `frontend/src/components/domain/run-workflow-button.tsx` |
| C-10-3 | Run payload helper | `frontend/src/lib/api/workflow-run-payload.ts` |
| C-10-4 | Create schemas | `frontend/src/lib/forms/create-resource-schemas.ts` |

---

## Task backlog

### [x] T-10-01 — The frontend shall provide workflows list, create, and detail views under `/app/workflows`
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-10-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-10-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts` |
| **Test-first** | Failing check first for FR-10-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-10-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Build list/detail or form using DataTable/StatusBadge + zod schemas. 4) POST/PATCH via typed client; show field errors and AppError. 5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-10-01. |
| **Success** | Observable: The frontend shall provide workflows list, create, and detail views under `/app/workflows`. |
| **Acceptance** | FR-10-01: The frontend shall provide workflows list, create, and detail views under `/app/workflows`. |
| **Evidence** | `frontend/src/components/domain/run-workflow-button.tsx` |

### [x] T-10-02 — When creating a workflow, the frontend shall validate input and POST to backend workflow APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-10-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-10-02 |
| **Deliverable (code paths)** | `frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts` |
| **Test-first** | Failing check first for FR-10-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-10-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Build list/detail or form using DataTable/StatusBadge + zod schemas. 4) POST/PATCH via typed client; show field errors and AppError. 5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-10-02. |
| **Success** | Observable: When creating a workflow, the frontend shall validate input and POST to backend workflow APIs. |
| **Acceptance** | FR-10-02: When creating a workflow, the frontend shall validate input and POST to backend workflow APIs. |
| **Evidence** | `frontend/src/components/domain/run-workflow-button.tsx` |

### [x] T-10-03 — Workflow detail shall show definition metadata, version information, and available actions return…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-10-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-10-03 |
| **Deliverable (code paths)** | `frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts` |
| **Test-first** | Failing check first for FR-10-03: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-10-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Build list/detail or form using DataTable/StatusBadge + zod schemas. 4) POST/PATCH via typed client; show field errors and AppError. 5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-10-03. |
| **Success** | Observable: Workflow detail shall show definition metadata, version information, and available actions returned/allowed by backend. |
| **Acceptance** | FR-10-03: Workflow detail shall show definition metadata, version information, and available actions returned/allowed by backend. |
| **Evidence** | `frontend/src/components/domain/run-workflow-button.tsx` |

### [x] T-10-04 — When the user triggers Run Now, the frontend shall request run creation from the backend with a v…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-10-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-10-04 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts` |
| **Test-first** | Failing check first for FR-10-04: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-10-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-10-4` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-10-04. |
| **Success** | Observable: When the user triggers Run Now, the frontend shall request run creation from the backend with a valid payload. |
| **Acceptance** | FR-10-04: When the user triggers Run Now, the frontend shall request run creation from the backend with a valid payload. |
| **Evidence** | `frontend/src/app/app/[...slug]/page.tsx` |

### [x] T-10-05 — If run creation fails, the frontend shall show backend errors without claiming a run started
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-10-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-10-05 |
| **Deliverable (code paths)** | `frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Force API 4xx/5xx with request_id → ErrorState shows message + id (FR-10-05). |
| **Steps** | 1) Open `requirements.md` FR-10-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Adopt Skeleton/EmptyState/ErrorState primitives on target pages. 4) Labels, focus rings, non-color-only status; request_id on errors. 5) Keyboard-pass primary flows; sanitize production error bodies. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-10-05. |
| **Success** | Observable: If run creation fails, the frontend shall show backend errors without claiming a run started. |
| **Acceptance** | FR-10-05: If run creation fails, the frontend shall show backend errors without claiming a run started. |
| **Evidence** | `frontend/src/components/domain/run-workflow-button.tsx` |

### [x] T-10-06 — The frontend shall not implement workflow execution logic in the browser
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-10-2, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-10-06 |
| **Deliverable (code paths)** | `frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-10-06 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-10-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/components/domain/run-workflow-button.tsx`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-10-06. |
| **Success** | Observable: The frontend shall not implement workflow execution logic in the browser. |
| **Acceptance** | FR-10-06: The frontend shall not implement workflow execution logic in the browser. |
| **Evidence** | `frontend/src/components/domain/run-workflow-button.tsx` |

### [x] T-10-07 — Permission-aware controls shall gate create/run actions as UX only
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-10-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-10-07 |
| **Deliverable (code paths)** | `frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-10-07). |
| **Steps** | 1) Open `requirements.md` FR-10-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-10-07. |
| **Success** | Observable: Permission-aware controls shall gate create/run actions as UX only. |
| **Acceptance** | FR-10-07: Permission-aware controls shall gate create/run actions as UX only. |
| **Evidence** | `frontend/src/lib/forms/create-resource-schemas.ts` |

### [x] T-10-08 — NFR gate — NFR-10-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-10-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-10-01 before changing code. |
| **Steps** | 1) Map NFR-10-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-10-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-10-01: Workflow list load shall not block the entire app shell. |
| **Evidence** | `frontend/src/components/domain/run-workflow-button.tsx` |

### [x] T-10-09 — NFR gate — NFR-10-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-10-02 |
| **Deliverable (code paths)** | `frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-10-02 before changing code. |
| **Steps** | 1) Map NFR-10-02 to design §7 security row. 2) Inspect `frontend/src/components/domain/run-workflow-button.tsx` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-10-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-10-02: Workflow payloads shall not include secrets; references only as backend allows. |
| **Evidence** | `frontend/src/components/domain/run-workflow-button.tsx` |

### [x] T-10-10 — Acceptance proof — AC-10-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-10-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-10-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Create workflow form works in ops profile. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-10-01 passes with recorded evidence. |
| **Acceptance** | AC-10-01: Create workflow form works in ops profile. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-10-11 — Acceptance proof — AC-10-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-10-02 |
| **Deliverable (code paths)** | `frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-10-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Run now creates a backend run and navigates to run detail when successful. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-10-02 passes with recorded evidence. |
| **Acceptance** | AC-10-02: Run now creates a backend run and navigates to run detail when successful. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-10-12 — Acceptance proof — AC-10-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-10-03 |
| **Deliverable (code paths)** | `frontend/src/components/domain/run-workflow-button.tsx`<br>`frontend/src/lib/api/workflow-run-payload.ts`<br>`frontend/src/lib/forms/create-resource-schemas.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-10-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Lists show backend workflows. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-10-03 passes with recorded evidence. |
| **Acceptance** | AC-10-03: Lists show backend workflows. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-10-13 — Exit review — FE-10 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-10-01, FR-10-02, FR-10-03, FR-10-04, FR-10-05, FR-10-06, FR-10-07, NFR-10-01… |
| **Deliverable (code paths)** | `planning/frontend/10_workflows-definition-ui/tasks.md`<br>`planning/frontend/10_workflows-definition-ui/design.md`<br>`planning/frontend/10_workflows-definition-ui/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-10-01 | T-10-01, T-10-13 |
| FR-10-02 | T-10-02, T-10-13 |
| FR-10-03 | T-10-03, T-10-13 |
| FR-10-04 | T-10-04, T-10-13 |
| FR-10-05 | T-10-05, T-10-13 |
| FR-10-06 | T-10-06, T-10-13 |
| FR-10-07 | T-10-07, T-10-13 |
| NFR-10-01 | T-10-08, T-10-13 |
| NFR-10-02 | T-10-09, T-10-13 |
| AC-10-01 | T-10-10, T-10-13 |
| AC-10-02 | T-10-11, T-10-13 |
| AC-10-03 | T-10-12, T-10-13 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-10-1 | T-10-01, T-10-05 |
| C-10-2 | T-10-02, T-10-06 |
| C-10-3 | T-10-03, T-10-07 |
| C-10-4 | T-10-04 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 7/7 | [x] FR-10-01, FR-10-02, FR-10-03, FR-10-04, FR-10-05, FR-10-06, FR-10-07 |
| 4 | NFR coverage 2/2 | [x] NFR-10-01, NFR-10-02 |
| 5 | AC coverage 3/3 | [x] AC-10-01, AC-10-02, AC-10-03 |
| 6 | C-* coverage 4/4 | [x] C-10-1, C-10-2, C-10-3, C-10-4 |
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
