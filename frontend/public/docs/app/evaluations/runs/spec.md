# Spec: Evaluation run detail

**Route:** `/app/evaluations/runs`  
**Permission (typical):** evaluations:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Template for /app/evaluations/runs/{runId} detail of a single evaluation execution.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Scores, suite type, timestamps, failure details

## Backend / API contracts

- Evaluation service records per-run outcomes

## Architecture mapping

- Evidence for fitness function components (quality, safety, compliance)

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/evaluations/runs/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/evaluations/runs/spec.md`
