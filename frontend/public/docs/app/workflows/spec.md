# Spec: Workflows

**Route:** `/app/workflows`  
**Permission (typical):** workflows:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

List Workflow DNA definitions available for governed execution.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Workflow table / cards with status and metadata
- Create workflow → /app/workflows/new
- Run now on detail (separate route)
- Flagship example: wf_customer_onboarding_v12

## Backend / API contracts

- GET /api/v1/workflows
- POST /api/v1/workflows/{id}/run with input_payload
- DNA validation: human gates, rollback, provenance, audit writes

## Architecture mapping

- Workflow DNA is a bounded state graph (structure.md Execution layer)
- Evolution never mutates production DNA directly

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/workflows/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/workflows/spec.md`
