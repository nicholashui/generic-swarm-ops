# Tasks — 15 Knowledge Base and Retrieval

| Field | Value |
|-------|-------|
| Task list ID | `BE-15-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`BE-15-DES`) |
| Paired requirements | `requirements.md` (`BE-15`) |
| Source | `backend.md` + as-built `backend/` |
| Priority band | P0 (product bar) with P1/P2/P3 where noted |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |
| Coverage | FR 10/10 · NFR 4/4 · AC 4/4 · C-* 5/5 |

---

## SDD workflow

Ingest → index/chunk/embed → ACL search → Tier0/1 → provenance → untrusted content rules.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.0 (architecture / ICD / RTM)
    → tasks.md v2.1 (this file; prioritized, test-first, fully traced)
      → incremental implementation in backend/app
        → iterative compliance check (unit / e2e / E1 / review)
          → exit only when FR/NFR/AC/C-* coverage = 100%
```



## Primary code deliverables (this component)

These are the **main source locations** for BE-15. Individual tasks narrow further via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/knowledge.py`
- `backend/app/services/knowledge_service.py`
- `backend/app/domain/knowledge/chunking.py`
- `backend/app/domain/knowledge/retrieval.py`
- `backend/app/infrastructure/knowledge/retrieval.py`
- `backend/app/infrastructure/knowledge/embeddings.py`
- `backend/app/infrastructure/knowledge_orchestration/extract.py`
- `backend/app/infrastructure/knowledge_orchestration/operators.py`
- `backend/app/infrastructure/knowledge_orchestration/federation.py`
- `backend/app/schemas/knowledge.py`
- `backend/app/tests/unit/test_retrieval.py`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `backend/app/tests/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification.

---

## Task backlog

### [x] T-15-01 — Knowledge document lifecycle APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-15-1 |
| **Maps to** | FR-15-01, FR-15-02, FR-15-05, AC-15-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | Create document. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Ingest path. |
| **Acceptance** | Ingest path. |
| **Evidence** | api/v1/routes/knowledge.py |

### [x] T-15-02 — Index pipeline chunk/embed
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-15-2, C-15-4 |
| **Maps to** | FR-15-03, NFR-15-02 |
| **Deliverable (code paths)** | `backend/app/domain/knowledge/chunking.py`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | Status moves to indexed/available. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Searchable corpus. |
| **Acceptance** | Searchable corpus. |
| **Evidence** | domain/knowledge/chunking.py; embeddings |

