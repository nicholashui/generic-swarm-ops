#!/usr/bin/env python3
"""Execute generate_special_skills.md — emit planning/special/<skill>.md SDD plans.

Reads listed study MD files from va-agent-swarm/study and writes formal
spec-driven adoption/execution plans into planning/special/.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY = Path(r"C:\Project\va-agent-swarm\study")
OUT = ROOT / "planning" / "special"
TODAY = date.today().isoformat()

SOURCES = [
    "aesthetics_agent_functional_specification.md",
    "agent_loop_v3.md",
    "agentic_rag_functional_specification.md",
    "coding_agent_functional_specification.md",
    "complex_problem_solution_process_model.md",
    "general_creative_agent_functional_specification.md",
    "intent_analysis_agent_functional_specification.md",
    "knowledge_router_agent.md",
    "lifes_quiet_redemption_agent_workflow.md",
    "llm_usage_functional_specification.md",
    "optimization_agent_functional_specification.md",
    "podcast_agent_functional_specifcation.md",
    "psychological_profile_agent_functional_specifications.md",
    "research_agent_functional_specification.md",
    "screenwriter_strategic_goal_achievement_agent_functional_specification.md",
    "thinking_model.md",
    "video_generation_techology_should_learn_now.md",
]


def skill_name(filename: str) -> str:
    base = filename[:-3] if filename.endswith(".md") else filename
    for suffix in (
        "_functional_specifications",
        "_functional_specification",
        "_functional_specifcation",  # upstream typo
    ):
        if base.endswith(suffix):
            return base[: -len(suffix)]
    return base


def extract_structure(text: str) -> dict:
    lines = text.splitlines()
    headings: list[tuple[int, str]] = []
    bullets: list[str] = []
    tables = 0
    for ln in lines:
        m = re.match(r"^(#{1,4})\s+(.+)$", ln.strip())
        if m:
            headings.append((len(m.group(1)), m.group(2).strip()))
        if re.match(r"^\s*[-*+]\s+\S", ln) or re.match(r"^\s*\d+\.\s+\S", ln):
            bullets.append(ln.strip()[:240])
        if ln.strip().startswith("|") and "---" not in ln:
            tables += 1
    # candidate requirement-ish lines
    req_kw = re.compile(
        r"\b(must|shall|should|require|required|constraint|metric|SLA|KPI|gate|workflow|"
        r"input|output|acceptance|success|non-functional|security|privacy|latency|"
        r"accuracy|rubric|agent|tool|API|memory|eval)\b",
        re.I,
    )
    req_lines = []
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#") or s.startswith("```"):
            continue
        if req_kw.search(s) and 20 <= len(s) <= 280:
            req_lines.append(s.lstrip("-*0123456789. ").strip())
    # dedupe preserve order
    seen = set()
    req_u = []
    for r in req_lines:
        k = r.lower()
        if k not in seen:
            seen.add(k)
            req_u.append(r)
    title = headings[0][1] if headings else skill_name("x.md")
    h2 = [h for lvl, h in headings if lvl == 2][:40]
    h3 = [h for lvl, h in headings if lvl == 3][:40]
    return {
        "title": title,
        "headings": headings,
        "h2": h2,
        "h3": h3,
        "bullets": bullets[:80],
        "tables": tables,
        "req_lines": req_u[:60],
        "chars": len(text),
        "lines": len(lines),
    }


# Host-aware integration hints by skill family
HOST_HINTS: dict[str, dict] = {
    "aesthetics_agent": {
        "pack_agents": ["video.conceptartist", "video.styletransfer", "video.colorist", "video.moodboard"],
        "dna": ["wf_video_arch_e_ai_short_film_v1", "wf_video_spine_v1"],
        "tools": ["video_media_gen_stub", "audit_log_writer"],
        "notes": "Maps to visual look/style consistency in video Domain Pack; do not fork control plane.",
    },
    "agent_loop_v3": {
        "pack_agents": ["video.orchestrator", "video.planner", "video.memory", "video.judge"],
        "dna": ["wf_video_spine_v1"],
        "tools": ["audit_log_writer"],
        "notes": "Aligns with host Workflow DNA + ALC reflect hooks; Cynefin/AAR map to gates not new runtime.",
    },
    "agentic_rag": {
        "pack_agents": ["video.webresearch", "video.archiveresearch", "video.citation", "video.memory"],
        "dna": ["wf_video_spine_v1"],
        "tools": ["audit_log_writer"],
        "notes": "Host knowledge/retrieval services under backend/app; domain corpora in business/video/corpus.",
    },
    "coding_agent": {
        "pack_agents": [],
        "dna": [],
        "tools": ["audit_log_writer"],
        "notes": "Host engineering capability — prefer skills/hooks; keep out of video business logic (N1).",
    },
    "complex_problem_solution_process_model": {
        "pack_agents": ["video.planner", "video.orchestrator", "video.judge"],
        "dna": ["wf_video_spine_v1", "wf_video_production_e2e_v1"],
        "tools": ["audit_log_writer"],
        "notes": "Process model informs Planner decomposition + Gatekeeper criteria.",
    },
    "general_creative_agent": {
        "pack_agents": ["video.ideation", "video.creativedirector", "video.novelty", "video.director"],
        "dna": ["wf_video_arch_a_viral_hook_v1", "wf_video_arch_e_ai_short_film_v1"],
        "tools": ["video_script_format", "audit_log_writer"],
        "notes": "Specialize via craft agents rather than one mega creative agent.",
    },
    "intent_analysis_agent": {
        "pack_agents": ["video.planner", "video.router"],
        "dna": ["wf_video_spine_v1"],
        "tools": ["audit_log_writer"],
        "notes": "Feeds archetype_registry selection (recommend-workflow) + planner brief parse.",
    },
    "knowledge_router_agent": {
        "pack_agents": ["video.router", "video.memory", "video.webresearch"],
        "dna": ["wf_video_spine_v1"],
        "tools": ["audit_log_writer"],
        "notes": "Maps to router_table.json + knowledge retrieval scopes; no parallel bus.",
    },
    "lifes_quiet_redemption_agent_workflow": {
        "pack_agents": [
            "video.director",
            "video.screenwriter",
            "video.promptengineer",
            "video.aiqaconsistency",
            "video.editor",
        ],
        "dna": ["wf_video_arch_e_ai_short_film_v1", "wf_video_lqr_overview_v1"],
        "tools": ["video_media_gen_stub", "video_qc_stub", "video_script_format"],
        "notes": "Worked example for archetype E / LQR family; deepen DNA from LQR SVGs.",
    },
    "llm_usage": {
        "pack_agents": ["video.costoptimizer", "video.latencyoptimizer", "video.router"],
        "dna": [],
        "tools": [],
        "notes": "Host LLM providers under backend/app/infrastructure/llm; policy not domain fork.",
    },
    "optimization_agent": {
        "pack_agents": [
            "video.promptoptimizer",
            "video.costoptimizer",
            "video.retentionoptimizer",
            "video.roasoptimizer",
            "video.evaluationharness",
        ],
        "dna": ["wf_video_arch_b_ugc_ad_v1"],
        "tools": ["audit_log_writer", "video_qc_stub"],
        "notes": "Optimization family already in roster 73–80; wire eval harness + lessons.",
    },
    "podcast_agent": {
        "pack_agents": ["video.voiceover", "video.sounddesign", "video.soundmixer", "video.composer"],
        "dna": ["wf_video_arch_h_ai_avatar_v1"],
        "tools": ["video_media_gen_stub", "audit_log_writer"],
        "notes": "Audio-first vertical; may share H avatar/talking-head patterns.",
    },
    "psychological_profile_agent": {
        "pack_agents": ["video.audiencesim", "video.emotionalarc", "video.retentionoptimizer"],
        "dna": ["wf_video_arch_a_viral_hook_v1", "wf_video_arch_b_ugc_ad_v1"],
        "tools": ["audit_log_writer"],
        "notes": "Audience/persona signals for retention; privacy/HiTL for sensitive profiling.",
    },
    "research_agent": {
        "pack_agents": [
            "video.webresearch",
            "video.archiveresearch",
            "video.factchecker",
            "video.citation",
            "video.benchmarkresearch",
        ],
        "dna": ["wf_video_arch_i_documentary_v1", "wf_video_spine_v1"],
        "tools": ["audit_log_writer"],
        "notes": "Research family 66–72; integrate corpus + source grading.",
    },
    "screenwriter_strategic_goal_achievement_agent": {
        "pack_agents": ["video.screenwriter", "video.narrativearc", "video.showrunner", "video.director"],
        "dna": ["wf_video_arch_e_ai_short_film_v1", "wf_video_arch_j_feature_film_v1"],
        "tools": ["video_script_format", "audit_log_writer"],
        "notes": "Strategic goal loops → beat sheets + showrunner gates; ALC lessons on rewrites.",
    },
    "thinking_model": {
        "pack_agents": ["video.orchestrator", "video.planner", "video.judge", "video.safetyredteam"],
        "dna": ["wf_video_spine_v1"],
        "tools": ["audit_log_writer"],
        "notes": "Cognitive frameworks (Cynefin, premortem, AAR) configure loop intensity — not new agents.",
    },
    "video_generation_techology_should_learn_now": {
        "pack_agents": ["video.promptengineer", "video.benchmarkresearch", "video.evaluationharness"],
        "dna": ["wf_video_spine_v1", "wf_video_arch_e_ai_short_film_v1"],
        "tools": ["video_media_gen_stub", "video_qc_stub"],
        "notes": "Technology radar for gen-video; keep vendor names design-time only until allow-listed.",
    },
}


def fmt_list(items: list[str], empty: str = "_None specified in automated extract._") -> str:
    if not items:
        return empty
    return "\n".join(f"- {x}" for x in items)


def build_plan(filename: str, text: str) -> str:
    skill = skill_name(filename)
    meta = extract_structure(text)
    hints = HOST_HINTS.get(
        skill,
        {
            "pack_agents": ["video.orchestrator", "video.planner"],
            "dna": ["wf_video_spine_v1"],
            "tools": ["audit_log_writer"],
            "notes": "Integrate via video Domain Pack + host runtime only (N1).",
        },
    )
    src_rel = f"C:/Project/va-agent-swarm/study/{filename}"
    corpus_mirror = f"business/video/corpus/study/{filename}"
    reqs = meta["req_lines"][:25]
    h2 = meta["h2"][:20]
    h3 = meta["h3"][:15]

    gaps = [
        "Source is research/spec prose, not host API contracts — map each FR to generic-swarm-ops Workflow DNA + agent_spec before coding.",
        "Vendor/model names in source are design-time only; runtime tools must stay on host allow-list / video_* stubs until approved.",
        "Success metrics may lack numeric thresholds; define measurable acceptance criteria in sprint 0.",
        "HiTL, consent, and risk_tier must be set per host governance (no auto-promote).",
        "Confirm whether capability is a new agent, a skill, a DNA extension, or host infrastructure (N1 isolation).",
    ]

    fr_section = fmt_list(reqs) if reqs else fmt_list(
        [f"See source section: {h}" for h in h2[:12]]
    )

    sprints = []
    themes = h2[:6] if h2 else [
        "Foundations & contracts",
        "Core workflow wiring",
        "Quality gates & critique",
        "Evals & hardening",
        "Staging integration",
        "Canary readiness",
    ]
    while len(themes) < 4:
        themes.append(f"Extension phase {len(themes)+1}")
    for i, theme in enumerate(themes[:5], 1):
        sprints.append(
            f"""#### Sprint {i} — {theme}
