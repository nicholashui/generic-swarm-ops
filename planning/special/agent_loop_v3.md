# Special skill adoption plan — `agent_loop_v3`

| Field | Value |
|-------|-------|
| **Skill id** | `agent_loop_v3` |
| **Source** | `C:/Project/va-agent-swarm/study/agent_loop_v3.md` |
| **In-pack corpus mirror** | `business/video/corpus/study/agent_loop_v3.md` (if present under video corpus) |
| **Source size** | 714 lines / 52,163 chars / ~18 table rows detected |
| **Host product** | generic-swarm-ops |
| **Plan type** | Spec-driven development (SDD) learning + adoption execution |
| **Generated** | 2026-07-13 |
| **Generator** | `scripts/business/generate_special_skills_plans.py` via `generate_special_skills.md` |

## Host integration stance (N1/N2/N3)

Aligns with host Workflow DNA + ALC reflect hooks; Cynefin/AAR map to gates not new runtime.

| Kind | Guidance |
|------|----------|
| **Domain Pack agents** | Prefer existing `video.*` agents below; create new pack agent only if roster gap is real |
| **Workflow DNA** | Extend/index DNA under `business/video/workflows/`; entry via `video.orchestrator` / `video.planner` |
| **Host core** | Reuse runtime, ALC, knowledge, LLM adapters — do not rebuild a second control plane |
| **Selection** | When production-type relevant, use `business/video/archetype_registry.json` + recommend-workflow API |

**Candidate pack agents:**
- video.orchestrator
- video.planner
- video.memory
- video.judge

**Candidate DNA:**
- wf_video_spine_v1

**Candidate runtime tools (allow-listed / stubs):**
- audit_log_writer

---

## 1. Source Document Review & Requirement Extraction

### 1.1 Source outline (headings extracted)

**H2 sections:**
- 1. Core Principles (Refined from Research)
- 2. The Complete Agent Loop Process (Actionable)
- 3. State, Memory & Infrastructure Recommendations
- 4. Decision Framework (When to Use What)
- 5. Common Pitfalls & Mitigations (from Research)
- 6. Quick-Start Pseudocode Skeleton (Python-like)
- 7. References & Sources

**Selected H3 sections:**
- 1.1 Foundational: ReAct Paradigm (Yao et al., ICLR 2023)
- 1.2 Production xAI Multi-Agent Orchestration (2026)
- 1.3 Hierarchical + Self-Evolving (AgentOrchestra / Surveys 2025-2026)
- 1.4 Cognitive Architecture Enhancements from Ranked Human Thinking Models (v3 Addition)
- 1.5 Known Problems, Failure Modes & Targeted Mitigations (Research-Backed)
- Major Problem Categories & Frequency/Significance
- How Mitigations Integrate into the Loop Phases
- Phase 0: Initialization (Spec-Driven Setup)
- Phase 1: Core Iteration Loop (ReAct-Inspired, Controlled)
- Phase 2: Hierarchical Delegation & Sub-Loops
- Phase 3: Consolidation, Synthesis & Restructuring
- Phase 4: Reflection, Critique & Self-Evolution (Advanced)
- Phase 5: Termination & Output

### 1.2 Functional requirements (extracted / paraphrased from source language)

The following items were mined via keyword heuristics (must/shall/metric/workflow/gate/…) and structural scan. Treat them as a **backlog seed** — refine against full line-by-line human review of the source.

