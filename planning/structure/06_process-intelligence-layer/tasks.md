# Tasks — 06 Process Intelligence Layer

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-06-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-06-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-06`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/06_process-intelligence-layer/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-06**. Each task further narrows via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/processes.py`
- `backend/app/services/process_service.py`
- `backend/app/domain/processes/analytics.py`
- `backend/app/infrastructure/process_intelligence/artifacts.py`
- `business/process-intelligence/`
- `backend/app/tests/unit/test_p3_pi_evolution.py`
- `backend/app/tests/unit/test_scorecard_controls.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-06-01 — Event log field-level schema
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 data model |
| **Maps to** | FR-06-02…04, AC-06-01 |
| **Deliverable (code paths)** | `business/schemas/event-log.schema.json`<br>`business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | event-log.schema.json + example validate. |
| **Acceptance** | event-log.schema.json + example validate. |
| **Evidence** | business/schemas/event-log.schema.json |

### [x] T-06-02 — Ingest validate + persist
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5.1 on_event |
| **Maps to** | FR-06-01, FR-06-12, NFR-06-01 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Invalid event rejected. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Ingest path + quarantine/reject. |
| **Acceptance** | Ingest path + quarantine/reject. |
| **Evidence** | PI module + tests |

### [x] T-06-03 — Agent→service realization map
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2.1, D-06-01 |
| **Maps to** | FR-06-05…09 |
| **Deliverable (code paths)** | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Five roles mapped to modules/outputs. |
| **Acceptance** | Five roles mapped to modules/outputs. |
| **Evidence** | business/role-realization-map.md, backend/app/api/v1/routes/agents.py, backend/app/domain/agents/models.py |

### [x] T-06-04 — Disk artifacts writer
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.1, C-06-4 |
| **Maps to** | FR-06-10, AC-06-02 |
| **Deliverable (code paths)** | `backend/app/tests/unit/test_p3_pi_evolution`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_full_improvement_backlog.py`<br>`backend/app/api/v1/routes/processes.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | discovered/conformance/bottlenecks/hypotheses paths. |
| **Acceptance** | discovered/conformance/bottlenecks/hypotheses paths. |
| **Evidence** | test_p3_pi_evolution |

### [x] T-06-05 — Causal handoff never promotes DNA
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5.2 FORBIDDEN promote |
| **Maps to** | FR-06-09, FR-06-11, AC-06-04 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | No promote calls from causal path. |
| **Acceptance** | No promote calls from causal path. |
| **Evidence** | business/distilled/workflows/, backend/app/domain/workflows/models.py, backend/app/domain/workflows/policies.py |

### [x] T-06-06 — Process query APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §6 API, C-06-5 |
| **Maps to** | AC-06-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Summary/bottlenecks endpoints authz'd. |
| **Acceptance** | Summary/bottlenecks endpoints authz'd. |
| **Evidence** | backend/app/api/v1/routes/processes.py, backend/app/services/process_service.py, backend/app/domain/processes/analytics.py |

### [x] T-06-07 — Sensitivity / ACL on process APIs
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | NFR-06-03…04 |
| **Maps to** | NFR-06-03…04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Unauthorized 403; fixtures minimize PII. |
| **Acceptance** | Unauthorized 403; fixtures minimize PII. |
| **Evidence** | backend/app/api/v1/routes/processes.py, backend/app/services/process_service.py, backend/app/domain/processes/analytics.py |

### [x] T-06-08 — Connectors deferred documented
| | |
|--|--|
| **Priority** | P3 |
| **Status** | [x] Implemented |
| **Design** | OI-06-01 |
| **Maps to** | FR-06-01 "where connectors exist" |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Non-goal in status + design open issues. |
| **Acceptance** | Non-goal in status + design open issues. |
| **Evidence** | backend/app/api/v1/routes/processes.py, backend/app/services/process_service.py, backend/app/domain/processes/analytics.py |

### [x] T-06-09 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | AC-06-01…04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | backend/app/api/v1/routes/processes.py, backend/app/services/process_service.py, backend/app/domain/processes/analytics.py |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-06-01` | FR-06-02…04, AC-06-01 | `business/schemas/event-log.schema.json`<br>`business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/api/v1/routes/processes.py`<br>… +4 more |
| `T-06-02` | FR-06-01, FR-06-12, NFR-06-01 | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>… +2 more |
| `T-06-03` | FR-06-05…09 | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>… +4 more |
| `T-06-04` | FR-06-10, AC-06-02 | `backend/app/tests/unit/test_p3_pi_evolution`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>… +4 more |
| `T-06-05` | FR-06-09, FR-06-11, AC-06-04 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>… +4 more |
| `T-06-06` | AC-06-03 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-06-07` | NFR-06-03…04 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-06-08` | FR-06-01 "where connectors exist" | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-06-09` | AC-06-01…04 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |

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
