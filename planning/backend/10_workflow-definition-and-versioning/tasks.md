# Tasks — 10 Workflow Definition and Versioning

| Field | Value |
|-------|-------|
| Task list ID | `BE-10-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-10-DES`) |
| Paired requirements | `requirements.md` (`BE-10`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 3/3 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Workflow CRUD → version pin → status lifecycle → schema validate → activate→BE-22.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-10. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/workflows.py`
- `backend/app/services/workflow_service.py`
- `backend/app/domain/workflows/models.py`
- `backend/app/domain/workflows/policies.py`
- `backend/app/schemas/workflows.py`
- `backend/app/infrastructure/repositories/workflow_repository.py`
- `backend/app/infrastructure/governance/structure_validators.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-10-01 — Workflow definition CRUD + list
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-10-1 |
| **Maps to** | FR-10-01, FR-10-06, AC-10-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| **Test-first** | Create/get workflow. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Definitions managed. |
| **Acceptance** | Definitions managed. |
| **Evidence** | api/v1/routes/workflows.py |

### [x] T-10-02 — Persist metadata schemas steps policies
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4, C-10-2 |
| **Maps to** | FR-10-02, FR-10-07, FR-10-09 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/models.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py` |
| **Test-first** | DNA fields round-trip. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Executable structure stored. |
| **Acceptance** | Executable structure stored. |
| **Evidence** | domain/workflows/models.py |

### [x] T-10-03 — Versioning + pin on runs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-10-01 |
| **Maps to** | FR-10-04, FR-10-05, AC-10-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| **Test-first** | Run stores workflow_version. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | History stable. |
| **Acceptance** | History stable. |
| **Evidence** | run model |

### [x] T-10-04 — Status draft/active/disabled/archived
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 status |
| **Maps to** | FR-10-03, FR-10-08, AC-10-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py` |
| **Test-first** | Disabled cannot start runs. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Lifecycle enforced. |
| **Acceptance** | Lifecycle enforced. |
| **Evidence** | workflows policies |

### [x] T-10-05 — Schema validate on create/update
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-10-10 |
| **Maps to** | FR-10-10, AC-10-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| **Test-first** | Invalid payload 422. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Corrupt DNA rejected. |
| **Acceptance** | Corrupt DNA rejected. |
| **Evidence** | workflows routes |

### [x] T-10-06 — Activate hooks to DNA validators (BE-22)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-10-02 |
| **Maps to** | FR-10-06, BE-22 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| **Test-first** | Invalid DNA cannot activate. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safe activation. |
| **Acceptance** | Safe activation. |
| **Evidence** | runtime activate + structure_validators |

### [x] T-10-07 — AuthZ workflows:*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-10-02 |
| **Maps to** | NFR-10-02, NFR-10-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Unauthorized update 403. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Controlled authors. |
| **Acceptance** | Controlled authors. |
| **Evidence** | permissions |

### [x] T-10-08 — Flagship seed workflow
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | TV-10-03 |
| **Maps to** | AC-10-01 |
| **Deliverable (code paths)** | `business DNA / seed`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py` |
| **Test-first** | E1 starts flagship. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Seed present. |
| **Acceptance** | Seed present. |
| **Evidence** | business DNA / seed |

### [x] T-10-09 — Exit review — workflow defs complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-10-01, AC-10-02, AC-10-03, AC-10-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-10-10 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-10-01 |
| **Deliverable (code paths)** | `requirements.md`<br>`10_workflow-definition-and-versioning/tasks.md RTM`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=1 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 10_workflow-definition-and-versioning/tasks.md RTM |

### [x] T-10-11 — Implement/verify all design components C-*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-10-3, C-10-1, C-10-2, C-10-3 |
| **Maps to** | AC-10-01, AC-10-02, AC-10-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| **Test-first** | Component module import/smoke or route presence. |
| **Steps** | 1) Map each C-* to module path in design. 2) Verify module exists and is wired. 3) Add smoke test if missing. |
| **Success** | All design components have implementation anchors. |
| **Acceptance** | Components covered: C-10-1, C-10-2, C-10-3 |
| **Evidence** | ### 3.1 Components |

### [x] T-10-12 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-10-01, D-10-02 |
| **Maps to** | FR-10-01, FR-10-02, NFR-10-01, AC-10-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-10-13 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-10-01, AC-10-02, AC-10-03, AC-10-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-10-14 — Exit review — BE-10 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-10-01, FR-10-02, FR-10-03, FR-10-04, FR-10-05, FR-10-06, FR-10-07, FR-10-08, FR-10-09, FR-10-10, NFR-10-01, NFR-10-02, NFR-10-03, AC-10-01, AC-10-02, AC-10-03, AC-10-04 |
| **Deliverable (code paths)** | `planning/backend/10_workflow-definition-and-versioning/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/10_workflow-definition-and-versioning/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-10-01` | FR-10-01, FR-10-06, AC-10-01 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| `T-10-02` | FR-10-02, FR-10-07, FR-10-09 | `backend/app/domain/workflows/models.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py`<br>… +5 more |
| `T-10-03` | FR-10-04, FR-10-05, AC-10-02 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| `T-10-04` | FR-10-03, FR-10-08, AC-10-03 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py`<br>… +5 more |
| `T-10-05` | FR-10-10, AC-10-04 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| `T-10-06` | FR-10-06, BE-22 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| `T-10-07` | NFR-10-02, NFR-10-03 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py`<br>… +5 more |
| `T-10-08` | AC-10-01 | `business DNA / seed`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>… +6 more |
| `T-10-09` | AC-10-01, AC-10-02, AC-10-03, AC-10-04 | `tasks.md`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>… +1 more |
| `T-10-10` | NFR-10-01 | `requirements.md`<br>`10_workflow-definition-and-versioning/tasks.md RTM`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>… +2 more |
| `T-10-11` | AC-10-01, AC-10-02, AC-10-03 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>`backend/app/infrastructure/repositories/workflow_repository.py` |
| `T-10-12` | FR-10-01, FR-10-02, NFR-10-01, AC-10-01 | `backend/app`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>… +1 more |
| `T-10-13` | AC-10-01, AC-10-02, AC-10-03, AC-10-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py`<br>… +1 more |
| `T-10-14` | FR-10-01, FR-10-02, FR-10-03, FR-10-04, FR-10-05, FR-10-06, FR-10-07, FR-10-08, … | `planning/backend/10_workflow-definition-and-versioning/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>… +2 more |

---

## Compliance checkpoint

```text
[x] Every task has Deliverable (code paths) with repo-relative file/dir locations
[x] Primary code deliverables section lists component anchors
[x] Requirements IDs still mapped (Maps to)
[x] Master index planning/backend/TASK_TO_CODE_TRACEABILITY.md updated
[x] All tasks [x] Implemented with evidence
```

## Implementation log

| Item | Status |
|------|--------|
| Code-path deliverables on every task | [x] |
| Component primary deliverables listed | [x] |
| Traceability index generated | [x] |

## Notes

- **Deliverable (code paths)** is the authoritative implementation location for the task.
- Paths are repo-relative from workspace root (e.g. `backend/app/runtime.py`).
- If a file moves, update the deliverable path in this tasks.md and regenerate the master index.
- Version **2.2** adds mandatory code-location traceability on top of v2.1 RTM coverage.
