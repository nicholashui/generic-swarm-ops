# User guide: Agents catalog

**Screen:** `/app/agents`  
**Who:** Operators with `agents:read` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

List organization AI workers with status, tools, knowledge access, and ownership before exposing them to live workflows.

## Step-by-step

1. Open Agents from the sidebar.
2. Filter or search by owner, status, or knowledge access.
3. Inspect an agent row for tool count and knowledge linkage.
4. Click Create agent when you have agents:write (or admin) rights.
5. Prefer draft → review → active; do not activate high-risk agents without governance checks.

## UI checklist

- [ ] Domain pack summary panel (optional domain context)
- [ ] Searchable agent table (name, owner, tools, knowledge, status, updated)
- [ ] Metrics: total / active / draft / knowledge-linked
- [ ] Create agent action → /app/agents/new

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

- Spec: `/docs/app/agents/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
