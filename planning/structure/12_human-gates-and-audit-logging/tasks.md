# Tasks — 12 Human Gates and Audit Logging

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-12-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-12-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-12`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/12_human-gates-and-audit-logging/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-12**. Each task further narrows via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/approvals.py`
- `backend/app/api/v1/routes/audit_logs.py`
- `backend/app/domain/approvals/service.py`
- `backend/app/domain/approvals/models.py`
- `backend/app/domain/audit/events.py`
- `backend/app/domain/audit/models.py`
- `backend/app/services/approval_service.py`
- `backend/app/services/audit_service.py`
- `backend/app/runtime.py`
- `backend/app/tests/unit/test_scorecard_controls.py`
- `backend/app/tests/e2e/test_e1_operator_path.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-12-01 — Gate trigger table implemented
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 triggers |
| **Maps to** | FR-12-01…03, FR-12-06 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | DNA/irreversible/risk/DRC predicates pause run. |
| **Acceptance** | DNA/irreversible/risk/DRC predicates pause run. |
| **Evidence** | E1 billing gate |

### [x] T-12-02 — ApprovalRequest model
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5.1 |
| **Maps to** | FR-12-01, FR-12-07 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | pending approvals with risk_tier + run/step ids. |
| **Acceptance** | pending approvals with risk_tier + run/step ids. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-12-03 — Approval state machine
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5.3 |
| **Maps to** | FR-12-04…05 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | pending→approved |
| **Acceptance** | pending→approved |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-12-04 — Approve resumes execution
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3 architecture |
| **Maps to** | FR-12-04, AC-12-02, TV-12-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | E1 approve→complete. |
| **Acceptance** | E1 approve→complete. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-12-05 — Reject fails + lesson
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-12-03, C-12-6 |
| **Maps to** | FR-12-05, STRUCT-16 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | rejected status + improvement_lessons entry. |
| **Acceptance** | rejected status + improvement_lessons entry. |
| **Evidence** | runtime.decide_approval |

### [x] T-12-06 — Reviewer RBAC
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §6, NFR-12-03 |
| **Maps to** | AC-12-04, TV-12-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Non-reviewer 403. |
| **Acceptance** | Non-reviewer 403. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-12-07 — AuditEvent model + append
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5.2, D-12-02 |
| **Maps to** | FR-12-08…10, AC-12-03 |
| **Deliverable (code paths)** | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | tool + approval events queryable. |
| **Acceptance** | tool + approval events queryable. |
| **Evidence** | backend/app/domain/audit/events.py, backend/app/api/v1/routes/audit_logs.py, backend/app/runtime.py |

### [x] T-12-08 — Audit query filters
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §5.2 filters |
| **Maps to** | FR-12-11, TV-12-04 |
| **Deliverable (code paths)** | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Filter actor/action/resource/time. |
| **Acceptance** | Filter actor/action/resource/time. |
| **Evidence** | backend/app/domain/audit/events.py, backend/app/api/v1/routes/audit_logs.py, backend/app/runtime.py |

### [x] T-12-09 — No user delete audit API
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | NFR-12-04 |
| **Maps to** | NFR-12-04 |
| **Deliverable (code paths)** | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Append-only from clients. |
| **Acceptance** | Append-only from clients. |
| **Evidence** | backend/app/domain/audit/events.py, backend/app/api/v1/routes/audit_logs.py, backend/app/runtime.py |

### [x] T-12-10 — Fail-closed if required audit fails
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §6.1 |
| **Maps to** | FR-12-12 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`backend/app/tests/unit/test_real_execution.py`<br>`backend/app/tests/unit/test_hardening.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Policy documented; action incomplete on audit failure. |
| **Acceptance** | Policy documented; action incomplete on audit failure. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-12-11 — FE approvals surface
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-12-5 |
| **Maps to** | AC-12-05, FR-12-07 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Approvals page shows risk context. |
| **Acceptance** | Approvals page shows risk context. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-12-12 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/e2e/test_e1_operator_path.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-12-01` | FR-12-01…03, FR-12-06 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>… +3 more |
| `T-12-02` | FR-12-01, FR-12-07 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>… +3 more |
| `T-12-03` | FR-12-04…05 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>… +3 more |
| `T-12-04` | FR-12-04, AC-12-02, TV-12-01 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>… +3 more |
| `T-12-05` | FR-12-05, STRUCT-16 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>… +3 more |
| `T-12-06` | AC-12-04, TV-12-03 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>… +3 more |
| `T-12-07` | FR-12-08…10, AC-12-03 | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>… +3 more |
| `T-12-08` | FR-12-11, TV-12-04 | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>… +3 more |
| `T-12-09` | NFR-12-04 | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>… +3 more |
| `T-12-10` | FR-12-12 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +4 more |
| `T-12-11` | AC-12-05, FR-12-07 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>… +3 more |
| `T-12-12` |  | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/services/audit_service.py`<br>… +3 more |

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
