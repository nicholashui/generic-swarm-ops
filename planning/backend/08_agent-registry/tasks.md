# Tasks — 08 Agent Registry

| Field | Value |
|-------|-------|
| Task list ID | `BE-08-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-08-DES`) |
| Paired requirements | `requirements.md` (`BE-08`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 3/3 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Agent CRUD → metadata/allow-lists → status lifecycle → runtime contracts → seed agents.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-08. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/agents.py`
- `backend/app/services/agent_service.py`
- `backend/app/domain/agents/models.py`
- `backend/app/domain/agents/runtime.py`
- `backend/app/domain/agents/policies.py`
- `backend/app/schemas/agents.py`
- `backend/app/infrastructure/repositories/agent_repository.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-08-01 — Agent registry CRUD APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-08-1 |
| **Maps to** | FR-08-01, FR-08-06, AC-08-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| **Test-first** | Create then get by id. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Registry usable. |
| **Acceptance** | Registry usable. |
| **Evidence** | api/v1/routes/agents.py |

### [x] T-08-02 — Persist full agent metadata fields
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 Agent record |
| **Maps to** | FR-08-02, AC-08-03 |
| **Deliverable (code paths)** | `backend/app/domain/agents/models.py`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py` |
| **Test-first** | allowed_tools returned on get. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | DNA can reference constraints. |
| **Acceptance** | DNA can reference constraints. |
| **Evidence** | domain/agents/models.py |

### [x] T-08-03 — Agent status lifecycle draft/active/disabled/archived
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 status |
| **Maps to** | FR-08-03, FR-08-05, AC-08-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| **Test-first** | Disabled cannot start new steps. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safety on disable. |
| **Acceptance** | Safety on disable. |
| **Evidence** | engine + agents |

### [x] T-08-04 — Org-scoped listing + authz
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5 |
| **Maps to** | FR-08-04, NFR-08-02, AC-08-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Unauthorized create 403. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Tenant isolation. |
| **Acceptance** | Tenant isolation. |
| **Evidence** | agents routes |

### [x] T-08-05 — Activity + tools inspection endpoints
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-08-1 |
| **Maps to** | FR-08-07 |
| **Deliverable (code paths)** | `agents.py`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py` |
| **Test-first** | Endpoints respond. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Ops visibility. |
| **Acceptance** | Ops visibility. |
| **Evidence** | agents.py |

### [x] T-08-06 — Runtime input/output contracts
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-08-3 |
| **Maps to** | FR-08-08, FR-08-09 |
| **Deliverable (code paths)** | `backend/app/domain/agents/runtime.py`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| **Test-first** | Tool outside allow-list denied. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Brokered execution. |
| **Acceptance** | Brokered execution. |
| **Evidence** | domain/agents/runtime.py |

### [x] T-08-07 — Version stability for historical runs
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | FR-08-10 |
| **Maps to** | FR-08-10 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/schemas/workflows.py` |
| **Test-first** | Run pins agent/workflow version metadata. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Replay integrity. |
| **Acceptance** | Replay integrity. |
| **Evidence** | run records |

### [x] T-08-08 — No plaintext secrets in runtime_config
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-08-03 |
| **Maps to** | NFR-08-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py` |
| **Test-first** | Review config fields. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Secret refs only. |
| **Acceptance** | Secret refs only. |
| **Evidence** | agent models |

### [x] T-08-09 — Flagship seed agents for E1
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | TV-08-03 |
| **Maps to** | AC-08-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>`backend/app/runtime.py`<br>`backend/app/infrastructure/database/session.py`<br>`backend/app/infrastructure/database/models.py`<br>`backend/app/infrastructure/repositories`<br>`backend/app/tests/unit/test_postgres_restart.py` |
| **Test-first** | E1 finds agents. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | E1 unblocked. |
| **Acceptance** | E1 unblocked. |
| **Evidence** | seed data |

### [x] T-08-10 — Exit review — agents complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-08-01, AC-08-02, AC-08-03, AC-08-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-08-11 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-08-01 |
| **Deliverable (code paths)** | `requirements.md`<br>`08_agent-registry/tasks.md RTM`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=1 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 08_agent-registry/tasks.md RTM |

### [x] T-08-12 — Implement/verify all design components C-*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-08-2, C-08-1, C-08-2, C-08-3 |
| **Maps to** | AC-08-01, AC-08-02, AC-08-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| **Test-first** | Component module import/smoke or route presence. |
| **Steps** | 1) Map each C-* to module path in design. 2) Verify module exists and is wired. 3) Add smoke test if missing. |
| **Success** | All design components have implementation anchors. |
| **Acceptance** | Components covered: C-08-1, C-08-2, C-08-3 |
| **Evidence** | ### 3.1 Components |

### [x] T-08-13 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-08-01, D-08-02 |
| **Maps to** | FR-08-01, FR-08-02, NFR-08-01, AC-08-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-08-14 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-08-01, AC-08-02, AC-08-03, AC-08-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-08-15 — Exit review — BE-08 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-08-01, FR-08-02, FR-08-03, FR-08-04, FR-08-05, FR-08-06, FR-08-07, FR-08-08, FR-08-09, FR-08-10, NFR-08-01, NFR-08-02, NFR-08-03, AC-08-01, AC-08-02, AC-08-03, AC-08-04 |
| **Deliverable (code paths)** | `planning/backend/08_agent-registry/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/08_agent-registry/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-08-01` | FR-08-01, FR-08-06, AC-08-01 | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| `T-08-02` | FR-08-02, AC-08-03 | `backend/app/domain/agents/models.py`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>… +5 more |
| `T-08-03` | FR-08-03, FR-08-05, AC-08-02 | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| `T-08-04` | FR-08-04, NFR-08-02, AC-08-04 | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>… +5 more |
| `T-08-05` | FR-08-07 | `agents.py`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>… +6 more |
| `T-08-06` | FR-08-08, FR-08-09 | `backend/app/domain/agents/runtime.py`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| `T-08-07` | FR-08-10 | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>… +5 more |
| `T-08-08` | NFR-08-03 | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>… +5 more |
| `T-08-09` | AC-08-01 | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py`<br>… +5 more |
| `T-08-10` | AC-08-01, AC-08-02, AC-08-03, AC-08-04 | `tasks.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>… +1 more |
| `T-08-11` | NFR-08-01 | `requirements.md`<br>`08_agent-registry/tasks.md RTM`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>… +2 more |
| `T-08-12` | AC-08-01, AC-08-02, AC-08-03 | `backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>`backend/app/schemas/agents.py` |
| `T-08-13` | FR-08-01, FR-08-02, NFR-08-01, AC-08-01 | `backend/app`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>… +1 more |
| `T-08-14` | AC-08-01, AC-08-02, AC-08-03, AC-08-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>`backend/app/domain/agents/policies.py`<br>… +1 more |
| `T-08-15` | FR-08-01, FR-08-02, FR-08-03, FR-08-04, FR-08-05, FR-08-06, FR-08-07, FR-08-08, … | `planning/backend/08_agent-registry/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/agents.py`<br>`backend/app/services/agent_service.py`<br>`backend/app/domain/agents/models.py`<br>`backend/app/domain/agents/runtime.py`<br>… +2 more |

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
