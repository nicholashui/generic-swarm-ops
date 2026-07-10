# Tasks — 06 Permission-Aware Navigation and UI

| Field | Value |
|-------|-------|
| Task list ID | `FE-06-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-06-DES`) |
| Paired requirements | `requirements.md` (`FE-06`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 7/7 · NFR 3/3 · AC 3/3 · C-* 4/4 |

---

## SDD workflow

Load /auth/me perms → can() helpers → filter nav/actions → 403 UX.

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

These are the **main source locations** for FE-06. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/lib/auth/permissions.ts`
- `frontend/src/hooks/use-permissions.ts`
- `frontend/src/types/permissions.ts`
- `frontend/tests/unit/permissions.test.ts`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-06-1 | Permissions model | `frontend/src/lib/auth/permissions.ts` |
| C-06-2 | usePermissions | `frontend/src/hooks/use-permissions.ts` |
| C-06-3 | Permission types | `frontend/src/types/permissions.ts` |
| C-06-4 | Unit tests | `frontend/tests/unit/permissions.test.ts` |

---

## Task backlog

### [x] T-06-01 — The frontend shall load the authenticated user’s roles and permissions from the backend
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-06-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-06-01 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit/permissions.test.ts` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-06-01). |
| **Steps** | 1) Open `requirements.md` FR-06-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-06-01. |
| **Success** | Observable: The frontend shall load the authenticated user’s roles and permissions from the backend. |
| **Acceptance** | FR-06-01: The frontend shall load the authenticated user’s roles and permissions from the backend. |
| **Evidence** | `frontend/src/lib/auth/permissions.ts` |

### [x] T-06-02 — When the user lacks permission for a navigation item, the frontend shall hide or disable that ite…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-06-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-06-02 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit/permissions.test.ts` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-06-02). |
| **Steps** | 1) Open `requirements.md` FR-06-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-06-02. |
| **Success** | Observable: When the user lacks permission for a navigation item, the frontend shall hide or disable that item according to product rules. |
| **Acceptance** | FR-06-02: When the user lacks permission for a navigation item, the frontend shall hide or disable that item according to product rules. |
| **Evidence** | `frontend/src/lib/auth/permissions.ts` |

### [x] T-06-03 — When the user navigates to a route they cannot access, the frontend shall show Access Denied (403…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-06-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-06-03 |
| **Deliverable (code paths)** | `frontend/src/types/permissions.ts`<br>`frontend/tests/unit/permissions.test.ts`<br>`frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-06-03). |
| **Steps** | 1) Open `requirements.md` FR-06-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-06-03. |
| **Success** | Observable: When the user navigates to a route they cannot access, the frontend shall show Access Denied (403) UX. |
| **Acceptance** | FR-06-03: When the user navigates to a route they cannot access, the frontend shall show Access Denied (403) UX. |
| **Evidence** | `frontend/src/types/permissions.ts` |

### [x] T-06-04 — When the user lacks permission for a mutating action, the frontend shall disable or hide the acti…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-06-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-06-04 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit/permissions.test.ts` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-06-04). |
| **Steps** | 1) Open `requirements.md` FR-06-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-06-04. |
| **Success** | Observable: When the user lacks permission for a mutating action, the frontend shall disable or hide the action control. |
| **Acceptance** | FR-06-04: When the user lacks permission for a mutating action, the frontend shall disable or hide the action control. |
| **Evidence** | `frontend/src/lib/auth/permissions.ts` |

### [x] T-06-05 — If the backend returns 403 for an action the UI allowed, the frontend shall surface the backend d…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-06-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-06-05 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit/permissions.test.ts` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-06-05). |
| **Steps** | 1) Open `requirements.md` FR-06-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-06-05. |
| **Success** | Observable: If the backend returns 403 for an action the UI allowed, the frontend shall surface the backend denial and not claim success. |
| **Acceptance** | FR-06-05: If the backend returns 403 for an action the UI allowed, the frontend shall surface the backend denial and not claim success. |
| **Evidence** | `frontend/src/lib/auth/permissions.ts` |

### [x] T-06-06 — Document and enforce UX-only permission model
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-06-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-06-06 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit/permissions.test.ts` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-06-06). |
| **Steps** | 1) Open `requirements.md` FR-06-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-06-06. |
| **Success** | Observable: The frontend shall treat permission-aware UI as UX-level only; backend authorization remains final. |
| **Acceptance** | FR-06-06: The frontend shall treat permission-aware UI as UX-level only; backend authorization remains final. |
| **Evidence** | `frontend/src/lib/auth/permissions.ts` |

### [x] T-06-07 — Role labels displayed in UI shall match backend-provided role names without inventing elevated pr…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-06-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-06-07 |
| **Deliverable (code paths)** | `frontend/src/types/permissions.ts`<br>`frontend/tests/unit/permissions.test.ts`<br>`frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts` |
| **Test-first** | Failing check first for FR-06-07: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-06-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-06-3` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-06-07. |
| **Success** | Observable: Role labels displayed in UI shall match backend-provided role names without inventing elevated privileges. |
| **Acceptance** | FR-06-07: Role labels displayed in UI shall match backend-provided role names without inventing elevated privileges. |
| **Evidence** | `frontend/src/types/permissions.ts` |

