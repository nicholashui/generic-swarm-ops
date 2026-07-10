# Adoption Action Plan

**Source strategy:** `adoption.md` v2.2 · `adoption_hk.md` v2.2 · `review_adoption.md`  
**Plan version:** 3.2 (rethink)  
**Date:** 2026-07-10  
**Repos:** generic-swarm-ops (host) × va-agent-swarm (complete video Domain Pack)  
**Non-negotiables:** **N1** ALC · **N2** Domain Pack host · **N3** **ALL 114 agents + ALL processes + in-project retention**  
**Strategy peer:** `adoption.md` v2.3 rethink (L0/L1/L2 maturity)

---

## 0. Rethink — execution principles (read first)

### 0.1 What was wrong with the previous plan shape

| Problem | Why it hurts | Fix |
|---------|--------------|-----|
| **SPEC theater** | Filling deep SPEC.md for all 114 before first E2E burns weeks with zero runtime proof | **L0 catalog** = dir + minimal agent_spec + MAP. Deep SPEC = **L2 activation** work |
| **DNA theater** | Stubbing 10 archetypes + LQR + 6-phase as “done” while none run | **Index all processes early**; **one runnable DNA** (spine/viral-hook) before depth |
| **Gate confusion** | ALC required on every draft placeholder blocks register/import | **Hard ALC only when status → active** or DNA `production_ready`; draft still carries ALC fields |
| **Milestone confusion** | Phase 2 “all agents present” looks like N3 complete | Three DoD levels: **Catalog**, **Spine**, **N3 complete** |
| **Namespace collision** | Generic already has `business_orchestrator` (ops) | Video meta agents only under `video.*` (`video.orchestrator`, …) — never overwrite ops seeds |
| **Playbook bloat** | 100+ micro-steps without a weekly outcome | §15 is reference; **§0.3 critical path** is what you execute weekly |
| **N2 vs N3 order** | Second domain before video catalog is fine; second domain before spine is a distraction | **example_domain** only to prove register API; then **video spine** before other domains |

### 0.2 Maturity model (use this when updating Status)

| Level | Name | Minimum bar | Counts toward |
|-------|------|-------------|----------------|
| **L0** | Catalog | Folder + ROSTER/MAP + draft `agent_spec.json` (ALC fields present) | N3 presence |
| **L1** | Indexed | Appears in PROCESSES.md and/or DNA stub and/or `standby_pool` | N3 reachability |
| **L2** | Runtime | `active` or invoked; ALC gate passed; on runnable DNA; tools stub OK | Demo / production path |

**N3 complete** = all 114 ≥ **L1**, inventory CI green, processes indexed, retention CI on, spine ≥ **L2**.  
**Not required for N3 complete:** all 114 at L2, live Sora/Veo, full FE timeline editor.

### 0.3 Critical path (only this is “default work”)

Do **in order**. Everything else is parallel or later.

| Order | Outcome | Parent IDs | Timebox |
|-------|---------|------------|---------|
| **1** | ADR + approve | P0-01, P0-02 | 1 day |
| **2** | L0 catalog: ROSTER, 114 dirs, MAP, PROCESSES index, inventory script | P0-03…P0-07, N3-CI-01 (early) | 3–5 days |
| **3** | Platform: schemas + domain register + example_domain dry-run | DP-01…DP-07 | 1 week |
| **4** | Platform: agent_id lessons + ALC on **active** + E1 still green | ALC-01…ALC-10, REG-01 | 1–2 weeks |
| **5** | Spine L2: 8–12 agents full enough + viral-hook DNA + stubs + e2e | VID-01…VID-10, FE-01 list | 2–3 weeks |
| **6** | Process depth: remaining DNA families + waves W2–W5 + orphan/retention CI | N3-P-*, W*, DOD-02 | ongoing |
| **7** | Other domains | DP-09/DP-10 | **after** spine L2 (N2), full N3 optional later |

### 0.4 What “detailed steps” mean now

- **§5** = backlog (parents).  
- **§15** = deep procedure when stuck or onboarding a new implementer.  
- **§0.3** = what the team works this week.  
- Do **not** require every §15 micro-step before shipping spine demo — require **Verify** gates for the critical-path parents only.

---

## 1. How to use this list

| Field | Meaning |
|-------|---------|
| **ID** | Stable task id (`P0-01`, `N3-A-03`, `ALC-02`, …) |
| **Step** | Micro-step id under a parent (`P0-03.s1`, `ALC-02.s3`, …) — see **§15 Detailed playbooks** |
| **Phase** | 0–5 from `adoption.md` §6 |
| **Workstream** | `GOV` · `N3` roster/process · `DP` Domain Pack · `ALC` learning · `EV` evolution · `VID` video runtime · `FE` frontend · `T` test · `REG` regression · `DOC` docs · `RISK` risk |
| **Priority** | **P0** critical path · **P1** phase exit · **P2** important · **P3** later |
| **Owner** | `platform` · `video-pack` · `va-specs` · `product` · `both` |
| **Status** | `todo` · `in_progress` · `blocked` · `done` · `leverage` (already exists) |
| **Depends on** | Prerequisite IDs |
| **Acceptance** | Exit criteria |
| **Primary paths** | Files / APIs to touch |

**Roster source of truth:** `adoption.md` **Appendix A** (114 pack ids `video.*`).  
**CI contract (N3):** `count(business/video/agents/*) == 114` AND MAP rows == 114 AND no orphan agents.

**Execution order:** High-level tables in **§5** → for each parent ID, open **§15** and complete every `.sN` micro-step before marking the parent `done`.

---

## 2. Non-negotiable checklist (must stay true)

