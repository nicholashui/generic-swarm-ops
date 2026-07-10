# Tasks — 14 Audit Logging

| Field | Value |
|-------|-------|
| Task list ID | `BE-14-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-14-DES`) |
| Paired requirements | `requirements.md` (`BE-14`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 7/7 · NFR 4/4 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Event model → writers on mutations → read-only APIs → redaction → search filters.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-14. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/audit_logs.py`
- `backend/app/services/audit_service.py`
- `backend/app/domain/audit/events.py`
- `backend/app/domain/audit/models.py`
- `backend/app/schemas/audit_logs.py`
- `backend/app/infrastructure/repositories/audit_repository.py`
- `backend/app/runtime.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-14-01 — Audit event model + fields
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-14-3, §4 |
| **Maps to** | FR-14-02 |
| **Deliverable (code paths)** | `backend/app/domain/audit/models.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | Schema includes request_id/actor. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Rich forensics. |
| **Acceptance** | Rich forensics. |
| **Evidence** | domain/audit/models.py |

### [x] T-14-02 — Write audits for important actions list
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-14-2, D-14-02 |
| **Maps to** | FR-14-01, FR-14-05, AC-14-01, AC-14-02 |
| **Deliverable (code paths)** | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | Run start + approval create events. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Coverage complete. |
| **Acceptance** | Coverage complete. |
| **Evidence** | domain/audit/events.py |

### [x] T-14-03 — Append-only via API (no client mutate)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-14-01, FR-14-03 |
| **Maps to** | FR-14-03, FR-14-06, AC-14-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | No PATCH/DELETE audit. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Integrity. |
| **Acceptance** | Integrity. |
| **Evidence** | api/v1/routes/audit_logs.py |

### [x] T-14-04 — List/search + get with audit:read
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-14-1 |
| **Maps to** | FR-14-04, NFR-14-03, AC-14-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | Viewer without perm denied. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Controlled access. |
| **Acceptance** | Controlled access. |
| **Evidence** | audit_logs routes |

### [x] T-14-05 — Redact secrets from audit metadata
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-14-07, NFR-14-04 |
| **Maps to** | FR-14-07, NFR-14-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | Review sample events. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No tokens/passwords stored. |
| **Acceptance** | No tokens/passwords stored. |
| **Evidence** | event writer |

### [x] T-14-06 — Filterable search (time/actor/action)
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | NFR-14-02 |
| **Maps to** | NFR-14-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | Query params work. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Investigator UX. |
| **Acceptance** | Investigator UX. |
| **Evidence** | audit routes |

### [x] T-14-07 — Write overhead acceptable
| | |
|--|--|
| **Priority** | P2 |
| **Status** | [x] Implemented |
| **Design** | NFR-14-01 |
| **Maps to** | NFR-14-01 |
| **Deliverable (code paths)** | `perf notes/tests`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | No major latency regression. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | On critical path ok. |
| **Acceptance** | On critical path ok. |
| **Evidence** | perf notes/tests |

### [x] T-14-08 — Exit review — audit complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-14-01, AC-14-02, AC-14-03, AC-14-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-14-09 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-14-01, D-14-02 |
| **Maps to** | FR-14-01, FR-14-02, NFR-14-01, AC-14-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-14-10 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-14-01, AC-14-02, AC-14-03, AC-14-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-14-11 — Exit review — BE-14 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-14-01, FR-14-02, FR-14-03, FR-14-04, FR-14-05, FR-14-06, FR-14-07, NFR-14-01, NFR-14-02, NFR-14-03, NFR-14-04, AC-14-01, AC-14-02, AC-14-03, AC-14-04 |
| **Deliverable (code paths)** | `planning/backend/14_audit-logging/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/14_audit-logging/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-14-01` | FR-14-02 | `backend/app/domain/audit/models.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| `T-14-02` | FR-14-01, FR-14-05, AC-14-01, AC-14-02 | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| `T-14-03` | FR-14-03, FR-14-06, AC-14-03 | `backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| `T-14-04` | FR-14-04, NFR-14-03, AC-14-04 | `backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| `T-14-05` | FR-14-07, NFR-14-04 | `backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| `T-14-06` | NFR-14-02 | `backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>`backend/app/infrastructure/repositories/audit_repository.py` |
| `T-14-07` | NFR-14-01 | `perf notes/tests`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>… +1 more |
| `T-14-08` | AC-14-01, AC-14-02, AC-14-03, AC-14-04 | `tasks.md`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>… +1 more |
| `T-14-09` | FR-14-01, FR-14-02, NFR-14-01, AC-14-01 | `backend/app`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>… +1 more |
| `T-14-10` | AC-14-01, AC-14-02, AC-14-03, AC-14-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py`<br>… +1 more |
| `T-14-11` | FR-14-01, FR-14-02, FR-14-03, FR-14-04, FR-14-05, FR-14-06, FR-14-07, NFR-14-01,… | `planning/backend/14_audit-logging/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>… +2 more |

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
