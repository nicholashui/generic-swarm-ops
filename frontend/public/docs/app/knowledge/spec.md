# Spec: Knowledge hub

**Route:** `/app/knowledge`  
**Permission (typical):** knowledge:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Hub for sources, indexed documents, and search — grounded retrieval for agents.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Cards linking to sources, documents, search
- Freshness and failure signals

## Backend / API contracts

- GET /knowledge, /knowledge/search
- Tiered retrieval (vector → graph → hierarchical) per structure.md Knowledge layer
- Provenance required for trusted rules

## Architecture mapping

- Eight memory types + retrieval tiers 0–2
- Escalation: start cheap (tier 0), escalate only when needed

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/knowledge/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/knowledge/spec.md`
