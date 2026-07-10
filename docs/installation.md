# Installation

## Requirements

- **Node.js 20+** and npm
- **Git**
- **Python 3.11+** (backend)
- **PostgreSQL 14+** (primary runtime store; local or Docker)
- **pnpm** (frontend; via `corepack enable` or standalone install)

## Full setup

```bash
# 1) Starter + business layer
npm run bootstrap

# 2) Postgres — create DB and set backend/.env (see backend/docs/postgres-runbook.md)
# DATABASE_URL=postgresql://user:pass@localhost:5432/generic_swarm_ops

# 3) Backend
cd backend
python -m pip install -e .
set PYTHONPATH=.
uvicorn app.main:app --reload
# Ready when: GET /api/v1/health/ready → "database": "postgres"

# 4) Frontend (ops profile)
cd frontend
set NEXT_PUBLIC_DEMO_MODE=false
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
pnpm install
pnpm dev
```

## Seed login

- `admin@example.com` / `admin-password`

## Business layer commands

```bash
npm run business:init
npm run business:validate
npm run business:governance
npm run business:security
npm run business:evolution:check
npm run business:eval -- --dry-run
```

`starter.md` baseline is already executed for this repo. Ongoing work is validating and extending the business OS + runtime.

## Dual harness

```bash
npm run sync          # regenerate .trae/ and .grok/
npm run sync:check
```

## Optional env flags

| Variable | Purpose |
|----------|---------|
| `GENERIC_SWARM_AUTO_REFLECT` | Auto-reflect on terminal runs (default true) |
| `GENERIC_SWARM_LLM_CRITIC_ENABLED` | Optional LLM critic |
| `GENERIC_SWARM_EMBEDDINGS_ENABLED` / `GENERIC_SWARM_PGVECTOR_ENABLED` | Retrieval embeddings |
| `NEO4J_URI` | Optional graph federation push |

See `docs/usage.md` and `backend/.env.example`.
