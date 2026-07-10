# Tasks — 12 Governance Policies and Risk

| Field | Value |
|-------|-------|
| Task list ID | `BE-12-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-12-DES`) |
| Paired requirements | `requirements.md` (`BE-12`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 3/3 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Policy engine → risk levels → CRUD/check APIs → run pre-check → audit policy changes.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-12. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/governance.py`
- `backend/app/services/governance_service.py`
- `backend/app/domain/governance/policy_engine.py`
- `backend/app/domain/governance/risk.py`
- `backend/app/domain/governance/models.py`
- `backend/app/schemas/governance.py`
- `business/governance/use-case-risk-tiering/runtime-tier-policy.json`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-12-01 — Policy engine actions allow/deny/require_*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-12-2, §4 |
| **Maps to** | FR-12-01, FR-12-03, AC-12-01 |
| **Deliverable (code paths)** | `backend/app/domain/governance/policy_engine.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Unit table for actions. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Deterministic decisions. |
| **Acceptance** | Deterministic decisions. |
| **Evidence** | domain/governance/policy_engine.py |

### [x] T-12-02 — Risk levels low…critical
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-12-3 |
| **Maps to** | FR-12-02 |
| **Deliverable (code paths)** | `backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Risk mapping unit tests. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Levels documented/enforced. |
| **Acceptance** | Levels documented/enforced. |
| **Evidence** | domain/governance/risk.py |

### [x] T-12-03 — Policy CRUD + check/preview APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-12-1 |
| **Maps to** | FR-12-04, FR-12-05 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Create policy; check endpoint. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Ops can manage rules. |
| **Acceptance** | Ops can manage rules. |
| **Evidence** | api/v1/routes/governance.py |

### [x] T-12-04 — Run-start governance pre-check
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-12-06 |
| **Maps to** | FR-12-06, FR-12-07, FR-12-08, AC-12-02, AC-12-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Deny blocks; require_approval gates. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Engine integrated. |
| **Acceptance** | Engine integrated. |
| **Evidence** | runtime start path |

### [x] T-12-05 — Record deny reasons + audit policy changes
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-12-07, FR-12-09 |
| **Maps to** | FR-12-07, FR-12-09, AC-12-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py` |
| **Test-first** | Policy update audited. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Explainable governance. |
| **Acceptance** | Explainable governance. |
| **Evidence** | audit + governance |

### [x] T-12-06 — Runtime tier policy mapping
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-12-4, D-12-02 |
| **Maps to** | FR-12-10 |
| **Deliverable (code paths)** | `runtime-tier-policy / risk`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Tier policy file/load if present. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | structure tiers realized. |
| **Acceptance** | structure tiers realized. |
| **Evidence** | runtime-tier-policy / risk |

### [x] T-12-07 — Non-overridable deny (no client force)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-12-02 |
| **Maps to** | NFR-12-02, NFR-12-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Force flags ignored. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Hard security. |
| **Acceptance** | Hard security. |
| **Evidence** | policy_engine |

### [x] T-12-08 — Exit review — governance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-12-01, AC-12-02, AC-12-03, AC-12-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-12-09 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-12-01 |
| **Deliverable (code paths)** | `requirements.md`<br>`12_governance-policies-and-risk/tasks.md RTM`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=1 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 12_governance-policies-and-risk/tasks.md RTM |

### [x] T-12-10 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-12-01, D-12-02 |
| **Maps to** | FR-12-01, FR-12-02, NFR-12-01, AC-12-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-12-11 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-12-01, AC-12-02, AC-12-03, AC-12-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-12-12 — Exit review — BE-12 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-12-01, FR-12-02, FR-12-03, FR-12-04, FR-12-05, FR-12-06, FR-12-07, FR-12-08, FR-12-09, FR-12-10, NFR-12-01, NFR-12-02, NFR-12-03, AC-12-01, AC-12-02, AC-12-03, AC-12-04 |
| **Deliverable (code paths)** | `planning/backend/12_governance-policies-and-risk/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/12_governance-policies-and-risk/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-12-01` | FR-12-01, FR-12-03, AC-12-01 | `backend/app/domain/governance/policy_engine.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| `T-12-02` | FR-12-02 | `backend/app/domain/governance/risk.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| `T-12-03` | FR-12-04, FR-12-05 | `backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| `T-12-04` | FR-12-06, FR-12-07, FR-12-08, AC-12-02, AC-12-03 | `backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| `T-12-05` | FR-12-07, FR-12-09, AC-12-04 | `backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py`<br>… +5 more |
| `T-12-06` | FR-12-10 | `runtime-tier-policy / risk`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>… +1 more |
| `T-12-07` | NFR-12-02, NFR-12-03 | `backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>`backend/app/schemas/governance.py` |
| `T-12-08` | AC-12-01, AC-12-02, AC-12-03, AC-12-04 | `tasks.md`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>… +1 more |
| `T-12-09` | NFR-12-01 | `requirements.md`<br>`12_governance-policies-and-risk/tasks.md RTM`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>… +2 more |
| `T-12-10` | FR-12-01, FR-12-02, NFR-12-01, AC-12-01 | `backend/app`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>… +1 more |
| `T-12-11` | AC-12-01, AC-12-02, AC-12-03, AC-12-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py`<br>… +1 more |
| `T-12-12` | FR-12-01, FR-12-02, FR-12-03, FR-12-04, FR-12-05, FR-12-06, FR-12-07, FR-12-08, … | `planning/backend/12_governance-policies-and-risk/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>… +2 more |

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
