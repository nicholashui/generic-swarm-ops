# Self-improvement, Loop Engineering & Knowledge Orchestration

This document maps three external frameworks onto **Generic Swarm Ops**, and
describes what we ship in-repo (governed, sandbox-safe).

## Sources (research mapping)

| Framework | Core idea | GSO mapping |
|-----------|-----------|-------------|
| [Self-Evolving Agents](https://github.com/nicholashui/what-is-self-evolving-agent/blob/main/book/BOOK_EN.md) | What / When / How evolve; closed loop; archive; empirical validation | Workflow DNA sandbox, lessons library, auto-propose variants, fitness archive |
| [Loop Engineering](https://github.com/nicholashui/what-is-loop-engineering/tree/main/book) | Control system: prompt → observe → verify → iterate; 8 components | Loop DNA + runner around workflow runs |
| [Agents-K1 knowledge orchestration](https://github.com/nicholashui/what-is-agent-k1/blob/book/agents-k1-complete-guide/book/Agents-K1-Complete-Guide.md) | Agent-native KG; typed entities/relations; operators; provenance | Lite five-module extract + graph store + typed operators |

## Safety / governance (non-negotiable)

1. **Never mutate production DNA directly** — proposals only in `evolution_variants`.
2. **Empirical validation** before canary (existing sandbox eval + corpus).
3. **Human gates** for tier ≥4 irreversible steps.
4. **No host code self-modification** in this phase (DGM-style code rewrite is deferred).
5. **Provenance** on lessons, graph nodes, and loop runs.

## What we implement

### A. Self-improvement loop (Reflexion + inter-episode lessons)

```
run fails or completes
  → reflect (extract lessons from errors / gate waits)
  → write to lesson library (utility scoring)
  → optionally auto-propose sandbox variant (changes only)
  → human/canary path unchanged
```

**When:** inter-run (after each workflow run).  
**What:** memory lessons + optional DNA tweak proposals.  
**How:** textual/rule reflection + population archive of variants.

### B. Loop Engineering runner

Eight components (encoded in Loop DNA):

| Component | GSO |
|-----------|-----|
| Trigger | API `POST /loops/run` or schedule stub |
| Isolation | each loop run has own `loop_run_id`; sandbox variants |
| Generator | workflow `_execute_run` / agents |
| Evaluator | eval harness + step status + stop rules |
| State/Memory | lessons + loop_runs collection |
| Skills/Knowledge | AGENTS.md, SOPs, knowledge search |
| Connectors | tool adapters (local) |
| Stopping condition | max_iterations, success, fail_budget, escalate |

Cycle: **prompt (start/continue run) → observe (status) → verify (eval) → iterate or stop**.

### C. Knowledge orchestration (K1-lite)

Not full Scholar-KG / 4B extractor. We ship:

- **Entity + claim + relation extraction** (rule/heuristic) on index
- **Graph** in runtime store (`knowledge_nodes`, `knowledge_edges`)
- **Operators:** seed resolve, lineage (shared entities / BUILD_ON links), gap detection
- **Fusion:** keyword Tier-0 + entity multi-hop + graph neighborhood

Stable IDs + evidence spans preserve Agents-K1 auditability spirit.

## API surface

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/improvement/reflect/{run_id}` | Extract lessons from a run |
| GET | `/api/v1/improvement/lessons` | List lesson library |
| POST | `/api/v1/improvement/auto-propose` | Propose sandbox variant from failures |
| POST | `/api/v1/loops/run` | Start governed improvement loop |
| GET | `/api/v1/loops/{id}` | Loop run status |
| POST | `/api/v1/knowledge/graph/extract/{document_id}` | Build graph from doc |
| GET | `/api/v1/knowledge/graph/query` | Seed + neighborhood |
| GET | `/api/v1/knowledge/graph/gaps` | Gap detection |

## Implemented backlog (all)

| Item | Status |
|------|--------|
| Auto-reflect on terminal run states | `GENERIC_SWARM_AUTO_REFLECT` (default true) |
| FE Improve on run detail | `ImproveRunButton` |
| Optional LLM critic | `GENERIC_SWARM_LLM_CRITIC_ENABLED` + API base |
| Population archive UI | `/app/evolution` + `GET /evolution/archive` |
| Tier-0 embeddings | hashing embed + optional pgvector table |
| Neo4j / GraphAnything export | `POST /knowledge/graph/federate` → Cypher/JSON |
| Sandboxed skill/prompt evolution | `/improvement/skills/*` |

## Non-goals (still deferred)

- Full DGM code self-rewrite of the backend host
- Full LightRAG product / GRPO 4B training
- Unattended production promotion
