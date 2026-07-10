# Tasks — 10 Workflow DNA Definition

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-10-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-10-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-10`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/10_workflow-dna-definition/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-10**. Each task further narrows via **Deliverable (code paths)**.

- `business/distilled/workflows/`
- `backend/app/domain/workflows/models.py`
- `backend/app/domain/workflows/policies.py`
- `backend/app/api/v1/routes/workflows.py`
- `backend/app/services/workflow_service.py`
- `backend/app/infrastructure/governance/structure_validators.py`
- `backend/app/tests/unit/test_structure_sdd_validators.py`
- `business/fixtures/negative/`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-10-01 — DNA field-level model complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 + §4.1 step model |
| **Maps to** | FR-10-01…09 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | All required fields in schema. |
| **Acceptance** | All required fields in schema. |
| **Evidence** | workflow-dna.schema.json |

### [x] T-10-02 — Schema + example validate
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-10-1, C-10-2 |
| **Maps to** | AC-10-01 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | business:validate green for example. |
| **Acceptance** | business:validate green for example. |
| **Evidence** | business/distilled/workflows/, backend/app/domain/workflows/models.py, backend/app/domain/workflows/policies.py |

### [x] T-10-03 — V-DNA-01 irreversible without gate
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.2 V-DNA-01 |
| **Maps to** | FR-10-10, AC-10-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py` |
| **Test-first** | Negative fixture fails. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Requirement behaviour satisfied in deliverable code. |
| **Acceptance** | AC/FR mapped behaviour verified against deliverable paths. |
| **Evidence** | dna-irreversible-without-gate.json + validators |

### [x] T-10-04 — V-DNA-02 irreversible without rollback
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | V-DNA-02 |
| **Maps to** | FR-10-11 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Requirement behaviour satisfied in deliverable code. |
| **Acceptance** | AC/FR mapped behaviour verified against deliverable paths. |
| **Evidence** | dna-irreversible-without-rollback.json |

### [x] T-10-05 — V-DNA-03…05 high-risk, audit, wildcards
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.2 |
| **Maps to** | FR-10-12, NFR-10-03 |
| **Deliverable (code paths)** | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/runtime.py`<br>`business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | validate-business + structure_validators. |
| **Acceptance** | validate-business + structure_validators. |
| **Evidence** | backend/app/domain/audit/events.py, backend/app/api/v1/routes/audit_logs.py, backend/app/runtime.py |

### [x] T-10-06 — Flagship onboarding DNA
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §6 |
| **Maps to** | FR-10-13, AC-10-03 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | wf_customer_onboarding_v12 with gate+fitness. |
| **Acceptance** | wf_customer_onboarding_v12 with gate+fitness. |
| **Evidence** | business/distilled/workflows/, backend/app/domain/workflows/models.py, backend/app/domain/workflows/policies.py |

### [x] T-10-07 — Versioning protocol
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5 versioning |
| **Maps to** | AC-10-04 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | version required; promote bumps version. |
| **Acceptance** | version required; promote bumps version. |
| **Evidence** | business/distilled/workflows/, backend/app/domain/workflows/models.py, backend/app/domain/workflows/policies.py |

### [x] T-10-08 — DRC binding fields
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | guardrails.decision_requirement_cards |
| **Maps to** | FR-10-06, STRUCT-07 |
| **Deliverable (code paths)** | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Example DNA + schema support. |
| **Acceptance** | Example DNA + schema support. |
| **Evidence** | business/experts/, business/experts/decision-requirement-cards/, business/fixtures/negative/ |

### [x] T-10-09 — FE create maps to DNA
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-10-6 |
| **Maps to** | design FE |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Zod forms for workflow create. |
| **Acceptance** | Zod forms for workflow create. |
| **Evidence** | business/distilled/workflows/, backend/app/domain/workflows/models.py, backend/app/domain/workflows/policies.py |

### [x] T-10-10 — No secrets in DNA
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-10-02 |
| **Maps to** | NFR-10-02 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | security scan clean. |
| **Acceptance** | security scan clean. |
| **Evidence** | business/distilled/workflows/, backend/app/domain/workflows/models.py, backend/app/domain/workflows/policies.py |

### [x] T-10-11 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | business/distilled/workflows/, backend/app/domain/workflows/models.py, backend/app/domain/workflows/policies.py |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-10-01` | FR-10-01…09 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| `T-10-02` | AC-10-01 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| `T-10-03` | FR-10-10, AC-10-02 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>… +4 more |
| `T-10-04` | FR-10-11 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| `T-10-05` | FR-10-12, NFR-10-03 | `backend/app/domain/audit/events.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/runtime.py`<br>`business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>… +3 more |
| `T-10-06` | FR-10-13, AC-10-03 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| `T-10-07` | AC-10-04 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| `T-10-08` | FR-10-06, STRUCT-07 | `business/experts/`<br>`business/experts/decision-requirement-cards/`<br>`business/fixtures/negative/`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>… +2 more |
| `T-10-09` | design FE | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| `T-10-10` | NFR-10-02 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |
| `T-10-11` |  | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative/` |

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
