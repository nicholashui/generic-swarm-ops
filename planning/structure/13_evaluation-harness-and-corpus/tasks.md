# Tasks — 13 Evaluation Harness and Corpus

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-13-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-13-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-13`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/13_evaluation-harness-and-corpus/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-13**. Each task further narrows via **Deliverable (code paths)**.

- `business/evals/`
- `business/evals/golden-tasks/`
- `business/evals/adversarial-tests/`
- `backend/app/api/v1/routes/evaluations.py`
- `backend/app/domain/evaluations/evaluators.py`
- `backend/app/services/evaluation_service.py`
- `backend/app/infrastructure/evolution/corpus_eval.py`
- `backend/app/tests/unit/test_scorecard_controls.py`
- `package.json`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-13-01 — Eight eval class locations
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2, §3.1 C-13-1…7 |
| **Maps to** | FR-13-01…08 |
| **Deliverable (code paths)** | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`package.json` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | golden/regression/adversarial/historical/human-review/benchmark/retrieval present. |
| **Acceptance** | golden/regression/adversarial/historical/human-review/benchmark/retrieval present. |
| **Evidence** | business/evals/, business/evals/golden-tasks/, business/evals/adversarial-tests/ |

### [x] T-13-02 — Golden corpus ≥20
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-13-1 |
| **Maps to** | FR-13-01, AC-13-01 |
| **Deliverable (code paths)** | `business/evals/golden-tasks/`<br>`business/evals/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`package.json` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Count ≥20 JSON tasks. |
| **Acceptance** | Count ≥20 JSON tasks. |
| **Evidence** | business/evals/golden-tasks/ |

### [x] T-13-03 — business:eval harness green
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-13-8, §5 algorithm |
| **Maps to** | AC-13-05, NFR-13-01 |
| **Deliverable (code paths)** | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`package.json` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | npm run business:eval pass. |
| **Acceptance** | npm run business:eval pass. |
| **Evidence** | business/evals/, business/evals/golden-tasks/, business/evals/adversarial-tests/ |

### [x] T-13-04 — Evaluation card model
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 card |
| **Maps to** | FR-13-09…10, AC-13-03 |
| **Deliverable (code paths)** | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`package.json` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Schema + example validate. |
| **Acceptance** | Schema + example validate. |
| **Evidence** | business/evals/, business/evals/golden-tasks/, business/evals/adversarial-tests/ |

### [x] T-13-05 — INV: no auto production promote
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-13-02, FR-13-12…13 |
| **Maps to** | AC-13-04 |
| **Deliverable (code paths)** | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`package.json` |
| **Test-first** | Negative assertion. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Harness/evolution block unattended promote. |
| **Acceptance** | Harness/evolution block unattended promote. |
| **Evidence** | business/evals/, business/evals/golden-tasks/, business/evals/adversarial-tests/ |

### [x] T-13-06 — Multi-step tool-using cases preferred
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-13-03, FR-13-11 |
| **Maps to** | FR-13-11 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Flagship/onboarding fixtures multi-step. |
| **Acceptance** | Flagship/onboarding fixtures multi-step. |
| **Evidence** | backend/app/domain/workflows/engine.py, backend/app/domain/workflows/states.py, backend/app/runtime.py |

### [x] T-13-07 — Runtime required_checks integration
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-13-10 |
| **Maps to** | design runtime path |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | block_on_fail works with execution (11). |
| **Acceptance** | block_on_fail works with execution (11). |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-13-08 — No secrets in fixtures
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-13-04 |
| **Maps to** | NFR-13-04 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`business/evals/`<br>`business/evals/golden-tasks/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | security scan clean on evals. |
| **Acceptance** | security scan clean on evals. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-13-09 — FE evaluations surface
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §6 FE |
| **Maps to** | design interfaces |
| **Deliverable (code paths)** | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`package.json` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | /app/evaluations lists cards. |
| **Acceptance** | /app/evaluations lists cards. |
| **Evidence** | business/evals/, business/evals/golden-tasks/, business/evals/adversarial-tests/ |

### [x] T-13-10 — Content growth backlog documented
| | |
|--|--|
| **Priority** | P2 |
| **Status** | [x] Implemented |
| **Design** | OI-13-01 |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`package.json` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Exhaustive per-agent packs = content growth, not P0 gap. |
| **Acceptance** | Exhaustive per-agent packs = content growth, not P0 gap. |
| **Evidence** | business/evals/, business/evals/golden-tasks/, business/evals/adversarial-tests/ |

### [x] T-13-11 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`package.json` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | business/evals/, business/evals/golden-tasks/, business/evals/adversarial-tests/ |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-13-01` | FR-13-01…08 | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +1 more |
| `T-13-02` | FR-13-01, AC-13-01 | `business/evals/golden-tasks/`<br>`business/evals/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +1 more |
| `T-13-03` | AC-13-05, NFR-13-01 | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +1 more |
| `T-13-04` | FR-13-09…10, AC-13-03 | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +1 more |
| `T-13-05` | AC-13-04 | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +1 more |
| `T-13-06` | FR-13-11 | `backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>… +4 more |
| `T-13-07` | design runtime path | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`business/evals/`<br>`business/evals/golden-tasks/`<br>… +4 more |
| `T-13-08` | NFR-13-04 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +4 more |
| `T-13-09` | design interfaces | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +1 more |
| `T-13-10` |  | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +1 more |
| `T-13-11` |  | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +1 more |

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
