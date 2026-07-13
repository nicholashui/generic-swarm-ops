# Special skill adoption plan — `psychological_profile_agent`

| Field | Value |
|-------|-------|
| **Skill id** | `psychological_profile_agent` |
| **Source** | `C:/Project/va-agent-swarm/study/psychological_profile_agent_functional_specifications.md` |
| **In-pack corpus mirror** | `business/video/corpus/study/psychological_profile_agent_functional_specifications.md` (if present under video corpus) |
| **Source size** | 500 lines / 45,391 chars / ~227 table rows detected |
| **Host product** | generic-swarm-ops |
| **Plan type** | Spec-driven development (SDD) learning + adoption execution |
| **Generated** | 2026-07-13 |
| **Generator** | `scripts/business/generate_special_skills_plans.py` via `generate_special_skills.md` |

## Host integration stance (N1/N2/N3)

Audience/persona signals for retention; privacy/HiTL for sensitive profiling.

| Kind | Guidance |
|------|----------|
| **Domain Pack agents** | Prefer existing `video.*` agents below; create new pack agent only if roster gap is real |
| **Workflow DNA** | Extend/index DNA under `business/video/workflows/`; entry via `video.orchestrator` / `video.planner` |
| **Host core** | Reuse runtime, ALC, knowledge, LLM adapters — do not rebuild a second control plane |
| **Selection** | When production-type relevant, use `business/video/archetype_registry.json` + recommend-workflow API |

**Candidate pack agents:**
- video.audiencesim
- video.emotionalarc
- video.retentionoptimizer

**Candidate DNA:**
- wf_video_arch_a_viral_hook_v1
- wf_video_arch_b_ugc_ad_v1

**Candidate runtime tools (allow-listed / stubs):**
- audit_log_writer

---

## 1. Source Document Review & Requirement Extraction

### 1.1 Source outline (headings extracted)

**H2 sections:**
- 100 Writer Profiles for Screenwriting Framework
- 📊 Complete File Overview Table
- 📈 Parameter Explanations and Usage Guide
- 🔧 Framework Adaptation Matrix
- 📊 Quick Query Index
- 🛠️ Tool Configuration Quick Reference
- 📋 Personalized Configuration Generator
- 📝 Usage Instructions

**Selected H3 sections:**
- Profiles 1-25: Introverted Creative Type
- Profiles 26-50: Extroverted Social Type
- Nos. 51-75: Trauma Experience Type
- Profiles 76-100: Professional Transition Type
- Field Definitions
- Energy Mode Interpretation
- Phase 1 (Motivation Exploration) Adaptation
- Phase 2 (Audience Definition) Adaptation
- Phase 3 (Method Design) Adaptation
- Stage 4 (Emotional Design) Adaptation
- Phase 5 (Execution and Creation) Adaptation
- Stage 6 (Iterative Refinement) Adaptation
- By MBTI Type
- By Core Motivation
- By Primary Fear

### 1.2 Functional requirements (extracted / paraphrased from source language)

The following items were mined via keyword heuristics (must/shall/metric/workflow/gate/…) and structural scan. Treat them as a **backlog seed** — refine against full line-by-line human review of the source.

- Purpose:** Provide personalized parameter configurations for the framework in this chapter and Appendix A workflow
- Framework adaptation (key focuses for each stage, predicted obstacles, success strategies)
- | REALX | 38 | Real Estate Agent | ESTJ | Deal Stories | Failure | Transaction Narrative | Morning | High Frequency High Intensity | High | Medium | Low | Low | Medium | CRM Modified | 25/5 | 10 | Performance Tracking | Overly Commercial | Humanity Injection |
- | IMMGR | 35 | Immigrant | ISFJ | Cultural bridge | Non-acceptance | Immigration narrative | Evening | Medium frequency medium intensity | Medium | Medium | Medium | Medium | Medium | Bilingual tools | 25/5 | 6 | Immigrant community | Cultural translation | Universal emotions |
- | SPYX | 50 | Former intelligence agent | INTJ | Spy narrative | Exposure | Spy drama | Late night | Low-frequency high-intensity | Extremely low | High | Low | Low | Low | Secure tools | 30/5 | 8 | None | Sensitive content | Fully fictional |
- | MBTI Tendency | 16 types | Psychological type tendency, affects tool selection |
- | Weekly Target Pages | Number | Sustainable output goal |
- | High Frequency High Intensity | Can write every day, high output each time | 1-2 hours daily |
- | High Frequency Medium Intensity | Can write every day, stable output | 45-60 minutes daily |
- | High Frequency Low Intensity | Can write every day, but low output | 30 minutes daily, multiple times |
- | Medium Frequency High Intensity | Write every other day, high output each time | 2 hours every other day |
- | Medium Frequency Medium Intensity | Write every other day, stable output | 1 hour every other day |
- | Medium Frequency Low Intensity | Write every other day, low output | 45 minutes every other day |
- | Low Frequency High Intensity | 2-3 times per week, high output each time | 3 hours concentrated on weekends |
- | Low Frequency Medium Intensity | 2-3 times per week, stable output | 2 hours concentrated on weekends |
- | Low Frequency Low Intensity | 2-3 times per week, low output | 1 hour on weekends |
- | Low Frequency Extreme Intensity | 1-2 times per week, but extremely high output | 4-6 hours concentrated on weekends |
- | Trauma Experience Type | Moderate | 1 | Community Validation | Protect Privacy |
- | Code Group | Structural Complexity | Constraint Quantity | Tool Complexity | Special Notes |
- | Code Group | Feedback Source | Iteration Count | Review Tool | Special Notes |
- | Social Need | Recommended Tool Combination | Accountability Method |
- | Medium | Standard Tool Combination | Small Writing Group |
- Execute workflow**: Follow the steps in Appendix A

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

