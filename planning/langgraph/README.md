# LangGraph Adoption Plan — Index

**Program:** Adopt [LangGraph](https://github.com/langchain-ai/langgraph) as the **stateful multi-orchestration execution engine** for generic-swarm-ops.  
**Date:** 2026-07-16  
**Status:** **Implemented (MVP+)** — see `IMPLEMENTATION_STATUS.md`  
**Host path:** `C:\Project\generic-swarm-ops`  
**Upstream:** https://github.com/langchain-ai/langgraph  

---

## Why this program exists

Today’s execution path is a **thin linear runner** (`runtime._execute_run` over DNA step lists + manual `dispatch` + local tool adapters). It proves E1 and video stubs, but feels **empty** for real multi-agent orchestration:

| Gap today | LangGraph capability to adopt |
|-----------|-------------------------------|
| Linear step list, weak branching/loops | `StateGraph` nodes, conditional edges, cycles |
| No durable mid-run agent state beyond run JSON | Checkpointers (Postgres) + thread_id resume |
| Human gates bolted as run status flags | First-class **interrupts** + resume with payload |
| One “orchestrator” string, no supervisor/team patterns | Supervisor, handoffs, subgraphs, multi-agent topologies |
| FE shows lists/shells, not live graph topology | Graph canvas, node status, interrupt review UI |
| Manual queue/dispatch mental model | Durable graph runs with explicit pause/resume |

**This is not “delete FastAPI and replace everything with LangGraph.”**  
LangGraph becomes the **orchestration runtime** under the existing control plane (auth, RBAC, audit, risk tiers, domain packs, evolution sandbox).

---

## Non-negotiables (locked for this plan)

| ID | Rule |
|----|------|
| **LG-N1** | FastAPI remains the **public control plane** (`/api/v1/*`). LangGraph is an **engine**, not a second product API surface. |
| **LG-N2** | Governance wins: risk tiers, allow-listed tools, audit logs, no silent production DNA mutation. Graph nodes must call host tool broker / adapters. |
| **LG-N3** | Domain packs stay under `business/<domain_id>/`. Graphs may live as pack artifacts; **no** video logic in core except shared graph primitives. |
| **LG-N4** | E1 path and product bar must not regress: onboarding + human gates must remain runnable during migration (dual-engine or strangle pattern). |
| **LG-N5** | Evolution remains sandbox-only: graph topology/prompt variants proposed and evaluated offline before canary. |
| **LG-N6** | Prefer **Postgres checkpointer** aligned with existing `DATABASE_URL`; MemorySaver only for unit tests. |

---

## Target architecture (summary)

```text
                    Next.js Ops Console
           (graph canvas · run timeline · HITL panel)
                              │
                              ▼
                     FastAPI /api/v1/*
              auth · RBAC · workflows · runs · approvals
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
     Legacy DNA runner                 LangGraph Engine
     (_execute_run, opt-in)            (default for new / migrated)
              │                               │
              │         ┌─────────────────────┤
              │         ▼                     ▼
              │   Compiled StateGraph    Postgres Checkpointer
              │   (supervisor / pipeline / router / pack subgraphs)
              │         │
              └────► Tool Broker + Adapters + Memory + Audit
```

---

## Sub-functional units (implementation order)

| Order | Spec file | Layer | Theme | Depends on |
|------:|-----------|-------|-------|------------|
| 00 | [`00_program-charter-and-adoption-strategy.md`](./00_program-charter-and-adoption-strategy.md) | Both | Goals, scope, strangle plan, success metrics | — |
| 01 | [`01_runtime-boundary-dual-engine.md`](./01_runtime-boundary-dual-engine.md) | Backend | Engine interface, feature flags, run.engine field | 00 |
| 02 | [`02_graph-state-model-and-schema.md`](./02_graph-state-model-and-schema.md) | Backend | Typed graph state, reducers, message channels | 00 |
| 03 | [`03_checkpointing-and-durable-execution.md`](./03_checkpointing-and-durable-execution.md) | Backend | PostgresSaver, thread_id, resume, crash recovery | 01, 02 |
| 04 | [`04_dna-to-stategraph-compiler.md`](./04_dna-to-stategraph-compiler.md) | Backend | Compile Workflow DNA / pack DNA → StateGraph | 02, 03 |
| 05 | [`05_multi-orchestration-patterns.md`](./05_multi-orchestration-patterns.md) | Backend | Supervisor, pipeline, router, critique, map-reduce | 04 |
| 06 | [`06_hitl-interrupts-approval-bridge.md`](./06_hitl-interrupts-approval-bridge.md) | Backend | interrupt() ↔ approvals API | 03, 04 |
| 07 | [`07_tool-nodes-and-permission-broker.md`](./07_tool-nodes-and-permission-broker.md) | Backend | ToolNode wrapping host adapters | 04, 06 |
| 08 | [`08_memory-alc-and-retrieval-nodes.md`](./08_memory-alc-and-retrieval-nodes.md) | Backend | Pre-act retrieve, post-act write, ALC | 02, 07 |
| 09 | [`09_streaming-events-and-observability.md`](./09_streaming-events-and-observability.md) | Backend | SSE/stream map from graph events | 03, 05 |
| 10 | [`10_domain-pack-graph-artifacts.md`](./10_domain-pack-graph-artifacts.md) | Backend | Video spine + multipack graphs | 05, 07 |
| 11 | [`11_backend-api-surface-for-graphs.md`](./11_backend-api-surface-for-graphs.md) | Backend | Routes: start/resume/cancel/topology/state | 01–09 |
| 12 | [`12_frontend-graph-run-console.md`](./12_frontend-graph-run-console.md) | Frontend | Live graph run UI, node states, stream | 09, 11 |
| 13 | [`13_frontend-graph-authoring-and-topology.md`](./13_frontend-graph-authoring-and-topology.md) | Frontend | Author/view topology, pattern picker | 05, 11 |
| 14 | [`14_frontend-hitl-and-interrupt-ux.md`](./14_frontend-hitl-and-interrupt-ux.md) | Frontend | Interrupt review, edit state, resume | 06, 12 |
| 15 | [`15_evaluation-evolution-on-graphs.md`](./15_evaluation-evolution-on-graphs.md) | Both | Golden trajectories, sandbox graph variants | 05, 11 |
| 16 | [`16_security-tenancy-and-sandbox.md`](./16_security-tenancy-and-sandbox.md) | Backend | Isolation, injection, budget caps | 07, 03 |
| 17 | [`17_migration-e1-and-video-spine.md`](./17_migration-e1-and-video-spine.md) | Both | Strangle E1 + viral-hook onto LangGraph | 04–14 |
| 18 | [`18_testing-strategy-and-acceptance.md`](./18_testing-strategy-and-acceptance.md) | Both | Unit/integration/e2e gates | all |
| 19 | [`19_dependencies-ops-and-rollout.md`](./19_dependencies-ops-and-rollout.md) | Both | pyproject, env, flags, phased rollout | 00, 18 |

**Suggested delivery waves**

| Wave | Specs | Outcome |
|------|-------|---------|
| **W0** | 00–01 | Charter + dual-engine flag |
| **W1** | 02–04, 07 | First compiled graph runs tools |
| **W2** | 03, 06, 11 | Durable HITL + API |
| **W3** | 05, 08–10 | Multi-orchestration + packs |
| **W4** | 12–14 | FE graph console + authoring + HITL |
| **W5** | 15–19 | Eval, security, migrate E1/video, rollout |

---

## How to use these specs

Each `NN_*.md` file is a **self-contained sub-functional unit** with:

1. Goal  
2. Problem / current gap  
3. Requirements (functional + non-functional)  
4. Design  
5. Tasks (actionable, ordered)  
6. Acceptance criteria  
7. Traceability (APIs, files, structure.md sections)  
8. Risks / open questions  

**Agent prompt template:**

```text
Implement planning/langgraph/NN_<name>.md only.
Do not expand into later units.
Keep LG-N1…N6. Preserve E1 via dual-engine until 17 is done.
Write tests listed in the unit. Update structure.md only when architecture
intent for LangGraph is accepted as product SoT (separate PR preferred).
```

---

## Relationship to structure.md

**`structure.md` v3.1** is the product architecture SoT and **already includes** LangGraph as the normative target orchestration engine (§0.2, §0.2.1 LG-N, §2.1, §4, §10–12).

These `planning/langgraph/*` files are the **delivery breakdown** (tasks, waves, acceptance). They must not contradict `structure.md`; if they diverge, **structure.md wins**.

---

## External references

- LangGraph repo: https://github.com/langchain-ai/langgraph  
- Concepts: durable execution, interrupts/HITL, memory, streaming, multi-agent patterns  
- Host constraints: FastAPI control plane, Postgres, domain packs N1–N3, evolution sandbox-only  

---

*End of index.*
