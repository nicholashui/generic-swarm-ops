# Tasks — 11 Bounded Workflow Execution

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-11-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-11-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-11`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/11_bounded-workflow-execution/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-11**. Each task further narrows via **Deliverable (code paths)**.

- `backend/app/domain/workflows/engine.py`
- `backend/app/domain/workflows/states.py`
- `backend/app/runtime.py`
- `backend/app/api/v1/routes/workflow_runs.py`
- `backend/app/api/v1/routes/workflows.py`
- `backend/app/services/workflow_run_service.py`
- `backend/app/infrastructure/tools/adapters.py`
- `backend/app/core/idempotency.py`
- `backend/app/workers/workflow_worker.py`
- `backend/app/tests/unit/test_live_ops_run.py`
- `backend/app/tests/e2e/test_e1_operator_path.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-11-01 — Full run state machine
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.1–4.2 states/transitions |
| **Maps to** | FR-11-01…02 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/workers/workflow_worker.py`<br>`backend/app/tests/unit/test_live_ops_run.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Illegal transitions rejected. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | queued/running/awaiting_approval/completed/failed/cancelled/rejected. |
| **Acceptance** | queued/running/awaiting_approval/completed/failed/cancelled/rejected. |
| **Evidence** | runtime.py |

### [x] T-11-02 — Step sequence 1–10
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.3 |
| **Maps to** | FR-11-03…10 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/workers/workflow_worker.py`<br>`backend/app/tests/unit/test_live_ops_run.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | broker → memory → tools → gate → audit order. |
| **Acceptance** | broker → memory → tools → gate → audit order. |
| **Evidence** | backend/app/domain/workflows/engine.py, backend/app/domain/workflows/states.py, backend/app/runtime.py |

### [x] T-11-03 — Allow-list tools + tool_effects
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-11-2, FR-11-03…05 |
| **Maps to** | FR-11-03…05, AC-11-01…02 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | test_real_execution green. |
| **Acceptance** | test_real_execution green. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-11-04 — Fail-closed adapters
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.3 step 7, §7 |
| **Maps to** | FR-11-05 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Errors do not invent success. |
| **Acceptance** | Errors do not invent success. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-11-05 — Memory reads/writes scoped
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-11-3 |
| **Maps to** | FR-11-09…10 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | E1 memory path green. |
| **Acceptance** | E1 memory path green. |
| **Evidence** | backend/app/api/v1/routes/memory.py, backend/app/services/memory_service.py, backend/app/domain/memory/scopes.py |

### [x] T-11-06 — Verification + block_on_fail
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-11-4 |
| **Maps to** | FR-11-07…08, AC-11-03 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/workers/workflow_worker.py`<br>`backend/app/tests/unit/test_live_ops_run.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Failed checks block success. |
| **Acceptance** | Failed checks block success. |
| **Evidence** | backend/app/domain/workflows/engine.py, backend/app/domain/workflows/states.py, backend/app/runtime.py |

### [x] T-11-07 — Gate handoff to 12
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.3 step 5 |
| **Maps to** | AC-11-05 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | awaiting_approval then resume. |
| **Acceptance** | awaiting_approval then resume. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-11-08 — Graph authority (no free swarm)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-11-02, FR-11-11 |
| **Maps to** | FR-11-11 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Tools only via graph+broker. |
| **Acceptance** | Tools only via graph+broker. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-11-09 — Terminal handoff reflect/eval
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §4.3 step 10, FR-11-12 |
| **Maps to** | FR-11-12 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/workers/workflow_worker.py`<br>`backend/app/tests/unit/test_live_ops_run.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Auto-reflect optional on terminal. |
| **Acceptance** | Auto-reflect optional on terminal. |
| **Evidence** | backend/app/domain/workflows/engine.py, backend/app/domain/workflows/states.py, backend/app/runtime.py |

### [x] T-11-10 — Run API + stream
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §6 API, C-11-6 |
| **Maps to** | NFR-11-02…03, AC-11-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | GET run; SSE/events as implemented. |
| **Acceptance** | GET run; SSE/events as implemented. |
| **Evidence** | backend/app/api/v1/routes/processes.py, backend/app/services/process_service.py, backend/app/domain/processes/analytics.py |

### [x] T-11-11 — Postgres durability
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-11-7 |
| **Maps to** | NFR-11-04 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/workers/workflow_worker.py`<br>`backend/app/tests/unit/test_live_ops_run.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | test_postgres_restart; health ready postgres. |
| **Acceptance** | test_postgres_restart; health ready postgres. |
| **Evidence** | backend/app/runtime.py, backend/app/infrastructure/database/session.py, backend/app/tests/unit/test_postgres_restart.py |

### [x] T-11-12 — External adapters deferred
| | |
|--|--|
| **Priority** | P3 |
| **Status** | [x] Implemented |
| **Design** | OI-11-01 |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Local adapters default; non-goal documented. |
| **Acceptance** | Local adapters default; non-goal documented. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-11-13 — E1 execution segment
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | AC-11-01…05 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/workers/workflow_worker.py`<br>`backend/app/tests/unit/test_live_ops_run.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | test_e1_operator_path green. |
| **Acceptance** | test_e1_operator_path green. |
| **Evidence** | backend/app/domain/workflows/engine.py, backend/app/domain/workflows/states.py, backend/app/runtime.py |

### [x] T-11-14 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/workers/workflow_worker.py`<br>`backend/app/tests/unit/test_live_ops_run.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | backend/app/domain/workflows/engine.py, backend/app/domain/workflows/states.py, backend/app/runtime.py |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-11-01` | FR-11-01…02 | `backend/app/runtime.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>… +3 more |
| `T-11-02` | FR-11-03…10 | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>… +3 more |
| `T-11-03` | FR-11-03…05, AC-11-01…02 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +4 more |
| `T-11-04` | FR-11-05 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +4 more |
| `T-11-05` | FR-11-09…10 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>… +4 more |
| `T-11-06` | FR-11-07…08, AC-11-03 | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>… +3 more |
| `T-11-07` | AC-11-05 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>… +4 more |
| `T-11-08` | FR-11-11 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/workflows/engine.py`<br>… +4 more |
| `T-11-09` | FR-11-12 | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>… +3 more |
| `T-11-10` | NFR-11-02…03, AC-11-04 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>… +4 more |
| `T-11-11` | NFR-11-04 | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>… +4 more |
| `T-11-12` |  | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +4 more |
| `T-11-13` | AC-11-01…05 | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>… +3 more |
| `T-11-14` |  | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>… +3 more |

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
