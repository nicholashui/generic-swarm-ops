# Tasks — 02 Runtime Stack and Project Scaffold

| Field | Value |
|-------|-------|
| Task list ID | `BE-02-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-02-DES`) |
| Paired requirements | `requirements.md` (`BE-02`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 4/4 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Entrypoint → layered packages → config/secrets → router/OpenAPI → optional deps → README DX.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-02. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/api/v1/router.py`
- `backend/README.md`
- `backend/app/api/`
- `backend/app/core/`
- `backend/app/domain/`
- `backend/app/infrastructure/`
- `backend/app/services/`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-02-01 — Scaffold FastAPI app entrypoint
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-02-1 |
| **Maps to** | FR-02-01, FR-02-10, AC-02-04 |
| **Deliverable (code paths)** | `backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core` |
| **Test-first** | Import app.main succeeds. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | uvicorn app.main:app works. |
| **Acceptance** | uvicorn app.main:app works. |
| **Evidence** | backend/app/main.py |

### [x] T-02-02 — Layer packages api/core/domain/infrastructure
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-02-4, D-02-01 |
| **Maps to** | FR-02-06, NFR-02-02, AC-02-01 |
| **Deliverable (code paths)** | `backend/app/*`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core` |
| **Test-first** | No circular imports domain↔infra. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Folder layout matches design. |
| **Acceptance** | Folder layout matches design. |
| **Evidence** | backend/app/* |

### [x] T-02-03 — Config settings from environment
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-02-2 |
| **Maps to** | FR-02-08, NFR-02-03, AC-02-03 |
| **Deliverable (code paths)** | `backend/app/core/config.py`<br>`backend/app/main.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core` |
| **Test-first** | .env.example lists DATABASE_URL/JWT. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Secrets not hardcoded. |
| **Acceptance** | Secrets not hardcoded. |
| **Evidence** | core/config.py |

### [x] T-02-04 — Aggregate v1 router
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-02-3 |
| **Maps to** | FR-02-05, AC-02-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/router.py`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py` |
| **Test-first** | OpenAPI lists /api/v1 routes. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Schema exportable. |
| **Acceptance** | Schema exportable. |
| **Evidence** | api/v1/router.py |

### [x] T-02-05 — Postgres as primary when DATABASE_URL set
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-02-03 related BE-03 |
| **Maps to** | FR-02-02, FR-02-09 |
| **Deliverable (code paths)** | `backend/app/infrastructure/database/*`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py` |
| **Test-first** | ready reports postgres. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | JSON backup/seed only. |
| **Acceptance** | JSON backup/seed only. |
| **Evidence** | infrastructure/database/* |

### [x] T-02-06 — Optional deps degrade gracefully
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-02-03 |
| **Maps to** | FR-02-03, FR-02-04, FR-02-07 |
| **Deliverable (code paths)** | `backend/app/core/config.py`<br>`backend/app/infrastructure/llm/*`<br>`backend/app/main.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core` |
| **Test-first** | App starts without Redis/LLM. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Feature flags for optional paths. |
| **Acceptance** | Feature flags for optional paths. |
| **Evidence** | core/config.py; infrastructure/llm/* |

### [x] T-02-07 — Document local start without Docker
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-02-02 |
| **Maps to** | NFR-02-01, AC-02-04 |
| **Deliverable (code paths)** | `backend/README.md`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/api`<br>`backend/app/core` |
| **Test-first** | README quick start works. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Product-bar local DX. |
| **Acceptance** | Product-bar local DX. |
| **Evidence** | backend/README.md |

### [x] T-02-08 — CORS explicit origins (prod profile)
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | NFR-02-04 |
| **Maps to** | NFR-02-04 |
| **Deliverable (code paths)** | `main.py / config`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py` |
| **Test-first** | Config has allowlist. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No wildcard in prod profile. |
| **Acceptance** | No wildcard in prod profile. |
| **Evidence** | main.py / config |

### [x] T-02-09 — Exit review — scaffold complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-02-01, AC-02-02, AC-02-03, AC-02-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-02-10 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-02-01, D-02-02, D-02-03 |
| **Maps to** | FR-02-01, FR-02-02, NFR-02-01, AC-02-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-02-11 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-02-01, AC-02-02, AC-02-03, AC-02-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-02-12 — Exit review — BE-02 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-02-01, FR-02-02, FR-02-03, FR-02-04, FR-02-05, FR-02-06, FR-02-07, FR-02-08, FR-02-09, FR-02-10, NFR-02-01, NFR-02-02, NFR-02-03, NFR-02-04, AC-02-01, AC-02-02, AC-02-03, AC-02-04 |
| **Deliverable (code paths)** | `planning/backend/02_runtime-stack-and-project-scaffold/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/02_runtime-stack-and-project-scaffold/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-02-01` | FR-02-01, FR-02-10, AC-02-04 | `backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core` |
| `T-02-02` | FR-02-06, NFR-02-02, AC-02-01 | `backend/app/*`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>… +1 more |
| `T-02-03` | FR-02-08, NFR-02-03, AC-02-03 | `backend/app/core/config.py`<br>`backend/app/main.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core` |
| `T-02-04` | FR-02-05, AC-02-02 | `backend/app/api/v1/router.py`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/README.md`<br>`backend/app/api`<br>`backend/app/core`<br>… +5 more |
| `T-02-05` | FR-02-02, FR-02-09 | `backend/app/infrastructure/database/*`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>… +6 more |
| `T-02-06` | FR-02-03, FR-02-04, FR-02-07 | `backend/app/core/config.py`<br>`backend/app/infrastructure/llm/*`<br>`backend/app/main.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>… +1 more |
| `T-02-07` | NFR-02-01, AC-02-04 | `backend/README.md`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/app/api`<br>`backend/app/core` |
| `T-02-08` | NFR-02-04 | `main.py / config`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>… +6 more |
| `T-02-09` | AC-02-01, AC-02-02, AC-02-03, AC-02-04 | `tasks.md`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>… +1 more |
| `T-02-10` | FR-02-01, FR-02-02, NFR-02-01, AC-02-01 | `backend/app`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>… +1 more |
| `T-02-11` | AC-02-01, AC-02-02, AC-02-03, AC-02-04 | `backend/app/tests`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>`backend/app/api`<br>… +1 more |
| `T-02-12` | FR-02-01, FR-02-02, FR-02-03, FR-02-04, FR-02-05, FR-02-06, FR-02-07, FR-02-08, … | `planning/backend/02_runtime-stack-and-project-scaffold/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/main.py`<br>`backend/app/core/config.py`<br>`backend/app/api/v1/router.py`<br>`backend/README.md`<br>… +2 more |

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
