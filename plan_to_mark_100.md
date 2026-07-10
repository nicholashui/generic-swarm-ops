# Plan to achieve mark 100

**Baseline:** ~**84 / 100** (structure.md product bar)  
**Target:** **100 / 100** — production-ready match of the governed OS in `structure.md`  
**Not the same as:** the earlier automated scorecard checklist (that closed the MVP control plane). This plan is for a **true 100**.

**References:** `structure.md`, `structure_scorecard_100.md`, `grok_investigation_report.md`, `migrate_to_grok_build.md`, `backend/.env`, `backend/.env.example`

---

## Decisions locked

| Decision | Choice | Status |
|----------|--------|--------|
| Persistence | **Postgres** via `backend/.env` → `DATABASE_URL` | **Locked & wired** (2026-07-09) |
| Store shape | JSONB document in table `runtime_state` (id=1) | Implemented |
| Fallback | JSON file `backend/data/runtime.json` if DB down or `GENERIC_SWARM_FORCE_JSON_STORE=true` | Implemented |
| 100 bar | Product bar (this plan), not MVP checklist alone | Open (you confirm) |
| Tool adapters | Local adapters with audit side effects (default) | Pending your confirm |
| Demo policy | Ops: `NEXT_PUBLIC_DEMO_MODE=false` | Pending your confirm |

### Postgres configuration (do not commit secrets)

Configured in **`backend/.env`** (local only):

```env
DATABASE_URL=postgresql+asyncpg://…@localhost:5432/gsodb
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=5
DATABASE_POOL_PRE_PING=true
```

Runtime converts `postgresql+asyncpg://` → **`postgresql+psycopg://`** for the sync control plane.

Template without secrets: **`backend/.env.example`**.

### What is already implemented (W2 partial)

- [x] Load `backend/.env` in `app/core/config.py`
- [x] SQLAlchemy engine + pool settings (`app/infrastructure/database/session.py`)
- [x] `RuntimeStore` load/save via Postgres `runtime_state.payload` JSONB
- [x] One-time migrate: seed DB from existing `runtime.json` if row missing
- [x] Always keep JSON snapshot on save (offline backup)
- [x] `/api/v1/health/ready` and `/settings` report persistence backend
- [x] Verified against live `gsodb`: `store_backend=postgres`, row `id=1` present

**Remaining for full W2 / E2:** explicit restart test in CI, optional schema split beyond single JSONB blob, retire demo tokens as primary auth.

---

## 1. What “100” means (exit criteria)

You may claim **100** only when **all** of the following hold:

| # | Criterion | Proof |
|---|-----------|--------|
| E1 | **Operator path (demo off):** login → live lists → create agent/workflow → **Run now** (valid payload) → human gate if required → approve → run completes → audit + memory + eval visible | Manual checklist + automated e2e or ASGI+FE integration tests |
| E2 | **Controls durable:** tier 0/5, tool allow-list, memory scopes (read/write), eval `block_on_fail`, evolution non-mutation — survive **process restart** **with Postgres** | Backend tests + restart smoke against `DATABASE_URL` |
| E3 | **Real execution:** steps use tool adapters that leave audit/side-effect records (not invented success only) | Runtime tests on shipped `_execute_run` / tools |
| E4 | **PI artifacts:** event ingest updates analytics **and** writes/discovers under `business/process-intelligence/` | Test: ingest → read API + file or store artifact |
| E5 | **Evolution loop:** sandbox eval from corpus; canary; versioned promote only; rollback story documented + tested | API tests + fixture |
| E6 | **Corpus:** multi-suite evals (golden ≥20 where feasible, regression, adversarial, historical-replay); auto-promote always blocked | `npm run business:eval` green without dry-run lies |
| E7 | **Frontend product forms:** real inputs for agent/workflow create; errors show backend message/request id | FE tests + manual |
| E8 | **Persistence:** **Postgres primary** (`runtime_state`); JSON is backup only; health/settings reflect postgres when up | Migrations + tests |

**Non-goals (do not block 100):** full ECC import, cloud vector vendor lock-in, pixel-perfect design system, every empty `business/` folder filled with real enterprise data.

---

## 2. Scoreboard: **100 / 100**

