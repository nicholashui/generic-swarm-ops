# Tasks — 01 Platform Charter, Boundaries, and Design Principles

| Field | Value |
|-------|-------|
| Task list ID | `BE-01-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-01-DES`) |
| Paired requirements | `requirements.md` (`BE-01`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 14/14 · NFR 4/4 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Charter invariants → priority lattice → boundary checks → handoff gates to BE-05/11/14/20/22.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-01. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/main.py`
- `backend/app/runtime.py`
- `backend/app/api/v1/router.py`
- `backend.md`
- `structure.md`
- `planning/backend/01_platform-charter-boundaries-and-principles/design.md`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-01-01 — Document charter invariants INV-01…05 in review checklist
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3 INV, D-01-01…03 |
| **Maps to** | FR-01-01, FR-01-02, FR-01-03, FR-01-04, AC-01-01 |
| **Deliverable (code paths)** | `planning/backend/01_*/design.md`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md`<br>`backend/app/api/v1/routes/evolution.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/tests/unit/test_scorecard_controls.py`<br>`backend/app/tests/unit/test_p3_pi_evolution.py` |
| **Test-first** | Charter review rejects thin-proxy proposals. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Checklist used in design reviews. |
| **Acceptance** | Checklist used in design reviews. |
| **Evidence** | backend.md §1–6; planning/backend/01_*/design.md |

### [x] T-01-02 — Encode design priority lattice Safety→…→Autonomy
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 priority table |
| **Maps to** | FR-01-05, FR-01-06, FR-01-07, NFR-01-01 |
| **Deliverable (code paths)** | `structure.md`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| **Test-first** | Trade-off table present; linked from BE-22/20. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Priorities non-bypassable by prompt-only features. |
| **Acceptance** | Priorities non-bypassable by prompt-only features. |
| **Evidence** | structure.md; design §4 |

### [x] T-01-03 — Enforce API-first / FE simplicity boundary
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-01-03, C-01-3 |
| **Maps to** | FR-01-08, FR-01-13 |
| **Deliverable (code paths)** | `backend/app/api`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| **Test-first** | No direct DB/LLM access from FE contracts. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | All ops via /api/v1. |
| **Acceptance** | All ops via /api/v1. |
| **Evidence** | backend/app/api; frontend client |

### [x] T-01-04 — Wire AuthN default-on for protected routes
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | INV-01, BE-05 handoff |
| **Maps to** | FR-01-09, NFR-01-03 |
| **Deliverable (code paths)** | `api/dependencies.py`<br>`backend/app/core/auth.py`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Unauthenticated protected route → 401. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Secure by default. |
| **Acceptance** | Secure by default. |
| **Evidence** | api/dependencies.py; core/auth.py |

### [x] T-01-05 — Require governance + HITL before irreversible actions
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | INV-02 |
| **Maps to** | FR-01-10 |
| **Deliverable (code paths)** | `backend/app/domain/workflows/engine.py`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/services/approval_service.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/schemas/approvals.py` |
| **Test-first** | High-risk path creates gate or deny. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No silent irreversible tool success. |
| **Acceptance** | No silent irreversible tool success. |
| **Evidence** | domain/workflows/engine.py; approvals |

### [x] T-01-06 — Mandate audit on important mutations
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | INV-03 |
| **Maps to** | FR-01-11 |
| **Deliverable (code paths)** | `backend/app/domain/audit/*`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/services/audit_service.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`backend/app/schemas/audit_logs.py` |
| **Test-first** | Sample mutation writes audit event. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Audit present for login/run/approve paths. |
| **Acceptance** | Audit present for login/run/approve paths. |
| **Evidence** | domain/audit/* |

### [x] T-01-07 — Long-running work non-blocking API pattern
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | INV-04 |
| **Maps to** | FR-01-12 |
| **Deliverable (code paths)** | `backend/app/runtime.py`<br>`backend/app/main.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| **Test-first** | Start run returns id without waiting full completion. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Async/continue execution path. |
| **Acceptance** | Async/continue execution path. |
| **Evidence** | workflow_runs routes; runtime.py |

### [x] T-01-08 — Forbid unattended production DNA mutation (charter)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | INV-05, NFR-01-04 |
| **Maps to** | FR-01-04, NFR-01-04, AC-01-04 |
| **Deliverable (code paths)** | `backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/tests/unit/test_structure_sdd_validators.py`<br>`business/fixtures/negative` |
| **Test-first** | Design/code review of evolution paths. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | sandbox_only + validators only promote path. |
| **Acceptance** | sandbox_only + validators only promote path. |
| **Evidence** | evolution routes; structure_validators |

### [x] T-01-09 — Capability domain map (auth…evolution…improve)
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §1 purpose FR-01-14 |
| **Maps to** | FR-01-14, AC-01-02 |
| **Deliverable (code paths)** | `planning/backend/README.md`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | README lists BE-01…24 order. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Downstream specs reference BE-01. |
| **Acceptance** | Downstream specs reference BE-01. |
| **Evidence** | planning/backend/README.md |

### [x] T-01-10 — Exit review — charter complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 score |
| **Maps to** | AC-01-01, AC-01-02, AC-01-03, AC-01-04 |
| **Deliverable (code paths)** | `backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| **Test-first** | Compliance checkpoint all [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Quality 100. |
| **Acceptance** | Quality 100. |
| **Evidence** | tasks.md compliance |

### [x] T-01-11 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-01-02 |
| **Deliverable (code paths)** | `requirements.md`<br>`01_platform-charter-boundaries-and-principles/tasks.md RTM`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=1 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 01_platform-charter-boundaries-and-principles/tasks.md RTM |

### [x] T-01-12 — Implement/verify all design components C-*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-01-1, C-01-2, C-01-1, C-01-2, C-01-3 |
| **Maps to** | AC-01-01, AC-01-02, AC-01-03 |
| **Deliverable (code paths)** | `backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| **Test-first** | Component module import/smoke or route presence. |
| **Steps** | 1) Map each C-* to module path in design. 2) Verify module exists and is wired. 3) Add smoke test if missing. |
| **Success** | All design components have implementation anchors. |
| **Acceptance** | Components covered: C-01-1, C-01-2, C-01-3 |
| **Evidence** | ### 3.1 Components |

### [x] T-01-13 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-01-01, D-01-02, D-01-03 |
| **Maps to** | FR-01-01, FR-01-02, NFR-01-01, AC-01-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-01-14 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-01-01, AC-01-02, AC-01-03, AC-01-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-01-15 — Exit review — BE-01 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-01-01, FR-01-02, FR-01-03, FR-01-04, FR-01-05, FR-01-06, FR-01-07, FR-01-08, FR-01-09, FR-01-10, FR-01-11, FR-01-12, FR-01-13, FR-01-14, NFR-01-01, NFR-01-02, NFR-01-03, NFR-01-04, AC-01-01, AC-01-02, AC-01-03, AC-01-04 |
| **Deliverable (code paths)** | `planning/backend/01_platform-charter-boundaries-and-principles/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/01_platform-charter-boundaries-and-principles/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-01-01` | FR-01-01, FR-01-02, FR-01-03, FR-01-04, AC-01-01 | `planning/backend/01_*/design.md`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>… +5 more |
| `T-01-02` | FR-01-05, FR-01-06, FR-01-07, NFR-01-01 | `structure.md`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| `T-01-03` | FR-01-08, FR-01-13 | `backend/app/api`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>… +1 more |
| `T-01-04` | FR-01-09, NFR-01-03 | `api/dependencies.py`<br>`backend/app/core/auth.py`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>… +6 more |
| `T-01-05` | FR-01-10 | `backend/app/domain/workflows/engine.py`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>… +6 more |
| `T-01-06` | FR-01-11 | `backend/app/domain/audit/*`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>… +6 more |
| `T-01-07` | FR-01-12 | `backend/app/runtime.py`<br>`backend/app/main.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| `T-01-08` | FR-01-04, NFR-01-04, AC-01-04 | `backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md`<br>… +4 more |
| `T-01-09` | FR-01-14, AC-01-02 | `planning/backend/README.md`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>… +6 more |
| `T-01-10` | AC-01-01, AC-01-02, AC-01-03, AC-01-04 | `backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| `T-01-11` | NFR-01-02 | `requirements.md`<br>`01_platform-charter-boundaries-and-principles/tasks.md RTM`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>… +2 more |
| `T-01-12` | AC-01-01, AC-01-02, AC-01-03 | `backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>`planning/backend/01_platform-charter-boundaries-and-principles/design.md` |
| `T-01-13` | FR-01-01, FR-01-02, NFR-01-01, AC-01-01 | `backend/app`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>… +1 more |
| `T-01-14` | AC-01-01, AC-01-02, AC-01-03, AC-01-04 | `backend/app/tests`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>`structure.md`<br>… +1 more |
| `T-01-15` | FR-01-01, FR-01-02, FR-01-03, FR-01-04, FR-01-05, FR-01-06, FR-01-07, FR-01-08, … | `planning/backend/01_platform-charter-boundaries-and-principles/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/main.py`<br>`backend/app/runtime.py`<br>`backend/app/api/v1/router.py`<br>`backend.md`<br>… +2 more |

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
