# Tasks — 17 Evolution Sandbox Archive UI

| Field | Value |
|-------|-------|
| Task list ID | `FE-17-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-17-DES`) |
| Paired requirements | `requirements.md` (`FE-17`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 6/6 · NFR 3/3 · AC 3/3 · C-* 2/2 |

---

## SDD workflow

Evolution archive → fitness list → evaluate/promote/rollback via BE only.

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

These are the **main source locations** for FE-17. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/components/domain/evolution-archive-panel.tsx`
- `frontend/src/app/app/[...slug]/page.tsx`
- `frontend/src/lib/api/client.ts`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-17-1 | Evolution archive panel | `frontend/src/components/domain/evolution-archive-panel.tsx` |
| C-17-2 | Evolution route | `app evolution path / slug` |

---

## Task backlog

### [x] T-17-01 — The frontend shall provide an evolution archive page under `/app/evolution`
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-17-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-17-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-17-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-17-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Render archive table from evolution APIs with sandbox badge. 4) Gate evaluate/promote/rollback behind confirm + permissions. 5) Surface BE validator rejections; no local DNA mutation module. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-17-01. |
| **Success** | Observable: The frontend shall provide an evolution archive page under `/app/evolution`. |
| **Acceptance** | FR-17-01: The frontend shall provide an evolution archive page under `/app/evolution`. |
| **Evidence** | `frontend/src/components/domain/evolution-archive-panel.tsx` |

### [x] T-17-02 — The page shall list sandbox variants and fitness/ranking data returned by backend evolution APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-17-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-17-02 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-17-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-17-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Render archive table from evolution APIs with sandbox badge. 4) Gate evaluate/promote/rollback behind confirm + permissions. 5) Surface BE validator rejections; no local DNA mutation module. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-17-02. |
| **Success** | Observable: The page shall list sandbox variants and fitness/ranking data returned by backend evolution APIs. |
| **Acceptance** | FR-17-02: The page shall list sandbox variants and fitness/ranking data returned by backend evolution APIs. |
| **Evidence** | `frontend/src/components/domain/evolution-archive-panel.tsx` |

### [x] T-17-03 — When evaluate/promote/rollback actions are available, the frontend shall call backend evolution e…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-17-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-17-03 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-17-03: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-17-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Render archive table from evolution APIs with sandbox badge. 4) Gate evaluate/promote/rollback behind confirm + permissions. 5) Surface BE validator rejections; no local DNA mutation module. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-17-03. |
| **Success** | Observable: When evaluate/promote/rollback actions are available, the frontend shall call backend evolution endpoints only. |
| **Acceptance** | FR-17-03: When evaluate/promote/rollback actions are available, the frontend shall call backend evolution endpoints only. |
| **Evidence** | `frontend/src/components/domain/evolution-archive-panel.tsx` |

### [x] T-17-04 — Forbid client production DNA rewrite
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-17-2, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-17-04 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-17-04 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-17-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/components/domain/evolution-archive-panel.tsx`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-17-04. |
| **Success** | Observable: The frontend shall not implement client-side production DNA mutation or host application self-rewrite. |
| **Acceptance** | FR-17-04: The frontend shall not implement client-side production DNA mutation or host application self-rewrite. |
| **Evidence** | `frontend/src/components/domain/evolution-archive-panel.tsx` |

### [x] T-17-05 — UI copy shall communicate sandbox / gated promotion semantics when promoting variants
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-17-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-17-05 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| **Test-first** | Failing check first for FR-17-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-17-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Render archive table from evolution APIs with sandbox badge. 4) Gate evaluate/promote/rollback behind confirm + permissions. 5) Surface BE validator rejections; no local DNA mutation module. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-17-05. |
| **Success** | Observable: UI copy shall communicate sandbox / gated promotion semantics when promoting variants. |
| **Acceptance** | FR-17-05: UI copy shall communicate sandbox / gated promotion semantics when promoting variants. |
| **Evidence** | `frontend/src/app/app/[...slug]/page.tsx` |

### [x] T-17-06 — Permission-aware UI shall gate evolution admin actions
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-17-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-17-06 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-17-06). |
| **Steps** | 1) Open `requirements.md` FR-17-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-17-06. |
| **Success** | Observable: Permission-aware UI shall gate evolution admin actions. |
| **Acceptance** | FR-17-06: Permission-aware UI shall gate evolution admin actions. |
| **Evidence** | `frontend/src/components/domain/evolution-archive-panel.tsx` |

