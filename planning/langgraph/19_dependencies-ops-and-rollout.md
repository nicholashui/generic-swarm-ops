# LG-19 — Dependencies, Ops, and Rollout

**Unit ID:** LG-19  
**Layer:** Backend + Frontend + Ops  
**Priority:** P1  
**Depends on:** LG-00, LG-18  

---

## 1. Goal

Specify packages, environment variables, start scripts, and phased rollout so LangGraph adoption is operable on local Windows (this host) and future deploys.

---

## 2. Requirements

| ID | Requirement |
|----|-------------|
| FR-19-01 | Add Python deps: `langgraph`, checkpoint package as needed; pin versions. |
| FR-19-02 | Env vars documented in this unit (and later mirrored to `.env.example` on implement). |
| FR-19-03 | `start_all.ps1` remains valid; no separate LangGraph process required. |
| FR-19-04 | Health ready reports engine availability. |
| FR-19-05 | Rollout phases W0–W5 with go/no-go. |
| NFR-19-01 | Offline-friendly: core paths work without LangSmith API keys. |
| NFR-19-02 | License review MIT-compatible. |

---

## 3. Design

### 3.1 Planned dependencies

| Package | Role |
|---------|------|
| `langgraph` | StateGraph, compile, interrupts |
| `langgraph-checkpoint-postgres` or official postgres saver | Durable threads |
| Optional `langchain-core` | Messages/tools types if required by LangGraph version |

Avoid hard dependency on cloud deployment platform for MVP.

### 3.2 Environment variables

| Variable | Default | Meaning |
|----------|---------|---------|
| `GENERIC_SWARM_ENGINE_DEFAULT` | `legacy` | Default engine |
| `GENERIC_SWARM_LANGGRAPH_ENABLED` | `true` | Allow selecting langgraph |
| `GENERIC_SWARM_LG_CHECKPOINT` | `postgres` \| `memory` \| `sqlite` | Checkpointer backend |
| `GENERIC_SWARM_LG_MAX_NODES` | `200` | Budget |
| `GENERIC_SWARM_LG_MAX_HANDOFFS` | `32` | Supervisor cap |
| `DATABASE_URL` | (existing) | Postgres for runtime + checkpoints |

### 3.3 Rollout waves (ops)

| Wave | Enable | Go/No-Go |
|------|--------|----------|
| W0 | Code dual-engine, default legacy | E1 legacy green |
| W1 | Internal langgraph onboarding | LG tests green |
| W2 | HITL + FE console for admins | Operator checklist |
| W3 | Video spine langgraph | Spine e2e |
| W4 | Pattern authoring UI | No prod auto-flip |
| W5 | Flagship default langgraph | 48h soak + rollback drill |

### 3.4 start_all interaction

No new port. Backend process loads LangGraph in-process. FE only needs rebuilt after graph UI lands.

---

## 4. Tasks

| ID | Task |
|----|------|
| T-19-01 | pyproject dependency pins + lock notes |
| T-19-02 | `.env.example` keys (on implement) |
| T-19-03 | Health fields |
| T-19-04 | Rollout runbook section in this file (done) |
| T-19-05 | Post-ship: update structure.md §4 when default flips |

---

## 5. Acceptance criteria

- [ ] Fresh venv install instructions work  
- [ ] App starts with langgraph importable  
- [ ] Default legacy path unchanged for existing users  
- [ ] Rollback is one env/workflow field change  

---

## 6. Traceability

| Item | Link |
|------|------|
| start scripts | `start_all.ps1`, `stop_all.ps1` |
| pyproject | `backend/pyproject.toml` |
| LangGraph | https://github.com/langchain-ai/langgraph |

---

## 7. Open questions (resolve during implement)

| # | Question | Options |
|---|----------|---------|
| Q1 | PostgresSaver table coexistence with `runtime_state`? | Same DB different tables |
| Q2 | Need LangGraph.js on FE? | No—FE is visualization only |
| Q3 | LLM provider for supervisor reasoning? | Stub classifier first; pluggable later |
| Q4 | When to edit structure.md SoT? | After W2 demo accepted |

*End LG-19.*
