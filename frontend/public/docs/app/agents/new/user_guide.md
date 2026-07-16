# User guide: Create agent

**Screen:** `/app/agents/new`  
**Who:** Operators with `agents:write (or create)` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Form to register a new agent with deliberate tool, memory, and knowledge scope.

## Step-by-step

1. Enter a clear agent name and objective description.
2. Select only the tools required for the role (least privilege).
3. Attach knowledge/memory scopes intentionally.
4. Submit and verify the agent appears in the catalog as draft or registered.
5. Activate only after ALC / inventory gates pass when required.

## UI checklist

- [ ] Create form (name, description, tools, memory scopes, knowledge sources, approval threshold)
- [ ] Submit via FormRouteActions → POST /agents
- [ ] Validation errors surfaced with request_id when available

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

- Spec: `/docs/app/agents/new/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
