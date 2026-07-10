# generic-swarm-ops

Governed, auditable, self-improving multi-agent business operating system for **Trae IDE** and **Grok Build** (dual-harness).

**Product bar:** mark **~100/100** (`structure_scorecard_100.md`, `mark_100_verification.md`) with E1 operator path green (`reviews/e1_operator_checklist.md`).

## Quick start

```bash
npm run bootstrap
```

Bootstrap keeps the starter layer intact, then validates the business operating-system layer.

Approved upstream repositories are downloaded into:

```text
external/sources/
```

Bootstrap and supporting commands write:

```text
sources/source-lock.json
docs/source-audit.md
.trae/
.grok/
business/
backend/
```

## Agent harnesses

| Harness | Generated tree | Notes |
|---------|----------------|--------|
| Trae IDE | `.trae/` | Settings, agents, commands, rules |
| Grok Build | `.grok/` | Rules, agents, skills, commands |

Shared source of truth: `rules/`, `skills/`, `hooks/`, `mcp-configs/`, and `scripts/adapters/shared.mjs`.

```bash
npm run sync          # regenerate .trae/* and .grok/*
npm run sync:check    # verify managed files exist
```

At session start (either harness), read `memory/handoff.md` and `memory/project.md` when present.

See `docs/trae.md`, `docs/grok.md`, `docs/sync.md`, and `migrate_to_grok_build.md`.

## Core Commands

- `npm run doctor`
- `npm run sources:download`
- `npm run sources:audit`
- `npm run sync`
- `npm run business:init`
- `npm run business:validate`
- `npm run business:governance`
- `npm run business:security`
- `npm run business:evolution:check`
- `npm run business:eval`

## What is shipped (product bar)

| Area | Status |
|------|--------|
| **Persistence** | Postgres primary (`runtime_state` JSONB); JSON snapshot backup |
| **Execution** | Local tool adapters + `tool_effects` + human gates |
| **Process intelligence** | Event ingest → discovered / conformance / bottlenecks artifacts |
| **Evolution** | Disk corpus eval, fitness, canary, versioned promote, rollback |
| **Self-improvement** | Auto-reflect, lesson library, auto-propose sandbox variants, Loop runner |
| **Knowledge** | Tier-0 keyword + embeddings; Tier-1 entity multi-hop; K1-lite graph + federation export |
| **Evaluation corpus** | ≥20 golden tasks + regression / adversarial / historical-replay |
| **Frontend** | Live ops (`NEXT_PUBLIC_DEMO_MODE=false`), real create forms, Improve pipeline, Evolution archive |
| **Evidence** | E1 e2e test, unit suites, Playwright smoke |

## Backend Runtime

FastAPI under `backend/` — control plane from `structure.md` / `backend.md`.

Key capabilities:

- password + bearer auth, RBAC
- workflow DNA execution with approvals
- tool adapters (crm, billing, email, audit, contract_parser, policy_retriever)
- memory scopes, knowledge search / graph, audit logs
- process intelligence + evolution + **improvement** + **loops** APIs
- Postgres durability; health/ready reports `database: postgres`

```bash
cd backend
# configure backend/.env (see backend/.env.example and docs/postgres-runbook.md)
set PYTHONPATH=.
uvicorn app.main:app --reload
# GET /api/v1/health/ready
```

Seed login: `admin@example.com` / `admin-password`

## Frontend

```bash
cd frontend
set NEXT_PUBLIC_DEMO_MODE=false
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
pnpm install
pnpm dev
```

Ops surfaces include agents, workflows, **Run now**, approvals, knowledge, evaluations, processes, **Improve** on runs, and **`/app/evolution`** archive.

## Docs map

| Doc | Topic |
|-----|--------|
| `structure.md` | Architecture source of truth |
| `plan_to_mark_100.md` | Product-bar plan (P0–P5 done) |
| `docs/self-improvement-and-orchestration.md` | Self-evolving / loops / K1-lite |
| `docs/architecture.md` | Layered architecture |
| `backend/docs/postgres-runbook.md` | Postgres ops |
| `book/book.md` | Full technical book |
| `memory/handoff.md` | Session continuity |

## License / policy

- `external/sources/` is untrusted until audited.
- Evolution never mutates production DNA directly (sandbox → canary only).
