# Special skill adoption plan — `agentic_rag`

| Field | Value |
|-------|-------|
| **Skill id** | `agentic_rag` |
| **Source** | `C:/Project/va-agent-swarm/study/agentic_rag_functional_specification.md` |
| **In-pack corpus mirror** | `business/video/corpus/study/agentic_rag_functional_specification.md` (if present under video corpus) |
| **Source size** | 238 lines / 15,507 chars / ~0 table rows detected |
| **Host product** | generic-swarm-ops |
| **Plan type** | Spec-driven development (SDD) learning + adoption execution |
| **Generated** | 2026-07-13 |
| **Generator** | `scripts/business/generate_special_skills_plans.py` via `generate_special_skills.md` |

## Host integration stance (N1/N2/N3)

Host knowledge/retrieval services under backend/app; domain corpora in business/video/corpus.

| Kind | Guidance |
|------|----------|
| **Domain Pack agents** | Prefer existing `video.*` agents below; create new pack agent only if roster gap is real |
| **Workflow DNA** | Extend/index DNA under `business/video/workflows/`; entry via `video.orchestrator` / `video.planner` |
| **Host core** | Reuse runtime, ALC, knowledge, LLM adapters — do not rebuild a second control plane |
| **Selection** | When production-type relevant, use `business/video/archetype_registry.json` + recommend-workflow API |

**Candidate pack agents:**
- video.webresearch
- video.archiveresearch
- video.citation
- video.memory

**Candidate DNA:**
- wf_video_spine_v1

**Candidate runtime tools (allow-listed / stubs):**
- audit_log_writer

---

## 1. Source Document Review & Requirement Extraction

### 1.1 Source outline (headings extracted)

**H2 sections:**
- 1. Core Concepts from Paper (Exact Mapping – Non-Negotiable)
- 2. Full System Architecture (Mermaid – Include & Render in README)
- 3. Detailed Data Models (Pydantic v2 – Required)
- 4. Per-Node Detailed Design (Contracts, Inputs/Outputs, Prompts)
- 5. Hybrid Retrieval & Indexing Design (65k MD Scale – Critical)
- 6. Tools (Dynamic & Extensible)
- 7. Graph Construction (`src/graph/agentic_rag_graph.py`)
- 8. UI, CLI, Evaluation & Production Features
- 9. Phased Implementation Plan (Strict Order – With Checkpoints)
- 10. Success Criteria (Measurable & Verifiable)
- 11. References & Recommended Starters

**Selected H3 sections:**
_No H3 headings extracted._

### 1.2 Functional requirements (extracted / paraphrased from source language)

The following items were mined via keyword heuristics (must/shall/metric/workflow/gate/…) and structural scan. Treat them as a **backlog seed** — refine against full line-by-line human review of the source.

