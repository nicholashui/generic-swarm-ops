# Spec: Organization settings

**Route:** `/app/settings/organization`  
**Permission (typical):** settings:update (org)  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Brand, locale, retention posture for the tenant.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- OrganizationSettingsForm — name/slug/status fields
- PATCH organization

## Backend / API contracts

- GET/PATCH /organizations/{id}

## Architecture mapping

- Multi-tenant org boundary for agents, memory, and audit

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/settings/organization/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/settings/organization/spec.md`