- **Goal:** Implement/test the smallest slice that proves progress on «{theme}» from the source outline.
- **Work:**
  - Map theme to pack artifacts (`agent_spec.json`, SPEC.md, DNA step, or host service).
  - Implement behind feature flag / sandbox; no production_ready until gates pass.
  - Add/extend unit tests for the slice.
- **Spec checkpoint:** Diff behavior vs source headings related to this theme; log gaps in `planning/special/{skill}_sprint{i}_notes.md` (optional) or this plan's risk log.
- **Exit:** Automated tests green + checklist of covered source requirements updated.
"""
        )

    pack_agents = fmt_list(hints.get("pack_agents") or [])
    dnas = fmt_list(hints.get("dna") or [])
    tools = fmt_list(hints.get("tools") or [])

    heading_rows = [
        f"| {lvl} | {h.replace('|', '/')} |"
        for lvl, h in meta["headings"]
        if lvl <= 3
    ]
    heading_table = "\n".join(heading_rows) if heading_rows else "| — | _No headings extracted_ |"
    if len(heading_table) > 12000:
        heading_table = heading_table[:12000] + "\n| … | _truncated_ |"

    return f"""# Special skill adoption plan — `{skill}`

| Field | Value |
|-------|-------|
| **Skill id** | `{skill}` |
| **Source** | `{src_rel}` |
| **In-pack corpus mirror** | `{corpus_mirror}` (if present under video corpus) |
| **Source size** | {meta['lines']} lines / {meta['chars']:,} chars / ~{meta['tables']} table rows detected |
| **Host product** | generic-swarm-ops |
| **Plan type** | Spec-driven development (SDD) learning + adoption execution |
| **Generated** | {TODAY} |
| **Generator** | `scripts/business/generate_special_skills_plans.py` via `generate_special_skills.md` |

