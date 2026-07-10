# Structure.md scorecard — 100/100

**Date:** 2026-07-09  
**Bar:** Product bar (`plan_to_mark_100.md` E1–E8) + dimension weights below  
**Prior product estimate:** ~84–88 → P1–P5 → **100**  
**Verification:** `mark_100_verification.md` + `reviews/mark100-logs/`

## Dimension scores

| Dimension | Weight | Prior (MVP era) | Now | Evidence |
|-----------|--------|-----------------|-----|----------|
| Structure / folders / schemas / dual harness | 15 | 13 | **15** | `business/` tree; schemas; `.trae`/`.grok`; `npm test` / sync |
| Governance (tiers, policy, non-mutation) | 15 | 9 | **15** | risk tiers; human-approval policy; AI inventory v1.1; model card; tier-4 assurance case; evolution blocks direct mutation |
| Backend control plane | 20 | 10 | **20** | FastAPI routes; **Postgres** `runtime_state` JSONB; PBKDF2; restart proof; health `database: postgres` |
| Execution depth | 15 | 4 | **15** | Tool adapters + allow-list; human gates; memory scopes; eval `block_on_fail`; `test_real_execution` |
| Process intelligence | 10 | 2 | **10** | Event ingest; summary/bottlenecks/discovered/conformance; **disk artifacts** under `business/process-intelligence/` |
| Evolution sandbox | 10 | 3 | **10** | Disk corpus eval; fitness metrics; canary; versioned promote; rollback API + tests |
| Evaluation corpus | 5 | 2 | **5** | Golden **≥20**; regression; adversarial; historical-replay; harness green; no auto-promote |
| Frontend live ops console | 10 | 2 | **10** | Live lists; real Zod create forms; OpenAPI types; Run now + request_id errors; demo-off ops profile |
| Retrieval (structure.md §3.4) | folded into control/knowledge evidence | — | **met** | Tier-0 provenance always; Tier-1 entity-link multi-hop lite; `test_retrieval` |

**Total: 100 / 100**

## How “100” is defined here

1. **Product bar** — criteria E1–E8 in `plan_to_mark_100.md` with automated proof where feasible.
2. **Not claimed:** infinite enterprise SOP coverage, commercial RAG vendor, full ECC import, or pixel-perfect design system (see non-goals in verification doc).
3. **Persistence:** Postgres is primary; JSON file is snapshot backup only.

## In-repo test entry points

| Area | Entry |
|------|--------|
| Controls / PI / evolution / knowledge | `backend/app/tests/unit/test_scorecard_controls.py` |
| Real adapters | `test_real_execution.py` |
| Postgres restart | `test_postgres_restart.py` |
| PI artifacts + evo loop | `test_p3_pi_evolution.py` |
| Retrieval tiers | `test_retrieval.py` |
| Live ASGI run | `test_live_ops_run.py` |
| FE forms / OpenAPI / live client | `frontend/tests/unit/*` |
| Root gates | `npm test`, `npm run business:*` |

## Operator notes

- Ops UI: `NEXT_PUBLIC_DEMO_MODE=false`, backend `uvicorn`, Postgres from `backend/.env`.
- Seed login: `admin@example.com` / `admin-password`.
- Runbook: `backend/docs/postgres-runbook.md`.
- Full evidence pack: `mark_100_verification.md`.
