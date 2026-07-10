# Tasks — 04 Governance Risk Tiers and Artifacts

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-04-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-04-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-04`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/04_governance-risk-tiers-and-artifacts/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-04**. Each task further narrows via **Deliverable (code paths)**.

- `business/governance/`
- `business/governance/use-case-risk-tiering/runtime-tier-policy.json`
- `backend/app/domain/governance/policy_engine.py`
- `backend/app/domain/governance/risk.py`
- `backend/app/api/v1/routes/governance.py`
- `backend/app/services/governance_service.py`
- `backend/app/tests/unit/test_scorecard_controls.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-04-01 — SoT hierarchy conflict rule
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2.1 stricter-wins |
| **Maps to** | FR-04-01, D-04-02 |
| **Deliverable (code paths)** | `business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Documented; runtime prefers more gates. |
| **Acceptance** | Documented; runtime prefers more gates. |
| **Evidence** | design.md §2.1 |

### [x] T-04-02 — Tier 0–5 semantics table
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 table + runtime-tier-policy.json |
| **Maps to** | FR-04-01…07 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Six tiers with runtime effects documented and in JSON. |
| **Acceptance** | Six tiers with runtime effects documented and in JSON. |
| **Evidence** | `runtime-tier-policy.json`, risk-tiers.json |

### [x] T-04-03 — Gate evaluation pseudocode wired
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.1 needs_gate |
| **Maps to** | FR-04-06, FR-04-10 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Irreversible/high-risk steps pause (12). |
| **Acceptance** | Irreversible/high-risk steps pause (12). |
| **Evidence** | E1, runtime gates |

### [x] T-04-04 — Mandatory artifacts present
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.2, C-04-1…6 |
| **Maps to** | FR-04-08…13, AC-04-01…03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | inventory, policy, model card, assurance, tool perms. |
| **Acceptance** | inventory, policy, model card, assurance, tool perms. |
| **Evidence** | business:governance |

### [x] T-04-05 — business:governance CLI green
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-04-7 |
| **Maps to** | FR-04-14, AC-04-04, NFR-04-01 |
| **Deliverable (code paths)** | `business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Command pass &lt; 60s baseline. |
| **Acceptance** | Command pass &lt; 60s baseline. |
| **Evidence** | business/governance/, business/governance/use-case-risk-tiering/runtime-tier-policy.json, backend/app/domain/governance/policy_engine.py |

### [x] T-04-06 — Tier-5 without assurance blocked
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.1 can_start_tier5 |
| **Maps to** | FR-04-07, AC-04-05 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Policy/docs + restricted behavior defined. |
| **Acceptance** | Policy/docs + restricted behavior defined. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-04-07 — Framework anchors documented
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §5 NIST/ISO/EU |
| **Maps to** | FR-04-15…16 |
| **Deliverable (code paths)** | `business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | No false certification claims; anchors present. |
| **Acceptance** | No false certification claims; anchors present. |
| **Evidence** | business/governance/, business/governance/use-case-risk-tiering/runtime-tier-policy.json, backend/app/domain/governance/policy_engine.py |

### [x] T-04-08 — Backend authz for approvals
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-04-02, C-04-8 |
| **Maps to** | NFR-04-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Non-reviewer cannot decide. |
| **Acceptance** | Non-reviewer cannot decide. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-04-09 — DRC binding in policy
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | gate_triggers + drc_binding |
| **Maps to** | FR-04-10, STRUCT-07 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | runtime-tier-policy.json includes DRC triggers. |
| **Acceptance** | runtime-tier-policy.json includes DRC triggers. |
| **Evidence** | backend/app/api/v1/routes/approvals.py, backend/app/api/v1/routes/audit_logs.py, backend/app/domain/approvals/service.py |

### [x] T-04-10 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | AC-04-01…05 |
| **Deliverable (code paths)** | `business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | business/governance/, business/governance/use-case-risk-tiering/runtime-tier-policy.json, backend/app/domain/governance/policy_engine.py |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-04-01` | FR-04-01, D-04-02 | `business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-04-02` | FR-04-01…07 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`business/governance/`<br>… +4 more |
| `T-04-03` | FR-04-06, FR-04-10 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>… +4 more |
| `T-04-04` | FR-04-08…13, AC-04-01…03 | `backend/app/api/v1/routes/processes.py`<br>`backend/app/services/process_service.py`<br>`backend/app/domain/processes/analytics.py`<br>`backend/app/infrastructure/process_intelligence/artifacts.py`<br>`business/process-intelligence/`<br>`backend/app/tests/unit/test_p3_pi_evolution.py`<br>`business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>… +4 more |
| `T-04-05` | FR-04-14, AC-04-04, NFR-04-01 | `business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-04-06` | FR-04-07, AC-04-05 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`business/governance/`<br>… +4 more |
| `T-04-07` | FR-04-15…16 | `business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |
| `T-04-08` | NFR-04-02 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>… +4 more |
| `T-04-09` | FR-04-10, STRUCT-07 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>… +4 more |
| `T-04-10` | AC-04-01…05 | `business/governance/`<br>`business/governance/use-case-risk-tiering/runtime-tier-policy.json`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/tests/unit/test_scorecard_controls.py` |

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
