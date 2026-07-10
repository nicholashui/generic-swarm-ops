# Tasks — 20 Evolution Sandbox APIs

| Field | Value |
|-------|-------|
| Task list ID | `BE-20-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-20-DES`) |
| Paired requirements | `requirements.md` (`BE-20`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 3/3 · AC 5/5 · C-* 3/3 |

---

## SDD workflow

Propose sandbox → evaluate → canary/promote gates → rollback → archive → no host rewrite.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-20. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/evolution.py`
- `backend/app/infrastructure/evolution/corpus_eval.py`
- `backend/app/runtime.py`
- `backend/app/tests/unit/test_scorecard_controls.py`
- `backend/app/tests/unit/test_p3_pi_evolution.py`
- `frontend/src/components/domain/evolution-archive-panel.tsx`
- `frontend/src/app/app/[...slug]/page.tsx`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-20-01 — Propose sandbox_only variants
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-20-1, D-20-01 |
| **Maps to** | FR-20-01, FR-20-02, NFR-20-03, AC-20-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| **Test-first** | Propose creates sandbox variant. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No silent prod write. |
| **Acceptance** | No silent prod write. |
| **Evidence** | api/v1/routes/evolution.py |

### [x] T-20-02 — Evaluate via corpus/fitness
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-20-2 |
| **Maps to** | FR-20-03, AC-20-02 |
| **Deliverable (code paths)** | `backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`backend/app/api/v1/routes/evaluations.py`<br>`backend/app/services/evaluation_service.py`<br>`backend/app/domain/evaluations/evaluators.py`<br>`backend/app/domain/evaluations/models.py` |
| **Test-first** | Evaluate persists scores. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Empirical selection. |
| **Acceptance** | Empirical selection. |
| **Evidence** | infrastructure/evolution/corpus_eval.py |

### [x] T-20-03 — Canary promote + full promote gates
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-20-03 |
| **Maps to** | FR-20-04, FR-20-09, AC-20-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py` |
| **Test-first** | Promote without eval fails. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Gated promotion. |
| **Acceptance** | Gated promotion. |
| **Evidence** | evolution promote path |

### [x] T-20-04 — Rollback path
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5 API |
| **Maps to** | FR-20-05, AC-20-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| **Test-first** | Rollback restores prior. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Reversibility. |
| **Acceptance** | Reversibility. |
| **Evidence** | evolution routes |

### [x] T-20-05 — Fitness/population archive API
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-20-3 |
| **Maps to** | FR-20-06, AC-20-05 |
| **Deliverable (code paths)** | `GET /evolution/archive`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| **Test-first** | Archive lists ranked variants. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | FE /app/evolution data. |
| **Acceptance** | FE /app/evolution data. |
| **Evidence** | GET /evolution/archive |

### [x] T-20-06 — Forbid host code self-rewrite
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-20-02, FR-20-07 |
| **Maps to** | FR-20-07, FR-20-08 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| **Test-first** | No code-write evolution APIs. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | DGM non-goal enforced. |
| **Acceptance** | DGM non-goal enforced. |
| **Evidence** | evolution module scope |

### [x] T-20-07 — AuthZ + audit evolution actions
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-20-10, NFR-20-02 |
| **Maps to** | FR-20-10, NFR-20-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Unauthorized promote 403. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Controlled evolution. |
| **Acceptance** | Controlled evolution. |
| **Evidence** | permissions + audit |

### [x] T-20-08 — Exit review — evolution complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-20-01, AC-20-02, AC-20-03, AC-20-04, AC-20-05 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-20-09 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-20-01 |
| **Deliverable (code paths)** | `requirements.md`<br>`20_evolution-sandbox-apis/tasks.md RTM`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=1 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 20_evolution-sandbox-apis/tasks.md RTM |

### [x] T-20-10 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-20-01, D-20-02, D-20-03 |
| **Maps to** | FR-20-01, FR-20-02, NFR-20-01, AC-20-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-20-11 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-20-01, AC-20-02, AC-20-03, AC-20-04, AC-20-05 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-20-12 — Exit review — BE-20 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-20-01, FR-20-02, FR-20-03, FR-20-04, FR-20-05, FR-20-06, FR-20-07, FR-20-08, FR-20-09, FR-20-10, NFR-20-01, NFR-20-02, NFR-20-03, AC-20-01, AC-20-02, AC-20-03, AC-20-04, AC-20-05 |
| **Deliverable (code paths)** | `planning/backend/20_evolution-sandbox-apis/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/20_evolution-sandbox-apis/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-20-01` | FR-20-01, FR-20-02, NFR-20-03, AC-20-01 | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| `T-20-02` | FR-20-03, AC-20-02 | `backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>… +4 more |
| `T-20-03` | FR-20-04, FR-20-09, AC-20-03 | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>… +5 more |
| `T-20-04` | FR-20-05, AC-20-04 | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| `T-20-05` | FR-20-06, AC-20-05 | `GET /evolution/archive`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>… +1 more |
| `T-20-06` | FR-20-07, FR-20-08 | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx` |
| `T-20-07` | FR-20-10, NFR-20-02 | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>… +5 more |
| `T-20-08` | AC-20-01, AC-20-02, AC-20-03, AC-20-04, AC-20-05 | `tasks.md`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>… +1 more |
| `T-20-09` | NFR-20-01 | `requirements.md`<br>`20_evolution-sandbox-apis/tasks.md RTM`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +2 more |
| `T-20-10` | FR-20-01, FR-20-02, NFR-20-01, AC-20-01 | `backend/app`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>… +1 more |
| `T-20-11` | AC-20-01, AC-20-02, AC-20-03, AC-20-04, AC-20-05 | `backend/app/tests`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>… +1 more |
| `T-20-12` | FR-20-01, FR-20-02, FR-20-03, FR-20-04, FR-20-05, FR-20-06, FR-20-07, FR-20-08, … | `planning/backend/20_evolution-sandbox-apis/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +2 more |

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
