# Spec: Memory

**Route:** `/app/memory`  
**Permission (typical):** memory:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Inspect scoped memory items (event, episodic, semantic, procedural, decision, exception, evaluation, provenance).

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Memory list / filters by scope and type
- Detail for individual items when selected

## Backend / API contracts

- GET /api/v1/memory
- Runtime enforces allowed_memory_scopes on agent reads/writes

## Architecture mapping

- Memory stewardship: provenance, retention, quality controls
- High-impact writes may require human review (memory-poisoning defense)

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/memory/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/memory/spec.md`
