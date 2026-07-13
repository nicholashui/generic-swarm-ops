# Special skill adoption plan — `research_agent`

| Field | Value |
|-------|-------|
| **Skill id** | `research_agent` |
| **Source** | `C:/Project/va-agent-swarm/study/research_agent_functional_specification.md` |
| **In-pack corpus mirror** | `business/video/corpus/study/research_agent_functional_specification.md` (if present under video corpus) |
| **Source size** | 895 lines / 46,072 chars / ~0 table rows detected |
| **Host product** | generic-swarm-ops |
| **Plan type** | Spec-driven development (SDD) learning + adoption execution |
| **Generated** | 2026-07-13 |
| **Generator** | `scripts/business/generate_special_skills_plans.py` via `generate_special_skills.md` |

## Host integration stance (N1/N2/N3)

Research family 66–72; integrate corpus + source grading.

| Kind | Guidance |
|------|----------|
| **Domain Pack agents** | Prefer existing `video.*` agents below; create new pack agent only if roster gap is real |
| **Workflow DNA** | Extend/index DNA under `business/video/workflows/`; entry via `video.orchestrator` / `video.planner` |
| **Host core** | Reuse runtime, ALC, knowledge, LLM adapters — do not rebuild a second control plane |
| **Selection** | When production-type relevant, use `business/video/archetype_registry.json` + recommend-workflow API |

**Candidate pack agents:**
- video.webresearch
- video.archiveresearch
- video.factchecker
- video.citation
- video.benchmarkresearch

**Candidate DNA:**
- wf_video_arch_i_documentary_v1
- wf_video_spine_v1

**Candidate runtime tools (allow-listed / stubs):**
- audit_log_writer

---

## 1. Source Document Review & Requirement Extraction

### 1.1 Source outline (headings extracted)

**H2 sections:**
- 1. Document Control
- 2. Purpose
- 3. Scope
- 4. Stakeholders, Roles, and External Actors
- 5. System Context and Architecture
- 6. Technology and Runtime Dependencies
- 7. Configuration Specification
- 8. User Interface Specification
- 9. User Roles and Permissions Specification
- 10. CLI Command Functional Requirements
- 11. Session Management Specification
- 12. External Document Preprocessing Specification
- 13. Research Workflow State Machine
- 14. Phase-by-Phase Functional Requirements
- 15. Source Fetching and Transformation Specification
- 16. Knowledge Compilation Specification
- 17. Final Report, Image Prompt, and YouTube Script Specification
- 18. Input and Output File Specification
- 19. Validation Rules
- 20. Error Handling and Recovery Specification

**Selected H3 sections:**
- 3.1 In Scope
- 3.2 Out of Scope
- 4.1 Human User Roles
- 4.2 System Actors
- 4.3 Access Model
- 5.1 Core Modules
- 5.2 Execution Model
- 7.1 Environment Variables
- 7.2 `.env` Resolution
- 8.1 Interface Type
- 8.2 Human Interaction Points
- 8.3 Unattended Mode
- 10.1 Common Command Behavior
- 10.2 `start`
- 10.3 `resume`

### 1.2 Functional requirements (extracted / paraphrased from source language)

The following items were mined via keyword heuristics (must/shall/metric/workflow/gate/…) and structural scan. Treat them as a **backlog seed** — refine against full line-by-line human review of the source.

- Document title: `Research Agent Functional Specification`
- System name: `grok-research-agent`
- Specification intent: Describe the functional behavior the system currently implements, including workflow behavior, file contracts, validation rules, failure handling, and integration points
- use Grok through the xAI OpenAI-compatible API for all LLM generation tasks;
- Eight-phase research workflow orchestration
- Web UI, API server, or multi-user collaboration
- `Research Operator`: Starts sessions, approves or revises workflow outputs, selects curated sources, optionally chooses full offline collection, and runs auxiliary commands
- `Reviewer/Study User`: Consumes generated report, drill pack, hypergraph, Mermaid output, image prompts, or YouTube script; this role is not technically distinct from the operator
- `LLM Provider`: xAI Grok, accessed through the OpenAI-compatible API
- Implements the workflow state machine
- Maps API exceptions into domain-specific runtime errors
- Defines output contracts and behavioral instructions for LLM calls
- Required packages:
- Packaged CLI entrypoint: `grok-research-agent = grok_research_agent.cli:main`
- Required for any command path that instantiates `GrokClient`
- Must be non-empty after whitespace trimming
- If absent, LLM-backed actions shall fail with a clear message
- Blank values shall be normalized back to `grok-3`
- Invalid or non-numeric values shall revert to `50000`
- Values below `1` shall be clamped to `1`
- Invalid or non-numeric values shall revert to `300`
- If absent, selecting `edit` shall still create the editable temporary file, but no external editor is launched automatically
- When the workflow constructs a default `GrokClient`, it shall attempt to load a `.env` file located two directory levels above the session directory.
- If no `.env` exists there, the system shall continue using process environment variables only.
- `--auto` shall bypass interactive prompts and drive the workflow to completion where possible.

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

