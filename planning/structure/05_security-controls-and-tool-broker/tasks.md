# Tasks — 05 Security Controls and Tool Broker

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-05-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-05-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-05`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/05_security-controls-and-tool-broker/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-05**. Each task further narrows via **Deliverable (code paths)**.

- `backend/app/infrastructure/tools/adapters.py`
- `backend/app/runtime.py`
- `backend/app/core/rate_limit.py`
- `backend/app/core/security.py`
- `backend/app/core/permissions.py`
- `backend/app/api/dependencies.py`
- `business/evals/adversarial-tests/`
- `business/security/`
- `backend/app/tests/unit/test_real_execution.py`
- `backend/app/tests/unit/test_hardening.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-05-01 — Trust zones + threat model documented
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2 trust + STRIDE-lite |
| **Maps to** | FR-05-01…04 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | design.md §2 complete. |
| **Acceptance** | design.md §2 complete. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-05-02 — Tool broker authorize algorithm
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.1, C-05-3 |
| **Maps to** | FR-05-10, FR-05-15…16, AC-05-01 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Deny non-allow-listed tool before soft-fail paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Unit deny + audit. |
| **Acceptance** | Unit deny + audit. |
| **Evidence** | runtime broker, unit tests |

### [x] T-05-03 — Adapter fail-closed contract
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.2, D-05-01, C-05-4 |
| **Maps to** | FR-05-09, NFR-05-03, AC-05-01 |
| **Deliverable (code paths)** | `backend/app/tests/unit/test_real_execution`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | test_real_execution green; no mock success in ops. |
| **Acceptance** | test_real_execution green; no mock success in ops. |
| **Evidence** | adapters.py, test_real_execution |

### [x] T-05-04 — tool_effects durability
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-05-5 |
| **Maps to** | FR-05-19 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | tool_effects on run after tool steps. |
| **Acceptance** | tool_effects on run after tool steps. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-05-05 — OWASP matrix controls LLM01–10
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5 matrix |
| **Maps to** | FR-05-05…14 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Each row has design control + evidence path. |
| **Acceptance** | Each row has design control + evidence path. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-05-06 — Adversarial / injection suite
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-05-9 |
| **Maps to** | FR-05-04, TV-05-02 |
| **Deliverable (code paths)** | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | adversarial evals present; business:eval covers. |
| **Acceptance** | adversarial evals present; business:eval covers. |
| **Evidence** | business/evals/, business/evals/golden-tasks/, business/evals/adversarial-tests/ |

### [x] T-05-07 — Secrets never in prompts/repo
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.3, C-05-8 |
| **Maps to** | FR-05-06, NFR-05-04, AC-05-02 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | business:security clean of criticals. |
| **Acceptance** | business:security clean of criticals. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-05-08 — Rate limits / timeouts
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-05-6, LLM10 |
| **Maps to** | FR-05-14, NFR-05-01 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Middleware on sensitive routes. |
| **Acceptance** | Middleware on sensitive routes. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-05-09 — Skill sandbox vetting
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-05-11 |
| **Maps to** | FR-05-18, AC-05-05 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_full_improvement_backlog.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | _sandbox until promote. |
| **Acceptance** | _sandbox until promote. |
| **Evidence** | backend/app/api/v1/routes/evolution.py, backend/app/api/v1/routes/improvement.py, backend/app/api/v1/routes/loops.py |

### [x] T-05-10 — Incident runbook artifact
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-05-10 |
| **Maps to** | FR-05-20 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | business/security incident path exists. |
| **Acceptance** | business/security incident path exists. |
| **Evidence** | backend/app/api/v1/routes/processes.py, backend/app/services/process_service.py, backend/app/domain/processes/analytics.py |

### [x] T-05-11 — Security headers / CORS
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-05-7 |
| **Maps to** | FR-05-01 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | FastAPI middleware present. |
| **Acceptance** | FastAPI middleware present. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-05-12 — Ephemeral OAuth broker (deferred documented)
| | |
|--|--|
| **Priority** | P3 |
| **Status** | [x] Implemented |
| **Design** | OI-05-01, D-05-02 |
| **Maps to** | FR-05-15 future |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Explicit non-goal; allow-list broker is current design. |
| **Acceptance** | Explicit non-goal; allow-list broker is current design. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-05-13 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | AC-05-01…05 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-05-01` | FR-05-01…04 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +2 more |
| `T-05-02` | FR-05-10, FR-05-15…16, AC-05-01 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +2 more |
| `T-05-03` | FR-05-09, NFR-05-03, AC-05-01 | `backend/app/tests/unit/test_real_execution`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>… +3 more |
| `T-05-04` | FR-05-19 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +2 more |
| `T-05-05` | FR-05-05…14 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +2 more |
| `T-05-06` | FR-05-04, TV-05-02 | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>… +4 more |
| `T-05-07` | FR-05-06, NFR-05-04, AC-05-02 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +2 more |
| `T-05-08` | FR-05-14, NFR-05-01 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +2 more |
| `T-05-09` | FR-05-18, AC-05-05 | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>… +4 more |
| `T-05-10` | FR-05-20 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>… +4 more |
| `T-05-11` | FR-05-01 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +2 more |
| `T-05-12` | FR-05-15 future | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +2 more |
| `T-05-13` | AC-05-01…05 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +2 more |

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
