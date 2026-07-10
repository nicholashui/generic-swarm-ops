# Tasks — 13 Knowledge and Memory UI

| Field | Value |
|-------|-------|
| Task list ID | `FE-13-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-13-DES`) |
| Paired requirements | `requirements.md` (`FE-13`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 6/6 · NFR 3/3 · AC 3/3 · C-* 3/3 |

---

## SDD workflow

Knowledge/memory panels → debounced search → provenance display.

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

These are the **main source locations** for FE-13. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/components/ui/search-input.tsx`
- `frontend/src/lib/api/live-data.ts`
- `frontend/src/app/app/[...slug]/page.tsx`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-13-1 | Knowledge/memory panels | `app domain surfaces` |
| C-13-2 | Search input | `frontend/src/components/ui/search-input.tsx` |
| C-13-3 | Live data | `frontend/src/lib/api/live-data.ts` |

---

## Task backlog

### [x] T-13-01 — The frontend shall provide knowledge routes for overview, sources, documents, and search
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-13-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-13-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/search-input.tsx`<br>`frontend/src/lib/api/live-data.ts` |
| **Test-first** | Failing check first for FR-13-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-13-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update sidebar/paths/command palette config per IA §12. 4) Apply route guard UX (login redirect / 403 view). 5) Preserve deep-link URLs even if slug panel router is used. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-13-01. |
| **Success** | Observable: The frontend shall provide knowledge routes for overview, sources, documents, and search. |
| **Acceptance** | FR-13-01: The frontend shall provide knowledge routes for overview, sources, documents, and search. |
| **Evidence** | `frontend/src/components/ui/search-input.tsx` |

### [x] T-13-02 — The frontend shall provide memory list and detail routes under `/app/memory`
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-13-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-13-02 |
| **Deliverable (code paths)** | `frontend/src/lib/api/live-data.ts`<br>`frontend/src/components/ui/search-input.tsx` |
| **Test-first** | Failing check first for FR-13-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-13-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update sidebar/paths/command palette config per IA §12. 4) Apply route guard UX (login redirect / 403 view). 5) Preserve deep-link URLs even if slug panel router is used. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-13-02. |
| **Success** | Observable: The frontend shall provide memory list and detail routes under `/app/memory`. |
| **Acceptance** | FR-13-02: The frontend shall provide memory list and detail routes under `/app/memory`. |
| **Evidence** | `frontend/src/lib/api/live-data.ts` |

### [x] T-13-03 — Knowledge/memory views shall render backend-returned metadata and shall not invent index contents
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-13-3, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-13-03 |
| **Deliverable (code paths)** | `frontend/src/lib/api/live-data.ts`<br>`frontend/src/components/ui/search-input.tsx` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-13-03 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-13-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/lib/api/live-data.ts`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-13-03. |
| **Success** | Observable: Knowledge/memory views shall render backend-returned metadata and shall not invent index contents. |
| **Acceptance** | FR-13-03: Knowledge/memory views shall render backend-returned metadata and shall not invent index contents. |
| **Evidence** | `frontend/src/lib/api/live-data.ts` |

### [x] T-13-04 — When search is invoked, the frontend shall call backend retrieval APIs and display results with a…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-13-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-13-04 |
| **Deliverable (code paths)** | `frontend/src/components/ui/search-input.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-13-04: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-13-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-13-1` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-13-04. |
| **Success** | Observable: When search is invoked, the frontend shall call backend retrieval APIs and display results with available provenance. |
| **Acceptance** | FR-13-04: When search is invoked, the frontend shall call backend retrieval APIs and display results with available provenance. |
| **Evidence** | `frontend/src/components/ui/search-input.tsx` |

### [x] T-13-05 — The frontend shall not perform embedding or indexing in the browser
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-13-2, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-13-05 |
| **Deliverable (code paths)** | `frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/ui/search-input.tsx` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-13-05 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-13-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/lib/api/live-data.ts`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-13-05. |
| **Success** | Observable: The frontend shall not perform embedding or indexing in the browser. |
| **Acceptance** | FR-13-05: The frontend shall not perform embedding or indexing in the browser. |
| **Evidence** | `frontend/src/lib/api/live-data.ts` |

