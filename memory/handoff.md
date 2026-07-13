# Handoff

## Current status

- Product bar **~100** with E1 operator path **PASS** (`reviews/e1_operator_checklist.md`, `test_e1_operator_path`).
- Full self-improvement backlog + guided Improve → Evaluate → Canary UI.
- Docs: `docs/self-improvement-and-orchestration.md`
- **Adoption `adoption.md` / `adoption_hk.md` v2.4 (2026-07-13):** N3 **implementation complete** status after improvements Waves 0–5; v2.3 rethink retained; research snapshot gaps marked CLOSED／已關閉; §7.5 DoD checked for N3 framing; post-N3 residual (deep L2, live media, advanced FE) explicit. HK aligned with EN.
- **Video corpus migration (2026-07-13):** `migration_plan.md` executed — `business/video/corpus/` **325** files from va; all **114 SPEC.md** expanded (no refer-only). `check_video_corpus_standalone.py` + `test_video_corpus_standalone` green. Upstream va optional.
- **`adoption_plan.md` v3.2 rethink:** §0 principles + critical path §0.3; §15 playbooks as reference depth; avoid SPEC/DNA theater.
- **`adoption_plan_hk.md`:** Traditional Chinese full translation of `adoption_plan.md` v3.2.
- Product rename: **generic-swarm-ops** (not genetic); env prefix `GENERIC_SWARM_*`.
- **SPEC enrichment (2026-07-13):** All 114 `business/video/agents/*/SPEC.md` rewritten from corpus via `enrich_video_agent_specs.py` (full agents.md row + §11 common structure + deep-spec embeds + system/workflow mentions). Sizes ~10–195 KB.

### Session study (2026-07-11) — READ ONLY; ready for next instruction

User chain of work (do not execute until asked):

1. **Compared repos:** `generic-swarm-ops` (this host) × `va-agent-swarm` → wrote `repo_compare.md` (2026-07-11).
2. **Studied improvement** from `adoption.md` + `repo_compare.md` → wrote **`improvements.md` v1.0** (execution plan).
3. **Execution prompt:** `improvement_prompt.txt` — mandatory SDD flow for coding agents.

**Wave 0 implemented (2026-07-11):** SDD under `planning/improvement/wave-0/`; `business/video/` L0 catalog (114 agents); Domain Pack schemas; inventory CI; register stub.  
**Wave 1 implemented (2026-07-11):** SDD under `planning/improvement/wave-1/`; ALC lessons `agent_id` + activation gate; `POST /domains/register`; agent_genome sandbox; example_research DNA; FE DomainPackPanel.  
**Wave 2 implemented (2026-07-12):** SDD under `planning/improvement/wave-2/`; spine + viral-hook DNA; video_* stubs; standby_pool 114; spine E2E unit test green.  
**Wave 3 implemented (2026-07-12):** SDD under `planning/improvement/wave-3/`; multi-gen coevolution; lesson utility dashboard; governance review; video LQR golden + corpus overlay; skill sandbox domain metadata; FE LessonUtilityPanel.  
**Wave 4 implemented (2026-07-12):** SDD under `planning/improvement/wave-4/`; example_education third pack; ≥20 mixed-domain load; red-team tool misuse + allow-list immutability; isolation helpers; add-domain-pack runbook + versioning matrix; FE multi-pack summary.  
**Wave 5 / N3 complete (2026-07-12):** SDD under `planning/improvement/wave-5/`; 114 agents registered+ALC; standby/router; DNA e2e+B–J+LQR+delivery; process_coverage va_only=0; retention policy; CI `n3-inventory.yml`; `GET /domains/video/n3-status`; FE VideoN3RosterPanel. Unit suite **104 passed**; inventory **114 n3=complete**. Post-N3: real media providers, deeper L2 activation, advanced FE.

### Chain re-verify (`run_all_improvement.md`, 2026-07-12)

| Wave | Result |
|------|--------|
| 0 | PASS (8 domain-pack tests + inventory + register dry-run) |
| 1 | PASS (12 ALC tests) |
| 2 | PASS (3 spine E2E) |
| 3 | PASS (7 coevolution) |
| 4 | PASS (8 multipack) |
| 5 | PASS (9 N3 + inventory n3=complete) |
| Full unit | **104 passed** |

Report: `planning/improvement/chain-run-report.md`.

---

### Key corpus map

| File | Role |
|------|------|
| `repo_compare.md` | Gap analysis + merge recommendation (generic host, va = video pack) |
| `adoption.md` v2.3 | Strategy: N1/N2/N3, L0/L1/L2, full 114 roster, ALC, Domain Pack |
| `adoption_plan.md` v3.2 | Action tables + critical path + §15 playbooks |
| **`improvements.md` v1.0** | **SoT for coding execution** — Waves 0–5, file-level tasks, agent prompts |
| **`improvement_prompt.txt`** | **How to run each wave** — Phase 1 Requirements → 2 Design → 3 Tasks → implement under `planning/improvement/<wave>/` |

