# Spec: Roles

**Route:** `/app/settings/roles`  
**Permission (typical):** settings:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Permission matrix and responsibility boundaries for RBAC roles.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Roles explanation / matrix view

## Backend / API contracts

- Role definitions enforced in backend permissions module

## Architecture mapping

- Least privilege; high-risk actions need elevated roles + gates

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/settings/roles/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/settings/roles/spec.md`
