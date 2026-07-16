# Spec: Integrations

**Route:** `/app/settings/integrations`  
**Permission (typical):** settings:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Connected systems and automation endpoints configuration overview.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Integration list / status

## Backend / API contracts

- Tool adapters and external systems behind the API

## Architecture mapping

- Integrations execute only through governed tool adapters

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/settings/integrations/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/settings/integrations/spec.md`
