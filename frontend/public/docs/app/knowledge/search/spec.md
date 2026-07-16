# Spec: Knowledge search

**Route:** `/app/knowledge/search`  
**Permission (typical):** knowledge:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Ad-hoc search across the knowledge corpus.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Search input and result list
- Uses GET /knowledge/search?query=

## Backend / API contracts

- GET /api/v1/knowledge/search?query=...
- Optional graph federate POST /knowledge/graph/federate

## Architecture mapping

- Default tier-0 keyword/vector; escalate for multi-hop only when needed

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/knowledge/search/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/knowledge/search/spec.md`
