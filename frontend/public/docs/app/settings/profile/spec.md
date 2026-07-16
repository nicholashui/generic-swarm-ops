# Spec: User profile

**Route:** `/app/settings/profile`  
**Permission (typical):** authenticated user  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Current user profile display and self-service profile fields when enabled.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Profile summary for the session user

## Backend / API contracts

- GET /auth/me
- Optional PATCH user self fields

## Architecture mapping

- Session established via password login BFF cookies

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/settings/profile/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/settings/profile/spec.md`
