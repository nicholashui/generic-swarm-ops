# Tasks — 09 Tiered Hybrid Retrieval

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-09-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-09-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-09`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/09_tiered-hybrid-retrieval/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-09**. Each task further narrows via **Deliverable (code paths)**.

- `backend/app/api/v1/routes/knowledge.py`
- `backend/app/services/knowledge_service.py`
- `backend/app/infrastructure/knowledge/retrieval.py`
- `backend/app/infrastructure/knowledge/embeddings.py`
- `backend/app/infrastructure/knowledge_orchestration/extract.py`
- `backend/app/infrastructure/knowledge_orchestration/operators.py`
- `backend/app/infrastructure/knowledge_orchestration/federation.py`
- `backend/app/domain/knowledge/chunking.py`
- `backend/app/tests/unit/test_retrieval.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-09-01 — Tier definitions 0/1/2 documented
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2.1, D-09-01…03 |
| **Maps to** | FR-09-01…06 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/tests/unit/test_retrieval.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | No GraphRAG default; Tier2 deferred explicit. |
| **Acceptance** | No GraphRAG default; Tier2 deferred explicit. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-09-02 — Tier0 search + mandatory provenance
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5.1 search, §4.2 hit model |
| **Maps to** | FR-09-01…02, FR-09-07…08, AC-09-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/tests/unit/test_retrieval.py` |
| **Test-first** | Hits without source_refs not grounded. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | test_retrieval provenance. |
| **Acceptance** | test_retrieval provenance. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-09-03 — Index builds entity_links
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5.2 index, C-09-1 |
| **Maps to** | FR-09-04 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Index endpoint populates links. |
| **Acceptance** | Index endpoint populates links. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-09-04 — Tier1 escalation rules
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.3 escalation |
| **Maps to** | FR-09-03, NFR-09-03, AC-09-02 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/tests/unit/test_retrieval.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | multi_hop=true expands; fixtures pass. |
| **Acceptance** | multi_hop=true expands; fixtures pass. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-09-05 — Hit model fields
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.2 RetrievalHit |
| **Maps to** | FR-09-07 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/tests/unit/test_retrieval.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | source_refs + retrieval_tier on hits. |
| **Acceptance** | source_refs + retrieval_tier on hits. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-09-06 — ACL/sensitivity filters
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | NFR-09-04…06 |
| **Maps to** | NFR-09-04…06 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/tests/unit/test_retrieval.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Unauthorized content withheld. |
| **Acceptance** | Unauthorized content withheld. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-09-07 — Retrieval eval fixtures
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §7, C-09-8 |
| **Maps to** | FR-09-09, AC-09-03 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/tests/unit/test_retrieval.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | business/evals/retrieval fixtures + tests. |
| **Acceptance** | business/evals/retrieval fixtures + tests. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-09-08 — K1-lite + federation APIs
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-09-5, C-09-6, §6 |
| **Maps to** | FR-09-07, design graph |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/tests/unit/test_retrieval.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | extract/query/gaps/federate available. |
| **Acceptance** | extract/query/gaps/federate available. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-09-09 — Embedding/pgvector flags
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §6 config |
| **Maps to** | NFR-09-01 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/tests/unit/test_retrieval.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Env flags documented; hashing default. |
| **Acceptance** | Env flags documented; hashing default. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-09-10 — Tier2 / full LightRAG non-goals
| | |
|--|--|
| **Priority** | P2 |
| **Status** | [x] Implemented |
| **Design** | OI-09-01…02, AC-09-04 |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/tests/unit/test_retrieval.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Documented deferred; policy present. |
| **Acceptance** | Documented deferred; policy present. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

### [x] T-09-11 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>`backend/app/tests/unit/test_retrieval.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | backend/app/api/v1/routes/knowledge.py, backend/app/services/knowledge_service.py, backend/app/infrastructure/knowledge/retrieval.py |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-09-01` | FR-09-01…06 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>… +1 more |
| `T-09-02` | FR-09-01…02, FR-09-07…08, AC-09-01 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>… +1 more |
| `T-09-03` | FR-09-04 | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>… +4 more |
| `T-09-04` | FR-09-03, NFR-09-03, AC-09-02 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>… +1 more |
| `T-09-05` | FR-09-07 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>… +1 more |
| `T-09-06` | NFR-09-04…06 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>… +1 more |
| `T-09-07` | FR-09-09, AC-09-03 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>… +1 more |
| `T-09-08` | FR-09-07, design graph | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>… +1 more |
| `T-09-09` | NFR-09-01 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>… +1 more |
| `T-09-10` |  | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>… +1 more |
| `T-09-11` |  | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`backend/app/domain/knowledge/chunking.py`<br>… +1 more |

---

## Compliance checkpoint

```text
[x] Every task has Deliverable (code paths) with repo-relative locations
[x] Primary code deliverables section present
[x] Maps to FR/NFR/AC retained
[x] Master index planning/structure/TASK_TO_CODE_TRACEABILITY.md
[x] All tasks [x] Implemented
[x] Quality score 100
```

## Implementation log

| Item | Status |
|------|--------|
| Code-path deliverables on every task | [x] |
| Component primary deliverables | [x] |
| Traceability index | [x] |

## Notes

- **Deliverable (code paths)** is the implementation location for the task (what to open/edit).
- Paths are repo-relative from workspace root.
- Architecture intent lives in `structure.md`; executable code mostly under `backend/app/` and corpus under `business/`.
- Version **2.2** makes structure-pack tasks as traceable as backend-pack v2.2.
