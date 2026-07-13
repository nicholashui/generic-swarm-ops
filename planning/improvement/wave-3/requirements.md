# Wave 3 Requirements — Learning, Coevolution & Quality on Video Tasks

**Wave:** 3  
**Source of truth:** `improvements.md` v1.0 § Wave 3  
**Cross-refs:** `adoption.md` v2.3 (N1/N2/N3, ALC, L0/L1/L2), `repo_compare.md`, Wave 0–2 exits under `planning/improvement/wave-{0,1,2}/`  
**Date:** 2026-07-12  
**Status:** Ready for design / implementation  

---

## 1. Goal of this wave

Prove **measurable autonomous improvement** on video-related tasks using ALC + sandbox evolution—**without** production DNA mutation or auto-promote:

1. **Multi-generation coevolution** experiment: planner genome × aesthetics/QC genome against video goldens (deterministic offline fitness).
2. **Lesson utility** scoring + reuse metrics exposed as API and ops-console panel.
3. **Skill sandbox** for video prompt skills (`domain=video` metadata; sandbox path only → explicit promote).
4. **Governance review** of learned artifacts (variants + skill proposals) for human sign-off lists—no auto-promote.
5. Expand evals with **LQR / consistency** rubrics under the video pack; corpus eval can load pack goldens when DNA domain is video.
6. Protect **E1**, inventory **114**, and Wave 1–2 ALC / spine paths.

**Out of scope (Wave 4+):** Multi-pack load tests, red-team tool misuse suite, third domain pack, full roster activation (Wave 5), real Sora/Veo providers, advanced timeline FE.

---

## 2. Non-negotiables (N1 / N2 / N3)

From `adoption.md` v2.3 §0 (quoted sense):

| # | Requirement |
|---|-------------|
| **N1** | **va-agent-swarm** keeps **all** video agent-specific business logic; every agent must gain **mandatory autonomous learning** (individual knowledge growth). Video logic lives only under domain pack paths (`business/video/` …). Every registered agent must implement the **Agent Learning Contract** (ALC) or fail activation. |
| **N2** | **generic-swarm-ops** becomes a **universal foundation** for dozens of multi-agent (MMA) systems beyond video. Introduce **Domain Pack** interface, schemas, registration hooks, and isolation so any `business/<domain>/` onboard is config + artifacts, not a fork of the runtime. |
| **N3** | **Adopt ALL agents and ALL business processes from va-agent-swarm** into the generic project — from **orchestrator / planner / meta-agents down through every specialist and workflow-support agent**. **No agent may be dropped.** Inventory CI remains enforced for video pack presence. |

**Wave 3 enforcement:**

- **N1:** Coevolution genomes and skill proposals bind to `agent_id` / pack domain; video LQR fixtures live under `business/video/`; agents learn via ALC utility metrics, not hard-coded video rules in core.
- **N2:** Coevolution, lesson utility, and governance-review APIs are domain-agnostic (`domain_id` / `agent_id` parameters); host remains universal.
- **N3:** No agent deletion; inventory still PASS 114; roster files untouched except optional process/docs notes.

**Additional hard constraint:** Evolution remains **`sandbox_only`**; never auto-promote learned artifacts to production DNA or production skills.

---

## 3. Functional requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-W3-01 | Runtime + API: run multi-generation **coevolution experiment** (default ≥2 generations) producing sandbox variants with fitness and audit trail. | P0 |
| FR-W3-02 | Coevolution pairs **planner genome** × **aesthetics/QC genome** (agent_ids e.g. `video.planner` × `video.aiqaconsistency` or equivalent pack ids) against video-related DNA / goldens. | P0 |
| FR-W3-03 | Fitness includes suite metrics **plus** ALC enrichment: `knowledge_growth` / `lesson_reuse` (normalized) when agent_id / lessons available. Composite fitness recorded per variant/generation. | P0 |
| FR-W3-04 | Next generation seeds from elite genomes (sandbox mutation only); production workflows collection never overwritten by coevolution. | P0 |
| FR-W3-05 | **Lesson utility dashboard** API: ranked lessons by utility, reuse/wins, optional filter by `agent_id` / domain. | P0 |
| FR-W3-06 | **Video skill sandbox** propose path: skill_name may be video-prefixed; optional `domain=video` metadata; writes under `skills/_sandbox`; promote remains explicit admin path. | P0 |
| FR-W3-07 | **Governance review** API: list pending learned artifacts (sandbox variants + skill proposals) with status for human sign-off. Does not promote. | P0 |
| FR-W3-08 | Structure: **LQR / consistency** golden eval fixture(s) under `business/video/evals/` (+ optional rubric markdown). | P0 |
| FR-W3-09 | Corpus eval optionally loads **video pack goldens** when DNA `domain` is `video` (or target matches video DNA ids). | P0 |
| FR-W3-10 | Unit tests: coevolution runs ≥2 gens; variants audited; fitness metrics present; utility dashboard non-empty when lessons seeded; skill propose sandbox path; governance lists pending; no production DNA mutation. | P0 |
| FR-W3-11 | Measurable improvement: ≥1 fitness metric improves across generations **or** experiment records comparable elite fitness with full audit (deterministic offline). | P0 |
| FR-W3-12 | FE: lesson utility summary panel (evolution page or adjacent) showing top lessons / reuse metrics. | P1 |
| FR-W3-13 | Docs: domain-packs (or self-improvement) note coevolution + utility + governance review surfaces. | P1 |

---

