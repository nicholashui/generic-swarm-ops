# Tasks — 06 Authorization and RBAC

| Field | Value |
|-------|-------|
| Task list ID | `BE-06-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-06-DES`) |
| Paired requirements | `requirements.md` (`BE-06`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 4/4 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Permission catalog → role maps → route dependencies → deny tests → no self-escalation.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-06. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/core/permissions.py`
- `backend/app/api/dependencies.py`
- `backend/app/runtime.py`
- `backend/app/tests/unit/test_scorecard_controls.py`
- `backend/app/tests/unit/test_hardening.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-06-01 — Permission catalog strings
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-06-1 |
| **Maps to** | FR-06-01, FR-06-04, FR-06-05, FR-06-06, FR-06-07 |
| **Deliverable (code paths)** | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Catalog includes agents/workflows/approvals/… |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Stable permission names. |
| **Acceptance** | Stable permission names. |
| **Evidence** | core/permissions.py |

### [x] T-06-02 — Role → permission maps (Owner…Viewer…)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 roles |
| **Maps to** | FR-06-02, AC-06-01, AC-06-02, AC-06-03 |
| **Deliverable (code paths)** | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Matrix unit tests. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Least privilege defaults. |
| **Acceptance** | Least privilege defaults. |
| **Evidence** | permissions + seeds |

### [x] T-06-03 — Route require_permission dependencies
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-06-2, D-06-02 |
| **Maps to** | FR-06-03, NFR-06-03, AC-06-04 |
| **Deliverable (code paths)** | `api/dependencies.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Missing perm → 403. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Server-side enforcement. |
| **Acceptance** | Server-side enforcement. |
| **Evidence** | api/dependencies.py |

### [x] T-06-04 — API keys use same permission model
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-06-03 |
| **Maps to** | FR-06-10 |
| **Deliverable (code paths)** | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Key without perm denied. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Parity with users. |
| **Acceptance** | Parity with users. |
| **Evidence** | auth + permissions |

### [x] T-06-05 — Avoid existence leaks on deny (where policy)
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | FR-06-09 |
| **Maps to** | FR-06-09 |
| **Deliverable (code paths)** | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py`<br>`backend/app/api/v1/routes/governance.py`<br>`backend/app/services/governance_service.py`<br>`backend/app/domain/governance/policy_engine.py`<br>`backend/app/domain/governance/risk.py`<br>`backend/app/domain/governance/models.py` |
| **Test-first** | Cross-org get behaviour documented/tested. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safe 403/404 policy. |
| **Acceptance** | Safe 403/404 policy. |
| **Evidence** | route handlers |

### [x] T-06-06 — ABAC extension points (org/risk)
| | |
|--|--|
| **Priority** | P2 |
| **Status** | [x] Implemented |
| **Design** | D-06-01 future |
| **Maps to** | FR-06-08 |
| **Deliverable (code paths)** | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Hooks/comments for ABAC. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Upgrade path without rewrite. |
| **Acceptance** | Upgrade path without rewrite. |
| **Evidence** | permissions design |

### [x] T-06-07 — Block privilege self-escalation
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-06-04 |
| **Maps to** | NFR-06-04 |
| **Deliverable (code paths)** | `users/settings routes`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Non-owner cannot assign Owner. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Escalation closed. |
| **Acceptance** | Escalation closed. |
| **Evidence** | users/settings routes |

### [x] T-06-08 — Exit review — RBAC complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-06-01, AC-06-02, AC-06-03, AC-06-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-06-09 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-06-01, NFR-06-02 |
| **Deliverable (code paths)** | `requirements.md`<br>`06_authorization-and-rbac/tasks.md RTM`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=2 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 06_authorization-and-rbac/tasks.md RTM |

### [x] T-06-10 — Implement/verify all design components C-*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-06-3, C-06-1, C-06-2, C-06-3 |
| **Maps to** | AC-06-01, AC-06-02, AC-06-03 |
| **Deliverable (code paths)** | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Component module import/smoke or route presence. |
| **Steps** | 1) Map each C-* to module path in design. 2) Verify module exists and is wired. 3) Add smoke test if missing. |
| **Success** | All design components have implementation anchors. |
| **Acceptance** | Components covered: C-06-1, C-06-2, C-06-3 |
| **Evidence** | ### 3.1 Components |

### [x] T-06-11 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-06-01, D-06-02, D-06-03 |
| **Maps to** | FR-06-01, FR-06-02, NFR-06-01, AC-06-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-06-12 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-06-01, AC-06-02, AC-06-03, AC-06-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-06-13 — Exit review — BE-06 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-06-01, FR-06-02, FR-06-03, FR-06-04, FR-06-05, FR-06-06, FR-06-07, FR-06-08, FR-06-09, FR-06-10, NFR-06-01, NFR-06-02, NFR-06-03, NFR-06-04, AC-06-01, AC-06-02, AC-06-03, AC-06-04 |
| **Deliverable (code paths)** | `planning/backend/06_authorization-and-rbac/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/06_authorization-and-rbac/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-06-01` | FR-06-01, FR-06-04, FR-06-05, FR-06-06, FR-06-07 | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| `T-06-02` | FR-06-02, AC-06-01, AC-06-02, AC-06-03 | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| `T-06-03` | FR-06-03, NFR-06-03, AC-06-04 | `api/dependencies.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| `T-06-04` | FR-06-10 | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py`<br>`backend/app/api/v1/routes/auth.py`<br>… +4 more |
| `T-06-05` | FR-06-09 | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py`<br>`backend/app/api/v1/routes/governance.py`<br>… +4 more |
| `T-06-06` | FR-06-08 | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| `T-06-07` | NFR-06-04 | `users/settings routes`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| `T-06-08` | AC-06-01, AC-06-02, AC-06-03, AC-06-04 | `tasks.md`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| `T-06-09` | NFR-06-01, NFR-06-02 | `requirements.md`<br>`06_authorization-and-rbac/tasks.md RTM`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +1 more |
| `T-06-10` | AC-06-01, AC-06-02, AC-06-03 | `backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| `T-06-11` | FR-06-01, FR-06-02, NFR-06-01, AC-06-01 | `backend/app`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| `T-06-12` | AC-06-01, AC-06-02, AC-06-03, AC-06-04 | `backend/app/tests`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_hardening.py` |
| `T-06-13` | FR-06-01, FR-06-02, FR-06-03, FR-06-04, FR-06-05, FR-06-06, FR-06-07, FR-06-08, … | `planning/backend/06_authorization-and-rbac/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>… +1 more |

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
