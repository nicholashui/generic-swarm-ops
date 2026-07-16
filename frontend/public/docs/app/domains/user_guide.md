# User guide: Domains

**Screen:** `/app/domains`  
**Who:** Operators with `workflows:read` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Multi-domain pack surface: domain inventory, video N3 roster, workflow recommendation, and special-skill registry views.

## Step-by-step

1. Open Domains from the sidebar.
2. Review pack inventory and N3 roster health.
3. Paste a production brief into Recommend Workflow and inspect ranked DNA options.
4. Browse special skills available to the pack; do not enable skills that fail security vetting.
5. Register new packs only through approved inventory + schema gates.

## UI checklist

- [ ] DomainPackPanel — pack/agent inventory context
- [ ] VideoN3RosterPanel — N3 retention roster status
- [ ] RecommendWorkflowPanel — free-text brief → ranked DNA recommendation
- [ ] SpecialSkillsPanel — pack special-skill integrations from REGISTRY

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

- Spec: `/docs/app/domains/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
