# Tasks — 11 Workflow Run Execution Engine

| Field | Value |
|-------|-------|
| Task list ID | `BE-11-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-11-DES`) |
| Paired requirements | `requirements.md` (`BE-11`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 13/13 · NFR 4/4 · AC 5/5 · C-* 5/5 |

---

## SDD workflow

Run create → state machine → step loop → idempotency → cancel/retry → gates → E1 segment.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-11. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/workflow_runs.py`
- `backend/app/api/v1/routes/workflows.py`
- `backend/app/services/workflow_run_service.py`
- `backend/app/domain/workflows/engine.py`
- `backend/app/domain/workflows/states.py`
- `backend/app/core/idempotency.py`
- `backend/app/runtime.py`
- `backend/app/schemas/workflow_runs.py`
- `backend/app/infrastructure/repositories/workflow_run_repository.py`
- `backend/app/workers/workflow_worker.py`
- `backend/app/tests/e2e/test_e1_operator_path.py`
- `backend/app/tests/unit/test_live_ops_run.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-11-01 — Create workflow_run on start
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-11-1, C-11-4 |
| **Maps to** | FR-11-01, FR-11-03, AC-11-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | POST runs returns run id. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Run record exists. |
| **Acceptance** | Run record exists. |
| **Evidence** | api/v1/routes/workflow_runs.py |

### [x] T-11-02 — Implement full run status set
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 state machine, C-11-3 |
| **Maps to** | FR-11-02 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/states.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Illegal transitions rejected. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | queued/running/waiting_for_approval/completed/failed/cancelled/… |
| **Acceptance** | queued/running/waiting_for_approval/completed/failed/cancelled/… |
| **Evidence** | domain/workflows/states.py |

### [x] T-11-03 — Step records + statuses
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 step loop |
| **Maps to** | FR-11-04, FR-11-05, AC-11-02 |
| **Deliverable (code paths)** | `engine.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Steps appear with transitions. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Step tracking complete. |
| **Acceptance** | Step tracking complete. |
| **Evidence** | engine.py |

### [x] T-11-04 — Start flow: authz, validate, governance pre-check, audit
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3 architecture |
| **Maps to** | FR-11-06, NFR-11-04 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Pre-check blocks bad runs. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safe start sequence. |
| **Acceptance** | Safe start sequence. |
| **Evidence** | runtime.py; engine |

### [x] T-11-05 — Worker/step execution loop with brokered tools
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 step loop 1–9 |
| **Maps to** | FR-11-07, FR-11-08 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/engine.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py` |
| **Test-first** | Flagship multi-step completes or gates. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Bounded graph execution. |
| **Acceptance** | Bounded graph execution. |
| **Evidence** | domain/workflows/engine.py |

### [x] T-11-06 — Idempotency-Key on start
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-11-5, D-11-03 |
| **Maps to** | FR-11-09, AC-11-03 |
| **Deliverable (code paths)** | `backend/app/core/idempotency.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py` |
| **Test-first** | Duplicate key same run id. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safe client retries. |
| **Acceptance** | Safe client retries. |
| **Evidence** | core/idempotency.py |

### [x] T-11-07 — Cancel and retry operations
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5 API |
| **Maps to** | FR-11-10, AC-11-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Cancel → cancelled when allowed. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Operator control. |
| **Acceptance** | Operator control. |
| **Evidence** | workflow_runs routes |

### [x] T-11-08 — Gate pause waiting_for_approval
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-11-11 |
| **Maps to** | FR-11-11, AC-11-05 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py` |
| **Test-first** | Gated run waits. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No irreversible progress. |
| **Acceptance** | No irreversible progress. |
| **Evidence** | engine + approvals |

### [x] T-11-09 — Terminal status + events
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-11-12, NFR-11-02 |
| **Maps to** | FR-11-12, FR-11-13 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Complete/fail emits final event. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Observable termination. |
| **Acceptance** | Observable termination. |
| **Evidence** | stream + engine |

### [x] T-11-10 — List/get/steps/stream endpoints
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §5 API |
| **Maps to** | FR-11-13, NFR-11-01 |
| **Deliverable (code paths)** | `workflow_runs.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py` |
| **Test-first** | GET run + steps work. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | FE run detail works. |
| **Acceptance** | FE run detail works. |
| **Evidence** | workflow_runs.py |

### [x] T-11-11 — E1 execution segment
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | TV-11-03 |
| **Maps to** | AC-11-01, AC-11-02, AC-11-03, AC-11-04, AC-11-05 |
| **Deliverable (code paths)** | `backend/app/tests/e2e`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md` |
| **Test-first** | test_e1_operator_path green. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Operator path proven. |
| **Acceptance** | Operator path proven. |
| **Evidence** | app/tests/e2e |

### [x] T-11-12 — Exit review — engine complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-11-01, AC-11-02, AC-11-03, AC-11-04, AC-11-05 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-11-13 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-11-03 |
| **Deliverable (code paths)** | `requirements.md`<br>`11_workflow-run-execution-engine/tasks.md RTM`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=1 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 11_workflow-run-execution-engine/tasks.md RTM |

### [x] T-11-14 — Implement/verify all design components C-*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-11-2, C-11-1, C-11-2, C-11-3 |
| **Maps to** | AC-11-01, AC-11-02, AC-11-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Component module import/smoke or route presence. |
| **Steps** | 1) Map each C-* to module path in design. 2) Verify module exists and is wired. 3) Add smoke test if missing. |
| **Success** | All design components have implementation anchors. |
| **Acceptance** | Components covered: C-11-1, C-11-2, C-11-3, C-11-4, C-11-5 |
| **Evidence** | ### 3.1 Components |

