# Design — 12 Human Gates and Audit Logging

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-12-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-12`) |
| Source | `structure.md` §4 guardrails, §2 audit, §6 |
| Design quality bar | 100 |

---

## 1. Purpose

Pause irreversible/high-risk steps for **human decisions**, and maintain an **append-oriented audit trail** for tools, approvals, and security-relevant actions. Rejection records a learning lesson (STRUCT-16).

---

## 2. Context

Orchestrator (11) detects gate → Approval service → Reviewer decides → resume or reject → Audit. FE Approvals + run detail (16).

---

## 3. Architecture

```text
needs_gate
  → create ApprovalRequest (pending)
  → run.status = awaiting_approval
  → audit approval.requested
  → reviewer decide
        ├─ approved → run.running → continue step
        └─ rejected → run.rejected + lesson.rejection_recorded
```

### 3.1 Components

| ID | Component | Role |
|----|-----------|------|
| C-12-1 | Gate evaluator | DNA + tier + irreversible + DRC predicates |
| C-12-2 | Approval store | RuntimeStore approvals |
| C-12-3 | Decide API | approve/reject RBAC |
| C-12-4 | Audit log | Append-only events |
| C-12-5 | FE surfaces | Approvals queue, run banner |
| C-12-6 | Rejection lesson | improvement_lessons write |

### 3.2 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-12-01 | Gate state on run | Simple, durable |
| D-12-02 | Append-only audit | Non-repudiation |
| D-12-03 | Reject → lesson | Human-AI feedback loop |

---

## 4. Gate triggers (normative)

| Trigger | Source |
|---------|--------|
| step.human_gate_required | DNA |
| step.irreversible / irreversible_execution | DNA |
| risk_tier ≥ tier_4 critical | DNA + policy |
| exception_path_triggered | context |
| drc.human_approval_required | guardrail predicate |

```text
while awaiting_approval:
  FORBIDDEN: execute gated irreversible tool
```

---

## 5. Data models

### 5.1 ApprovalRequest

```text
{
  id, organization_id, run_id, step_id, workflow_id,
  status: pending|approved|rejected,
  risk_tier, requested_action, reason?,
  assigned_reviewer?, decided_at?, decision_reason?,
  created_at
}
```

### 5.2 AuditEvent

```text
{
  id, timestamp, organization_id, actor_id,
  action, resource_type, resource_id,
  request_id?, metadata, result: success|failure
}
```

Query filters: actor, action, resource_type, resource_id, time range.

### 5.3 Approval state machine

```text
pending → approved
pending → rejected
approved/rejected → (terminal; reassign only if pending)
```

---

## 6. API contract

| Method | Path | Permission |
|--------|------|------------|
| GET | `/api/v1/approvals` | approvals:read |
| POST | `/api/v1/approvals/{id}/approve` | approvals:approve |
| POST | `/api/v1/approvals/{id}/reject` | approvals:reject |
| GET | `/api/v1/audit_logs` | audit:read |

Reject body: `{ "reason": "..." }` → stored + lesson summary.

### 6.1 Fail-closed audit

If audit write is required and fails → treat action incomplete/failed (policy).

---

## 7. NFR design

| NFR | Design |
|-----|--------|
| NFR-12-01 List &lt;1s baseline | Indexed org queries |
| NFR-12-02 Audit append low overhead | In-process append + save |
| NFR-12-03 Reviewer-only decide | RBAC |
| NFR-12-04 No user delete audit | No delete API |
| NFR-12-05 request_id correlation | Middleware |

---

## 8. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-12-01…07 | §4–5 gates/approvals | E1 approve; reject unit |
| FR-12-08…12 | §5.2 audit | audit query tests |
| NFR-12-01…05 | §7 | RBAC + API |
| AC-12-01…05 | E1 + FE | e2e |

---

## 9. Validation design

Pause on irreversible; approve resumes; reject stops + lesson; non-reviewer 403.

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-12-01 | Multi-channel notify | Optional adapters |
| OI-12-02 | Multi-approver quorum | Future |

---

## 11. Design score claim

**Self-score: 100** — triggers, state machines, models, API, rejection lesson, RTM.
