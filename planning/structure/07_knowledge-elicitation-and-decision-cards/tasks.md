# Tasks — 07 Knowledge Elicitation and Decision Cards

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-07-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-07-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-07`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/07_knowledge-elicitation-and-decision-cards/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-07**. Each task further narrows via **Deliverable (code paths)**.

- `business/experts/`
- `business/experts/decision-requirement-cards/`
- `business/fixtures/negative/`
- `backend/app/infrastructure/governance/structure_validators.py`
- `backend/app/tests/unit/test_structure_sdd_validators.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-07-01 — Six method templates + README map
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2.1, C-07-1 |
| **Maps to** | FR-07-01…07 |
| **Deliverable (code paths)** | `business/experts/elicitation-methods/`<br>`business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | 01–06 templates + method→path table. |
| **Acceptance** | 01–06 templates + method→path table. |
| **Evidence** | business/experts/elicitation-methods/ |

### [x] T-07-02 — Experts folder layout
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2.1 paths |
| **Maps to** | FR-07-01…07, AC-07-02 |
| **Deliverable (code paths)** | `business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/`<br>`business/memory/`<br>`business/evals/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | profiles, shadow-logs, DRCs, transcripts. |
| **Acceptance** | profiles, shadow-logs, DRCs, transcripts. |
| **Evidence** | business/, business/process-intelligence/, business/knowledge-base/ |

### [x] T-07-03 — DRC schema field-level publish rules
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 model, C-07-2 |
| **Maps to** | FR-07-08…12, AC-07-01 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | schema requires expert_sources, provenance, validation_tests, last_reviewed. |
| **Acceptance** | schema requires expert_sources, provenance, validation_tests, last_reviewed. |
| **Evidence** | decision-requirement-card.schema.json |

### [x] T-07-04 — Publish-quality sample DRC
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-07-3 |
| **Maps to** | AC-07-03 |
| **Deliverable (code paths)** | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | drc_contract_exception_001.json validates. |
| **Acceptance** | drc_contract_exception_001.json validates. |
| **Evidence** | experts/decision-requirement-cards/ |

### [x] T-07-05 — Negative DRC missing expert_sources
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.2 publish rules, C-07-4 |
| **Maps to** | FR-07-13, AC-07-04, TV-07-03 |
| **Deliverable (code paths)** | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Fixture must fail validator. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | test_structure_sdd_validators. |
| **Acceptance** | test_structure_sdd_validators. |
| **Evidence** | fixtures/negative/drc-missing-expert-sources.json |

### [x] T-07-06 — DRC state machine documented
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.1 draft→published→retired |
| **Maps to** | FR-07-12 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | States and transitions in design. |
| **Acceptance** | States and transitions in design. |
| **Evidence** | backend/app/domain/workflows/engine.py, backend/app/domain/workflows/states.py, backend/app/runtime.py |

### [x] T-07-07 — DNA binding to DRC
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5, C-07-7 |
| **Maps to** | FR-07-11 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | workflow-dna.example lists DRC path + predicate. |
| **Acceptance** | workflow-dna.example lists DRC path + predicate. |
| **Evidence** | workflow-dna.example.json guardrails |

### [x] T-07-08 — Distiller / curator process paths
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-07-5, C-07-6, §3 |
| **Maps to** | FR-07-14…15 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | distilled/_sandbox + knowledge-base paths documented/seeded. |
| **Acceptance** | distilled/_sandbox + knowledge-base paths documented/seeded. |
| **Evidence** | backend/app/api/v1/routes/processes.py, backend/app/services/process_service.py, backend/app/domain/processes/analytics.py |

### [x] T-07-09 — Validator unit tests
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-07-4 |
| **Maps to** | AC-07-01…04 |
| **Deliverable (code paths)** | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | test_structure_sdd_validators green. |
| **Acceptance** | test_structure_sdd_validators green. |
| **Evidence** | business/experts/, business/experts/decision-requirement-cards/, business/fixtures/negative/ |

### [x] T-07-10 — Interview SaaS deferred
| | |
|--|--|
| **Priority** | P3 |
| **Status** | [x] Implemented |
| **Design** | OI-07-01, D-07-01 |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Explicit non-goal; schema-first is target. |
| **Acceptance** | Explicit non-goal; schema-first is target. |
| **Evidence** | business/experts/, business/experts/decision-requirement-cards/, business/fixtures/negative/ |

### [x] T-07-11 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | business/experts/, business/experts/decision-requirement-cards/, business/fixtures/negative/ |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-07-01` | FR-07-01…07 | `business/experts/elicitation-methods/`<br>`business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| `T-07-02` | FR-07-01…07, AC-07-02 | `business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/`<br>`business/memory/`<br>`business/evals/`<br>… +4 more |
| `T-07-03` | FR-07-08…12, AC-07-01 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/experts/`<br>`business/experts/decision-requirement-cards/`<br>… +2 more |
| `T-07-04` | AC-07-03 | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| `T-07-05` | FR-07-13, AC-07-04, TV-07-03 | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| `T-07-06` | FR-07-12 | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>… +4 more |
| `T-07-07` | FR-07-11 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/experts/`<br>`business/experts/decision-requirement-cards/`<br>… +2 more |
| `T-07-08` | FR-07-14…15 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`business/experts/`<br>`business/experts/decision-requirement-cards/`<br>… +3 more |
| `T-07-09` | AC-07-01…04 | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| `T-07-10` |  | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| `T-07-11` |  | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |

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
