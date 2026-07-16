# Spec: Evaluations

**Route:** `/app/evaluations`  
**Permission (typical):** evaluations:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Golden / regression / adversarial / historical-replay evaluation results for workflows and variants.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Evaluation runs table
- Detail under /app/evaluations/runs/{id}

## Backend / API contracts

- GET /api/v1/evaluations
- Eval corpus under business/evals/
- Promotion blocked without passing required checks

## Architecture mapping

- Everything is testable (structure.md principles)
- Evaluation layer gates evolution promotion

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/evaluations/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/evaluations/spec.md`
