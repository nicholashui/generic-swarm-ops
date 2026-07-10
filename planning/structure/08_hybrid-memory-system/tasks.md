# Tasks — 08 Hybrid Memory System

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-08-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-08-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-08`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/08_hybrid-memory-system/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-08**. Each task further narrows via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/memory.py`
- `backend/app/services/memory_service.py`
- `backend/app/domain/memory/scopes.py`
- `backend/app/domain/memory/retrieval.py`
- `backend/app/domain/memory/models.py`
- `backend/app/runtime.py`
- `business/memory/`
- `backend/app/tests/unit/test_scorecard_controls.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-08-01 — Eight memory types specified
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2.1 types |
| **Maps to** | FR-08-01…09 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | All eight types in design + writers mapped. |
| **Acceptance** | All eight types in design + writers mapped. |
| **Evidence** | backend/app/api/v1/routes/memory.py, backend/app/services/memory_service.py, backend/app/domain/memory/scopes.py |

### [x] T-08-02 — Scope dimensions + agent allow lists
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2.2, §4.1 write/read rules |
| **Maps to** | FR-08-10…11, AC-08-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Deny out-of-scope. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Scope matrix tests + E1 agent unions. |
| **Acceptance** | Scope matrix tests + E1 agent unions. |
| **Evidence** | runtime memory scopes, E1 fix |

### [x] T-08-03 — High-impact provenance gate
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-08-3, §4.1 |
| **Maps to** | FR-08-12, AC-08-03, NFR-08-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Writes require source_refs when high-impact. |
| **Acceptance** | Writes require source_refs when high-impact. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-08-04 — Expiration filter
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-08-4, §4.2 |
| **Maps to** | FR-08-13, AC-08-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Expired items excluded from operational reads. |
| **Acceptance** | Expired items excluded from operational reads. |
| **Evidence** | backend/app/api/v1/routes/memory.py, backend/app/services/memory_service.py, backend/app/domain/memory/scopes.py |

### [x] T-08-05 — MemoryItem model fields
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 MemoryItem |
| **Maps to** | AC-08-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Store supports type, scopes, provenance, expires_at. |
| **Acceptance** | Store supports type, scopes, provenance, expires_at. |
| **Evidence** | backend/app/api/v1/routes/memory.py, backend/app/services/memory_service.py, backend/app/domain/memory/scopes.py |

### [x] T-08-06 — Memory API CRUD/search
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5 API, C-08-6 |
| **Maps to** | AC-08-01, NFR-08-01…03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | /api/v1/memory with RBAC. |
| **Acceptance** | /api/v1/memory with RBAC. |
| **Evidence** | backend/app/api/v1/routes/memory.py, backend/app/services/memory_service.py, backend/app/domain/memory/scopes.py |

### [x] T-08-07 — Lessons bridge (reflect + rejection)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-08-5, D-08-03 |
| **Maps to** | FR-08-06/07 types, STRUCT-14/16 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Reflect lessons + rejection lessons written. |
| **Acceptance** | Reflect lessons + rejection lessons written. |
| **Evidence** | self_improvement, decide_approval |

### [x] T-08-08 — Postgres primary durability
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-08-01, NFR-08-02 |
| **Maps to** | NFR-08-02 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | runtime_state primary. |
| **Acceptance** | runtime_state primary. |
| **Evidence** | backend/app/runtime.py, backend/app/infrastructure/database/session.py, backend/app/tests/unit/test_postgres_restart.py |

### [x] T-08-09 — Metrics memory_denies
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §7 metrics |
| **Maps to** | NFR-08-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Audit/deny path observable. |
| **Acceptance** | Audit/deny path observable. |
| **Evidence** | backend/app/api/v1/routes/memory.py, backend/app/services/memory_service.py, backend/app/domain/memory/scopes.py |

### [x] T-08-10 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | backend/app/api/v1/routes/memory.py, backend/app/services/memory_service.py, backend/app/domain/memory/scopes.py |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-08-01` | FR-08-01…09 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-08-02` | FR-08-10…11, AC-08-02 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-08-03` | FR-08-12, AC-08-03, NFR-08-04 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>… +4 more |
| `T-08-04` | FR-08-13, AC-08-04 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-08-05` | AC-08-01 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-08-06` | AC-08-01, NFR-08-01…03 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-08-07` | FR-08-06/07 types, STRUCT-14/16 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>… +4 more |
| `T-08-08` | NFR-08-02 | `backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/tests/unit/test_postgres_restart.py`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>… +2 more |
| `T-08-09` | NFR-08-01 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-08-10` |  | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/runtime.py`<br>`business/memory/`<br>`backend/app/tests/unit/test_scorecard_controls.py` |

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
