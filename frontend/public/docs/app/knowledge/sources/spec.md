# Spec: Knowledge sources

**Route:** `/app/knowledge/sources`  
**Permission (typical):** knowledge:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Connected knowledge sources with type, status, document counts, last sync, errors.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Sources table + metrics
- Detail routes for individual sources

## Backend / API contracts

- Knowledge source inventory via knowledge APIs / service layer
- Sync status drives freshness indicators

## Architecture mapping

- Sources feed semantic/procedural knowledge with provenance records

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/knowledge/sources/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/knowledge/sources/spec.md`
