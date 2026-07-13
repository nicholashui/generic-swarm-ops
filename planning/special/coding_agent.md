# Special skill adoption plan — `coding_agent`

| Field | Value |
|-------|-------|
| **Skill id** | `coding_agent` |
| **Source** | `C:/Project/va-agent-swarm/study/coding_agent_functional_specification.md` |
| **In-pack corpus mirror** | `business/video/corpus/study/coding_agent_functional_specification.md` (if present under video corpus) |
| **Source size** | 948 lines / 96,965 chars / ~32 table rows detected |
| **Host product** | generic-swarm-ops |
| **Plan type** | Spec-driven development (SDD) learning + adoption execution |
| **Generated** | 2026-07-13 |
| **Generator** | `scripts/business/generate_special_skills_plans.py` via `generate_special_skills.md` |

## Host integration stance (N1/N2/N3)

Host engineering capability — prefer skills/hooks; keep out of video business logic (N1).

| Kind | Guidance |
|------|----------|
| **Domain Pack agents** | Prefer existing `video.*` agents below; create new pack agent only if roster gap is real |
| **Workflow DNA** | Extend/index DNA under `business/video/workflows/`; entry via `video.orchestrator` / `video.planner` |
| **Host core** | Reuse runtime, ALC, knowledge, LLM adapters — do not rebuild a second control plane |
| **Selection** | When production-type relevant, use `business/video/archetype_registry.json` + recommend-workflow API |

**Candidate pack agents:**
_None specified in automated extract._

**Candidate DNA:**
_None specified in automated extract._

**Candidate runtime tools (allow-listed / stubs):**
- audit_log_writer

---

## 1. Source Document Review & Requirement Extraction

### 1.1 Source outline (headings extracted)

