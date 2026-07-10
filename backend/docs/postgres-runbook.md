# Postgres runbook (local ops)

Primary durable store for the Generic Swarm backend control plane.

## Prerequisites

- Postgres listening on the host/port in `backend/.env`
- Database and role already created (example: `gsodb` / `gso_agent`)
- Python deps: `SQLAlchemy`, `psycopg[binary]`, `python-dotenv` (see `backend/pyproject.toml`)

## Configuration

`backend/.env` (never commit real secrets):

```env
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@localhost:5432/gsodb
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=5
DATABASE_POOL_PRE_PING=true
```

Template: `backend/.env.example`

The runtime converts `postgresql+asyncpg://` to **`postgresql+psycopg://`** for the sync control plane.

## Start order

1. Start Postgres.
2. From `backend/`:

   ```bash
   cd backend
   set PYTHONPATH=.
   uvicorn app.main:app --reload
   ```

3. Check readiness:

   ```bash
   curl http://127.0.0.1:8000/api/v1/health/ready
   ```

   Expect `"database": "postgres"` when connected.

4. Optional: require Postgres or fail health:

   ```bash
   set GENERIC_SWARM_REQUIRE_POSTGRES=true
   ```

5. Start frontend (ops profile):

   ```bash
   cd frontend
   set NEXT_PUBLIC_DEMO_MODE=false
   set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
   pnpm dev
   ```

## Data layout

| Store | Role |
|-------|------|
| Postgres table `runtime_state` (id=1, `payload` JSONB) | **Primary** runtime document |
| `backend/data/runtime.json` | Snapshot backup written on every save; seed source if DB empty |

First connect with empty `runtime_state` migrates from `runtime.json` if present.

## Offline / tests without Postgres

```bash
set GENERIC_SWARM_FORCE_JSON_STORE=true
```

## Seed login

- `admin@example.com` / `admin-password`
- Static bearer tokens (`admin-token`, …) remain for local smoke only — prefer password login for ops.

## Restart durability check

```bash
cd backend
set PYTHONPATH=.
python -m unittest app.tests.unit.test_postgres_restart -v
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| `store_backend` is `json-file` | Check Postgres up, `DATABASE_URL`, install `psycopg-binary` |
| `libpq library not found` | `pip install "psycopg[binary]"` |
| 503 on `/health/ready` | Unset `GENERIC_SWARM_REQUIRE_POSTGRES` or fix DB connectivity |
