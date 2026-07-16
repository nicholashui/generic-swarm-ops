# User guide: Create workflow

**Screen:** `/app/workflows/new`  
**Who:** Operators with `workflows:write` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Form to create a new Workflow DNA record through the live API.

## Step-by-step

1. Fill identity (id/name/domain/objective) carefully; encode version in id when appropriate.
2. Declare steps, tools, and human gates for irreversible actions.
3. Submit and open the new workflow to verify it lists correctly.
4. Do not promote untested DNA to high autonomy tiers.

## UI checklist

- [ ] Create form fields for identity and configuration
- [ ] POST via FormRouteActions → /workflows

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

- Spec: `/docs/app/workflows/new/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
