# LG-01 — Runtime Boundary and Dual Engine

**Unit ID:** LG-01  
**Layer:** Backend  
**Priority:** P0  
**Depends on:** LG-00  

---

## 1. Goal

Introduce a clean **engine interface** so runs can execute on `legacy` or `langgraph` without forking the public API, enabling safe strangle migration.

---

## 2. Problem / gap

`start_workflow_run` → queue → `dispatch_queued_runs` → `_execute_run` is a single hard-coded path. There is no seam for an alternate orchestrator.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-01-01 | Define `WorkflowEngine` protocol: `start`, `dispatch_or_continue`, `resume_from_approval`, `cancel`, `get_execution_view`. |
| FR-01-02 | Persist `run.engine` ∈ {`legacy`,`langgraph`} and optional `run.graph_thread_id`. |
| FR-01-03 | Config `GENERIC_SWARM_ENGINE_DEFAULT=legacy|langgraph`. |
| FR-01-04 | Per-workflow override `workflow.execution_engine` or DNA metadata `engine: langgraph`. |
| FR-01-05 | Dispatch route routes to selected engine. |
| FR-01-06 | Health ready reports `orchestration_engine` capabilities. |
| NFR-01-01 | Default remains `legacy` until LG-17 acceptance. |
| NFR-01-02 | Engine selection is audited on run start. |

---

## 4. Design

```text
runtime.start_workflow_run(...)
   → pick engine from workflow meta / flag
   → run.engine = ...
   → engine.on_queued(run)

runtime.dispatch_queued_runs(...)
   → for each run: engines[run.engine].execute(run)

runtime.decide_approval(...)
   → engines[run.engine].resume(run, decision)
```

### 4.1 Proposed modules

```text
backend/app/infrastructure/orchestration/
  __init__.py
  protocol.py          # WorkflowEngine Protocol
  registry.py          # get_engine(name)
  legacy_engine.py     # wraps current _execute_run
  langgraph_engine.py  # LG implementation (filled in later units)
```

### 4.2 Run record extensions

```json
{
  "engine": "langgraph",
  "graph_thread_id": "thread_run_abc",
  "graph_id": "g_wf_customer_onboarding_v12",
  "graph_checkpoint_ns": "org_default",
  "orchestration_pattern": "pipeline"
}
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-01-01 | Add `WorkflowEngine` protocol + registry |
| T-01-02 | Extract legacy path into `LegacyWorkflowEngine` without behavior change |
| T-01-03 | Stub `LangGraphWorkflowEngine` raising `NotImplemented` or passthrough error until LG-04 |
| T-01-04 | Wire start/dispatch/approve to registry |
| T-01-05 | Config + env docs for engine default |
| T-01-06 | Unit tests: engine selection matrix |
| T-01-07 | Health endpoint field for engines |

---

## 6. Acceptance criteria

- [ ] E1 still passes with default `legacy`  
- [ ] Setting workflow to `langgraph` before engine ready returns clear 501/validation error  
- [ ] `run.engine` persisted and visible on GET run  

---

## 7. Traceability

| Item | Path |
|------|------|
| Runtime | `backend/app/runtime.py` |
| Dispatch route | `backend/app/api/v1/routes/workflow_runs.py` |
| Config | `backend/app/core/config.py` |

---

## 8. Risks

| Risk | Mitigation |
|------|------------|
| Big-bang rewrite of runtime.py | Extract only; no logic change in legacy |
| FE assumes only step list | Keep step list projection for both engines |

*End LG-01.*
