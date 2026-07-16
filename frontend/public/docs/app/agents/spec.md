# Spec: Agents catalog

**Route:** `/app/agents`  
**Permission (typical):** agents:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

List organization AI workers with status, tools, knowledge access, and ownership before exposing them to live workflows.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Domain pack summary panel (optional domain context)
- Searchable agent table (name, owner, tools, knowledge, status, updated)
- Metrics: total / active / draft / knowledge-linked
- Create agent action → /app/agents/new

## Backend / API contracts

- GET /api/v1/agents
- Agents declare allowed tools and memory scopes; ALC fields may gate activation
- No direct LLM calls from the UI

## Architecture mapping

- Execution layer roster (structure.md §4)
- Domain packs may register additional agents (business/<domain_id>/)

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/agents/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/agents/spec.md`
