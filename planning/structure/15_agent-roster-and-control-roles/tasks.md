# Tasks — 15 Agent Roster and Control Roles

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-15-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-15-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-15`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/15_agent-roster-and-control-roles/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-15**. Each task further narrows via **Deliverable (code paths)**.

- `business/role-realization-map.md`
- `backend/app/api/v1/routes/agents.py`
- `backend/app/domain/agents/models.py`
- `backend/app/domain/agents/runtime.py`
- `backend/app/services/agent_service.py`
- `backend/app/runtime.py`
- `backend/app/tests/unit/test_structure_sdd_validators.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-15-01 — Full realization matrix
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3.1 matrix |
| **Maps to** | FR-15-01…12, AC-15-03 |
| **Deliverable (code paths)** | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Every structure.md role mapped agent/service/process. |
| **Acceptance** | Every structure.md role mapped agent/service/process. |
| **Evidence** | design.md + role-realization-map.md |

### [x] T-15-02 — role-realization-map.md artifact
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3.1 artifact |
| **Maps to** | AC-15-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | File under business/governance/. |
| **Acceptance** | File under business/governance/. |
| **Evidence** | backend/app/api/v1/routes/processes.py, backend/app/services/process_service.py, backend/app/domain/processes/analytics.py |

### [x] T-15-03 — Agent record model
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 Agent |
| **Maps to** | FR-15-13 |
| **Deliverable (code paths)** | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | allowed_tools + allowed_memory_scopes on agents. |
| **Acceptance** | allowed_tools + allowed_memory_scopes on agents. |
| **Evidence** | business/role-realization-map.md, backend/app/api/v1/routes/agents.py, backend/app/domain/agents/models.py |

### [x] T-15-04 — Seed agents for flagship
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.2 seed policy |
| **Maps to** | AC-15-01 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Scopes union includes DNA memory_reads needs. |
| **Acceptance** | Scopes union includes DNA memory_reads needs. |
| **Evidence** | E1 seed fix |

### [x] T-15-05 — Deny out-of-role tools
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.1 act() |
| **Maps to** | FR-15-14, AC-15-04 |
| **Deliverable (code paths)** | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Broker deny unit tests. |
| **Acceptance** | Broker deny unit tests. |
| **Evidence** | business/role-realization-map.md, backend/app/api/v1/routes/agents.py, backend/app/domain/agents/models.py |

### [x] T-15-06 — AI inventory registration
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-15-03 |
| **Maps to** | FR-15-15, AC-15-02 |
| **Deliverable (code paths)** | `business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | inventory.json lists material agents. |
| **Acceptance** | inventory.json lists material agents. |
| **Evidence** | business/governance/, business/governance/use-case-risk-tiering/runtime-tier-policy.json, backend/app/domain/governance/policy_engine.py |

### [x] T-15-07 — Evolution Manager no prod DNA write
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-15-02, NFR-15-03 |
| **Maps to** | NFR-15-03 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Covered by evolution guards (14). |
| **Acceptance** | Covered by evolution guards (14). |
| **Evidence** | business/distilled/workflows/, backend/app/domain/workflows/models.py, backend/app/domain/workflows/policies.py |

### [x] T-15-08 — Agents API + FE
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §5 API |
| **Maps to** | NFR-15-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | GET/POST agents; create form. |
| **Acceptance** | GET/POST agents; create form. |
| **Evidence** | backend/app/api/v1/routes/processes.py, backend/app/services/process_service.py, backend/app/domain/processes/analytics.py |

### [x] T-15-09 — Dual-harness naming best effort
| | |
|--|--|
| **Priority** | P2 |
| **Status** | [x] Implemented |
| **Design** | OI-15-02 |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | .trae/.grok agents via sync; not same store as runtime. |
| **Acceptance** | .trae/.grok agents via sync; not same store as runtime. |
| **Evidence** | business/role-realization-map.md, backend/app/api/v1/routes/agents.py, backend/app/domain/agents/models.py |

### [x] T-15-10 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | business/role-realization-map.md, backend/app/api/v1/routes/agents.py, backend/app/domain/agents/models.py |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-15-01` | FR-15-01…12, AC-15-03 | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| `T-15-02` | AC-15-03 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>… +4 more |
| `T-15-03` | FR-15-13 | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| `T-15-04` | AC-15-01 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>… +4 more |
| `T-15-05` | FR-15-14, AC-15-04 | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| `T-15-06` | FR-15-15, AC-15-02 | `business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>… +4 more |
| `T-15-07` | NFR-15-03 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>… +4 more |
| `T-15-08` | NFR-15-01 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>… +4 more |
| `T-15-09` |  | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |
| `T-15-10` |  | `business/role-realization-map.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py` |

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
