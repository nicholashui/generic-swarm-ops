# Spec: Process intelligence

**Route:** `/app/processes`  
**Permission (typical):** processes:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Process mining outputs: discovered processes, conformance, bottlenecks from real event logs.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Process summary metrics
- Process list / detail cards

## Backend / API contracts

- GET /api/v1/processes/summary and related process endpoints
- Artifacts under business/process-intelligence/

## Architecture mapping

- Process Intelligence layer (structure.md §2.3)
- Learn from actual traces, not only SOPs

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/processes/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/processes/spec.md`