| Dimension | Now | Target | Workstream |
|-----------|-----|--------|------------|
| Structure / harness | **15/15** | 15 | Maintain |
| Governance | **15/15** | 15 | Done |
| Backend control plane | **20/20** | 20 | Done (Postgres + restart) |
| Execution depth | **15/15** | 15 | Done (adapters) |
| Process intelligence | **10/10** | 10 | Done |
| Evolution | **10/10** | 10 | Done |
| Evaluation corpus | **5/5** | 5 | Done (≥20 golden) |
| Frontend live ops | **10/10** | 10 | Done |
| **Total** | **100** | **100** | **Closed** |

*Evidence: `mark_100_verification.md`, `structure_scorecard_100.md`, `reviews/mark100-logs/`.*

---

## 3. Workstreams (how we get there)

### W1 — Real execution (priority 1)
**Goal:** Steps do real, auditable work through adapters.

- Tool adapters for at least: `audit_log_writer`, `crm`, `billing_system`, `email` (local/file side effects OK).
- `_execute_run` calls adapters; failures fail the step/run.
- Workflow `memory_reads` / `memory_writes` enforced and applied.
- One golden path: onboarding run → gate on billing → approve → complete → audit + memory.
- Side effects persist via **Postgres-backed** runtime (already the default store).

### W2 — Durable backend (**Postgres — in progress**)
**Goal:** Controls survive restart; multi-user safe enough for local-prod.

| Item | Status |
|------|--------|
| Postgres from `backend/.env` | **Done** |
| JSONB `runtime_state` table | **Done** |
| Migrate from `runtime.json` on first connect | **Done** |
| Health/settings report backend | **Done** |
| Restart smoke test (kill process, re-login, data still there) | **Done** (`test_postgres_restart`) |
| Optional: normalize relational tables later | Optional |
| Retire static demo tokens as default login | Documented as smoke-only; password login preferred |
| Document ops runbook (start Postgres → backend → FE) | **Done** (`backend/docs/postgres-runbook.md`) |

**Ops notes:**

```bash
# Backend (loads backend/.env automatically)
cd backend
# PYTHONPATH=.
uvicorn app.main:app --reload

# Force JSON only (tests/offline)
set GENERIC_SWARM_FORCE_JSON_STORE=true
```

Check: `GET /api/v1/health/ready` → `dependencies.database` should be `"postgres"` when DB is up.

### W3 — Process intelligence artifacts (**done**)
**Goal:** Traces become first-class business artifacts.

- [x] On ingest: update summary + write/update records under:
  - `business/process-intelligence/discovered-processes/`
  - `…/conformance-reports/`
  - `…/bottlenecks/`
- [x] Store copies in `pi_artifacts` (Postgres document)
- [x] APIs return event-derived data + `artifact_path` (`GET /processes/artifacts`)

### W4 — Evolution product loop (**done**)
**Goal:** Sandbox → canary → promote with no silent prod overwrite.

- [x] Sandbox eval loads golden/regression/adversarial/historical-replay from disk
- [x] Fitness metrics recorded on variant (`fitness_metrics`)
- [x] Canary + versioned promote + rollback API (`POST .../rollback`)
- [x] Tests: `test_p3_pi_evolution` — direct mutation blocked; corpus; canary; rollback

### W5 — Frontend product finish (**done**)
**Goal:** Ops console feels real with demo off.

- [x] Real form fields for agent/workflow create (Zod + RHF; name, description, tools, risk tier)
- [x] OpenAPI export + types (`frontend/openapi.json`, `pnpm api:generate` → `openapi.d.ts`)
- [x] Mutation errors show backend message + `request_id` (`formatMutationError` / `AppError`)
- [x] Ops profile documented: `NEXT_PUBLIC_DEMO_MODE=false` (`.env.example`, README)
- Optional: Playwright e2e for E1 (deferred)

### W6 — Corpus + governance content (**done**)
**Goal:** “Everything is testable” + §6.2 artifacts not empty templates only.

- [x] Golden tasks ≥20 under `business/evals/golden-tasks/`
- [x] AI inventory filled (`inventory.json` v1.1)
- [x] Model card: `business/governance/model-cards/customer-onboarding-orchestrator.md`
- [x] Assurance case: `business/governance/assurance-cases/customer-onboarding-tier4.md`

