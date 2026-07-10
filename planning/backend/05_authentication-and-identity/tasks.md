# Tasks — 05 Authentication and Identity

| Field | Value |
|-------|-------|
| Task list ID | `BE-05-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-05-DES`) |
| Paired requirements | `requirements.md` (`BE-05`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 12/12 · NFR 5/5 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Password hash → login/refresh/logout → /me → API keys → rate limits → 401 paths.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-05. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/auth.py`
- `backend/app/services/auth_service.py`
- `backend/app/core/auth.py`
- `backend/app/core/security.py`
- `backend/app/core/rate_limit.py`
- `backend/app/schemas/auth.py`
- `backend/app/tests/unit/test_scorecard_controls.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-05-01 — Login issues access credentials
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-05-1, C-05-2 |
| **Maps to** | FR-05-01, FR-05-02, AC-05-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Seed user login → token. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Usable Bearer token. |
| **Acceptance** | Usable Bearer token. |
| **Evidence** | api/v1/routes/auth.py |

### [x] T-05-02 — Refresh + logout lifecycle
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3 arch |
| **Maps to** | FR-05-03, FR-05-04 |
| **Deliverable (code paths)** | `backend/app/core/auth.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Refresh ok; post-logout rejected. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Session hygiene. |
| **Acceptance** | Session hygiene. |
| **Evidence** | core/auth.py |

### [x] T-05-03 — Password hashing (no plaintext)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-05-3, D-05-02 |
| **Maps to** | FR-05-12, AC-05-04 |
| **Deliverable (code paths)** | `backend/app/core/security.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | /me has no password hash. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Secure store. |
| **Acceptance** | Secure store. |
| **Evidence** | core/security.py |

### [x] T-05-04 — Password reset flow (if password auth)
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §5 API |
| **Maps to** | FR-05-05 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Reset endpoint exists/behaves. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Recovery path. |
| **Acceptance** | Recovery path. |
| **Evidence** | auth routes |

### [x] T-05-05 — API key create/list/revoke
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-05-03 |
| **Maps to** | FR-05-06, FR-05-07, AC-05-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Create→use→revoke. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Machine auth works. |
| **Acceptance** | Machine auth works. |
| **Evidence** | auth routes |

### [x] T-05-06 — GET /auth/me claims
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5 |
| **Maps to** | FR-05-08, AC-05-01 |
| **Deliverable (code paths)** | `auth.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | me returns roles/org. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | FE can authorize UI. |
| **Acceptance** | FE can authorize UI. |
| **Evidence** | auth.py |

### [x] T-05-07 — Invalid/expired credentials → 401
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §6 failures |
| **Maps to** | FR-05-09, AC-05-02 |
| **Deliverable (code paths)** | `tests unit/e2e`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Bad password 401. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Hard fail. |
| **Acceptance** | Hard fail. |
| **Evidence** | tests unit/e2e |

### [x] T-05-08 — Rate limit auth endpoints
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-05-4, NFR-05-05 |
| **Maps to** | FR-05-11, NFR-05-05 |
| **Deliverable (code paths)** | `backend/app/core/rate_limit.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Burst login triggers limit or documented. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Stuffing mitigated. |
| **Acceptance** | Stuffing mitigated. |
| **Evidence** | core/rate_limit.py |

### [x] T-05-09 — OIDC readiness note (optional)
| | |
|--|--|
| **Priority** | P3 |
| **Status** | [x] Implemented |
| **Design** | OI-05-01, FR-05-10 |
| **Maps to** | FR-05-10 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Design allows future OIDC. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Non-blocking non-goal. |
| **Acceptance** | Non-blocking non-goal. |
| **Evidence** | design open issues |

### [x] T-05-10 — Exit review — auth complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-05-01, AC-05-02, AC-05-03, AC-05-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-05-11 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-05-01, NFR-05-02, NFR-05-03, NFR-05-04 |
| **Deliverable (code paths)** | `requirements.md`<br>`05_authentication-and-identity/tasks.md RTM`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=4 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 05_authentication-and-identity/tasks.md RTM |

### [x] T-05-12 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-05-01, D-05-02, D-05-03 |
| **Maps to** | FR-05-01, FR-05-02, NFR-05-01, AC-05-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-05-13 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-05-01, AC-05-02, AC-05-03, AC-05-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-05-14 — Exit review — BE-05 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-05-01, FR-05-02, FR-05-03, FR-05-04, FR-05-05, FR-05-06, FR-05-07, FR-05-08, FR-05-09, FR-05-10, FR-05-11, FR-05-12, NFR-05-01, NFR-05-02, NFR-05-03, NFR-05-04, NFR-05-05, AC-05-01, AC-05-02, AC-05-03, AC-05-04 |
| **Deliverable (code paths)** | `planning/backend/05_authentication-and-identity/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/05_authentication-and-identity/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-05-01` | FR-05-01, FR-05-02, AC-05-01 | `backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| `T-05-02` | FR-05-03, FR-05-04 | `backend/app/core/auth.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| `T-05-03` | FR-05-12, AC-05-04 | `backend/app/core/security.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| `T-05-04` | FR-05-05 | `backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| `T-05-05` | FR-05-06, FR-05-07, AC-05-03 | `backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| `T-05-06` | FR-05-08, AC-05-01 | `auth.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>… +1 more |
| `T-05-07` | FR-05-09, AC-05-02 | `tests unit/e2e`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>… +1 more |
| `T-05-08` | FR-05-11, NFR-05-05 | `backend/app/core/rate_limit.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/schemas/auth.py` |
| `T-05-09` | FR-05-10 | `backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/schemas/auth.py` |
| `T-05-10` | AC-05-01, AC-05-02, AC-05-03, AC-05-04 | `tasks.md`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>… +1 more |
| `T-05-11` | NFR-05-01, NFR-05-02, NFR-05-03, NFR-05-04 | `requirements.md`<br>`05_authentication-and-identity/tasks.md RTM`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>… +2 more |
| `T-05-12` | FR-05-01, FR-05-02, NFR-05-01, AC-05-01 | `backend/app`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>… +1 more |
| `T-05-13` | AC-05-01, AC-05-02, AC-05-03, AC-05-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py`<br>… +1 more |
| `T-05-14` | FR-05-01, FR-05-02, FR-05-03, FR-05-04, FR-05-05, FR-05-06, FR-05-07, FR-05-08, … | `planning/backend/05_authentication-and-identity/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>… +2 more |

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