**H2 sections:**
- 1. Project Structure (must be created exactly – agent-first and legible)
- 2. Persistent Identity & Research Constitution (OpenClaw + Karpathy + Harness + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- 3. Agent Roles (all internal to single Orchestrator thread – Harness-Engineered + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- 4. Full Phase-by-Phase Flow (Harness-Engineered + Ratchet + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness – must be implemented exactly)
- 5. Quality Gates & Invariants (Mechanical Enforcement – Harness Core + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- 6. Master Orchestrator Prompt v1.0 (must be used verbatim as entry point after YES, START)
- 7. Non-Functional Requirements (Harness-Enforced, Local-First + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- 8. Extra Power-Ups (Highly Recommended)
- 9. How to Start Right Now
- 1. Executive Recommendation
- 2. Specific, Actionable Upgrades (All Mandatory for v1.1, Python-Only)
- 3. Updated Phase 0.5 Additions (Exact Python-Only Files/Folders)
- 4. New Invariants to Add to Section 5 (Quality Gates)
- 5. Expected Outcomes After Python-Only Integration
- 6. Implementation Priority Order (Python-Only)

**Selected H3 sections:**
- AGENTS.md (must be written verbatim – progressive disclosure map + Hermes hierarchy + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- ORCHESTRATOR_SOUL.md (exact content – must be written verbatim)
- ORCHESTRATOR_DIRECTIVE.md (exact content – must be written verbatim)
- Research Swarm – 10 Specialist Types (Orchestrator routes dynamically)
- 3.1 Standardized Task Brief Template (must be embedded verbatim and used every time the Orchestrator delegates code work)
- 3.2 Pre-Dispatch Improvement Review Block (must run before every Coding Agent dispatch)
- Phase 0: Guided Requirement Discovery (Intent Analyst leads)
- Phase 0.5: Harness Initialization (Orchestrator takes over completely – Local-First + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- Phase 1: Backend Specification (Smart Swarm + Validator + Critic Ratchet Loop + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- Phase 2: Backend Implementation (TDD + Code Critic + Feature Branches + Ratchet + Harness + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- Phase 3: Frontend Specification & Implementation (IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness continues)
- Phase 4: Integration, Polish & Delivery (Full Autonomy + Final Hermes + Final Lightning Optimization + Final Core Skills Evolution + Final Meta-Harness)
- 7.0 Mandated Tech Stack (Open-Source, Local-First)
- 2.1 Skills System – Python Claw Code Parity (Highest ROI)
- 2.2 Tool Registry + Hook Pipeline (Safety & Observability Moat)

### 1.2 Functional requirements (extracted / paraphrased from source language)

The following items were mined via keyword heuristics (must/shall/metric/workflow/gate/…) and structural scan. Treat them as a **backlog seed** — refine against full line-by-line human review of the source.

- Purpose:** This is the **SINGLE SOURCE OF TRUTH** document that any coding agent (or human developer) must follow to implement the complete, production-grade, no-code "N1ch01as Architect" tool.
- The N1ch01as Architect itself is an **AGI-like thinking agent** that uses:
- Embedded Standardized Task Brief Template:** The exact template the Orchestrator must use every time it delegates code work. This ensures consistent, professional, controlled delegation with zero ambiguity. Includes the 4-step Delegation Loop (brief → code → review → decide).
- Superpowers** (process constraint by obra) — strict TDD discipline: no product code without failing test first. Enforces: ask requirements → brainstorm → plan → write tests → implement → review → iterate. Highest one-pass quality.
- These three skills are complementary, non-conflicting, and will be automatically referenced, used, and evolved by the Skill Creator Agent in every relevant phase. They can be combined (e.g., Planning uses Superpowers + gstack, Execution uses GSD).
- Core Philosophy (must be enforced everywhere):**
- The Orchestrator delegates to and controls the Coding Agent like a senior IT professional managing a dev team, always using the Standardized Task Brief Template.
- Relentless self-improvement: every loop must ratchet quality upward (never sideways or downward).
- Users usually have vague ideas — the system must proactively clarify, critique, and professionalize them via Guided Discovery.
- Closed Learning Loop: after every complex task, autonomously create/improve skills, issue memory nudges, and update persistent memory & user profile.
- Agent Lightning: trace every action with spans, run Trainer/Optimizer after every phase for continuous selective self-optimization.
- This document is **completely standalone**. All agent prompts, rubrics, identity files, templates, and implementation details are fully inlined below.
- Clear agent roles** (Orchestrator handles all switching in a single thread — you never copy-paste new prompts).
- IT Professional Delegation** — Orchestrator acts as Senior IT PM/Architect, instructs Coding Agent with the Standardized Task Brief Template, reviews output, enforces quality.
- Quality gates** (score + tests + invariants pass) instead of blind "repeat 5 times" — now raised to ≥ 9.8/10 with weighted rubric + ratchet rule + evaluation harnesses.
- API-first** (OpenAPI spec becomes the contract between backend & frontend).
- Folder structure** for maintainability and agent legibility.
- Built-in synchronization** (Sync Agent keeps specs = code at all times).
- Validator Agent** — mental dry-run catches logical gaps before coding starts.
- Ratchet Rule** — never keep a change that does not strictly improve the sacred metric.
- Harness Engineering** — mechanical invariants, evaluation harnesses, progressive disclosure, agent legibility.
- % Agent-Generated** — every file (code, tests, linters, CI, docs) created by agents.
- Hermes Closed Learning Loop** — autonomous skill creation/improvement, persistent memory with nudges, deepening user profile, sub-agent spawning.
- Agent Lightning** — span-based tracing, LightningStore, Trainer/Optimizer loop for continuous selective self-optimization.
- ├── initial_idea.md                   # Raw user input (vague by design) – archived after discovery

### 1.3 Non-functional constraints (host-normalized)

| Area | Constraint for adoption |
|------|-------------------------|
| **Isolation** | Video/business logic stays under `business/video/**` (N1) |
| **ALC** | Any new/updated agent: `requires_alc`, memory scope includes `agent`, `alc_version`, reflect hook |
| **Tools** | Design-time vendor names documented in SPEC only; runtime via host allow-list |
| **Security** | No secrets in repo; staging credentials via env; audit_log on irreversible steps |
| **UX/Ops** | Human gates on irreversible publish/package; audit trail required |
| **Eval** | Regression suite before canary; no auto-promote of evolution variants |

### 1.4 Core workflows (from source structure)

- Workflow/theme: 1. Project Structure (must be created exactly – agent-first and legible)
- Workflow/theme: 2. Persistent Identity & Research Constitution (OpenClaw + Karpathy + Harness + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- Workflow/theme: 3. Agent Roles (all internal to single Orchestrator thread – Harness-Engineered + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- Workflow/theme: 4. Full Phase-by-Phase Flow (Harness-Engineered + Ratchet + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness – must be implemented exactly)
- Workflow/theme: 5. Quality Gates & Invariants (Mechanical Enforcement – Harness Core + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- Workflow/theme: 6. Master Orchestrator Prompt v1.0 (must be used verbatim as entry point after YES, START)
- Workflow/theme: 7. Non-Functional Requirements (Harness-Enforced, Local-First + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- Workflow/theme: 8. Extra Power-Ups (Highly Recommended)
- Workflow/theme: 9. How to Start Right Now
- Workflow/theme: 1. Executive Recommendation

### 1.5 Dependencies called out or implied by source

- Knowledge/docs: source study file + related corpus under `business/video/corpus/`
- Agents: see candidate pack agents above
- Host services: workflow runs, memory, knowledge retrieval, LLM providers, approvals
- External (design-time): any model/vendor APIs named in source — **not** enabled until allow-listed

### 1.6 Success metrics (seed)

| Metric | How to operationalize in host |
|--------|-------------------------------|
| Spec coverage | % of extracted FRs with automated or checklist validation |
| DNA/run success | Workflow run reach `succeeded` / gated package without unhandled errors |
| Quality | Domain rubric / QC stub → real QC when available |
| Latency/cost | p50/p95 step times; token/cost proxies via costoptimizer patterns |
| Safety | Zero unauthorized tool expansion; HiTL on irreversible steps |

### 1.7 Gaps & assumptions to resolve before development

- Source is research/spec prose, not host API contracts — map each FR to generic-swarm-ops Workflow DNA + agent_spec before coding.
- Vendor/model names in source are design-time only; runtime tools must stay on host allow-list / video_* stubs until approved.
- Success metrics may lack numeric thresholds; define measurable acceptance criteria in sprint 0.
- HiTL, consent, and risk_tier must be set per host governance (no auto-promote).
- Confirm whether capability is a new agent, a skill, a DNA extension, or host infrastructure (N1 isolation).

**Additional source-specific gaps:**
- Confirm ownership: skill vs agent vs DNA-only process.
- Resolve any ambiguous thresholds in source metrics with product owner.
- Identify which sections are aspirational research vs MVP-required.

---

## 2. Dependency Mapping & Pre-Development Setup

### 2.1 Internal dependencies (generic-swarm-ops)

| Dependency | Path / surface | Use |
|------------|----------------|-----|
| Video Domain Pack | `business/video/` | Agents, DNA, corpus, roster |
| Archetype selection | `archetype_registry.json`, recommend-workflow API | Brief → DNA |
| Workflow DNA schema | `business/schemas/workflow-dna.schema.json` | Validate DNA |
| Runtime | `backend/app/runtime.py` | Runs, approvals, domain packs |
| LLM layer | `backend/app/infrastructure/llm/` | Model calls |
| Knowledge/memory | `backend/app/domain/knowledge`, `memory` | RAG / episodic |
| ALC / governance | ALC validator, tool-permission-register | Safety |
| Evals | `backend/app/domain/evaluations`, video evals | Regression |
| FE ops (optional) | `frontend/` domain panels | Operator UX |

### 2.2 External dependencies

| Dependency | Purpose | Notes |
|------------|---------|-------|
| LLM API (OpenAI/xAI/etc.) | Inference | Via host provider abstraction |
| Media gen vendors (design-time) | Video/audio generation | Stay on stubs until approved |
| Search/archive APIs | Research skills | Optional; mock in unit tests |
| Object storage | Artifacts | Host local/S3 adapters |

### 2.3 Pre-development setup checklist

1. [ ] Clone/sync `generic-swarm-ops`; Python venv + `backend` deps installed.
2. [ ] Confirm `business/video/corpus` standalone PASS: `python scripts/business/check_video_corpus_standalone.py`.
3. [ ] Inventory PASS: `python scripts/business/inventory_check.py`.
4. [ ] Read source: `C:/Project/va-agent-swarm/study/coding_agent_functional_specification.md` and mirror under corpus if present.
5. [ ] Map FRs → existing agents/DNA (avoid duplicate agents).
6. [ ] Create feature branch `special/coding_agent`.
7. [ ] Configure staging env vars for LLM (no production keys in git).
8. [ ] Ensure tool allow-list / stubs for any new tool ids (proposal only).
9. [ ] Seed golden brief(s) for this skill under `business/video/evals/` or tests.
10. [ ] Open tracking row in planning (link this file).

---

## 3. Spec-Aligned Implementation Roadmap

### 3.0 Sprint 0 — Spec freeze (3–5 days)

- Complete human line-by-line pass of source; freeze MVP FR list in this plan §1.2.
- Decide artifact type: **(A)** pack agent SPEC update, **(B)** new DNA, **(C)** host skill/service, **(D)** docs-only.
- Write acceptance criteria table FR-id → test-id.
- **Checkpoint:** Product owner signs MVP list.

#### Sprint 1 — 1. Project Structure (must be created exactly – agent-first and legible)
- **Goal:** Implement/test the smallest slice that proves progress on «1. Project Structure (must be created exactly – agent-first and legible)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/coding_agent_sprint1_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 2 — 2. Persistent Identity & Research Constitution (OpenClaw + Karpathy + Harness + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- **Goal:** Implement/test the smallest slice that proves progress on «2. Persistent Identity & Research Constitution (OpenClaw + Karpathy + Harness + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/coding_agent_sprint2_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 3 — 3. Agent Roles (all internal to single Orchestrator thread – Harness-Engineered + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- **Goal:** Implement/test the smallest slice that proves progress on «3. Agent Roles (all internal to single Orchestrator thread – Harness-Engineered + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/coding_agent_sprint3_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 4 — 4. Full Phase-by-Phase Flow (Harness-Engineered + Ratchet + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness – must be implemented exactly)
- **Goal:** Implement/test the smallest slice that proves progress on «4. Full Phase-by-Phase Flow (Harness-Engineered + Ratchet + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness – must be implemented exactly)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/coding_agent_sprint4_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 5 — 5. Quality Gates & Invariants (Mechanical Enforcement – Harness Core + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)
- **Goal:** Implement/test the smallest slice that proves progress on «5. Quality Gates & Invariants (Mechanical Enforcement – Harness Core + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/coding_agent_sprint5_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.


### 3.N Final integration sprint

- Wire recommend-workflow / planner notes if skill affects archetype choice.
- Update `PROCESSES.md` / process_coverage if new process_id.
- Update agent SPECs with self-contained embeds (no refer-only).
- **Checkpoint:** Full FR matrix green or explicitly deferred with reason.

---

## 4. Testing & Validation Framework

### 4.1 Unit tests

| Area | Cases |
|------|-------|
| Parsing / contracts | Inputs from source workflows validate schema |
| Agent/DNA config | agent_spec ALC fields; DNA schema validate |
| Selector/tools | Mocks for external APIs; no real spend in CI |
| Safety | Forbidden tool expansion; irreversible steps require gate |

Suggested path: `backend/app/tests/unit/test_special_coding_agent.py`

### 4.2 Integration tests

- Register/load video pack; start recommended DNA run with fixture brief.
- Assert step agents resolve in roster/standby.
- Approval path for package/publish step succeeds after HiTL simulate.

### 4.3 End-to-end / operator path

- Operator: brief → recommend-workflow (if applicable) → run DNA → approve → audit log present.
- Error handling: empty brief, missing tool, mid-run failure → graceful fail + lesson hook.
- Security: unauthenticated denied; cross-org isolation preserved.
- UX: status surfaces (if FE touched) show run state without silent hang.

### 4.4 Requirement traceability

| Source FR (id) | Test type | Test id | Pass criteria |
|----------------|-----------|---------|---------------|
| FR-01 (from §1.2 item 1) | unit | `test_fr01_*` | Assert expected contract |
| FR-02 | integration | `test_fr02_*` | Run path green |
| … | … | … | … |

_Populate concrete FR-ids during Sprint 0._

### 4.5 Compliance checks

- [ ] N1: no video logic in host core
- [ ] ALC present on agents touched
- [ ] C2PA/provenance notes if media artifacts claimed
- [ ] Privacy review if profiling/personalization involved

---

## 5. Deployment & Post-Launch Monitoring Plan

### 5.1 Phased deployment

| Phase | Scope | Gate |
|-------|-------|------|
| **Dev** | Feature branch + unit/integration | CI green |
| **Staging** | Full DNA run with stubs/real LLM sandbox | Manual QA checklist |
| **Canary 10%** | Enable for 10% orgs/projects or internal tenants only | Error rate < budget; no P0 |
| **Ramp 50%** | Expand if canary stable 72h | Same + latency SLO |
| **GA 100%** | Default on for eligible risk tiers | Runbook + rollback tested |

### 5.2 Rollback

- Feature flag off / DNA `production_ready: false`.
- Revert to prior DNA id (e.g. spine / previous archetype).
- Notify via audit + ops channel.

### 5.3 Monitoring metrics

| Metric | Signal | Alert |
|--------|--------|-------|
| Uptime / run success | % runs succeeded | < 95% over 1h |
| Accuracy / QC | QC pass rate, rubric scores | Drop > 10% vs baseline |
| Latency | p95 step/run duration | Breach SLO |
| Cost | tokens / $ per successful run | > 1.5× baseline |
| User satisfaction | thumbs / CSAT if available | sustained drop |
| Safety | unauthorized tool attempts, gate bypass attempts | any |

### 5.4 Learning loop

- Failed runs → reflect → lessons (ALC) — **no auto-promote**.
- Periodic re-read of source study for drift vs implementation.

---

## 6. Risk Mitigation & Timeline

### 6.1 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Source ambiguity / research-only content | H | H | Sprint 0 freeze; defer non-MVP explicitly |
| Dependency on unallow-listed vendors | H | H | Stubs first; design-time docs only |
| Overlapping agents (duplicate control) | M | H | Map to existing `video.*` roster first |
| DNA theater (stubs marked done) | M | M | Depth field + e2e test required for "ready" |
| Privacy (profiling / voice / likeness) | M | H | HiTL + compliance agents; legal review |
| Scope creep vs N3 video focus | M | M | Timebox; backlog residual in this plan |

### 6.2 Timeline (indicative)

| Milestone | Target | Deliverable |
|-----------|--------|-------------|
| M0 Spec freeze | Week 0–1 | MVP FR list signed |
| M1 Vertical slice | Week 1–2 | One testable DNA/agent path |
| M2 Hardening | Week 2–4 | Tests + gates + docs |
| M3 Staging | Week 4–5 | Staging sign-off |
| M4 Canary 10% | Week 5–6 | Canary metrics OK |
| M5 GA | Week 6–8 | GA + monitoring dashboards |

_Adjust duration up for large sources (e.g. coding_agent, podcast_agent, screenwriter strategic). _

### 6.3 Effort hint from source size

| Source lines | Suggested minimum calendar |
|--------------|----------------------------|
| < 300 | 2–3 weeks to canary |
| 300–800 | 4–6 weeks |
| > 800 | 6–10 weeks phased |

This source: **948 lines** → plan capacity accordingly.

---

## Appendix A — Source heading index (full H2/H3 extract)

| Level | Heading |
|------:|---------|
| 1 | task.md – Final Specification for "N1ch01as Architect v1.0" (Harness-Engineered AGI Meta-System Builder – Local Install Edition with Guided Requirement Discovery + IT Professional Delegation Model + Embedded Task Brief Template + Hermes-Agent Closed Learning Loop + Agent Lightning Tracing & Trainer/Optimizer + Claude Code Core Skills: Superpowers, GSD, gstack + Meta-Harness Outer-Loop Optimization) |
| 2 | 1. Project Structure (must be created exactly – agent-first and legible) |
| 2 | 2. Persistent Identity & Research Constitution (OpenClaw + Karpathy + Harness + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness) |
| 3 | AGENTS.md (must be written verbatim – progressive disclosure map + Hermes hierarchy + Agent Lightning + Claude Code Core Skills + Meta-Harness) |
| 1 | AGENTS.md – Harness Engineering Context Map + Hermes Hierarchical Discovery + Agent Lightning Tracing + Claude Code Core Skills + Meta-Harness Outer-Loop |
| 3 | ORCHESTRATOR_SOUL.md (exact content – must be written verbatim) |
| 3 | ORCHESTRATOR_DIRECTIVE.md (exact content – must be written verbatim) |
| 2 | 3. Agent Roles (all internal to single Orchestrator thread – Harness-Engineered + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness) |
| 3 | Research Swarm – 10 Specialist Types (Orchestrator routes dynamically) |
| 3 | 3.1 Standardized Task Brief Template (must be embedded verbatim and used every time the Orchestrator delegates code work) |
| 3 | 3.2 Pre-Dispatch Improvement Review Block (must run before every Coding Agent dispatch) |
| 2 | 4. Full Phase-by-Phase Flow (Harness-Engineered + Ratchet + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness – must be implemented exactly) |
| 3 | Phase 0: Guided Requirement Discovery (Intent Analyst leads) |
| 3 | Phase 0.5: Harness Initialization (Orchestrator takes over completely – Local-First + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness) |
| 3 | Phase 1: Backend Specification (Smart Swarm + Validator + Critic Ratchet Loop + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness) |
| 3 | Phase 2: Backend Implementation (TDD + Code Critic + Feature Branches + Ratchet + Harness + IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness) |
| 3 | Phase 3: Frontend Specification & Implementation (IT Delegation + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness continues) |
| 3 | Phase 4: Integration, Polish & Delivery (Full Autonomy + Final Hermes + Final Lightning Optimization + Final Core Skills Evolution + Final Meta-Harness) |
| 2 | 5. Quality Gates & Invariants (Mechanical Enforcement – Harness Core + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness) |
| 2 | 6. Master Orchestrator Prompt v1.0 (must be used verbatim as entry point after YES, START) |
| 2 | 7. Non-Functional Requirements (Harness-Enforced, Local-First + Hermes + Agent Lightning + Claude Code Core Skills + Meta-Harness) |
| 3 | 7.0 Mandated Tech Stack (Open-Source, Local-First) |
| 2 | 8. Extra Power-Ups (Highly Recommended) |
| 2 | 9. How to Start Right Now |
| 1 | task_extension_01.md – High-Signal Recommendations for N1ch01as Architect v1.0 |
| 2 | 1. Executive Recommendation |
| 2 | 2. Specific, Actionable Upgrades (All Mandatory for v1.1, Python-Only) |
| 3 | 2.1 Skills System – Python Claw Code Parity (Highest ROI) |
| 3 | 2.2 Tool Registry + Hook Pipeline (Safety & Observability Moat) |
| 3 | 2.3 Plugin System (Extensibility Without Forking) |
| 3 | 2.4 Session & Memory Management – Python Claw Code Compaction |
| 3 | 2.5 Self-Documenting Harness – CLAW.md Pattern (Python Edition) |
| 3 | 2.6 AI-Orchestrated Development Workflow (Python-Native OmX Style) |
| 2 | 3. Updated Phase 0.5 Additions (Exact Python-Only Files/Folders) |
| 2 | 4. New Invariants to Add to Section 5 (Quality Gates) |
| 2 | 5. Expected Outcomes After Python-Only Integration |
| 2 | 6. Implementation Priority Order (Python-Only) |

---

## Appendix B — Traceability

| Artifact | Location |
|----------|----------|
| This plan | `planning/special/coding_agent.md` |
| Upstream study | `C:/Project/va-agent-swarm/study/coding_agent_functional_specification.md` |
| Host pack | `business/video/` |
| Selection | `business/video/archetype_registry.json` |
| Command origin | `generate_special_skills.md` |

---

*End of plan — `coding_agent` — generated 2026-07-13*
