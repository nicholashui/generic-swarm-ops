# User guide: Dashboard

**Screen:** `/app`  
**Who:** Operators with `workflows:read (and related read scopes for tiles)` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Command surface for governed automation: metrics, pending approvals, recent workflows, knowledge freshness, and onboarding checklist.

## Step-by-step

1. Sign in at /login (POST credentials; never put password in the URL).
2. Confirm metrics load (live mode requires backend health ready with Postgres).
3. Open a pending approval or workflow from the tables when attention is needed.
4. Use header help (panel icon) for Spec / User guide tabs on this screen.
5. Use the book icon for a full-page document view of the same markdown.

## UI checklist

- [ ] Metric cards (agents, workflows, pending approvals, audit volume)
- [ ] Pending approvals table with deep links
- [ ] Recent workflows / knowledge status
- [ ] Onboarding checklist for first-time operators
- [ ] Primary actions: Create agent, Create workflow

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

- Spec: `/docs/app/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
