# Special skill adoption plan — `knowledge_router_agent`

| Field | Value |
|-------|-------|
| **Skill id** | `knowledge_router_agent` |
| **Source** | `C:/Project/va-agent-swarm/study/knowledge_router_agent.md` |
| **In-pack corpus mirror** | `business/video/corpus/study/knowledge_router_agent.md` (if present under video corpus) |
| **Source size** | 343 lines / 18,368 chars / ~0 table rows detected |
| **Host product** | generic-swarm-ops |
| **Plan type** | Spec-driven development (SDD) learning + adoption execution |
| **Generated** | 2026-07-13 |
| **Generator** | `scripts/business/generate_special_skills_plans.py` via `generate_special_skills.md` |

## Host integration stance (N1/N2/N3)

Maps to router_table.json + knowledge retrieval scopes; no parallel bus.

| Kind | Guidance |
|------|----------|
| **Domain Pack agents** | Prefer existing `video.*` agents below; create new pack agent only if roster gap is real |
| **Workflow DNA** | Extend/index DNA under `business/video/workflows/`; entry via `video.orchestrator` / `video.planner` |
| **Host core** | Reuse runtime, ALC, knowledge, LLM adapters — do not rebuild a second control plane |
| **Selection** | When production-type relevant, use `business/video/archetype_registry.json` + recommend-workflow API |

**Candidate pack agents:**
- video.router
- video.memory
- video.webresearch

**Candidate DNA:**
- wf_video_spine_v1

**Candidate runtime tools (allow-listed / stubs):**
- audit_log_writer

---

## 1. Source Document Review & Requirement Extraction

### 1.1 Source outline (headings extracted)

**H2 sections:**
- Executive Summary
- 1. Purpose & Success Criteria
- 2. Architecture Overview
- 3. Input / Output Contract (Strict & Rich)
- 4. Core Components (Detailed)
- 5. Particular Use Case Implementations
- 6. Knowledge Base Integration Requirements
- 7. Phased Implementation Roadmap
- 8. Evaluation Framework
- 9. Edge Cases & Mitigations
- 10. Tech Recommendations (Aligned with Your Stack)
- 11. Generalization to Any Domain
- Next Steps (Recommended)

**Selected H3 sections:**
- Input from Requesting Agent
- Output from Router
- 4.1 Query Analyzer + Intent Classifier
- 4.2 Planner (for High-Complexity / Pipeline Queries)
- 4.3 Hybrid Retrieval Engine (The Heart)
- 4.4 Context Assembler
- 4.5 Explainer & Traceability
- 4.6 Multi-Level Critic (Self-Improving Core)
- Use Case 1: Character Consistency Critic Agent
- Use Case 2: Video Prompt Optimizer Agent
- Use Case 3: Multi-Agent Orchestrator Designer
- Use Case 4: Shot Planning Agent (Script → Shot List → Generation)

### 1.2 Functional requirements (extracted / paraphrased from source language)

The following items were mined via keyword heuristics (must/shall/metric/workflow/gate/…) and structural scan. Treat them as a **backlog seed** — refine against full line-by-line human review of the source.

- Domains:** AI Filmmaking (text-to-video, consistency, cinematic pipelines) + AI Agents (multi-agent orchestration, advanced RAG, self-improving systems)
- Performance-Supervised Improvement** (soft labels from actual agent success, like AgentRouter)
- Serve as the single, intelligent gateway between any requesting agent and the curated knowledge base. It must understand *who* is asking, *what* they need, and *why*, then deliver the optimal context pack with full reasoning.
- Success Criteria (Quality Gates)**
- Retrieval precision (relevant files returned in top results): ≥ 88% (critic or human eval)
- Routing decision quality (downstream agent success improvement): measurable lift
- Latency: < 4s p95 for standard queries; < 8s for complex pipeline queries
- Continuous improvement: Routing accuracy improves over time via critic feedback and performance signals
- Requesting Agent (e.g. Character Consistency Critic)
- Knowledge Router Agent
- └── Optional Pre-computed Centroids per Domain/Agent Cluster
- Self-Reflection**: The Router itself uses reflection tokens / critic steps (Self-RAG inspired) to judge its own retrieval quality before finalizing output.
- "task_description": "Ensure face, clothing, and prop consistency across 12 shots in a cinematic wuxia fight scene using Seedance + Kling hybrid workflow",
- Decomposes into sub-tasks (e.g., 1. Character bible creation, 2. Shot-by-shot consistency rules, 3. Lighting-specific mitigations, 4. Tool-specific prompt patterns).
- Reflection step: “Are these passages actually useful for the downstream agent’s goal?” “Is anything critical missing?”
- For creative agents: often returns “Knowledge Pack” with sections like Best Practices, Failure Modes & Mitigations, Tool-Specific Notes, Prompt Templates.
- Every output includes a clear `reasoning_trace` (structured + natural language). This is non-negotiable for debugging and critic loops.
- Downstream Utility Critic**: (Ideal) Observes or gets feedback from the requesting agent after it uses the context (“Did this knowledge help you succeed? What was missing?”). Feeds back as soft supervision signal (like AgentRouter’s F1-based training targets).
- Request Example**: See Input contract above (wuxia fight scene).
- Planner decomposes: “Orchestration for consistency across shots” + “Cost/latency optimization for video gen agents”
- Iterative routing across scriptwriting, cinematography language, tool-specific shot capabilities, consistency constraints
- Every `.md` file **must** have rich frontmatter (this is non-negotiable for the Router to work well):
- Structured Knowledge Pack output
- Performance signal feedback loop (downstream agent success → soft labels)
- Cost/latency-aware routing

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

