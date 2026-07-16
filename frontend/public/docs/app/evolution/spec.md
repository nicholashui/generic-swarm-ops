# Spec: Evolution archive

**Route:** `/app/evolution`  
**Permission (typical):** workflows:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Sandbox population archive: variants ranked by fitness; evaluate/canary without silent production mutation. Lesson utility feeds coevolution fitness.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- EvolutionArchivePanel
- LessonUtilityPanel
- Evaluate / canary promote actions when authorized

## Backend / API contracts

- GET /evolution/archive, /evolution/variants
- POST /evolution/variants/{id}/evaluate, /promote
- POST /evolution/coevolution/run
- GET /improvement/lesson-utility

## Architecture mapping

- Evolution layer: propose → test → canary → promote/rollback (structure.md §5)
- Non-negotiable: never mutate production DNA directly
- Fitness combines quality, safety, compliance, efficiency, human satisfaction minus risk/latency/cost

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/evolution/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/evolution/spec.md`