- Workflow/theme: 100 Writer Profiles for Screenwriting Framework
- Workflow/theme: 📊 Complete File Overview Table
- Workflow/theme: 📈 Parameter Explanations and Usage Guide
- Workflow/theme: 🔧 Framework Adaptation Matrix
- Workflow/theme: 📊 Quick Query Index
- Workflow/theme: 🛠️ Tool Configuration Quick Reference
- Workflow/theme: 📋 Personalized Configuration Generator
- Workflow/theme: 📝 Usage Instructions

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
4. [ ] Read source: `C:/Project/va-agent-swarm/study/psychological_profile_agent_functional_specifications.md` and mirror under corpus if present.
5. [ ] Map FRs → existing agents/DNA (avoid duplicate agents).
6. [ ] Create feature branch `special/psychological_profile_agent`.
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

#### Sprint 1 — 100 Writer Profiles for Screenwriting Framework
- **Goal:** Implement/test the smallest slice that proves progress on «100 Writer Profiles for Screenwriting Framework» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/psychological_profile_agent_sprint1_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 2 — 📊 Complete File Overview Table
- **Goal:** Implement/test the smallest slice that proves progress on «📊 Complete File Overview Table» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/psychological_profile_agent_sprint2_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 3 — 📈 Parameter Explanations and Usage Guide
- **Goal:** Implement/test the smallest slice that proves progress on «📈 Parameter Explanations and Usage Guide» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/psychological_profile_agent_sprint3_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 4 — 🔧 Framework Adaptation Matrix
- **Goal:** Implement/test the smallest slice that proves progress on «🔧 Framework Adaptation Matrix» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/psychological_profile_agent_sprint4_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 5 — 📊 Quick Query Index
- **Goal:** Implement/test the smallest slice that proves progress on «📊 Quick Query Index» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/psychological_profile_agent_sprint5_notes.md` (optional) or this plan's risk log.
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

Suggested path: `backend/app/tests/unit/test_special_psychological_profile_agent.py`

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

This source: **500 lines** → plan capacity accordingly.

---

## Appendix A — Source heading index (full H2/H3 extract)

| Level | Heading |
|------:|---------|
| 1 | 100 Creator Psychological Profile Library |
| 2 | 100 Writer Profiles for Screenwriting Framework |
| 2 | 📊 Complete File Overview Table |
| 3 | Profiles 1-25: Introverted Creative Type |
| 3 | Profiles 26-50: Extroverted Social Type |
| 3 | Nos. 51-75: Trauma Experience Type |
| 3 | Profiles 76-100: Professional Transition Type |
| 2 | 📈 Parameter Explanations and Usage Guide |
| 3 | Field Definitions |
| 3 | Energy Mode Interpretation |
| 2 | 🔧 Framework Adaptation Matrix |
| 3 | Phase 1 (Motivation Exploration) Adaptation |
| 3 | Phase 2 (Audience Definition) Adaptation |
| 3 | Phase 3 (Method Design) Adaptation |
| 3 | Stage 4 (Emotional Design) Adaptation |
| 3 | Phase 5 (Execution and Creation) Adaptation |
| 3 | Stage 6 (Iterative Refinement) Adaptation |
| 2 | 📊 Quick Query Index |
| 3 | By MBTI Type |
| 3 | By Core Motivation |
| 3 | By Primary Fear |
| 3 | By Creative Style |
| 2 | 🛠️ Tool Configuration Quick Reference |
| 3 | Configure Based on Social Needs |
| 3 | Configure by Perfectionism Level |
| 3 | Energy Mode Configuration |
| 2 | 📋 Personalized Configuration Generator |
| 1 | profile_config_generator.py |
| 1 | 完整檔案數據（簡化示例） |
| 1 | ... 其他99個檔案 |
| 1 | 使用示例 |
| 1 | 生成 QINTV 的配置 |
| 1 | 導出到文件 |
| 2 | 📝 Usage Instructions |

---

## Appendix B — Traceability

| Artifact | Location |
|----------|----------|
| This plan | `planning/special/psychological_profile_agent.md` |
| Upstream study | `C:/Project/va-agent-swarm/study/psychological_profile_agent_functional_specifications.md` |
| Host pack | `business/video/` |
| Selection | `business/video/archetype_registry.json` |
| Command origin | `generate_special_skills.md` |

---

*End of plan — `psychological_profile_agent` — generated 2026-07-13*
