# Troubleshooting

## Starter / bootstrap

- Run `npm run doctor` for local prerequisites.
- Inspect `sources/source-lock.json` for clone failures.
- Inspect `docs/source-audit.md` for audit warnings.
- Run `npm run business:init` if required business seed files are missing.
- Run `npm run business:validate` for schema, provenance, risk-tier, or workflow-gate failures.
- Run `npm run business:security` for secrets, unsafe permissions, or prompt-injection coverage gaps.
- Run `npm run business:evolution:check` if sandbox promotion evidence is incomplete.

## Backend / Postgres

| Symptom | Check |
|---------|--------|
| Ready shows no postgres | `DATABASE_URL` in `backend/.env`; Postgres running; `GET /api/v1/health/ready` |
| Empty DB after restart | Primary store is Postgres JSONB; JSON file is **backup only** — ensure DB is the same instance |
| Auth fails | Prefer password login (`admin@example.com` / `admin-password`); static tokens are smoke-only |
| Tool step fails closed | Inspect `tool_effects` and audit `tool.executed`; adapters reject missing inputs |
| Flagship run fails mid-run on memory | Agents need correct `allowed_memory_scopes` (seed/normalize union includes organization scopes) |
| Import / PYTHONPATH errors | From `backend/`: `set PYTHONPATH=.` then re-run tests or uvicorn |

Full Postgres ops: `backend/docs/postgres-runbook.md`.

## Frontend

| Symptom | Check |
|---------|--------|
| Demo data only | Set `NEXT_PUBLIC_DEMO_MODE=false` and point `NEXT_PUBLIC_API_BASE_URL` at backend |
| Mutations show no detail | Backend error envelope includes `message` + `request_id` — open network tab |
| Playwright smoke skipped | Start backend + frontend, or `E2E_START=1 pnpm test:e2e` for Next auto-start |
| OpenAPI types drift | From `frontend/`: `pnpm api:generate` with backend export available |

## Evolution / improve

- Variants stay **sandbox-only** until evaluate → canary / versioned promote.
- `auto_promote` is always blocked.
- Skill proposals land under `business/distilled/skills/_sandbox/` until explicit promote.

## Useful verification

```bash
npm test
cd backend && set PYTHONPATH=. && python -m unittest discover -s app/tests/unit -p "test_*.py" -v
cd frontend && pnpm lint && pnpm typecheck && pnpm test
```
