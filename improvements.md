# Improvements Plan for generic-swarm-ops

**Version:** 1.0  
**Date:** 2026-07-11  
**Status:** Ready for coding agent execution (spec-driven, phased, production-first)  
**Purpose:** Transform generic-swarm-ops into the definitive **universal governed Multi-Agent (MMA) host/platform** while cleanly enabling the va-agent-swarm video Domain Pack (and future packs). This plan directly addresses the analysis in `repo_compare.md` and executes/enhances the adoption strategy in `adoption.md` v2.3.  

**Audience:** Coding agents (Claude Code, Kiro, Cursor, OpenClaw, Hermes, self-refining N1ch01as Architect harnesses), human reviewers, and future contributors.  
**Output Format for Agents:** Feed sections as task.md-style specs. Each Wave/Phase has clear non-negotiables, file paths, acceptance criteria, tests, and traceability. Use critic loops, sandbox discipline, and E1 regression protection.

---

## 1. Executive Summary

generic-swarm-ops is already a **high-maturity production platform** (mark ~100, E1 operator path PASS, shipped FastAPI runtime, Workflow DNA, evolution sandbox, governance, Next.js ops console, self-improvement harness). However, it lacks the formal **Domain Pack architecture** and **Agent Learning Contract (ALC)** needed to become a true universal host for dozens of MMA systems.

`va-agent-swarm` is a **world-class complete specification corpus** (114-agent roster across 10 categories, deep functional/technical specs, 6-phase E2E processes, archetypes A–J, LQR family, orchestration spine, rich knowledge corpus) but has **zero executable runtime**.

**Recommended Merge (from repo_compare.md + adoption.md v2.3):**
- **generic-swarm-ops** = Universal governed MMA host/platform (runtime, governance, evolution, ALC enforcement, Domain Pack SDK, multi-tenant FE shell).
- **va-agent-swarm** = Complete **Video Production Domain Pack** imported into `business/video/` (full 114 agents + full processes retained forever in generic; va repo stays upstream research/narration/scripts SoT).

**User Concern Addressed:**
- After these improvements, **generic-swarm-ops will strongly benefit other projects** (tutoring/DeepTutor, trading automation, content pipelines, enterprise modernization, education agents, etc.).
- **No business-specific (VA/video) logic, info, or memory pollutes the generic core.** All domain logic is strictly isolated under `business/<domain_id>/` packs with manifest-driven registration, namespace isolation (`video.*` tools), and org/domain-scoped memory.

**Outcome:** A production-ready, future-proof platform where any new domain can be onboarded in hours/days (copy skeleton → manifest → agents + DNA → register → ALC-enabled learning) while the video pack delivers the full 114-agent autonomous swarm.

**Non-Negotiables (N1/N2/N3 from adoption.md):**
- **N1:** All video-specific business logic stays in `business/video/` pack. Every agent gets mandatory autonomous per-agent learning via ALC.
- **N2:** generic becomes universal foundation for **dozens** of MMA systems (Domain Pack contract, isolation, extensibility).
- **N3:** **Adopt ALL 114 agents + ALL business processes** from va into generic `business/video/` (roster + MAP + dirs + specs). **No agent dropped.** Retention policy enforced by inventory CI. Full catalog present before declaring adoption complete.

**Success Definition:**
- Platform: Domain Pack SDK + ALC works for video + second example pack; every active agent accumulates scoped lessons; E1/mark~100 protected.
- Video Pack (N3): All 114 agents in `business/video/agents/` (L0 catalog complete); all processes indexed + spine runnable (L2); orchestrator-down integrity; retention forever.
- Other Projects: Clear reuse playbook; new packs inherit full platform power without forking.

---

## 2. Background & Context

