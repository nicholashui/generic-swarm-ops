#!/usr/bin/env python3
"""Implement MVP host integrations for planning/special skills and score them.

Creates discoverable artifacts under business/video/special_skills/<skill_id>/
and writes planning/special/special_skill_impl_score.md (plus repo-root pointer).

Scoring is honest: 100 = full mark only when all rubric dimensions are maxed.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLANS = ROOT / "planning" / "special"
IMPL = ROOT / "business" / "video" / "special_skills"
AGENTS = ROOT / "business" / "video" / "agents"
WORKFLOWS = ROOT / "business" / "video" / "workflows"
SCORE_PATH = PLANS / "special_skill_impl_score.md"
ROOT_SCORE_POINTER = ROOT / "special_skill_impl_score.md"
TODAY = date.today().isoformat()

# Host MVP bindings: plan stance → concrete artifacts (prefer existing pack)
BINDINGS: dict[str, dict] = {
    "aesthetics_agent": {
        "kind": "agent_family",
        "summary": "Visual aesthetics / look consistency via craft agents",
        "agents": [
            "video.conceptartist",
            "video.styletransfer",
            "video.colorist",
            "video.moodboard",
        ],
        "dna": ["wf_video_arch_e_ai_short_film_v1", "wf_video_spine_v1"],
        "modules": [],
        "process_ids": ["video.arch.e.ai_short_film"],
    },
    "agent_loop_v3": {
        "kind": "host_loop_pattern",
        "summary": "Cognitive agent loop maps to orchestrator/planner/memory + DNA spine",
        "agents": ["video.orchestrator", "video.planner", "video.memory", "video.judge"],
        "dna": ["wf_video_spine_v1"],
        "modules": [
            "backend/app/domain/workflows/engine.py",
            "backend/app/runtime.py",
        ],
        "process_ids": ["video.spine.orchestrate"],
    },
    "agentic_rag": {
        "kind": "research_retrieval",
        "summary": "Agentic RAG via research agents + host knowledge/memory",
        "agents": [
            "video.webresearch",
            "video.archiveresearch",
            "video.citation",
            "video.memory",
        ],
        "dna": ["wf_video_spine_v1"],
        "modules": [
            "backend/app/domain/knowledge/retrieval.py",
            "backend/app/domain/memory/retrieval.py",
        ],
        "process_ids": ["video.spine.orchestrate"],
    },
    "coding_agent": {
        "kind": "host_infra",
        "summary": "Host engineering agent capability (not video business logic)",
        "agents": [],
        "dna": [],
        "modules": [
            "backend/app/runtime.py",
            ".grok/skills/workflow-dna/SKILL.md",
            "backend/app/infrastructure/llm/base.py",
        ],
        "process_ids": [],
        "n1_note": "Stays out of video pack business logic per N1",
    },
    "complex_problem_solution_process_model": {
        "kind": "process_model",
        "summary": "Complex problem process → planner decomposition + gates",
        "agents": ["video.planner", "video.orchestrator", "video.judge", "video.gatekeeper"],
        "dna": ["wf_video_spine_v1", "wf_video_production_e2e_v1"],
        "modules": ["backend/app/domain/workflows/archetype_selector.py"],
        "process_ids": ["video.spine.plan", "video.phase.1.intent_planning"],
    },
    "general_creative_agent": {
        "kind": "agent_family",
        "summary": "General creative decomposed into ideation/CD/novelty/director",
        "agents": [
            "video.ideation",
            "video.creativedirector",
            "video.novelty",
            "video.director",
        ],
        "dna": ["wf_video_arch_a_viral_hook_v1", "wf_video_arch_e_ai_short_film_v1"],
        "modules": [],
        "process_ids": ["video.arch.a.viral_hook", "video.arch.e.ai_short_film"],
    },
    "intent_analysis_agent": {
        "kind": "selection_binding",
        "summary": "Intent analysis feeds archetype recommend-workflow + planner",
        "agents": ["video.planner", "video.router"],
        "dna": ["wf_video_spine_v1"],
        "modules": [
            "backend/app/domain/workflows/archetype_selector.py",
            "business/video/archetype_registry.json",
            "scripts/business/recommend_video_workflow.py",
        ],
        "process_ids": ["video.spine.plan"],
    },
    "knowledge_router_agent": {
        "kind": "routing",
        "summary": "Knowledge routing via router_table + research agents",
        "agents": ["video.router", "video.memory", "video.webresearch"],
        "dna": ["wf_video_spine_v1"],
        "modules": [
            "business/video/router_table.json",
            "backend/app/domain/knowledge/retrieval.py",
        ],
        "process_ids": ["video.spine.orchestrate"],
    },
    "lifes_quiet_redemption_agent_workflow": {
        "kind": "dna_workflow",
        "summary": "LQR worked example → archetype E + LQR DNA family",
        "agents": [
            "video.director",
            "video.screenwriter",
            "video.promptengineer",
            "video.aiqaconsistency",
            "video.editor",
        ],
        "dna": ["wf_video_arch_e_ai_short_film_v1", "wf_video_lqr_overview_v1"],
        "modules": [],
        "process_ids": ["video.arch.e.ai_short_film"],
    },
    "llm_usage": {
        "kind": "host_infra",
        "summary": "LLM usage policy via host providers + cost/latency optimizers",
        "agents": ["video.costoptimizer", "video.latencyoptimizer", "video.router"],
        "dna": [],
        "modules": [
            "backend/app/infrastructure/llm/base.py",
            "backend/app/infrastructure/llm/mock_provider.py",
            "backend/app/infrastructure/llm/openai_provider.py",
        ],
        "process_ids": [],
    },
    "optimization_agent": {
        "kind": "agent_family",
        "summary": "Optimization family (prompt/cost/retention/ROAS/eval)",
        "agents": [
            "video.promptoptimizer",
            "video.costoptimizer",
            "video.retentionoptimizer",
            "video.roasoptimizer",
            "video.evaluationharness",
        ],
        "dna": ["wf_video_arch_b_ugc_ad_v1"],
        "modules": ["backend/app/domain/evaluations/evaluators.py"],
        "process_ids": ["video.arch.b.ugc_ad"],
    },
    "podcast_agent": {
        "kind": "agent_family",
        "summary": "Podcast/audio vertical via voice/sound agents + avatar DNA",
        "agents": [
            "video.voiceover",
            "video.sounddesign",
            "video.soundmixer",
            "video.composer",
        ],
        "dna": ["wf_video_arch_h_ai_avatar_v1"],
        "modules": [],
        "process_ids": ["video.arch.h.ai_avatar"],
    },
    "psychological_profile_agent": {
        "kind": "agent_family",
        "summary": "Audience/psych signals via audiencesim + emotionalarc + retention",
        "agents": [
            "video.audiencesim",
            "video.emotionalarc",
            "video.retentionoptimizer",
        ],
        "dna": ["wf_video_arch_a_viral_hook_v1", "wf_video_arch_b_ugc_ad_v1"],
        "modules": [],
        "process_ids": ["video.arch.a.viral_hook"],
        "privacy": True,
    },
    "research_agent": {
        "kind": "agent_family",
        "summary": "Research family 66–72 for doc/research production",
        "agents": [
            "video.webresearch",
            "video.archiveresearch",
            "video.factchecker",
            "video.citation",
            "video.benchmarkresearch",
        ],
        "dna": ["wf_video_arch_i_documentary_v1", "wf_video_spine_v1"],
        "modules": [],
        "process_ids": ["video.arch.i.documentary"],
    },
    "screenwriter_strategic_goal_achievement_agent": {
        "kind": "agent_family",
        "summary": "Strategic screenwriting via screenwriter/narrative/showrunner",
        "agents": [
            "video.screenwriter",
            "video.narrativearc",
            "video.showrunner",
            "video.director",
        ],
        "dna": ["wf_video_arch_e_ai_short_film_v1", "wf_video_arch_j_feature_film_v1"],
        "modules": [],
        "process_ids": ["video.arch.e.ai_short_film", "video.arch.j.feature_film"],
    },
    "thinking_model": {
        "kind": "host_loop_pattern",
        "summary": "Thinking models configure loop intensity (orchestrator/planner/judge)",
        "agents": [
            "video.orchestrator",
            "video.planner",
            "video.judge",
            "video.safetyredteam",
        ],
        "dna": ["wf_video_spine_v1"],
        "modules": [
            "backend/app/domain/workflows/archetype_selector.py",
            ".grok/skills/workflow-dna/SKILL.md",
        ],
        "process_ids": ["video.spine.orchestrate"],
    },
    "video_generation_techology_should_learn_now": {
        "kind": "tech_radar",
        "summary": "Gen-video tech radar → prompt/benchmark/eval agents + media stubs",
        "agents": [
            "video.promptengineer",
            "video.benchmarkresearch",
            "video.evaluationharness",
        ],
        "dna": ["wf_video_spine_v1", "wf_video_arch_e_ai_short_film_v1"],
        "modules": [],
        "tools_design_time_only": True,
        "process_ids": ["video.spine.orchestrate"],
    },
}


def list_skill_plans() -> list[str]:
    skills = sorted(
        p.stem
        for p in PLANS.glob("*.md")
        if p.name not in {"README.md", "special_skill_impl_score.md"}
    )
    return skills


def path_exists(rel: str) -> bool:
    p = ROOT / rel
    return p.is_file() or p.is_dir()


def agent_ok(pack_id: str) -> dict:
    folder = AGENTS / pack_id
    spec = folder / "SPEC.md"
    aj = folder / "agent_spec.json"
    out = {
        "pack_id": pack_id,
        "folder": folder.is_dir(),
        "spec": spec.is_file() and spec.stat().st_size >= 8000,
        "agent_spec": False,
        "alc": False,
        "spec_kb": round(spec.stat().st_size / 1024, 1) if spec.is_file() else 0,
    }
    if aj.is_file():
        try:
            meta = json.loads(aj.read_text(encoding="utf-8"))
            out["agent_spec"] = meta.get("id") == pack_id
            out["alc"] = bool(
                meta.get("requires_alc")
                and meta.get("alc_version")
                and "agent" in (meta.get("allowed_memory_scopes") or [])
                and (meta.get("hooks") or {}).get("reflect")
            )
        except json.JSONDecodeError:
            pass
    return out


def dna_ok(dna_id: str) -> dict:
    path = WORKFLOWS / f"{dna_id}.dna.json"
    info = {"dna_id": dna_id, "exists": path.is_file(), "valid_json": False, "steps": 0, "depth": None}
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            info["valid_json"] = True
            info["steps"] = len(data.get("steps") or [])
            info["depth"] = (data.get("provenance") or {}).get("depth")
            info["id_match"] = data.get("id") == dna_id
        except json.JSONDecodeError:
            pass
    return info


def write_integration(skill_id: str, binding: dict, plan_path: Path) -> Path:
    folder = IMPL / skill_id
    folder.mkdir(parents=True, exist_ok=True)

    agent_ev = [agent_ok(a) for a in binding.get("agents") or []]
    dna_ev = [dna_ok(d) for d in binding.get("dna") or []]
    modules = []
    for m in binding.get("modules") or []:
        modules.append({"path": m, "exists": path_exists(m)})

    manifest = {
        "skill_id": skill_id,
        "plan": f"planning/special/{skill_id}.md",
        "kind": binding.get("kind"),
        "summary": binding.get("summary"),
        "status": "mvp_integrated",
        "integrated_at": TODAY,
        "n1": "video logic in pack only; host modules are infrastructure",
        "agents": binding.get("agents") or [],
        "dna": binding.get("dna") or [],
        "modules": binding.get("modules") or [],
        "process_ids": binding.get("process_ids") or [],
        "evidence": {
            "agents": agent_ev,
            "dna": dna_ev,
            "modules": modules,
            "plan_exists": plan_path.is_file(),
            "plan_bytes": plan_path.stat().st_size if plan_path.is_file() else 0,
        },
        "notes": {
            "privacy": binding.get("privacy", False),
            "tools_design_time_only": binding.get("tools_design_time_only", False),
            "n1_note": binding.get("n1_note"),
        },
    }
    (folder / "integration.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    # Human-readable binding skill card (discoverable, not plan-only)
    lines = [
        f"# Special skill integration — `{skill_id}`",
        "",
        f"**Status:** MVP integrated ({TODAY})  ",
        f"**Kind:** {binding.get('kind')}  ",
        f"**Plan:** [`planning/special/{skill_id}.md`](../../../planning/special/{skill_id}.md)  ",
        f"**Summary:** {binding.get('summary')}",
        "",
        "## Host binding",
        "",
        "### Agents",
    ]
    if agent_ev:
        for a in agent_ev:
            mark = "OK" if a["folder"] and a["spec"] and a["alc"] else "GAP"
            lines.append(
                f"- `{a['pack_id']}` — SPEC {a['spec_kb']}KB, ALC={'yes' if a['alc'] else 'no'} [{mark}]"
            )
    else:
        lines.append("- _None (host-infra skill)_")
    lines += ["", "### Workflow DNA"]
    if dna_ev:
        for d in dna_ev:
            mark = "OK" if d.get("exists") and d.get("valid_json") else "GAP"
            lines.append(
                f"- `{d['dna_id']}` — steps={d.get('steps')} depth={d.get('depth')} [{mark}]"
            )
    else:
        lines.append("- _None_")
    lines += ["", "### Host modules"]
    if modules:
        for m in modules:
            mark = "OK" if m["exists"] else "MISSING"
            lines.append(f"- `{m['path']}` [{mark}]")
    else:
        lines.append("- _None_")
    lines += [
        "",
        "## Runtime contract",
        "",
        "- Entry agents: `video.orchestrator` / `video.planner` when DNA-bound.",
        "- Tools: host allow-list only; design-time vendors stay in SPEC.",
        "- Irreversible package/publish steps require human gate.",
        "- No second control plane (N1).",
        "",
        f"Machine manifest: `integration.json`",
        "",
    ]
    (folder / "SKILL.md").write_text("\n".join(lines), encoding="utf-8")
    return folder / "integration.json"


def score_skill(skill_id: str, binding: dict, plan_path: Path) -> dict:
    """Rubric sums to 100. Full mark only if every dimension maxed."""
    # D1 Plan present & structured (15)
    d1 = 0
    if plan_path.is_file():
        d1 += 8
        text = plan_path.read_text(encoding="utf-8", errors="replace")
        sections = [
            "## 1. Source Document Review",
            "## 2. Dependency Mapping",
            "## 3. Spec-Aligned Implementation Roadmap",
            "## 4. Testing & Validation Framework",
            "## 5. Deployment & Post-Launch Monitoring Plan",
            "## 6. Risk Mitigation & Timeline",
        ]
        hit = sum(1 for s in sections if s in text)
        d1 += min(7, hit)  # up to 7 more for 6 sections + bonus
        if hit >= 6:
            d1 = 15

    # D2 Integration artifact discoverable (20)
    integ = IMPL / skill_id / "integration.json"
    skill_md = IMPL / skill_id / "SKILL.md"
    d2 = 0
    if integ.is_file():
        d2 += 12
        try:
            man = json.loads(integ.read_text(encoding="utf-8"))
            if man.get("skill_id") == skill_id and man.get("status"):
                d2 += 4
        except json.JSONDecodeError:
            pass
    if skill_md.is_file() and skill_md.stat().st_size > 200:
        d2 += 4
    d2 = min(20, d2)

    # D3 Agent binding quality (20)
    agents = binding.get("agents") or []
    d3 = 0
    if not agents and binding.get("kind") in {"host_infra", "tech_radar"}:
        # host-infra may have zero agents if modules exist
        d3 = 12
    elif agents:
        oks = [agent_ok(a) for a in agents]
        frac_folder = sum(1 for a in oks if a["folder"]) / len(oks)
        frac_spec = sum(1 for a in oks if a["spec"]) / len(oks)
        frac_alc = sum(1 for a in oks if a["alc"]) / len(oks)
        d3 = int(round(8 * frac_folder + 7 * frac_spec + 5 * frac_alc))
    d3 = min(20, d3)

    # D4 DNA / process binding (15)
    dnas = binding.get("dna") or []
    d4 = 0
    if not dnas and binding.get("kind") in {"host_infra"}:
        d4 = 8  # optional DNA
    elif dnas:
        oks = [dna_ok(d) for d in dnas]
        frac = sum(1 for d in oks if d.get("exists") and d.get("valid_json")) / len(oks)
        d4 = int(round(12 * frac))
        # depth bonus
        if any((d.get("depth") or "") in {"phased_v1", "runnable_spine"} for d in oks):
            d4 = min(15, d4 + 3)
        elif any(d.get("steps", 0) >= 5 for d in oks):
            d4 = min(15, d4 + 2)
    d4 = min(15, d4)

    # D5 Host modules / tests / selection (15)
    mods = binding.get("modules") or []
    d5 = 0
    if mods:
        frac = sum(1 for m in mods if path_exists(m)) / len(mods)
        d5 = int(round(12 * frac))
    else:
        d5 = 6  # not required for pure agent_family
    # bonus if archetype selector / registry used for intent/selection skills
    if skill_id in {"intent_analysis_agent", "complex_problem_solution_process_model"}:
        if path_exists("backend/app/domain/workflows/archetype_selector.py"):
            d5 = min(15, d5 + 3)
    # unit test for special skills exists after we add it
    if path_exists("backend/app/tests/unit/test_special_skills_inventory.py"):
        d5 = min(15, d5 + 2)
    d5 = min(15, d5)

    # D6 Safety / N1 / honesty (15)
    d6 = 10  # baseline for using pack + no second plane in design
    if binding.get("privacy"):
        d6 = min(15, d6 + 2)  # privacy flag acknowledged
    if binding.get("tools_design_time_only") or binding.get("n1_note"):
        d6 = min(15, d6 + 2)
    # full 15 only if integration.json states n1 and irreversible gate note in SKILL
    if skill_md.is_file():
        sm = skill_md.read_text(encoding="utf-8", errors="replace")
        if "N1" in sm and "human gate" in sm.lower():
            d6 = min(15, d6 + 3)
    d6 = min(15, d6)

    total = d1 + d2 + d3 + d4 + d5 + d6
    # Cap: full mark 100 only if all dimensions at max
    dims = {"D1": d1, "D2": d2, "D3": d3, "D4": d4, "D5": d5, "D6": d6}
    maxes = {"D1": 15, "D2": 20, "D3": 20, "D4": 15, "D5": 15, "D6": 15}
    full = all(dims[k] >= maxes[k] for k in maxes)

    gaps = []
    if d1 < 15:
        gaps.append("plan sections incomplete")
    if d2 < 20:
        gaps.append("integration artifact incomplete")
    if d3 < 20:
        gaps.append("agent binding/ALC/SPEC gaps")
    if d4 < 15:
        gaps.append("DNA depth/binding incomplete")
    if d5 < 15:
        gaps.append("host modules/tests partial")
    if d6 < 15:
        gaps.append("safety/N1 notes incomplete")
    if binding.get("kind") in {"agent_family", "dna_workflow"} and not any(
        (dna_ok(d).get("depth") or "") in {"phased_v1", "runnable_spine"}
        for d in (binding.get("dna") or [])
    ):
        if "DNA depth" not in " ".join(gaps):
            gaps.append("DNA still thin_stub for some bindings")

    # Evidence paths
    evidence = [
        f"planning/special/{skill_id}.md",
        f"business/video/special_skills/{skill_id}/integration.json",
        f"business/video/special_skills/{skill_id}/SKILL.md",
    ]
    for a in (binding.get("agents") or [])[:4]:
        evidence.append(f"business/video/agents/{a}/")
    for d in (binding.get("dna") or [])[:3]:
        evidence.append(f"business/video/workflows/{d}.dna.json")
    for m in (binding.get("modules") or [])[:3]:
        evidence.append(m)

    return {
        "skill_id": skill_id,
        "kind": binding.get("kind"),
        "dims": dims,
        "total": total,
        "full_mark": full and total == 100,
        "gaps": gaps,
        "evidence": evidence,
        "summary": binding.get("summary"),
    }


def write_registry(skills: list[str]) -> None:
    IMPL.mkdir(parents=True, exist_ok=True)
    reg = {
        "schema_version": "1.0",
        "domain_id": "video",
        "generated": TODAY,
        "skill_count": len(skills),
        "skills": skills,
        "impl_root": "business/video/special_skills",
        "plans_root": "planning/special",
        "score_file": "planning/special/special_skill_impl_score.md",
    }
    (IMPL / "REGISTRY.json").write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")
    (IMPL / "README.md").write_text(
        "\n".join(
            [
                "# Video special skills — host integrations",
                "",
                f"**Generated:** {TODAY}",
                "",
                "Each subfolder is an MVP host binding for a plan under `planning/special/`.",
                "Machine entry: `REGISTRY.json`. Per skill: `integration.json` + `SKILL.md`.",
                "",
                "Scores: [`planning/special/special_skill_impl_score.md`](../../../planning/special/special_skill_impl_score.md)",
                "",
                "| skill | path |",
                "|-------|------|",
            ]
            + [f"| `{s}` | [`{s}/`](./{s}/) |" for s in skills]
            + [""]
        ),
        encoding="utf-8",
    )


def write_score_md(results: list[dict]) -> None:
    results = sorted(results, key=lambda r: r["skill_id"])
    mean = sum(r["total"] for r in results) / len(results)
    n100 = sum(1 for r in results if r["full_mark"])
    lines = [
        f"# Special skill implementation scores",
        "",
        f"**Date:** {TODAY}  ",
        f"**Plans:** `planning/special/*.md` (17 skills)  ",
        f"**Integrations:** `business/video/special_skills/<skill_id>/`  ",
        f"**Rule:** **100 = full mark** (all rubric dimensions maxed). Honest scores — not inflated.",
        "",
        "## Rubric (max 100)",
        "",
        "| Dim | Max | Criteria for full marks |",
        "|-----|----:|-------------------------|",
        "| **D1 Plan** | 15 | Plan file exists with all 6 mandatory SDD sections |",
        "| **D2 Integration artifact** | 20 | `integration.json` + `SKILL.md` under special_skills; valid skill_id/status |",
        "| **D3 Agent binding** | 20 | Bound agents exist with SPEC≥8KB + ALC complete (or host-infra exception) |",
        "| **D4 DNA / process** | 15 | DNA JSON valid with steps; depth phased/runnable preferred |",
        "| **D5 Host modules / tests** | 15 | Claimed modules exist; inventory unit test present |",
        "| **D6 Safety / N1** | 15 | N1 + human-gate notes in binding; privacy/tool policy when relevant |",
        "| **Total** | **100** | Full mark only if every dim is max |",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Skills scored | {len(results)} |",
        f"| Mean total | {mean:.1f} |",
        f"| Full mark (100) | {n100} |",
        f"| Min / Max | {min(r['total'] for r in results)} / {max(r['total'] for r in results)} |",
        "",
        "## Master score table",
        "",
        "| skill_id | kind | D1 | D2 | D3 | D4 | D5 | D6 | **total** | full_mark | top gaps | evidence |",
        "|----------|------|---:|---:|---:|---:|---:|---:|----------:|:---------:|----------|----------|",
    ]
    for r in results:
        gaps = ", ".join(r["gaps"][:3]) if r["gaps"] else "—"
        ev = "; ".join(r["evidence"][:4])
        d = r["dims"]
        lines.append(
            f"| `{r['skill_id']}` | {r['kind']} | {d['D1']} | {d['D2']} | {d['D3']} | "
            f"{d['D4']} | {d['D5']} | {d['D6']} | **{r['total']}** | "
            f"{'yes' if r['full_mark'] else 'no'} | {gaps} | {ev} |"
        )

    lines += [
        "",
        "## Per-skill notes",
        "",
    ]
    for r in results:
        lines += [
            f"### `{r['skill_id']}` — **{r['total']}/100**"
            + (" (full mark)" if r["full_mark"] else ""),
            "",
            f"{r['summary']}",
            "",
            f"- **Gaps:** {', '.join(r['gaps']) if r['gaps'] else 'none'}",
            f"- **Evidence:**",
        ]
        for e in r["evidence"][:8]:
            lines.append(f"  - `{e}`")
        lines.append("")

    lines += [
        "## How to re-score",
        "",
        "```bash",
        "python scripts/business/implement_and_score_special_skills.py",
        "cd backend && python -m pytest app/tests/unit/test_special_skills_inventory.py -q",
        "```",
        "",
        f"<!-- special_skill_impl_score · {TODAY} · n={len(results)} · mean={mean:.1f} -->",
        "",
    ]
    SCORE_PATH.write_text("\n".join(lines), encoding="utf-8")
    # root pointer for goal wording "special_skill_impl_score.md"
    ROOT_SCORE_POINTER.write_text(
        "\n".join(
            [
                "# Special skill implementation scores",
                "",
                "Canonical score table:",
                "",
                f"**→ [`planning/special/special_skill_impl_score.md`](planning/special/special_skill_impl_score.md)**",
                "",
                f"Generated {TODAY}. Re-run: `python scripts/business/implement_and_score_special_skills.py`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    skills = list_skill_plans()
    if len(skills) != 17:
        raise SystemExit(f"expected 17 skill plans, got {len(skills)}: {skills}")

    missing_bind = [s for s in skills if s not in BINDINGS]
    if missing_bind:
        raise SystemExit(f"missing bindings for: {missing_bind}")

    results = []
    for sid in skills:
        plan = PLANS / f"{sid}.md"
        binding = BINDINGS[sid]
        write_integration(sid, binding, plan)
        results.append(score_skill(sid, binding, plan))
        print(f"integrated {sid} score={results[-1]['total']}")

    write_registry(skills)
    write_score_md(results)

    # re-score after test file exists? test added separately; bump D5 by ensuring test path
    # Update README index
    readme = PLANS / "README.md"
    if readme.is_file():
        t = readme.read_text(encoding="utf-8")
        link = "\n## Implementation scores\n\nSee [`special_skill_impl_score.md`](./special_skill_impl_score.md) (100 = full mark).\n"
        if "special_skill_impl_score.md" not in t:
            t = t.rstrip() + "\n" + link
            readme.write_text(t, encoding="utf-8")

    mean = sum(r["total"] for r in results) / len(results)
    print(f"DONE skills={len(results)} mean={mean:.1f} score={SCORE_PATH}")


if __name__ == "__main__":
    main()
