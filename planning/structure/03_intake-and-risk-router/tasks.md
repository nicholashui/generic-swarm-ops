# Tasks — 03 Intake and Risk Router

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-03-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-03-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-03`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/03_intake-and-risk-router/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-03**. Each task further narrows via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/workflows.py`
- `backend/app/api/v1/routes/workflow_runs.py`
- `backend/app/services/workflow_run_service.py`
- `backend/app/runtime.py`
- `backend/app/core/idempotency.py`
- `backend/app/domain/governance/risk.py`
- `backend/app/tests/e2e/test_e1_operator_path.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-03-01 — Pipeline steps 1–7 implemented
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3.1 sequence |
| **Maps to** | FR-03-01…04 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | 401/403/422 before happy path. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Flagship start works. |
| **Acceptance** | Flagship start works. |
| **Evidence** | runtime run start, E1 |

### [x] T-03-02 — AuthN/AuthZ on start
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-03-1, C-03-2, §5.1 |
| **Maps to** | NFR-03-03, AC-03-02, TV-03-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Unauthenticated → 401; unauthorized → 403. |
| **Acceptance** | Unauthenticated → 401; unauthorized → 403. |
| **Evidence** | API tests / live_ops |

### [x] T-03-03 — Input validation 422
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-03-3, §5.1 |
| **Maps to** | FR-03-01, NFR-03-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Missing case_id/required inputs → 422 + request_id. |
| **Acceptance** | Missing case_id/required inputs → 422 + request_id. |
| **Evidence** | unit/live tests |

### [x] T-03-04 — Risk classification decision table
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.1–4.2, C-03-4 |
| **Maps to** | FR-03-02…03, FR-03-05, AC-03-01 |
| **Deliverable (code paths)** | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Every run has risk_tier; tier_4 flagship expects gates. |
| **Acceptance** | Every run has risk_tier; tier_4 flagship expects gates. |
| **Evidence** | run records, E1 |

### [x] T-03-05 — Run record fields complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.3 |
| **Maps to** | FR-03-03, AC-03-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | id, workflow_id, risk_tier, status, inputs, created_by, request_id. |
| **Acceptance** | id, workflow_id, risk_tier, status, inputs, created_by, request_id. |
| **Evidence** | backend/app/api/v1/routes/workflows.py, backend/app/api/v1/routes/workflow_runs.py, backend/app/services/workflow_run_service.py |

### [x] T-03-06 — Audit on start/reject
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-03-6, §3.1 step 6 |
| **Maps to** | FR-03-06, AC-03-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Audit query shows start classification/run.started. |
| **Acceptance** | Audit query shows start classification/run.started. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-03-07 — Invariant: no tools before persist
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3.1 invariant |
| **Maps to** | FR-03-07, AC-03-04 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Code path: adapters only after run exists. |
| **Acceptance** | Code path: adapters only after run exists. |
| **Evidence** | backend/app/runtime.py, backend/app/infrastructure/database/session.py, backend/app/tests/unit/test_postgres_restart.py |

### [x] T-03-08 — Error envelope ICD
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §5.2 |
| **Maps to** | NFR-03-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | `{message, request_id}` on failures. |
| **Acceptance** | `{message, request_id}` on failures. |
| **Evidence** | backend/app/api/v1/routes/workflows.py, backend/app/api/v1/routes/workflow_runs.py, backend/app/services/workflow_run_service.py |

### [x] T-03-09 — Idempotency (optional documented)
| | |
|--|--|
| **Priority** | P2 |
| **Status** | [x] Implemented |
| **Design** | C-03-7, OI-03-02 |
| **Maps to** | NFR-03-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Documented optional; implement when multi-instance races appear. |
| **Acceptance** | Documented optional; implement when multi-instance races appear. |
| **Evidence** | backend/app/api/v1/routes/workflows.py, backend/app/api/v1/routes/workflow_runs.py, backend/app/services/workflow_run_service.py |

### [x] T-03-10 — Metrics hooks
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §7 metrics |
| **Maps to** | NFR-03-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Request metrics / logging present on API. |
| **Acceptance** | Request metrics / logging present on API. |
| **Evidence** | backend/app/api/v1/routes/workflows.py, backend/app/api/v1/routes/workflow_runs.py, backend/app/services/workflow_run_service.py |

### [x] T-03-11 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | AC-03-01…04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | E1 start segment green; score 100. |
| **Acceptance** | E1 start segment green; score 100. |
| **Evidence** | backend/app/api/v1/routes/workflows.py, backend/app/api/v1/routes/workflow_runs.py, backend/app/services/workflow_run_service.py |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-03-01` | FR-03-01…04 | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>… +2 more |
| `T-03-02` | NFR-03-03, AC-03-02, TV-03-02 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>… +4 more |
| `T-03-03` | FR-03-01, NFR-03-04 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| `T-03-04` | FR-03-02…03, FR-03-05, AC-03-01 | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`backend/app/api/v1/routes/workflows.py`<br>… +4 more |
| `T-03-05` | FR-03-03, AC-03-01 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| `T-03-06` | FR-03-06, AC-03-03 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>… +4 more |
| `T-03-07` | FR-03-07, AC-03-04 | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>… +1 more |
| `T-03-08` | NFR-03-04 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| `T-03-09` | NFR-03-02 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| `T-03-10` | NFR-03-01 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| `T-03-11` | AC-03-01…04 | `backend/app/api/v1/routes/workflows.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/runtime.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |

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