- Target Audience:** Builders of harnesses, multi-agent systems, coding agents, research agents (e.g., N1ch01as-style Architect with critic/self-refinement loops).
- Definition**: Interleave **verbal reasoning traces (Thoughts)** with **actions** (tool calls, environment interactions, or delegation). Observations from actions ground and update reasoning.
- Action**: Decide and output executable step (tool call with args, sub-agent delegation, or `Finish`/`Done`).
- Observation**: Environment / tool / sub-agent returns structured result (data + metadata: status, confidence, summary, issues).
- grok-4.20-multi-agent** (or equivalent): Launches configurable teams (4 agents for quick/focused; 16 for deep/comprehensive).
- Each contributes reasoning, tool calls, findings.
- Leader agent** synthesizes discussion, cross-references, and delivers final structured answer.
- Parallel tool invocation and iteration based on intermediate findings.
- Sub-agent internal states encrypted/hidden by default (control + security); only leader outputs + (optionally) encrypted content exposed.
- Strengths**: Deep multi-step research, structured outputs (tables, comparisons), realtime refinement, automatic tool use without client intervention in the loop.
- Plan-first elements**: Complementary patterns in xAI tools like Grok Build CLI use explicit plan generation first, then parallel sub-agent execution (e.g., up to 8 sub-agents in isolated Git worktrees).
- Decomposes into sub-tasks → delegates to **specialized sub-agents** (Deep Researcher, Analyzer, Browser/Tool agents, Reporter, etc.).
- Each sub-agent runs its **own loop** (ReAct-style or domain-optimized).
- TEA Protocol inspiration** (Tool-Environment-Agent): Treat tools, environments, and agents as first-class, versioned, lifecycle-managed entities with standardized protocols for context, invocation, and evolution.
- Consolidation**: Planner aggregates sub-results, harmonizes evidence, resolves conflicts, updates global plan/state, or triggers refinement. Dedicated Reporter agent often handles final synthesis with citations/deduplication.
- Performance evidence**: AgentOrchestra-style systems reach 89%+ on GAIA benchmark; sub-agents + self-evolution add double-digit gains; hierarchical routing improves scalability vs flat multi-agent.
- Memory Architecture Upgrade**: Add "Pattern Store" (vector + metadata of successful/failed traces with outcome scores) to support RPD fast matching. Hierarchical memory now explicitly tags traces with Cynefin context type for better retrieval.
- Disobeying or misinterpreting task spec, vague roles, missing success criteria or output contracts.
- Phase 0: Mandatory structured Task Specification with explicit success criteria, constraints, output schema, and quality thresholds. Use "living spec" that can be updated.
- Agent repeats the same (or similar) actions without progress; common in ReAct from poor exception handling or missing info; can be induced by prompt injection.
- `Done` / `Finish` tool with mandatory verification before acceptance.
- In hierarchical: Orchestrator monitors sub-agent progress and can kill/reassign stuck branches.
- Aggressive hierarchical memory: Short-term working memory + long-term persistent store (vector search, semantic caching, MemGPT-style).
- Fabricated facts, incorrect tool results interpretation, or unverified claims propagating (worse in multi-agent).
- Inter-Agent Misalignment & Coordination Failures (Multi-Agent Specific)**

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

- Workflow/theme: 1. Core Principles (Refined from Research)
- Workflow/theme: 2. The Complete Agent Loop Process (Actionable)
- Workflow/theme: 3. State, Memory & Infrastructure Recommendations
- Workflow/theme: 4. Decision Framework (When to Use What)
- Workflow/theme: 5. Common Pitfalls & Mitigations (from Research)
- Workflow/theme: 6. Quick-Start Pseudocode Skeleton (Python-like)
- Workflow/theme: 7. References & Sources

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
4. [ ] Read source: `C:/Project/va-agent-swarm/study/agent_loop_v3.md` and mirror under corpus if present.
5. [ ] Map FRs → existing agents/DNA (avoid duplicate agents).
6. [ ] Create feature branch `special/agent_loop_v3`.
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

