# Repository Comparison: generic-swarm-ops vs va-agent-swarm

**Date:** 2026-07-11  
**Purpose:** Detailed comparison of common functions, strengths, weaknesses, ratings, and gaps based on deep scans of both repos (structure.md, backend.md, frontend.md, adoption.md audits + va study/agents.md, SYSTEM_REFERENCE.md, agent specs, workflows, UI docs, 66-chapter reference, etc.).  
**Methodology:** Identify overlapping functional areas from architecture, specs, and implementation. Rate implementation maturity, spec depth, readiness for production/video domain use. Note missing capabilities.  
**Key Insight:** These repos are highly complementary. `generic-swarm-ops` is a **production-ready governed platform** (runtime, governance, evolution, backend/frontend). `va-agent-swarm` is a **world-class research/spec corpus** for video production multi-agent systems (114 agents, detailed functional/technical specs, workflows, LQR, archetypes, UI concepts) but lacks executable runtime.

---

## Summary Table: Overall Ratings

| Area / Function                  | generic-swarm-ops                          | va-agent-swarm                              | Which is Better?          | Rating (1-10) | Key Gap / Recommendation |
|----------------------------------|--------------------------------------------|---------------------------------------------|---------------------------|---------------|--------------------------|
| **Agent Definition & Roster**   | Basic seed agents (5 ops); domain stubs   | **Complete 114-agent roster** (10 categories, detailed specs in agents.md +  individual functional/technical specs) | va (spec depth)          | generic: 4<br>va: 9 | Import full va roster into generic `business/video/agents/` as Domain Pack. generic needs per-agent schemas + ALC. |
| **Workflow / Process Definition & Orchestration** | Strong Workflow DNA schema, bounded state graph, runtime execution, SSE | Excellent video-specific processes (6-phase E2E, archetypes A–J, LQR family, SVGs, human→AI maps, orchestration spine #53–#56) | Complementary (generic runtime + va domain) | generic: 8<br>va: 8 | Map va processes to generic DNA. generic spine ready; va provides rich video content. |
| **Knowledge Management, RAG, Memory** | Tiered hybrid retrieval (LightRAG-lite), hybrid memory types, provenance, agent/ org scopes | Strong conceptual agentic RAG, knowledge router specs, reference corpus (66 chapters distilled) | generic (implementation) | generic: 7<br>va: 6 | Seed va reference + agentic RAG specs into generic knowledge layer. Add agent-scoped memory. |
| **Evaluation & Quality Assurance** | Full harness (golden, regression, adversarial, human review), EvaluationCard, fitness functions | Rich rubrics, quality gates, critique buses, consistency mechanisms (LQR), psychological alignment | va (domain rubrics)     | generic: 8<br>va: 7 | Port va rubrics/critique into generic evals. generic has better runtime integration. |
| **Governance, Risk, Approvals, Security** | Excellent: risk tiers (0-5), approval gates, audit logs, OWASP mapping, tool permission broker, red-team | Conceptual security/ethics agents, some policy mentions | generic (full implementation) | generic: 9<br>va: 3 | va specs can inform domain-specific risk overrides in generic governance. |
| **Evolution, Learning, Self-Improvement** | Strong sandbox (propose/test/canary/rollback), auto-reflect, lessons, skill sandbox, GEPA-style reflection | Strong intent for per-agent reflection, self-refine, episodic memory, agent_loop iterations (v1–v3) | generic (runtime) + va (intent) | generic: 8<br>va: 6 | Implement Agent Learning Contract (ALC) in generic using va reflection concepts. Add agent genomes. |
| **Frontend / UI for Management** | Production Next.js ops console (dashboard, agents, workflows, runs, Improve, evolution archive, SSE) + OpenDesign MCP | Detailed UI specs (agent management, pipeline viz, production scale discovery, project creation, RETHINK_100) | generic (implemented)   | generic: 8<br>va: 7 | Extend generic FE with video domain pages inspired by va UI specs. Use OpenDesign for consistency. |
| **Backend / Runtime Execution Engine** | Mature FastAPI + runtime.py, workflow engine, workers, state management, tool effects, SSE | Almost none (mostly SVG helpers, narration scripts) | generic (by far)        | generic: 9<br>va: 1 | va is spec-only; rebuild as Domain Pack on generic runtime. No second platform. |
| **Tool Integration & Adapters** | Local adapters (CRM, email, billing, contract, policy), tool permission broker, effects logging | Conceptual media gen tools, adapters for Sora/Veo/etc., prompt tools | generic (framework)     | generic: 7<br>va: 4 | Add video.* media adapters (stubs first for CI) to generic. va provides requirements. |
| **Documentation & Research Depth** | Strong architecture docs (structure.md, backend.md, frontend.md), SDD, gap analyses | **Outstanding** video domain research (114 agents, 66-chapter distillation, deep agent specs, UI, workflows, system_build_plan) | va (domain research)    | generic: 7<br>va: 10 | Use va as authoritative video knowledge seed for generic `business/video/knowledge/`. Keep va as upstream research repo. |
| **Process Intelligence / Analytics** | Dedicated layer (event logs, process miner, conformance, bottleneck, causal agents, PI artifacts) | Implicit in workflows/human→AI maps, some analytics mentions | generic (implementation) | generic: 8<br>va: 4 | va can provide video-specific process models to seed generic PI. |
| **Multi-Domain / Extensibility** | Domain Pack concept emerging, business/ extension point, schemas for multiple packs | Single-domain focus (video) with modular agent specs | generic (platform design) | generic: 7<br>va: 3 | generic designed for dozens of MMA packs; va is perfect first rich pack example. |
| **Overall Production Readiness** | High (product bar ~100, E1 pass, shipped runtime/governance) | Low (spec-complete, runtime-absent) | generic               | generic: 9<br>va: 2 | Merge: generic = host; va = complete Domain Pack (full roster + processes). |

---

## Detailed Explanations by Area

### 1. Agent Definition & Roster
- **generic-swarm-ops**: Has seed ops agents (business_orchestrator, quality_compliance, execution, finance_ops, communications). Domain agents are stubs/placeholders. Strong registry concepts in backend schemas but not populated with 114 video specialists.
- **va-agent-swarm**: Gold standard — full parsed 114-agent roster (study/agents.md), 10 categories (Above-the-Line, Camera, Editorial, Sound, Performance, Distribution, Education, AI-Era, Meta/Orchestration spine #53-80, Workflow Support #81-114), plus deep functional + technical specs for dozens of agents (aesthetics, research, psychological profile/recommendation, coding, general creative, intent analysis, optimization, podcast, screenwriter/strategic goal, knowledge_router, agent_loop v1-v3, planner v2.x, etc.).
- **Rating & Explanation**: va wins decisively on **spec depth and completeness** for video domain. generic has better **runtime registry** foundation. **Gap**: generic missing full roster import and per-agent `agent_spec.json` + ALC bindings. **Recommendation**: Wave 0 import all 114 into `business/video/agents/<pack_id>/` with stable IDs and MAP traceability. Never drop agents.

### 2. Workflow / Process Definition & Orchestration
- **generic-swarm-ops**: Excellent WorkflowDNA schema (inputs, steps, agents, tools, guardrails, verification, rollback, fitness). Bounded state-graph execution, runtime engine, SSE streaming, human gates. Strong for general business processes (e.g., customer onboarding).
- **va-agent-swarm**: Outstanding video-specific decomposition — 6-phase E2E production pipeline, archetypes A–J (viral-hook to feature-film), LQR family (character consistency, per-shot loop, quality gates, engine routing, scene flow), human vs AI workflow maps, orchestration spine (Orchestrator #53, Planner #54, Router #55, Judge #56 + GateKeeper etc.).
- **Rating & Explanation**: Complementary. generic provides **executable runtime + DNA engine**; va provides **rich domain content** (video production logic, critique/QC meshes, consistency mechanisms). **Gap**: va has no executable DNA/runtime; generic lacks video-specific processes pre-import. **Recommendation**: Map va processes to generic WorkflowDNA (orchestrator-down hierarchy required). Start with spine + viral-hook archetype for E2E proof.

### 3. Knowledge Management, RAG, Memory
- **generic-swarm-ops**: Tiered hybrid retrieval (Tier 0 vector default, Tier 1 LightRAG-lite for relational, Tier 2 hierarchical summaries optional), hybrid memory (event, episodic, semantic, procedural, decision, exception, evaluation, provenance), agent/org scopes, provenance always.
- **va-agent-swarm**: Strong conceptual support for agentic RAG, knowledge_router_agent spec, massive distilled reference corpus (66 chapters under study/reference/how_to_build_a_video_agent_system), intent analysis, research specs.
- **Rating & Explanation**: generic better on **implemented retrieval + memory architecture**. va better on **video-domain knowledge depth** (research, aesthetics, psychological alignment, consistency rules). **Gap**: generic learning not strongly per-agent yet; va lacks runtime RAG wiring. **Recommendation**: Seed va reference corpus + agentic RAG specs into generic knowledge layer with full provenance. Extend generic for agent-scoped episodic memory and pre-act retrieval.

### 4. Evaluation & Quality Assurance
- **generic-swarm-ops**: Mature harness (golden tasks, regression, adversarial, human-review sets, historical replay, cost/latency benchmarks, business metrics, safety/compliance). EvaluationCard schema, fitness functions with Pareto selection.
- **va-agent-swarm**: Excellent domain rubrics (aesthetics, psychological alignment, consistency in LQR, quality gates, critique buses, human vs AI workflow coverage matrix).
- **Rating & Explanation**: generic stronger on **runtime evaluation integration and harness**. va stronger on **video-specific quality criteria and rubrics**. **Gap**: va rubrics not yet in executable form. **Recommendation**: Port va rubrics/critique mechanisms into generic EvaluationCards and step guardrails. Use for video golden tasks.

### 5. Governance, Risk, Approvals, Security
- **generic-swarm-ops**: Production-grade — risk tiers (0 Observe to 5 Restricted), approval gates, audit logs, OWASP LLM + Agentic mapping, tool permission broker, red-team, threat models, model cards, assurance cases, NIST/ISO/EU AI Act alignment.
- **va-agent-swarm**: Conceptual (ethics agents, some policy mentions in specs, safety red-team in meta agents) but no implemented governance layer.
- **Rating & Explanation**: generic far superior in **implemented governance and security controls**. va can contribute domain-specific risk overrides and ethics agents. **Gap**: va lacks runtime governance. **Recommendation**: Use generic governance for all packs; extend with va-inspired video risk policies inside `business/video/policies/`.

### 6. Evolution, Learning, Self-Improvement
- **generic-swarm-ops**: Strong sandbox discipline (propose → test → canary → promote/rollback, never mutate production), auto-reflect, lessons-learned, skill sandbox, GEPA-style natural language reflection, improvement APIs, fitness with human gates.
- **va-agent-swarm**: Excellent intent and iteration history — agent_loop v1–v3 with self-refine/Reflexion, episodic memory concepts, planner iterations, RETHINK_100 culture, self-improvement loops in UI specs.
- **Rating & Explanation**: generic better on **sandboxed runtime evolution**. va better on **per-agent reflection intent and iteration patterns**. **Gap**: generic learning currently more workflow-centric than per-agent; va lacks executable evolution. **Recommendation**: Implement mandatory Agent Learning Contract (ALC) in generic (episodic write, reflect tagged by agent_id, pre-act retrieve, sandbox proposals). Use va reflection patterns.

### 7. Frontend / UI for Management
- **generic-swarm-ops**: Production Next.js ops console with dashboard, agent/workflow/run management, approvals queue, knowledge browser, evolution archive, Improve button, SSE real-time, permission-aware nav, loading/empty/error states, OpenDesign MCP workflow.
- **va-agent-swarm**: Detailed aspirational UI specs (agent management dashboard, production pipeline visualization, scale/quality discovery, project creation flow, architecture communication, RETHINK_100 improvements, master shell, surface map).
- **Rating & Explanation**: generic better on **implemented, responsive, real-time ops console**. va better on **video-domain specific UI concepts and flows**. **Gap**: generic lacks dedicated video domain pages. **Recommendation**: Extend generic FE with `/app/domains/video/*` routes inspired by va UI specs. Apply OpenDesign consistently.

### 8. Backend / Runtime Execution Engine
- **generic-swarm-ops**: Mature and shipped — FastAPI control plane, runtime.py with workflow engine/states, workers, Postgres runtime_state JSONB, tool effects, SSE, auth/RBAC, domain models, services layer.
- **va-agent-swarm**: Virtually absent (only SVG generation helpers and narration scripts; no backend, no runtime, no execution engine).
- **Rating & Explanation**: generic overwhelmingly better. va is **spec-only**. **Gap**: va has no executable core. **Recommendation**: Rebuild va **exclusively as a Domain Pack** on generic runtime (`business/video/`). Do not create a second platform (LangGraph/Temporal duplicate forbidden).

### 9. Tool Integration & Adapters
- **generic-swarm-ops**: Framework in place (adapters.py pattern, tool permission broker, ephemeral scoped credentials, effects logging). Current seeds are ops-focused (CRM, email, billing, contract_parser, policy_retriever).
- **va-agent-swarm**: Conceptual requirements for media generation tools (Sora, Veo, Kling, ElevenLabs, etc.), prompt tools, consistency tools.
- **Rating & Explanation**: generic has better **integration framework**. va has better **video media tool requirements**. **Gap**: generic missing video.* media adapters. **Recommendation**: Add video domain adapters (stubs first for CI, real providers later with rate limits/budgets).

### 10. Documentation & Research Depth
- **generic-swarm-ops**: Strong technical architecture (structure.md with full layers, backend.md, frontend.md), SDD process, gap analyses, product bar evidence.
- **va-agent-swarm**: Exceptional video domain research depth — 114 agents with specs, 66-chapter "how to build a video agent system" distillation, deep functional/technical specs for many agents, system_build_plan (M0–M12), UI designs, workflows, human/AI maps, agent_loop/planner iterations, RETHINK_100 culture.
- **Rating & Explanation**: va is the clear winner for **domain research and spec richness**. generic stronger on **platform architecture docs**. **Gap**: va research not yet wired into executable system. **Recommendation**: Treat va as authoritative upstream research/narration repo. Seed its reference corpus and specs into generic `business/video/knowledge/` and agent packs with full provenance.

### 11–12. Process Intelligence & Multi-Domain Extensibility
- **generic-swarm-ops**: Dedicated Process Intelligence layer (event logs, miner/conformance/bottleneck/causal agents, PI artifacts). Domain Pack design for multiple MMA systems.
- **va-agent-swarm**: Implicit process models in workflows and human→AI maps. Single-domain (video) focus.
- **Rating & Explanation**: generic better on both. **Recommendation**: Use va video processes to enrich generic PI. generic architecture already supports dozens of packs — va is ideal first rich example.

---

## Missing Functions / Gaps Summary

**Missing or Weak in generic-swarm-ops**:
- Full video agent roster (114) and domain-specific specs/rubrics.
- Video production processes (archetypes, LQR, 6-phase E2E, consistency mechanisms).
- Rich video-domain knowledge corpus and agentic RAG patterns.
- Per-agent Learning Contract (ALC) enforcement and agent-scoped memory.
- Video-specific media tool adapters.
- Dedicated video domain UI pages and pipeline visualization.

**Missing or Weak in va-agent-swarm**:
- Any production backend/runtime/execution engine.
- Governance, risk tiers, approvals, audit, security controls.
- Evolution sandbox and runtime self-improvement.
- Workflow DNA execution + SSE + workers.
- Tool integration framework and permission broker.
- Scalable multi-tenant backend (auth, RBAC, state management).
- Production frontend ops console with real-time updates.

**Functions Strong in Both (Complementary)**:
- Agent concepts and iteration (va specs + generic runtime).
- Workflow/process thinking (va domain content + generic DNA engine).
- Evaluation/quality (va rubrics + generic harness).
- Self-improvement intent (va reflection patterns + generic sandbox).

---

## Final Recommendation

**Optimal Merge Strategy (as in adoption.md v2.3)**:
- **generic-swarm-ops** = Universal governed MMA host/platform (keep and extend its runtime, governance, evolution, backend/frontend, Domain Pack SDK).
- **va-agent-swarm** = Complete video Domain Pack (import **full 114-agent roster + full processes** into `business/video/`, retain forever in generic project). va repo remains upstream research, specs, narration/scripts source of truth.
- **Key Actions**:
  1. Wave 0: Full catalog import (directories + MAP + minimal specs for all 114).
  2. Implement ALC + agent-scoped learning in generic.
  3. Map va processes to WorkflowDNA (spine first).
  4. Seed va knowledge/reference into generic.
  5. Extend frontend with video domain views.
  6. Add video media tool adapters (stubs → real).
- **Result**: Production-ready video swarm with autonomous per-agent learning, governed execution, and future-proof extensibility to other domains. No duplication, no second platform.

This comparison confirms the two repos together form a powerful foundation when properly merged as platform + rich domain pack.

*End of repo_compare.md*