### 2.1 Current State of generic-swarm-ops (from deep repo scan 2026-07-11)
- **Strengths (Production-Ready Core):**
  - Backend: FastAPI + `runtime.py` (workflow engine, states, SSE, workers, tool effects), Postgres `runtime_state` JSONB, full auth/RBAC/permissions, audit logs, approvals, idempotency, rate limiting.
  - Workflow: Mature `WorkflowDNA` schema + validators + bounded execution.
  - Evolution: Sandbox (propose → test → canary → promote/rollback), `corpus_eval.py`, lessons, reflection, skill sandbox, GEPA-style natural language improvement. **Never mutates production directly.**
  - Governance/Security: Risk tiers (0–5), human gates, OWASP/Agentic mapping, tool permission broker, red-team, threat models, model cards, assurance cases.
  - Knowledge/Memory: Tiered hybrid retrieval (Tier-0 vector + K1-lite), hybrid memory types (event/episodic/semantic/procedural/decision/exception/evaluation/provenance), scopes, provenance always.
  - Self-Improvement: APIs for reflect/lessons/auto-propose/loops; FE `ImproveRunButton` + evolution archive panel.
  - Frontend: Next.js 15+ production ops console (dashboard, agents/tools/workflows/runs, approvals queue, knowledge browser, real-time SSE, permission-aware nav, loading/empty/error states, OpenDesign MCP).
  - Meta/Harness: `.grok/` + `.trae/` agents (bottleneck-analyzer, business-orchestrator, causal-improvement, conformance, evaluation-harness, evolution-manager, governance-officer, knowledge-curator/distiller, memory-steward, process-miner, security-red-team, task-mining, tool-permission-broker), commands, skills, rules.
  - Planning/SDD: Extensive `planning/` (structure/backend/frontend SDD with design/requirements/tasks per layer), gap analyses, traceability matrices.
  - Business Layer: `business/` with schemas (WorkflowDNA, EvaluationCard, DecisionRequirementCard, EventLog), evals (20+ golden tasks for customer-onboarding + regression/adversarial/human-review), governance (risk tiers, approval policy, model cards, assurance cases), process-intelligence (bottlenecks, causal hypotheses, conformance, event logs), security (incident reports, prompt-injection tests, red-team, threat models, tool permissions), examples/fixtures.
  - Product Bar: `status.md`, `mark_100_verification.md`, `structure_scorecard_100.md`, E1 operator checklist + e2e test green.
  - Other: Full OpenAPI, tests (unit/integration/e2e/load/security), scripts for scaffold/sync/doctor/eval-harness, book/ docs with SVGs.

- **Critical Gaps (Blocking Universal Platform + va Adoption):**
  - No `business/video/` directory or Domain Pack skeleton.
  - No formal Domain Pack SDK (`domain-manifest.schema.json`, `agent-spec.schema.json`, `learning-log.schema.json`, registration API/hooks, manifest loader).
  - ALC incomplete: Lessons tied to `workflow_id` only; `reflect_on_workflow_run` writes `agent=None`; no per-agent episodic write/reflect/retrieve/pre-act inject; no `agent_id` on lessons or activation gates.
  - Domain layer stubs: Most `backend/app/domain/*/models.py`, `policies.py`, `runtime.py` etc. are 31-byte placeholders.
  - No video-specific anything: No 114-agent roster import, no orchestration spine mapping, no media adapters (Sora/Veo/etc.), no LQR/archetype processes as DNA.
  - Missing inventory/CI gates for roster completeness and ALC enforcement.
  - FE lacks domain pack routes or full-roster management views.
  - Self-improvement is workflow-centric; agent genomes + coevolution not yet implemented.
  - Multi-pack isolation and second-pack proof missing.

- **Repo Structure Highlights (1297+ items):**
  - `backend/app/domain/agents/`, `approvals/`, `audit/`, `evaluations/`, `governance/`, `knowledge/`, `memory/`, `processes/`, `workflows/` — mostly stubs.
  - `business/adapters/`, `distilled/`, `evals/`, `evolution/`, `examples/`, `experts/`, `fixtures/`, `governance/`, `knowledge-base/`, `materials/`, `policies/`, `process-intelligence/`, `reports/`, `schemas/`, `security/`.
  - `frontend/src/app/app/[...slug]/page.tsx` (large dynamic shell), domain components (approval, evolution, improve, run console, etc.).
  - `planning/` with 20+ detailed SDD folders (structure/backend/frontend) containing design.md/requirements.md/tasks.md per sub-layer.
  - `.grok/agents/` + `.trae/agents/` (18+ meta-agents), commands, skills, rules.
  - Full test suites, OpenAPI, pnpm frontend, pyproject backend.

### 2.2 Key Insights from repo_compare.md (2026-07-11)
- **Complementary Strengths:** generic = production runtime/governance/evolution/FE (9/10 overall). va = unmatched video domain research/spec depth (114 agents, 66-chapter corpus, deep specs for aesthetics/psych/intent/RAG/loop/planner, UI concepts, workflows).
- **Gaps in generic:** Missing full roster, video processes, per-agent learning (ALC), video tools, dedicated domain UI, formal multi-domain extensibility.
- **Gaps in va:** Zero runtime/backend/FE/governance/evolution (spec-only).
- **Recommendation:** generic = host/platform. va = complete Domain Pack imported into `business/video/` (full roster + full processes, retained forever). No second platform (LangGraph/Temporal duplicate forbidden). Map va concepts onto generic primitives (DNA steps, ALC reflect, evaluation steps, provenance).

