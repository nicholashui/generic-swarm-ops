# Tasks — 13 Human Approval Gates

| Field | Value |
|-------|-------|
| Task list ID | `BE-13-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-13-DES`) |
| Paired requirements | `requirements.md` (`BE-13`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 3/3 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Approval model → create on gate → approve/reject APIs → block while pending → E1 gate.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-13. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/approvals.py`
- `backend/app/services/approval_service.py`
- `backend/app/domain/approvals/service.py`
- `backend/app/domain/approvals/models.py`
- `backend/app/schemas/approvals.py`
- `backend/app/infrastructure/repositories/approval_repository.py`
- `backend/app/tests/unit/test_scorecard_controls.py`
- `backend/app/tests/e2e/test_e1_operator_path.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-13-01 — ApprovalRequest model + statuses
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-13-3, §4 |
| **Maps to** | FR-13-01, FR-13-02, FR-13-03 |
| **Deliverable (code paths)** | `backend/app/domain/approvals/models.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Pending created on gate. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Entity complete. |
| **Acceptance** | Entity complete. |
| **Evidence** | domain/approvals/models.py |

### [x] T-13-02 — Create approval when gate required
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-13-2 |
| **Maps to** | FR-13-01, AC-13-01 |
| **Deliverable (code paths)** | `backend/app/domain/approvals/service.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Flagship gated run pending. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Engine handoff works. |
| **Acceptance** | Engine handoff works. |
| **Evidence** | domain/approvals/service.py |

### [x] T-13-03 — Approve resumes run
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3 arch |
| **Maps to** | FR-13-04, AC-13-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Approve → continue. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | HITL path. |
| **Acceptance** | HITL path. |
| **Evidence** | approvals service + engine |

### [x] T-13-04 — Reject stops gated action
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3 |
| **Maps to** | FR-13-05, AC-13-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Reject path. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safe stop. |
| **Acceptance** | Safe stop. |
| **Evidence** | tests |

### [x] T-13-05 — Decision reason required/stored
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-13-01 |
| **Maps to** | FR-13-02, AC-13-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Reason persisted. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Auditability. |
| **Acceptance** | Auditability. |
| **Evidence** | approval records |

### [x] T-13-06 — Approve/reject/reassign/decision APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-13-1, §5 |
| **Maps to** | FR-13-06, FR-13-07, FR-13-09 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | RBAC on decide. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Ops console can decide. |
| **Acceptance** | Ops console can decide. |
| **Evidence** | api/v1/routes/approvals.py |

### [x] T-13-07 — Block irreversible while pending
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-13-02, FR-13-08 |
| **Maps to** | FR-13-08 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | No tool side effect mid-gate. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Hard pause. |
| **Acceptance** | Hard pause. |
| **Evidence** | engine |

### [x] T-13-08 — Audit approval decisions
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-13-10 |
| **Maps to** | FR-13-10 |
| **Deliverable (code paths)** | `backend/app/domain/audit`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Audit event on decide. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Forensics. |
| **Acceptance** | Forensics. |
| **Evidence** | domain/audit |

### [x] T-13-09 — E1 human gate segment
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | TV-13-03 |
| **Maps to** | AC-13-01, AC-13-02, AC-13-03, AC-13-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | E1 includes gate. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | E1 green. |
| **Acceptance** | E1 green. |
| **Evidence** | test_e1_operator_path |

### [x] T-13-10 — Exit review — approvals complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-13-01, AC-13-02, AC-13-03, AC-13-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-13-11 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-13-01, NFR-13-02, NFR-13-03 |
| **Deliverable (code paths)** | `requirements.md`<br>`13_human-approval-gates/tasks.md RTM`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=3 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 13_human-approval-gates/tasks.md RTM |

### [x] T-13-12 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-13-01, D-13-02 |
| **Maps to** | FR-13-01, FR-13-02, NFR-13-01, AC-13-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-13-13 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-13-01, AC-13-02, AC-13-03, AC-13-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-13-14 — Exit review — BE-13 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-13-01, FR-13-02, FR-13-03, FR-13-04, FR-13-05, FR-13-06, FR-13-07, FR-13-08, FR-13-09, FR-13-10, NFR-13-01, NFR-13-02, NFR-13-03, AC-13-01, AC-13-02, AC-13-03, AC-13-04 |
| **Deliverable (code paths)** | `planning/backend/13_human-approval-gates/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/13_human-approval-gates/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-13-01` | FR-13-01, FR-13-02, FR-13-03 | `backend/app/domain/approvals/models.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| `T-13-02` | FR-13-01, AC-13-01 | `backend/app/domain/approvals/service.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| `T-13-03` | FR-13-04, AC-13-02 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| `T-13-04` | FR-13-05, AC-13-03 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| `T-13-05` | FR-13-02, AC-13-04 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| `T-13-06` | FR-13-06, FR-13-07, FR-13-09 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| `T-13-07` | FR-13-08 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| `T-13-08` | FR-13-10 | `backend/app/domain/audit`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>… +1 more |
| `T-13-09` | AC-13-01, AC-13-02, AC-13-03, AC-13-04 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>`backend/app/infrastructure/repositories/approval_repository.py` |
| `T-13-10` | AC-13-01, AC-13-02, AC-13-03, AC-13-04 | `tasks.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>… +1 more |
| `T-13-11` | NFR-13-01, NFR-13-02, NFR-13-03 | `requirements.md`<br>`13_human-approval-gates/tasks.md RTM`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>… +2 more |
| `T-13-12` | FR-13-01, FR-13-02, NFR-13-01, AC-13-01 | `backend/app`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>… +1 more |
| `T-13-13` | AC-13-01, AC-13-02, AC-13-03, AC-13-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py`<br>… +1 more |
| `T-13-14` | FR-13-01, FR-13-02, FR-13-03, FR-13-04, FR-13-05, FR-13-06, FR-13-07, FR-13-08, … | `planning/backend/13_human-approval-gates/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>… +2 more |

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