Related chat shares (user-provided): repo compare study; adoption+compare → improvements study.

---

### Merge model (internalize)

- **generic-swarm-ops** = universal governed MMA **host** (runtime, governance, evolution, FE ops console).
- **va-agent-swarm** = complete **video Domain Pack** → import into `business/video/` (full 114 agents + all processes, retained forever). va stays upstream research/narration SoT.
- **No second control plane** (no LangGraph/Temporal host rebuild).
- **No video pollution of core:** all domain logic under `business/<domain_id>/`; namespaces e.g. `video.*`; ops seed uses `business_orchestrator`, video uses `video.orchestrator`.

### Non-negotiables (N1 / N2 / N3)

| ID | Meaning |
|----|---------|
| **N1** | Video business logic only in pack; every agent gets mandatory **Agent Learning Contract (ALC)** for autonomous per-agent learning |
| **N2** | generic is universal host for **dozens** of MMA packs (Domain Pack SDK + isolation); second pack proof required |
| **N3** | Adopt **ALL 114 agents + ALL processes** from va; inventory CI; never drop agents; in-project retention |

### Maturity model

| Level | Name | Meaning |
|-------|------|---------|
| **L0 Catalog** | Present | Dir + ROSTER/MAP + draft `agent_spec` |
| **L1 Indexed** | Reachable | PROCESSES / DNA stub / `standby_pool` |
| **L2 Runtime** | Runnable | active, ALC gate, tools (stub OK), on DNA path |

N3 complete ≈ all agents ≥ L1, spine ≥ L2, inventory CI green, processes indexed — **not** all 114 deep L2 in one sprint.

### Improvements waves (execute in order)

| Wave | Goal | Horizon |
|------|------|---------|
| **0** | Inventory, skeletons, schemas, CI gates; 114 placeholder dirs; ROSTER/MAP/PROCESSES | 1–2 wk |
| **1** | Domain Pack SDK + full ALC + register API + example pack isolation + FE domain shell | 2–3 wk |
| **2** | Catalog complete + spine E2E (viral-hook/spine DNA) + media stubs + goldens | 3–5 wk |
| **3** | Learning/coevolution on video goldens; measurable fitness | 2–3 wk |
| **4** | Multi-pack proof, load, security, runbook | 2–3 wk |
| **5** | Full roster activation + full process wiring (N3 completion) | 8–16+ wk |

First 30 days focus: Wave 0 → Wave 1 → Wave 2 spine; protect E1 every PR.

### SDD execution protocol (`improvement_prompt.txt`)

For each wave `planning/improvement/wave-N/`:

1. **Phase 1** `requirements.md` — goals, N1/N2/N3 quote, FRs/NFRs, acceptance, Structure/Backend/Frontend subsections  
2. **Phase 2** `design.md` — architecture, schemas, isolation, sandbox, Structure/Backend/Frontend impact  
3. **Phase 3** `tasks.md` — numbered steps, exact paths tagged Structure|Backend|Frontend, tests, acceptance  

Then implement tasks, run tests, completion report.  
**Rules:** sandbox for risky changes; no direct production mutation of host; stop if N1/N2/N3 or E1 violated.

### Critical platform gaps (confirmed)

- No `business/video/` yet  
- No domain-manifest / agent-spec / learning-log schemas; no `/domains` register  
- Lessons workflow-centric (`agent_id` missing historically; ALC incomplete)  
- Domain layer models largely stubs  
- No video adapters; FE no full video pack roster UI  

### Complementary strengths (repo_compare)

| generic strong | va strong |
|----------------|-----------|
| Runtime, governance, evolution sandbox, FE ops, PI | 114 roster, deep specs, processes A–J/LQR, research corpus, UI concepts |

### User concern (resolved in plan)

Improvements **benefit other projects** (tutoring, trading, content, etc.) via Domain Pack + ALC.  
**Zero business-specific pollution** of generic core if isolation rules hold.

### Shipped backlog (platform already)

| Item | How |
|------|-----|
| Auto-reflect | Terminal runs (`GENERIC_SWARM_AUTO_REFLECT=true`) |
| FE Improve | Reflect + Propose sandbox variant |
| LLM critic | Optional `GENERIC_SWARM_LLM_CRITIC_ENABLED` |
| Population archive | `/app/evolution` + archive API |
| Embeddings / federation | Tier-0 + optional pgvector; Cypher/JSON export |
| Skill sandbox | `_sandbox/` then explicit promote |
| Runtime path sanitize | `sanitize_legacy_product_names*` on load/save (genetic→generic) |

### Tests (last known green)

- Backend unit suite (incl. skill sandbox / improvement backlog)
- Frontend lint / typecheck / vitest / build

### Seed login

- `admin@example.com` / `admin-password`

### Next when instructed

1. Read `improvement_prompt.txt` + `improvements.md` Wave N  
2. Run full SDD Phases 1–3 into `planning/improvement/wave-N/`  
3. Implement + verify; never skip inventory/ALC/E1 gates  
