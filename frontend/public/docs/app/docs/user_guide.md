# User guide: Full-page document viewer

**Screen:** `/app/docs`  
**Who:** Operators with `authenticated (app shell)` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Dedicated markdown viewer for static files under public/docs via ?md= path.

## Step-by-step

1. Prefer opening docs from the header book icon (pre-fills md for current route).
2. You may also navigate to /app/docs?md=/docs/app/workflows/spec.md.
3. Missing files show a neutral empty state, not a crash.

## UI checklist

- [ ] FullPageMarkdownDocument
- [ ] Query parameter md=/docs/...

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

- Spec: `/docs/app/docs/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
