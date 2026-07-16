# User guide: Knowledge hub

**Screen:** `/app/knowledge`  
**Who:** Operators with `knowledge:read` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Hub for sources, indexed documents, and search — grounded retrieval for agents.

## Step-by-step

1. Open Knowledge to assess corpus health.
2. Use Sources to manage connectors; Documents for corpus rows; Search for ad-hoc queries.
3. Investigate failed ingestions before relying on agents that need those sources.
4. Prefer documents with clear provenance for compliance-sensitive workflows.

## UI checklist

- [ ] Cards linking to sources, documents, search
- [ ] Freshness and failure signals

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

- Spec: `/docs/app/knowledge/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