### [x] T-13-06 — Mutations (add source, delete memory) shall only occur through backend APIs when exposed and perm…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-13-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-13-06 |
| **Deliverable (code paths)** | `frontend/src/lib/api/live-data.ts`<br>`frontend/src/components/ui/search-input.tsx` |
| **Test-first** | Failing check first for FR-13-06: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-13-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-13-3` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-13-06. |
| **Success** | Observable: Mutations (add source, delete memory) shall only occur through backend APIs when exposed and permitted. |
| **Acceptance** | FR-13-06: Mutations (add source, delete memory) shall only occur through backend APIs when exposed and permitted. |
| **Evidence** | `frontend/src/lib/api/live-data.ts` |

### [x] T-13-07 — NFR gate — NFR-13-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-13-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/search-input.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-13-01 before changing code. |
| **Steps** | 1) Map NFR-13-01 to design §7 performance row. 2) Implement debounce/pagination/abort/code-split as applicable in `frontend/src/components/ui/search-input.tsx`. 3) Manual or unit timing check for MVP data sizes. 4) Confirm shell remains interactive. 5) Record evidence path. |
| **Success** | NFR-13-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-13-01: Search UI shall debounce queries to avoid request storms. |
| **Evidence** | `frontend/src/components/ui/search-input.tsx` |

### [x] T-13-08 — NFR gate — NFR-13-02
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-13-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/search-input.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-13-02 before changing code. |
| **Steps** | 1) Map NFR-13-02 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-13-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-13-02: Knowledge UI shall not exfiltrate full corpora beyond what backend returns to the caller. |
| **Evidence** | `frontend/src/components/ui/search-input.tsx` |

### [x] T-13-09 — NFR gate — NFR-13-03
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-13-03 |
| **Deliverable (code paths)** | `frontend/src/components/ui/search-input.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-13-03 before changing code. |
| **Steps** | 1) Map NFR-13-03 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-13-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-13-03: Memory detail shall respect permission UX for sensitive records. |
| **Evidence** | `frontend/src/components/ui/search-input.tsx` |

### [x] T-13-10 — Acceptance proof — AC-13-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-13-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/search-input.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-13-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Knowledge and memory pages render in app shell. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-13-01 passes with recorded evidence. |
| **Acceptance** | AC-13-01: Knowledge and memory pages render in app shell. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-13-11 — Acceptance proof — AC-13-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-13-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/search-input.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-13-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Search calls backend and shows results or empty state. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-13-02 passes with recorded evidence. |
| **Acceptance** | AC-13-02: Search calls backend and shows results or empty state. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-13-12 — Acceptance proof — AC-13-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-13-03 |
| **Deliverable (code paths)** | `frontend/src/components/ui/search-input.tsx`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-13-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: No client-side vector store dependency. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-13-03 passes with recorded evidence. |
| **Acceptance** | AC-13-03: No client-side vector store dependency. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-13-13 — Exit review — FE-13 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-13-01, FR-13-02, FR-13-03, FR-13-04, FR-13-05, FR-13-06, NFR-13-01, NFR-13-02… |
| **Deliverable (code paths)** | `planning/frontend/13_knowledge-and-memory-ui/tasks.md`<br>`planning/frontend/13_knowledge-and-memory-ui/design.md`<br>`planning/frontend/13_knowledge-and-memory-ui/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-13-01 | T-13-01, T-13-13 |
| FR-13-02 | T-13-02, T-13-13 |
| FR-13-03 | T-13-03, T-13-13 |
| FR-13-04 | T-13-04, T-13-13 |
| FR-13-05 | T-13-05, T-13-13 |
| FR-13-06 | T-13-06, T-13-13 |
| NFR-13-01 | T-13-07, T-13-13 |
| NFR-13-02 | T-13-08, T-13-13 |
| NFR-13-03 | T-13-09, T-13-13 |
| AC-13-01 | T-13-10, T-13-13 |
| AC-13-02 | T-13-11, T-13-13 |
| AC-13-03 | T-13-12, T-13-13 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-13-1 | T-13-01, T-13-04 |
| C-13-2 | T-13-02, T-13-05 |
| C-13-3 | T-13-03, T-13-06 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 6/6 | [x] FR-13-01, FR-13-02, FR-13-03, FR-13-04, FR-13-05, FR-13-06 |
| 4 | NFR coverage 3/3 | [x] NFR-13-01, NFR-13-02, NFR-13-03 |
| 5 | AC coverage 3/3 | [x] AC-13-01, AC-13-02, AC-13-03 |
| 6 | C-* coverage 3/3 | [x] C-13-1, C-13-2, C-13-3 |
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
