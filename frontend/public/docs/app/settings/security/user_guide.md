# User guide: Security settings

**Screen:** `/app/settings/security`  
**Who:** Operators with `settings:read` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Session, MFA posture, allowed domains, and security controls summary.

## Step-by-step

1. Review session and domain allowlists with security owners.
2. Enable MFA when offered by the deployment.
3. Treat security settings changes as high-impact and audit them.

## UI checklist

- [ ] Security configuration panels

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

- Spec: `/docs/app/settings/security/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