- all outlined requirements. The backend server must be created within a dedicated 'backend' folder structure. Ensure the
- implementation includes proper API endpoints, database schema design, authentication mechanisms, error handling, logging
- systems, and follows RESTful principles. Document all API endpoints with clear specifications, implement comprehensive
- modifying API connection configurations, authentication parameters, model endpoints, and any existing LLM integration code
- components with modern frameworks, implement state management for complex data flows, establish API integrations with
- user feedback mechanisms, ensure cross-browser compatibility, implement proper security measures for data handling, write
- complete frontend project structure to the designated frontend folder. The final deliverable must provide exceptional user
- Task Owner:** Coding Agent
- The system **must**:
- Natively ingest and index your **~65,000 Markdown files (~500 MB corpus)** using **hierarchical chunking** with memory-safe, incremental, resumable processing.
- Include **persistent knowledge compounding** via optional Karpathy-style LLM Wiki output (`wiki_output/` vault with `index.md`, `log.md`, concepts/, frontmatter, [[links]]`).
- Core Agentic Design Patterns** (must be visible as explicit graph cycles/conditional edges):
- Tool Use** — Dynamic, interleaved tool calling (ReAct-style: think → act → observe).
- Multi-Agent Collaboration** — Specialized agents with shared state, hierarchical supervision, or flat peer coordination.
- Single-agent routing + multi-agent delegation.
- Stateful memory (conversation + long-term index + checkpoints).
- Router --> Planner[Planner Agent<br/>Decompose + Multi-Hop Plan]
- Planner --> ToolRouter[Tool Router<br/>Structured Decision: Vector | LightRAG | Web | Wiki]
- ToolRouter --> Web[Tavily Web Search Tool]
- Vector & LightRAGNode & Web --> Researcher[Researcher + Grader Agent<br/>Reflection Loop + Doc Rubric Scoring]
- Researcher --> Generator[Generator Agent<br/>Synthesize with Citations]
- Generator --> Critic[Critic Agent<br/>Faithfulness + Hallucination Check]
- Final --> WikiSynth[Optional Wiki Synthesizer Agent<br/>Karpathy-style Persistent Output]
- subgraph "State & Memory"
- query_analyzer**: Classify complexity (simple/factual vs. multi-hop/relational). Decide routing. Prompt: `prompts/analyzer.md` (rubric-based classification).

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

- Workflow/theme: 1. Core Concepts from Paper (Exact Mapping – Non-Negotiable)
- Workflow/theme: 2. Full System Architecture (Mermaid – Include & Render in README)
- Workflow/theme: 3. Detailed Data Models (Pydantic v2 – Required)
- Workflow/theme: 4. Per-Node Detailed Design (Contracts, Inputs/Outputs, Prompts)
- Workflow/theme: 5. Hybrid Retrieval & Indexing Design (65k MD Scale – Critical)
- Workflow/theme: 6. Tools (Dynamic & Extensible)
- Workflow/theme: 7. Graph Construction (`src/graph/agentic_rag_graph.py`)
- Workflow/theme: 8. UI, CLI, Evaluation & Production Features
- Workflow/theme: 9. Phased Implementation Plan (Strict Order – With Checkpoints)
- Workflow/theme: 10. Success Criteria (Measurable & Verifiable)

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
4. [ ] Read source: `C:/Project/va-agent-swarm/study/agentic_rag_functional_specification.md` and mirror under corpus if present.
5. [ ] Map FRs → existing agents/DNA (avoid duplicate agents).
6. [ ] Create feature branch `special/agentic_rag`.
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

#### Sprint 1 — 1. Core Concepts from Paper (Exact Mapping – Non-Negotiable)
- **Goal:** Implement/test the smallest slice that proves progress on «1. Core Concepts from Paper (Exact Mapping – Non-Negotiable)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/agentic_rag_sprint1_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 2 — 2. Full System Architecture (Mermaid – Include & Render in README)
- **Goal:** Implement/test the smallest slice that proves progress on «2. Full System Architecture (Mermaid – Include & Render in README)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/agentic_rag_sprint2_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 3 — 3. Detailed Data Models (Pydantic v2 – Required)
- **Goal:** Implement/test the smallest slice that proves progress on «3. Detailed Data Models (Pydantic v2 – Required)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/agentic_rag_sprint3_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 4 — 4. Per-Node Detailed Design (Contracts, Inputs/Outputs, Prompts)
- **Goal:** Implement/test the smallest slice that proves progress on «4. Per-Node Detailed Design (Contracts, Inputs/Outputs, Prompts)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/agentic_rag_sprint4_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 5 — 5. Hybrid Retrieval & Indexing Design (65k MD Scale – Critical)
- **Goal:** Implement/test the smallest slice that proves progress on «5. Hybrid Retrieval & Indexing Design (65k MD Scale – Critical)» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/agentic_rag_sprint5_notes.md` (optional) or this plan's risk log.
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

Suggested path: `backend/app/tests/unit/test_special_agentic_rag.py`

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

This source: **238 lines** → plan capacity accordingly.

---

## Appendix A — Source heading index (full H2/H3 extract)

| Level | Heading |
|------:|---------|
| 1 | Task: Build Ultra-Production-Grade Hybrid Agentic RAG System – Exhaustive Architectural & Implementation Specification (April 2026) |
| 1 | How to create backend services |
| 1 | How to create frontend services |
| 2 | 1. Core Concepts from Paper (Exact Mapping – Non-Negotiable) |
| 2 | 2. Full System Architecture (Mermaid – Include & Render in README) |
| 2 | 3. Detailed Data Models (Pydantic v2 – Required) |
| 2 | 4. Per-Node Detailed Design (Contracts, Inputs/Outputs, Prompts) |
| 2 | 5. Hybrid Retrieval & Indexing Design (65k MD Scale – Critical) |
| 2 | 6. Tools (Dynamic & Extensible) |
| 2 | 7. Graph Construction (`src/graph/agentic_rag_graph.py`) |
| 2 | 8. UI, CLI, Evaluation & Production Features |
| 2 | 9. Phased Implementation Plan (Strict Order – With Checkpoints) |
| 2 | 10. Success Criteria (Measurable & Verifiable) |
| 2 | 11. References & Recommended Starters |

---

## Appendix B — Traceability

| Artifact | Location |
|----------|----------|
| This plan | `planning/special/agentic_rag.md` |
| Upstream study | `C:/Project/va-agent-swarm/study/agentic_rag_functional_specification.md` |
| Host pack | `business/video/` |
| Selection | `business/video/archetype_registry.json` |
| Command origin | `generate_special_skills.md` |

---

*End of plan — `agentic_rag` — generated 2026-07-13*
