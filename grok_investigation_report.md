# Grok investigation & remediation report

> **Historical snapshot (2026-07-09 investigation).** Product bar mark ~100 and self-improvement have since shipped. For current status use `status.md`, `mark_100_verification.md`, and `docs/architecture.md`. Claims below about “JSON-only store” or “demo frontend” are **outdated**.

**Project:** generic-swarm-ops  
**Spec baseline:** `structure.md` v2.1 (Research-Integrated Edition)  
**Supporting specs:** `tasks.md`, `backend.md`, `frontend.md`  
**Investigation date:** 2026-07-09  
**Source instruction:** `grok_investigate_now.md`  
**Status (at investigation time):** DONE_WITH_CONCERNS — later superseded by mark-100 product bar

---

## 1. Investigation scope

### 1.1 Objective

Deep compliance investigation of the full repository against `structure.md`, identify errors/bugs/inconsistencies/gaps, implement necessary fixes, update outdated docs/content, capture improvement ideas, and produce this report with a post-remediation checklist.

### 1.2 Scope covered

| Layer | Paths | Method |
|-------|-------|--------|
| Spec | `structure.md` §§0–12 | Full read + mapping |
| Business OS | `business/**` | Tree vs §3.5, schemas, content density, gate scripts |
| Backend | `backend/app/**` | Routes, `runtime.py`, stubs, authz, tests |
| Frontend | `frontend/src/**` | Routes, demo mode, API client, nav, tests |
| Agents / harness | `.trae/`, `.grok/`, `skills/`, `rules/` | Roster parity |
| Automation | `npm test`, business gates, backend unittest, frontend typecheck/test | Live runs |

### 1.3 Out of scope for this pass (documented as backlog)

- Production DB, real LLM providers, LightRAG/vector graph indexing
- Full frontend live API wiring (demo → real) end-to-end
- Full evolution propose/test/canary **API** product surface
- Event-log ingest + process-mining engines
- Filling entire knowledge-base/materials corpora

---

## 2. Architecture compliance summary (structure.md)

| Structure section | Scaffold / MVP | Runtime depth | Notes |
|-------------------|----------------|---------------|-------|
| §1 Principles | Yes | Partial | Safety-first encoded in rules/agents; enforcement incomplete pre-fix |
| §2 Process Intelligence | Folders + agents | Partial | Process aggregate APIs only; no event ingest/mining |
| §3 Knowledge & hybrid memory | Folders + schemas | Partial | Memory CRUD + provenance fields; no tiered LightRAG |
| §3.5 Folder structure | **50/50 paths** | Scaffold | Most content was empty; seeded first real SOP/evals/inventory |
| §4 Workflow DNA | Schema + example + runtime | Partial | DNA model + human gates; steps not real tool/LLM execution |
| §5 Evolution sandbox | Files + scripts | **Offline only** | No backend evolution API; non-mutation rule in scripts/canary |
| §6 Governance / risk tiers | JSON + policy | Improved | Tiers present; runtime now maps tier → start/gate rules |
| §7 Security | Register + rules | Partial | Tool allow-list at step; password reset closed; no full DLP |
| §8 Evaluation | Schema + harness | Partial | Corpus was empty; golden/regression/adversarial seeds added |
| §9 Agent roster | Dual harness complete | Yes | Trae/Grok agents match control + learning + PI agents |
| §10 Human-AI interaction | UI shell | Weak | Confidence/evidence UX not fully productized |
| §11 90-day rollout | Docs | Early | Days 1–14 skeleton; content still sparse |

**Overall maturity:** Validated **governed multi-agent OS skeleton** with a working **local JSON FastAPI control plane** and a **demo frontend shell**. Not yet a production operational swarm per structure.md depth.

---

## 3. Inventory of identified issues

### 3.1 Critical

| ID | Issue | Location | Severity | Status after remediation |
|----|-------|----------|----------|---------------------------|
| C1 | `list_collection` missing on runtime; workers/repos/seed callers break if used | `backend/app/runtime.py` (absent); callers under workers/repositories | Critical | **Fixed** — helper added |
| C2 | Unauthenticated password reset | `backend/app/api/v1/routes/auth.py`, `runtime.reset_password` | Critical | **Fixed** — requires authenticated self/admin (or reset token) |
| C3 | Archive workflow/tool without permission checks | `runtime.archive_workflow`, `archive_tool` | Critical | **Fixed** — `assert_permission` |
| C4 | Empty operational business corpus (knowledge, materials, evals) | `business/**` | Critical (content) | **Partially fixed** — SOP, golden/regression/adversarial seeds, AI inventory, IR plan |
| C5 | Broken provenance refs to missing SOP | examples cited `materials/sops/customer-onboarding.md` | Critical (content integrity) | **Fixed** — SOP file created |
| C6 | Workflow DNA example agents not in roster | `business/examples/workflow-dna.example.json` | Critical (consistency) | **Fixed** — mapped to roster agents |
| C7 | No evolution sandbox **runtime** (structure §5.1 product path) | backend routes | Critical (feature gap) | **Open** — offline sandbox only; documented backlog |
| C8 | Frontend no real auth/API (demo default) | `frontend/src/lib/**` | Critical (product gap) | **Open** — intentional MVP scaffold; not closed this pass |

