# LG-09 — Streaming Events and Observability

**Unit ID:** LG-09  
**Layer:** Backend  
**Priority:** P1  
**Depends on:** LG-03, LG-05  

---

## 1. Goal

Map LangGraph runtime events to the host **SSE / run event** model so operators see node starts, handoffs, tool calls, interrupts, and completion in real time.

---

## 2. Problem / gap

Stream endpoint exists for runs but is thin relative to a true multi-agent graph. Empty orchestration feels worse when the UI cannot show *why* a supervisor chose an agent.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-09-01 | Stream events: `node.started`, `node.completed`, `handoff`, `tool_call.*`, `interrupt`, `checkpoint`, `run.completed`, `error`. |
| FR-09-02 | Existing `GET /workflow-runs/{id}/stream` remains the FE contract (extended types OK). |
| FR-09-03 | Each event includes `run_id`, `node_id`, `agent_id?`, `ts`, `payload`. |
| FR-09-04 | Optional correlation id for multi-agent fan-out. |
| FR-09-05 | Structured logs remain JSON with request_id. |
| NFR-09-01 | Streams must not include secrets or full system prompts by default. |
| NFR-09-02 | Backpressure: drop or sample high-volume token streams if needed. |

---

## 4. Design

Bridge LangGraph stream modes (`updates`, `events`) → host event bus / SSE.

```text
graph.astream(...) → EventNormalizer → run_events store + SSE
```

### Modules

```text
backend/app/infrastructure/langgraph_engine/streaming.py
backend/app/infrastructure/langgraph_engine/event_normalize.py
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-09-01 | Event type enum extension |
| T-09-02 | Normalizer unit tests |
| T-09-03 | Wire engine execute to emit stream events |
| T-09-04 | SSE integration smoke test |

---

## 6. Acceptance criteria

- [ ] Supervisor run emits ≥1 `handoff` event in test capture  
- [ ] Interrupt emits stream event before waiting state  
- [ ] No bearer tokens in event payloads (scan test)  

---

## 7. Traceability

| Item | Link |
|------|------|
| Stream route | `workflow_runs.py` stream |
| structure.md | §10 HAI visibility |

*End LG-09.*
