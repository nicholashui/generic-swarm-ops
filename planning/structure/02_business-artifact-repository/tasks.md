# Tasks — 02 Business Artifact Repository

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-02-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-02-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-02`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/02_business-artifact-repository/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-02**. Each task further narrows via **Deliverable (code paths)**.

- `business/`
- `business/process-intelligence/`
- `business/knowledge-base/`
- `business/experts/`
- `business/materials/`
- `business/distilled/`
- `business/memory/`
- `business/evals/`
- `business/governance/`
- `business/security/`
- `business/evolution/`
- `package.json`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-02-01 — Ten domain roots + subfolders
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §3.1 tree, C-02-1 |
| **Maps to** | FR-02-01…11, AC-02-01, V-02-01 |
| **Deliverable (code paths)** | `business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/`<br>`business/memory/`<br>`business/evals/`<br>`business/governance/`<br>`business/security/`<br>`business/evolution/`<br>`package.json` |
| **Test-first** | Structural test lists required paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | `business:init` + paths exist. |
| **Acceptance** | `business:init` + paths exist. |
| **Evidence** | `business/**`, init-business.mjs |

### [x] T-02-02 — Dual-store SoT rules documented
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §2.1 data plane, D-02-01 |
| **Maps to** | NFR-02-02, design conflict rule |
| **Deliverable (code paths)** | `docs/architecture.md`<br>`business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/`<br>`business/memory/`<br>`business/evals/`<br>`business/governance/`<br>`business/security/`<br>`business/evolution/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | design §2.1 complete; architecture/status consistent. |
| **Acceptance** | design §2.1 complete; architecture/status consistent. |
| **Evidence** | design.md §2.1, docs/architecture.md |

### [x] T-02-03 — Schema registry + examples validate
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-02-5, V-02-02 |
| **Maps to** | FR-02-12, AC-02-03 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/` |
| **Test-first** | Invalid example must fail. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | validate failures: none. |
| **Acceptance** | validate failures: none. |
| **Evidence** | business:validate |

### [x] T-02-04 — Secret scan business/
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-02-3, V-02-03, §4.3 |
| **Maps to** | NFR-02-03…04, AC-02-04 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | business:security no critical secrets. |
| **Acceptance** | business:security no critical secrets. |
| **Evidence** | security-controls.mjs |

### [x] T-02-05 — Provenance on promotable artifacts
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | V-02-04, §4.1–4.2 |
| **Maps to** | FR-02-12 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Publish/promote blocked without source_refs (DNA/DRC validators). |
| **Acceptance** | Publish/promote blocked without source_refs (DNA/DRC validators). |
| **Evidence** | structure_validators, schemas |

### [x] T-02-06 — Sandbox quarantine for skills
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-02-6, D-02-03 |
| **Maps to** | FR-02-06 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_full_improvement_backlog.py`<br>`business/`<br>`business/process-intelligence/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Skills under distilled/skills/_sandbox until promote. |
| **Acceptance** | Skills under distilled/skills/_sandbox until promote. |
| **Evidence** | improvement skills API |

### [x] T-02-07 — Negative fixtures location
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | D-02-03, fixtures/ |
| **Maps to** | V-02-05 shared with 10 |
| **Deliverable (code paths)** | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | business/fixtures/negative/* present. |
| **Acceptance** | business/fixtures/negative/* present. |
| **Evidence** | dna-*.json, drc-*.json |

### [x] T-02-08 — Lifecycle draft→published
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | §4.2 lifecycle |
| **Maps to** | FR-02-12 |
| **Deliverable (code paths)** | `business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/`<br>`business/memory/`<br>`business/evals/`<br>`business/governance/`<br>`business/security/`<br>`business/evolution/`<br>`package.json` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Documented lifecycle; validators enforce publish rules. |
| **Acceptance** | Documented lifecycle; validators enforce publish rules. |
| **Evidence** | business/, business/process-intelligence/, business/knowledge-base/ |

### [x] T-02-09 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | AC-02-01…04 |
| **Deliverable (code paths)** | `business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/`<br>`business/memory/`<br>`business/evals/`<br>`business/governance/`<br>`business/security/`<br>`business/evolution/`<br>`package.json` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | All V-02-* covered; score 100. |
| **Acceptance** | All V-02-* covered; score 100. |
| **Evidence** | business/, business/process-intelligence/, business/knowledge-base/ |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-02-01` | FR-02-01…11, AC-02-01, V-02-01 | `business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/`<br>`business/memory/`<br>`business/evals/`<br>… +4 more |
| `T-02-02` | NFR-02-02, design conflict rule | `docs/architecture.md`<br>`business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/`<br>`business/memory/`<br>… +4 more |
| `T-02-03` | FR-02-12, AC-02-03 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/`<br>`business/process-intelligence/`<br>… +4 more |
| `T-02-04` | NFR-02-03…04, AC-02-04 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +4 more |
| `T-02-05` | FR-02-12 | `backend/app/api/v1/routes/knowledge.py`<br>`backend/app/services/knowledge_service.py`<br>`backend/app/infrastructure/knowledge/retrieval.py`<br>`backend/app/infrastructure/knowledge/embeddings.py`<br>`backend/app/infrastructure/knowledge_orchestration/extract.py`<br>`backend/app/infrastructure/knowledge_orchestration/operators.py`<br>`backend/app/infrastructure/knowledge_orchestration/federation.py`<br>`business/`<br>… +4 more |
| `T-02-06` | FR-02-06 | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>… +4 more |
| `T-02-07` | V-02-05 shared with 10 | `business/distilled/workflows/`<br>`backend/app/domain/workflows/models.py`<br>`backend/app/domain/workflows/policies.py`<br>`backend/app/api/v1/routes/workflows.py`<br>`backend/app/services/workflow_service.py`<br>`backend/app/infrastructure/governance/structure_validators.py`<br>`business/`<br>`business/process-intelligence/`<br>… +4 more |
| `T-02-08` | FR-02-12 | `business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/`<br>`business/memory/`<br>`business/evals/`<br>… +4 more |
| `T-02-09` | AC-02-01…04 | `business/`<br>`business/process-intelligence/`<br>`business/knowledge-base/`<br>`business/experts/`<br>`business/materials/`<br>`business/distilled/`<br>`business/memory/`<br>`business/evals/`<br>… +4 more |

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
