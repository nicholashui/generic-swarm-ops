# Spec: Dashboard

**Route:** `/app`  
**Permission (typical):** workflows:read (and related read scopes for tiles)  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Command surface for governed automation: metrics, pending approvals, recent workflows, knowledge freshness, and onboarding checklist.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Metric cards (agents, workflows, pending approvals, audit volume)
- Pending approvals table with deep links
- Recent workflows / knowledge status
- Onboarding checklist for first-time operators
- Primary actions: Create agent, Create workflow

## Backend / API contracts

- Aggregates live lists via product-data facade when not in demo mode
- GET /agents, /workflows, /approvals, /knowledge, /audit-logs, /memory, /evaluations, /processes
- Auth: bearer via same-origin /api/proxy (httpOnly cookie on BFF login)

## Architecture mapping

- Maps to structure.md Execution + Governance + Knowledge visibility
- Does not execute agents directly; backend remains control plane
- Design priorities: Safety → Auditability → Correctness → Efficiency → Autonomy

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/spec.md`
