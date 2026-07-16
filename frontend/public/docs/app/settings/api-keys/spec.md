# Spec: API keys

**Route:** `/app/settings/api-keys`  
**Permission (typical):** settings:read / settings:update  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Machine credentials for automation; masked display after mint.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- ApiKeyTable — list, create, revoke
- Secret shown once at creation

## Backend / API contracts

- GET/POST /auth/api-keys, DELETE /auth/api-keys/{id}
- Keys authenticate as bearer tokens

## Architecture mapping

- Service accounts still subject to RBAC and audit

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/settings/api-keys/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/settings/api-keys/spec.md`
