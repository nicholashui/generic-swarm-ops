# LG-07 — Tool Nodes and Permission Broker

**Unit ID:** LG-07  
**Layer:** Backend  
**Priority:** P0  
**Depends on:** LG-04, LG-06  

---

## 1. Goal

Ensure every LangGraph tool call goes through the **host tool permission broker and adapters**—so multi-agent graphs cannot escape allow-lists, audit, or side-effect recording.

---

## 2. Problem / gap

Linear runner already calls adapters; a naive LangGraph `ToolNode` with free LangChain tools would **bypass** allow-lists and `tool_effects`, recreating excessive agency risk (OWASP LLM06).

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-07-01 | Provide `HostToolNode` that resolves tools only via host registry/adapters. |
| FR-07-02 | Enforce intersection: agent.allowed_tools ∩ step.tools ∩ RBAC ∩ risk policy. |
| FR-07-03 | Persist `tool_effects` into graph state and host store. |
| FR-07-04 | Fail closed on unknown tool or cross-namespace pack violation. |
| FR-07-05 | Support stub tools for video (`video_media_gen_stub`, etc.) unchanged. |
| FR-07-06 | Emit audit event `tool.executed` / `tool.denied` per call. |
| NFR-07-01 | Timeouts and per-run tool call budget. |
| NFR-07-02 | No raw credentials in graph state or tool args logs. |

---

## 4. Design

```text
LangGraph agent node
   → proposes tool_call{name, args}
   → HostToolNode
        → broker.authorize(agent_id, tool_name, risk)
        → adapters.invoke(tool_name, args, ctx)
        → append tool_effects + audit
   → state update
```

### Modules

```text
backend/app/infrastructure/langgraph_engine/tools/
  host_tool_node.py
  budgets.py
```

Reuse: `backend/app/infrastructure/tools/adapters.py`, permission checks in runtime.

---

## 5. Tasks

| ID | Task |
|----|------|
| T-07-01 | Implement HostToolNode |
| T-07-02 | Port allow-list checks from legacy path |
| T-07-03 | Budget counters in state.metrics |
| T-07-04 | Denial tests (cross-namespace, missing tool) |
| T-07-05 | Adapter success writes tool_effects |

---

## 6. Acceptance criteria

- [ ] Unauthorized tool attempt never executes adapter  
- [ ] Successful tool leaves durable effect record  
- [ ] Video stub tools work inside graph node  

---

## 7. Traceability

| Item | Link |
|------|------|
| structure.md | §7 security, tool broker |
| Adapters | `infrastructure/tools/adapters.py` |
| Wave4 multipack isolation tests | `test_wave4_multipack.py` patterns |

*End LG-07.*
