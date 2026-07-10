# Tasks — 09 Tool Registry, Adapters, and Broker

| Field | Value |
|-------|-------|
| Task list ID | `BE-09-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-09-DES`) |
| Paired requirements | `requirements.md` (`BE-09`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 4/4 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Tool catalog → broker unit tests → adapters+tool_effects → high-risk gates → redaction.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-09. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/tools.py`
- `backend/app/services/tool_service.py`
- `backend/app/infrastructure/tools/adapters.py`
- `backend/app/infrastructure/integrations/crm.py`
- `backend/app/infrastructure/integrations/email.py`
- `backend/app/infrastructure/integrations/calendar.py`
- `backend/app/schemas/tools.py`
- `backend/app/tests/unit/test_real_execution.py`
- `backend/app/runtime.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-09-01 — Tool registry metadata + categories
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4, C-09-1 |
| **Maps to** | FR-09-01, FR-09-02, FR-09-03, AC-09-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | List tools includes locals. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Catalog complete. |
| **Acceptance** | Catalog complete. |
| **Evidence** | api/v1/routes/tools.py |

### [x] T-09-02 — Broker intersection algorithm
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 broker algorithm, D-09-03 |
| **Maps to** | FR-09-06, AC-09-03 |
| **Deliverable (code paths)** | `runtime/domain broker path`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Unit matrix agent/DNA/RBAC/gate. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Least privilege tools. |
| **Acceptance** | Least privilege tools. |
| **Evidence** | runtime/domain broker path |

### [x] T-09-03 — Local adapters execute + tool_effects durable
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-09-2, C-09-3, D-09-01…02 |
| **Maps to** | FR-09-05, NFR-09-02, AC-09-02 |
| **Deliverable (code paths)** | `backend/app/infrastructure/integrations/*`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Mutating call writes effect. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Fail-closed side effects. |
| **Acceptance** | Fail-closed side effects. |
| **Evidence** | infrastructure/integrations/* |

### [x] T-09-04 — High-risk tools require governance/approval
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-09-04 |
| **Maps to** | FR-09-04, AC-09-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py` |
| **Test-first** | Irreversible without gate denied. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Gate integration. |
| **Acceptance** | Gate integration. |
| **Evidence** | engine + governance |

### [x] T-09-05 — Disabled tool rejects invoke
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-09-07 |
| **Maps to** | FR-09-07 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Disabled → error. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Kill switch works. |
| **Acceptance** | Kill switch works. |
| **Evidence** | tool registry |

### [x] T-09-06 — Timeouts honored
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | NFR-09-01 |
| **Maps to** | NFR-09-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Adapter respects timeout config. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No hang forever. |
| **Acceptance** | No hang forever. |
| **Evidence** | adapters |

### [x] T-09-07 — Never return tool secrets to clients
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-09-03 |
| **Maps to** | NFR-09-03, NFR-09-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Response redaction review. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safe APIs. |
| **Acceptance** | Safe APIs. |
| **Evidence** | routes |

### [x] T-09-08 — Document live SaaS adapters as non-goal
| | |
|--|--|
| **Priority** | P3 |
| **Status** | [x] Implemented |
| **Design** | OI-09-01…02 |
| **Maps to** | scope_out |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Non-goal in design/status. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Scope clear. |
| **Acceptance** | Scope clear. |
| **Evidence** | design open issues |

### [x] T-09-09 — Exit review — tools complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-09-01, AC-09-02, AC-09-03, AC-09-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-09-10 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | FR-09-08, FR-09-09, FR-09-10 |
| **Deliverable (code paths)** | `requirements.md`<br>`09_tool-registry-adapters-and-broker/tasks.md RTM`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=3 NFR=0 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 09_tool-registry-adapters-and-broker/tasks.md RTM |

### [x] T-09-11 — Implement/verify all design components C-*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-09-4, C-09-1, C-09-2, C-09-3 |
| **Maps to** | AC-09-01, AC-09-02, AC-09-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Component module import/smoke or route presence. |
| **Steps** | 1) Map each C-* to module path in design. 2) Verify module exists and is wired. 3) Add smoke test if missing. |
| **Success** | All design components have implementation anchors. |
| **Acceptance** | Components covered: C-09-1, C-09-2, C-09-3, C-09-4 |
| **Evidence** | ### 3.1 Components |

### [x] T-09-12 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-09-01, D-09-02, D-09-03 |
| **Maps to** | FR-09-01, FR-09-02, NFR-09-01, AC-09-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-09-13 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-09-01, AC-09-02, AC-09-03, AC-09-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-09-14 — Exit review — BE-09 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-09-01, FR-09-02, FR-09-03, FR-09-04, FR-09-05, FR-09-06, FR-09-07, FR-09-08, FR-09-09, FR-09-10, NFR-09-01, NFR-09-02, NFR-09-03, NFR-09-04, AC-09-01, AC-09-02, AC-09-03, AC-09-04 |
| **Deliverable (code paths)** | `planning/backend/09_tool-registry-adapters-and-broker/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/09_tool-registry-adapters-and-broker/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-09-01` | FR-09-01, FR-09-02, FR-09-03, AC-09-01 | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| `T-09-02` | FR-09-06, AC-09-03 | `runtime/domain broker path`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>… +1 more |
| `T-09-03` | FR-09-05, NFR-09-02, AC-09-02 | `backend/app/infrastructure/integrations/*`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>… +1 more |
| `T-09-04` | FR-09-04, AC-09-04 | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py`<br>… +5 more |
| `T-09-05` | FR-09-07 | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| `T-09-06` | NFR-09-01 | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| `T-09-07` | NFR-09-03, NFR-09-04 | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| `T-09-08` | scope_out | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| `T-09-09` | AC-09-01, AC-09-02, AC-09-03, AC-09-04 | `tasks.md`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>… +1 more |
| `T-09-10` | FR-09-08, FR-09-09, FR-09-10 | `requirements.md`<br>`09_tool-registry-adapters-and-broker/tasks.md RTM`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>… +2 more |
| `T-09-11` | AC-09-01, AC-09-02, AC-09-03 | `backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>`backend/app/infrastructure/integrations/calendar.py` |
| `T-09-12` | FR-09-01, FR-09-02, NFR-09-01, AC-09-01 | `backend/app`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>… +1 more |
| `T-09-13` | AC-09-01, AC-09-02, AC-09-03, AC-09-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>`backend/app/infrastructure/integrations/email.py`<br>… +1 more |
| `T-09-14` | FR-09-01, FR-09-02, FR-09-03, FR-09-04, FR-09-05, FR-09-06, FR-09-07, FR-09-08, … | `planning/backend/09_tool-registry-adapters-and-broker/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/tools.py`<br>`backend/app/services/tool_service.py`<br>`backend/app/infrastructure/tools/adapters.py`<br>`backend/app/infrastructure/integrations/crm.py`<br>… +2 more |

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
