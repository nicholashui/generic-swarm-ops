# Tasks — 22 Production DNA Safety

| Field | Value |
|-------|-------|
| Task list ID | `BE-22-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-22-DES`) |
| Paired requirements | `requirements.md` (`BE-22`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 7/7 · NFR 2/2 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Validators → activate hooks → business:validate → structured errors → rejection lessons.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-22. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/infrastructure/governance/structure_validators.py`
- `backend/app/runtime.py`
- `backend/app/services/workflow_service.py`
- `backend/app/tests/unit/test_structure_sdd_validators.py`
- `business/fixtures/negative/`
- `package.json`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-22-01 — Implement structure_validators checks
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-22-1, §4 checks |
| **Maps to** | FR-22-01, FR-22-02, NFR-22-01, AC-22-02, AC-22-03 |
| **Deliverable (code paths)** | `backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| **Test-first** | Negative DNA fixtures fail. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Deterministic safety. |
| **Acceptance** | Deterministic safety. |
| **Evidence** | infrastructure/governance/structure_validators.py |

### [x] T-22-02 — Hook validators on activate/production_ready
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-22-2, D-22-01 |
| **Maps to** | FR-22-04, FR-22-07, AC-22-01 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py` |
| **Test-first** | Valid DNA activates; invalid rejected. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No partial unsafe activate. |
| **Acceptance** | No partial unsafe activate. |
| **Evidence** | runtime.py |

### [x] T-22-03 — Integrate business:validate style checks
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-22-3 |
| **Maps to** | FR-22-03 |
| **Deliverable (code paths)** | `package scripts / business`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| **Test-first** | npm run business:validate green on corpus. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Corpus gate. |
| **Acceptance** | Corpus gate. |
| **Evidence** | package scripts / business |

### [x] T-22-04 — Machine-readable validation errors
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-22-06 |
| **Maps to** | FR-22-06 |
| **Deliverable (code paths)** | `backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| **Test-first** | Error list structured. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | FE/tests can parse. |
| **Acceptance** | FE/tests can parse. |
| **Evidence** | validators output |

### [x] T-22-05 — Rejection → lesson without prod mutation
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-22-03, FR-22-05 |
| **Maps to** | FR-22-05, AC-22-04 |
| **Deliverable (code paths)** | `backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py` |
| **Test-first** | Reject records lesson option. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Learning from failures. |
| **Acceptance** | Learning from failures. |
| **Evidence** | runtime rejection path |

### [x] T-22-06 — No client bypass force flags
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-22-02, NFR-22-02 |
| **Maps to** | NFR-22-02 |
| **Deliverable (code paths)** | `backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| **Test-first** | Force activate ignored. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Hard gate. |
| **Acceptance** | Hard gate. |
| **Evidence** | activate API |

### [x] T-22-07 — Exit review — DNA safety complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-22-01, AC-22-02, AC-22-03, AC-22-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-22-08 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-22-01, D-22-02, D-22-03 |
| **Maps to** | FR-22-01, FR-22-02, NFR-22-01, AC-22-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-22-09 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-22-01, AC-22-02, AC-22-03, AC-22-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-22-10 — Exit review — BE-22 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-22-01, FR-22-02, FR-22-03, FR-22-04, FR-22-05, FR-22-06, FR-22-07, NFR-22-01, NFR-22-02, AC-22-01, AC-22-02, AC-22-03, AC-22-04 |
| **Deliverable (code paths)** | `planning/backend/22_production-dna-safety/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/22_production-dna-safety/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-22-01` | FR-22-01, FR-22-02, NFR-22-01, AC-22-02, AC-22-03 | `backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| `T-22-02` | FR-22-04, FR-22-07, AC-22-01 | `backend/app/runtime.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json`<br>… +5 more |
| `T-22-03` | FR-22-03 | `package scripts / business`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>… +1 more |
| `T-22-04` | FR-22-06 | `backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| `T-22-05` | FR-22-05, AC-22-04 | `backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json`<br>… +5 more |
| `T-22-06` | NFR-22-02 | `backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>`package.json` |
| `T-22-07` | AC-22-01, AC-22-02, AC-22-03, AC-22-04 | `tasks.md`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>… +1 more |
| `T-22-08` | FR-22-01, FR-22-02, NFR-22-01, AC-22-01 | `backend/app`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>… +1 more |
| `T-22-09` | AC-22-01, AC-22-02, AC-22-03, AC-22-04 | `backend/app/tests`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative`<br>… +1 more |
| `T-22-10` | FR-22-01, FR-22-02, FR-22-03, FR-22-04, FR-22-05, FR-22-06, FR-22-07, NFR-22-01,… | `planning/backend/22_production-dna-safety/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>… +2 more |

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