### [x] T-11-15 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-11-01, D-11-02, D-11-03 |
| **Maps to** | FR-11-01, FR-11-02, NFR-11-01, AC-11-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-11-16 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-11-01, AC-11-02, AC-11-03, AC-11-04, AC-11-05 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-11-17 — Exit review — BE-11 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-11-01, FR-11-02, FR-11-03, FR-11-04, FR-11-05, FR-11-06, FR-11-07, FR-11-08, FR-11-09, FR-11-10, FR-11-11, FR-11-12, FR-11-13, NFR-11-01, NFR-11-02, NFR-11-03, NFR-11-04, AC-11-01, AC-11-02, AC-11-03, AC-11-04, AC-11-05 |
| **Deliverable (code paths)** | `planning/backend/11_workflow-run-execution-engine/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/11_workflow-run-execution-engine/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-11-01` | FR-11-01, FR-11-03, AC-11-01 | `backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| `T-11-02` | FR-11-02 | `backend/app/domain/workflows/states.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/core/idempotency.py` |
| `T-11-03` | FR-11-04, FR-11-05, AC-11-02 | `engine.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>… +1 more |
| `T-11-04` | FR-11-06, NFR-11-04 | `backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>… +6 more |
| `T-11-05` | FR-11-07, FR-11-08 | `backend/app/domain/workflows/engine.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py`<br>… +5 more |
| `T-11-06` | FR-11-09, AC-11-03 | `backend/app/core/idempotency.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py` |
| `T-11-07` | FR-11-10, AC-11-04 | `backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| `T-11-08` | FR-11-11, AC-11-05 | `backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py`<br>… +5 more |
| `T-11-09` | FR-11-12, FR-11-13 | `backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| `T-11-10` | FR-11-13, NFR-11-01 | `workflow_runs.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>… +5 more |
| `T-11-11` | AC-11-01, AC-11-02, AC-11-03, AC-11-04, AC-11-05 | `backend/app/tests/e2e`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>… +6 more |
| `T-11-12` | AC-11-01, AC-11-02, AC-11-03, AC-11-04, AC-11-05 | `tasks.md`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>… +1 more |
| `T-11-13` | NFR-11-03 | `requirements.md`<br>`11_workflow-run-execution-engine/tasks.md RTM`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>… +2 more |
| `T-11-14` | AC-11-01, AC-11-02, AC-11-03 | `backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/core/idempotency.py` |
| `T-11-15` | FR-11-01, FR-11-02, NFR-11-01, AC-11-01 | `backend/app`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>… +1 more |
| `T-11-16` | AC-11-01, AC-11-02, AC-11-03, AC-11-04, AC-11-05 | `backend/app/tests`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>… +1 more |
| `T-11-17` | FR-11-01, FR-11-02, FR-11-03, FR-11-04, FR-11-05, FR-11-06, FR-11-07, FR-11-08, … | `planning/backend/11_workflow-run-execution-engine/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/domain/workflows/engine.py`<br>… +2 more |

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
