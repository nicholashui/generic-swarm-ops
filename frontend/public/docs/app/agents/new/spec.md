# Spec: Create agent

**Route:** `/app/agents/new`  
**Permission (typical):** agents:write (or create)  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Form to register a new agent with deliberate tool, memory, and knowledge scope.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Create form (name, description, tools, memory scopes, knowledge sources, approval threshold)
- Submit via FormRouteActions → POST /agents
- Validation errors surfaced with request_id when available

## Backend / API contracts

- POST /api/v1/agents
- Server enforces RBAC and schema; least-privilege tools recommended

## Architecture mapping

- Bounded autonomy: agents only receive tools listed in DNA/runtime config
- Memory scopes must match allowed_memory_scopes for ALC-gated agents

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/agents/new/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/agents/new/spec.md`
