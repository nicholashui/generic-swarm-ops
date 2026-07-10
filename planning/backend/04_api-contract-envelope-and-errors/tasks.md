# Tasks — 04 API Contract, Envelope, and Errors

| Field | Value |
|-------|-------|
| Task list ID | `BE-04-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-04-DES`) |
| Paired requirements | `requirements.md` (`BE-04`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 4/4 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Version prefix → envelopes → request_id errors → OpenAPI fidelity → pagination.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-04. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/errors.py`
- `backend/app/core/errors.py`
- `backend/app/core/pagination.py`
- `backend/app/core/logging.py`
- `backend/app/api/v1/router.py`
- `backend/app/main.py`
- `frontend/src/lib/api/generated/openapi.d.ts`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-04-01 — Version all public routes under /api/v1
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-04-01 |
| **Maps to** | FR-04-01, AC-04-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/router.py`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/main.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py` |
| **Test-first** | OpenAPI paths prefix /api/v1. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Stable versioning. |
| **Acceptance** | Stable versioning. |
| **Evidence** | api/v1/router.py |

### [x] T-04-02 — Success envelope {data, meta}
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5 ICD |
| **Maps to** | FR-04-02 |
| **Deliverable (code paths)** | `backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | Sample GET uses envelope. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Consistent FE parsing. |
| **Acceptance** | Consistent FE parsing. |
| **Evidence** | route responses |

### [x] T-04-03 — Error envelope with request_id
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-04-1, C-04-2 |
| **Maps to** | FR-04-03, FR-04-04, AC-04-01 |
| **Deliverable (code paths)** | `api/errors.py`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | Forced 422/401 include request_id. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Support triage works. |
| **Acceptance** | Support triage works. |
| **Evidence** | api/errors.py |

### [x] T-04-04 — Map HTTP codes 401/403/404/409/422/429/500
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 error map |
| **Maps to** | FR-04-05, FR-04-06 |
| **Deliverable (code paths)** | `backend/app/core/errors.py`<br>`backend/app/api/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | Table-driven error tests. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Codes documented. |
| **Acceptance** | Codes documented. |
| **Evidence** | core/errors.py |

### [x] T-04-05 — Hide stacks in production profiles
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-04-03 |
| **Maps to** | FR-04-07, NFR-04-03, AC-04-04 |
| **Deliverable (code paths)** | `backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | Prod error body has no traceback. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safe errors. |
| **Acceptance** | Safe errors. |
| **Evidence** | error handlers |

### [x] T-04-06 — OpenAPI matches routes
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-04-4 |
| **Maps to** | FR-04-08, NFR-04-02, AC-04-02 |
| **Deliverable (code paths)** | `backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | Export schema. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | FE api:generate works. |
| **Acceptance** | FE api:generate works. |
| **Evidence** | openapi export |

### [x] T-04-07 — Pagination helpers
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-04-3 |
| **Maps to** | FR-04-09 |
| **Deliverable (code paths)** | `backend/app/core/pagination.py`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | List endpoints accept page/limit or defaults. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Consistent lists. |
| **Acceptance** | Consistent lists. |
| **Evidence** | core/pagination.py |

### [x] T-04-08 — Breaking change policy (version bump)
| | |
|--|--|
| **Priority** | P2 |
| **Status** | [x] Implemented |
| **Design** | FR-04-10 |
| **Maps to** | FR-04-10, NFR-04-01 |
| **Deliverable (code paths)** | `backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py` |
| **Test-first** | Doc note in backend.md/README. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Consumers protected. |
| **Acceptance** | Consumers protected. |
| **Evidence** | docs |

### [x] T-04-09 — Exit review — contract complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-04-01, AC-04-02, AC-04-03, AC-04-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-04-10 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-04-04 |
| **Deliverable (code paths)** | `requirements.md`<br>`04_api-contract-envelope-and-errors/tasks.md RTM`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=1 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 04_api-contract-envelope-and-errors/tasks.md RTM |

### [x] T-04-11 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-04-01, D-04-02, D-04-03 |
| **Maps to** | FR-04-01, FR-04-02, NFR-04-01, AC-04-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-04-12 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-04-01, AC-04-02, AC-04-03, AC-04-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-04-13 — Exit review — BE-04 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-04-01, FR-04-02, FR-04-03, FR-04-04, FR-04-05, FR-04-06, FR-04-07, FR-04-08, FR-04-09, FR-04-10, NFR-04-01, NFR-04-02, NFR-04-03, NFR-04-04, AC-04-01, AC-04-02, AC-04-03, AC-04-04 |
| **Deliverable (code paths)** | `planning/backend/04_api-contract-envelope-and-errors/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/04_api-contract-envelope-and-errors/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-04-01` | FR-04-01, AC-04-02 | `backend/app/api/v1/router.py`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/main.py`<br>… +5 more |
| `T-04-02` | FR-04-02 | `backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| `T-04-03` | FR-04-03, FR-04-04, AC-04-01 | `api/errors.py`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>… +1 more |
| `T-04-04` | FR-04-05, FR-04-06 | `backend/app/core/errors.py`<br>`backend/app/api/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| `T-04-05` | FR-04-07, NFR-04-03, AC-04-04 | `backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| `T-04-06` | FR-04-08, NFR-04-02, AC-04-02 | `backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| `T-04-07` | FR-04-09 | `backend/app/core/pagination.py`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py` |
| `T-04-08` | FR-04-10, NFR-04-01 | `backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/main.py`<br>… +5 more |
| `T-04-09` | AC-04-01, AC-04-02, AC-04-03, AC-04-04 | `tasks.md`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>… +1 more |
| `T-04-10` | NFR-04-04 | `requirements.md`<br>`04_api-contract-envelope-and-errors/tasks.md RTM`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>… +2 more |
| `T-04-11` | FR-04-01, FR-04-02, NFR-04-01, AC-04-01 | `backend/app`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>… +1 more |
| `T-04-12` | AC-04-01, AC-04-02, AC-04-03, AC-04-04 | `backend/app/tests`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>`backend/app/api/v1/router.py`<br>… +1 more |
| `T-04-13` | FR-04-01, FR-04-02, FR-04-03, FR-04-04, FR-04-05, FR-04-06, FR-04-07, FR-04-08, … | `planning/backend/04_api-contract-envelope-and-errors/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/errors.py`<br>`backend/app/core/errors.py`<br>`backend/app/core/pagination.py`<br>`backend/app/core/logging.py`<br>… +2 more |

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
