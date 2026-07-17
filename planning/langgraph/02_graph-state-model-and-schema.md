# LG-02 — Graph State Model and Schema

**Unit ID:** LG-02  
**Layer:** Backend  
**Priority:** P0  
**Depends on:** LG-00  

---

## 1. Goal

Define a **typed, host-aligned graph state** that LangGraph nodes share, including messages, case payload, risk context, tool effects, and interrupt payloads—rich enough for multi-agent orchestration, not an empty step index.

---

## 2. Problem / gap

Run state today is a flat dict: `steps[]`, `status`, `input_payload`, sparse `output`. There is no channel for agent messages, shared scratchpad, supervisor routing decisions, or subgraph isolation.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-02-01 | Define `HostGraphState` (TypedDict or Pydantic) used by all host-compiled graphs. |
| FR-02-02 | Include channels: `messages`, `case`, `risk`, `route`, `artifacts`, `tool_effects`, `interrupt`, `metrics`. |
| FR-02-03 | Reducers for append-only lists (messages, tool_effects, audit_hints). |
| FR-02-04 | Map state ↔ existing run projection (`steps`, `current_step`, `output`) for API/FE compatibility. |
| FR-02-05 | Support nested subgraph state namespaces for pack specialists. |
| FR-02-06 | Schema version field `state_schema_version` for migrations. |
| NFR-02-01 | No secrets in state; credentials resolved only inside tool broker at call time. |
| NFR-02-02 | State JSON-serializable for checkpointer. |

---

## 4. Design

### 4.1 Core state sketch

```python
class HostGraphState(TypedDict, total=False):
    state_schema_version: str
    organization_id: str
    run_id: str
    workflow_id: str
    domain_id: str | None
    case: dict          # input_payload + evolving case fields
    risk: dict          # risk_tier, flags, gate reasons
    messages: Annotated[list[dict], add_messages]  # agent/supervisor chat
    route: dict         # next_agent, pattern, handoff_reason
    active_agent_id: str | None
    artifacts: dict     # named outputs (script, qc_report, …)
    tool_effects: Annotated[list[dict], operator.add]
    memory_hits: list[dict]
    interrupt: dict | None  # {type, approval_id, payload_preview}
    metrics: dict       # tokens, cost, latency
    error: dict | None
```

### 4.2 Projection to existing Run API

| Graph state | Run field |
|-------------|-----------|
| node visit log | `steps[]` with status |
| `interrupt` | `status=waiting_for_approval`, `approval_request_id` |
| `artifacts` | `output` |
| `error` | `error` |
| `metrics` | `token_usage` / `cost_usage` |

### 4.3 Modules

```text
backend/app/infrastructure/langgraph_engine/state.py
backend/app/infrastructure/langgraph_engine/projection.py
backend/app/schemas/graph_state.py
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-02-01 | Author `HostGraphState` + reducers |
| T-02-02 | Implement `project_state_to_run` / `seed_state_from_run` |
| T-02-03 | JSON schema export for FE types (optional OpenAPI component) |
| T-02-04 | Unit tests: reducer merge, serialization round-trip |
| T-02-05 | Document forbidden keys (password, token, raw secrets) |

---

## 6. Acceptance criteria

- [ ] State round-trips through JSON without loss of required fields  
- [ ] Projection produces FE-compatible step list for a 3-node graph  
- [ ] Secrets scanner test rejects state containing `password`/`api_key` patterns when written via helper  

---

## 7. Traceability

| Item | Link |
|------|------|
| structure.md | §3.3 memory, §4 DNA, §6 risk |
| LangGraph | State + reducers docs |

*End LG-02.*
