# LangGraph implementation status

**Date:** 2026-07-17  
**Code host:** `C:\Project\generic-swarm-ops`  
**Mode:** Non-stop rewrite pass complete for MVP+ multi-pattern product slice

## Unit matrix

| Unit | Status | Notes |
|------|--------|-------|
| LG-00 Charter | Done (SoT) | `structure.md` v3.1 |
| LG-01 Dual engine | **Done** | `infrastructure/orchestration/*` |
| LG-02 State model | **Done** | `langgraph_engine/state.py` |
| LG-03 Checkpointer | **Done (memory)** | `MemorySaver`; env for postgres later |
| LG-04 Compiler / topology | **Done** | DNA → topology + StateGraph skeleton |
| LG-05 Patterns | **Done** | pipeline, supervisor, router, critique, map_reduce, pack_spine |
| LG-06 HITL bridge | **Done** | Gates → approvals → resume |
| LG-07 Host tools | **Done** | broker + adapters only |
| LG-08 Memory/ALC | **Done MVP** | `inject_memory_hits` |
| LG-09 Streaming | **Done MVP** | normalize_event on SSE; FE polls graph-state |
| LG-10 Pack graphs | **Done** | `business/video/graphs/*.graph.json` + APIs |
| LG-11 APIs | **Done** | topology, graph-state, trajectory, patterns, engines, domain graphs |
| LG-12 FE graph console | **Done** | `GraphRunConsole` |
| LG-13 Authoring UI | **Done** | `PatternAuthoringPanel` |
| LG-14 Interrupt UX | **Done** | approval context + waiting banner |
| LG-15 Trajectory | **Done** | score on complete + `/trajectory` |
| LG-16 Security | **Done MVP** | tenant thread check, budgets, redaction |
| LG-17 Migration | **Done MVP** | flagship + video DNA prefer langgraph; default env `langgraph` |
| LG-18 Tests | **Done** | `test_langgraph_engine` + E1 green |
| LG-19 Ops | **Done MVP** | deps in pyproject; env vars; health engines |

## Backend layout

```text
backend/app/infrastructure/
  orchestration/          # dual-engine registry
  langgraph_engine/
    engine.py             # multi-pattern dispatcher
    patterns/runners.py   # pipeline…pack_spine
    pack_loader.py
    trajectory.py
    streaming.py
    security.py
    nodes/memory_read.py
    tools/host_tool_node.py
    compiler.py, state.py, checkpointer.py, graph_builder.py
business/video/graphs/
  video_spine.graph.json
  viral_hook.graph.json
```

## Frontend layout

```text
frontend/src/components/domain/graph/
  graph-topology-panel.tsx
  graph-run-console.tsx
  pattern-authoring-panel.tsx
run-workflow-button.tsx     # engine selector (default langgraph)
run-waiting-banner.tsx
approval-decision-panel.tsx # interrupt context
```

## Operator path (rewritten)

1. Open workflow → set pattern / engine → Save  
2. **Run now** (engine=langgraph) → auto-dispatch  
3. Run page: **GraphRunConsole** (status, topology, trajectory, events)  
4. On gate: waiting banner → Approvals (node/engine/preview) → Approve  
5. Trajectory score on completion  

## Env

| Variable | Default |
|----------|---------|
| `GENERIC_SWARM_ENGINE_DEFAULT` | **`langgraph`** |
| `GENERIC_SWARM_LANGGRAPH_ENABLED` | `true` |
| `GENERIC_SWARM_LG_CHECKPOINT` | `memory` |
| `GENERIC_SWARM_LG_MAX_NODES` | `200` |
| `GENERIC_SWARM_LG_MAX_HANDOFFS` | `32` |

Rollback: set `GENERIC_SWARM_ENGINE_DEFAULT=legacy`.

## Tests

```powershell
cd C:\Project\generic-swarm-ops\backend
$env:PYTHONPATH="."
$env:GENERIC_SWARM_FORCE_JSON_STORE="true"
python -m unittest app.tests.unit.test_langgraph_engine app.tests.e2e.test_e1_operator_path -v
# OK (12 tests as of this pass)
```

## Residual (optional future)

- PostgresSaver production wiring  
- True LangGraph `interrupt()` / Command resume (current: host approval bridge)  
- Deep LLM supervisor reasoning (stubs/heuristics today)  
- Playwright full UI CI for graph console  
