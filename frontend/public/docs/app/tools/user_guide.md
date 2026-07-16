# User guide: Tools

**Screen:** `/app/tools`  
**Who:** Operators with `tools:read` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Catalog of tool adapters available to workflow steps (CRM, billing, email, parsers, etc.).

## Step-by-step

1. Open Tools to review connected integrations.
2. Check status (connected / error) before assigning tools to agents.
3. Open a tool detail when diagnosing failed workflow steps.
4. Never grant irreversible tools without human gates in Workflow DNA.

## UI checklist

- [ ] Tool list with category, status, last used, usage
- [ ] Detail deep links for individual tools

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

- Spec: `/docs/app/tools/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
