# Spec: Audit logs

**Route:** `/app/audit-logs`  
**Permission (typical):** audit:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Immutable-style operational audit trail for auth, workflow, approval, and tool actions.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Chronological audit table with actor, action, resource, outcome
- Filters by type when provided

## Backend / API contracts

- GET /api/v1/audit-logs
- Runtime appends audit events on login, DNA steps, approvals, tool effects

## Architecture mapping

- Auditability is priority #2 after Safety
- Supports EU AI Act / assurance case evidence trails

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/audit-logs/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/audit-logs/spec.md`
