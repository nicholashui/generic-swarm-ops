# LG-04 — DNA / Workflow → StateGraph Compiler

**Unit ID:** LG-04  
**Layer:** Backend  
**Priority:** P0  
**Depends on:** LG-02, LG-03  

---

## 1. Goal

Compile existing **Workflow DNA** and runtime workflow definitions into LangGraph `StateGraph` instances so the host keeps a portable IR while execution becomes a real graph.

---

## 2. Problem / gap

DNA JSON and workflow `steps[]` are documentation + linear execution. They are not compiled into a graph with edges, conditions, or nested specialists—so orchestration stays empty.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-04-01 | Compiler inputs: workflow record and/or `business/**/workflows/*.dna.json`. |
| FR-04-02 | Output: compiled LangGraph app (`compile(checkpointer=...)`). |
| FR-04-03 | Each DNA step → node function (agent node and/or tool node). |
| FR-04-04 | Support linear edges by default; optional `edges` / `conditions` in DNA metadata. |
| FR-04-05 | `production_ready` DNA still passes structure validators before compile. |
| FR-04-06 | Cache compiled graphs by `(workflow_id, version, content_hash)`. |
| FR-04-07 | Emit static **topology JSON** for FE (nodes, edges, pattern). |
| NFR-04-01 | Compile failures are ValidationError with path to DNA field. |
| NFR-04-02 | Deterministic node ids = DNA step ids. |

---

## 4. Design

### 4.1 Compilation pipeline

```text
DNA / workflow steps
   → validate (structure validators)
   → normalize to IntermediateGraphIR
   → attach pattern template (pipeline default)
   → build StateGraph(HostGraphState)
   → add nodes (agent_node, tool_node, gate_node)
   → add edges + conditional edges
   → compile(checkpointer)
```

### 4.2 Intermediate IR (example)

```yaml
graph_ir:
  id: g_wf_customer_onboarding_v12
  pattern: pipeline
  nodes:
    - id: verify_contract
      kind: agent_tools
      agent_id: quality_compliance_agent
      tools: [contract_parser, policy_retriever]
    - id: human_gate_billing
      kind: interrupt_gate
      risk_tier: tier_4_execute_with_gate
  edges:
    - [verify_contract, create_customer_record]
    - [create_customer_record, human_gate_billing]
```

### 4.3 Modules

```text
backend/app/infrastructure/langgraph_engine/compiler/
  dna_compiler.py
  ir.py
  topology.py
  cache.py
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-04-01 | Define IntermediateGraphIR schema |
| T-04-02 | Implement linear DNA→IR mapper |
| T-04-03 | Implement IR→StateGraph builder (pipeline) |
| T-04-04 | Integrate validators pre-compile |
| T-04-05 | Topology export endpoint data structure |
| T-04-06 | Unit tests: onboarding DNA compiles; invalid DNA fails |
| T-04-07 | Compile cache + invalidation on version change |

---

## 6. Acceptance criteria

- [ ] `wf_customer_onboarding_v12` compiles and runs one happy path with stub tools  
- [ ] Topology JSON lists all step nodes + edges  
- [ ] Unsafe production DNA fails compile  

---

## 7. Traceability

| Item | Link |
|------|------|
| DNA validators | `structure_validators.py` |
| Video DNA | `business/video/workflows/*.dna.json` |
| structure.md | §4 Workflow DNA |

*End LG-04.*