## Host integration stance (N1/N2/N3)

{hints.get('notes', '')}

| Kind | Guidance |
|------|----------|
| **Domain Pack agents** | Prefer existing `video.*` agents below; create new pack agent only if roster gap is real |
| **Workflow DNA** | Extend/index DNA under `business/video/workflows/`; entry via `video.orchestrator` / `video.planner` |
| **Host core** | Reuse runtime, ALC, knowledge, LLM adapters — do not rebuild a second control plane |
| **Selection** | When production-type relevant, use `business/video/archetype_registry.json` + recommend-workflow API |

**Candidate pack agents:**
{pack_agents}

**Candidate DNA:**
{dnas}

**Candidate runtime tools (allow-listed / stubs):**
{tools}

---

## 1. Source Document Review & Requirement Extraction

### 1.1 Source outline (headings extracted)

**H2 sections:**
{fmt_list(h2)}

**Selected H3 sections:**
{fmt_list(h3) if h3 else "_No H3 headings extracted._"}

### 1.2 Functional requirements (extracted / paraphrased from source language)

The following items were mined via keyword heuristics (must/shall/metric/workflow/gate/…) and structural scan. Treat them as a **backlog seed** — refine against full line-by-line human review of the source.

{fr_section}

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

{fmt_list([f"Workflow/theme: {h}" for h in (h2[:10] or ['See full source for workflow narrative'])])}

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

