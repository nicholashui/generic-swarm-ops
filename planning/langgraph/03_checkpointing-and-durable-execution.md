# LG-03 — Checkpointing and Durable Execution

**Unit ID:** LG-03  
**Layer:** Backend  
**Priority:** P0  
**Depends on:** LG-01, LG-02  

---

## 1. Goal

Make multi-step orchestration **crash-safe and resumable** using LangGraph checkpointers, aligned with host Postgres—not only in-memory demo graphs.

---

## 2. Problem / gap

Runs live in a single `runtime_state` blob. Process crash mid-step loses fine-grained agent memory. Resume after approval re-enters a coarse function, not a true checkpoint.

LangGraph durable execution + checkpointers exist specifically for long-running agents and HITL.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-03-01 | Production engine uses **Postgres-backed** checkpointer when DB available. |
| FR-03-02 | Tests may use `MemorySaver`. |
| FR-03-03 | `thread_id` = stable function of `organization_id` + `run_id`. |
| FR-03-04 | Resume after process restart continues from last checkpoint. |
| FR-03-05 | Cancel marks thread cancelled and prevents further invokes. |
| FR-03-06 | Checkpoint metadata includes `run_id`, `workflow_id`, `engine`. |
| NFR-03-01 | Checkpoint tables/migrations documented; no secrets in checkpoint values. |
| NFR-03-02 | Tenant isolation: org A cannot resume org B thread_id. |

---

## 4. Design

### 4.1 Options

| Option | Use |
|--------|-----|
| `MemorySaver` | Unit tests only |
| `PostgresSaver` / langgraph-checkpoint-postgres | Local-prod + prod |
| Fallback | If no DB, file/sqlite checkpointer for dev only (flag) |

### 4.2 Thread ID scheme

```text
thread_id = f"{organization_id}:{run_id}"
```

### 4.3 Lifecycle

```text
start → compile graph → invoke(config={thread_id}) 
  → interrupt or complete → checkpoint stored
resume → update_state / Command(resume=...) → continue
crash → new process → same thread_id → continues
```

### 4.4 Modules

```text
backend/app/infrastructure/langgraph_engine/checkpointer.py
backend/app/infrastructure/langgraph_engine/thread_ids.py
backend/scripts or alembic: checkpoint DDL if required
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-03-01 | Add dependency for LangGraph + checkpointer package to `pyproject.toml` |
| T-03-02 | Factory `get_checkpointer()` from settings |
| T-03-03 | Wire compile/invoke with checkpointer in engine |
| T-03-04 | Restart durability test (kill mid-run mock) |
| T-03-05 | Tenant isolation negative test |
| T-03-06 | Ops notes: cleanup old checkpoints (retention policy) |

---

## 6. Acceptance criteria

- [ ] Simulated crash + resume test green  
- [ ] MemorySaver tests isolated from Postgres tests  
- [ ] Cross-org resume returns 404/403  

---

## 7. Traceability

| Item | Link |
|------|------|
| Postgres runtime | `backend/app/infrastructure/database/` |
| LangGraph durable execution | upstream docs |

*End LG-03.*
