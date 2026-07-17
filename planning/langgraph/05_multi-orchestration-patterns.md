# LG-05 — Multi-Orchestration Patterns

**Unit ID:** LG-05  
**Layer:** Backend  
**Priority:** P0  
**Depends on:** LG-04  

---

## 1. Goal

Ship a **pattern library** so the host can run multiple orchestration styles—supervisor teams, pipelines, routers, critique loops—not a single empty linear chain.

---

## 2. Problem / gap

Only one mental model exists: ordered steps. Real multi-agent systems need:

- Supervisor that delegates to specialists  
- Conditional routing by intent/risk  
- Parallel fan-out / join (map-reduce style)  
- Critique / evaluator loops  
- Pack subgraphs (video spine under host supervisor)

LangGraph multi-agent patterns (supervisor, handoffs, subgraphs) are the intended implementation vehicle.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-05-01 | Pattern enum: `pipeline`, `supervisor`, `router`, `critique`, `map_reduce`, `pack_spine`. |
| FR-05-02 | Each pattern has a builder that returns a compiled/uncompiled StateGraph. |
| FR-05-03 | Supervisor pattern supports N specialist nodes + handoff tool/route channel. |
| FR-05-04 | Router pattern selects next node from `state.route` or classifier node. |
| FR-05-05 | Critique pattern: worker → critic → accept/revise loop with max iterations. |
| FR-05-06 | Map-reduce: fan-out over list in state, join aggregator node. |
| FR-05-07 | Patterns declared in DNA metadata `orchestration.pattern` + `orchestration.config`. |
| FR-05-08 | Pattern catalog API for FE authoring (list patterns + params schema). |
| NFR-05-01 | Max loop iterations enforced (denial-of-wallet). |
| NFR-05-02 | Patterns must not bypass tool allow-lists. |

---

## 4. Design

### 4.1 Pattern sketches

**Pipeline** (default DNA):  
`START → n1 → n2 → … → END`

**Supervisor:**  
```text
START → supervisor ⇄ specialist_a|specialist_b|specialist_c → END
```
Supervisor writes `route.next_agent`; conditional edges dispatch; specialists return to supervisor until `route.done`.

**Router:**  
```text
START → classify → (branch_a | branch_b | branch_c) → join → END
```

**Critique:**  
```text
START → produce → critique → (revise|accept) → END
```

**Pack spine:**  
Host entry → domain subgraph (video.planner → video.orchestrator → …) → host audit node.

### 4.2 DNA metadata example

```yaml
orchestration:
  pattern: supervisor
  config:
    supervisor_agent: video.orchestrator
    specialists:
      - video.screenwriter
      - video.webresearch
      - video.aiqaconsistency
    max_handoffs: 12
```

### 4.3 Modules

```text
backend/app/infrastructure/langgraph_engine/patterns/
  base.py
  pipeline.py
  supervisor.py
  router.py
  critique.py
  map_reduce.py
  pack_spine.py
  catalog.py
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-05-01 | Implement pipeline builder (parity with linear DNA) |
| T-05-02 | Implement supervisor + handoff tests (2 specialists) |
| T-05-03 | Implement router + critique + map_reduce MVP |
| T-05-04 | Wire DNA metadata → pattern selection in compiler |
| T-05-05 | Pattern catalog JSON schema for FE |
| T-05-06 | Integration test: supervisor graph produces artifacts from 2 agents |

---

## 6. Acceptance criteria

- [ ] At least **three** patterns runnable in tests without live LLM (heuristic nodes OK)  
- [ ] Supervisor test shows ≥2 handoffs recorded in state.messages or route log  
- [ ] Max iteration circuit breaker trips in unit test  

---

## 7. Traceability

| Item | Link |
|------|------|
| structure.md | §2 architecture, §9 agents |
| Video entry agents | `video.orchestrator`, `video.planner` |
| LangGraph multi-agent | upstream multi-agent how-tos |

*End LG-05.*
