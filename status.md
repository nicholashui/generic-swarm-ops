# Status

## Current phase

**Mark 100** (product bar) complete. **E1 operator path PASS.** Self-improvement / Loop Engineering / K1-lite knowledge orchestration shipped.

## Latest update

- Closed `plan_to_mark_100.md` P0–P5: Postgres primary store, real tool adapters, PI disk artifacts, evolution corpus/fitness/canary/rollback, FE real forms + OpenAPI, ≥20 golden tasks, tiered retrieval.
- E1 API path verified (`reviews/e1_operator_checklist.md`, `backend/app/tests/e2e/test_e1_operator_path.py`): login → create agent → flagship run → human gate → complete → reflect → propose → evaluate → canary.
- Fixed flagship agents’ memory scopes so `memory_reads` no longer fail mid-run.
- Self-improvement: auto-reflect, lesson library, auto-propose, Loop DNA runner, optional LLM critic, skill sandbox.
- FE: Improve pipeline (Reflect → Propose → Evaluate → Canary), `/app/evolution` archive, Playwright smoke.
- Scorecard: `structure_scorecard_100.md` / `mark_100_verification.md` at **100/100** (product bar). FE lint fixed (0 errors).
- Branch/PR: `feat/mark-100-self-improvement-e1` / https://github.com/nicholashui/generic-swarm-ops/pull/1

## Commands (green)

```bash
# Root
npm test
npm run business:validate
npm run business:eval

# Backend
cd backend
set PYTHONPATH=.
python -m unittest discover -s app/tests/unit -p "test_*.py" -v
python -m unittest discover -s app/tests/e2e -p "test_*.py" -v

# Frontend
cd frontend
pnpm lint
pnpm typecheck
pnpm test
```

## Seed login

- `admin@example.com` / `admin-password`

## Structure SDD close-out

- Specs under `planning/structure/` (requirements + design + tasks) executed; tasks marked `[x]`.
- Gap report goal **100/100**: `planning/gap_analysis_for_structure.md`.
- Added: elicitation templates, DNA/DRC negative validators, role map, runtime tier policy, rejection→lesson.
- **Runtime enforcement:** production DNA validation on `activate_workflow_version` / `production_ready` create-update (`structure_validators` + unit tests).

## Remaining non-goals / later

- Full LightRAG vendor / Neo4j production mesh
- Live external CRM/email adapters
- DGM-style host code self-rewrite
- Full Playwright UI CI with always-on servers
- Ephemeral per-tool OAuth credential broker (when live SaaS adapters land)
