# Tasks — 17 Phased Rollout and Operator Path

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-17-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-17-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-17`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/17_phased-rollout-and-operator-path/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-17**. Each task further narrows via **Deliverable (code paths)**.

- `backend/app/tests/e2e/test_e1_operator_path.py`
- `reviews/e1_operator_checklist.md`
- `status.md`
- `mark_100_verification.md`
- `structure_scorecard_100.md`
- `planning/gap_analysis_for_structure.md`
- `planning/structure/IMPLEMENTATION_STATUS.md`
- `structure.md`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-17-01 — Phase A foundation exit
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3 Phase A |
| **Maps to** | FR-17-01, AC-17-01 |
| **Deliverable (code paths)** | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Tree, schema, inventory, tiers, audit, ≥20 golden. |
| **Acceptance** | Tree, schema, inventory, tiers, audit, ≥20 golden. |
| **Evidence** | business:*, golden count |

### [x] T-17-02 — Phase B shadow learning exit
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3 Phase B |
| **Maps to** | FR-17-02, AC-17-02 |
| **Deliverable (code paths)** | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Event ingest + ≥1 DRC + knowledge path. |
| **Acceptance** | Event ingest + ≥1 DRC + knowledge path. |
| **Evidence** | business/experts/, business/experts/decision-requirement-cards/, business/fixtures/negative/ |

### [x] T-17-03 — Phase C co-pilot exit
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3 Phase C |
| **Maps to** | FR-17-03, AC-17-03 |
| **Deliverable (code paths)** | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | DNA run + gates + provenance + regression. |
| **Acceptance** | DNA run + gates + provenance + regression. |
| **Evidence** | backend/app/tests/e2e/test_e1_operator_path.py, reviews/e1_operator_checklist.md, status.md |

### [x] T-17-04 — Phase D evolution exit
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3 Phase D |
| **Maps to** | FR-17-04…05, AC-17-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_full_improvement_backlog.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Propose/eval/canary/rollback; no auto-promote. |
| **Acceptance** | Propose/eval/canary/rollback; no auto-promote. |
| **Evidence** | backend/app/api/v1/routes/evolution.py, backend/app/api/v1/routes/improvement.py, backend/app/api/v1/routes/loops.py |

### [x] T-17-05 — E1 operator path sequence
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 steps 1–10 |
| **Maps to** | FR-17-06…10, AC-17-05, NFR-17-01 |
| **Deliverable (code paths)** | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/core/idempotency.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md` |
| **Test-first** | e2e is the integration test. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | test_e1_operator_path green. |
| **Acceptance** | test_e1_operator_path green. |
| **Evidence** | backend/app/tests/e2e/test_e1_operator_path.py |

### [x] T-17-06 — Command matrix release gate
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.2 |
| **Maps to** | TV-17-04, AC-17-06 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | npm test, business:*, unit/e2e, FE tests, health postgres. |
| **Acceptance** | npm test, business:*, unit/e2e, FE tests, health postgres. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-17-07 — Verification + scorecard pack
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.1 assets |
| **Maps to** | AC-17-06 |
| **Deliverable (code paths)** | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | mark_100_verification + structure_scorecard_100. |
| **Acceptance** | mark_100_verification + structure_scorecard_100. |
| **Evidence** | backend/app/tests/e2e/test_e1_operator_path.py, reviews/e1_operator_checklist.md, status.md |

### [x] T-17-08 — Ops environment profile
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.3 env |
| **Maps to** | NFR-17-04 |
| **Deliverable (code paths)** | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | DATABASE_URL + DEMO_MODE=false documented. |
| **Acceptance** | DATABASE_URL + DEMO_MODE=false documented. |
| **Evidence** | backend/app/tests/e2e/test_e1_operator_path.py, reviews/e1_operator_checklist.md, status.md |

### [x] T-17-09 — Non-bypass audit
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2 invariant, NFR-17-03 |
| **Maps to** | NFR-17-03 |
| **Deliverable (code paths)** | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | No flags disable auth/gates in ops profile. |
| **Acceptance** | No flags disable auth/gates in ops profile. |
| **Evidence** | backend/app/domain/audit/events.py, backend/app/api/v1/routes/audit_logs.py, backend/app/runtime.py |

### [x] T-17-10 — Non-goals register
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §9 deferred |
| **Maps to** | D-17-03 |
| **Deliverable (code paths)** | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | status.md lists LightRAG/CRM/DGM/Playwright CI/broker. |
| **Acceptance** | status.md lists LightRAG/CRM/DGM/Playwright CI/broker. |
| **Evidence** | backend/app/tests/e2e/test_e1_operator_path.py, reviews/e1_operator_checklist.md, status.md |

### [x] T-17-11 — Structure SDD scores 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | DESIGN_QUALITY_SCORE + this TASKS score |
| **Maps to** | AC-17-06 |
| **Deliverable (code paths)** | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | design 100 + tasks 100 + gap analysis 100. |
| **Acceptance** | design 100 + tasks 100 + gap analysis 100. |
| **Evidence** | DESIGN_QUALITY_SCORE.md, TASKS_QUALITY_SCORE.md, gap_analysis_for_structure.md |

### [x] T-17-12 — Manual UI dogfood optional
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-17-02 |
| **Maps to** | TV-17-03 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Checklist exists; API e2e required. |
| **Acceptance** | Checklist exists; API e2e required. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-17-13 — Exit review (release)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | AC-17-01…06 |
| **Deliverable (code paths)** | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Phases A–D + E1 + matrix + scores 100. |
| **Acceptance** | Phases A–D + E1 + matrix + scores 100. |
| **Evidence** | backend/app/tests/e2e/test_e1_operator_path.py, reviews/e1_operator_checklist.md, status.md |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-17-01` | FR-17-01, AC-17-01 | `business/evals/`<br>`business/evals/golden-tasks/`<br>`business/evals/adversarial-tests/`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>… +4 more |
| `T-17-02` | FR-17-02, AC-17-02 | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>… +4 more |
| `T-17-03` | FR-17-03, AC-17-03 | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| `T-17-04` | FR-17-04…05, AC-17-04 | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>… +4 more |
| `T-17-05` | FR-17-06…10, AC-17-05, NFR-17-01 | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`backend/app/domain/workflows/engine.py`<br>`backend/app/domain/workflows/states.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_run_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>… +4 more |
| `T-17-06` | TV-17-04, AC-17-06 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>… +4 more |
| `T-17-07` | AC-17-06 | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| `T-17-08` | NFR-17-04 | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| `T-17-09` | NFR-17-03 | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>… +3 more |
| `T-17-10` | D-17-03 | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| `T-17-11` | AC-17-06 | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |
| `T-17-12` | TV-17-03 | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>… +4 more |
| `T-17-13` | AC-17-01…06 | `backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`structure_scorecard_100.md`<br>`planning/gap_analysis_for_structure.md`<br>`planning/structure/IMPLEMENTATION_STATUS.md`<br>`structure.md` |

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
