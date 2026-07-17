# LG-06 — HITL Interrupts ↔ Approval Bridge

**Unit ID:** LG-06  
**Layer:** Backend  
**Priority:** P0  
**Depends on:** LG-03, LG-04  

---

## 1. Goal

Map LangGraph **interrupts** (first-class pause/resume) to the host **approvals** model so human gates are real orchestration events, not only a status string.

---

## 2. Problem / gap

Today: step sets `waiting_for_approval`, creates approval row, `decide_approval` re-enters `_execute_run`.  
No interrupt payload editing, no time-travel friendly checkpoint, no structured “resume value” into the next node.

LangGraph interrupts + checkpointer enable inspect/modify/resume semantics used in production HITL agents.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-06-01 | Gate nodes call LangGraph interrupt (or equivalent pause) with preview payload. |
| FR-06-02 | On interrupt, create host approval record; set run status `waiting_for_approval`. |
| FR-06-03 | `POST .../approvals/{id}/decision` resumes graph with decision + optional edits. |
| FR-06-04 | Reject path routes to compensating/fail node per DNA. |
| FR-06-05 | Support multiple sequential interrupts in one run. |
| FR-06-06 | Approval detail includes graph node_id, thread_id, state preview. |
| NFR-06-01 | Only roles with `approvals:approve` may resume. |
| NFR-06-02 | Resume is idempotent for duplicate decision posts. |

---

## 4. Design

### 4.1 Sequence

```text
graph node "gate_billing"
  → interrupt(value={preview, risk_tier, node_id})
  → engine maps to create_approval(...)
  → run.status = waiting_for_approval
operator POST decision approved
  → engine.Command(resume={decision, reason, overrides})
  → graph continues from checkpoint
```

### 4.2 Bridge module

```text
backend/app/infrastructure/langgraph_engine/hitl_bridge.py
  create_approval_from_interrupt(...)
  resume_graph_from_decision(...)
```

### 4.3 Compatibility

Keep approval REST shape; extend response with optional:

```json
{
  "graph_node_id": "activate_billing",
  "thread_id": "org:run_...",
  "interrupt_payload": {}
}
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-06-01 | Implement interrupt gate node factory |
| T-06-02 | Wire interrupt → approval creation |
| T-06-03 | Wire decide_approval → graph resume |
| T-06-04 | Reject path tests |
| T-06-05 | Multi-gate onboarding graph test (2 interrupts) |
| T-06-06 | Idempotent decision test |

---

## 6. Acceptance criteria

- [ ] E1-equivalent path with 2 interrupt gates completes on LangGraph engine  
- [ ] Approval without graph context still works for legacy engine  
- [ ] Unauthorized resume denied  

---

## 7. Traceability

| Item | Link |
|------|------|
| Approvals routes | `backend/app/api/v1/routes/approvals.py` |
| structure.md | §6.1 tiers, §4.3 lifecycle |
| LangGraph | interrupts / HITL docs |

*End LG-06.*
