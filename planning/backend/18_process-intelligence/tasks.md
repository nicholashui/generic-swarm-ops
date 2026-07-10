# Tasks — 18 Process Intelligence

| Field | Value |
|-------|-------|
| Task list ID | `BE-18-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-18-DES`) |
| Paired requirements | `requirements.md` (`BE-18`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 6/6 · NFR 2/2 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Analytics APIs → disk artifacts → no DNA mutation → authz → performance baseline.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-18. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/processes.py`
- `backend/app/services/process_service.py`
- `backend/app/domain/processes/analytics.py`
- `backend/app/infrastructure/process_intelligence/artifacts.py`
- `backend/app/schemas/processes.py`
- `business/process-intelligence/`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-18-01 — Process metrics APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-18-1, C-18-2 |
| **Maps to** | FR-18-01, FR-18-02, FR-18-04, AC-18-01, AC-18-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py` |
| **Test-first** | metrics/bottlenecks/failures respond. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Ops analytics surface. |
| **Acceptance** | Ops analytics surface. |
| **Evidence** | api/v1/routes/processes.py |

### [x] T-18-02 — PI disk artifacts writer
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-18-3, D-18-01 |
| **Maps to** | FR-18-03, AC-18-03 |
| **Deliverable (code paths)** | `backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence` |
| **Test-first** | Artifact path receives output. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | business/process-intelligence/* used. |
| **Acceptance** | business/process-intelligence/* used. |
| **Evidence** | infrastructure/process_intelligence/artifacts.py |

### [x] T-18-03 — PI cannot mutate production DNA
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-18-02, FR-18-05 |
| **Maps to** | FR-18-05 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/runtime.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative` |
| **Test-first** | Code review/path test. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Read-only improvements signals. |
| **Acceptance** | Read-only improvements signals. |
| **Evidence** | PI services |

### [x] T-18-04 — Authorize PI summaries
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-18-06 |
| **Maps to** | FR-18-06, NFR-18-02, AC-18-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Unauthorized denied. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Org isolation. |
| **Acceptance** | Org isolation. |
| **Evidence** | processes routes |

### [x] T-18-05 — Aggregate performance baseline
| | |
|--|--|
| **Priority** | P2 |
| **Status** | [x] Implemented |
| **Design** | NFR-18-01 |
| **Maps to** | NFR-18-01 |
| **Deliverable (code paths)** | `analytics.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py` |
| **Test-first** | Small history under 1s local. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Usable dashboards. |
| **Acceptance** | Usable dashboards. |
| **Evidence** | analytics.py |

### [x] T-18-06 — Document commercial PM suite non-goal
| | |
|--|--|
| **Priority** | P3 |
| **Status** | [x] Implemented |
| **Design** | OI-18-01 |
| **Maps to** | scope_out |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md` |
| **Test-first** | Non-goal listed. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Scope control. |
| **Acceptance** | Scope control. |
| **Evidence** | design |

### [x] T-18-07 — Exit review — PI complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-18-01, AC-18-02, AC-18-03, AC-18-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-18-08 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-18-01, D-18-02 |
| **Maps to** | FR-18-01, FR-18-02, NFR-18-01, AC-18-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-18-09 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-18-01, AC-18-02, AC-18-03, AC-18-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-18-10 — Exit review — BE-18 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-18-01, FR-18-02, FR-18-03, FR-18-04, FR-18-05, FR-18-06, NFR-18-01, NFR-18-02, AC-18-01, AC-18-02, AC-18-03, AC-18-04 |
| **Deliverable (code paths)** | `planning/backend/18_process-intelligence/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/18_process-intelligence/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-18-01` | FR-18-01, FR-18-02, FR-18-04, AC-18-01, AC-18-02 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence`<br>… +5 more |
| `T-18-02` | FR-18-03, AC-18-03 | `backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence` |
| `T-18-03` | FR-18-05 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence`<br>… +5 more |
| `T-18-04` | FR-18-06, NFR-18-02, AC-18-04 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence`<br>… +5 more |
| `T-18-05` | NFR-18-01 | `analytics.py`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>… +6 more |
| `T-18-06` | scope_out | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>`business/process-intelligence`<br>… +5 more |
| `T-18-07` | AC-18-01, AC-18-02, AC-18-03, AC-18-04 | `tasks.md`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>… +1 more |
| `T-18-08` | FR-18-01, FR-18-02, NFR-18-01, AC-18-01 | `backend/app`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>… +1 more |
| `T-18-09` | AC-18-01, AC-18-02, AC-18-03, AC-18-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`backend/app/schemas/processes.py`<br>… +1 more |
| `T-18-10` | FR-18-01, FR-18-02, FR-18-03, FR-18-04, FR-18-05, FR-18-06, NFR-18-01, NFR-18-02… | `planning/backend/18_process-intelligence/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>… +2 more |

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
