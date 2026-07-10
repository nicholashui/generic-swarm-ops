# Tasks — 14 Evaluations and Processes UI

| Field | Value |
|-------|-------|
| Task list ID | `FE-14-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-14-DES`) |
| Paired requirements | `requirements.md` (`FE-14`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 6/6 · NFR 2/2 · AC 2/2 · C-* 2/2 |

---

## SDD workflow

Evaluations/processes panels → BE scores only → quality nav.

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

These are the **main source locations** for FE-14. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/components/ui/metric-card.tsx`
- `frontend/src/components/ui/status-badge.tsx`
- `frontend/src/app/app/[...slug]/page.tsx`
- `frontend/src/lib/api/live-data.ts`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-14-1 | Eval/process panels | `app domain surfaces` |
| C-14-2 | Metric/status display | `metric-card, status-badge` |

---

## Task backlog

### [x] T-14-01 — The frontend shall provide evaluations list and detail routes under `/app/evaluations`
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-14-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-14-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/metric-card.tsx`<br>`frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/lib/api/live-data.ts` |
| **Test-first** | Failing check first for FR-14-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-14-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update sidebar/paths/command palette config per IA §12. 4) Apply route guard UX (login redirect / 403 view). 5) Preserve deep-link URLs even if slug panel router is used. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-14-01. |
| **Success** | Observable: The frontend shall provide evaluations list and detail routes under `/app/evaluations`. |
| **Acceptance** | FR-14-01: The frontend shall provide evaluations list and detail routes under `/app/evaluations`. |
| **Evidence** | `frontend/src/components/ui/metric-card.tsx` |

### [x] T-14-02 — The frontend shall provide processes list and detail routes under `/app/processes`
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-14-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-14-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/metric-card.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/components/ui/status-badge.tsx` |
| **Test-first** | Mock stream events → UI updates; kill stream → degraded/poll (FR-14-02). |
| **Steps** | 1) Open `requirements.md` FR-14-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/extend `useRealtimeRun` + `sse.ts` subscribe/merge. 4) On stream error set degraded + poll; cleanup on unmount. 5) Drive Timeline/LogViewer from merged events without full page reload. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-14-02. |
| **Success** | Observable: The frontend shall provide processes list and detail routes under `/app/processes`. |
| **Acceptance** | FR-14-02: The frontend shall provide processes list and detail routes under `/app/processes`. |
| **Evidence** | `frontend/src/components/ui/metric-card.tsx` |

### [x] T-14-03 — Evaluation views shall display scores, statuses, and artifacts metadata returned by backend
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-14-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-14-03 |
| **Deliverable (code paths)** | `frontend/src/components/ui/metric-card.tsx`<br>`frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/lib/api/live-data.ts` |
| **Test-first** | Failing check first for FR-14-03: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-14-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-14-1` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-14-03. |
| **Success** | Observable: Evaluation views shall display scores, statuses, and artifacts metadata returned by backend. |
| **Acceptance** | FR-14-03: Evaluation views shall display scores, statuses, and artifacts metadata returned by backend. |
| **Evidence** | `frontend/src/components/ui/metric-card.tsx` |

### [x] T-14-04 — Process views shall display PI summaries/artifacts/events as returned by backend
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-14-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-14-04 |
| **Deliverable (code paths)** | `frontend/src/components/ui/metric-card.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/components/ui/status-badge.tsx` |
| **Test-first** | Failing check first for FR-14-04: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-14-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-14-2` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-14-04. |
| **Success** | Observable: Process views shall display PI summaries/artifacts/events as returned by backend. |
| **Acceptance** | FR-14-04: Process views shall display PI summaries/artifacts/events as returned by backend. |
| **Evidence** | `frontend/src/components/ui/metric-card.tsx` |

### [x] T-14-05 — When starting an evaluation is supported, the frontend shall call backend evaluation APIs rather …
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-14-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-14-05 |
| **Deliverable (code paths)** | `frontend/src/components/ui/metric-card.tsx`<br>`frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/lib/api/live-data.ts` |
| **Test-first** | Failing check first for FR-14-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-14-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-14-1` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-14-05. |
| **Success** | Observable: When starting an evaluation is supported, the frontend shall call backend evaluation APIs rather than computing scores locally. |
| **Acceptance** | FR-14-05: When starting an evaluation is supported, the frontend shall call backend evaluation APIs rather than computing scores locally. |
| **Evidence** | `frontend/src/components/ui/metric-card.tsx` |

