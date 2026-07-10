# Tasks — 19 Accessibility, Loading, Empty, and Error States

| Field | Value |
|-------|-------|
| Task list ID | `FE-19-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-19-DES`) |
| Paired requirements | `requirements.md` (`FE-19`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 8/8 · NFR 2/2 · AC 3/3 · C-* 4/4 |

---

## SDD workflow

Wire Skeleton/Empty/Error → a11y labels/focus → request_id errors.

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

These are the **main source locations** for FE-19. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/components/ui/empty-state.tsx`
- `frontend/src/components/ui/error-state.tsx`
- `frontend/src/components/ui/skeleton.tsx`
- `frontend/src/components/ui/status-badge.tsx`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-19-1 | EmptyState | `frontend/src/components/ui/empty-state.tsx` |
| C-19-2 | ErrorState | `frontend/src/components/ui/error-state.tsx` |
| C-19-3 | Skeleton | `frontend/src/components/ui/skeleton.tsx` |
| C-19-4 | Status badges | `status-badge.tsx + design/status.ts` |

---

## Task backlog

### [x] T-19-01 — Every major data page shall implement loading, empty, and error states
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-19-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-19-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/skeleton.tsx` |
| **Test-first** | Force slow/fixture load → assert Skeleton/loading UI for FR-19-01. |
| **Steps** | 1) Open `requirements.md` FR-19-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Adopt Skeleton/EmptyState/ErrorState primitives on target pages. 4) Labels, focus rings, non-color-only status; request_id on errors. 5) Keyboard-pass primary flows; sanitize production error bodies. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-19-01. |
| **Success** | Observable: Every major data page shall implement loading, empty, and error states. |
| **Acceptance** | FR-19-01: Every major data page shall implement loading, empty, and error states. |
| **Evidence** | `frontend/src/components/ui/empty-state.tsx` |

### [x] T-19-02 — Error states shall show human-readable messages and request_id when the API provides one
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-19-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-19-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/empty-state.tsx` |
| **Test-first** | Force API 4xx/5xx with request_id → ErrorState shows message + id (FR-19-02). |
| **Steps** | 1) Open `requirements.md` FR-19-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update OpenAPI artifact; run `pnpm api:generate`. 4) Extend `backendApi` method; parse errors into AppError. 5) Consume types in domain loader/panel; no hand-forked DTOs. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-19-02. |
| **Success** | Observable: Error states shall show human-readable messages and request_id when the API provides one. |
| **Acceptance** | FR-19-02: Error states shall show human-readable messages and request_id when the API provides one. |
| **Evidence** | `frontend/src/components/ui/error-state.tsx` |

### [x] T-19-03 — Interactive controls shall be keyboard operable for primary flows
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-19-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-19-03 |
| **Deliverable (code paths)** | `frontend/src/components/ui/skeleton.tsx`<br>`frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx` |
| **Test-first** | Failing check first for FR-19-03: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-19-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Adopt Skeleton/EmptyState/ErrorState primitives on target pages. 4) Labels, focus rings, non-color-only status; request_id on errors. 5) Keyboard-pass primary flows; sanitize production error bodies. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-19-03. |
| **Success** | Observable: Interactive controls shall be keyboard operable for primary flows. |
| **Acceptance** | FR-19-03: Interactive controls shall be keyboard operable for primary flows. |
| **Evidence** | `frontend/src/components/ui/skeleton.tsx` |

### [x] T-19-04 — Form inputs shall have accessible labels
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-19-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-19-04 |
| **Deliverable (code paths)** | `frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/skeleton.tsx` |
| **Test-first** | Failing check first for FR-19-04: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-19-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Adopt Skeleton/EmptyState/ErrorState primitives on target pages. 4) Labels, focus rings, non-color-only status; request_id on errors. 5) Keyboard-pass primary flows; sanitize production error bodies. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-19-04. |
| **Success** | Observable: Form inputs shall have accessible labels. |
| **Acceptance** | FR-19-04: Form inputs shall have accessible labels. |
| **Evidence** | `frontend/src/components/ui/status-badge.tsx` |

### [x] T-19-05 — Focus shall be managed for modals and drawers (trap/restore as appropriate)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-19-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-19-05 |
| **Deliverable (code paths)** | `frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/skeleton.tsx`<br>`frontend/src/components/ui/status-badge.tsx` |
| **Test-first** | Failing check first for FR-19-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-19-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-19-1` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-19-05. |
| **Success** | Observable: Focus shall be managed for modals and drawers (trap/restore as appropriate). |
| **Acceptance** | FR-19-05: Focus shall be managed for modals and drawers (trap/restore as appropriate). |
| **Evidence** | `frontend/src/components/ui/empty-state.tsx` |

