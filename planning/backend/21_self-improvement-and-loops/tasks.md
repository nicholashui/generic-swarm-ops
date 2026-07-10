# Tasks — 21 Self-Improvement and Loops

| Field | Value |
|-------|-------|
| Task list ID | `BE-21-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-21-DES`) |
| Paired requirements | `requirements.md` (`BE-21`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 9/9 · NFR 3/3 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Reflect/lessons → auto-propose sandbox → skill sandbox → loop runner → E1 improve.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-21. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/improvement.py`
- `backend/app/api/v1/routes/loops.py`
- `backend/app/infrastructure/self_improvement/reflection.py`
- `backend/app/infrastructure/self_improvement/lessons.py`
- `backend/app/infrastructure/self_improvement/skill_sandbox.py`
- `backend/app/infrastructure/self_improvement/llm_critic.py`
- `backend/app/infrastructure/loop_engineering/runner.py`
- `backend/app/infrastructure/loop_engineering/loop_dna.py`
- `backend/app/tests/unit/test_full_improvement_backlog.py`
- `backend/app/tests/unit/test_self_improvement_orchestration.py`
- `frontend/src/components/domain/improve-run-button.tsx`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-21-01 — Reflect on run → lessons
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-21-1 |
| **Maps to** | FR-21-01, FR-21-02, NFR-21-01, AC-21-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| **Test-first** | POST reflect creates lessons. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Learning capture. |
| **Acceptance** | Learning capture. |
| **Evidence** | api/v1/routes/improvement.py |

### [x] T-21-02 — Auto-propose sandbox variants from lessons
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-21-01 |
| **Maps to** | FR-21-03, FR-21-08, AC-21-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py` |
| **Test-first** | Propose is sandbox_only. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No direct prod DNA mutate. |
| **Acceptance** | No direct prod DNA mutate. |
| **Evidence** | improvement routes |

### [x] T-21-03 — Optional LLM critic feature flag
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-21-4, D-21-02 |
| **Maps to** | FR-21-04, NFR-21-02 |
| **Deliverable (code paths)** | `backend/app/infrastructure/llm/*`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| **Test-first** | Disabled by default; no env dump. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Cost/safety controlled. |
| **Acceptance** | Cost/safety controlled. |
| **Evidence** | infrastructure/llm/* |

### [x] T-21-04 — Skill sandbox write + explicit promote
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-21-03 |
| **Maps to** | FR-21-05, NFR-21-03, AC-21-03 |
| **Deliverable (code paths)** | `improvement/skills`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| **Test-first** | Sandbox not promoted until action. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Vetted skills. |
| **Acceptance** | Vetted skills. |
| **Evidence** | improvement/skills |

### [x] T-21-05 — Loop DNA runner start/status
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-21-2, C-21-3 |
| **Maps to** | FR-21-06, AC-21-04 |
| **Deliverable (code paths)** | `backend/app/infrastructure/loop_engineering/*`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| **Test-first** | Start returns id. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Bounded loops. |
| **Acceptance** | Bounded loops. |
| **Evidence** | infrastructure/loop_engineering/* |

### [x] T-21-06 — Auto-reflect on terminal runs (flag)
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | FR-21-07 |
| **Maps to** | FR-21-07 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| **Test-first** | With AUTO_REFLECT=true lessons appear. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Closed loop option. |
| **Acceptance** | Closed loop option. |
| **Evidence** | runtime terminal hook |

### [x] T-21-07 — AuthZ + provenance on improve actions
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-21-09 |
| **Maps to** | FR-21-09 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Unauthorized denied; provenance stored. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Governed SI. |
| **Acceptance** | Governed SI. |
| **Evidence** | improvement + audit |

### [x] T-21-08 — E1 improve segment
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | TV-21-03 |
| **Maps to** | AC-21-01, AC-21-02, AC-21-03, AC-21-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| **Test-first** | E1 reflect→propose→eval→canary. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | E1 green. |
| **Acceptance** | E1 green. |
| **Evidence** | test_e1_operator_path |

### [x] T-21-09 — Exit review — self-improvement complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-21-01, AC-21-02, AC-21-03, AC-21-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-21-10 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-21-01, D-21-02, D-21-03 |
| **Maps to** | FR-21-01, FR-21-02, NFR-21-01, AC-21-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-21-11 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-21-01, AC-21-02, AC-21-03, AC-21-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-21-12 — Exit review — BE-21 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-21-01, FR-21-02, FR-21-03, FR-21-04, FR-21-05, FR-21-06, FR-21-07, FR-21-08, FR-21-09, NFR-21-01, NFR-21-02, NFR-21-03, AC-21-01, AC-21-02, AC-21-03, AC-21-04 |
| **Deliverable (code paths)** | `planning/backend/21_self-improvement-and-loops/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/21_self-improvement-and-loops/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-21-01` | FR-21-01, FR-21-02, NFR-21-01, AC-21-01 | `backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| `T-21-02` | FR-21-03, FR-21-08, AC-21-02 | `backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py`<br>… +5 more |
| `T-21-03` | FR-21-04, NFR-21-02 | `backend/app/infrastructure/llm/*`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>… +1 more |
| `T-21-04` | FR-21-05, NFR-21-03, AC-21-03 | `improvement/skills`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>… +1 more |
| `T-21-05` | FR-21-06, AC-21-04 | `backend/app/infrastructure/loop_engineering/*`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>… +1 more |
| `T-21-06` | FR-21-07 | `backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| `T-21-07` | FR-21-09 | `backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py`<br>… +5 more |
| `T-21-08` | AC-21-01, AC-21-02, AC-21-03, AC-21-04 | `backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/self_improvement/llm_critic.py` |
| `T-21-09` | AC-21-01, AC-21-02, AC-21-03, AC-21-04 | `tasks.md`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>… +1 more |
| `T-21-10` | FR-21-01, FR-21-02, NFR-21-01, AC-21-01 | `backend/app`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>… +1 more |
| `T-21-11` | AC-21-01, AC-21-02, AC-21-03, AC-21-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>… +1 more |
| `T-21-12` | FR-21-01, FR-21-02, FR-21-03, FR-21-04, FR-21-05, FR-21-06, FR-21-07, FR-21-08, … | `planning/backend/21_self-improvement-and-loops/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>… +2 more |

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