- Workflow/theme: Executive Summary
- Workflow/theme: 1. Purpose & Success Criteria
- Workflow/theme: 2. Architecture Overview
- Workflow/theme: 3. Input / Output Contract (Strict & Rich)
- Workflow/theme: 4. Core Components (Detailed)
- Workflow/theme: 5. Particular Use Case Implementations
- Workflow/theme: 6. Knowledge Base Integration Requirements
- Workflow/theme: 7. Phased Implementation Roadmap
- Workflow/theme: 8. Evaluation Framework
- Workflow/theme: 9. Edge Cases & Mitigations

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
4. [ ] Read source: `C:/Project/va-agent-swarm/study/knowledge_router_agent.md` and mirror under corpus if present.
5. [ ] Map FRs → existing agents/DNA (avoid duplicate agents).
6. [ ] Create feature branch `special/knowledge_router_agent`.
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

#### Sprint 1 — Executive Summary
- **Goal:** Implement/test the smallest slice that proves progress on «Executive Summary» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/knowledge_router_agent_sprint1_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 2 — 1. Purpose & Success Criteria
- **Goal:** Implement/test the smallest slice that proves progress on «1. Purpose & Success Criteria» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/knowledge_router_agent_sprint2_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 3 — 2. Architecture Overview
- **Goal:** Implement/test the smallest slice that proves progress on «2. Architecture Overview» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/knowledge_router_agent_sprint3_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 4 — 3. Input / Output Contract (Strict & Rich)
- **Goal:** Implement/test the smallest slice that proves progress on «3. Input / Output Contract (Strict & Rich)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/knowledge_router_agent_sprint4_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 5 — 4. Core Components (Detailed)
- **Goal:** Implement/test the smallest slice that proves progress on «4. Core Components (Detailed)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/knowledge_router_agent_sprint5_notes.md` (optional) or this plan's risk log.
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

Suggested path: `backend/app/tests/unit/test_special_knowledge_router_agent.py`

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

This source: **343 lines** → plan capacity accordingly.

---

## Appendix A — Source heading index (full H2/H3 extract)

| Level | Heading |
|------:|---------|
| 1 | Knowledge Router Agent — Complete Specification & Implementation Guide |
| 2 | Executive Summary |
| 2 | 1. Purpose & Success Criteria |
| 2 | 2. Architecture Overview |
| 2 | 3. Input / Output Contract (Strict & Rich) |
| 3 | Input from Requesting Agent |
| 3 | Output from Router |
| 2 | 4. Core Components (Detailed) |
| 3 | 4.1 Query Analyzer + Intent Classifier |
| 3 | 4.2 Planner (for High-Complexity / Pipeline Queries) |
| 3 | 4.3 Hybrid Retrieval Engine (The Heart) |
| 3 | 4.4 Context Assembler |
| 3 | 4.5 Explainer & Traceability |
| 3 | 4.6 Multi-Level Critic (Self-Improving Core) |
| 2 | 5. Particular Use Case Implementations |
| 3 | Use Case 1: Character Consistency Critic Agent |
| 3 | Use Case 2: Video Prompt Optimizer Agent |
| 3 | Use Case 3: Multi-Agent Orchestrator Designer |
| 3 | Use Case 4: Shot Planning Agent (Script → Shot List → Generation) |
| 2 | 6. Knowledge Base Integration Requirements |
| 2 | 7. Phased Implementation Roadmap |
| 2 | 8. Evaluation Framework |
| 2 | 9. Edge Cases & Mitigations |
| 2 | 10. Tech Recommendations (Aligned with Your Stack) |
| 2 | 11. Generalization to Any Domain |
| 2 | Next Steps (Recommended) |

---

## Appendix B — Traceability

| Artifact | Location |
|----------|----------|
| This plan | `planning/special/knowledge_router_agent.md` |
| Upstream study | `C:/Project/va-agent-swarm/study/knowledge_router_agent.md` |
| Host pack | `business/video/` |
| Selection | `business/video/archetype_registry.json` |
| Command origin | `generate_special_skills.md` |

---

*End of plan — `knowledge_router_agent` — generated 2026-07-13*