## 4. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR-W3-01 | All evolution / coevolution remains `sandbox_only` until explicit canary/promote. |
| NFR-W3-02 | No production workflow DNA silent overwrite; no auto_promote true path. |
| NFR-W3-03 | Deterministic offline evaluation (no external LLM required for unit tests). |
| NFR-W3-04 | Full backend unit suite green; inventory CI PASS 114. |
| NFR-W3-05 | E1 operator path and Wave 1–2 ALC/spine tests remain green. |
| NFR-W3-06 | Coevolution APIs accept generic domain/agent ids (N2); video is the proving pack only. |
| NFR-W3-07 | FE typecheck/lint not broken if FE touched. |

---

## 5. Success / acceptance criteria

| Gate | Pass condition |
|------|----------------|
| AC-1 | Coevolution experiment returns `generations >= 2`; each generation has evaluated variants; audit events recorded |
| AC-2 | `fitness_metrics` include `suite_pass_rate` and ALC fields (`lesson_reuse` / `knowledge_growth` or composite including them) when lessons/genomes present |
| AC-3 | Lesson utility API returns ranked lessons (utility descending) |
| AC-4 | Video skill propose writes under `business/distilled/skills/_sandbox` (or equivalent sandbox path); `sandbox_only: true` |
| AC-5 | Governance review lists sandbox variants and/or skill proposals with pending status; does not change promote state |
| AC-6 | LQR/consistency golden exists under `business/video/evals/`; video DNA eval path can reference pack goldens |
| AC-7 | Unit: `test_wave3_coevolution` (or equivalent) green; no production workflow version mutation during experiment |
| AC-8 | Inventory PASS count=114; full unit suite green |
| AC-9 | FE lesson utility panel renders (demo or API) without typecheck break |
| AC-10 | Completion report under `planning/improvement/wave-3/` with evidence |

---

## 6. Traceability

| Item | Source |
|------|--------|
| Multi-gen sandbox coevolution | improvements.md Wave 3 tasks; adoption.md ALC / evolution sandbox |
| Lesson utility + reuse dashboard | improvements.md Wave 3; Wave 1 metrics foundation |
| Skill sandbox video prompts | improvements.md Wave 3; existing `propose_skill_sandbox` |
| Governance of learned artifacts | improvements.md Wave 3; adoption.md governance |
| LQR/consistency evals | improvements.md Wave 3; va LQR process family |
| Fitness quality + growth/reuse | improvements.md Wave 3 acceptance |
| Sandbox discipline | adoption.md evolution; N1/N2 |
| Full roster / inventory | N3; Wave 0–2 inventory gate |
| Spine DNA + goldens baseline | Wave 2 exit |

---

## 7. Structure / Backend / Frontend requirements

### 7.1 Structure

| ID | Requirement |
|----|-------------|
| ST-W3-01 | Add LQR/consistency golden JSON under `business/video/evals/golden/` with rubrics and provenance. |
| ST-W3-02 | Optional rubric markdown under `business/video/evals/rubrics/`. |
| ST-W3-03 | SDD + completion artifacts under `planning/improvement/wave-3/`. |
| ST-W3-04 | Docs note for coevolution / utility / governance (e.g. `docs/domain-packs.md`). |
| ST-W3-05 | Do not remove or shrink roster, MAP, or inventory agents. |

### 7.2 Backend

| ID | Requirement |
|----|-------------|
| BE-W3-01 | `coevolution` module + `RuntimeServices.run_coevolution_experiment`. |
| BE-W3-02 | Enrich sandbox fitness with ALC metrics when agent genomes / lessons apply. |
| BE-W3-03 | `lesson_utility_dashboard` (+ route under improvement). |
| BE-W3-04 | `governance_review_learned_artifacts` (+ route under evolution or improvement). |
| BE-W3-05 | Corpus eval loads video pack eval paths for domain=video DNA. |
| BE-W3-06 | Skill propose continues sandbox-only; tests cover video skill name/domain metadata. |
| BE-W3-07 | Unit tests for coevolution, utility, governance, corpus video path, no production mutation. |

### 7.3 Frontend

| ID | Requirement |
|----|-------------|
| FE-W3-01 | Lesson utility panel component (top lessons, reuse/growth summary). |
| FE-W3-02 | Mount on evolution (or improvement-adjacent) ops console surface. |
| FE-W3-03 | Demo-mode fallback when API unavailable. |
| FE-W3-04 | API client helpers if needed for new endpoints. |

---

## 8. Risks & constraints

| Risk | Mitigation |
|------|------------|
| Fitness “improvement” flaky offline | Deterministic rule-based fitness; assert generation records + non-decreasing elite composite when lessons accumulate, **or** explicit comparable fitness with audit |
| Auto-promote temptation | `auto_promote` always false; governance review is list-only |
| Video logic leaking into host | Coevolution params are generic; video fixtures stay in pack |
| Corpus noise from unrelated goldens | Pack path load gated by DNA domain / target match |
| Breaking E1 / spine | Regression via full unit suite + inventory CI |
| FE scope creep | P1 panel only; no timeline editor |

**Constraint:** Prefer reusing `propose_evolution_variant`, `sandbox_evaluate_variant`, `propose_skill_sandbox`, `improvement_metrics`, and `LessonLibrary` utility ranking over inventing parallel systems.

---

## 9. Internal critic (Phase 1)

| Question | Answer |
|----------|--------|
| Does this ship measurable learning without prod mutation? | Yes — multi-gen sandbox + fitness + audit. |
| N1 isolation? | Video goldens/skills in pack; agents via agent_id. |
| N2 universal host? | APIs domain-agnostic. |
| N3 roster? | Inventory untouched. |
| Wave 4 bleed? | Load/security/third pack deferred. |

*End Phase 1 — Requirements.*
