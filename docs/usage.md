# Usage

## Common Commands

- `npm run bootstrap`
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

## Backend Commands

```bash
cd backend
# backend/.env with DATABASE_URL (see .env.example)
set PYTHONPATH=.
python -m pip install -e .
uvicorn app.main:app --reload
python -m unittest discover -s app/tests/unit -p "test_*.py"
python -m unittest discover -s app/tests/e2e -p "test_*.py"
```

Readiness: `GET http://127.0.0.1:8000/api/v1/health/ready` → `database: postgres`.

## Frontend Commands

```bash
cd frontend
set NEXT_PUBLIC_DEMO_MODE=false
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
pnpm install
pnpm dev
pnpm lint && pnpm typecheck && pnpm test
```

## Seed credentials

- `admin@example.com` / `admin-password` (prefer password login)
- Static bearer tokens (`admin-token`, …) remain for curl smoke only

## Runtime flow (E1)

1. Log in (password → cookie `gso_access_token` + session user cookie).
2. List workflows / agents from live API.
3. Create agent/workflow via real forms (or use flagship `wf_customer_onboarding_v12`).
4. **Run now** with valid payload (`case_id` required for flagship).
5. Approve human-gated billing step as reviewer.
6. Inspect audit logs, memory, evaluations, process summaries.
7. On run detail: **Improve** → Reflect → Propose → Evaluate → Canary (or **Run full pipeline**).
8. Open `/app/evolution` population archive.

## Self-improvement APIs

| Method | Path |
|--------|------|
| POST | `/api/v1/improvement/reflect/{run_id}` |
| GET | `/api/v1/improvement/lessons` |
| POST | `/api/v1/improvement/auto-propose` |
| POST | `/api/v1/loops/run` |
| GET | `/api/v1/evolution/archive` |
| POST | `/api/v1/knowledge/graph/federate` |

## Business artifacts

- Event / PI outputs: `business/process-intelligence/`
- Lessons: `business/evolution/lessons-learned/`
- Golden evals: `business/evals/golden-tasks/`
- Governance: model card + assurance case under `business/governance/`
- Retrieval policy: `business/knowledge-base/provenance/retrieval-tier-policy.md`