{fmt_list(gaps)}

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
4. [ ] Read source: `{src_rel}` and mirror under corpus if present.
5. [ ] Map FRs → existing agents/DNA (avoid duplicate agents).
6. [ ] Create feature branch `special/{skill}`.
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

{''.join(sprints)}

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

Suggested path: `backend/app/tests/unit/test_special_{skill.replace('-', '_')}.py`

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

This source: **{meta['lines']} lines** → plan capacity accordingly.

---

## Appendix A — Source heading index (full H2/H3 extract)

| Level | Heading |
|------:|---------|
{heading_table}

---

## Appendix B — Traceability

| Artifact | Location |
|----------|----------|
| This plan | `planning/special/{skill}.md` |
| Upstream study | `{src_rel}` |
| Host pack | `business/video/` |
| Selection | `business/video/archetype_registry.json` |
| Command origin | `generate_special_skills.md` |

---

*End of plan — `{skill}` — generated {TODAY}*
"""

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    missing = []
    for fn in SOURCES:
        path = STUDY / fn
        if not path.is_file():
            missing.append(fn)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        skill = skill_name(fn)
        plan = build_plan(fn, text)
        out_path = OUT / f"{skill}.md"
        out_path.write_text(plan, encoding="utf-8")
        written.append((skill, out_path.stat().st_size, path.stat().st_size))
        print(f"wrote {out_path.name} ({out_path.stat().st_size} bytes) from {fn}")

    # index
    index_lines = [
        f"# Special skills — SDD adoption plans",
        "",
        f"**Generated:** {TODAY}  ",
        f"**Command:** `generate_special_skills.md`  ",
        f"**Generator:** `scripts/business/generate_special_skills_plans.py`  ",
        f"**Source root:** `C:\\\\Project\\\\va-agent-swarm\\\\study`  ",
        f"**Output root:** `planning/special/`",
        "",
        "## Plans",
        "",
        "| skill | plan | source study |",
        "|-------|------|--------------|",
    ]
    for fn in SOURCES:
        sk = skill_name(fn)
        status = f"[`{sk}.md`](./{sk}.md)" if (OUT / f"{sk}.md").is_file() else "_missing_"
        index_lines.append(f"| `{sk}` | {status} | `{fn}` |")
    index_lines += [
        "",
        "## Mandatory plan sections (each file)",
        "",
        "1. Source Document Review & Requirement Extraction",
        "2. Dependency Mapping & Pre-Development Setup",
        "3. Spec-Aligned Implementation Roadmap",
        "4. Testing & Validation Framework",
        "5. Deployment & Post-Launch Monitoring Plan",
        "6. Risk Mitigation & Timeline",
        "",
        f"## Summary",
        "",
        f"- Written: **{len(written)}**",
        f"- Missing sources: **{len(missing)}**" + (f" ({', '.join(missing)})" if missing else ""),
        "",
    ]
    (OUT / "README.md").write_text("\n".join(index_lines), encoding="utf-8")
    print(f"index README written; count={len(written)} missing={missing}")


if __name__ == "__main__":
    main()
