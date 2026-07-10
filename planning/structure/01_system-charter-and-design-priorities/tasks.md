# Tasks — 01 System Charter and Design Priorities

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-01-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-01-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-01`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/01_system-charter-and-design-priorities/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-01**. Each task further narrows via **Deliverable (code paths)**.

- `structure.md`
- `planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`
- `planning/structure/01_system-charter-and-design-priorities/requirements.md`
- `planning/structure/01_system-charter-and-design-priorities/design.md`
- `backend/app/runtime.py`
- `backend.md`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-01-01 — Mission catalog M1–M4 documented and referenced
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-01-1, §4.2 Mission |
| **Maps to** | FR-01-01…04, AC-01-01 |
| **Deliverable (code paths)** | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| **Test-first** | Spec review checklist includes four capabilities. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Reviewer finds M1–M4 in &lt;1 minute. |
| **Acceptance** | Reviewer finds M1–M4 in &lt;1 minute. |
| **Evidence** | `structure.md`, `design.md` §4.2 |

### [x] T-01-02 — Priority lattice algorithm + PR checklist
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-01-2, C-01-4, §4.1, D-01-02 |
| **Maps to** | FR-01-05…08, NFR-01-02, AC-01-01 |
| **Deliverable (code paths)** | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| **Test-first** | Checklist file must exist before merge of autonomy-increasing PRs. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | `PR_PRIORITY_LATTICE_CHECKLIST.md` present; all items usable. |
| **Acceptance** | `PR_PRIORITY_LATTICE_CHECKLIST.md` present; all items usable. |
| **Evidence** | `planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md` |

### [x] T-01-03 — Principle catalog mapped to hooks
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-01-3, C-01-6, §4.3 |
| **Maps to** | FR-01-09…16, AC-01-02, TV-01-01 |
| **Deliverable (code paths)** | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| **Test-first** | Fail review if any principle has zero hook. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Full matrix in design; no orphan principles. |
| **Acceptance** | Full matrix in design; no orphan principles. |
| **Evidence** | `design.md` §4.3 |

### [x] T-01-04 — INV-01-1/2: no direct production DNA mutation
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-01-5, INV-01-1, INV-01-2 |
| **Maps to** | FR-01-04, FR-01-13, NFR-01-04, AC-01-03 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| **Test-first** | Unit tests expect reject before feature land. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Automated tests green. |
| **Acceptance** | Automated tests green. |
| **Evidence** | evolution unit tests, `business:evolution:check` |

### [x] T-01-05 — INV-01-3: eval pass ≠ unattended production promote
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | INV-01-3, C-01-5 |
| **Maps to** | FR-01-12, TV-01-02 |
| **Deliverable (code paths)** | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py` |
| **Test-first** | Negative assertion in eval/evolution tests. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Invariant tests green. |
| **Acceptance** | Invariant tests green. |
| **Evidence** | eval harness + evolution promote guards |

### [x] T-01-06 — INV-01-4: priorities not overridable by prompts
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | INV-01-4, NFR-01-01, NFR-01-03 |
| **Maps to** | NFR-01-01, NFR-01-03 |
| **Deliverable (code paths)** | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | No prompt-only security path in design or code. |
| **Acceptance** | No prompt-only security path in design or code. |
| **Evidence** | STRUCT-05 design + runtime RBAC |

### [x] T-01-07 — Downstream design compliance sweep
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-01-6 |
| **Maps to** | AC-01-02, AC-01-04 |
| **Deliverable (code paths)** | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | All design.md v2.0 claim 100. |
| **Acceptance** | All design.md v2.0 claim 100. |
| **Evidence** | `DESIGN_QUALITY_SCORE.md` |

### [x] T-01-08 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | AC-01-01…04 |
| **Deliverable (code paths)** | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | All T-01-* [x]; quality score 100. |
| **Acceptance** | All T-01-* [x]; quality score 100. |
| **Evidence** | structure.md, planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md, planning/structure/01_system-charter-and-design-priorities/requirements.md |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-01-01` | FR-01-01…04, AC-01-01 | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| `T-01-02` | FR-01-05…08, NFR-01-02, AC-01-01 | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| `T-01-03` | FR-01-09…16, AC-01-02, TV-01-01 | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| `T-01-04` | FR-01-04, FR-01-13, NFR-01-04, AC-01-03 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>… +4 more |
| `T-01-05` | FR-01-12, TV-01-02 | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`structure.md`<br>… +4 more |
| `T-01-06` | NFR-01-01, NFR-01-03 | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| `T-01-07` | AC-01-02, AC-01-04 | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |
| `T-01-08` | AC-01-01…04 | `structure.md`<br>`planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md`<br>`planning/structure/01_system-charter-and-design-priorities/requirements.md`<br>`planning/structure/01_system-charter-and-design-priorities/design.md`<br>`backend/app/runtime.py`<br>`backend.md` |

---

## Compliance checkpoint

```text
[x] Every task has Deliverable (code paths) with repo-relative locations
[x] Primary code deliverables section present
[x] Maps to FR/NFR/AC retained
[x] Master index planning/structure/TASK_TO_CODE_TRACEABILITY.md
[x] All tasks [x] Implemented
[x] Quality score 100
```

## Implementation log

| Item | Status |
|------|--------|
| Code-path deliverables on every task | [x] |
| Component primary deliverables | [x] |
| Traceability index | [x] |

## Notes

- **Deliverable (code paths)** is the implementation location for the task (what to open/edit).
- Paths are repo-relative from workspace root.
- Architecture intent lives in `structure.md`; executable code mostly under `backend/app/` and corpus under `business/`.
- Version **2.2** makes structure-pack tasks as traceable as backend-pack v2.2.
