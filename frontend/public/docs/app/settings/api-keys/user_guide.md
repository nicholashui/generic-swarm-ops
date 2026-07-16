# User guide: API keys

**Screen:** `/app/settings/api-keys`  
**Who:** Operators with `settings:read / settings:update` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Machine credentials for automation; masked display after mint.

## Step-by-step

1. Create keys with descriptive names and store secrets in a vault immediately.
2. Revoke unused or leaked keys without delay.
3. Never commit API keys to git or docs.

## UI checklist

- [ ] ApiKeyTable — list, create, revoke
- [ ] Secret shown once at creation

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

- Spec: `/docs/app/settings/api-keys/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
