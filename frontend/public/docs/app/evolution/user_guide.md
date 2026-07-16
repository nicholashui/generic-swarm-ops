# User guide: Evolution archive

**Screen:** `/app/evolution`  
**Who:** Operators with `workflows:read` (or stronger)

## Before you start

- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.
- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.
- You are signed in (session cookies set by `POST /api/auth/login`).

## What this screen is for

Sandbox population archive: variants ranked by fitness; evaluate/canary without silent production mutation. Lesson utility feeds coevolution fitness.

## Step-by-step

1. Open Evolution to browse sandbox variants.
2. Inspect fitness and evaluation evidence before canary.
3. Run evaluate on a variant; only canary/promote with sufficient evidence and permissions.
4. Review lesson utility for coevolution signals.
5. If a canary fails metrics, roll back — do not force promote.

## UI checklist

- [ ] EvolutionArchivePanel
- [ ] LessonUtilityPanel
- [ ] Evaluate / canary promote actions when authorized

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

- Spec: `/docs/app/evolution/spec.md`
- Architecture: `structure.md`
- Backend plan: `backend.md`
- Frontend plan: `frontend.md`
