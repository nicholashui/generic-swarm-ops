# LG-14 — Frontend HITL and Interrupt UX

**Unit ID:** LG-14  
**Layer:** Frontend  
**Priority:** P0  
**Depends on:** LG-06, LG-12  

---

## 1. Goal

Upgrade approval UX for **graph interrupts**: show node context, payload preview, optional field overrides, and resume—making human gates part of multi-agent orchestration, not a disconnected queue item.

---

## 2. Problem / gap

Approval panel is generic approve/reject. It does not show graph node, artifacts preview, or allow safe state edits before resume.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-14-01 | Approval detail shows `graph_node_id`, workflow, risk, interrupt payload preview. |
| FR-14-02 | Deep link from interrupted run node → approval. |
| FR-14-03 | Approve/Reject with reason (existing). |
| FR-14-04 | Optional override JSON (validated server-side) for resume payload. |
| FR-14-05 | After decision, navigate to run console and show resumed node. |
| FR-14-06 | Banner on run console when `waiting_for_approval` with CTA. |
| NFR-14-01 | Override editor disabled for roles without approve permission. |
| NFR-14-02 | Clear empty/error states when interrupt payload missing (legacy). |

---

## 4. Design

Enhance `ApprovalDecisionPanel`:

```text
[Context card: node, risk, artifacts]
[Payload preview]
[Optional overrides editor]
[Approve] [Reject]
```

Run console banner:

```text
Waiting for human gate on node activate_billing → Review approval
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-14-01 | Extend types for interrupt fields |
| T-14-02 | Upgrade ApprovalDecisionPanel UI |
| T-14-03 | Run console waiting banner + link |
| T-14-04 | E2E smoke (Playwright optional) login→run→approve |
| T-14-05 | Unit tests for panel states |

---

## 6. Acceptance criteria

- [ ] Operator can approve from UI and see run leave waiting state  
- [ ] Legacy approvals without graph fields still work  
- [ ] Override rejected when schema invalid  

---

## 7. Traceability

| Item | Link |
|------|------|
| Approval panel | `approval-decision-panel.tsx` |
| structure.md | §6 gates, §10 HAI |

*End LG-14.*
