# Tasks — 23 Security Hardening and Cross-Cutting NFRs

| Field | Value |
|-------|-------|
| Task list ID | `BE-23-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-23-DES`) |
| Paired requirements | `requirements.md` (`BE-23`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 4/4 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Defaults authn/z → validation → rate limits → untrusted data → ACL → fail-closed.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-23. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/core/rate_limit.py`
- `backend/app/core/security.py`
- `backend/app/core/permissions.py`
- `backend/app/api/dependencies.py`
- `backend/app/api/errors.py`
- `backend/app/main.py`
- `backend/app/infrastructure/tools/adapters.py`
- `backend/app/tests/unit/test_hardening.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-23-01 — AuthN/AuthZ defaults on protected routes
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-23-3, §4 |
| **Maps to** | FR-23-01, AC-23-01 |
| **Deliverable (code paths)** | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py`<br>`backend/app/api/v1/routes/auth.py`<br>`backend/app/services/auth_service.py`<br>`backend/app/core/auth.py` |
| **Test-first** | No auth → 401. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Secure default. |
| **Acceptance** | Secure default. |
| **Evidence** | dependencies + permissions |

### [x] T-23-02 — Request validation + upload sanitization
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 |
| **Maps to** | FR-23-02, AC-23-03 |
| **Deliverable (code paths)** | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Invalid body 422; bad upload rejected. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Input hygiene. |
| **Acceptance** | Input hygiene. |
| **Evidence** | pydantic models; routes |

### [x] T-23-03 — Secrets only from env; never return secrets
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-23-04 |
| **Maps to** | FR-23-03, NFR-23-04 |
| **Deliverable (code paths)** | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Secret scan / review. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | No hardcoded secrets. |
| **Acceptance** | No hardcoded secrets. |
| **Evidence** | config; repo policy |

### [x] T-23-04 — Rate limit sensitive endpoints
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-23-1 |
| **Maps to** | FR-23-04, NFR-23-01, AC-23-02 |
| **Deliverable (code paths)** | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Auth/workflow write limited. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Abuse resistance. |
| **Acceptance** | Abuse resistance. |
| **Evidence** | core/rate_limit.py |

### [x] T-23-05 — Untrusted data handling (injection assumption)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-23-01, FR-23-05…06 |
| **Maps to** | FR-23-05, FR-23-06, AC-23-04 |
| **Deliverable (code paths)** | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Content cannot expand privileges. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Deterministic security outside LLM. |
| **Acceptance** | Deterministic security outside LLM. |
| **Evidence** | broker + retrieval |

### [x] T-23-06 — Org/department ACL data access
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-23-07 |
| **Maps to** | FR-23-07 |
| **Deliverable (code paths)** | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Cross-org deny tests. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Tenant safety. |
| **Acceptance** | Tenant safety. |
| **Evidence** | repositories filters |

### [x] T-23-07 — Reliability fail-closed + layered maintainability
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | FR-23-08…10, D-23-02 |
| **Maps to** | FR-23-08, FR-23-09, FR-23-10, NFR-23-02, NFR-23-03 |
| **Deliverable (code paths)** | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Adapter errors not success; headers present. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Ops-grade quality. |
| **Acceptance** | Ops-grade quality. |
| **Evidence** | adapters; main middleware |

### [x] T-23-08 — Exit review — hardening complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-23-01, AC-23-02, AC-23-03, AC-23-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-23-09 — Implement/verify all design components C-*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-23-2, C-23-4, C-23-1, C-23-2, C-23-3 |
| **Maps to** | AC-23-01, AC-23-02, AC-23-03 |
| **Deliverable (code paths)** | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Component module import/smoke or route presence. |
| **Steps** | 1) Map each C-* to module path in design. 2) Verify module exists and is wired. 3) Add smoke test if missing. |
| **Success** | All design components have implementation anchors. |
| **Acceptance** | Components covered: C-23-1, C-23-2, C-23-3, C-23-4 |
| **Evidence** | ### 3.1 Components |

### [x] T-23-10 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-23-01, D-23-02 |
| **Maps to** | FR-23-01, FR-23-02, NFR-23-01, AC-23-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-23-11 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-23-01, AC-23-02, AC-23-03, AC-23-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-23-12 — Exit review — BE-23 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-23-01, FR-23-02, FR-23-03, FR-23-04, FR-23-05, FR-23-06, FR-23-07, FR-23-08, FR-23-09, FR-23-10, NFR-23-01, NFR-23-02, NFR-23-03, NFR-23-04, AC-23-01, AC-23-02, AC-23-03, AC-23-04 |
| **Deliverable (code paths)** | `planning/backend/23_security-hardening-and-nfr/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/23_security-hardening-and-nfr/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-23-01` | FR-23-01, AC-23-01 | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py`<br>… +3 more |
| `T-23-02` | FR-23-02, AC-23-03 | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| `T-23-03` | FR-23-03, NFR-23-04 | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| `T-23-04` | FR-23-04, NFR-23-01, AC-23-02 | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| `T-23-05` | FR-23-05, FR-23-06, AC-23-04 | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| `T-23-06` | FR-23-07 | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| `T-23-07` | FR-23-08, FR-23-09, FR-23-10, NFR-23-02, NFR-23-03 | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| `T-23-08` | AC-23-01, AC-23-02, AC-23-03, AC-23-04 | `tasks.md`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>… +1 more |
| `T-23-09` | AC-23-01, AC-23-02, AC-23-03 | `backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>`backend/app/main.py` |
| `T-23-10` | FR-23-01, FR-23-02, NFR-23-01, AC-23-01 | `backend/app`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>… +1 more |
| `T-23-11` | AC-23-01, AC-23-02, AC-23-03, AC-23-04 | `backend/app/tests`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`backend/app/api/errors.py`<br>… +1 more |
| `T-23-12` | FR-23-01, FR-23-02, FR-23-03, FR-23-04, FR-23-05, FR-23-06, FR-23-07, FR-23-08, … | `planning/backend/23_security-hardening-and-nfr/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>… +2 more |

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