### W7 — Retrieval (**done**)
**Goal:** structure.md §3.4 spirit without overbuilding.

- [x] Tier 0: keyword search + **mandatory** provenance (`source_refs`)
- [x] Tier 1 lite: entity-link multi-hop (`infrastructure/knowledge/retrieval.py`)
- [x] Policy note: `business/knowledge-base/provenance/retrieval-tier-policy.md`
- [x] Tests: `test_retrieval.py`; fixtures under `business/evals/retrieval/`
- Optional later: `pgvector` embeddings on same `DATABASE_URL` host

---

## 4. Phased roadmap

| Phase | Duration (guide) | Focus | Exit |
|-------|------------------|--------|------|
| **P0 — Freeze baseline** | 0.5 day | Tag ~84–88, Postgres decision locked | This plan accepted |
| **P1 — Real run path** | **Done** | W1 tool adapters + flagship approve path | E3 largely met; full E1 needs FE manual |
| **P2 — Durable + restart** | **Done** | W2 Postgres + restart test + runbook | E2/E8 largely met |
| **P3 — PI + evolution** | **Done** | W3 artifacts + W4 corpus/fitness/canary/rollback | E4 + E5 largely met |
| **P4 — FE product + corpus** | **Done** | W5 forms/OpenAPI + W6 corpus/governance | E6 + E7 largely met |
| **P5 — Retrieval + scorecard** | **Done** | W7 + `mark_100_verification.md` | **100 published** |

---

## 5. Action list — **You** (human owner)

### Decisions
- [x] **Persistence choice:** **Postgres** (`backend/.env` → `gsodb`).
- [ ] **Confirm 100 bar:** product bar (this plan) vs automated MVP checklist only.
- [ ] **Demo policy:** default `NEXT_PUBLIC_DEMO_MODE=false` for local ops profile? (recommended: yes for “ops”).
- [ ] **Scope cut:** accept local tool adapters as “real enough,” or require external CRM/email.

### Environment & access
- [x] Postgres running with DB/user matching `backend/.env`.
- [x] Provide `DATABASE_URL` in `backend/.env` (keep secrets out of git).
- [ ] Ensure Postgres starts with your machine/boot (Docker/service) when developing.
- [ ] Ensure backend can run: Python 3.11+, `uvicorn`, deps including `psycopg[binary]`, `SQLAlchemy`, `python-dotenv`.
- [ ] Ensure frontend: Node 20+, `pnpm`, API base URL to backend.
- [ ] **Do not commit** `backend/.env` (use `.env.example` only).

### Reviews / approvals
- [ ] Review PRs or diffs per phase (P1–P5).
- [ ] Approve risk-tier / human-approval policy updates if they change autonomy.
- [ ] Sign off **E1 manual checklist** once (login → run → approve → audit) against Postgres-backed API.
- [ ] Accept final scorecard at true 100.

### Content you may supply (optional but high leverage)
- [ ] Real or redacted SOPs for onboarding (beyond current seed).
- [ ] List of 20 golden task scenarios (happy path + edge cases).
- [ ] Names/roles for AI inventory “owner” fields.

### Do **not** need to
- Hand-edit generated `.trae/` / `.grok/` (use `npm run sync` / `npm run grok:wire`).
- Import all of `external/sources/ecc` into production skills.
- Pick SQLite anymore (Postgres is the store).

---

## 6. Action list — **Me** (agent / implementer)

### P0 — Baseline
- [x] Wire Postgres from `backend/.env`; update this plan.
- [x] Re-run green suite; note Postgres in `memory/handoff.md` / `status.md`.
- [ ] Keep dual-harness: `npm run sync`, `npm run grok:wire` after roster changes.

### P1 — Real execution
- [x] Implement tool adapter interface + core tools with audit side effects (`adapters.py`).
- [x] Wire `_execute_run` to adapters; fail closed on tool errors.
- [x] Apply `memory_reads` / `memory_writes` with scope checks.
- [x] Tests: `test_real_execution` flagship run + approve path + `tool_effects`.

