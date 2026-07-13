# Special skill adoption plan — `screenwriter_strategic_goal_achievement_agent`

| Field | Value |
|-------|-------|
| **Skill id** | `screenwriter_strategic_goal_achievement_agent` |
| **Source** | `C:/Project/va-agent-swarm/study/screenwriter_strategic_goal_achievement_agent_functional_specification.md` |
| **In-pack corpus mirror** | `business/video/corpus/study/screenwriter_strategic_goal_achievement_agent_functional_specification.md` (if present under video corpus) |
| **Source size** | 1600 lines / 58,999 chars / ~10 table rows detected |
| **Host product** | generic-swarm-ops |
| **Plan type** | Spec-driven development (SDD) learning + adoption execution |
| **Generated** | 2026-07-13 |
| **Generator** | `scripts/business/generate_special_skills_plans.py` via `generate_special_skills.md` |

## Host integration stance (N1/N2/N3)

Strategic goal loops → beat sheets + showrunner gates; ALC lessons on rewrites.

| Kind | Guidance |
|------|----------|
| **Domain Pack agents** | Prefer existing `video.*` agents below; create new pack agent only if roster gap is real |
| **Workflow DNA** | Extend/index DNA under `business/video/workflows/`; entry via `video.orchestrator` / `video.planner` |
| **Host core** | Reuse runtime, ALC, knowledge, LLM adapters — do not rebuild a second control plane |
| **Selection** | When production-type relevant, use `business/video/archetype_registry.json` + recommend-workflow API |

**Candidate pack agents:**
- video.screenwriter
- video.narrativearc
- video.showrunner
- video.director

**Candidate DNA:**
- wf_video_arch_e_ai_short_film_v1
- wf_video_arch_j_feature_film_v1

**Candidate runtime tools (allow-listed / stubs):**
- video_script_format
- audit_log_writer

---

## 1. Source Document Review & Requirement Extraction

### 1.1 Source outline (headings extracted)

**H2 sections:**
- Strategic Goal Achievement Framework Practical Demonstration: "Screenwriting" In-Depth Exploration
- Framework in Action: From Vague Ideas to Clear Actions
- Transformation Results: From Vague to Clear Complete Metamorphosis
- Open-Source Framework Implementation Guide
- Learning Points and Application Guide
- Practical Exercise: Apply Framework Immediately
- Goal: [Your goal]
- Root Motivation: [Core motivation discovered]
- Open Source Framework Ecosystem Integration
- Framework Implementation Success Factors
- Complete Screenwriting Workflow with Open Source Frameworks
- 📋 Workflow Overview
- 🎬 Stage 1: Motive Exploration and Story Seed (Week 1)
- Today's Triggers
- Five Whys Deep Dive
- Story Seed
- 🎯 Stage 2: Audience Definition and Persona Profiles (Week 2)
- ⚙️ Stage 3: Structure Design and Method Selection (Week 3)
- 💭 Stage 4: Emotional Design and Theme Deepening (Week 4)
- ✍️ Stage 5: Execute Creation (Weeks 5-12)

**Selected H3 sections:**
- **Stage 1: Motivation and Purpose** — Why Pursue Screenwriting?
- **Stage 2: Audience and Context** — For Whom Are We Writing?
- **Stage 3: Methods and Constraints** — How to Write It? What Are the Limitations?
- **Stage 4: Emotional Expectations** — What Do I Want to Feel?
- **Stage 5: Execution and Impact** — What reactions do I want from the audience?
- **Stage 6: Iteration and Reflection** — How do I actually do it?
- 🔧 **Phase 1: Motivation Mining Framework Combination**
- 🎯 **Phase 2: Audience Analysis Framework Combination**
- ⚙️ **Phase 3: Method Design Framework Combination**
- 💭 **Stage 4: Emotional Design Framework Combination**
- 📊 **Phase 5: Impact Measurement Framework Combination**
- 🚀 **Phase 6: Execution Management Framework Integration**
- 🔍 **Motivation Diagnosis Toolkit**
- 👥 **Audience Analysis Toolkit**
- ⚡ **Action Planning Toolkit**