| ID | Rule | Status |
|----|------|--------|
| N3-RULE-01 | Import **all** va agents 1–114; never drop meta (#53–80) or support (#81–114) | todo |
| N3-RULE-02 | Import **all** va business processes (6-phase + A–J + LQR + UI process docs) | todo |
| N3-RULE-03 | Orchestrator-down: DNA enters via `video.orchestrator` / `video.planner` | todo |
| N3-RULE-04 | Every agent in ≥1 DNA step **or** `standby_pool` | todo |
| N3-RULE-05 | Agents remain in git as draft/registered even when not active | todo |
| N3-RULE-06 | Inventory CI fails if agent folder missing | todo |
| N1-RULE-01 | ALC **hard-required** for agents status=`active` / DNA production_ready; draft carries ALC fields | todo |
| N2-RULE-01 | Second pack proves host without runtime fork (**after spine L2**) | todo |
| RETHINK-01 | Ops seeds (`business_orchestrator`, …) never replaced by video meta agents | todo |
| RETHINK-02 | Weekly work follows §0.3 critical path, not §15 exhaustively | todo |

---

## 3. Phase overview

| Phase | Focus | Duration | Exit summary |
|-------|--------|----------|--------------|
| **0** | L0 catalog + ADR | 1–2 weeks | ROSTER/MAP/114 dirs (minimal specs); PROCESSES **index**; baseline green |
| **1** | Domain Pack SDK + ALC runtime | 2–3 weeks | Register; agent_id lessons; ALC on **active**; E1 green |
| **2** | Catalog L0 complete + **spine L2** E2E | 3–5 weeks | 114 at L0; process **index**; viral-hook **runnable**; not “all DNA deep” |
| **3** | Learning + coevolution on spine | 2–3 weeks | ≥1 fitness gain on video goldens |
| **4** | Multi-pack proof + security + load | 2–3 weeks | Second pack **after spine**; isolation; runbook |
| **5** | Raise agents/processes toward N3 complete (L1 all, more L2) | 8–16+ weeks | Orphans=0; process DNAs bound; retention CI; N3 DoD |

| Bundle | Target | Meaning |
|--------|--------|---------|
| **Demo** (0–2 critical path) | 6–9 weeks | Catalog L0 + spine L2 |
| **Platform hardened** (through 4) | 10–16 weeks | N2 + security |
| **N3 complete** (through 5) | +8–16 weeks | All ≥ L1; spine solid L2; processes indexed & bound |

---

## 4. Already shipped (leverage — do not rebuild)

| ID | Capability | Status | Primary paths |
|----|------------|--------|---------------|
| BASE-01 | FastAPI + Postgres control plane | leverage | `backend/app/runtime.py` |
| BASE-02 | Workflow DNA validate / activate | leverage | `structure_validators.py`, workflows routes |
| BASE-03 | Run lifecycle + SSE + pause/resume/expire | leverage | `workflow_runs` routes |
| BASE-04 | Local tool adapters + `tool_effects` | leverage | `infrastructure/tools/adapters.py` |
| BASE-05 | Run reflect + lesson library + disk lessons | leverage | `improvement` routes, `self_improvement/*` |
| BASE-06 | Auto-reflect | leverage | `GENERIC_SWARM_AUTO_REFLECT` |
| BASE-07 | Evolution sandbox (sandbox_only) | leverage | `evolution` routes, `corpus_eval.py` |
| BASE-08 | Skill sandbox | leverage | `/improvement/skills/*` |
| BASE-09 | FE Improve + Evolution UI | leverage | `improve-run-button.tsx`, `evolution-archive-panel.tsx` |
| BASE-10 | E1 + unit suites green | leverage | `test_e1_operator_path.py`, `tests/unit/*` |
| BASE-11 | 20 onboarding goldens | leverage | `business/evals/golden-tasks/` |
| BASE-12 | Dual harness + business:* scripts | leverage | `npm run sync`, `business:validate` |

---

## 5. Master action tables

### 5.1 Phase 0 — Full inventory & skeletons

| ID | Task | Workstream | Priority | Owner | Status | Depends on | Primary paths | Acceptance |
|----|------|------------|----------|-------|--------|------------|---------------|------------|
| P0-01 | Approve `adoption.md` v2.2 + this plan as execution contract | GOV | P0 | product | todo | — | `status.md` | Written approval |
| P0-02 | ADR: dual-repo + pack-on-generic + **N3 retention of all 114 agents** | GOV | P0 | product | todo | P0-01 | `docs/` or `business/governance/` | ADR bans second control plane; forbids agent drop |
| P0-03 | Export `business/video/ROSTER.json` from va `agents.md` (114) | N3 | P0 | both | todo | P0-01 | `business/video/ROSTER.json` | Count == 114; ids 1–114 |
| P0-04 | Export `business/video/PROCESSES.md` (6-phase + A–J + LQR + UI) | N3 | P0 | both | todo | P0-01 | `business/video/PROCESSES.md` | Orchestrator→leaf covered |
| P0-05 | Create `business/video/` skeleton (manifest, agents, workflows, evals, knowledge, tools, ui) | DP | P0 | platform | todo | P0-02 | `business/video/**` | Tree exists |
| P0-06 | Create **placeholder dir for every Appendix A pack id** | N3 | P0 | platform | todo | P0-03, P0-05 | `business/video/agents/video.*/` | **114** directories |
| P0-07 | Write `business/video/MAP.md` one row per agent (va id → pack_id → source path) | N3 | P0 | both | todo | P0-06 | `MAP.md` | Rows == 114; no omissions |
| P0-08 | Create `business/example_domain/` skeleton (N2 seed) | DP | P0 | platform | todo | P0-02 | `business/example_domain/**` | Minimal pack tree |
| P0-09 | Baseline green: unit + E1 + FE lint/typecheck/test | REG | P0 | platform | todo | — | `status.md` | Commands pass |
| P0-10 | Inventory deep-spec modules (research, GCA, aesthetics, DIA, RAG, …) into PROCESSES/MAP | N3 | P1 | va-specs | todo | P0-04 | PROCESSES.md | Modules listed |
| P0-11 | Risk register owners for R-01…R-11 | RISK | P1 | product | todo | P0-01 | this plan §8 | Owners assigned |
| P0-12 | Sync policy: PR copy va→generic full roster; no submodule until stable | GOV | P1 | product | todo | P0-02 | ADR appendix | Decision logged |

**Phase 0 exit**

| Check | Status |
|-------|--------|
| ROSTER + MAP + 114 dirs | todo |
| PROCESSES.md complete | todo |
| ADR + N3 rules approved | todo |
| E1/unit baseline green | todo |

---

### 5.2 Phase 1 — Domain Pack SDK + ALC

| ID | Task | Workstream | Priority | Owner | Status | Depends on | Primary paths | Acceptance |
|----|------|------------|----------|-------|--------|------------|---------------|------------|
| DP-01 | Add `business/schemas/domain-manifest.schema.json` | DP | P0 | platform | todo | P0-05 | `business/schemas/` | Valid/invalid fixtures |
| DP-02 | Add `business/schemas/agent-spec.schema.json` (alc, scopes, tools, domain_id) | DP | P0 | platform | todo | P0-07 | `agent-spec.schema.json` | ALC fields required when requires_alc |
| DP-03 | Add `business/schemas/learning-log.schema.json` with **agent_id** | DP | P0 | platform | todo | DP-02 | `learning-log.schema.json` | agent_id required |
| DP-04 | Schema unit tests | T | P0 | platform | todo | DP-01..03 | tests / business fixtures | Green |
| DP-05 | Domain register API and/or `npm run domain:register` | DP | P0 | platform | todo | DP-01 | `routes/domains.py`, `router.py` | Draft load works |
| DP-06 | Invalid manifest fails closed | T | P0 | platform | todo | DP-05 | domains service | Unit deny |
| DP-07 | Dry-run register `example_domain` | DP | P0 | platform | todo | DP-05, P0-08 | example_domain | Success |
| DP-08 | Dry-run register `video` pack (draft agents) | DP | P0 | platform | todo | DP-05, P0-06 | business/video | Success |
| ALC-01 | Extend `Lesson` + store with `agent_id` (back-compat) | ALC | P0 | platform | todo | BASE-05 | `lessons.py`, runtime | Old lessons load |
| ALC-02 | Split reflect lessons by `step.agent` / `agent_id` | ALC | P0 | platform | todo | ALC-01 | `reflection.py`, `reflect_on_workflow_run` | Multi-agent → multi agent_id |
| ALC-03 | `POST /api/v1/improvement/reflect/agent/{agent_id}` | ALC | P0 | platform | todo | ALC-02 | `routes/improvement.py` | Agent filter works |
| ALC-04 | `GET /lessons?agent_id=` | ALC | P0 | platform | todo | ALC-01 | improvement routes | Query works |
| ALC-05 | Episodic write after step (agent scope / agent_episodes) | ALC | P0 | platform | todo | ALC-01 | runtime step loop | Episode fields complete |
| ALC-06 | Pre-step inject top-k agent lessons + agent memory | ALC | P0 | platform | todo | ALC-05 | step preflight | Unit: inject called |
| ALC-07 | Isolation: agent A cannot read B episodes | ALC | P0 | platform | todo | ALC-05 | memory policies | Unit deny/empty |
| ALC-08 | ALC gate on agent activate | ALC | P0 | platform | todo | DP-02, ALC-02 | `update_agent_status` | Deny without ALC |
| ALC-09 | ALC gate on DNA `production_ready` if step agent fails ALC | ALC | P0 | platform | todo | ALC-08 | structure_validators | Unit block |
| ALC-10 | Auto-reflect writes agent-scoped lessons | ALC | P0 | platform | todo | ALC-02 | `_auto_reflect_if_enabled` | Terminal run writes agent lessons |
| ALC-11 | Metrics growth/reuse by agent_id | ALC | P1 | platform | todo | ALC-01 | improvement metrics API | Non-empty after 2 runs |
| ALC-12 | example_domain agents with `allowed_memory_scopes` incl. `agent` | DP | P0 | platform | todo | ALC-08, DP-07 | example agent_spec | Activate OK |
| ALC-13 | Automated test: same agent learns across two runs | T | P0 | platform | todo | ALC-06, ALC-12 | new unit/e2e | Green |
| EV-01 | Variant type `agent_genome` + always sandbox_only until promote | EV | P1 | platform | todo | ALC-01 | evolution service | Unit: no direct production |
| EV-02 | Promote/rollback path for agent_genome | EV | P1 | platform | todo | EV-01 | evolution routes | Policy tests |
| DOC-01 | `docs/domain-packs.md` + structure.md ALC/Domain Pack | DOC | P1 | platform | todo | DP-05, ALC-08 | docs/ | Review complete |
| REG-01 | E1 still PASS after ALC/runtime changes | REG | P0 | platform | todo | ALC-02, ALC-08 | e2e E1 | Green |

**Phase 1 exit:** register works; agent_id lessons; ALC gates; E1 green.

---

### 5.3 Phase 2 — Full catalog + spine E2E

| ID | Task | Workstream | Priority | Owner | Status | Depends on | Primary paths | Acceptance |
|----|------|------------|----------|-------|--------|------------|---------------|------------|
| N3-A-01 | **L0 for all 114:** minimal agent_spec + stub SPEC (1 screen); deep SPEC only for spine | N3 | P0 | video-pack | todo | P0-07, DP-02 | `business/video/agents/**` | Inventory count == 114; spine SPECs richer |
| N3-A-02 | ALC **fields** on all agent_specs (draft OK); hard gate only on activate | N3 | P0 | platform | todo | N3-A-01, ALC-08 | agent_spec.json × 114 | Schema validate; activate gate tested on spine |
| N3-P-01 | PROCESSES coverage matrix (process → DNA id → agents) — **index first** | N3 | P0 | both | todo | P0-04 | PROCESSES.md | Every process row has target; status stub/ready |
| N3-P-02 | DNA: **one runnable** viral-hook + **lightweight stubs** for other families (index binding, not full depth) | N3 | P0 | video-pack | todo | N3-P-01, BASE-02 | `business/video/workflows/*.dna.json` | Viral-hook runnable; others validate schema |
| N3-P-03 | Declare orchestrator-entry on all executable DNAs | N3 | P0 | video-pack | todo | N3-P-02 | DNA steps | Entry = orchestrator/planner |
| VID-01 | Flesh spine agents: orchestrator, planner, router, judge, producer, director, screenwriter | VID | P0 | platform | todo | N3-A-01, ALC-08 | runtime / register | Status active |
| VID-02 | Intent/DIA + research module runnable (deep-spec wiring) | VID | P0 | video-pack | todo | VID-01 | agents + knowledge | Active on spine DNA |
| VID-03 | Author `wf_video_arch_a_viral_hook_v1` (orchestrator-down) | VID | P0 | video-pack | todo | N3-P-02, VID-01 | workflows/ | DNA validator pass |
| VID-04 | Tool permission entries for `video.*` | VID | P0 | platform | todo | VID-03 | tool-permission-register.json | Scoped + gates listed |
| VID-05 | Adapters: media_gen_stub, script_format, qc_stub | VID | P0 | platform | todo | VID-04, BASE-04 | `adapters.py` | tool_effects unit green |
| VID-06 | Golden evals hook quality + human gate | VID | P0 | video-pack | todo | VID-03 | `business/video/evals/` | business:eval green |
| VID-07 | Regression: irreversible steps human-gated | T | P0 | platform | todo | VID-03 | video regression JSON | Pass |
| VID-08 | Adversarial: injection must not expand allow-list | T | P0 | platform | todo | VID-05 | video adversarial JSON | Pass |
| VID-09 | E2E: queued→running→waiting_for_approval→succeeded | T | P0 | platform | todo | VID-03, VID-05 | new e2e | Green |
| VID-10 | E2E: agent lessons after terminal + auto-reflect | T | P0 | platform | todo | VID-09, ALC-10 | e2e | agent_id lessons non-empty |
| VID-11 | Improve pipeline propose sandbox still works | FE | P1 | platform | todo | VID-10, BASE-09 | ImproveRunButton | sandbox_only variant |
| FE-01 | Domain page lists **full 114** roster (filter draft/active) | FE | P0 | platform | todo | N3-A-01 | `frontend` domains/video | vitest smoke |
| VID-12 | Knowledge seeds from va reference (68 chapters + top specs) + provenance | VID | P1 | va-specs | todo | P0-10 | `knowledge/seeds/` | Provenance present |
| VID-13 | Index seeds Tier-0; retrieval smoke with acting_agent_id | VID | P1 | platform | todo | VID-12 | knowledge APIs | Scoped hits |
| N3-CI-01 | Inventory script: fail if agent count ≠ 114 | N3 | P0 | platform | todo | N3-A-01 | scripts/ or business:validate | CI hook ready |
| REG-02 | Customer-onboarding E1 still green | REG | P0 | platform | todo | VID-05 | e2e E1 | No regression |
| DOC-02 | Update status.md + handoff with spine path + N3 catalog status | DOC | P1 | platform | todo | VID-09 | handoff.md | Documented |

**Phase 2 exit:** (a) all 114 in project (b) process stubs complete (c) spine E2E demo.

---

### 5.4 Phase 3 — Learning & coevolution

| ID | Task | Workstream | Priority | Owner | Status | Depends on | Acceptance |
|----|------|------------|----------|-------|--------|------------|------------|
| EV-03 | Multi-generation sandbox on video goldens | EV | P0 | platform | todo | VID-06, EV-01 | ≥2 generations stored |
| EV-04 | Coevolution: planner genome × aesthetics / director | EV | P1 | platform | todo | EV-03 | Shared fitness recorded |
| EV-05 | Lesson utility/reuse dashboard (API or FE) | ALC | P1 | platform | todo | ALC-11 | Visible metrics |
| EV-06 | Video prompt skills via skill sandbox | EV | P1 | platform | todo | BASE-08, VID-01 | sandbox then explicit promote |
| EV-07 | Governance review of learned artifacts | GOV | P0 | product | todo | EV-03 | Sign-off; no auto_promote |
| EV-08 | Prove ≥1 fitness metric improves without prod regression | EV | P0 | platform | todo | EV-03 | Written report |
| EV-09 | Audit events for propose/eval/canary | EV | P0 | platform | todo | EV-03 | Audit present |

---

### 5.5 Phase 4 — Multi-pack, isolation, security, load

| ID | Task | Workstream | Priority | Owner | Status | Depends on | Acceptance |
|----|------|------------|----------|-------|--------|------------|------------|
| DP-09 | Second pack example_research or podcast-lite (**after** video catalog exists) | DP | P0 | platform | todo | DP-08 | Zero runtime forks |
| T-01 | Cross-pack memory isolation test | T | P0 | platform | todo | DP-09, ALC-07 | No bleed |
| T-02 | Load ~20 concurrent mixed-domain runs | T | P1 | platform | todo | DP-09 | No crash; no lost lessons |
| T-03 | Evolution archive p95 ~1k variants (if feasible) | T | P2 | platform | todo | EV-03 | Note recorded |
| T-04 | FE under 5 SSE runs | FE | P2 | platform | todo | FE-01 | Pass |
| T-05 | Red-team video tool misuse | RISK | P0 | platform | todo | VID-05 | Allow-list holds |
| T-06 | Prompt-injection CI gate | T | P0 | platform | todo | VID-08 | Required green |
| DOC-03 | Runbook “Add a Domain Pack” + engine_range | DOC | P0 | platform | todo | DP-09, DOC-01 | Published |
| DOC-04 | PR gates: platform vs pack | DOC | P1 | product | todo | DOC-03 | Written |
| DOD-01 | Platform DoD D1–D6 from adoption.md §7.5 platform | GOV | P0 | product | todo | REG-02, T-01 | All true |

**Note:** Phase 4 must **not** mark N3 complete; full N3 is Phase 5.

---

### 5.6 Phase 5 — N3 complete (mandatory)

#### 5.6.1 Activation waves (agents)

| ID | Wave | Scope (from adoption.md §5.1) | Workstream | Priority | Owner | Status | Depends on | Acceptance |
|----|------|-------------------------------|------------|----------|-------|--------|------------|------------|
| W0 | Catalog | All 114 already in tree (Phase 2) | N3 | P0 | — | leverage | N3-A-01 | count==114 |
| W1 | Spine active | orchestrator, planner, router, judge, producer, intent/DIA, director, screenwriter, research | VID | P0 | platform | todo | VID-01..03 | active + E2E |
| W2 | QC + creative | aiqaconsistency, aesthetics, optimization, gatekeeper, memory | VID | P0 | video-pack | todo | W1 | active on spine |
| W3 | Production crafts | cats 2–5 + promptengineer, avatardesign, voiceclone, talent | VID | P0 | video-pack | todo | W2 | active on gen/post DNAs (stubs OK) |
| W4 | Domain + GTM | cats 6–8 remainder + education specialists used by archetypes | VID | P1 | video-pack | todo | W3 | active per DNA |
| W5 | Full meta + support | remaining #57–80, #81–114 + standby_pool | N3 | P0 | platform | todo | W4 | all orchestrator-reachable |
| W6 | Process complete | A–J + LQR + 6-phase + UI processes | N3 | P0 | both | todo | W5, N3-P-10 | inventory 100% |

#### 5.6.2 Process wiring tasks

| ID | Task | Workstream | Priority | Owner | Status | Depends on | Acceptance |
|----|------|------------|----------|-------|--------|------------|------------|
| N3-P-10 | Flesh `wf_video_production_e2e_v1` + phase sub-DNAs | N3 | P0 | video-pack | todo | N3-P-02, W2 | Runnable or fully stubbed with real agent ids |
| N3-P-11 | Flesh `wf_video_arch_a` … `wf_video_arch_j` with real agent bindings | N3 | P0 | video-pack | todo | N3-P-02, W3 | 10 archetype DNAs complete |
| N3-P-12 | Flesh `wf_video_lqr_*` family (6 LQR SVGs) | N3 | P0 | video-pack | todo | N3-P-02, W2 | LQR coverage |
| N3-P-13 | Wire deep-spec modules (GCA, aesthetics, RAG, DIA, optimization) into DNA/services | N3 | P0 | platform | todo | W2 | Not dropped; documented |
| N3-P-14 | `standby_pool` + router tables for every agent | N3 | P0 | platform | todo | W5 | Orphan check == 0 |
| N3-CI-02 | Orphan-agent CI in default pipeline | N3 | P0 | platform | todo | N3-P-14 | Fail on orphan |
| N3-CI-03 | Retention CI: fail if Appendix A pack_id directory deleted | N3 | P0 | platform | todo | N3-CI-01 | Enforced |
| N3-A-10 | Activate remaining agents category-by-category with ALC | N3 | P0 | platform | todo | W2–W5 | active or registered+reachable |
| FE-02 | `/app/domains/video` dashboard (stages, assets, roster status) | FE | P1 | platform | todo | FE-01 | Shipped |
| FE-03 | Advanced timeline (optional product decision) | FE | P3 | platform | todo | FE-02 | Go/no-go recorded |
| DOC-05 | Banner on va SYSTEM_REFERENCE → generic pack paths | DOC | P2 | va-specs | todo | W1 | Cross-link |
| DOC-06 | Optional sync script va→business/video | DOC | P2 | both | todo | W6 | Documented; no silent overwrite |
| DOD-02 | **N3 DoD** all six boxes from adoption.md §7.5 Full va adoption | GOV | P0 | product | todo | W6, N3-CI-02/03 | All true |
| DP-10 | Other domains (podcast/research/…) **only after** DOD-02 | DP | P2 | product | todo | DOD-02 | N2 without stealing N3 |

---

### 5.7 Testing matrix (concrete)

| ID | Layer | Case | Depends on | Status |
|----|-------|------|------------|--------|
| T-10 | Unit | ALC activate denied | ALC-08 | todo |
| T-11 | Unit | lessons have agent_id + provenance | ALC-01/02 | todo |
| T-12 | Unit | cross-agent isolation | ALC-07 | todo |
| T-13 | Unit | invalid domain manifest | DP-06 | todo |
| T-14 | Unit | agent_genome cannot skip sandbox | EV-01 | todo |
| T-15 | Unit | video adapters write tool_effects | VID-05 | todo |
| T-16 | Unit | inventory count == 114 | N3-CI-01 | todo |
| T-17 | E2E | video spine lifecycle + approval | VID-09 | todo |
| T-18 | E2E | auto-reflect agent+org lessons | VID-10 | todo |
| T-19 | E2E | E1 still PASS | REG-01/02 | todo |
| T-20 | Eval | video golden/regression/adversarial | VID-06..08 | todo |
| T-21 | Eval | process DNA coverage vs PROCESSES.md | N3-P-10..12 | todo |
| T-22 | Load | multi-domain concurrency | T-02 | todo |
| T-23 | CI | orphan + retention gates | N3-CI-02/03 | todo |

### 5.8 Definition of Done

#### Platform (adoption.md §7.5)

| # | Gate | Linked tasks | Status |
|---|------|--------------|--------|
| D1 | ALC enforced for requires_alc packs | ALC-08/09 | todo |
| D2 | Video spine E2E green | VID-09/10 | todo |
| D3 | Second pack without runtime edits | DP-09 | todo |
| D4 | sandbox_only never bypassed | EV-01, BASE-07 | todo |
| D5 | Unit + e2e + business:eval green | T-10…T-20 | todo |
| D6 | status.md / handoff updated | DOC-02 | todo |

#### Full va adoption N3 (mandatory)

| # | Gate | Linked tasks | Status |
|---|------|--------------|--------|
| N3-D1 | Agent count + MAP == 114 | N3-A-01, N3-CI-01 | todo |
| N3-D2 | All 10 categories; meta includes orchestrator/planner/router/judge | N3-A-01, W1 | todo |
| N3-D3 | All processes indexed + DNA/docs | N3-P-01..12 | todo |
| N3-D4 | Every agent orchestrator-reachable | N3-P-14, N3-CI-02 | todo |
| N3-D5 | Retention CI enforced | N3-CI-03 | todo |
| N3-D6 | Activation waves documented; inactive remain draft/registered | W0–W6, DOC-02 | todo |

---

## 6. Category import checklist (N3 catalog)

Use with Appendix A pack ids. Status = folder+MAP+agent_spec present (Phase 2), not necessarily active.

| Cat | Range | Count | Wave for activation | Catalog status |
|-----|-------|-------|---------------------|----------------|
| 1 ATL | 1–5 | 5 | W1 (producer/director/screenwriter) + W4 rest | todo |
| 2 Cam | 6–8 | 3 | W3 | todo |
| 3 Edit | 9–18 | 10 | W3 | todo |
| 4 Snd | 19–22 | 4 | W3 | todo |
| 5 Perf | 23–27 | 5 | W3 | todo |
| 6 Dist | 28–31 | 4 | W4 | todo |
| 7 Edu | 32–45 | 14 | W4 | todo |
| 8 AI | 46–52 | 7 | W2–W3 | todo |
| 9 Meta | 53–80 | 28 | W1 spine + W5 rest | todo |
| 10 Sup | 81–114 | 34 | W5 | todo |
| **Total** | **1–114** | **114** | — | todo |

---

## 7. Process import checklist (N3)

| Process family | DNA / artifact targets | Status |
|----------------|------------------------|--------|
| 6-phase E2E production | `wf_video_production_e2e_v1` + phase subs | todo |
| Archetype A viral-hook | `wf_video_arch_a_viral_hook_v1` | todo |
| Archetypes B–J | `wf_video_arch_b` … `j` | todo |
| LQR (6 SVGs) | `wf_video_lqr_*` | todo |
| Human↔AI workflow maps | coverage matrix in PROCESSES.md | todo |
| Critique / QC / delivery fabric | eval steps + approvals in DNAs | todo |
| Agent management / UI processes | FE domain routes | todo |
| Deep-spec modules (GCA, aesthetics, RAG, DIA, …) | services + DNA hooks | todo |
| system_build_plan M0–M12 retarget | DOC note pack-on-generic | todo |

---

## 8. Risk mitigation actions

| ID | Risk | Mitigation task | Priority | Owner | Status | Linked |
|----|------|-----------------|----------|-------|--------|--------|
| R-01 | Dual platform rewrite | Enforce ADR; reject second FastAPI/LangGraph host in va | P0 | product | todo | P0-02 |
| R-02 | Loss of va fidelity | Provenance on seeds; MAP 1:1 | P0 | video-pack | todo | VID-12, P0-07 |
| R-03 | Unfinished N3 / agent drop | Wave 0 full import; Phase 5 mandatory; retention CI | P0 | product | todo | N3-CI-03, DOD-02 |
| R-04 | Orphan agents | standby_pool + orphan CI | P0 | platform | todo | N3-P-14 |
| R-05 | Shared memory pollution | ALC isolation tests | P0 | platform | todo | ALC-07, T-01 |
| R-06 | Evolution regression | Fitness + human gate + audit; no auto_promote | P0 | platform | todo | EV-07/09 |
| R-07 | Media API cost | Stubs in CI; allow-lists | P0 | platform | todo | VID-05 |
| R-08 | Break E1 / mark-100 | REG-01/02 every platform PR | P0 | platform | todo | REG-* |
| R-09 | Migration loss | Pack-in-git; backups before renames | P1 | platform | todo | P0-05 |
| R-10 | Doc language drift | EN canonical in pack; HK scripts in va | P2 | both | todo | N3-A-01 |
| R-11 | Scope explosion during Phase 2 | Catalog complete early; activate in waves | P0 | product | todo | P0-06, W* |

---

## 9. First 30 days

| Week | Focus IDs | Outcome |
|------|-----------|---------|
| **1** | P0-01…P0-09, DP-01/02 draft | Contract, 114 dirs, MAP, ROSTER, PROCESSES, baseline green |
| **2** | DP-03…DP-08, ALC-01…ALC-05, ALC-08 | Register + agent_id lessons + activate gate |
| **3** | ALC-06/07/10/13, EV-01, REG-01, DOC-01, N3-A-01 start | Retrieve-before-act; E1 green; start full SPEC import |
| **4** | N3-A-01/02, N3-P-02/03, VID-01…VID-10, FE-01, N3-CI-01, DOC-02 | Catalog complete + spine E2E |

| 30-day success | Status |
|----------------|--------|
| 114 agent dirs + MAP | todo |
| ALC + domain register working | todo |
| Spine E2E with human gate + agent lessons | todo |
| E1 still PASS | todo |

---

## 10. Critical path

```text
P0 approve/ADR → ROSTER+MAP+114 dirs → baseline green
        │
        ▼
 schemas → domain register → ALC agent_id lessons + gates → REG E1
        │
        ▼
 N3-A full 114 agent_spec → process DNA stubs → spine agents + viral-hook E2E
        │
        ├──► Phase 3 multi-gen learning
        │
        ├──► Phase 4 second pack + isolation (not N3 complete)
        │
        └──► Phase 5 waves W2–W6 + process wiring + orphan/retention CI → DOD-02 N3 DONE
```

---

## 11. Ownership summary

| Owner | Primary IDs |
|-------|-------------|
| **platform** | DP-*, ALC-*, EV-*, REG-*, N3-CI-*, most T-*, VID adapters/runtime |
| **video-pack** | N3-A-*, N3-P-*, VID DNA/evals, MAP content |
| **va-specs** | P0-03/04/10, VID-12, DOC-05, fidelity |
| **product** | P0-01/02/11, EV-07, DOD-*, DP-10 gate, R-01/R-03 |
| **both** | P0-07, W6, R-10 |

---

## 12. Progress rollup

| Bucket | ~Count | todo | leverage | done |
|--------|--------|------|----------|------|
| BASE | 12 | 0 | 12 | 0 |
| Phase 0 | 12 | 12 | 0 | 0 |
| Phase 1 | 22 | 22 | 0 | 0 |
| Phase 2 | 20 | 20 | 0 | 0 |
| Phase 3 | 7 | 7 | 0 | 0 |
| Phase 4 | 10 | 10 | 0 | 0 |
| Phase 5 waves + process | 18 | 17 | 1 | 0 |
| Tests | 14 | 14 | 0 | 0 |
| Risks | 11 | 11 | 0 | 0 |
| **Total** | **~126** | **~113** | **13** | **0** |

Update status cells as work completes. **N3 is not done until DOD-02 is true.**

---

## 13. Related documents

| Document | Role |
|----------|------|
| `adoption.md` v2.2 | Strategy + Appendix A roster + Appendix B readiness |
| `adoption_hk.md` / `adoption_hk.script.txt` | ZH + YouTube script |
| `review_adoption.md` | Original brief |
| `status.md` / `memory/handoff.md` | Live status |
| va `study/agents.md` | Authoritative 114 names |
| va `study/SYSTEM_REFERENCE.md` | Process integration map |

---

## 14. Changelog

| Version | Date | Notes |
|---------|------|-------|
| 1.0 | 2026-07-10 | Initial tables from adoption.md v2 |
| 2.0 | 2026-07-10 | Research-backed BASE leverage + as-built gaps |
| 3.0 | 2026-07-10 | Aligned to adoption.md v2.2 N3 |
| 3.1 | 2026-07-10 | §15 Detailed step-by-step playbooks |
| **3.2** | **2026-07-10** | **Rethink:** §0 principles; L0/L1/L2; critical path §0.3; SPEC/DNA theater fixes; ALC on active; namespace split; §15 is reference depth |

---

## 15. Detailed step-by-step playbooks

Each parent task from §5 is broken into ordered micro-steps.  
**Critical-path parents (§0.3):** complete every micro-step before marking parent `done`.  
**Non-critical parents:** use playbooks as needed; do not block spine demo.  
Commands assume repo root `generic-swarm-ops` unless noted. Paths use forward slashes.

### 15.0 Conventions used in playbooks

| Convention | Meaning |
|------------|---------|
| `va/` | `C:\Project\va-agent-swarm` (or clone path) |
| `gso/` | `C:\Project\generic-swarm-ops` |
| **Verify** | Must pass before next step |
| **Stop** | Hard gate — do not continue if fail |
| Stub SPEC | Minimal SPEC.md: name, va id, category, 3–5 bullet duties, source link, status `draft` |
| Full SPEC | Duties + tools + critique partners + ALC notes + provenance from va deep-spec if any |

**Daily loop (recommended):**

| Step | Action |
|------|--------|
| 1 | Pick next parent ID from critical path (§10) |
| 2 | Open its playbook subsection below |
| 3 | Execute `.s1`, `.s2`, … in order; tick Status |
| 4 | Run **Verify** commands for that parent |
| 5 | Commit with message `feat(adoption): <parent-id> <short>` |
| 6 | Re-run REG baseline if you touched `runtime.py` or routes |

---

### 15.1 Phase 0 playbooks

#### P0-01 — Approve strategy

| Step | Action | Status |
|------|--------|--------|
| P0-01.s1 | Open `adoption.md` v2.2 and this plan; confirm N1/N2/N3 understood | todo |
| P0-01.s2 | Record approval in `status.md` under Latest update: date + “adoption v2.2 + plan v3.1 approved” | todo |
| P0-01.s3 | Optionally open GitHub issue/milestone “Video Domain Pack N3” linked to this plan | todo |

**Verify:** `status.md` contains approval note.

#### P0-02 — ADR (dual-repo + pack-on-generic + N3 retention)

| Step | Action | Status |
|------|--------|--------|
| P0-02.s1 | Create `docs/adr/` if missing | todo |
| P0-02.s2 | Write `docs/adr/0001-video-domain-pack-on-generic.md` with: Context, Decision, Consequences | todo |
| P0-02.s3 | Decision must include: (a) generic is only control plane; (b) no LangGraph/Temporal second host in va; (c) all 114 agents live under `business/video/agents/`; (d) deletion of roster agents forbidden | todo |
| P0-02.s4 | Link ADR from `business/video/README.md` (create README stub if needed) | todo |

**Verify:** ADR file exists and contains the four decision bullets.

#### P0-03 — Export ROSTER.json (114)

| Step | Action | Status |
|------|--------|--------|
| P0-03.s1 | Open `va/study/agents.md` | todo |
| P0-03.s2 | Parse all table rows `\| N \| **NameAgent**` for N=1..114 (Agent-named rows only) | todo |
| P0-03.s3 | Cross-check counts per category: 5+3+10+4+5+4+14+7+28+34 = 114 | todo |
| P0-03.s4 | Create `gso/business/video/` if missing | todo |
| P0-03.s5 | Write `business/video/ROSTER.json` array of objects: `{ "id": 1, "name": "DirectorAgent", "category": 1, "pack_id": "video.director" }` for all 114 using Appendix A pack ids from `adoption.md` | todo |
| P0-03.s6 | Validate JSON parses; `length == 114`; unique `id` and unique `pack_id` | todo |

**Verify:**

```bash
# PowerShell example
(Get-Content business/video/ROSTER.json -Raw | ConvertFrom-Json).Count  # expect 114
```

**Stop** if count ≠ 114.

#### P0-04 — Export PROCESSES.md

| Step | Action | Status |
|------|--------|--------|
| P0-04.s1 | Read `va/study/SYSTEM_REFERENCE.md` §6.1 (six phases) | todo |
| P0-04.s2 | List archetype files `va/study/workflows/A-*.svg` … `J-*.svg` (10) | todo |
| P0-04.s3 | List LQR files `lqr-*.svg` (6) | todo |
| P0-04.s4 | List UI process docs under `va/study/ui/*.md` (EN only) | todo |
| P0-04.s5 | Write `business/video/PROCESSES.md` with sections: Orchestration spine, 6-phase E2E, A–J, LQR, UI processes, Deep-spec modules | todo |
| P0-04.s6 | For each process row add columns: `process_id`, `source_path`, `target_dna_id` (placeholder OK), `entry_agent` (`video.orchestrator` or `video.planner`), `status` (`stub`/`draft`/`ready`) | todo |

**Verify:** PROCESSES.md mentions Orchestrator #53 / Planner #54, phases 1–6, archetypes A–J, and LQR.

#### P0-05 — Skeleton `business/video/`

| Step | Action | Status |
|------|--------|--------|
| P0-05.s1 | Create dirs: `agents/`, `workflows/`, `evals/golden/`, `evals/regression/`, `evals/adversarial/`, `knowledge/seeds/`, `tools/`, `policies/`, `ui/`, `schemas/` (optional local) | todo |
| P0-05.s2 | Write `business/video/README.md`: purpose, N3 rules, link to ROSTER/MAP/PROCESSES/ADR | todo |
| P0-05.s3 | Write draft `business/video/manifest.json` with `domain_id: "video"`, `requires_alc: true`, `version: "0.1.0"` (agents array can be filled after P0-06) | todo |
| P0-05.s4 | Write `business/video/tools/adapters.md` stub listing planned `video.*` tools | todo |

**Verify:** tree exists; README states retention of all 114 agents.

#### P0-06 — 114 placeholder agent directories

| Step | Action | Status |
|------|--------|--------|
| P0-06.s1 | For each `pack_id` in ROSTER.json, create `business/video/agents/<pack_id>/` | todo |
| P0-06.s2 | In each dir create minimal files: `agent_spec.json` (draft), `SPEC.md` (stub SPEC), empty `prompts/.gitkeep`, `rubrics/.gitkeep` | todo |
| P0-06.s3 | `agent_spec.json` minimum fields: `id`, `va_id`, `name`, `domain_id: "video"`, `status: "draft"`, `requires_alc: true`, `allowed_memory_scopes: ["agent","workflow_memory","organization_memory"]`, `allowed_tools: []`, `hooks: { "reflect": true }`, `alc_version: "0.1.0"` | todo |
| P0-06.s4 | Run directory count == 114 | todo |

**Verify:**

```bash
# expect 114
(Get-ChildItem business/video/agents -Directory).Count
```

**Stop** if ≠ 114.

#### P0-07 — MAP.md (1:1)

| Step | Action | Status |
|------|--------|--------|
| P0-07.s1 | Create `business/video/MAP.md` with header table: va_id \| name \| pack_id \| category \| va_source \| generic_path \| runtime_status \| notes | todo |
| P0-07.s2 | One row per ROSTER entry; `generic_path` = `business/video/agents/<pack_id>/` | todo |
| P0-07.s3 | For agents with deep-spec files, set `va_source` to that path; else `study/agents.md#<id>` | todo |
| P0-07.s4 | Confirm row count == 114 | todo |

**Verify:** no blank pack_id; no duplicate pack_id.

#### P0-08 — example_domain skeleton

| Step | Action | Status |
|------|--------|--------|
| P0-08.s1 | Create `business/example_domain/` with same subfolder pattern as video (smaller) | todo |
| P0-08.s2 | Add 1–2 toy agents e.g. `example.worker`, `example.reviewer` with ALC fields | todo |
| P0-08.s3 | Add one toy workflow DNA file `wf_example_echo_v1.dna.json` (minimal valid DNA later in Phase 1) | todo |
| P0-08.s4 | README explains N2 purpose only | todo |

#### P0-09 — Baseline green

| Step | Action | Status |
|------|--------|--------|
| P0-09.s1 | From `gso/`: run root tests used in `status.md` (`npm test` if applicable) | todo |
| P0-09.s2 | Backend: `cd backend` + unittest unit suite | todo |
| P0-09.s3 | Backend: e2e `test_e1_operator_path` | todo |
| P0-09.s4 | Frontend: `pnpm lint`, `pnpm typecheck`, `pnpm test` | todo |
| P0-09.s5 | Paste pass evidence (date + summary) into `status.md` or `reviews/mark100-logs/` | todo |

**Stop** if E1 fails — fix before Phase 1 code changes.

#### P0-10 — Deep-spec inventory

| Step | Action | Status |
|------|--------|--------|
| P0-10.s1 | Enumerate `va/study/*specification*.md` and related | todo |
| P0-10.s2 | Add table to PROCESSES.md: module → files → pack target (service or agent) | todo |
| P0-10.s3 | Mark coding agent as sandbox-only / no host rewrite | todo |

#### P0-11 / P0-12

| Step | Action | Status |
|------|--------|--------|
| P0-11.s1 | Copy risk table §8; add Owner column filled for each R-id | todo |
| P0-12.s1 | ADR appendix: sync = PR copy from va to generic; submodule deferred | todo |
| P0-12.s2 | Document “never leave agents only in va after Wave 0” | todo |

---

### 15.2 Phase 1 playbooks (Domain Pack + ALC)

#### DP-01…DP-03 — Schemas

| Step | Action | Status |
|------|--------|--------|
| DP-01.s1 | Copy style from `business/schemas/workflow-dna.schema.json` (JSON Schema draft used in repo) | todo |
| DP-01.s2 | Author `domain-manifest.schema.json`: required `domain_id`, `version`, `requires_alc`, `agents[]`, `workflows[]` | todo |
| DP-02.s1 | Author `agent-spec.schema.json`: required `id`, `domain_id`, `status`, `requires_alc`, `allowed_memory_scopes`, `hooks.reflect`, `alc_version` | todo |
| DP-02.s2 | If `requires_alc` true, schema must require `"agent"` in `allowed_memory_scopes` | todo |
| DP-03.s1 | Author `learning-log.schema.json` with required `agent_id`, `text` or `lesson_text`, `provenance` | todo |
| DP-0x.s_fix | Add positive + negative fixtures under `business/fixtures/` or tests | todo |

**Verify:** invalid fixtures fail validation; valid pass.

#### DP-05 — Domain register

| Step | Action | Status |
|------|--------|--------|
| DP-05.s1 | Add `backend/app/api/v1/routes/domains.py` with `POST /register` (auth + RBAC) | todo |
| DP-05.s2 | Implement loader: read `business/<domain>/manifest.json`, validate schema, load agents into org draft catalog (do not force active) | todo |
| DP-05.s3 | Wire router in `backend/app/api/v1/router.py` prefix `/domains` | todo |
| DP-05.s4 | Optional CLI `npm run domain:register -- --domain video --dry-run` | todo |
| DP-05.s5 | Unit test: dry-run video + example_domain | todo |

**Verify:** dry-run returns counts; no production DNA mutation.

#### DP-06 — Fail closed

| Step | Action | Status |
|------|--------|--------|
| DP-06.s1 | Missing required_alc field → 400 | todo |
| DP-06.s2 | Unknown agent path → 400 | todo |
| DP-06.s3 | Malformed JSON → 400 | todo |

#### ALC-01 — Lesson.agent_id

| Step | Action | Status |
|------|--------|--------|
| ALC-01.s1 | Edit `backend/app/infrastructure/self_improvement/lessons.py`: add `agent_id: str \| None = None` | todo |
| ALC-01.s2 | Include `agent_id` in `to_dict` / `lesson_from_dict` | todo |
| ALC-01.s3 | Dedup key: same text + workflow_id + agent_id | todo |
| ALC-01.s4 | `retrieve(..., agent_id=None)` filters when set | todo |
| ALC-01.s5 | Unit: old lessons without agent_id still load | todo |

#### ALC-02 — Split reflect by step agent

| Step | Action | Status |
|------|--------|--------|
| ALC-02.s1 | In `reflection.py` / `reflect_on_workflow_run`, for each failed/waiting/completed step read `step["agent"]` or `step["agent_id"]` | todo |
| ALC-02.s2 | Emit lessons tagged with that agent_id; if missing agent, tag `agent_id: null` + workflow-level | todo |
| ALC-02.s3 | When writing memory via `_write_memory`, pass agent when available (not always `None`) | todo |
| ALC-02.s4 | Unit: multi-step multi-agent run → ≥2 distinct agent_id lessons | todo |

#### ALC-03 / ALC-04 — Agent reflect API

| Step | Action | Status |
|------|--------|--------|
| ALC-03.s1 | `POST /improvement/reflect/agent/{agent_id}` body optional `{ "run_id": "..." }` | todo |
| ALC-03.s2 | Filter lessons/run steps to that agent only | todo |
| ALC-04.s1 | Extend `GET /improvement/lessons` with `agent_id` query | todo |
| ALC-04.s2 | OpenAPI / frontend client regen if project uses `pnpm api:generate` | todo |

#### ALC-05 — Episodic write

| Step | Action | Status |
|------|--------|--------|
| ALC-05.s1 | On step completion in runtime, append episode: agent_id, run_id, step_id, status, summary, critique | todo |
| ALC-05.s2 | Store in collection `agent_episodes` or memory scope `agent` | todo |
| ALC-05.s3 | Audit event `agent.episode_written` (optional but recommended) | todo |

#### ALC-06 — Pre-step inject

| Step | Action | Status |
|------|--------|--------|
| ALC-06.s1 | Before tool/LLM step execution, load top-k lessons for step agent + agent memory | todo |
| ALC-06.s2 | Attach to step context under `injected_lessons` (for logs/tests) | todo |
| ALC-06.s3 | Unit mock: assert retrieve called with correct agent_id | todo |

#### ALC-07 — Isolation

| Step | Action | Status |
|------|--------|--------|
| ALC-07.s1 | Test agent A retrieve with B’s agent_id returns empty/403 | todo |
| ALC-07.s2 | Enforce in memory search when `acting_agent_id` set | todo |

#### ALC-08 / ALC-09 — Activation gates

| Step | Action | Status |
|------|--------|--------|
| ALC-08.s1 | In `update_agent_status(..., "active")` only (not draft/registered): if domain requires_alc → check alc_version, agent scope, hooks.reflect | todo |
| ALC-08.s2 | Fail with clear error code `alc_required`; **draft import must still succeed** | todo |
| ALC-09.s1 | DNA `production_ready` / activate version: each **active** step agent must pass ALC; draft-only agents allowed only if DNA not production_ready | todo |
| ALC-09.s2 | Unit: production_ready DNA with non-ALC agent denied; draft DNA with draft agents allowed | todo |

#### ALC-10 — Auto-reflect agent lessons

| Step | Action | Status |
|------|--------|--------|
| ALC-10.s1 | `_auto_reflect_if_enabled` already calls reflect — ensure ALC-02 path used | todo |
| ALC-10.s2 | Confirm disk artifact under `business/evolution/lessons-learned/` includes agent_id fields when present | todo |

#### ALC-11…ALC-13 / EV-01 / REG-01

| Step | Action | Status |
|------|--------|--------|
| ALC-11.s1 | `GET /improvement/metrics?agent_id=` returns counts + utility | todo |
| ALC-12.s1 | example agents scopes include `agent`; activate after register | todo |
| ALC-13.s1 | Test: run1 → lessons; run2 → retrieve uses lessons (uses counter++) | todo |
| EV-01.s1 | propose evolution with `variant_type: agent_genome` forces sandbox_only true | todo |
| EV-01.s2 | Reject payload with direct production mutation flag | todo |
| REG-01.s1 | Re-run e2e E1 + unit suite after all Phase 1 merges | todo |
| DOC-01.s1 | Write `docs/domain-packs.md` (register, ALC, N3 retention) | todo |
| DOC-01.s2 | Patch `structure.md` short section linking Domain Pack + ALC | todo |

---

### 15.3 Phase 2 playbooks (catalog + spine)

#### N3-A-01 — L0 catalog for all 114 (not full prose for all)

| Step | Action | Status |
|------|--------|--------|
| N3-A-01.s1 | Batch by category 1→10 (do not skip meta/support) — **L0 only** | todo |
| N3-A-01.s2 | For each agent: confirm MAP row + folder + minimal agent_spec from P0-06 | todo |
| N3-A-01.s3 | Stub SPEC.md: one paragraph role + link to va agents.md id + status draft (**not** full deep-spec dump) | todo |
| N3-A-01.s4 | **Spine only** (orchestrator, planner, router, judge, producer, director, screenwriter, + intent/research): fuller SPEC + tools planned | todo |
| N3-A-01.s5 | Defer deep SPEC for remaining agents to **activation wave** (Phase 5 / W*) | todo |
| N3-A-01.s6 | Inventory count == 114 after each category batch | todo |

**Verify:** 114 agent_spec.json parse; inventory green; spine SPECs richer than stubs.

#### N3-A-02 — ALC fields complete

| Step | Action | Status |
|------|--------|--------|
| N3-A-02.s1 | Script validate every agent_spec against agent-spec.schema.json | todo |
| N3-A-02.s2 | Fix any missing `agent` scope or reflect hook | todo |
| N3-A-02.s3 | Set `manifest.json` `agents` array to all 114 pack_ids | todo |

#### N3-P-01…P-03 — Processes & DNA stubs

| Step | Action | Status |
|------|--------|--------|
| N3-P-01.s1 | Expand PROCESSES.md matrix: each process → target_dna_id → agent pack_ids | todo |
| N3-P-02.s1 | Create DNA stub files for: e2e, arch_a…arch_j (10), lqr_* (at least 1 overview + 5 siblings or 6 files) | todo |
| N3-P-02.s2 | Each DNA must satisfy workflow-dna.schema.json required fields (use example DNA as template) | todo |
| N3-P-02.s3 | Steps may be placeholders but must name real pack_ids from roster | todo |
| N3-P-03.s1 | First step agent = `video.orchestrator` or `video.planner` on every executable DNA | todo |
| N3-P-03.s2 | Document exception policy: none allowed for production_ready | todo |

**DNA stub template approach:** copy `business/examples/workflow-dna.example.json` → rename ids → replace steps agents with video pack ids → set `production_ready: false` → `domain: "video"`.

#### VID-01 — Spine agents active

| Step | Action | Status |
|------|--------|--------|
| VID-01.s1 | Ensure spine agent_specs validate ALC | todo |
| VID-01.s2 | Register video pack into runtime (domain register or seed path) | todo |
| VID-01.s3 | Activate spine agents via API/admin (status active) | todo |
| VID-01.s4 | Confirm non-spine remain draft | todo |

#### VID-02 — Intent + research

| Step | Action | Status |
|------|--------|--------|
| VID-02.s1 | Map DIA spec to intent agent pack id (or dedicated `video` intent agent if added to MAP) | todo |
| VID-02.s2 | Wire research agent to knowledge search tool (existing Tier-0 OK) | todo |
| VID-02.s3 | Add steps on spine DNA for intent → research | todo |

#### VID-03 — Viral-hook DNA (runnable)

| Step | Action | Status |
|------|--------|--------|
| VID-03.s1 | Author full step list for archetype A from `A-viral-hook.svg` + SYSTEM_REFERENCE phases 1–2 | todo |
| VID-03.s2 | Recommended order: orchestrator/planner → intent → producer gate → director/screenwriter → research/aesthetics → media_gen_stub → qc_stub → human_gate? → package | todo |
| VID-03.s3 | Set human_gate_required true on irreversible publish-like step | todo |
| VID-03.s4 | Validate DNA; create workflow version in runtime; do not set production_ready until ALC+evals | todo |

#### VID-04 / VID-05 — Tools

| Step | Action | Status |
|------|--------|--------|
| VID-04.s1 | Add tool entries: `video_media_gen_stub`, `video_script_format`, `video_qc_stub` to tool-permission-register.json | todo |
| VID-04.s2 | Scope tools to video workflows; list requires_human_gate_for as needed | todo |
| VID-05.s1 | Implement adapter functions in `adapters.py` returning `_effect(...)` like crm/email | todo |
| VID-05.s2 | Register in `TOOL_ADAPTERS` dict | todo |
| VID-05.s3 | Unit tests assert tool_effects ids and status ok | todo |

#### VID-06…VID-08 — Evals

| Step | Action | Status |
|------|--------|--------|
| VID-06.s1 | Create golden JSON under `business/video/evals/golden/` modeled on customer-onboarding goldens | todo |
| VID-06.s2 | Assertions: human gate hit when expected; final status succeeded | todo |
| VID-07.s1 | Regression: remove human_gate on irreversible step → must fail validate | todo |
| VID-08.s1 | Adversarial fixture: malicious script input; tools remain allow-listed | todo |
| VID-0x.s_harness | Wire pack evals into `npm run business:eval` discovery if needed | todo |

#### VID-09 / VID-10 — E2E tests

| Step | Action | Status |
|------|--------|--------|
| VID-09.s1 | Add `backend/app/tests/e2e/test_video_spine_path.py` mirroring E1 pattern | todo |
| VID-09.s2 | Steps: auth → ensure agents → start viral-hook run → approve if needed → succeeded | todo |
| VID-10.s1 | After terminal, call reflect; assert lessons with agent_id for spine agents | todo |
| VID-10.s2 | Assert auto-reflect flag path if enabled | todo |

#### FE-01 — Full roster UI

| Step | Action | Status |
|------|--------|--------|
| FE-01.s1 | Add route `/app/domains/video` or agents filter `domain=video` | todo |
| FE-01.s2 | List all 114 with status badge draft/active | todo |
| FE-01.s3 | Vitest: renders without crash; filter works | todo |

#### N3-CI-01 — Inventory CI

| Step | Action | Status |
|------|--------|--------|
| N3-CI-01.s1 | Script reads ROSTER.json + scans `business/video/agents/*` | todo |
| N3-CI-01.s2 | Fail if missing pack_id or extras without MAP note | todo |
| N3-CI-01.s3 | Hook into `npm run business:validate` or dedicated `npm run video:inventory` | todo |

#### VID-11…DOC-02 / REG-02

| Step | Action | Status |
|------|--------|--------|
| VID-11.s1 | Manual or e2e: Improve reflect→propose on video run; variant sandbox_only | todo |
| VID-12.s1 | Copy curated seeds with frontmatter provenance `source: va-agent-swarm@<gitsha>` | todo |
| VID-13.s1 | Index via knowledge API; search with acting_agent_id | todo |
| REG-02.s1 | Re-run E1 after video adapters merged | todo |
| DOC-02.s1 | Update status.md + memory/handoff.md with operator path and catalog count 114 | todo |

---

### 15.4 Phase 3 playbooks (learning)

| Parent | Micro-steps | Status |
|--------|-------------|--------|
| EV-03 | s1 Create ≥2 sandbox variants from video failures; s2 evaluate each on video goldens; s3 store fitness in archive | todo |
| EV-04 | s1 Mutate planner genome; s2 mutate aesthetics/director genome; s3 joint eval scorecard | todo |
| EV-05 | s1 Expose metrics endpoint in FE panel or docs; s2 show reuse/utility | todo |
| EV-06 | s1 Propose skill under `_sandbox/`; s2 human promote only | todo |
| EV-07 | s1 Governance checklist review; s2 record decision; s3 confirm auto_promote still impossible | todo |
| EV-08 | s1 Baseline metric; s2 post-evolution metric; s3 no prod DNA auto change | todo |
| EV-09 | s1 Query audit for evolution events; s2 assert propose/eval/canary present | todo |

---

### 15.5 Phase 4 playbooks

| Parent | Micro-steps | Status |
|--------|-------------|--------|
| DP-09 | s1 Scaffold second pack; s2 register without editing runtime core; s3 one toy DNA | todo |
| T-01 | s1 Write integration test video memory vs research agent_id; s2 assert empty/deny | todo |
| T-02 | s1 Script N=20 concurrent starts mixed domains; s2 assert no crash; s3 lesson count stable | todo |
| T-03 | s1 If archive large, measure list latency; s2 record p95 note | todo |
| T-04 | s1 Open 5 run SSE streams; s2 FE remains usable | todo |
| T-05 | s1 Attempt tool misuse cases; s2 allow-list holds | todo |
| T-06 | s1 Add adversarial to CI required; s2 fail pipeline on regression | todo |
| DOC-03 | s1 Write Add Domain Pack runbook; s2 engine_range versioning | todo |
| DOC-04 | s1 Platform PR checklist; s2 Pack PR checklist | todo |
| DOD-01 | s1 Tick platform D1–D6 only when evidence linked | todo |

---

### 15.6 Phase 5 playbooks (N3 complete)

#### Per-wave activation checklist (apply to W2–W5)

| Step | Action | Status |
|------|--------|--------|
| Wx.s1 | Select pack_ids for wave from §5.6.1 | todo |
| Wx.s2 | Ensure agent_spec ALC validates | todo |
| Wx.s3 | Ensure each agent appears in ≥1 DNA step **or** add to standby_pool | todo |
| Wx.s4 | Activate agent (status active) or keep registered if intentionally standby | todo |
| Wx.s5 | Run smoke: register pack + start DNA that includes at least one new agent | todo |
| Wx.s6 | Update MAP.md runtime_status column | todo |
| Wx.s7 | Re-run inventory + orphan check | todo |

#### N3-P-10 — Six-phase E2E DNA

| Step | Action | Status |
|------|--------|--------|
| N3-P-10.s1 | Map SYSTEM_REFERENCE phases 1–6 to step groups | todo |
| N3-P-10.s2 | Bind real pack_ids for each phase (stubs for media) | todo |
| N3-P-10.s3 | Entry orchestrator/planner; human gates on irreversible | todo |
| N3-P-10.s4 | Validate DNA; optional dry-run execution | todo |

#### N3-P-11 — Archetypes B–J

| Step | Action | Status |
|------|--------|--------|
| N3-P-11.s1 | For each SVG B–J, list major stages | todo |
| N3-P-11.s2 | Create/flesh DNA with orchestrator entry | todo |
| N3-P-11.s3 | Ensure feature-film-class DNA can reference full roster via standby where needed | todo |
| N3-P-11.s4 | Coverage matrix: 10/10 archetypes done | todo |

#### N3-P-12 — LQR family

| Step | Action | Status |
|------|--------|--------|
| N3-P-12.s1 | One DNA per LQR SVG or one parent DNA with subflows documented | todo |
| N3-P-12.s2 | Include continuity / AIQA / quality-gate agents | todo |
| N3-P-12.s3 | Mark PROCESSES.md LQR rows ready | todo |

#### N3-P-13 — Deep-spec modules

| Step | Action | Status |
|------|--------|--------|
| N3-P-13.s1 | GCA as shared service/tool used by director/screenwriter | todo |
| N3-P-13.s2 | Aesthetics critic hooked to gen steps | todo |
| N3-P-13.s3 | Agentic RAG → knowledge pipeline docs + APIs | todo |
| N3-P-13.s4 | DIA → intent steps | todo |
| N3-P-13.s5 | Optimization agents linked to delivery DNA | todo |
| N3-P-13.s6 | Coding agent constrained sandbox-only (document) | todo |

#### N3-P-14 / CI / DOD-02

| Step | Action | Status |
|------|--------|--------|
| N3-P-14.s1 | Build `standby_pool.json`: all 114 pack_ids with route metadata | todo |
| N3-P-14.s2 | Router/orchestrator can select any pool member | todo |
| N3-P-14.s3 | Orphan script: agent not in any DNA step and not in pool → fail | todo |
| N3-CI-02.s1 | Add orphan check to CI | todo |
| N3-CI-03.s1 | Fail if Appendix A directory removed | todo |
| N3-A-10.s1 | Walk categories activating remaining agents per wave checklist | todo |
| FE-02.s1 | Dashboard: pipeline stages, asset placeholders, roster status counts | todo |
| DOC-05.s1 | Banner on va SYSTEM_REFERENCE linking generic paths | todo |
| DOC-06.s1 | Sync script documented; dry-run default | todo |
| DOD-02.s1 | Collect evidence links for N3-D1…D6 | todo |
| DOD-02.s2 | Product sign-off in status.md “N3 complete” | todo |
| DP-10.s1 | Only after DOD-02, schedule other domains | todo |

---

### 15.7 Detailed test execution steps

| Test ID | Detailed steps | Status |
|---------|----------------|--------|
| T-10 | Create agent missing agent scope → activate → expect 4xx alc_required | todo |
| T-11 | Reflect multi-agent run → GET lessons?agent_id= → non-empty + provenance | todo |
| T-12 | Write episode as A; retrieve as B → empty/deny | todo |
| T-13 | POST domains/register bad manifest → 400 | todo |
| T-14 | propose agent_genome with production mutation → reject | todo |
| T-15 | Call video_media_gen_stub → tool_effects row exists | todo |
| T-16 | Run inventory script → exit 0 only if 114 | todo |
| T-17 | Full video spine e2e | todo |
| T-18 | Reflect after e2e → agent lessons | todo |
| T-19 | E1 e2e green | todo |
| T-20 | business:eval includes video pack fixtures | todo |
| T-21 | Script: every PROCESSES.md DNA file exists | todo |
| T-22 | Load harness 20 concurrent | todo |
| T-23 | CI config includes inventory+orphan+retention | todo |

---

### 15.8 Operator runbook (spine demo after Phase 2)

| Step | Action | Status |
|------|--------|--------|
| OP.s1 | Start backend (Postgres + FastAPI per backend README) | todo |
| OP.s2 | Start frontend with `NEXT_PUBLIC_DEMO_MODE=false` | todo |
| OP.s3 | Login seed admin | todo |
| OP.s4 | Confirm video agents visible (114 list / filter) | todo |
| OP.s5 | Start `wf_video_arch_a_viral_hook_v1` run | todo |
| OP.s6 | Approve human gate if prompted | todo |
| OP.s7 | Open Improve → Reflect; confirm agent lessons | todo |
| OP.s8 | Propose sandbox variant; confirm sandbox_only | todo |
| OP.s9 | Log evidence in handoff.md | todo |

---

### 15.9 Definition of Done evidence checklist

| Gate | Required evidence artifact | Status |
|------|---------------------------|--------|
| D1 ALC | Unit log T-10 + code ref ALC-08 | todo |
| D2 Spine E2E | T-17 log + run_id | todo |
| D3 Second pack | DP-09 dry-run output | todo |
| D4 sandbox_only | T-14 + evolution test | todo |
| D5 Suites green | CI URL or local log bundle | todo |
| D6 Handoff | status.md + handoff.md paragraphs | todo |
| N3-D1 | inventory script output 114 | todo |
| N3-D2 | MAP category counts | todo |
| N3-D3 | PROCESSES.md all rows ready | todo |
| N3-D4 | orphan script exit 0 | todo |
| N3-D5 | retention CI job present | todo |
| N3-D6 | waves table statuses done | todo |

---

*End of adoption action plan v3.1*
