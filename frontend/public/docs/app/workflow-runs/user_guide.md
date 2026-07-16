# User guide: Workflow runs

**Screen:** `/app/workflow-runs`  
**Who:** Operators with `workflows:read` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Template for run detail screens (/app/workflow-runs/{runId}) — events, improve pipeline, pause/resume/cancel.

## Step-by-step

1. Open a run from a workflow detail or dashboard link.
2. Watch events for step progress and human-gate waits.
3. Approve blocking gates from Approvals when status is awaiting_approval.
4. Use Improve only to propose sandbox variants — never expect silent production mutation.
5. Cancel or expire stuck runs per ops policy.

## UI checklist

- [ ] WorkflowRunConsole with event stream
- [ ] ImproveRunButton (reflect → propose → evaluate → canary)
- [ ] Lifecycle: pause / resume / cancel / expire when allowed

## Safety notes

- Prefer reversible actions; require human approval for irreversible tool effects.
- Do not promote evolution variants without golden/adversarial evaluation evidence.
- Keep secrets out of chat, tickets, and git; use API keys vaulting for machines.

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| Empty / demo data | `NEXT_PUBLIC_DEMO_MODE`, backend up, login cookies |
| 403 on load | Sign in again; role permissions for this screen |
| Stale numbers | Hard refresh; verify API proxy `/api/proxy/*` |
| Help drawer empty | Missing `public/docs/...` markdown for this route |

## Related

- Spec: `/docs/app/workflow-runs/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