- Workflow/theme: 1. Document Control
- Workflow/theme: 2. Purpose
- Workflow/theme: 3. Scope
- Workflow/theme: 4. Stakeholders, Roles, and External Actors
- Workflow/theme: 5. System Context and Architecture
- Workflow/theme: 6. Technology and Runtime Dependencies
- Workflow/theme: 7. Configuration Specification
- Workflow/theme: 8. User Interface Specification
- Workflow/theme: 9. User Roles and Permissions Specification
- Workflow/theme: 10. CLI Command Functional Requirements

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
4. [ ] Read source: `C:/Project/va-agent-swarm/study/research_agent_functional_specification.md` and mirror under corpus if present.
5. [ ] Map FRs → existing agents/DNA (avoid duplicate agents).
6. [ ] Create feature branch `special/research_agent`.
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

#### Sprint 1 — 1. Document Control
- **Goal:** Implement/test the smallest slice that proves progress on «1. Document Control» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/research_agent_sprint1_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 2 — 2. Purpose
- **Goal:** Implement/test the smallest slice that proves progress on «2. Purpose» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/research_agent_sprint2_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 3 — 3. Scope
- **Goal:** Implement/test the smallest slice that proves progress on «3. Scope» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/research_agent_sprint3_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 4 — 4. Stakeholders, Roles, and External Actors
- **Goal:** Implement/test the smallest slice that proves progress on «4. Stakeholders, Roles, and External Actors» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/research_agent_sprint4_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 5 — 5. System Context and Architecture
- **Goal:** Implement/test the smallest slice that proves progress on «5. System Context and Architecture» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/research_agent_sprint5_notes.md` (optional) or this plan's risk log.
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

Suggested path: `backend/app/tests/unit/test_special_research_agent.py`

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

This source: **895 lines** → plan capacity accordingly.

---

## Appendix A — Source heading index (full H2/H3 extract)

| Level | Heading |
|------:|---------|
| 1 | Research Agent Functional Specification |
| 2 | 1. Document Control |
| 2 | 2. Purpose |
| 2 | 3. Scope |
| 3 | 3.1 In Scope |
| 3 | 3.2 Out of Scope |
| 2 | 4. Stakeholders, Roles, and External Actors |
| 3 | 4.1 Human User Roles |
| 3 | 4.2 System Actors |
| 3 | 4.3 Access Model |
| 2 | 5. System Context and Architecture |
| 3 | 5.1 Core Modules |
| 3 | 5.2 Execution Model |
| 2 | 6. Technology and Runtime Dependencies |
| 2 | 7. Configuration Specification |
| 3 | 7.1 Environment Variables |
| 3 | 7.2 `.env` Resolution |
| 2 | 8. User Interface Specification |
| 3 | 8.1 Interface Type |
| 3 | 8.2 Human Interaction Points |
| 3 | 8.3 Unattended Mode |
| 2 | 9. User Roles and Permissions Specification |
| 2 | 10. CLI Command Functional Requirements |
| 3 | 10.1 Common Command Behavior |
| 3 | 10.2 `start` |
| 3 | 10.3 `resume` |
| 3 | 10.4 `list-sessions` |
| 3 | 10.5 `list-types` |
| 3 | 10.6 `update` |
| 3 | 10.7 `synthesize` |
| 3 | 10.8 `compile` |
| 3 | 10.9 `drill` |
| 3 | 10.10 `feed` |
| 3 | 10.11 `show` |
| 3 | 10.12 `generate-images` |
| 3 | 10.13 `youtube-script` |
| 2 | 11. Session Management Specification |
| 3 | 11.1 Session Identity |
| 3 | 11.2 Session State |
| 3 | 11.3 Session Persistence Rules |
| 3 | 11.4 Run Directory Rules |
| 2 | 12. External Document Preprocessing Specification |
| 3 | 12.1 Feature Purpose |
| 3 | 12.2 Trigger Rules |
| 3 | 12.3 Supported Inputs |
| 3 | 12.4 Processing Rules |
| 3 | 12.5 Aggregated Outputs |
| 3 | 12.6 Status Rules |
| 3 | 12.7 Prompt Injection Rules |
| 2 | 13. Research Workflow State Machine |
| 3 | 13.1 State Definitions |
| 3 | 13.2 Interactive Progression Rules |
| 3 | 13.3 Auto-Mode Progression Rules |
| 2 | 14. Phase-by-Phase Functional Requirements |
| 3 | 14.1 Phase 0 - Scope Confirmation |
| 3 | 14.2 Phase 1 - Discovery |
| 3 | 14.3 Phase 2 - Curation and Gap Analysis |
| 3 | 14.4 Phase 3 - Extraction |
| 3 | 14.5 Phase 4 - Notebook Assembly |
| 3 | 14.6 Phase 5 - Synthesis and Review |
| 3 | 14.7 Phase 6 - Full Offline Collection |
| 3 | 14.8 Phase 7 - Final Polish |
| 3 | 14.9 Phase 8 - Complete |
| 2 | 15. Source Fetching and Transformation Specification |
| 3 | 15.1 URL Validation |
| 3 | 15.2 HTTP Fetch Rules |
| 3 | 15.3 Content-Type Handling |
| 3 | 15.4 HTML Text Normalization |
| 2 | 16. Knowledge Compilation Specification |
| 3 | 16.1 Compiler Inputs and Outputs |
| 3 | 16.2 Hypergraph Contract |
| 3 | 16.3 Core Concepts Contract |
| 3 | 16.4 Drill-Pack Contract |
| 3 | 16.5 Feed and Hypergraph Update |
| 3 | 16.6 Mermaid Rendering |
| 2 | 17. Final Report, Image Prompt, and YouTube Script Specification |
| 3 | 17.1 Final Report Output Contract |
| 3 | 17.2 Image Prompt Generation |
| 3 | 17.3 YouTube Script Generation |
| 2 | 18. Input and Output File Specification |
| 3 | 18.1 Session Root Outputs |
| 3 | 18.2 Knowledge Base Outputs |
| 3 | 18.3 Run-Scoped Outputs |
| 2 | 19. Validation Rules |
| 3 | 19.1 CLI Validation |
| 3 | 19.2 Semantic Validation |
| 3 | 19.3 File Validation |
| 2 | 20. Error Handling and Recovery Specification |
| 3 | 20.1 Grok API Errors |
| 3 | 20.2 LLM Timeout Tolerance |
| 3 | 20.3 Source Fetch Errors |
| 3 | 20.4 JSON Robustness |
| 3 | 20.5 Non-Fatal Degradation Rules |
| 2 | 21. Integration Specifications |
| 3 | 21.1 xAI Grok Integration |
| 3 | 21.2 Remote Web Integration |
| 3 | 21.3 Local Document Integration |
| 2 | 22. Security and Privacy Requirements |
| 2 | 23. Non-Functional Constraints with Functional Impact |
| 2 | 24. Current Implementation Notes and Known Functional Gaps |
| 2 | 25. Acceptance Criteria |
| 2 | 26. Traceability Summary |

---

## Appendix B — Traceability

| Artifact | Location |
|----------|----------|
| This plan | `planning/special/research_agent.md` |
| Upstream study | `C:/Project/va-agent-swarm/study/research_agent_functional_specification.md` |
| Host pack | `business/video/` |
| Selection | `business/video/archetype_registry.json` |
| Command origin | `generate_special_skills.md` |

---

*End of plan — `research_agent` — generated 2026-07-13*
