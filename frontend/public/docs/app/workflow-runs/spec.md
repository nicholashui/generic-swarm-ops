# Spec: Workflow runs

**Route:** `/app/workflow-runs`  
**Permission (typical):** workflows:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Template for run detail screens (/app/workflow-runs/{runId}) — events, improve pipeline, pause/resume/cancel.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- WorkflowRunConsole with event stream
- ImproveRunButton (reflect → propose → evaluate → canary)
- Lifecycle: pause / resume / cancel / expire when allowed

## Backend / API contracts

- GET /workflow-runs, /workflow-runs/{id}/stream
- POST improve/reflect, improvement/auto-propose, evolution evaluate/promote
- POST pause/resume/cancel/expire

## Architecture mapping

- Runtime walks DNA graph; tool_effects + audit on each step
- Self-improvement writes lessons; variants stay sandbox until approved

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/workflow-runs/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/workflow-runs/spec.md`