### 1.2 Functional requirements (extracted / paraphrased from source language)

The following items were mined via keyword heuristics (must/shall/metric/workflow/gate/…) and structural scan. Treat them as a **backlog seed** — refine against full line-by-line human review of the source.

- Further Question:** "Heal myself" — What do I want to heal? Is it childhood trauma? The pain of heartbreak? Anger at the world? Please vividly describe a specific event or experience that made me realize "I must write screenplays."
- Must Have:** Emotional authenticity, character depth
- Should Have:** Innovative structure, visual impact
- Question:** What limitations must I adhere to? Why can't these limitations be broken?
- Problem Diagnosis:** The expected impact is too vague, lacking observable success metrics, making it hard to evaluate effectiveness.
- Question:** What reactions will tell me "it's a success"?
- ✅ **Observability** - Specific success metrics
- Time Required:** 30 minutes
- Method Level:** From "non-linear narrative" → "philosophical expression simulating memory fragments"
- I hope they think "I'm not alone in thinking this" after watching, then proactively talk with friends, be gentler to strangers. If someone messages "This character is me," I'll know it's a success.
- [Kanban Board System](https://github.com/kanban-tools/board) - Visualized Workflow
- Use Kanban to visualize workflow
- Every insight must have corresponding specific actions
- Set observable success metrics
- Exercise 1: Open-Source Tool Quick Diagnosis**
- Use the following open-source tool combination to diagnose your goal:
- Tool:** [Five Whys Digital Template](https://github.com/lean-startup-circle/five-whys/blob/main/templates/digital-five-whys.md)
- Tool:** [Empathy Map Canvas](https://github.com/designthinkingtools/empathy-map/blob/main/canvas-template.json)
- Tool:** [GTD Next Action Template](https://github.com/gtd-methodology/gtd-tools/blob/main/next-action-template.md)
- Context**: @[Environment/Tool requirements]
- Energy**: [Required energy level: High/Medium/Low]
- Success Criteria**: [Success criteria]
- Tool:** [OKR Tracking Sheet](https://github.com/7geese/okr-framework/blob/main/templates/okr-template.csv)
- Tool:** [Motivation Archaeology Toolkit](https://github.com/motivation-tools/archaeology)
- Tool:** [Persona Builder CLI](https://github.com/uxtools/persona-cli)

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

- Workflow/theme: Strategic Goal Achievement Framework Practical Demonstration: "Screenwriting" In-Depth Exploration
- Workflow/theme: Framework in Action: From Vague Ideas to Clear Actions
- Workflow/theme: Transformation Results: From Vague to Clear Complete Metamorphosis
- Workflow/theme: Open-Source Framework Implementation Guide
- Workflow/theme: Learning Points and Application Guide
- Workflow/theme: Practical Exercise: Apply Framework Immediately
- Workflow/theme: Goal: [Your goal]
- Workflow/theme: Root Motivation: [Core motivation discovered]
- Workflow/theme: Open Source Framework Ecosystem Integration
- Workflow/theme: Framework Implementation Success Factors

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
4. [ ] Read source: `C:/Project/va-agent-swarm/study/screenwriter_strategic_goal_achievement_agent_functional_specification.md` and mirror under corpus if present.
5. [ ] Map FRs → existing agents/DNA (avoid duplicate agents).
6. [ ] Create feature branch `special/screenwriter_strategic_goal_achievement_agent`.
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

#### Sprint 1 — Strategic Goal Achievement Framework Practical Demonstration: "Screenwriting" In-Depth Exploration
- **Goal:** Implement/test the smallest slice that proves progress on «Strategic Goal Achievement Framework Practical Demonstration: "Screenwriting" In-Depth Exploration» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/screenwriter_strategic_goal_achievement_agent_sprint1_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 2 — Framework in Action: From Vague Ideas to Clear Actions
- **Goal:** Implement/test the smallest slice that proves progress on «Framework in Action: From Vague Ideas to Clear Actions» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/screenwriter_strategic_goal_achievement_agent_sprint2_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 3 — Transformation Results: From Vague to Clear Complete Metamorphosis
- **Goal:** Implement/test the smallest slice that proves progress on «Transformation Results: From Vague to Clear Complete Metamorphosis» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/screenwriter_strategic_goal_achievement_agent_sprint3_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 4 — Open-Source Framework Implementation Guide
- **Goal:** Implement/test the smallest slice that proves progress on «Open-Source Framework Implementation Guide» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/screenwriter_strategic_goal_achievement_agent_sprint4_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
#### Sprint 5 — Learning Points and Application Guide
- **Goal:** Implement/test the smallest slice that proves progress on «Learning Points and Application Guide» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/screenwriter_strategic_goal_achievement_agent_sprint5_notes.md` (optional) or this plan's risk log.
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

Suggested path: `backend/app/tests/unit/test_special_screenwriter_strategic_goal_achievement_agent.py`

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

This source: **1600 lines** → plan capacity accordingly.

---

## Appendix A — Source heading index (full H2/H3 extract)

| Level | Heading |
|------:|---------|
| 2 | Strategic Goal Achievement Framework Practical Demonstration: "Screenwriting" In-Depth Exploration |
| 2 | Framework in Action: From Vague Ideas to Clear Actions |
| 3 | **Stage 1: Motivation and Purpose** — Why Pursue Screenwriting? |
| 3 | **Stage 2: Audience and Context** — For Whom Are We Writing? |
| 3 | **Stage 3: Methods and Constraints** — How to Write It? What Are the Limitations? |
| 3 | **Stage 4: Emotional Expectations** — What Do I Want to Feel? |
| 3 | **Stage 5: Execution and Impact** — What reactions do I want from the audience? |
| 3 | **Stage 6: Iteration and Reflection** — How do I actually do it? |
| 2 | Transformation Results: From Vague to Clear Complete Metamorphosis |
| 2 | Open-Source Framework Implementation Guide |
| 3 | 🔧 **Phase 1: Motivation Mining Framework Combination** |
| 3 | 🎯 **Phase 2: Audience Analysis Framework Combination** |
| 3 | ⚙️ **Phase 3: Method Design Framework Combination** |
| 3 | 💭 **Stage 4: Emotional Design Framework Combination** |
| 3 | 📊 **Phase 5: Impact Measurement Framework Combination** |
| 3 | 🚀 **Phase 6: Execution Management Framework Integration** |
| 2 | Learning Points and Application Guide |
| 2 | Practical Exercise: Apply Framework Immediately |
| 3 | 🔍 **Motivation Diagnosis Toolkit** |
| 1 | Five Whys Analysis |
| 2 | Goal: [Your goal] |
| 2 | Root Motivation: [Core motivation discovered] |
| 3 | 👥 **Audience Analysis Toolkit** |
| 3 | ⚡ **Action Planning Toolkit** |
| 1 | Next Action Definition |
| 3 | 📊 **Progress Tracking Toolkit** |
| 3 | ⏰ **Time Allocation and Tool Usage** |
| 1 | Install the tool |
| 1 | Quickly generate user personas |
| 1 | Python script for quick planning |
| 1 | Break down tasks |
| 1 | Set priorities |
| 1 | Create time blocks |
| 3 | 🤖 **Automated Assessment Tool** |
| 1 | Clone the assessment tool |
| 1 | Install dependencies |
| 1 | Run assessment |
| 1 | Assessment configuration file config.yaml |
| 3 | 📈 **Advanced Analysis Tools** |
| 3 | 🛡️ **Obstacle Prediction Engine** |
| 1 | Install the prediction engine |
| 1 | Configure personal profile |
| 1 | Initialize analyzer |
| 1 | Input goal information |
| 1 | Predict obstacles |
| 1 | Generate coping strategies |
| 3 | 🎯 **Scenario Simulation Training** |
| 1 | Create obstacle scenarios |
| 1 | Conduct simulation training |
| 3 | 💪 **Resilience Building** |
| 1 | 基於個人特質生成鼓勵語句 |
| 1 | 生成個人化鼓勵語句 |
| 2 | Open Source Framework Ecosystem Integration |
| 3 | 🔄 **Continuous Improvement Loop** |
| 1 | 建立改進循環 |
| 1 | 自動收集進度數據 |
| 1 | 生成改進洞察 |
| 3 | 📱 **Mobile Integration Tool** |
| 3 | 🤝 **Community Collaboration Platform** |
| 1 | Find accountability partner |
| 1 | Crowdsourced solutions |
| 3 | 🔮 **AI Prediction and Optimization** |
| 1 | Train personalized prediction model |
| 1 | Input historical data |
| 1 | Predict current goal success probability |
| 1 | Optimization strategy suggestions |
| 3 | 📊 **Data Visualization Dashboard** |
| 3 | 🎓 **Learning Path Recommendations** |
| 1 | 分析技能差距 |
| 1 | 推薦學習路徑 |
| 2 | Framework Implementation Success Factors |
| 3 | ✅ **Successful Implementation Checklist** |
| 3 | 🚨 **Common Implementation Pitfalls** |
| 3 | 🎯 **Best Practice Recommendations** |
| 1 | Appendix A: Complete Screenwriting Workflow |
| 2 | Complete Screenwriting Workflow with Open Source Frameworks |
| 2 | 📋 Workflow Overview |
| 2 | 🎬 Stage 1: Motive Exploration and Story Seed (Week 1) |
| 3 | Goal |
| 3 | Open Source Tool Combination |
| 1 | Install Obsidian (cross-platform) |
| 1 | Windows: Download https://obsidian.md/download |
| 1 | Or use Scoop |
| 1 | Create screenplay project repository |
| 1 | Motivation Exploration Journal Template |
| 2 | Today's Triggers |
| 2 | Five Whys Deep Dive |
| 2 | Story Seed |
| 1 | Install Logseq |
| 1 | Windows |
| 1 | Or download AppImage (Linux) |
| 1 | 情感強度追蹤腳本 |
| 1 | emotion_tracker.py |
| 1 | 使用示例 |
| 1 | Emotion intensity tracking script |
| 3 | Stage 1 Deliverables |
| 2 | 🎯 Stage 2: Audience Definition and Persona Profiles (Week 2) |
| 3 | Goal |
| 3 | Open Source Tool Combination |
| 1 | Run Excalidraw locally |
| 3 | Stage 2 Deliverables |
| 2 | ⚙️ Stage 3: Structure Design and Method Selection (Week 3) |
| 3 | Objective |
| 3 | Open Source Tool Combination |
| 1 | Linux installation |
| 1 | Windows - Download installer |
| 1 | https://github.com/trelby/trelby/releases |
| 3 | Stage 3 Deliverables |
| 2 | 💭 Stage 4: Emotional Design and Theme Deepening (Week 4) |
| 3 | Objective |
| 3 | Open Source Tool Combination |
| 1 | Install Manuskript |
| 1 | or |
| 1 | Emotion curve data |
| 3 | Stage 4 Deliverables |
| 2 | ✍️ Stage 5: Execute Creation (Weeks 5-12) |
| 3 | Goal |
| 3 | Open Source Tool Combination |
| 1 | Install editor with Fountain syntax support |
| 1 | VS Code extension |
| 1 | writing_tracker.py |
| 1 | Usage example |
| 3 | Stage 5 Deliverables |
| 2 | 🔄 Stage 6: Iteration and Refinement (Weeks 13-16) |
| 3 | Goal |
| 3 | Open Source Tool Combination |
| 1 | Install LanguageTool |
| 1 | Docker method |
| 1 | Install Afterwriting CLI |
| 1 | Convert Fountain to PDF |
| 3 | Stage 6 Deliverables |
| 2 | 📊 Complete Tool List |
| 3 | Essential Tools (Free and Open Source) |

---

## Appendix B — Traceability

| Artifact | Location |
|----------|----------|
| This plan | `planning/special/screenwriter_strategic_goal_achievement_agent.md` |
| Upstream study | `C:/Project/va-agent-swarm/study/screenwriter_strategic_goal_achievement_agent_functional_specification.md` |
| Host pack | `business/video/` |
| Selection | `business/video/archetype_registry.json` |
| Command origin | `generate_special_skills.md` |

---

*End of plan — `screenwriter_strategic_goal_achievement_agent` — generated 2026-07-13*