#### Sprint 1 — 1. Core Principles (Refined from Research)
- **Goal:** Implement/test the smallest slice that proves progress on «1. Core Principles (Refined from Research)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/agent_loop_v3_sprint1_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 2 — 2. The Complete Agent Loop Process (Actionable)
- **Goal:** Implement/test the smallest slice that proves progress on «2. The Complete Agent Loop Process (Actionable)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/agent_loop_v3_sprint2_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 3 — 3. State, Memory & Infrastructure Recommendations
- **Goal:** Implement/test the smallest slice that proves progress on «3. State, Memory & Infrastructure Recommendations» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/agent_loop_v3_sprint3_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 4 — 4. Decision Framework (When to Use What)
- **Goal:** Implement/test the smallest slice that proves progress on «4. Decision Framework (When to Use What)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/agent_loop_v3_sprint4_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 5 — 5. Common Pitfalls & Mitigations (from Research)
- **Goal:** Implement/test the smallest slice that proves progress on «5. Common Pitfalls & Mitigations (from Research)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/agent_loop_v3_sprint5_notes.md` (optional) or this plan's risk log.
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

Suggested path: `backend/app/tests/unit/test_special_agent_loop_v3.py`

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

This source: **714 lines** → plan capacity accordingly.

---

## Appendix A — Source heading index (full H2/H3 extract)

| Level | Heading |
|------:|---------|
| 1 | Refined Agent Loop: Hierarchical, ReAct-Inspired, Production-Grade Design |
| 2 | 1. Core Principles (Refined from Research) |
| 3 | 1.1 Foundational: ReAct Paradigm (Yao et al., ICLR 2023) |
| 3 | 1.2 Production xAI Multi-Agent Orchestration (2026) |
| 3 | 1.3 Hierarchical + Self-Evolving (AgentOrchestra / Surveys 2025-2026) |
| 3 | 1.4 Cognitive Architecture Enhancements from Ranked Human Thinking Models (v3 Addition) |
| 3 | 1.5 Known Problems, Failure Modes & Targeted Mitigations (Research-Backed) |
| 3 | Major Problem Categories & Frequency/Significance |
| 3 | How Mitigations Integrate into the Loop Phases |
| 2 | 2. The Complete Agent Loop Process (Actionable) |
| 3 | Phase 0: Initialization (Spec-Driven Setup) |
| 3 | Phase 1: Core Iteration Loop (ReAct-Inspired, Controlled) |
| 1 | In production: trigger critic or escalate to human |
| 1 | 1. Observe + build context (summarize if long) |
| 1 | 2. Reason + Decide (strict structured output) |
| 1 | 3. Execute with robust error handling |
| 1 | Structured error observation |
| 1 | 4. Structured observation + update state |
| 1 | Optional: exponential backoff on errors |
| 1 | Success path |
| 1 | Successful test call in recovery → fully recover |
| 1 | Test call failed during recovery → go back to OPEN |
| 1 | Optional: if critic_mode == "ensemble": run red_team + paul_elder in parallel and aggregate |
| 1 | Validate on held-out or re-execution |
| 3 | Phase 2: Hierarchical Delegation & Sub-Loops |
| 3 | Phase 3: Consolidation, Synthesis & Restructuring |
| 3 | Phase 4: Reflection, Critique & Self-Evolution (Advanced) |
| 3 | Phase 5: Termination & Output |
| 2 | 3. State, Memory & Infrastructure Recommendations |
| 2 | 4. Decision Framework (When to Use What) |
| 2 | 5. Common Pitfalls & Mitigations (from Research) |
| 2 | 6. Quick-Start Pseudocode Skeleton (Python-like) |
| 1 | 1. Observe |
| 1 | 2. Reason + Decide |
| 1 | 3. Update state |
| 1 | 4. Optional light reflection or full self-evolution pass |
| 2 | 7. References & Sources |

---

## Appendix B — Traceability

| Artifact | Location |
|----------|----------|
| This plan | `planning/special/agent_loop_v3.md` |
| Upstream study | `C:/Project/va-agent-swarm/study/agent_loop_v3.md` |
| Host pack | `business/video/` |
| Selection | `business/video/archetype_registry.json` |
| Command origin | `generate_special_skills.md` |

---

*End of plan — `agent_loop_v3` — generated 2026-07-13*
