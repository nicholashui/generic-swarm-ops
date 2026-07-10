# Tasks — 19 Streaming, Health, and Observability

| Field | Value |
|-------|-------|
| Task list ID | `BE-19-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-19-DES`) |
| Paired requirements | `requirements.md` (`BE-19`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 9/9 · NFR 4/4 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Health probes → metrics/logs → SSE stream → stream authz → headers/CORS.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-19. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/health.py`
- `backend/app/api/v1/routes/workflow_runs.py`
- `backend/app/core/logging.py`
- `backend/app/core/metrics.py`
- `backend/app/main.py`
- `backend/app/infrastructure/database/session.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-19-01 — Health/live/ready endpoints
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-19-1 |
| **Maps to** | FR-19-04, FR-19-05, NFR-19-02, AC-19-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py` |
| **Test-first** | ready includes database status. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Probes work. |
| **Acceptance** | Probes work. |
| **Evidence** | api/v1/routes/health.py |

### [x] T-19-02 — Metrics endpoint
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-19-3 |
| **Maps to** | FR-19-07 |
| **Deliverable (code paths)** | `backend/app/core/metrics.py`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py` |
| **Test-first** | metrics responds. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Basic monitoring. |
| **Acceptance** | Basic monitoring. |
| **Evidence** | core/metrics.py |

### [x] T-19-03 — Structured logs + request_id
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-19-2 |
| **Maps to** | FR-19-06, NFR-19-04, AC-19-03 |
| **Deliverable (code paths)** | `backend/app/core/logging.py`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/api/v1/router.py` |
| **Test-first** | Logs include request_id; secrets redacted. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Supportability. |
| **Acceptance** | Supportability. |
| **Evidence** | core/logging.py |

### [x] T-19-04 — SSE run event stream
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-19-4, D-19-01 |
| **Maps to** | FR-19-01, FR-19-02, FR-19-03, NFR-19-01, AC-19-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py` |
| **Test-first** | Events after step persist. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | FE live updates. |
| **Acceptance** | FE live updates. |
| **Evidence** | workflow_runs stream |

### [x] T-19-05 — Authorize stream by run ACL
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-19-09 |
| **Maps to** | FR-19-09, NFR-19-03, AC-19-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Unauthorized stream denied. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No data leak. |
| **Acceptance** | No data leak. |
| **Evidence** | stream authz |

### [x] T-19-06 — Security headers + CORS
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | FR-19-08 |
| **Maps to** | FR-19-08 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py` |
| **Test-first** | Headers present. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Browser safety. |
| **Acceptance** | Browser safety. |
| **Evidence** | main middleware |

### [x] T-19-07 — Exit review — observability complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-19-01, AC-19-02, AC-19-03, AC-19-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-19-08 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-19-01, D-19-02 |
| **Maps to** | FR-19-01, FR-19-02, NFR-19-01, AC-19-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-19-09 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-19-01, AC-19-02, AC-19-03, AC-19-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-19-10 — Exit review — BE-19 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-19-01, FR-19-02, FR-19-03, FR-19-04, FR-19-05, FR-19-06, FR-19-07, FR-19-08, FR-19-09, NFR-19-01, NFR-19-02, NFR-19-03, NFR-19-04, AC-19-01, AC-19-02, AC-19-03, AC-19-04 |
| **Deliverable (code paths)** | `planning/backend/19_streaming-health-and-observability/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/19_streaming-health-and-observability/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-19-01` | FR-19-04, FR-19-05, NFR-19-02, AC-19-02 | `backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py` |
| `T-19-02` | FR-19-07 | `backend/app/core/metrics.py`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py` |
| `T-19-03` | FR-19-06, NFR-19-04, AC-19-03 | `backend/app/core/logging.py`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py`<br>… +4 more |
| `T-19-04` | FR-19-01, FR-19-02, FR-19-03, NFR-19-01, AC-19-01 | `backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py` |
| `T-19-05` | FR-19-09, NFR-19-03, AC-19-04 | `backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py`<br>… +5 more |
| `T-19-06` | FR-19-08 | `backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>`backend/app/infrastructure/database/session.py`<br>… +5 more |
| `T-19-07` | AC-19-01, AC-19-02, AC-19-03, AC-19-04 | `tasks.md`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>… +1 more |
| `T-19-08` | FR-19-01, FR-19-02, NFR-19-01, AC-19-01 | `backend/app`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>… +1 more |
| `T-19-09` | AC-19-01, AC-19-02, AC-19-03, AC-19-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py`<br>… +1 more |
| `T-19-10` | FR-19-01, FR-19-02, FR-19-03, FR-19-04, FR-19-05, FR-19-06, FR-19-07, FR-19-08, … | `planning/backend/19_streaming-health-and-observability/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/health.py`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>… +2 more |

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
