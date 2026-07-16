# Spec: Users

**Route:** `/app/settings/users`  
**Permission (typical):** users:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

User roster, invitations, role assignment, disable lifecycle.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- UserAdminPanel — invite, role/status updates

## Backend / API contracts

- GET /users, POST invitations, PATCH users
- Accept invite via /users/invitations/accept (public with token)

## Architecture mapping

- RBAC roles map to permission strings used by API dependencies

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/settings/users/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/settings/users/spec.md`
