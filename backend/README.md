# Backend

FastAPI backend for the governed runtime described in `structure.md` and `backend.md`.

## What it provides

- token-based authentication and role checks
- API key creation, listing, revocation, and password reset support
- workflow listing, versioning, and queued execution
- workflow update, disable/archive, and run idempotency support
- workflow run dispatch, tracking, retry, cancellation, and streaming
- governance and approval gates
- memory and knowledge retrieval with basic CRUD/search endpoints
- audit log capture
- evaluation listing and manual run access
- process intelligence summaries, metrics, bottlenecks, costs, failures, and approval delays
- health, readiness, liveness, request IDs, CORS, and basic security headers
- in-memory rate limiting for sensitive auth and workflow-write endpoints
- structured error envelopes with request IDs for handled and unhandled failures
- request metrics and structured API request logging
- **Postgres primary persistence** (`DATABASE_URL` in `backend/.env`) with JSONB `runtime_state`
- JSON file snapshot backup + migrate-from-JSON on empty DB
- Local tool adapters (crm, billing, email, audit, contract_parser, policy_retriever) with durable `tool_effects`
- Evolution sandbox (corpus eval, canary, versioned promote, rollback, fitness archive)
- Self-improvement (auto-reflect, lessons, auto-propose, Loop DNA runner, skill sandbox)
- Knowledge: tiered retrieval + embeddings, K1-lite graph operators, federation export
- Process intelligence: event ingest writes disk artifacts under `business/process-intelligence/`

## Quick start

```bash
# 1) Postgres up + backend/.env configured (see docs/postgres-runbook.md)
cd backend
python -m pip install -e .
# PYTHONPATH=.
uvicorn app.main:app --reload
```

Readiness: `GET /api/v1/health/ready` should report `"database": "postgres"`.

Full Postgres ops: **`docs/postgres-runbook.md`**.

## Demo tokens (local smoke only)

Prefer password login for ops. Static tokens remain for quick curl smoke:

- `owner-token`
- `admin-token`
- `operator-token`
- `reviewer-token`

## Seed credentials

- `owner@example.com` / `owner-password`
- `admin@example.com` / `admin-password`
- `operator@example.com` / `operator-password`
- `reviewer@example.com` / `reviewer-password`

## Tests

```bash
set PYTHONPATH=.
python -m unittest discover -s app/tests/unit -p "test_*.py" -v
python -m unittest discover -s app/tests/e2e -p "test_*.py" -v
```

## Key env flags (see `.env.example`)

- `DATABASE_URL` — Postgres
- `GENERIC_SWARM_AUTO_REFLECT` — default true
- `GENERIC_SWARM_LLM_CRITIC_ENABLED` — optional
- `GENERIC_SWARM_EMBEDDINGS_ENABLED` / `GENERIC_SWARM_PGVECTOR_ENABLED`
- `NEO4J_URI` — optional federation push