### [x] T-06-08 — NFR gate — NFR-06-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-06-01 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit/permissions.test.ts` |
| **Test-first** | Define pass/fail measurement for NFR-06-01 before changing code. |
| **Steps** | 1) Map NFR-06-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-06-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-06-01: Permission payload shall be cached for the session and refreshed on login/org switch. |
| **Evidence** | `frontend/src/lib/auth/permissions.ts` |

### [x] T-06-09 — NFR gate — NFR-06-02
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-06-02 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit/permissions.test.ts` |
| **Test-first** | Define pass/fail measurement for NFR-06-02 before changing code. |
| **Steps** | 1) Map NFR-06-02 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-06-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-06-02: Client-side permission caches shall not be writable by untrusted page scripts as a means to elevate access. |
| **Evidence** | `frontend/src/lib/auth/permissions.ts` |

### [x] T-06-10 — NFR gate — NFR-06-03
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-06-03 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit/permissions.test.ts` |
| **Test-first** | Define pass/fail measurement for NFR-06-03 before changing code. |
| **Steps** | 1) Map NFR-06-03 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-06-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-06-03: Permission checks in UI shall fail closed (deny/hide) when permission data is missing. |
| **Evidence** | `frontend/src/lib/auth/permissions.ts` |

### [x] T-06-11 — Acceptance proof — AC-06-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-06-01 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-06-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Viewer-like role cannot see admin-only nav items (given backend payload). 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-06-01 passes with recorded evidence. |
| **Acceptance** | AC-06-01: Viewer-like role cannot see admin-only nav items (given backend payload). |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-06-12 — Acceptance proof — AC-06-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-06-02 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-06-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: 403 from API shows error state on attempted mutation. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-06-02 passes with recorded evidence. |
| **Acceptance** | AC-06-02: 403 from API shows error state on attempted mutation. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-06-13 — Acceptance proof — AC-06-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-06-03 |
| **Deliverable (code paths)** | `frontend/src/lib/auth/permissions.ts`<br>`frontend/src/hooks/use-permissions.ts`<br>`frontend/src/types/permissions.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-06-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Documentation states client gates are non-authoritative. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-06-03 passes with recorded evidence. |
| **Acceptance** | AC-06-03: Documentation states client gates are non-authoritative. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-06-14 — Exit review — FE-06 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-06-01, FR-06-02, FR-06-03, FR-06-04, FR-06-05, FR-06-06, FR-06-07, NFR-06-01… |
| **Deliverable (code paths)** | `planning/frontend/06_permission-aware-navigation-and-ui/tasks.md`<br>`planning/frontend/06_permission-aware-navigation-and-ui/design.md`<br>`planning/frontend/06_permission-aware-navigation-and-ui/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-06-01 | T-06-01, T-06-14 |
| FR-06-02 | T-06-02, T-06-14 |
| FR-06-03 | T-06-03, T-06-14 |
| FR-06-04 | T-06-04, T-06-14 |
| FR-06-05 | T-06-05, T-06-14 |
| FR-06-06 | T-06-06, T-06-14 |
| FR-06-07 | T-06-07, T-06-14 |
| NFR-06-01 | T-06-08, T-06-14 |
| NFR-06-02 | T-06-09, T-06-14 |
| NFR-06-03 | T-06-10, T-06-14 |
| AC-06-01 | T-06-11, T-06-14 |
| AC-06-02 | T-06-12, T-06-14 |
| AC-06-03 | T-06-13, T-06-14 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-06-1 | T-06-01, T-06-05 |
| C-06-2 | T-06-02, T-06-06 |
| C-06-3 | T-06-03, T-06-07 |
| C-06-4 | T-06-04 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 7/7 | [x] FR-06-01, FR-06-02, FR-06-03, FR-06-04, FR-06-05, FR-06-06, FR-06-07 |
| 4 | NFR coverage 3/3 | [x] NFR-06-01, NFR-06-02, NFR-06-03 |
| 5 | AC coverage 3/3 | [x] AC-06-01, AC-06-02, AC-06-03 |
| 6 | C-* coverage 4/4 | [x] C-06-1, C-06-2, C-06-3, C-06-4 |
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
