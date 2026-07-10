# Tasks — 16 Memory System

| Field | Value |
|-------|-------|
| Task list ID | `BE-16-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-16-DES`) |
| Paired requirements | `requirements.md` (`BE-16`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 9/9 · NFR 3/3 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Memory CRUD → scopes → department policy → run memory_reads → audit sensitive ops.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-16. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/memory.py`
- `backend/app/services/memory_service.py`
- `backend/app/domain/memory/scopes.py`
- `backend/app/domain/memory/retrieval.py`
- `backend/app/domain/memory/models.py`
- `backend/app/schemas/memory.py`
- `backend/app/infrastructure/repositories/memory_repository.py`
- `backend/app/tests/unit/test_scorecard_controls.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-16-01 — Memory CRUD + search APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-16-1 |
| **Maps to** | FR-16-01, FR-16-05, AC-16-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | Create/get memory. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Ops can inspect. |
| **Acceptance** | Ops can inspect. |
| **Evidence** | api/v1/routes/memory.py |

### [x] T-16-02 — Multi-scope memory model
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-16-2, D-16-01, §4 |
| **Maps to** | FR-16-02, FR-16-03 |
| **Deliverable (code paths)** | `backend/app/domain/memory/scopes.py`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | Scopes persisted. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Hybrid memory structure. |
| **Acceptance** | Hybrid memory structure. |
| **Evidence** | domain/memory/scopes.py |

### [x] T-16-03 — Scope/department policy enforcement
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-16-02, C-16-3 |
| **Maps to** | FR-16-04, FR-16-06, AC-16-02, AC-16-03 |
| **Deliverable (code paths)** | `backend/app/domain/memory/*`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py` |
| **Test-first** | Restricted mismatch deny. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Isolation works. |
| **Acceptance** | Isolation works. |
| **Evidence** | domain/memory/* |

### [x] T-16-04 — Permissions memory:read/write
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-16-02 |
| **Maps to** | NFR-16-02, NFR-16-03, AC-16-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Unauthorized write 403. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | RBAC enforced. |
| **Acceptance** | RBAC enforced. |
| **Evidence** | dependencies |

### [x] T-16-05 — Audit sensitive memory access/update
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | FR-16-07 |
| **Maps to** | FR-16-07 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py` |
| **Test-first** | Sensitive op audited. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Forensics. |
| **Acceptance** | Forensics. |
| **Evidence** | audit hooks |

### [x] T-16-06 — Expiration handling
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | FR-16-08 |
| **Maps to** | FR-16-08 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | Expired not returned as active. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | TTL semantics. |
| **Acceptance** | TTL semantics. |
| **Evidence** | memory retrieval |

### [x] T-16-07 — High-impact write filtering/review hooks
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | FR-16-09 |
| **Maps to** | FR-16-09 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | Policy path exists. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Poisoning defense. |
| **Acceptance** | Poisoning defense. |
| **Evidence** | memory write path |

### [x] T-16-08 — Flagship memory_reads mid-run
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | TV-16-03 |
| **Maps to** | AC-16-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | E1/run does not fail scopes. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Agent scopes configured. |
| **Acceptance** | Agent scopes configured. |
| **Evidence** | seed agents + tests |

### [x] T-16-09 — Exit review — memory complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-16-01, AC-16-02, AC-16-03, AC-16-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-16-10 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-16-01 |
| **Deliverable (code paths)** | `requirements.md`<br>`16_memory-system/tasks.md RTM`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=1 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 16_memory-system/tasks.md RTM |

### [x] T-16-11 — Implement/verify all design components C-*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-16-4, C-16-1, C-16-2, C-16-3 |
| **Maps to** | AC-16-01, AC-16-02, AC-16-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | Component module import/smoke or route presence. |
| **Steps** | 1) Map each C-* to module path in design. 2) Verify module exists and is wired. 3) Add smoke test if missing. |
| **Success** | All design components have implementation anchors. |
| **Acceptance** | Components covered: C-16-1, C-16-2, C-16-3, C-16-4 |
| **Evidence** | ### 3.1 Components |

### [x] T-16-12 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-16-01, D-16-02 |
| **Maps to** | FR-16-01, FR-16-02, NFR-16-01, AC-16-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-16-13 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-16-01, AC-16-02, AC-16-03, AC-16-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-16-14 — Exit review — BE-16 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-16-01, FR-16-02, FR-16-03, FR-16-04, FR-16-05, FR-16-06, FR-16-07, FR-16-08, FR-16-09, NFR-16-01, NFR-16-02, NFR-16-03, AC-16-01, AC-16-02, AC-16-03, AC-16-04 |
| **Deliverable (code paths)** | `planning/backend/16_memory-system/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/16_memory-system/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-16-01` | FR-16-01, FR-16-05, AC-16-01 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| `T-16-02` | FR-16-02, FR-16-03 | `backend/app/domain/memory/scopes.py`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| `T-16-03` | FR-16-04, FR-16-06, AC-16-02, AC-16-03 | `backend/app/domain/memory/*`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>… +6 more |
| `T-16-04` | NFR-16-02, NFR-16-03, AC-16-04 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py`<br>… +5 more |
| `T-16-05` | FR-16-07 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py`<br>… +5 more |
| `T-16-06` | FR-16-08 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| `T-16-07` | FR-16-09 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| `T-16-08` | AC-16-03 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| `T-16-09` | AC-16-01, AC-16-02, AC-16-03, AC-16-04 | `tasks.md`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>… +1 more |
| `T-16-10` | NFR-16-01 | `requirements.md`<br>`16_memory-system/tasks.md RTM`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>… +2 more |
| `T-16-11` | AC-16-01, AC-16-02, AC-16-03 | `backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>`backend/app/schemas/memory.py` |
| `T-16-12` | FR-16-01, FR-16-02, NFR-16-01, AC-16-01 | `backend/app`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>… +1 more |
| `T-16-13` | AC-16-01, AC-16-02, AC-16-03, AC-16-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>`backend/app/domain/memory/models.py`<br>… +1 more |
| `T-16-14` | FR-16-01, FR-16-02, FR-16-03, FR-16-04, FR-16-05, FR-16-06, FR-16-07, FR-16-08, … | `planning/backend/16_memory-system/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/memory.py`<br>`backend/app/services/memory_service.py`<br>`backend/app/domain/memory/scopes.py`<br>`backend/app/domain/memory/retrieval.py`<br>… +2 more |

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
