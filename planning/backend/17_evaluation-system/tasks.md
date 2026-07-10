# Tasks — 17 Evaluation System

| Field | Value |
|-------|-------|
| Task list ID | `BE-17-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-17-DES`) |
| Paired requirements | `requirements.md` (`BE-17`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 8/8 · NFR 4/4 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Evaluators → persist results → block promote on required fail → corpus eval for evolution.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-17. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/evaluations.py`
- `backend/app/services/evaluation_service.py`
- `backend/app/domain/evaluations/evaluators.py`
- `backend/app/domain/evaluations/models.py`
- `backend/app/infrastructure/evolution/corpus_eval.py`
- `backend/app/schemas/evaluations.py`
- `backend/app/workers/evaluation_worker.py`
- `business/evals/`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-17-01 — Evaluator types + result statuses
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-17-2, §4 |
| **Maps to** | FR-17-01, FR-17-02, FR-17-03 |
| **Deliverable (code paths)** | `backend/app/domain/evaluations/evaluators.py`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| **Test-first** | Schema pass/fail unit. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Multi-type eval. |
| **Acceptance** | Multi-type eval. |
| **Evidence** | domain/evaluations/evaluators.py |

### [x] T-17-02 — Link results to run/step/output
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 |
| **Maps to** | FR-17-04, AC-17-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| **Test-first** | Query by run id. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Traceable quality. |
| **Acceptance** | Traceable quality. |
| **Evidence** | evaluation models |

### [x] T-17-03 — Manual evaluation APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-17-1 |
| **Maps to** | FR-17-05, AC-17-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| **Test-first** | POST run evaluation persists. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Ops can trigger. |
| **Acceptance** | Ops can trigger. |
| **Evidence** | api/v1/routes/evaluations.py |

### [x] T-17-04 — Required fail blocks release/promote
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-17-02 |
| **Maps to** | FR-17-06, AC-17-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| **Test-first** | Failed required blocks promote path. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safety gate. |
| **Acceptance** | Safety gate. |
| **Evidence** | evolution promote + eval |

### [x] T-17-05 — Corpus evaluation for fitness
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-17-3 |
| **Maps to** | FR-17-07, AC-17-04 |
| **Deliverable (code paths)** | `backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/schemas/evaluations.py` |
| **Test-first** | Corpus eval smoke. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Evolution has scores. |
| **Acceptance** | Evolution has scores. |
| **Evidence** | infrastructure/evolution/corpus_eval.py |

### [x] T-17-06 — Persist evaluation runs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-17-08 |
| **Maps to** | FR-17-08 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py` |
| **Test-first** | History retained. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Comparable over time. |
| **Acceptance** | Comparable over time. |
| **Evidence** | store |

### [x] T-17-07 — AuthZ + no secret fixtures
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | NFR-17-03…04 |
| **Maps to** | NFR-17-03, NFR-17-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Unauthorized config denied. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safe corpora. |
| **Acceptance** | Safe corpora. |
| **Evidence** | evals fixtures |

### [x] T-17-08 — Exit review — evaluation complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-17-01, AC-17-02, AC-17-03, AC-17-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-17-09 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-17-01, NFR-17-02 |
| **Deliverable (code paths)** | `requirements.md`<br>`17_evaluation-system/tasks.md RTM`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=2 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 17_evaluation-system/tasks.md RTM |

### [x] T-17-10 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-17-01, D-17-02 |
| **Maps to** | FR-17-01, FR-17-02, NFR-17-01, AC-17-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-17-11 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-17-01, AC-17-02, AC-17-03, AC-17-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-17-12 — Exit review — BE-17 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-17-01, FR-17-02, FR-17-03, FR-17-04, FR-17-05, FR-17-06, FR-17-07, FR-17-08, NFR-17-01, NFR-17-02, NFR-17-03, NFR-17-04, AC-17-01, AC-17-02, AC-17-03, AC-17-04 |
| **Deliverable (code paths)** | `planning/backend/17_evaluation-system/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/17_evaluation-system/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-17-01` | FR-17-01, FR-17-02, FR-17-03 | `backend/app/domain/evaluations/evaluators.py`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| `T-17-02` | FR-17-04, AC-17-03 | `backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| `T-17-03` | FR-17-05, AC-17-01 | `backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| `T-17-04` | FR-17-06, AC-17-02 | `backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py` |
| `T-17-05` | FR-17-07, AC-17-04 | `backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/schemas/evaluations.py` |
| `T-17-06` | FR-17-08 | `backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py`<br>… +5 more |
| `T-17-07` | NFR-17-03, NFR-17-04 | `backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/schemas/evaluations.py`<br>… +5 more |
| `T-17-08` | AC-17-01, AC-17-02, AC-17-03, AC-17-04 | `tasks.md`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>… +1 more |
| `T-17-09` | NFR-17-01, NFR-17-02 | `requirements.md`<br>`17_evaluation-system/tasks.md RTM`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>… +2 more |
| `T-17-10` | FR-17-01, FR-17-02, NFR-17-01, AC-17-01 | `backend/app`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>… +1 more |
| `T-17-11` | AC-17-01, AC-17-02, AC-17-03, AC-17-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>… +1 more |
| `T-17-12` | FR-17-01, FR-17-02, FR-17-03, FR-17-04, FR-17-05, FR-17-06, FR-17-07, FR-17-08, … | `planning/backend/17_evaluation-system/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py`<br>… +2 more |

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
