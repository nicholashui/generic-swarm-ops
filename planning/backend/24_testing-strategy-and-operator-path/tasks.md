# Tasks — 24 Testing Strategy and Operator Path

| Field | Value |
|-------|-------|
| Task list ID | `BE-24-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-24-DES`) |
| Paired requirements | `requirements.md` (`BE-24`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 9/9 · NFR 4/4 · AC 4/4 · C-* 4/4 |

---

## SDD workflow

Unit suite → integration → E1 e2e → security pack → DoD evidence → non-goals doc.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-24. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/tests/unit/`
- `backend/app/tests/e2e/test_e1_operator_path.py`
- `reviews/e1_operator_checklist.md`
- `status.md`
- `mark_100_verification.md`
- `backend/README.md`
- `planning/gap_analysis_for_backend.md`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-24-01 — Unit suite for domain critical logic
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-24-1, FR-24-01 |
| **Maps to** | FR-24-01, NFR-24-01, AC-24-01 |
| **Deliverable (code paths)** | `backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | unittest discover unit green. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Fast regression net. |
| **Acceptance** | Fast regression net. |
| **Evidence** | backend/app/tests/unit |

### [x] T-24-02 — Integration tests API+DB paths
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-24-02 |
| **Maps to** | FR-24-02 |
| **Deliverable (code paths)** | `backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | Key route integrations green. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Wired system confidence. |
| **Acceptance** | Wired system confidence. |
| **Evidence** | tests |

### [x] T-24-03 — E2E E1 operator path
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-24-3, D-24-01, FR-24-03, FR-24-07 |
| **Maps to** | FR-24-03, FR-24-07, NFR-24-02, AC-24-02 |
| **Deliverable (code paths)** | `backend/app/tests/e2e`<br>`reviews/e1_operator_checklist.md`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | test_e1_operator_path green. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | login→…→canary proven. |
| **Acceptance** | login→…→canary proven. |
| **Evidence** | app/tests/e2e; reviews/e1_operator_checklist.md |

### [x] T-24-04 — Security test pack
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-24-04, NFR-24-03 |
| **Maps to** | FR-24-04, NFR-24-03, NFR-24-04 |
| **Deliverable (code paths)** | `unit/security tests`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | Authz/cross-org/token negatives. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Security regressions caught. |
| **Acceptance** | Security regressions caught. |
| **Evidence** | unit/security tests |

### [x] T-24-05 — MVP capability checklist evidenced
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-24-05 |
| **Maps to** | FR-24-05 |
| **Deliverable (code paths)** | `backend/README`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | Map MVP items to modules/tests. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | MVP bar met. |
| **Acceptance** | MVP bar met. |
| **Evidence** | backend/README |

### [x] T-24-06 — Mark ~100 DoD items 21–26 evidenced
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | FR-24-06, AC-24-03 |
| **Maps to** | FR-24-06, AC-24-03 |
| **Deliverable (code paths)** | `status.md`<br>`mark_100_verification.md`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`backend/README.md` |
| **Test-first** | Postgres, tools, evolution, SI, DNA safety, E1. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Product bar closed. |
| **Acceptance** | Product bar closed. |
| **Evidence** | status.md; mark_100_verification.md |

### [x] T-24-07 — Document non-goals explicitly
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-24-02, FR-24-08 |
| **Maps to** | FR-24-08, AC-24-04 |
| **Deliverable (code paths)** | `backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | Non-goals in status/backend design. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Not tracked as defects. |
| **Acceptance** | Not tracked as defects. |
| **Evidence** | status.md § Remaining non-goals |

### [x] T-24-08 — Link evidence in status continuity docs
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-24-4, FR-24-09 |
| **Maps to** | FR-24-09 |
| **Deliverable (code paths)** | `status.md`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | status.md points to tests/reviews. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Auditable release. |
| **Acceptance** | Auditable release. |
| **Evidence** | status.md |

### [x] T-24-09 — Exit review — testing/operator path complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-24-01, AC-24-02, AC-24-03, AC-24-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-24-10 — Implement/verify all design components C-*
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-24-2, C-24-1, C-24-2, C-24-3 |
| **Maps to** | AC-24-01, AC-24-02, AC-24-03 |
| **Deliverable (code paths)** | `backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | Component module import/smoke or route presence. |
| **Steps** | 1) Map each C-* to module path in design. 2) Verify module exists and is wired. 3) Add smoke test if missing. |
| **Success** | All design components have implementation anchors. |
| **Acceptance** | Components covered: C-24-1, C-24-2, C-24-3, C-24-4 |
| **Evidence** | ### 3.1 Components |

### [x] T-24-11 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-24-01, D-24-02 |
| **Maps to** | FR-24-01, FR-24-02, NFR-24-01, AC-24-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-24-12 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-24-01, AC-24-02, AC-24-03, AC-24-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-24-13 — Exit review — BE-24 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-24-01, FR-24-02, FR-24-03, FR-24-04, FR-24-05, FR-24-06, FR-24-07, FR-24-08, FR-24-09, NFR-24-01, NFR-24-02, NFR-24-03, NFR-24-04, AC-24-01, AC-24-02, AC-24-03, AC-24-04 |
| **Deliverable (code paths)** | `planning/backend/24_testing-strategy-and-operator-path/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/24_testing-strategy-and-operator-path/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-24-01` | FR-24-01, NFR-24-01, AC-24-01 | `backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| `T-24-02` | FR-24-02 | `backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| `T-24-03` | FR-24-03, FR-24-07, NFR-24-02, AC-24-02 | `backend/app/tests/e2e`<br>`reviews/e1_operator_checklist.md`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`status.md`<br>`mark_100_verification.md`<br>… +1 more |
| `T-24-04` | FR-24-04, NFR-24-03, NFR-24-04 | `unit/security tests`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>… +1 more |
| `T-24-05` | FR-24-05 | `backend/README`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>… +1 more |
| `T-24-06` | FR-24-06, AC-24-03 | `status.md`<br>`mark_100_verification.md`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`backend/README.md` |
| `T-24-07` | FR-24-08, AC-24-04 | `backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| `T-24-08` | FR-24-09 | `status.md`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| `T-24-09` | AC-24-01, AC-24-02, AC-24-03, AC-24-04 | `tasks.md`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>… +1 more |
| `T-24-10` | AC-24-01, AC-24-02, AC-24-03 | `backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>`backend/README.md` |
| `T-24-11` | FR-24-01, FR-24-02, NFR-24-01, AC-24-01 | `backend/app`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>… +1 more |
| `T-24-12` | AC-24-01, AC-24-02, AC-24-03, AC-24-04 | `backend/app/tests`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>`mark_100_verification.md`<br>… +1 more |
| `T-24-13` | FR-24-01, FR-24-02, FR-24-03, FR-24-04, FR-24-05, FR-24-06, FR-24-07, FR-24-08, … | `planning/backend/24_testing-strategy-and-operator-path/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`status.md`<br>… +2 more |

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
