# Generic Swarm Ops Frontend

Enterprise Next.js frontend for the governed AI business automation platform.

## Implemented Surface

- Public landing page plus auth routes for `login`, `register`, `forgot-password`, `reset-password`, and `accept-invite`.
- Authenticated `/app` dashboard with live (or demo) data.
- Dynamic `/app/[...slug]` covering agents, tools, workflows, workflow runs, approvals, knowledge, memory, evaluations, processes, audit logs, settings, and **evolution**.
- **Real** agent/workflow create forms (Zod + react-hook-form); mutation errors include backend message + `request_id`.
- **Run now** with valid payload builder (`case_id`, …).
- **Improve pipeline** on run detail: Reflect → Propose → Evaluate → Canary (or full pipeline).
- **Population archive** at `/app/evolution` (fitness ranking, eval/canary actions).

## Commands

```bash
pnpm install
pnpm dev
pnpm lint
pnpm typecheck
pnpm test
pnpm build
pnpm api:generate
pnpm test:e2e            # Playwright smoke (skips if servers down)
# E2E_START=1 pnpm test:e2e   # auto-start Next for UI smoke
```

## Notes

- Uses a documented fallback design workflow because the required `opendesign` MCP server is not currently available in this workspace.
- Targets the existing FastAPI backend under `../backend`.
- Defaults to demo mode for local preview unless `NEXT_PUBLIC_DEMO_MODE=false`.
- **Ops profile (recommended):** `NEXT_PUBLIC_DEMO_MODE=false` with a running backend and Postgres.
- **Demo profile:** leave `NEXT_PUBLIC_DEMO_MODE` unset/true for UI-only preview without live mutations.
- OpenAPI: `pnpm api:generate` exports FastAPI schema to `openapi.json` and generates `src/lib/api/generated/openapi.d.ts`.
- Create agent/workflow routes use real form fields (Zod + react-hook-form); mutation errors show backend message + `request_id`.
- Verified with `pnpm lint`, `pnpm typecheck`, `pnpm test`, and `pnpm build`.
