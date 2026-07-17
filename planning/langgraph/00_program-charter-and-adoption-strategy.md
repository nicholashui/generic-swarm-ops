# LG-00 — Program Charter and Adoption Strategy

**Unit ID:** LG-00  
**Layer:** Backend + Frontend (program)  
**Priority:** P0  
**Depends on:** —  
**Upstream:** [LangGraph](https://github.com/langchain-ai/langgraph)

---

## 1. Goal

Define *why*, *what*, and *how* generic-swarm-ops adopts LangGraph so multi-agent **orchestration is real** (graphs, supervisors, HITL interrupts, durable resume)—without discarding the governed host (auth, RBAC, audit, domain packs, evolution sandbox).

---

## 2. Problem statement (current design is “empty”)

| Symptom | Root cause in as-built code |
|---------|----------------------------|
| Workflows feel like a checklist | `_execute_run` walks a linear step array |
| “Orchestrator” is mostly a label | No dynamic routing, handoffs, or nested teams |
| Pause/resume is coarse | `waiting_for_approval` flag + re-enter `_execute_run` |
| FE cannot show a real graph | No topology/events model beyond step list |
| Video pack 114 agents underused | Standby tables exist; no live multi-agent graph |
| Dispatch is a footgun | Start queues; separate dispatch API |

LangGraph is a **low-level orchestration framework** for long-running stateful agents: durable execution, interrupts, memory, streaming—not a second product to fork the repo into.

---

## 3. Requirements

### 3.1 Functional

| ID | Requirement |
|----|-------------|
| FR-00-01 | Program shall introduce LangGraph as the **preferred execution engine** for multi-agent workflows. |
| FR-00-02 | Program shall preserve FastAPI as the only public control-plane API for operators and FE. |
| FR-00-03 | Program shall support **multiple orchestration patterns** (pipeline, supervisor, router, critique bus, pack subgraph). |
| FR-00-04 | Program shall migrate flagship paths (customer onboarding E1, video spine) without permanent dual-product UX. |
| FR-00-05 | Program shall keep domain pack isolation (video logic in `business/video/`). |
| FR-00-06 | Program shall expose FE surfaces to **see and control** graph runs (not only lists). |

### 3.2 Non-functional

| ID | Requirement |
|----|-------------|
| NFR-00-01 | Safety → Auditability → Correctness → Efficiency → Autonomy ordering preserved. |
| NFR-00-02 | No silent production graph/DNA mutation (sandbox evolution only). |
| NFR-00-03 | Strangle migration: legacy engine remains until acceptance gates pass. |
| NFR-00-04 | Postgres-first durability for checkpoints when `DATABASE_URL` configured. |
| NFR-00-05 | Dependency surface minimized: `langgraph` (+ checkpointer package as needed); avoid requiring full LangSmith cloud. |

### 3.3 Success metrics

| Metric | Target |
|--------|--------|
| E1 on LangGraph | Onboarding run completes with ≥1 interrupt-based gate |
| Multi-orch demo | Supervisor graph with ≥2 specialist nodes + handoff |
| FE proof | Operator can open run and see node graph + live status |
| Empty-feel score | Step list alone is insufficient; topology + state panel required |
| Regression | Existing unit suite remains green under dual-engine default-off |

---

## 4. Design

### 4.1 Adoption strategy: **Strangle + Dual Engine**

```text
Phase A: Engine behind flag `GENERIC_SWARM_ENGINE=langgraph|legacy` (default legacy)
Phase B: New workflows / pack DNA compile to LangGraph only
Phase C: E1 + video spine migrate; FE graph console default
Phase D: Legacy runner deprecated (compat shim only)
```

### 4.2 What LangGraph owns vs what host owns

| Concern | Owner |
|---------|--------|
| Graph topology, node scheduling, loops, branching | LangGraph |
| Checkpoint persistence / thread resume | LangGraph checkpointer + host DB config |
| Auth, tenancy, RBAC, rate limits | Host FastAPI |
| Tool credentials / allow-lists / audit | Host tool broker + audit service |
| Risk tier / approval policy records | Host governance + approvals tables |
| Domain pack manifests / inventory | Host business layer |
| Evolution propose/evaluate/canary | Host evolution (graph defs as artifacts) |

### 4.3 Deliverable artifact types

| Artifact | Location (planned) |
|----------|-------------------|
| Engine package | `backend/app/infrastructure/langgraph_engine/` |
| Graph registry | runtime store + optional `business/**/graphs/` |
| Compiler DNA→graph | `.../compiler/dna_compiler.py` |
| Pattern library | `.../patterns/{pipeline,supervisor,router}.py` |
| FE graph console | `frontend/src/components/domain/graph-*` |

### 4.4 Explicit non-goals (this program)

- Replacing Next.js with Streamlit/LangSmith Studio as primary UI  
- Mandatory LangSmith SaaS for core function  
- Deleting Workflow DNA schemas (DNA becomes **portable IR** compiled to graphs)  
- Free-form ungoverned agent swarms without allow-lists  

---

## 5. Tasks

| ID | Task | Output |
|----|------|--------|
| T-00-01 | Socialize LG-N1…N6 with maintainers; record decisions in this folder README | Decision log in README |
| T-00-02 | Add ADR stub section: “LangGraph as orchestration engine” | This file + README |
| T-00-03 | Inventory current runner call sites (`start_workflow_run`, `dispatch`, `_execute_run`) | Call-site list appendix |
| T-00-04 | Define feature flag + run record fields (see LG-01) | Spec handoff |
| T-00-05 | Define phased wave schedule and exit demos | README waves |
| T-00-06 | Plan structure.md §4 update when W2+ ships | Deferred edit note |

---

## 6. Acceptance criteria

- [ ] README index lists all units 00–19 with dependencies  
- [ ] LG-N1…N6 written and referenced by later units  
- [ ] Success metrics measurable via tests/demos  
- [ ] Call-site inventory exists for dual-engine wiring  

---

## 7. Traceability

| Item | Link |
|------|------|
| structure.md | §4 Execution, §5 Evolution, §0.3 Domain packs |
| Current runner | `backend/app/runtime.py` `_execute_run*` |
| E1 | `backend/app/tests/e2e/test_e1_operator_path.py` |
| LangGraph | https://github.com/langchain-ai/langgraph |

---

## 8. Risks

| Risk | Mitigation |
|------|------------|
| “Second control plane” sprawl | LG-N1; no public LangGraph server port required |
| Scope explosion (114 agents all deep) | Patterns first; pack spine second; specialists via supervisor routing |
| Breaking E1 mid-migration | Dual-engine default legacy until LG-17 |
| LLM cost | Graphs may use stub/heuristic nodes first; LLM nodes opt-in |

---

## 9. Appendix — Current call-site inventory (baseline)

| Function / route | Role |
|------------------|------|
| `POST /workflows/{id}/run` | Create queued run |
| `POST /workflow-runs/dispatch` | Execute queued runs |
| `runtime._execute_run` | Linear step body |
| `runtime.decide_approval` | Resume after gate |
| FE `RunWorkflowButton` | Start (+ dispatch) |
| FE `ApprovalDecisionPanel` | HITL decision |

*End LG-00.*