### 2.3 Key Strategy from adoption.md v2.3
- **Rethink:** L0 Catalog (dirs + roster + MAP + minimal agent_spec) → L1 Process-indexed → L2 Runtime (ALC-enforced, active). Catalog complete early; deep SPEC filled on activation. Spine first for E2E proof; full roster never dropped.
- **Target Architecture:**
  - `business/<domain_id>/manifest.json` + agents/ + workflows/ + tools/ + evals/ + knowledge/ + policies/ + ui/.
  - ALC mandatory for packs with `requires_alc: true` (episodic write with `agent_id`, reflect tagged, pre-act retrieve, sandbox proposals, provenance, metrics).
  - Agent genome (prompts/rubrics/tool prefs) coevolves with Workflow DNA.
  - Orchestration patterns as configurable DNA metadata (hierarchical, pipeline + gates, router, critique bus as eval steps).
  - Video logic 100% in pack; generic core untouched.
- **Phased Waves:** 0 (inventory/skeletons) → 1 (Domain Pack SDK + ALC) → 2 (catalog + spine E2E) → 3 (learning/coevolution) → 4 (multi-pack proof) → 5 (full roster + full processes wired, N3 complete).
- **Retention & Integrity:** Every agent in `business/video/agents/<pack_id>/` forever. Orchestrator-down hierarchy. Inventory CI fails on missing agents or incomplete MAP. No orphan agents.

### 2.4 User's Explicit Concern (from conversation)
"After applying these improvements on generic-swarm-ops, will it benefit to another project not only to va-agent-swarm? Or it will have business specific logic / info/ memory after improvement in generic-swarm-ops?"

**Answer (embedded in plan):** 
- **Benefits other projects massively** — generic becomes the reusable host. New domains (your DSE ICT tutoring, YouTube ASMR/educational agents, trading/Polymarket automation, creative wuxia/anime pipelines, ESP32 hardware agents, legacy modernization harnesses, business automation) plug in via the Domain Pack contract and inherit ALC, evolution, governance, real-time ops, self-improvement, multi-tenant, etc.
- **Zero pollution** — Strict separation enforced by architecture (manifest registration, namespace isolation, scoped memory, pack-only paths). Video-specific roster/processes/knowledge/rubrics stay in `business/video/`. Core runtime/schemas/governance/evolution/FE remain domain-agnostic. ALC is a generic platform capability.

This plan makes the improvements **executable by coding agents** while preserving (and enhancing) all existing production strengths.

---

## 3. Improvement Goals, Non-Negotiables & Success Metrics

### 3.1 Primary Goals
1. Implement full **Domain Pack architecture** so generic is the universal host for any MMA system (N2).
2. Implement complete **Agent Learning Contract (ALC)** platform-wide so every agent (any pack) autonomously learns (N1).
3. Enable clean, complete import of va-agent-swarm as the first rich **Video Domain Pack** (full 114 agents + full processes, retained forever) without touching generic core (N3).
4. Add supporting infrastructure (schemas, registration, inventory CI, FE extensions, media adapter pattern, agent genomes + coevolution) while protecting E1/mark~100 and sandbox discipline.
5. Provide clear reuse playbook + second example pack proof so other projects (tutoring, trading, content, etc.) benefit immediately.
6. Keep all changes spec-driven, testable, documented, and production-grade.

### 3.2 Non-Negotiables (Enforced in Every Wave)
- **N1 (Video Logic Isolation):** All VA/video business logic, agents, processes, knowledge, rubrics stay exclusively in `business/video/`. Never hard-code in core runtime/schemas/governance.
- **N2 (Universality):** Domain Pack contract + ALC + isolation work for video **and** at least one second pack (`business/example_research` or equivalent) before Phase 4 exit. New packs require zero changes to host runtime.
- **N3 (Full va Adoption + Retention):** All 114 agents (Appendix A in adoption.md) + all processes (orchestration spine, A–J archetypes, LQR, 6-phase E2E, support) present in `business/video/` with MAP 1:1, placeholder dirs, minimal agent_spec + ALC fields. **No agent omitted or deleted.** Inventory CI enforces. va repo = upstream only.
- **Platform Safety:** `sandbox_only` evolution never bypassed. Human gates for irreversible actions. E1 operator path + mark~100 regression suite green on every PR. No production self-modification of host code.
- **ALC Enforcement:** Activation to `active`/`production_ready` denied unless ALC bindings present (episodic write, reflect hook, allowed_memory_scopes includes "agent", provenance).
- **Traceability & Docs:** Every change references `adoption.md` §X or `repo_compare.md` area. Update `structure.md`/`backend.md`/`frontend.md`/`docs/domain-packs.md` + handoff notes.
- **Testing:** Unit + integration + domain evals + e2e (video spine + second pack) + load/isolation. Business eval harness green.

### 3.3 Success Metrics (Measurable DoD)
**Platform (N1/N2):**
- Domain register CLI/API + manifest validation works for video + example pack.
- ALC: Lessons written with `agent_id`; pre-step retrieve injects agent lessons; activation gate blocks without ALC; metrics endpoint shows growth/reuse.
- Second pack registers/runs in isolation (no memory bleed).
- E1 + unit + business:eval green; no regression on mark~100 paths.

