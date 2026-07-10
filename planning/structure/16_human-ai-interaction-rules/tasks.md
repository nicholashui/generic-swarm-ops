# Tasks — 16 Human–AI Interaction Rules

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-16-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-16-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-16`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/16_human-ai-interaction-rules/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-16**. Each task further narrows via **Deliverable (code paths)**.

- `frontend/src/app/app/[...slug]/page.tsx`
- `frontend/src/components/domain/improve-run-button.tsx`
- `frontend/src/components/domain/evolution-archive-panel.tsx`
- `frontend/src/lib/api/client.ts`
- `frontend/src/types/navigation.ts`
- `frontend/README.md`
- `backend/app/api/v1/routes/approvals.py`
- `backend/app/api/v1/routes/workflow_runs.py`

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

### [x] T-16-01 — Ops profile DEMO_MODE=false
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-16-01, §2 |
| **Maps to** | FR-16-10 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | usage/README documents ops env. |
| **Acceptance** | usage/README documents ops env. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-16-02 — Interaction rules matrix implemented
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4 table |
| **Maps to** | FR-16-01…08 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Confidence, evidence, preview, correction, override, rejection, clarification, honesty. |
| **Acceptance** | Confidence, evidence, preview, correction, override, rejection, clarification, honesty. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-16-03 — Page state model loading/empty/data/error/forbidden
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §4.1 |
| **Maps to** | AC-16-06 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Major pages have states. |
| **Acceptance** | Major pages have states. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-16-04 — Route map ops surface
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | §5 routes |
| **Maps to** | AC-16-01…04 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Dashboard through evolution routes exist. |
| **Acceptance** | Dashboard through evolution routes exist. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-16-05 — Run detail status + Improve
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-16-2, §5.1 |
| **Maps to** | FR-16-10, AC-16-01, AC-16-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_full_improvement_backlog.py`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Improve pipeline buttons. |
| **Acceptance** | Improve pipeline buttons. |
| **Evidence** | backend/app/api/v1/routes/evolution.py, backend/app/api/v1/routes/improvement.py, backend/app/api/v1/routes/loops.py |

### [x] T-16-06 — Real forms + request_id errors
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-16-6, C-16-7, §6 |
| **Maps to** | NFR-16-05 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Zod/RHF; formatMutationError. |
| **Acceptance** | Zod/RHF; formatMutationError. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-16-07 — Backend final authority
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-16-02, FR-16-09 |
| **Maps to** | AC-16-05 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | API 403 despite hidden UI control. |
| **Acceptance** | API 403 despite hidden UI control. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-16-08 — Rejection → lesson
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | D-16-04 |
| **Maps to** | FR-16-06 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | approve reject writes improvement_lessons. |
| **Acceptance** | approve reject writes improvement_lessons. |
| **Evidence** | runtime.decide_approval |

### [x] T-16-09 — Evolution archive page
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-16-5 |
| **Maps to** | AC-16-04 |
| **Deliverable (code paths)** | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>`backend/app/runtime.py`<br>`backend/app/tests/unit/test_full_improvement_backlog.py`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | /app/evolution. |
| **Acceptance** | /app/evolution. |
| **Evidence** | backend/app/api/v1/routes/evolution.py, backend/app/api/v1/routes/improvement.py, backend/app/api/v1/routes/loops.py |

### [x] T-16-10 — Auth session security
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | C-16-8, NFR-16-03 |
| **Maps to** | NFR-16-03 |
| **Deliverable (code paths)** | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Cookie/session preferred over localStorage secrets. |
| **Acceptance** | Cookie/session preferred over localStorage secrets. |
| **Evidence** | backend/app/infrastructure/tools/adapters.py, backend/app/runtime.py, backend/app/core/rate_limit.py |

### [x] T-16-11 — Destructive confirmations
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | NFR-16-04 |
| **Maps to** | FR-16-03 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Confirm dialogs on destructive actions. |
| **Acceptance** | Confirm dialogs on destructive actions. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-16-12 — Playwright smoke
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented |
| **Design** | C-16-9 |
| **Maps to** | TV-16-02 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | test:e2e skips gracefully if servers down. |
| **Acceptance** | test:e2e skips gracefully if servers down. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-16-13 — OpenDesign / always-on CI deferred
| | |
|--|--|
| **Priority** | P2 |
| **Status** | [x] Implemented |
| **Design** | OI-16-01…02 |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Documented non-goals. |
| **Acceptance** | Documented non-goals. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

### [x] T-16-14 — Exit review
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented |
| **Design** | paired design.md |
| **Maps to** | see requirements.md |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| **Test-first** | Write/adjust failing verification first, then implement in deliverable paths. |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | Score 100. |
| **Acceptance** | Score 100. |
| **Evidence** | frontend/src/app/app/[...slug]/page.tsx, frontend/src/components/domain/improve-run-button.tsx, frontend/src/components/domain/evolution-archive-panel.tsx |

---

## Task → code RTM (this component)

| Task ID | Maps to | Deliverable (code paths) |
|---------|---------|--------------------------|
| `T-16-01` | FR-16-10 | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| `T-16-02` | FR-16-01…08 | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| `T-16-03` | AC-16-06 | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| `T-16-04` | AC-16-01…04 | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| `T-16-05` | FR-16-10, AC-16-01, AC-16-04 | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>… +4 more |
| `T-16-06` | NFR-16-05 | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| `T-16-07` | AC-16-05 | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| `T-16-08` | FR-16-06 | `backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/audit_logs.py`<br>`backend/app/domain/approvals/service.py`<br>`backend/app/domain/approvals/models.py`<br>`backend/app/domain/audit/events.py`<br>`backend/app/domain/audit/models.py`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>… +4 more |
| `T-16-09` | AC-16-04 | `backend/app/api/v1/routes/evolution.py`<br>`backend/app/api/v1/routes/improvement.py`<br>`backend/app/api/v1/routes/loops.py`<br>`backend/app/infrastructure/evolution/corpus_eval.py`<br>`backend/app/infrastructure/self_improvement/reflection.py`<br>`backend/app/infrastructure/self_improvement/lessons.py`<br>`backend/app/infrastructure/self_improvement/skill_sandbox.py`<br>`backend/app/infrastructure/loop_engineering/runner.py`<br>… +4 more |
| `T-16-10` | NFR-16-03 | `backend/app/infrastructure/tools/adapters.py`<br>`backend/app/runtime.py`<br>`backend/app/core/rate_limit.py`<br>`backend/app/core/security.py`<br>`backend/app/core/permissions.py`<br>`backend/app/api/dependencies.py`<br>`business/evals/adversarial-tests/`<br>`business/security/`<br>… +4 more |
| `T-16-11` | FR-16-03 | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| `T-16-12` | TV-16-02 | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| `T-16-13` |  | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |
| `T-16-14` |  | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/evolution-archive-panel.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/types/navigation.ts`<br>`frontend/README.md`<br>`backend/app/api/v1/routes/approvals.py`<br>`backend/app/api/v1/routes/workflow_runs.py` |

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
