# User guide: Memory

**Screen:** `/app/memory`  
**Who:** Operators with `memory:read` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Inspect scoped memory items (event, episodic, semantic, procedural, decision, exception, evaluation, provenance).

## Step-by-step

1. Open Memory to audit what agents can recall.
2. Filter by scope (organization, agent, case) when diagnosing wrong decisions.
3. Treat unprovenanced high-impact memories as untrusted.
4. Retention and deletion follow org data-retention policy.

## UI checklist

- [ ] Memory list / filters by scope and type
- [ ] Detail for individual items when selected

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

- Spec: `/docs/app/memory/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
