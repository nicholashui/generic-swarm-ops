# Spec: Billing

**Route:** `/app/settings/billing`  
**Permission (typical):** settings:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Commercial plan and invoicing posture (feature-flag aware).

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Plan / billing status cards

## Backend / API contracts

- Billing feature may be gated by NEXT_PUBLIC_ENABLE_BILLING
- No payment secrets in the frontend

## Architecture mapping

- Commercial metadata only; not part of execution safety core

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/settings/billing/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/settings/billing/spec.md`