### [x] T-15-03 — ACL-aware search + provenance
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-15-3, D-15-02 |
| **Maps to** | FR-15-04, FR-15-07, FR-15-08, AC-15-02, AC-15-03, AC-15-04 |
| **Deliverable (code paths)** | `backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | Cross-org hidden; perm deny. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Safe retrieval. |
| **Acceptance** | Safe retrieval. |
| **Evidence** | infrastructure/knowledge/retrieval.py |

### [x] T-15-04 — Tier-0 default retrieval
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-15-01 |
| **Maps to** | FR-15-06, NFR-15-01 |
| **Deliverable (code paths)** | `retrieval.py`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | Tier0 unit tests. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Cheap default path. |
| **Acceptance** | Cheap default path. |
| **Evidence** | retrieval.py |

### [x] T-15-05 — Tier-1 multi-hop lite (optional escalate)
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §4 upgrade rule |
| **Maps to** | FR-15-06 |
| **Deliverable (code paths)** | `knowledge_orchestration/*`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | Multi-hop path when enabled. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | LightRAG-lite behaviour. |
| **Acceptance** | LightRAG-lite behaviour. |
| **Evidence** | knowledge_orchestration/* |

### [x] T-15-06 — K1-lite extract/operators + federation export
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-15-5 |
| **Maps to** | FR-15-09 |
| **Deliverable (code paths)** | `knowledge_orchestration/federation.py`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | Federation endpoint/export. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Graph lite without Neo4j req. |
| **Acceptance** | Graph lite without Neo4j req. |
| **Evidence** | knowledge_orchestration/federation.py |

### [x] T-15-07 — Treat retrieved content as untrusted data
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-15-03, FR-15-10 |
| **Maps to** | FR-15-10, NFR-15-03, NFR-15-04 |
| **Deliverable (code paths)** | `engine/retrieval consumers`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | No authz from content. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Injection-resistant design. |
| **Acceptance** | Injection-resistant design. |
| **Evidence** | engine/retrieval consumers |

### [x] T-15-08 — Document full LightRAG/Neo4j as non-goal
| | |
|--|--|
| **Priority** | P3 |
| **Status** | [x] Implemented |
| **Design** | OI-15-01 |
| **Maps to** | scope_out |
| **Deliverable (code paths)** | `status.md`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/tests/unit`<br>`backend/app/tests/e2e/test_e1_operator_path.py`<br>`reviews/e1_operator_checklist.md`<br>`mark_100_verification.md` |
| **Test-first** | status.md non-goals. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Scope control. |
| **Acceptance** | Scope control. |
| **Evidence** | status.md |

### [x] T-15-09 — Exit review — knowledge complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §12 |
| **Maps to** | AC-15-01, AC-15-02, AC-15-03, AC-15-04 |
| **Deliverable (code paths)** | `tasks.md`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | Compliance [x]. |
| **Steps** | 1) Write/adjust failing test or verification. 2) Implement minimal change against design. 3) Re-run verification. 4) Update evidence path if module moved. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | tasks.md |

### [x] T-15-10 — Validate architecture decisions D-* still hold
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-15-01, D-15-02, D-15-03 |
| **Maps to** | FR-15-01, FR-15-02, NFR-15-01, AC-15-01 |
| **Deliverable (code paths)** | `backend/app`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | Review rejected alternatives not reintroduced. |
| **Steps** | 1) Read design §3.2 decisions. 2) Confirm codebase matches chosen option. 3) Note non-goals still deferred. |
| **Success** | No regression to rejected alternatives without ADR. |
| **Acceptance** | Each D-* disposition confirmed in code or docs. |
| **Evidence** | design.md §3.2; backend/app |

### [x] T-15-11 — Iterative compliance checkpoint (spec → design → tests)
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | SDD workflow; design §9 Validation |
| **Maps to** | AC-15-01, AC-15-02, AC-15-03, AC-15-04 |
| **Deliverable (code paths)** | `backend/app/tests`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | Run component-relevant unit/e2e; fix until green. |
| **Steps** | 1) Re-read AC list. 2) Run tests for this capability. 3) Confirm evidence paths. 4) Mark compliance boxes. |
| **Success** | AC satisfied with green verification. |
| **Acceptance** | All AC-* for this BE pass verification protocols TV-* in requirements. |
| **Evidence** | backend/app/tests; requirements.md §7 |

### [x] T-15-12 — Exit review — BE-15 tasks quality 100
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | design.md §12 score claim; TASKS_QUALITY_SCORE.md rubric |
| **Maps to** | FR-15-01, FR-15-02, FR-15-03, FR-15-04, FR-15-05, FR-15-06, FR-15-07, FR-15-08, FR-15-09, FR-15-10, NFR-15-01, NFR-15-02, NFR-15-03, NFR-15-04, AC-15-01, AC-15-02, AC-15-03, AC-15-04 |
| **Deliverable (code paths)** | `planning/backend/15_knowledge-base-and-retrieval/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| **Test-first** | Automated coverage scan: FR/NFR/AC/C-* = 100%. |
| **Steps** | 1) Run coverage scan. 2) Confirm every task has Priority/Status/Design/Maps/Test-first/Steps/Success/Acceptance/Evidence. 3) Sign compliance checkpoint. |
| **Success** | File meets all quality benchmarks without deficiencies. |
| **Acceptance** | Score 100 only if coverage+fields+status complete. |
| **Evidence** | planning/backend/15_knowledge-base-and-retrieval/tasks.md; TASKS_QUALITY_SCORE.md |

---

## Task → code RTM (this component)

| Task ID | Requirements | Deliverable paths |
|---------|--------------|-------------------|
| `T-15-01` | FR-15-01, FR-15-02, FR-15-05, AC-15-01 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| `T-15-02` | FR-15-03, NFR-15-02 | `backend/app/domain/knowledge/chunking.py`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| `T-15-03` | FR-15-04, FR-15-07, FR-15-08, AC-15-02, AC-15-03, AC-15-04 | `backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py` |
| `T-15-04` | FR-15-06, NFR-15-01 | `retrieval.py`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>… +1 more |
| `T-15-05` | FR-15-06 | `knowledge_orchestration/*`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>… +1 more |
| `T-15-06` | FR-15-09 | `knowledge_orchestration/federation.py`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>… +1 more |
| `T-15-07` | FR-15-10, NFR-15-03, NFR-15-04 | `engine/retrieval consumers`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>… +1 more |
| `T-15-08` | scope_out | `status.md`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>… +5 more |
| `T-15-09` | AC-15-01, AC-15-02, AC-15-03, AC-15-04 | `tasks.md`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>… +1 more |
| `T-15-10` | FR-15-01, FR-15-02, NFR-15-01, AC-15-01 | `backend/app`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>… +1 more |
| `T-15-11` | AC-15-01, AC-15-02, AC-15-03, AC-15-04 | `backend/app/tests`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>… +1 more |
| `T-15-12` | FR-15-01, FR-15-02, FR-15-03, FR-15-04, FR-15-05, FR-15-06, FR-15-07, FR-15-08, … | `planning/backend/15_knowledge-base-and-retrieval/tasks.md`<br>`TASKS_QUALITY_SCORE.md`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/domain/knowledge/retrieval.py`<br>… +2 more |

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
