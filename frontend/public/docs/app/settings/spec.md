# Spec: Settings hub

**Route:** `/app/settings`  
**Permission (typical):** settings:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Organization administration hub: profile, org, users, roles, billing, API keys, security, integrations.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Card grid of settings destinations

## Backend / API contracts

- GET /settings and nested admin APIs
- RBAC enforced server-side

## Architecture mapping

- Admin plane separate from execution; still fully audited

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/settings/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/settings/spec.md`
