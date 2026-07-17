# LG-15 — Evaluation and Evolution on Graphs

**Unit ID:** LG-15  
**Layer:** Backend + Frontend  
**Priority:** P1  
**Depends on:** LG-05, LG-11  

---

## 1. Goal

Evaluate **graph trajectories** (not only final status) and evolve orchestration configs in the **sandbox** (pattern, prompts, specialist sets)—never silent production mutation.

---

## 2. Problem / gap

Evals focus on workflow outcomes. Multi-agent graphs need trajectory metrics: wrong handoffs, excessive loops, tool denials, interrupt quality. Evolution should mutate graph metadata in sandbox.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-15-01 | Golden tasks may assert event traces (node order, handoff counts). |
| FR-15-02 | Trajectory scorer: completion, safety (tool denials), efficiency (node visits), HITL count. |
| FR-15-03 | Evolution variants may change `orchestration` block only in sandbox. |
| FR-15-04 | Canary promotes graph config version like DNA version. |
| FR-15-05 | FE Improve pipeline works on langgraph runs. |
| NFR-15-01 | Auto-promote still blocked. |
| NFR-15-02 | Adversarial tests include prompt injection during supervisor routing. |

---

## 4. Design

```text
graph run → trajectory log → scorer → evaluation card
evolution.propose(orchestration_delta) → sandbox compile → corpus eval → canary
```

Store lessons with optional `graph_node_id` / `agent_id`.

---

## 5. Tasks

| ID | Task |
|----|------|
| T-15-01 | Trajectory log format + scorer |
| T-15-02 | 3 golden trajectory fixtures |
| T-15-03 | Sandbox mutation of orchestration metadata |
| T-15-04 | Wire into existing evolution APIs |
| T-15-05 | Adversarial routing test |

---

## 6. Acceptance criteria

- [ ] Failing trajectory golden fails eval  
- [ ] Sandbox variant cannot write production workflow without promote  
- [ ] Improve UI still functions on graph run  

---

## 7. Traceability

| Item | Link |
|------|------|
| structure.md | §5 Evolution, §8 Evaluation |
| business/evals | golden-tasks |

*End LG-15.*