**Video Pack (N3):**
- `business/video/agents/` contains exactly 114 dirs matching Appendix A + MAP.md with 1:1 rows.
- All 10 categories + meta spine (#53–#56) present.
- At least one orchestrator-down DNA family (viral-hook archetype or Phase 1–2) runs E2E with human gate + ALC reflects.
- Process index (`PROCESSES.md`) covers full va business processes.
- Inventory CI passes (count == 114, no missing pack_id).
- All agents orchestrator-reachable (DNA step or standby_pool).

**Other Projects / Reuse:**
- `docs/domain-packs.md` + reuse playbook published.
- Example pack (`business/example_research` or podcast lite) fully functional as proof.
- Clear onboarding: <1 day for new domain skeleton → registered + learning.

**Long-term:** Platform semver independent of pack semver. Contribution workflow (va for specs → generic pack PRs). Version compatibility matrix.

---

## 4. Detailed Phased Improvement Roadmap (Waves 0–5 + Ongoing)

Aligned to adoption.md Phases but expanded with file-level tasks, coding-agent-ready specs, tests, and traceability. Each Wave has **P0 (must)** / **P1 (should)** / **P2 (nice)** prioritization.

**Overall Timeline (indicative, parallelizable where safe):** 10–16 weeks for full platform + N3 video spine + second pack proof. Full roster activation can wave-rollout post-spine.

### Wave 0: Foundations — Inventory, Skeletons, Schemas, CI Gates (1–2 weeks, P0)
**Goal:** Complete catalog of va assets; create pack homes + minimal specs; add Domain Pack schemas + basic inventory CI. No runtime changes yet. Protect existing E1.

**Non-Negotiables:** Full roster + process index exported. Placeholder dirs for all 114 agents. Schemas added. CI gate skeleton. No agent dropped.

**Detailed Tasks (send to coding agent as task.md sections):**

1. **Export & Document va Assets (both repos, but canonical in generic)**
   - Parse `va-agent-swarm/study/agents.md` + `SYSTEM_REFERENCE.md` → produce `business/video/ROSTER.json` and `business/video/MAP.md` (1:1 rows for all 114, stable pack_id like `video.director`, `video.orchestrator`, etc. — match Appendix A in adoption.md).
   - Export full process index (orchestration spine, 6-phase E2E, A–J archetypes, LQR family, human→AI maps, support processes) → `business/video/PROCESSES.md`.
   - Create `business/video/README.md` with ownership note (N3 retention policy) + link to adoption.md §5.0.
   - **Acceptance:** `count(business/video/agents/*)` will eventually == 114; MAP rows == 114; no "later/P0-only" omissions. CI will enforce.

2. **Create business/video/ Skeleton + Placeholder Dirs (generic only)**
   - `mkdir -p business/video/{agents,workflows,tools,evals/golden,evals/regression,evals/adversarial,knowledge/seeds,policies,ui}`
   - For every pack_id in ROSTER/MAP: `mkdir business/video/agents/<pack_id>/` + stub `agent_spec.json` (id, domain_id:"video", role, requires_alc:true, allowed_memory_scopes:["agent"], alc_version, risk_tier, critique_rubric_ref, provenance) + `SPEC.md` placeholder (link to va source).
   - Add `.gitkeep` + minimal `prompts/` and `rubrics/` subdirs where deep specs exist in va.
   - **Acceptance:** 114 agent folders exist with minimal agent_spec.json containing ALC fields. No deletions allowed in future PRs.

3. **Add Domain Pack Schemas (generic, business/schemas/)**
   - Create `business/schemas/domain-manifest.schema.json` (fields: domain_id, version, display_name, default_risk_tier, requires_alc, agents[], workflows[], knowledge_seed_globs[], api_hooks{on_register, tool_namespace}).
   - Create `business/schemas/agent-spec.schema.json` (id, domain_id, role, tools[], allowed_memory_scopes[], alc{version, episodic_write, reflect_hook, pre_act_retrieve}, risk_tier, critique_rubric_ref, provenance, status).
   - Create `business/schemas/learning-log.schema.json` (agent_id, run_id, step_id, lesson_text, utility_score, reuse_count, source_refs[], captured_by, recorded_at).
   - Update existing `business/schemas/` index or common.py if needed.
   - Add JSON Schema validation helpers (reuse existing validator pattern).
   - **Acceptance:** `validate(domain-manifest)` and `validate(agent-spec)` pass on examples. Schemas referenced in adoption.md §3.1 / §4.1.

4. **Inventory CI Gate + Basic Domain Register Stub (generic)**
   - Add script or pytest in `scripts/business/` or `backend/app/tests/` : `inventory_check.py` or `test_domain_pack_inventory.py` that fails if `business/video/agents/` count != 114 or MAP incomplete or any roster agent lacks dir + minimal agent_spec.
   - Stub `POST /api/v1/domains/register` (or CLI `npm run domain:register` / python script) that validates manifest against schema and loads into draft catalog (org-scoped). Return draft status.
   - Add to default CI pipeline (`.github/workflows/` or existing test script).
   - **Acceptance:** CI fails on incomplete video pack inventory. Register stub accepts valid manifest for `example_domain` and `video`.

5. **Docs & Traceability Updates**
   - Create `docs/domain-packs.md` (high-level contract, manifest example, registration flow, isolation rules, reuse playbook).
   - Update `structure.md`, `backend.md`, `frontend.md` with "Domain Pack Extension Layer" section + links to adoption.md.
   - Update `adoption.md` changelog + cross-reference this `improvements.md`.
   - Add note in `status.md` / handoff about Wave 0 completion.
   - **Acceptance:** All docs reference adoption.md N1/N2/N3 and repo_compare gaps.

**Wave 0 Exit Criteria:** Full va roster + process index in generic `business/video/`. 114 placeholder agent dirs with minimal ALC-flagged specs. Schemas committed. Inventory CI gate exists and would pass on complete pack. E1 still green. Second skeleton `business/example_research/` optional but recommended for N2 proof later.

**Coding Agent Prompt Template for Wave 0:**
"Implement Wave 0 of improvements.md exactly. Focus on P0 tasks 1-5. Use existing patterns from business/schemas/, scripts/business/, backend/app/tests/. Do not modify runtime.py or core APIs yet. Create all files with proper headers, provenance notes linking to va sources and adoption.md §X. Run inventory check at end and confirm it would pass on complete roster. Update relevant docs. Output task completion report with file diffs and acceptance evidence."

### Wave 1: Domain Pack SDK + Full ALC Implementation (2–3 weeks, P0)
**Goal:** Make generic a true extensible host. ALC works platform-wide. Domain registration functional. Agent-scoped learning enforced. Second example pack proves N2.

**Non-Negotiables:** ALC gate blocks activation without bindings. Lessons carry `agent_id`. Pre-step memory inject works. Register API functional. Isolation tested. E1 protected.

**Detailed Tasks:**

1. **Runtime ALC Wiring (backend/app/)**
   - Extend `runtime.reflect_on_workflow_run` (or new `reflect_on_agent(agent_id, run_id, step_id)`) to write lessons with `agent_id`, step context, outcome, critique. Store in agent-scoped memory collection or `agent_episodes`.
   - Add pre-step hook in workflow step executor: retrieve top-k agent lessons + scoped memory before LLM/tool call; inject into prompt/context.
   - Add `POST /api/v1/improvement/reflect/agent/{agent_id}` route + service.
   - Metrics: `GET /api/v1/improvement/metrics?agent_id=...` (knowledge_growth_count, lesson_reuse_rate, human_gate_rate_delta).
   - **Files:** `backend/app/runtime.py`, `backend/app/api/v1/routes/improvement.py`, `backend/app/infrastructure/self_improvement/lessons.py` + reflection.py, `backend/app/infrastructure/memory/`.
   - **Acceptance:** Unit test: lesson persisted with correct `agent_id`; wrong agent cannot read another's private episodes; pre-step inject called.

2. **ALC Activation Gate + Status (backend/app/domain/agents/ + governance)**
   - Implement activation rule: If `requires_alc` and `domain.requires_alc`, deny `active`/`production_ready` unless `alc_version >= current`, `allowed_memory_scopes` includes "agent", `hooks.reflect == true`.
   - Add to `structure_validators.py` or new `alc_validator`.
   - Update agent status enum/model to include ALC readiness.
   - **Files:** `backend/app/domain/agents/`, `backend/app/infrastructure/governance/`, `backend/app/api/v1/routes/agents.py`.
   - **Acceptance:** Activate attempt without ALC fields fails with clear error. Spine agents can activate after ALC setup.

3. **Domain Pack Registration & Loading (backend + scripts)**
   - Full `POST /api/v1/domains/register` (validate manifest schema, create org/domain catalog entries, load agents/workflows as draft/registered with ALC fields from agent_spec).
   - CLI or `scripts/business/register_domain.mjs` (or Python equiv) for local/dev.
   - Tool namespace registration (`video.*` → allow-list in permission broker).
   - Eval pack auto-discovery (golden/regression/adversarial under pack evals/ loaded into harness).
   - **Files:** New or extend `backend/app/api/v1/routes/domains.py` (or reuse organizations/agents patterns), `backend/app/services/`, `scripts/business/`.
   - **Acceptance:** Register valid `video` manifest (even with stubs) succeeds; agents appear in catalog with correct ALC flags. Invalid manifest fails closed.

4. **Agent Genome + Coevolution Sandbox (evolution + infrastructure)**
   - Add evolution variant type `agent_genome` (prompts, rubrics, tool prefs, retrieval policy, critique weights).
   - `sandbox_only` propose path for genomes linked to agent_id.
   - Fitness function extension: include lesson reuse + knowledge growth (formula in adoption.md §4.3).
   - Coevolution experiment scaffold (planner genome × aesthetics genome evaluated on shared golden).
   - **Files:** `backend/app/infrastructure/evolution/`, `backend/app/api/v1/routes/evolution.py`, `backend/app/infrastructure/self_improvement/`.
   - **Acceptance:** Genome proposal created as sandbox_only; promote blocked if not gated; metrics include L_reuse / G_growth.

5. **Second Example Pack Proof + Isolation Tests**
   - Create minimal `business/example_research/` (manifest, 3–5 agents with ALC, 1 simple workflow DNA, 1 golden eval).
   - Integration tests: concurrent runs across video + example packs; memory isolation (video agent query returns empty for research agent_id); no cross-pack bleed.
   - **Files:** `business/example_research/`, `backend/app/tests/integration/test_domain_pack_isolation.py`, `backend/app/tests/`.
   - **Acceptance:** Second pack registers, runs E2E, learns lessons independently. Isolation tests pass.

6. **FE Domain Shell + Basic Roster View (frontend)**
   - Add domain-aware routes or components: list/filter agents by domain/pack (draft/active), show ALC status, basic pack dashboard placeholder.
   - Reuse existing domain components (agent table, evolution archive, improve button).
   - **Files:** `frontend/src/components/domain/`, `frontend/src/app/app/[...slug]/`, `frontend/src/lib/routes/`.
   - **Acceptance:** Ops console shows video pack agents (even stubs) + ALC status. No breakage to existing ops flows.

**Wave 1 Exit Criteria:** ALC fully wired and gated. Domain register functional for video + example pack. Second pack proves isolation + learning. E1 + new ALC/domain tests green. `docs/domain-packs.md` published.

**Coding Agent Prompt for Wave 1:**
"Implement Wave 1 of improvements.md P0 tasks. Extend existing patterns in runtime.py, self_improvement/, governance/, improvement routes. Add ALC fields to lessons and activation checks. Implement register endpoint + CLI stub. Create example_research pack skeleton. Write unit/integration tests for ALC gate, memory isolation, pre-step inject. Update docs. Protect all existing E1 paths. Provide evidence that activation without ALC is denied and that example pack learns independently."

### Wave 2: Video Pack Catalog Complete + Spine E2E (3–5 weeks, P0 for N3)
**Goal:** Full 114-agent catalog + minimal specs in-repo. Orchestration spine + first vertical (viral-hook or Phase 1–2) runnable E2E with human gate + ALC reflects. Process index complete. Media tool stubs.

**Non-Negotiables:** All 114 agents present (L0). Spine agents ALC-active and runnable. Orchestrator-down integrity. Inventory CI passes. No orphan agents.

**Detailed Tasks (high-level; expand per adoption.md §5.1–5.4):**

1. **Complete Agent Import (all categories)**
   - Flesh `business/video/agents/<pack_id>/` for all 114: full agent_spec.json from va deep specs where available; SPEC.md with provenance link to va `study/`.
   - Prioritize spine first (#53 Orchestrator, #54 Planner, #55 Router, #56 Judge, producer, intent/DIA, director, screenwriter, research, aesthetics).
   - Add standby_pool / router tables so every agent is invocable from orchestrator.
   - **Acceptance:** Inventory CI green (exactly 114, MAP 100%, every pack_id has dir + spec with ALC fields).

2. **Workflow DNA for Spine + First Archetype**
   - Map va orchestration spine + viral-hook archetype (or Phase 1–2 Intent&Planning → Creative) to `business/video/workflows/wf_video_spine_v1.dna.json` and `wf_video_arch_a_viral_hook_v1.dna.json`.
   - Use existing WorkflowDNA schema (inputs, steps with agent/tool refs, guardrails, verification, rollback, fitness).
   - Wire handoffs: orchestrator → planner/intent → director/screenwriter/research → media_stub → QC → human_gate.
   - **Files:** `business/video/workflows/`, `backend/app/domain/workflows/`.
   - **Acceptance:** DNA validator passes. Can queue/run spine DNA (stubs OK for media).

3. **Tool Adapter Stubs + Namespace (infrastructure/tools + pack)**
   - Add video.* media gen stubs (Sora/Veo/Kling/ElevenLabs/script format) in `backend/app/infrastructure/tools/adapters.py` pattern.
   - Register under `video.*` in tool-permission-register + pack tools/adapters.md.
   - Rate-limit/budget stubs for CI.
   - **Acceptance:** Spine DNA can invoke video.* stubs; permission broker allows only declared namespace.

4. **Golden Evals + Human Gate for Spine**
   - Port va rubrics (aesthetics, consistency, psychological alignment) into `business/video/evals/golden/` + EvaluationCards.
   - Add human gate step in spine DNA for irreversible actions (e.g., external publish).
   - **Acceptance:** `business:eval` harness green for spine golden tasks. Human gate triggers correctly.

5. **E2E Spine Run + ALC Proof**
   - End-to-end: login → queue viral-hook/spine DNA → running → waiting_for_approval (human gate) → succeeded → auto-reflect → agent lessons populated → sandbox propose visible in evolution archive.
   - FE: domain page shows roster + run progress.
   - **Acceptance:** Full E2E passes like E1 but for video spine. ALC lessons created with correct agent_ids. Metrics show growth.

6. **Knowledge Seeding (initial)**
   - Curate top va reference chapters + deep specs into `business/video/knowledge/seeds/` with provenance.
   - Index via generic Tier-0/K1. Agents retrieve with acting_agent_id scope.
   - **Acceptance:** Spine agents can retrieve relevant seeds pre-act.

**Wave 2 Exit Criteria:** Full catalog (L0 complete, inventory CI green). Spine E2E runnable with human gate + ALC reflects. First archetype DNA wired. Media stubs + permission namespace working. Process index covers spine + archetype A. E1 still green.

**Coding Agent Prompt for Wave 2:**
"Implement Wave 2 focusing on full catalog import (all 114 per Appendix A), spine + viral-hook DNA authoring, tool stubs, golden evals with va rubrics, and full E2E spine run. Use existing DNA schema and adapter patterns. Ensure orchestrator-down integrity and that every roster agent is reachable. Write e2e test mirroring test_e1_operator_path.py but for video spine. Confirm inventory CI passes and ALC lessons are agent-scoped. Update FE roster view minimally."

### Wave 3: Learning, Coevolution & Quality on Video Tasks (2–3 weeks)
**Goal:** Measurable autonomous improvement on video tasks via ALC + genomes. Multi-generation sandbox experiments. Lesson utility scoring.

**Tasks (summarized):**
- Multi-generation sandbox on video goldens (planner genome × aesthetics genome).
- Lesson utility scoring + reuse metrics dashboard.
- Skill sandbox for video prompt skills.
- Governance review of learned artifacts.
- Expand evals with LQR/consistency rubrics.
- **Acceptance:** Measurable improvement on ≥1 fitness metric (quality + growth/reuse) without production regression. All variants audit-logged. Coevolution experiment runs.

### Wave 4: Multi-Pack Proof, Load, Security Hardening (2–3 weeks)
**Goal:** Prove N2 at scale. Isolation, concurrency, security for multiple packs.

**Tasks:**
- Load tests: 20+ concurrent mixed-domain runs.
- Security: red-team video tool misuse + prompt injection (must not expand allow-list).
- Cross-pack isolation expanded.
- Docs kit: "Add a Domain Pack" runbook + versioning matrix.
- Optional: podcast or education lite pack as third example.
- **Acceptance:** Isolation/load/security tests pass. Runbook published. Platform handles mixed domains cleanly.

### Wave 5: Full Roster Activation + Full Process Wiring (N3 Completion, 8–16+ weeks, phased)
**Goal:** Activate remaining agents category-by-category. Wire all va processes (A–J, LQR, delivery, support) to real agent ids. Standby pool complete. No orphans. Full N3.

**Tasks (per adoption.md §5.1 Waves 2–6 + Phase 5):**
- Activate cats 2–10 progressively with ALC.
- Author remaining DNA families (full 6-phase E2E, all archetypes, LQR, delivery fabric).
- Standby_pool + router tables complete.
- Full-roster inventory CI in default pipeline (fail build on missing agent).
- Optional other domains only **after** video N3 complete.
- **Acceptance (mandatory for N3):** All 114 agents active or registered+orchestrator-reachable. All va business processes represented as DNA or linked pack docs. No process left va-only. Retention policy enforced forever. Inventory CI 100%.

**Ongoing / Post-Wave 5:**
- Media provider integrations (real adapters with budgets/rate limits) — after stubs.
- Advanced FE (timeline editor, pipeline viz) — P2, do not block N3.
- External stack adapters (Temporal optional) — later.
- Continuous: va upstream updates → pack PRs with provenance. Platform RFC process for shared schemas.

---

## 5. Final Suggestions & How to Execute with Coding Agents

### 5.1 Prioritized P0 Backlog (First 30 Days Focus)
1. Wave 0 full (inventory, skeletons, schemas, CI gate) — **start immediately**.
2. Wave 1 ALC core + register + example pack proof.
3. Wave 2 catalog complete + spine E2E (highest N3 value).
4. Docs + traceability updates in parallel.
5. Protect E1 on every PR via existing regression suite.

### 5.2 How to Send to Coding Agent (Recommended Workflow)
Use your existing harness (N1ch01as Architect style: spec-driven task.md, critic loops, quality gates, iterative 10/100 rethink).

**Example Prompt for Coding Agent (Claude/Kiro/Cursor):**
```
You are a senior production AI coding agent working on generic-swarm-ops.

Task: Implement Wave X (or specific tasks 1–N) from /improvements.md exactly as specified.

Context (must internalize):
- Background: repo_compare.md analysis + adoption.md v2.3 (N1/N2/N3, Domain Pack, ALC, L0/L1/L2, full roster retention).
- Current state: production platform with many domain stubs; no business/video/ yet; ALC partial.
- Non-negotiables: No business-specific logic in core. All video in business/video/. Sandbox discipline. E1/mark~100 protected. Full 114 agents retained.
- Patterns: Reuse existing WorkflowDNA, adapters.py, self_improvement/, governance/, runtime.py, FE domain components, business/schemas/, test structure.
- Output requirements: Clean code, full tests (unit + relevant integration/e2e), docs updates with traceability to adoption.md §X and repo_compare areas, provenance notes, acceptance evidence at end.

Constraints:
- Work in sandbox where possible; propose via evolution for risky changes.
- Run relevant tests before claiming done.
- If ambiguity, ask or choose the production-safe path that enables future packs.

Deliver: Completed files + test results + short report referencing improvements.md tasks.
```

**Iterative Loop (your preferred style):**
1. Agent implements Wave slice → runs tests → produces report.
2. You (or critic agent) review against non-negotiables + E1.
3. If gaps: "Rethink 10x: improve X per improvements.md §Y. Add critic for ALC edge cases."
4. Promote only after human gate + sandbox canary.
5. Update `adoption.md` / `improvements.md` changelog + status.

**For Self-Refining Harness:** Feed entire `improvements.md` + `adoption.md` + `repo_compare.md` as context corpus. Use memory-steward + evolution-manager agents to maintain task backlog and auto-propose refinements.

### 5.3 Risk Mitigation (from adoption.md §8, reinforced)
- Dual platform rewrite → Explicit ban + ADR.
- Scope explosion → Import full catalog Wave 0; activate in waves; forbid dropping agents.
- Learning pollution → Agent scopes + isolation tests (Wave 1+).
- E1 regression → Mandatory regression suite on every PR.
- Orphan agents → standby_pool + router + CI check.
- Media cost → Stubs in CI; budget gates later.

### 5.4 Long-Term Value for Your Other Projects
Once complete:
- Your DSE ICT tutoring (DeepTutor xAI Edition) → `business/education/` or `business/hkdse/` pack.
- YouTube content / Cantonese ASMR/sleep agents → `business/content/` or `business/video` extension.
- Trading/Polymarket/SMA automation → `business/trading/` pack with prediction market tools.
- ESP32 hardware AI avatar → `business/hardware/` or embedded pack.
- Legacy modernization harnesses → `business/enterprise/` ops pack.
- All inherit ALC autonomous learning, evolution, governance, real-time ops, multi-tenant, self-improvement — without rebuilding the wheel.

This plan turns generic-swarm-ops into your central "N1ch01as Architect" platform while delivering the full video swarm as the flagship Domain Pack.

---

## 6. Appendix

### References
- `repo_compare.md` — Full comparison table, gaps, merge recommendation.
- `adoption.md` v2.3 — Authoritative N1/N2/N3, target architecture, phased roadmap, full 114 roster (Appendix A), process map.
- `structure.md` / `backend.md` / `frontend.md` (+ _hk) — Current architecture.
- `planning/gap_analysis_for_*.md` + SDD tasks — Existing detailed specs.
- `business/schemas/` + `backend/app/tests/e2e/test_e1_operator_path.py` — Patterns to extend.
- `va-agent-swarm/study/agents.md` + `SYSTEM_REFERENCE.md` — Source of truth for roster/processes (import with provenance).

### Key Files to Touch (Summary)
- New/Extend: `business/video/**`, `business/schemas/{domain-manifest,agent-spec,learning-log}.schema.json`, `business/example_research/**`, `docs/domain-packs.md`.
- Core: `backend/app/runtime.py`, `backend/app/infrastructure/self_improvement/*`, `backend/app/api/v1/routes/{improvement,agents,domains,evolution}`, `backend/app/infrastructure/governance/`, `backend/app/infrastructure/tools/adapters.py`, `frontend/src/components/domain/*`.
- CI/Docs: `scripts/business/`, test files, `structure.md`/`backend.md`/`frontend.md`, `adoption.md` changelog, `status.md`.

**End of improvements.md v1.0**

*This document is designed to be fed directly to coding agents. It is traceable, phased, non-negotiable-enforcing, and production-first. Execute Wave 0 immediately to unblock everything else.*