### 3.2 Major

| ID | Issue | Status |
|----|-------|--------|
| M1 | Risk tier not driving gates (only step flags) | **Fixed partially** — tier 5 block start; tier 4 critical gates; tier 2 externalize gates; tool approval_requirement honored |
| M2 | Tool `approval_requirement` ignored at execution | **Fixed** |
| M3 | `evaluation_policy.block_on_fail` not enforced | **Fixed** |
| M4 | Domain/infra layers stubbed (`pass` / Generated module) | **Open** (architecture debt) |
| M5 | No event-log ingest / process mining APIs | **Open** |
| M6 | Memory scopes ≠ structure hybrid types; agent scopes not enforced | **Open** |
| M7 | Human-approval policy one-liner | **Fixed** — expanded policy |
| M8 | AI inventory empty | **Fixed** — `inventory.json` |
| M9 | No incident response plan | **Fixed** — plan doc |
| M10 | structure.md §9 Learning roster omitted PI agents from §2.3 | **Fixed** — roster expanded |
| M11 | structure.md sample `risk_tier` medium/high vs tier enums | **Fixed** — samples use `tier_*` |
| M12 | Frontend tools missing from sidebar | **Fixed** |
| M13 | Unit tests too thin for governance claims | **Improved** — 3 new runtime tests |

### 3.3 Minor

| ID | Issue | Status |
|----|-------|--------|
| m1 | Process metrics org-scoping edge cases | Open |
| m2 | Knowledge index only flips status | Open |
| m3 | SSE snapshot vs live stream | Open |
| m4 | Integrations return mocked payloads | Open (expected MVP) |
| m5 | `business:security` warning on workflow DNA tool language | Open (review warning) |
| m6 | Historical-replay folder missing from §3.5 tree | **Added** README under `evals/historical-replay/` |
| m7 | Frontend demo mode default true | Open (document; safe local default) |
| m8 | SHA-256 passwords / JSON store | Open (local MVP) |

---

## 4. Fixes implemented

### 4.1 Backend (`backend/app/runtime.py` and auth)

1. **`list_collection(name)`** — deep-copy collection helper for workers/repos/seed.
2. **`archive_tool` / `archive_workflow`** — require `tools:update` / `workflows:update`.
3. **Password reset** — rejects unauthenticated open reset; allows authenticated self or same-org admin/owner; optional `reset_token` path; min password length 8.
4. **Auth route** — `/reset-password` depends on `get_current_user`.
5. **Risk tier engine helpers** — `_tier_level`, `_tool_requires_approval`.
6. **Start run** — blocks tier ≥ 5 without assurance path; blocks tier 0 execute.
7. **Step execution** — honors tool approval requirements; tier 4 gates critical/irreversible actions; tier 2 gates externalizing action types.
8. **Evaluation block_on_fail** — fails the run when policy set and evaluation failed.

### 4.2 Backend tests

- `test_list_collection_helper`
- `test_password_reset_requires_auth`
- `test_tier_level_mapping`

### 4.3 Business content & governance

| Artifact | Purpose |
|----------|---------|
| `business/materials/sops/customer-onboarding.md` | Real SOP for provenance |
| `business/evals/golden-tasks/customer-onboarding-baseline.json` | First golden task |
| `business/evals/regression-tests/customer-onboarding-human-gate.json` | Gate regression assertions |
| `business/evals/adversarial-tests/prompt-injection-tool-misuse.json` | Adversarial seed |
| `business/evals/historical-replay/README.md` | §8 replay location |
| `business/governance/ai-inventory/inventory.json` | §6.2 inventory seed |
| `business/governance/human-approval-policy/policy.md` | Expanded policy |
| `business/security/incident-reports/incident-response-plan.md` | IR plan |
| `business/examples/workflow-dna.example.json` | Agents aligned to roster |

### 4.4 Spec & frontend

- `structure.md` — PI agents in §9 Learning roster; sample risk tiers → `tier_*`; DNA sample agents aligned.
- `frontend/src/types/navigation.ts` — Tools nav item.

---

## 5. Content / documentation updates

| File | Change |
|------|--------|
| `structure.md` | Roster, risk_tier samples, DNA agent names |
| Human approval policy | Full procedure |
| AI inventory | JSON register |
| IR plan | Containment/recovery |
| Eval seeds | Golden/regression/adversarial |
| SOP | Customer onboarding |
| This report | `grok_investigation_report.md` |
| `memory/handoff.md` | Will reflect investigation completion |