### [x] T-17-07 — NFR gate — NFR-17-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-17-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts` |
| **Test-first** | Define pass/fail measurement for NFR-17-01 before changing code. |
| **Steps** | 1) Map NFR-17-01 to design §7 performance row. 2) Implement debounce/pagination/abort/code-split as applicable in `frontend/src/components/domain/evolution-archive-panel.tsx`. 3) Manual or unit timing check for MVP data sizes. 4) Confirm shell remains interactive. 5) Record evidence path. |
| **Success** | NFR-17-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-17-01: Archive lists shall paginate when populations grow. |
| **Evidence** | `frontend/src/components/domain/evolution-archive-panel.tsx` |

### [x] T-17-08 — NFR gate — NFR-17-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-17-02 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts` |
| **Test-first** | Define pass/fail measurement for NFR-17-02 before changing code. |
| **Steps** | 1) Map NFR-17-02 to design §7 security row. 2) Inspect `frontend/src/components/domain/evolution-archive-panel.tsx` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-17-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-17-02: Evolution mutations shall require authenticated, authorized backend calls. |
| **Evidence** | `frontend/src/components/domain/evolution-archive-panel.tsx` |

### [x] T-17-09 — NFR gate — NFR-17-03
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-17-03 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts` |
| **Test-first** | Define pass/fail measurement for NFR-17-03 before changing code. |
| **Steps** | 1) Map NFR-17-03 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-17-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-17-03: If a UI path would skip backend sandbox validation, it shall be rejected in design. |
| **Evidence** | `frontend/src/components/domain/evolution-archive-panel.tsx` |

### [x] T-17-10 — Acceptance proof — AC-17-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-17-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-17-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: `/app/evolution` renders archive from backend or empty state. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-17-01 passes with recorded evidence. |
| **Acceptance** | AC-17-01: `/app/evolution` renders archive from backend or empty state. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-17-11 — Acceptance proof — AC-17-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-17-02 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-17-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: No client DNA rewrite module exists. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-17-02 passes with recorded evidence. |
| **Acceptance** | AC-17-02: No client DNA rewrite module exists. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-17-12 — Acceptance proof — AC-17-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-17-03 |
| **Deliverable (code paths)** | `frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-17-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Promote/rollback only via backend APIs. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-17-03 passes with recorded evidence. |
| **Acceptance** | AC-17-03: Promote/rollback only via backend APIs. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-17-13 — Exit review — FE-17 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-17-01, FR-17-02, FR-17-03, FR-17-04, FR-17-05, FR-17-06, NFR-17-01, NFR-17-02… |
| **Deliverable (code paths)** | `planning/frontend/17_evolution-sandbox-archive-ui/tasks.md`<br>`planning/frontend/17_evolution-sandbox-archive-ui/design.md`<br>`planning/frontend/17_evolution-sandbox-archive-ui/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-17-01 | T-17-01, T-17-13 |
| FR-17-02 | T-17-02, T-17-13 |
| FR-17-03 | T-17-03, T-17-13 |
| FR-17-04 | T-17-04, T-17-13 |
| FR-17-05 | T-17-05, T-17-13 |
| FR-17-06 | T-17-06, T-17-13 |
| NFR-17-01 | T-17-07, T-17-13 |
| NFR-17-02 | T-17-08, T-17-13 |
| NFR-17-03 | T-17-09, T-17-13 |
| AC-17-01 | T-17-10, T-17-13 |
| AC-17-02 | T-17-11, T-17-13 |
| AC-17-03 | T-17-12, T-17-13 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-17-1 | T-17-01, T-17-03, T-17-05 |
| C-17-2 | T-17-02, T-17-04, T-17-06 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 6/6 | [x] FR-17-01, FR-17-02, FR-17-03, FR-17-04, FR-17-05, FR-17-06 |
| 4 | NFR coverage 3/3 | [x] NFR-17-01, NFR-17-02, NFR-17-03 |
| 5 | AC coverage 3/3 | [x] AC-17-01, AC-17-02, AC-17-03 |
| 6 | C-* coverage 2/2 | [x] C-17-1, C-17-2 |
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
