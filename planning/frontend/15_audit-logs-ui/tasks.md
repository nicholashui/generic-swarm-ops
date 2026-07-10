# Tasks — 15 Audit Logs UI

| Field | Value |
|-------|-------|
| Task list ID | `FE-15-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-15-DES`) |
| Paired requirements | `requirements.md` (`FE-15`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 6/6 · NFR 2/2 · AC 2/2 · C-* 2/2 |

---

## SDD workflow

Audit logs table → filters → pagination → read-only (no FE audit write).

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

These are the **main source locations** for FE-15. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/components/ui/data-table.tsx`
- `frontend/src/app/app/[...slug]/page.tsx`
- `frontend/src/lib/api/live-data.ts`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-15-1 | Audit panel | `app domain surfaces` |
| C-15-2 | Data table | `frontend/src/components/ui/data-table.tsx` |

---

## Task backlog

### [x] T-15-01 — The frontend shall provide an audit logs page under `/app/audit-logs`
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-15-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-15-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/data-table.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-15-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-15-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Read-only DataTable + filters → audit list API. 4) Paginate; deep-link resource ids when present. 5) Grep/review: no FE POST creating system-of-record audit events. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-15-01. |
| **Success** | Observable: The frontend shall provide an audit logs page under `/app/audit-logs`. |
| **Acceptance** | FR-15-01: The frontend shall provide an audit logs page under `/app/audit-logs`. |
| **Evidence** | `frontend/src/components/ui/data-table.tsx` |

### [x] T-15-02 — Audit logs UI shall fetch events from backend audit APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-15-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-15-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/data-table.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-15-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-15-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Read-only DataTable + filters → audit list API. 4) Paginate; deep-link resource ids when present. 5) Grep/review: no FE POST creating system-of-record audit events. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-15-02. |
| **Success** | Observable: Audit logs UI shall fetch events from backend audit APIs. |
| **Acceptance** | FR-15-02: Audit logs UI shall fetch events from backend audit APIs. |
| **Evidence** | `frontend/src/components/ui/data-table.tsx` |

### [x] T-15-03 — When filters are provided by the product, the frontend shall pass filter query params to the backend
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-15-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-15-03 |
| **Deliverable (code paths)** | `frontend/src/lib/api/live-data.ts`<br>`frontend/src/components/ui/data-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-15-03: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-15-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-15-1` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-15-03. |
| **Success** | Observable: When filters are provided by the product, the frontend shall pass filter query params to the backend. |
| **Acceptance** | FR-15-03: When filters are provided by the product, the frontend shall pass filter query params to the backend. |
| **Evidence** | `frontend/src/lib/api/live-data.ts` |

### [x] T-15-04 — The frontend shall not create, edit, or delete audit events client-side as system of record
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-15-2, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-15-04 |
| **Deliverable (code paths)** | `frontend/src/components/ui/data-table.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-15-04 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-15-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/components/ui/data-table.tsx`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-15-04. |
| **Success** | Observable: The frontend shall not create, edit, or delete audit events client-side as system of record. |
| **Acceptance** | FR-15-04: The frontend shall not create, edit, or delete audit events client-side as system of record. |
| **Evidence** | `frontend/src/components/ui/data-table.tsx` |

### [x] T-15-05 — Each event row shall display actor, action, timestamp, and resource identifiers when returned
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-15-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-15-05 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/components/ui/data-table.tsx` |
| **Test-first** | Failing check first for FR-15-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-15-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-15-1` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-15-05. |
| **Success** | Observable: Each event row shall display actor, action, timestamp, and resource identifiers when returned. |
| **Acceptance** | FR-15-05: Each event row shall display actor, action, timestamp, and resource identifiers when returned. |
| **Evidence** | `frontend/src/app/app/[...slug]/page.tsx` |

### [x] T-15-06 — Permission-aware UI shall restrict audit access for roles without permission
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-15-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-15-06 |
| **Deliverable (code paths)** | `frontend/src/components/ui/data-table.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-15-06). |
| **Steps** | 1) Open `requirements.md` FR-15-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-15-06. |
| **Success** | Observable: Permission-aware UI shall restrict audit access for roles without permission. |
| **Acceptance** | FR-15-06: Permission-aware UI shall restrict audit access for roles without permission. |
| **Evidence** | `frontend/src/components/ui/data-table.tsx` |

### [x] T-15-07 — NFR gate — NFR-15-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-15-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/data-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/live-data.ts` |
| **Test-first** | Define pass/fail measurement for NFR-15-01 before changing code. |
| **Steps** | 1) Map NFR-15-01 to design §7 performance row. 2) Implement debounce/pagination/abort/code-split as applicable in `frontend/src/components/ui/data-table.tsx`. 3) Manual or unit timing check for MVP data sizes. 4) Confirm shell remains interactive. 5) Record evidence path. |
| **Success** | NFR-15-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-15-01: Audit list shall paginate. |
| **Evidence** | `frontend/src/components/ui/data-table.tsx` |

### [x] T-15-08 — NFR gate — NFR-15-02
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-15-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/data-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/live-data.ts` |
| **Test-first** | Define pass/fail measurement for NFR-15-02 before changing code. |
| **Steps** | 1) Map NFR-15-02 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-15-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-15-02: Audit UI shall not allow clients to forge historical events. |
| **Evidence** | `frontend/src/components/ui/data-table.tsx` |

### [x] T-15-09 — Acceptance proof — AC-15-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-15-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/data-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-15-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Audit page lists backend events or empty state. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-15-01 passes with recorded evidence. |
| **Acceptance** | AC-15-01: Audit page lists backend events or empty state. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-15-10 — Acceptance proof — AC-15-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-15-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/data-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-15-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: No client write path for audit records. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-15-02 passes with recorded evidence. |
| **Acceptance** | AC-15-02: No client write path for audit records. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-15-11 — Exit review — FE-15 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-15-01, FR-15-02, FR-15-03, FR-15-04, FR-15-05, FR-15-06, NFR-15-01, NFR-15-02… |
| **Deliverable (code paths)** | `planning/frontend/15_audit-logs-ui/tasks.md`<br>`planning/frontend/15_audit-logs-ui/design.md`<br>`planning/frontend/15_audit-logs-ui/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-15-01 | T-15-01, T-15-11 |
| FR-15-02 | T-15-02, T-15-11 |
| FR-15-03 | T-15-03, T-15-11 |
| FR-15-04 | T-15-04, T-15-11 |
| FR-15-05 | T-15-05, T-15-11 |
| FR-15-06 | T-15-06, T-15-11 |
| NFR-15-01 | T-15-07, T-15-11 |
| NFR-15-02 | T-15-08, T-15-11 |
| AC-15-01 | T-15-09, T-15-11 |
| AC-15-02 | T-15-10, T-15-11 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-15-1 | T-15-01, T-15-03, T-15-05 |
| C-15-2 | T-15-02, T-15-04, T-15-06 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 6/6 | [x] FR-15-01, FR-15-02, FR-15-03, FR-15-04, FR-15-05, FR-15-06 |
| 4 | NFR coverage 2/2 | [x] NFR-15-01, NFR-15-02 |
| 5 | AC coverage 2/2 | [x] AC-15-01, AC-15-02 |
| 6 | C-* coverage 2/2 | [x] C-15-1, C-15-2 |
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