---

## 6. Improvement ideas (actionable)

| # | Idea | Rationale | Effort |
|---|------|-----------|--------|
| I1 | Wire frontend `backendApi` + real session cookies; default `NEXT_PUBLIC_DEMO_MODE=false` in staging | Makes UI an operational console, not a mock | M |
| I2 | Export OpenAPI from FastAPI and generate `frontend` contracts | Ends `GeneratedPlaceholder` drift | S–M |
| I3 | Evolution APIs: propose variant → sandbox eval → canary → promote (never direct prod DNA mutate) | Closes structure §5 product gap | L |
| I4 | Event-log ingest + case timeline + conformance report generation | Enables process intelligence layer | L |
| I5 | Implement LightRAG/vector tier behind knowledge search (Tier 0 now; Tier 1 graph later) | structure §3.4 cost-tiered retrieval | L |
| I6 | Enforce agent `allowed_memory_scopes` and workflow `memory_reads`/`memory_writes` | Provenance + least privilege | M |
| I7 | Replace SHA-256 + JSON store with bcrypt/argon2 + Postgres | Production readiness | M–L |
| I8 | Expand golden tasks to ≥20 per 90-day plan Days 1–14 | “Everything is testable” | M |
| I9 | Split frontend `[...slug]` into route modules per surface | Maintainability / progressive API wiring | M |
| I10 | Add e2e tests: login → run workflow → approval → audit | Regression safety for gates | M |
| I11 | Curate ECC skill daily pack via agent-sort | Reduce 277-skill noise for Grok | S |
| I12 | Fitness function F scoring service for evolution variants | structure §5.2 objective scoring | M |

---

## 7. Post-remediation validation checklist

### 7.1 Automated (executed 2026-07-09)

| Check | Result |
|-------|--------|
| `python -m compileall backend/app` | **Pass** |
| `python -m unittest discover -s backend/app/tests/unit` | **Pass (7 tests)** |
| `npm test` | **Pass (16/16)** |
| `npm run business:validate` | **Pass** |
| `npm run business:governance` | **Pass** |
| `npm run business:security` | **Pass** (1 review warning) |
| `npm run business:evolution:check` | **Pass** |
| `cd frontend && pnpm typecheck` | **Pass** |
| `cd frontend && pnpm test` | **Pass (3 tests)** |
| Business §3.5 directories present | **50/50** |
| Dual-harness agents present | **18 Trae + 18 Grok** |

### 7.2 structure.md adherence (honest)

| Claim | Met? |
|-------|------|
| Folder structure §3.5 | **Yes** |
| Risk tiers defined | **Yes** |
| Human gates for sensitive steps | **Yes** (improved) |
| Provenance fields on core artifacts | **Yes** (schemas/examples) |
| Evolution never mutates production via engine | **Yes offline**; **no runtime engine** |
| Full hybrid memory + LightRAG | **No** |
| Full process mining | **No** |
| Full live frontend control plane | **No** (demo shell) |
| Eval corpus production-ready | **Started** (not ≥20 golden tasks) |

### 7.3 Remaining must-not-claim

Do **not** claim the system is production-complete vs structure.md. Claim:

> Scaffold + local MVP control plane, with critical authz/gate fixes applied and first operational artifacts seeded; advanced PI/evolution/RAG/frontend-live still backlog.

---

## 8. Evidence index

### Key code changes

- `backend/app/runtime.py` — authz, tiers, gates, list_collection, eval block
- `backend/app/api/v1/routes/auth.py` — authenticated reset
- `backend/app/services/auth_service.py` — reset signature
- `backend/app/tests/unit/test_runtime.py` — new tests
- `frontend/src/types/navigation.ts` — Tools link
- `structure.md` — roster + samples
- Business content files listed in §4.3

### Investigation sources

- Explore subagents: backend audit, frontend audit, business audit
- Host command validation suite (listed above)

---

## 9. Conclusion

**STATUS: DONE_WITH_CONCERNS**

The project **structurally matches** structure.md’s business-OS skeleton and exposes a substantial FastAPI surface for agents, workflows, approvals, knowledge, memory, governance, and process aggregates. Pre-fix gaps included real control failures (open password reset, missing archive permissions, missing `list_collection`) and empty content that broke provenance promises.

**This pass fixed the highest-severity control bugs**, aligned DNA/roster/spec samples, seeded first SOP/eval/governance content, and expanded approval/IR policy. **Major product gaps remain** (live frontend, evolution API, process mining, hybrid retrieval). Those are intentional multi-phase items, not silent omissions.

---

*Generated by executing `grok_investigate_now.md` against structure.md and the live codebase.*
