# User guide: Audit logs

**Screen:** `/app/audit-logs`  
**Who:** Operators with `audit:read` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Immutable-style operational audit trail for auth, workflow, approval, and tool actions.

## Step-by-step

1. Use Audit Logs for forensics after incidents or customer disputes.
2. Filter by actor or resource when reconstructing a run.
3. Export/share only under org compliance rules.

## UI checklist

- [ ] Chronological audit table with actor, action, resource, outcome
- [ ] Filters by type when provided

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

- Spec: `/docs/app/audit-logs/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
