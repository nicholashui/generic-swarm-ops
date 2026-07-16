# Spec: Tools

**Route:** `/app/tools`  
**Permission (typical):** tools:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Catalog of tool adapters available to workflow steps (CRM, billing, email, parsers, etc.).

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Tool list with category, status, last used, usage
- Detail deep links for individual tools

## Backend / API contracts

- GET /api/v1/tools
- Tool execution only through runtime adapters producing tool_effects
- Permission broker scopes credentials per task

## Architecture mapping

- Execution layer tool adapters; durable tool_effects for audit/rollback
- System prompts are not security controls — permissions enforced outside the LLM

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/tools/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/tools/spec.md`
