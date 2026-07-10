# Architecture

The repository combines a dual-harness starter (Trae + Grok), a business operating-system layer, a FastAPI control plane, and a Next.js ops console.

## Layers

| Layer | Role |
|-------|------|
| **Starter / harness** | Manifests, source download/audit, `npm run sync` → `.trae/` + `.grok/` |
| **Business** | Process intelligence, knowledge/memory, governance, evals, evolution sandbox artifacts under `business/` |
| **Backend runtime** | FastAPI control plane: auth, workflows, adapters, approvals, knowledge, memory, PI, evolution, improvement, loops |
| **Frontend** | Next.js ops console: live lists/forms when `NEXT_PUBLIC_DEMO_MODE=false` |
| **Generated** | Managed agent/rules files under `.trae/` and `.grok/` (do not hand-edit) |

## Persistence

- **Primary:** Postgres table `runtime_state` (JSONB document) via `DATABASE_URL` in `backend/.env`
- **Backup:** `backend/data/runtime.json` snapshot on every save; seed source if DB empty
- **Health:** `GET /api/v1/health/ready` → `"database": "postgres"` when connected

## Backend runtime

- `backend/app/main.py` — FastAPI app, middleware (request id, CORS, security headers)
- `backend/app/runtime.py` — governed engine (workflows, gates, memory scopes, store)
- `backend/app/infrastructure/tools/adapters.py` — real local tool adapters + `tool_effects`
- `backend/app/infrastructure/self_improvement/` — reflect, lessons, optional LLM critic, skill sandbox
- `backend/app/infrastructure/loop_engineering/` — Loop DNA + stop/continue runner
- `backend/app/infrastructure/knowledge/` — tiered retrieval + embeddings
- `backend/app/infrastructure/knowledge_orchestration/` — K1-lite extract, operators, federation
- `backend/app/infrastructure/process_intelligence/` — PI disk artifacts
- `backend/app/infrastructure/evolution/` — corpus eval against `business/evals/*`
- API routes include: auth, workflows, runs, approvals, knowledge (+ graph), memory, processes, evolution, **improvement**, **loops**, settings, health

## Business mapping

- `business/process-intelligence/` — event logs + generated discovered/conformance/bottleneck JSON
- `business/knowledge-base/` — rules, provenance, retrieval policy, federation exports
- `business/evolution/` — DNA, successful variants, lessons-learned artifacts
- `business/evals/` — golden (≥20), regression, adversarial, historical-replay, retrieval fixtures
- `business/governance/` — inventory, model card, assurance case, risk tiers, approval policy

## Runtime behavior

1. Operator logs in (password preferred; static tokens smoke-only).
2. Workflow run executes bounded steps; tools leave audited `tool_effects`.
3. Human-gated irreversible steps pause for approval.
4. On terminal status, **auto-reflect** writes lessons (and optional sandbox propose).
5. Evolution variants are sandbox-only until evaluate → canary / versioned promote.
6. Knowledge search: Tier 0 keyword+embedding; Tier 1 entity multi-hop; graph operators O1/O2/O5.

## Frontend behavior

- Ops profile: `NEXT_PUBLIC_DEMO_MODE=false` + API base to backend
- Real agent/workflow create forms (Zod + RHF); errors include `request_id`
- Run detail: Improve pipeline Reflect → Propose → Evaluate → Canary
- `/app/evolution` — population archive by fitness

## References

- `structure.md` — design source of truth
- `docs/self-improvement-and-orchestration.md` — self-evolving / loops / K1 mapping
- `backend/docs/postgres-runbook.md` — local Postgres ops
- `mark_100_verification.md` — product-bar evidence
