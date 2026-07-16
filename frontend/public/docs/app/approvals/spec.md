# Spec: Approvals queue

**Route:** `/app/approvals`  
**Permission (typical):** approvals:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Human decision gates for high-risk or irreversible workflow steps.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Queue table (title, workflow, requester, risk, status)
- Detail with ApprovalDecisionPanel (approve/reject + reason)

## Backend / API contracts

- GET /api/v1/approvals
- POST /api/v1/approvals/{id}/decision
- Audit events recorded for every decision

## Architecture mapping

- Governance risk tiers 0–5; irreversible tools require gates
- Approvals implement human-in-the-loop for Safety priority

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/approvals/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/approvals/spec.md`
