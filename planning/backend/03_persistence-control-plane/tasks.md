# Tasks — 03 Persistence Control Plane

| Field | Value |
|-------|-------|
| Task list ID | `BE-03-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-03-DES`) |
| Paired requirements | `requirements.md` (`BE-03`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 4/4 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

DB session → repositories/store → seed/backup rules → org isolation → ready probe.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-03. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/runtime.py`
- `backend/app/infrastructure/database/session.py`
- `backend/app/infrastructure/database/models.py`
- `backend/app/infrastructure/repositories/`
- `backend/app/tests/unit/test_postgres_restart.py`
- `docs/postgres-runbook.md`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-03-01 — Postgres session + models bootstrap
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-03-1, C-03-2 |
| **Maps to** | FR-03-01, FR-03-02, AC-03-01 |
| **Deliverable (code paths)** | `backend/app/infrastructure/database/*`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| **Test-first** | Connect with DATABASE_URL. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | runtime_state durable. |
| **Acceptance** | runtime_state durable. |
| **Evidence** | infrastructure/database/* |

### [x] T-03-02 — RuntimeStore / repositories for entities
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-03-3, C-03-4 |
| **Maps to** | FR-03-05, FR-03-07 |
| **Deliverable (code paths)** | `repositories/*`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| **Test-first** | Create entity; read back. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | CRUD persists across restart. |
| **Acceptance** | CRUD persists across restart. |
| **Evidence** | repositories/*; runtime.py |

### [x] T-03-03 — Migrate-from-JSON on empty DB
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-03-03 |
| **Maps to** | FR-03-03, FR-03-04, AC-03-03 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| **Test-first** | Empty DB seed path. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | JSON not live authority. |
| **Acceptance** | JSON not live authority. |
| **Evidence** | runtime seed logic |

### [x] T-03-04 — organization_id on tenant entities
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 entities |
| **Maps to** | FR-03-06, FR-03-10, AC-03-04 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py` |
| **Test-first** | Entity schema includes org_id. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Queries filter by org. |
| **Acceptance** | Queries filter by org. |
| **Evidence** | domain models |

### [x] T-03-05 — Snapshot backup path
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-03-03 |
| **Maps to** | FR-03-09 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| **Test-first** | Export snapshot file. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Portable backup. |
| **Acceptance** | Portable backup. |
| **Evidence** | runtime backup |

### [x] T-03-06 — Ready fails when DB unavailable
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §6 failures |
| **Maps to** | FR-03-08, AC-03-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/health.py`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md`<br>`backend/app/api/v1/routes/workflow_runs.py`<br>`backend/app/core/logging.py`<br>`backend/app/core/metrics.py`<br>`backend/app/main.py` |
| **Test-first** | Stop DB → ready not ok. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Probe accurate. |
| **Acceptance** | Probe accurate. |
| **Evidence** | api/v1/routes/health.py |

### [x] T-03-07 — SQL injection / bound params
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-03-04 |
| **Maps to** | NFR-03-03, NFR-03-04 |
| **Deliverable (code paths)** | `session/repositories`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py` |
| **Test-first** | ORM/bindings only. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No string-built SQL. |
| **Acceptance** | No string-built SQL. |
| **Evidence** | session/repositories |

### [x] T-03-08 — PK lookup performance baseline
| | |
|--|--|
| **Priority** | P2 |
| **Status** | [x] Implemented |
| **Design** | NFR-03-01 |
| **Maps to** | NFR-03-01 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| **Test-first** | Local get-by-id latency check. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | p95 target documented. |
| **Acceptance** | p95 target documented. |
| **Evidence** | tests or notes |

### [x] T-03-09 — Exit review — persistence complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-03-01, AC-03-02, AC-03-03, AC-03-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-03-10 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-03-02 |
| **Deliverable (code paths)** | `requirements.md`<br>`03_persistence-control-plane/tasks.md RTM`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=1 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 03_persistence-control-plane/tasks.md RTM |

### [x] T-03-11 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-03-01, D-03-02, D-03-03 |
| **Maps to** | FR-03-01, FR-03-02, NFR-03-01, AC-03-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-03-12 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-03-01, AC-03-02, AC-03-03, AC-03-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-03-13 — Exit review — BE-03 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-03-01, FR-03-02, FR-03-03, FR-03-04, FR-03-05, FR-03-06, FR-03-07, FR-03-08, FR-03-09, FR-03-10, NFR-03-01, NFR-03-02, NFR-03-03, NFR-03-04, AC-03-01, AC-03-02, AC-03-03, AC-03-04 |
| **Deliverable (code paths)** | `planning/backend/03_persistence-control-plane/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/03_persistence-control-plane/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-03-01` | FR-03-01, FR-03-02, AC-03-01 | `backend/app/infrastructure/database/*`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>… +1 more |
| `T-03-02` | FR-03-05, FR-03-07 | `repositories/*`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>… +1 more |
| `T-03-03` | FR-03-03, FR-03-04, AC-03-03 | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| `T-03-04` | FR-03-06, FR-03-10, AC-03-04 | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md`<br>… +5 more |
| `T-03-05` | FR-03-09 | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| `T-03-06` | FR-03-08, AC-03-01 | `backend/app/api/v1/routes/health.py`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>… +5 more |
| `T-03-07` | NFR-03-03, NFR-03-04 | `session/repositories`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>… +6 more |
| `T-03-08` | NFR-03-01 | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`docs/postgres-runbook.md` |
| `T-03-09` | AC-03-01, AC-03-02, AC-03-03, AC-03-04 | `tasks.md`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>… +1 more |
| `T-03-10` | NFR-03-02 | `requirements.md`<br>`03_persistence-control-plane/tasks.md RTM`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>… +2 more |
| `T-03-11` | FR-03-01, FR-03-02, NFR-03-01, AC-03-01 | `backend/app`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>… +1 more |
| `T-03-12` | AC-03-01, AC-03-02, AC-03-03, AC-03-04 | `backend/app/tests`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>… +1 more |
| `T-03-13` | FR-03-01, FR-03-02, FR-03-03, FR-03-04, FR-03-05, FR-03-06, FR-03-07, FR-03-08, … | `planning/backend/03_persistence-control-plane/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>… +2 more |

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