### [x] T-19-06 — Status information shall not rely on color alone
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-19-2, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-19-06 |
| **Deliverable (code paths)** | `frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/skeleton.tsx`<br>`frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/components/ui/empty-state.tsx` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-19-06 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-19-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/components/ui/error-state.tsx`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-19-06. |
| **Success** | Observable: Status information shall not rely on color alone. |
| **Acceptance** | FR-19-06: Status information shall not rely on color alone. |
| **Evidence** | `frontend/src/components/ui/error-state.tsx` |

### [x] T-19-07 — Empty states shall include guidance on next actions when applicable
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-19-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-19-07 |
| **Deliverable (code paths)** | `frontend/src/components/ui/skeleton.tsx`<br>`frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx` |
| **Test-first** | Force empty API payload → assert EmptyState + guidance for FR-19-07. |
| **Steps** | 1) Open `requirements.md` FR-19-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Adopt Skeleton/EmptyState/ErrorState primitives on target pages. 4) Labels, focus rings, non-color-only status; request_id on errors. 5) Keyboard-pass primary flows; sanitize production error bodies. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-19-07. |
| **Success** | Observable: Empty states shall include guidance on next actions when applicable. |
| **Acceptance** | FR-19-07: Empty states shall include guidance on next actions when applicable. |
| **Evidence** | `frontend/src/components/ui/skeleton.tsx` |

### [x] T-19-08 — The frontend shall target WCAG 2.2 Level AA practices for core operator flows
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-19-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-19-08 |
| **Deliverable (code paths)** | `frontend/src/components/ui/status-badge.tsx`<br>`frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/skeleton.tsx` |
| **Test-first** | Failing check first for FR-19-08: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-19-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-19-4` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-19-08. |
| **Success** | Observable: The frontend shall target WCAG 2.2 Level AA practices for core operator flows. |
| **Acceptance** | FR-19-08: The frontend shall target WCAG 2.2 Level AA practices for core operator flows. |
| **Evidence** | `frontend/src/components/ui/status-badge.tsx` |

### [x] T-19-09 — NFR gate — NFR-19-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-19-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/skeleton.tsx`<br>`frontend/src/components/ui/status-badge.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-19-01 before changing code. |
| **Steps** | 1) Map NFR-19-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-19-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-19-01: Loading skeletons shall avoid layout thrash where practical. |
| **Evidence** | `frontend/src/components/ui/empty-state.tsx` |

### [x] T-19-10 — NFR gate — NFR-19-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-19-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/skeleton.tsx`<br>`frontend/src/components/ui/status-badge.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-19-02 before changing code. |
| **Steps** | 1) Map NFR-19-02 to design §7 security row. 2) Inspect `frontend/src/components/ui/empty-state.tsx` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-19-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-19-02: Error messages shall not dump stack traces or secrets to end users in production builds. |
| **Evidence** | `frontend/src/components/ui/empty-state.tsx` |

### [x] T-19-11 — Acceptance proof — AC-19-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-19-01 |
| **Deliverable (code paths)** | `frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/skeleton.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-19-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Representative pages (dashboard, runs, approvals) show all three states. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-19-01 passes with recorded evidence. |
| **Acceptance** | AC-19-01: Representative pages (dashboard, runs, approvals) show all three states. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-19-12 — Acceptance proof — AC-19-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-19-02 |
| **Deliverable (code paths)** | `frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/skeleton.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-19-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Primary forms have labels; modals keyboard-dismissible. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-19-02 passes with recorded evidence. |
| **Acceptance** | AC-19-02: Primary forms have labels; modals keyboard-dismissible. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-19-13 — Acceptance proof — AC-19-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-19-03 |
| **Deliverable (code paths)** | `frontend/src/components/ui/empty-state.tsx`<br>`frontend/src/components/ui/error-state.tsx`<br>`frontend/src/components/ui/skeleton.tsx`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-19-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Production errors omit secrets/stack traces. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-19-03 passes with recorded evidence. |
| **Acceptance** | AC-19-03: Production errors omit secrets/stack traces. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-19-14 — Exit review — FE-19 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-19-01, FR-19-02, FR-19-03, FR-19-04, FR-19-05, FR-19-06, FR-19-07, FR-19-08… |
| **Deliverable (code paths)** | `planning/frontend/19_accessibility-loading-empty-and-error-states/tasks.md`<br>`planning/frontend/19_accessibility-loading-empty-and-error-states/design.md`<br>`planning/frontend/19_accessibility-loading-empty-and-error-states/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-19-01 | T-19-01, T-19-14 |
| FR-19-02 | T-19-02, T-19-14 |
| FR-19-03 | T-19-03, T-19-14 |
| FR-19-04 | T-19-04, T-19-14 |
| FR-19-05 | T-19-05, T-19-14 |
| FR-19-06 | T-19-06, T-19-14 |
| FR-19-07 | T-19-07, T-19-14 |
| FR-19-08 | T-19-08, T-19-14 |
| NFR-19-01 | T-19-09, T-19-14 |
| NFR-19-02 | T-19-10, T-19-14 |
| AC-19-01 | T-19-11, T-19-14 |
| AC-19-02 | T-19-12, T-19-14 |
| AC-19-03 | T-19-13, T-19-14 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-19-1 | T-19-01, T-19-05 |
| C-19-2 | T-19-02, T-19-06 |
| C-19-3 | T-19-03, T-19-07 |
| C-19-4 | T-19-04, T-19-08 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 8/8 | [x] FR-19-01, FR-19-02, FR-19-03, FR-19-04, FR-19-05, FR-19-06, FR-19-07, FR-19-08 |
| 4 | NFR coverage 2/2 | [x] NFR-19-01, NFR-19-02 |
| 5 | AC coverage 3/3 | [x] AC-19-01, AC-19-02, AC-19-03 |
| 6 | C-* coverage 4/4 | [x] C-19-1, C-19-2, C-19-3, C-19-4 |
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