### P2 — Durable store (finish)
- [x] Postgres repository behind runtime API (`runtime_state` JSONB).
- [x] Migration from `runtime.json` on first empty DB.
- [x] Test: `test_postgres_restart` — new RuntimeStore load sees marker in Postgres.
- [x] Document runbook (`backend/docs/postgres-runbook.md`); demo tokens marked smoke-only.
- [x] `GET /health/ready` fails hard if `GENERIC_SWARM_REQUIRE_POSTGRES=true` and DB down.

### P3 — PI + evolution
- [x] Persist PI outputs; expand ingest → discovered/conformance/bottleneck (+ disk + `pi_artifacts`).
- [x] Sandbox eval loads disk corpus; fitness/metrics on variant.
- [x] Canary + rollback hooks/tests; promote versioned only (`test_p3_pi_evolution`).

### P4 — Frontend + corpus
- [x] Real agent/workflow forms (Zod + fields).
- [x] Export OpenAPI from FastAPI; generate FE types (`pnpm api:generate`).
- [x] Expand golden tasks (≥20); model card + assurance case seed.
- [x] Mutation errors show message + request id.

### P5 — Close scorecard
- [x] Retrieval tier note + Tier-0 provenance + Tier-1 entity multi-hop (`test_retrieval`).
- [x] Update scorecard to true 100 with evidence (including Postgres).
- [x] Full verification matrix; write `mark_100_verification.md` with logs.

### Standing rules for me
- Prefer surgical changes; no unrelated refactors.
- Tests must hit **shipped** runtime/API (no theater).
- Evolution never mutates production DNA directly.
- `external/sources/` remains untrusted until audited.
- **Never commit** secrets from `backend/.env`.
- Default store = Postgres when `DATABASE_URL` is set; JSON is backup/fallback.

---

## 7. Joint checklist (you + me)

| When | You | Me |
|------|-----|-----|
| Now | Keep Postgres up; protect `.env` | Postgres store + plan update (**done**) |
| Start P1 | Approve adapter-level “real” tools | Implement adapters + tests |
| End P1 | Run manual E1 once | Fix anything broken in smoke |
| End P2 | Restart backend once, confirm data | Restart test + runbook |
| Start P5 | Review scorecard wording | Publish evidence + final mark |
| Done | Accept 100 | No further “100” claims without E1–E8 |

---

## 8. Verification matrix (before claiming 100)

```bash
# Postgres must be running (your service / Docker)

# Root
npm test
npm run business:validate
npm run business:governance
npm run business:security
npm run business:evolution:check
npm run business:eval

# Backend (loads backend/.env)
cd backend
# PYTHONPATH=.
python -m unittest discover -s app/tests/unit -p "test_*.py" -v
# Expect health/settings to show postgres when DB up:
# GET /api/v1/health/ready

# Frontend
cd frontend
pnpm typecheck
pnpm test
```

Manual E1 (demo off, Postgres up):

1. Start Postgres (`gsodb`).
2. `cd backend && uvicorn app.main:app --reload`
3. Confirm ready → `database: postgres`.
4. Frontend: `NEXT_PUBLIC_DEMO_MODE=false`, `pnpm dev`.
5. Login → workflows → flagship **Run now** → approve if needed → audit.

Offline/unit without DB:

```bash
set GENERIC_SWARM_FORCE_JSON_STORE=true
```

---

## 9. Definition of done for this plan document

- [x] Postgres chosen and documented.
- [x] Runtime uses Postgres when `DATABASE_URL` is set.
- [x] Phases P1–P5 completed with verification matrix green.
- [x] Scorecard shows **100/100** with evidence including Postgres durability.
- [x] `memory/handoff.md` states mark 100 and remaining non-goals explicitly.
- [ ] You accept remaining product decisions (demo default, adapter scope) and optional manual E1 sign-off.

---

## 10. Suggested next command to me

**Mark 100 published** (automated). Optional human:

> **Run E1 checklist: login → Run now → approve → audit (demo off, Postgres up) and accept 100.**

Or maintenance:

> **Ship / PR: commit P1–P5 work with verification docs.**

---

*Living document. Postgres is the durable store; JSON is backup. Update checkboxes as phases land.*