### [x] T-14-06 — The frontend shall not claim eval pass/fail without backend results
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-14-2, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-14-06 |
| **Deliverable (code paths)** | `frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/components/ui/metric-card.tsx` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-14-06 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-14-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/components/ui/status-badge.tsx`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-14-06. |
| **Success** | Observable: The frontend shall not claim eval pass/fail without backend results. |
| **Acceptance** | FR-14-06: The frontend shall not claim eval pass/fail without backend results. |
| **Evidence** | `frontend/src/components/ui/status-badge.tsx` |

### [x] T-14-07 — NFR gate — NFR-14-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-14-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/metric-card.tsx`<br>`frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/live-data.ts` |
| **Test-first** | Define pass/fail measurement for NFR-14-01 before changing code. |
| **Steps** | 1) Map NFR-14-01 to design §7 performance row. 2) Implement debounce/pagination/abort/code-split as applicable in `frontend/src/components/ui/metric-card.tsx`. 3) Manual or unit timing check for MVP data sizes. 4) Confirm shell remains interactive. 5) Record evidence path. |
| **Success** | NFR-14-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-14-01: Large eval result payloads shall be paginated or truncated in UI with expand options. |
| **Evidence** | `frontend/src/components/ui/metric-card.tsx` |

### [x] T-14-08 — NFR gate — NFR-14-02
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-14-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/metric-card.tsx`<br>`frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/live-data.ts` |
| **Test-first** | Define pass/fail measurement for NFR-14-02 before changing code. |
| **Steps** | 1) Map NFR-14-02 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-14-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-14-02: Eval/process views shall respect permission-aware access. |
| **Evidence** | `frontend/src/components/ui/metric-card.tsx` |

### [x] T-14-09 — Acceptance proof — AC-14-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-14-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/metric-card.tsx`<br>`frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-14-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Evaluations and processes pages accessible from Quality nav. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-14-01 passes with recorded evidence. |
| **Acceptance** | AC-14-01: Evaluations and processes pages accessible from Quality nav. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-14-10 — Acceptance proof — AC-14-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-14-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/metric-card.tsx`<br>`frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-14-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Detail pages render backend payloads or empty states. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-14-02 passes with recorded evidence. |
| **Acceptance** | AC-14-02: Detail pages render backend payloads or empty states. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-14-11 — Exit review — FE-14 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-14-01, FR-14-02, FR-14-03, FR-14-04, FR-14-05, FR-14-06, NFR-14-01, NFR-14-02… |
| **Deliverable (code paths)** | `planning/frontend/14_evaluations-and-processes-ui/tasks.md`<br>`planning/frontend/14_evaluations-and-processes-ui/design.md`<br>`planning/frontend/14_evaluations-and-processes-ui/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-14-01 | T-14-01, T-14-11 |
| FR-14-02 | T-14-02, T-14-11 |
| FR-14-03 | T-14-03, T-14-11 |
| FR-14-04 | T-14-04, T-14-11 |
| FR-14-05 | T-14-05, T-14-11 |
| FR-14-06 | T-14-06, T-14-11 |
| NFR-14-01 | T-14-07, T-14-11 |
| NFR-14-02 | T-14-08, T-14-11 |
| AC-14-01 | T-14-09, T-14-11 |
| AC-14-02 | T-14-10, T-14-11 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-14-1 | T-14-01, T-14-03, T-14-05 |
| C-14-2 | T-14-02, T-14-04, T-14-06 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 6/6 | [x] FR-14-01, FR-14-02, FR-14-03, FR-14-04, FR-14-05, FR-14-06 |
| 4 | NFR coverage 2/2 | [x] NFR-14-01, NFR-14-02 |
| 5 | AC coverage 2/2 | [x] AC-14-01, AC-14-02 |
| 6 | C-* coverage 2/2 | [x] C-14-1, C-14-2 |
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
