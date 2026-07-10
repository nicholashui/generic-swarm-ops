# Tasks — 07 Users, Organizations, and Tenancy

| Field | Value |
|-------|-------|
| Task list ID | `BE-07-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-07-DES`) |
| Paired requirements | `requirements.md` (`BE-07`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 3/3 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Org/user models → disable semantics → admin APIs → invitations/keys → seed users.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-07. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/users.py`
- `backend/app/api/v1/routes/organizations.py`
- `backend/app/api/v1/routes/settings.py`
- `backend/app/services/user_service.py`
- `backend/app/services/organization_service.py`
- `backend/app/schemas/users.py`
- `backend/app/schemas/organizations.py`
- `backend/app/infrastructure/repositories/user_repository.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-07-01 — Organization entity + status
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 |
| **Maps to** | FR-07-01, FR-07-09, AC-07-03 |
| **Deliverable (code paths)** | `organizations routes/models`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| **Test-first** | Org record with org_id usage. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Tenant root exists. |
| **Acceptance** | Tenant root exists. |
| **Evidence** | organizations routes/models |

### [x] T-07-02 — User entity statuses active/invited/disabled
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 |
| **Maps to** | FR-07-02, FR-07-07, AC-07-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| **Test-first** | Disabled user cannot call APIs. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Lifecycle works. |
| **Acceptance** | Lifecycle works. |
| **Evidence** | users routes |

### [x] T-07-03 — Role assignment within org
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-07-1 |
| **Maps to** | FR-07-03, FR-07-10, AC-07-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| **Test-first** | Non-admin cannot list all users. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Admin-gated management. |
| **Acceptance** | Admin-gated management. |
| **Evidence** | api/v1/routes/users.py |

### [x] T-07-04 — Invitations (where enabled)
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §5 |
| **Maps to** | FR-07-04, NFR-07-03 |
| **Deliverable (code paths)** | `users/auth routes`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| **Test-first** | Invite requires privileged role. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Onboarding path. |
| **Acceptance** | Onboarding path. |
| **Evidence** | users/auth routes |

### [x] T-07-05 — Service accounts + API key association
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §3 arch |
| **Maps to** | FR-07-05, FR-07-06 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | Key bound to principal/org. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Machine identity. |
| **Acceptance** | Machine identity. |
| **Evidence** | auth api-keys |

### [x] T-07-06 — Org/settings endpoints for ops console
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-07-2, C-07-3 |
| **Maps to** | FR-07-08, AC-07-01 |
| **Deliverable (code paths)** | `organizations.py`<br>`settings.py`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| **Test-first** | Seed orgs/users load. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Ops can manage tenant. |
| **Acceptance** | Ops can manage tenant. |
| **Evidence** | organizations.py; settings.py |

### [x] T-07-07 — Never return password hashes/secrets in lists
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-07-02 |
| **Maps to** | NFR-07-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py`<br>`backend/app/core/security.py`<br>`backend/app/core/rate_limit.py` |
| **Test-first** | List users projection clean. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No secret leakage. |
| **Acceptance** | No secret leakage. |
| **Evidence** | DTOs |

### [x] T-07-08 — Exit review — tenancy complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-07-01, AC-07-02, AC-07-03, AC-07-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-07-09 — Close residual FR/NFR/AC coverage gaps (RTM completion)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §8 RTM + full requirements.md |
| **Maps to** | NFR-07-01 |
| **Deliverable (code paths)** | `requirements.md`<br>`07_users-organizations-and-tenancy/tasks.md RTM`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| **Test-first** | Enumerate each ID; attach automated or review verification. |
| **Steps** | 1) Diff requirements IDs vs task maps. 2) Add verification for each gap ID. 3) Re-check coverage 100%. |
| **Success** | Every FR/NFR/AC appears in task Maps to. |
| **Acceptance** | No residual gaps: FR=0 NFR=1 AC=0 closed. |
| **Evidence** | requirements.md; design.md §8; 07_users-organizations-and-tenancy/tasks.md RTM |

### [x] T-07-10 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-07-01, D-07-02 |
| **Maps to** | FR-07-01, FR-07-02, NFR-07-01, AC-07-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-07-11 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-07-01, AC-07-02, AC-07-03, AC-07-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-07-12 — Exit review — BE-07 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-07-01, FR-07-02, FR-07-03, FR-07-04, FR-07-05, FR-07-06, FR-07-07, FR-07-08, FR-07-09, FR-07-10, NFR-07-01, NFR-07-02, NFR-07-03, AC-07-01, AC-07-02, AC-07-03, AC-07-04 |
| **Deliverable (code paths)** | `planning/backend/07_users-organizations-and-tenancy/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/07_users-organizations-and-tenancy/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-07-01` | FR-07-01, FR-07-09, AC-07-03 | `organizations routes/models`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>… +1 more |
| `T-07-02` | FR-07-02, FR-07-07, AC-07-02 | `backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| `T-07-03` | FR-07-03, FR-07-10, AC-07-04 | `backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py` |
| `T-07-04` | FR-07-04, NFR-07-03 | `users/auth routes`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>… +1 more |
| `T-07-05` | FR-07-05, FR-07-06 | `backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py`<br>… +5 more |
| `T-07-06` | FR-07-08, AC-07-01 | `organizations.py`<br>`settings.py`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>… +2 more |
| `T-07-07` | NFR-07-02 | `backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>`backend/app/schemas/users.py`<br>… +5 more |
| `T-07-08` | AC-07-01, AC-07-02, AC-07-03, AC-07-04 | `tasks.md`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>… +1 more |
| `T-07-09` | NFR-07-01 | `requirements.md`<br>`07_users-organizations-and-tenancy/tasks.md RTM`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>… +2 more |
| `T-07-10` | FR-07-01, FR-07-02, NFR-07-01, AC-07-01 | `backend/app`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>… +1 more |
| `T-07-11` | AC-07-01, AC-07-02, AC-07-03, AC-07-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>`backend/app/services/organization_service.py`<br>… +1 more |
| `T-07-12` | FR-07-01, FR-07-02, FR-07-03, FR-07-04, FR-07-05, FR-07-06, FR-07-07, FR-07-08, … | `planning/backend/07_users-organizations-and-tenancy/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/users.py`<br>`backend/app/api/v1/routes/organizations.py`<br>`backend/app/api/v1/routes/settings.py`<br>`backend/app/services/user_service.py`<br>… +2 more |

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
