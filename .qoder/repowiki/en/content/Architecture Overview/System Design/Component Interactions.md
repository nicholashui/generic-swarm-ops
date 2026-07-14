# Component Interactions

<cite>
**Referenced Files in This Document**
- [main.py](file://backend/app/main.py)
- [runtime.py](file://backend/app/runtime.py)
- [agent_service.py](file://backend/app/services/agent_service.py)
- [workflow_service.py](file://backend/app/services/workflow_service.py)
- [memory_service.py](file://backend/app/services/memory_service.py)
</cite>

## Table of Contents
1. Introduction
2. Project Structure
3. Core Components
4. Architecture Overview
5. Detailed Component Analysis
6. Dependency Analysis
7. Performance Considerations
8. Troubleshooting Guide
9. Conclusion

## Introduction
This document explains how the core components of the Generic Swarm Ops system interact to execute workflows, manage agents and tools, persist memory, and enforce governance controls. It focuses on request/response patterns, event-driven communication, state management across components, lifecycle management, error propagation, and failure handling strategies. The documentation is grounded in the backend implementation and highlights where each component participates in end-to-end flows.

## Project Structure
At a high level:
- HTTP entrypoint registers middleware, CORS, error handlers, and API routers.
- Services layer exposes domain operations (agents, workflows, memory).
- Runtime orchestrates execution, persistence, governance checks, approvals, tool invocation, memory writes, evaluations, and events.
- Infrastructure adapters are invoked by runtime for side-effecting tool calls.

```mermaid
graph TB
Client["Client"] --> API["FastAPI App<br/>main.py"]
API --> SvcAgents["Agent Service<br/>agent_service.py"]
API --> SvcWorkflows["Workflow Service<br/>workflow_service.py"]
API --> SvcMemory["Memory Service<br/>memory_service.py"]
SvcAgents --> RT["Runtime<br/>runtime.py"]
SvcWorkflows --> RT
SvcMemory --> RT
RT --> Store["RuntimeStore<br/>runtime.py"]
RT --> Tools["Tool Adapters<br/>infrastructure.tools.adapters"]
RT --> Eval["Evaluation<br/>runtime.py"]
RT --> Audit["Audit Logs<br/>runtime.py"]
RT --> Events["Stream Events<br/>runtime.py"]
```

**Diagram sources**
- [main.py:1-52](file://backend/app/main.py#L1-L52)
- [agent_service.py:1-30](file://backend/app/services/agent_service.py#L1-L30)
- [workflow_service.py:1-38](file://backend/app/services/workflow_service.py#L1-L38)
- [memory_service.py:1-27](file://backend/app/services/memory_service.py#L1-L27)
- [runtime.py:258-393](file://backend/app/runtime.py#L258-L393)

**Section sources**
- [main.py:1-52](file://backend/app/main.py#L1-L52)

## Core Components
- Agent Registry: CRUD and status management for agents; enforces activation preconditions via governance.
- Workflow Engine: Lifecycle of workflow definitions and runs; dispatches queued runs; executes steps with governance gates.
- Memory System: Scoped read/write access control; hybrid scopes (organization_memory, workflow_memory); provenance tracking.
- Tool Adapters: Side-effecting tool invocations with effect logging and audit trails.
- Governance Controls: Role-based permissions, risk tiers, human approval gates, production DNA validation, evaluation policies.

Key responsibilities and interactions:
- Services act as thin wrappers over Runtime methods, delegating authorization and persistence orchestration.
- Runtime maintains an in-process store backed by Postgres or JSON file, persists collections, emits events, and records audits.
- Tool execution is delegated to infrastructure adapters; failures propagate back to step/run state.
- Memory operations enforce agent scope allowlists and organization scoping.

**Section sources**
- [agent_service.py:1-30](file://backend/app/services/agent_service.py#L1-L30)
- [workflow_service.py:1-38](file://backend/app/services/workflow_service.py#L1-L38)
- [memory_service.py:1-27](file://backend/app/services/memory_service.py#L1-L27)
- [runtime.py:1308-1452](file://backend/app/runtime.py#L1308-L1452)
- [runtime.py:1454-1626](file://backend/app/runtime.py#L1454-L1626)
- [runtime.py:2339-2399](file://backend/app/runtime.py#L2339-L2399)

## Architecture Overview
The runtime is the central coordinator. It authenticates requests, validates permissions, manages workflow run state, invokes tool adapters, enforces governance gates, writes memory items, evaluates outcomes, and emits stream events.

```mermaid
classDiagram
class RuntimeServices {
+authenticate(token) AuthenticatedUser
+assert_permission(user, permission) void
+start_workflow_run(workflow_id, requested_by, payload, idempotency_key) dict
+dispatch_queued_runs(requested_by) list
+_execute_run(run, actor_user_id) void
+_write_memory(org, owner, scope, title, content, provenance, agent) void
+create_approval(run, step, actor_user_id) dict
+decide_approval(approval_id, decision, reason, decided_by) dict
+list_agents(current_user) list
+get_agent(current_user, agent_id) dict
+create_agent(current_user, payload) dict
+update_agent_status(current_user, agent_id, status) dict
+list_workflows(current_user) list
+get_workflow(current_user, workflow_id) dict
+create_workflow(current_user, payload) dict
+activate_workflow_version(current_user, workflow_id, version) dict
+search_memory(requested_by, query, scope, acting_agent_id) list
+create_memory_item(requested_by, payload, acting_agent_id) dict
}
class RuntimeStore {
+collection(name) list
+save() void
}
class ToolAdapterError
class AuthenticatedUser
RuntimeServices --> RuntimeStore : "persists state"
RuntimeServices --> ToolAdapterError : "catches"
RuntimeServices --> AuthenticatedUser : "uses"
```

**Diagram sources**
- [runtime.py:258-393](file://backend/app/runtime.py#L258-L393)
- [runtime.py:848-866](file://backend/app/runtime.py#L848-L866)
- [runtime.py:1660-1749](file://backend/app/runtime.py#L1660-L1749)
- [runtime.py:1938-2210](file://backend/app/runtime.py#L1938-L2210)
- [runtime.py:2211-2283](file://backend/app/runtime.py#L2211-L2283)
- [runtime.py:2339-2399](file://backend/app/runtime.py#L2339-L2399)

## Detailed Component Analysis

### Agent Registry
Responsibilities:
- List, get, create, update status, archive agents.
- Enforce activation prerequisites via governance (e.g., assurance case readiness).
- Provide activity and allowed tools per agent.

Interactions:
- Services delegate to Runtime for all agent operations.
- Activation may call into governance validators before updating status.

```mermaid
sequenceDiagram
participant Client as "Client"
participant API as "FastAPI"
participant Svc as "Agent Service"
participant RT as "Runtime"
participant Gov as "Governance Validator"
participant Store as "RuntimeStore"
Client->>API : PUT /agents/{id}/status
API->>Svc : update_agent_status(user, id, status)
Svc->>RT : update_agent_status(user, id, status)
alt status == active
RT->>Gov : assert_alc_ready(agent)
Gov-->>RT : ok or raises
end
RT->>Store : append/update agents collection
RT-->>Svc : updated agent
Svc-->>API : response
API-->>Client : 200 OK
```

**Diagram sources**
- [agent_service.py:16-17](file://backend/app/services/agent_service.py#L16-L17)
- [runtime.py:1346-1372](file://backend/app/runtime.py#L1346-L1372)

**Section sources**
- [agent_service.py:1-30](file://backend/app/services/agent_service.py#L1-L30)
- [runtime.py:1308-1396](file://backend/app/runtime.py#L1308-L1396)

### Workflow Engine
Responsibilities:
- Manage workflow definitions, versions, activation, disable/archive.
- Start runs with input validation, idempotency, and risk-tier gating.
- Dispatch queued runs, execute steps, handle approvals, evaluate results, emit events.

Execution flow:
- start_workflow_run creates a run record and queues it.
- dispatch_queued_runs transitions runs to running and invokes _execute_run_body.
- _execute_run_body iterates steps, checks agent/tool availability, enforces governance gates, reads/writes memory, invokes tool adapters, records effects, updates step/run state, and emits events.

```mermaid
sequenceDiagram
participant Client as "Client"
participant API as "FastAPI"
participant Svc as "Workflow Service"
participant RT as "Runtime"
participant Store as "RuntimeStore"
participant Tools as "Tool Adapters"
participant Eval as "Evaluation"
Client->>API : POST /workflows/{id}/runs
API->>Svc : start_workflow_run(id, user, payload)
Svc->>RT : start_workflow_run(...)
RT->>RT : validate schema, risk tier, idempotency
RT->>Store : append workflow_runs
RT-->>Svc : run created (queued)
Svc-->>API : 201 Created
Client->>API : POST /workflow_runs/dispatch
API->>Svc : dispatch_queued_runs(user)
Svc->>RT : dispatch_queued_runs(...)
loop For each queued run
RT->>RT : _execute_run_body(run, actor)
RT->>RT : check agent/tool availability
alt sensitive step requires approval
RT->>RT : _create_approval(...)
RT-->>Svc : run waiting_for_approval
else proceed
RT->>Tools : execute_tool(tool_id, payload)
Tools-->>RT : effect
RT->>Store : append tool_effects
RT->>RT : _write_memory(...)
RT->>Eval : _create_evaluation(run)
RT->>Store : save run+events+audit
end
end
```

**Diagram sources**
- [workflow_service.py:1-38](file://backend/app/services/workflow_service.py#L1-L38)
- [runtime.py:1660-1749](file://backend/app/runtime.py#L1660-L1749)
- [runtime.py:1755-1767](file://backend/app/runtime.py#L1755-L1767)
- [runtime.py:1938-2210](file://backend/app/runtime.py#L1938-L2210)
- [runtime.py:2211-2283](file://backend/app/runtime.py#L2211-L2283)

**Section sources**
- [workflow_service.py:1-38](file://backend/app/services/workflow_service.py#L1-L38)
- [runtime.py:1454-1626](file://backend/app/runtime.py#L1454-L1626)
- [runtime.py:1660-1749](file://backend/app/runtime.py#L1660-L1749)
- [runtime.py:1755-1767](file://backend/app/runtime.py#L1755-L1767)
- [runtime.py:1938-2210](file://backend/app/runtime.py#L1938-L2210)

### Memory System
Responsibilities:
- Scoped memory items with organization scoping and role-based visibility.
- Read/write enforcement based on agent allowed scopes.
- Provenance metadata and sensitivity levels.

Operations:
- search/get/create/update/delete memory items.
- During workflow execution, runtime performs scoped reads and writes with permission checks.

```mermaid
sequenceDiagram
participant Client as "Client"
participant API as "FastAPI"
participant Svc as "Memory Service"
participant RT as "Runtime"
participant Store as "RuntimeStore"
Client->>API : POST /memory/items
API->>Svc : create(requested_by, payload)
Svc->>RT : create_memory_item(requested_by, payload, acting_agent_id?)
RT->>RT : assert_memory_scope_allowed(agent, scope, action="write")
RT->>Store : append memory_items
RT-->>Svc : created item
Svc-->>API : 201 Created
```

**Diagram sources**
- [memory_service.py:1-27](file://backend/app/services/memory_service.py#L1-L27)
- [runtime.py:2339-2399](file://backend/app/runtime.py#L2339-L2399)
- [runtime.py:1901-1936](file://backend/app/runtime.py#L1901-L1936)

**Section sources**
- [memory_service.py:1-27](file://backend/app/services/memory_service.py#L1-L27)
- [runtime.py:2339-2399](file://backend/app/runtime.py#L2339-L2399)

### Tool Adapters
Responsibilities:
- Execute registered tools with side effects.
- Record tool effects and audit logs.
- Propagate errors back to step/run state.

Integration:
- Runtime invokes execute_tool for each tool declared in a step.
- Errors from adapters are caught and recorded as step failures.

```mermaid
flowchart TD
Start(["Step Execution"]) --> CheckAgent["Check agent available and enabled"]
CheckAgent --> |No| FailAgent["Mark step failed<br/>emit event"]
CheckAgent --> |Yes| CheckTools["Validate tools enabled and allowed"]
CheckTools --> |Fail| FailTool["Mark step failed<br/>emit event"]
CheckTools --> |OK| GateCheck["Determine if approval required"]
GateCheck --> |Requires Approval| CreateApproval["Create approval request<br/>pause run"]
GateCheck --> |No Approval Needed| ExecTools["Execute tool adapters"]
ExecTools --> ToolErr{"Tool error?"}
ToolErr --> |Yes| FailStep["Record tool failure<br/>audit + event"]
ToolErr --> |No| WriteMem["Write memory item (scoped)"]
WriteMem --> MemErr{"Permission denied?"}
MemErr --> |Yes| FailStep
MemErr --> |No| NextStep["Continue next step"]
FailAgent --> End(["Exit"])
FailTool --> End
FailStep --> End
NextStep --> End
```

**Diagram sources**
- [runtime.py:1938-2210](file://backend/app/runtime.py#L1938-L2210)

**Section sources**
- [runtime.py:1938-2210](file://backend/app/runtime.py#L1938-L2210)

### Governance Controls
Responsibilities:
- Role-based permissions and resource scoping.
- Risk-tier gating and human approval gates.
- Production DNA validation for workflow activation.
- Evaluation policy enforcement that can block completion.

Key behaviors:
- authenticate/assert_permission gate every operation.
- _tier_level maps risk tiers to numeric levels.
- _tool_requires_approval determines if a tool needs human review.
- _assert_production_dna_safe enforces structural rules when activating workflows.
- decide_approval resumes or terminates runs based on decisions.

```mermaid
flowchart TD
A["Operation Request"] --> B["Authenticate & authorize"]
B --> C{"Risk tier >= 4 and critical?"}
C --> |Yes| D["Require human approval"]
C --> |No| E{"Tier 2 and externalize/sensitive?"}
E --> |Yes| D
E --> |No| F["Proceed with execution"]
D --> G["Create approval request"]
G --> H["Run waits_for_approval"]
F --> I["Execute tools and write memory"]
I --> J["Evaluate outcome"]
J --> K{"block_on_fail?"}
K --> |Yes| L["Mark run failed"]
K --> |No| M["Complete run"]
```

**Diagram sources**
- [runtime.py:848-866](file://backend/app/runtime.py#L848-L866)
- [runtime.py:872-892](file://backend/app/runtime.py#L872-L892)
- [runtime.py:1469-1484](file://backend/app/runtime.py#L1469-L1484)
- [runtime.py:2004-2031](file://backend/app/runtime.py#L2004-L2031)
- [runtime.py:2249-2283](file://backend/app/runtime.py#L2249-L2283)
- [runtime.py:2187-2209](file://backend/app/runtime.py#L2187-L2209)

**Section sources**
- [runtime.py:848-866](file://backend/app/runtime.py#L848-L866)
- [runtime.py:1469-1484](file://backend/app/runtime.py#L1469-L1484)
- [runtime.py:2004-2031](file://backend/app/runtime.py#L2004-L2031)
- [runtime.py:2249-2283](file://backend/app/runtime.py#L2249-L2283)
- [runtime.py:2187-2209](file://backend/app/runtime.py#L2187-L2209)

## Dependency Analysis
- main.py wires FastAPI app, middleware, error handlers, and includes API router.
- Services depend on Runtime for business logic and persistence.
- Runtime depends on:
  - RuntimeStore for persistent collections (Postgres or JSON fallback).
  - Tool adapters for side effects.
  - Governance validators for agent activation and production DNA checks.
  - Self-improvement lessons library for injecting relevant lessons at step time.
  - Evaluation routines to assess outcomes.

```mermaid
graph LR
Main["main.py"] --> Router["API Router"]
Router --> AgentsSvc["agent_service.py"]
Router --> WorkflowsSvc["workflow_service.py"]
Router --> MemorySvc["memory_service.py"]
AgentsSvc --> RT["runtime.py"]
WorkflowsSvc --> RT
MemorySvc --> RT
RT --> Store["RuntimeStore"]
RT --> Tools["Tool Adapters"]
RT --> Eval["Evaluation"]
RT --> Audit["Audit Logs"]
RT --> Events["Stream Events"]
```

**Diagram sources**
- [main.py:1-52](file://backend/app/main.py#L1-L52)
- [agent_service.py:1-30](file://backend/app/services/agent_service.py#L1-L30)
- [workflow_service.py:1-38](file://backend/app/services/workflow_service.py#L1-L38)
- [memory_service.py:1-27](file://backend/app/services/memory_service.py#L1-L27)
- [runtime.py:258-393](file://backend/app/runtime.py#L258-L393)

**Section sources**
- [main.py:1-52](file://backend/app/main.py#L1-L52)

## Performance Considerations
- Use Postgres-backed RuntimeStore for concurrent access and durability; JSON fallback is suitable for local/dev.
- Avoid unnecessary deep copies in hot paths; current design uses deepcopy for safe responses.
- Batch operations where possible (e.g., dispatch_queued_runs) to reduce repeated saves.
- Limit memory context retrieval size (top-k hits) to reduce payload sizes during execution.
- Emit lightweight events and rely on consumers for real-time UI updates.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and diagnostics:
- Authentication failures: ensure bearer token or API key is valid and not revoked; check user status.
- Permission denied: verify role permissions and resource scoping; confirm organization_id alignment.
- Approval required: inspect approvals list and decide appropriately; rejections record lessons.
- Tool failures: examine tool_effects and audit logs for reasons; ensure tool is enabled and allowed for the agent.
- Memory scope denied: confirm agent.allowed_memory_scopes include the target scope.
- Run lifecycle: use pause/resume/retry/expire endpoints to manage stuck runs; monitor stream_events for progress.

Operational hooks:
- _append_audit records detailed actions with request correlation IDs.
- _emit_event publishes structured events for observability.
- Error classes provide consistent status codes and error codes for clients.

**Section sources**
- [runtime.py:848-866](file://backend/app/runtime.py#L848-L866)
- [runtime.py:1869-1893](file://backend/app/runtime.py#L1869-L1893)
- [runtime.py:1938-2210](file://backend/app/runtime.py#L1938-L2210)
- [runtime.py:2249-2283](file://backend/app/runtime.py#L2249-L2283)

## Conclusion
The Generic Swarm Ops system centers around a cohesive Runtime that coordinates agents, workflows, memory, tools, and governance. Services expose clean APIs while enforcing security and compliance. Event-driven signals and comprehensive audit trails support observability and troubleshooting. The design balances safety (approvals, DNA validation, evaluation blocking) with operational flexibility (pause/resume/retry/expire), enabling reliable automation with strong governance.