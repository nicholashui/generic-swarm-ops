# Spec: Create workflow

**Route:** `/app/workflows/new`  
**Permission (typical):** workflows:write  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Form to create a new Workflow DNA record through the live API.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Create form fields for identity and configuration
- POST via FormRouteActions → /workflows

## Backend / API contracts

- POST /api/v1/workflows
- Server-side schema and governance constraints

## Architecture mapping

- New DNA should follow bounded steps + guardrails + rollback pattern
- Prefer validation commands: npm run business:validate (repo root)

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/workflows/new/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/workflows/new/spec.md`
