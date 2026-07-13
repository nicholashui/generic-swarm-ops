# -*- coding: utf-8 -*-
"""Wave 5 N3 pack preparer — agent readiness, DNA families, router, process coverage.

Idempotent. Writes only under business/video/ (and docs paths below it).
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "business" / "video"
AGENTS = VIDEO / "agents"
WORKFLOWS = VIDEO / "workflows"
TODAY = date.today().isoformat()

ARCHETYPES = [
    ("b", "ugc_ad", "UGC Ad", ["video.ugccreator", "video.copywriter", "video.creativedirector"]),
    ("c", "animated_explainer", "Animated Explainer", ["video.animator_2d", "video.motiongraphics", "video.storyboard"]),
    ("d", "personalized_birthday", "Personalized Birthday", ["video.personalizationengineer", "video.screenwriter", "video.composer"]),
    ("e", "ai_short_film", "AI Short Film", ["video.director", "video.screenwriter", "video.cinematographer", "video.editor"]),
    ("f", "corporate_training", "Corporate Training", ["video.instructionaldesign", "video.sme", "video.screenwriter"]),
    ("g", "music_video", "Music Video", ["video.musicvideodirector", "video.composer", "video.choreography", "video.editor"]),
    ("h", "ai_avatar", "AI Avatar", ["video.avatardesign", "video.voiceclone", "video.promptengineer"]),
    ("i", "documentary", "Documentary", ["video.journalist", "video.factchecker", "video.editor", "video.archiveresearch"]),
    ("j", "feature_film", "Feature Film", ["video.showrunner", "video.director", "video.screenwriter", "video.editor"]),
]

SPINE_AGENTS = {
    "video.orchestrator",
    "video.planner",
    "video.director",
    "video.screenwriter",
    "video.webresearch",
    "video.aiqaconsistency",
    "video.producer",
}


def _step(sid: str, agent: str, tools: list[str], nxt: list[str], *, gate: bool = False) -> dict:
    return {
        "id": sid,
        "state": "critical_gate" if gate else "execution",
        "next": nxt,
        "agent": agent,
        "tools": tools,
        "action_type": "irreversible_execution" if gate else "analysis",
        "human_gate_required": gate,
        "irreversible": gate,
    }


def write_thin_dna(
    dna_id: str,
    name: str,
    objective: str,
    specialist_agents: list[str],
    source_refs: list[str],
) -> Path:
    steps: list[dict] = []
    steps.append(_step("orchestrate", "video.orchestrator", ["audit_log_writer"], ["plan"]))
    steps.append(_step("plan", "video.planner", ["audit_log_writer"], ["specialize_0"]))
    last = "plan"
    for i, agent in enumerate(specialist_agents):
        sid = f"specialize_{i}"
        nxt = [f"specialize_{i+1}"] if i + 1 < len(specialist_agents) else ["qc"]
        tool = "video_script_format" if "screen" in agent or "copy" in agent else "audit_log_writer"
        if "prompt" in agent or "avatar" in agent or "media" in agent:
            tool = "video_media_gen_stub"
        steps.append(_step(sid, agent, [tool], nxt))
        last = sid
    steps.append(_step("qc", "video.aiqaconsistency", ["video_qc_stub"], ["package"]))
    steps.append(
        _step("package", "video.producer", ["video_package_stub"], ["complete"], gate=True)
    )
    # fix first specialize next from plan
    for s in steps:
        if s["id"] == "plan":
            s["next"] = ["specialize_0"] if specialist_agents else ["qc"]
    dna = {
        "id": dna_id,
        "name": name,
        "domain": "video",
        "objective": objective,
        "owner": "video.orchestrator",
        "version": "1.0.0",
        "risk_tier": "tier_3_execute_reversible",
        "production_ready": False,
        "inputs": ["brief"],
        "preconditions": ["brief is non-empty"],
        "steps": steps,
        "memory_reads": ["organization_memory"],
        "memory_writes": ["event_log", "lessons_learned"],
        "guardrails": {"human_approval_required_if": ["step.irreversible == true"]},
        "verification": {"required_checks": ["qc_pass", "package_approved"]},
        "rollback": {"reversible": False, "rollback_steps": ["unpublish_stub", "notify_producer"]},
        "fitness_metrics": ["quality", "cycle_time"],
        "audit_log_write_required": True,
        "provenance": {
            "source_refs": source_refs + ["improvements.md#wave-5", "planning/improvement/wave-5/"],
            "captured_by": "wave-5-n3",
            "recorded_at": f"{TODAY}T00:00:00Z",
            "depth": "thin_stub_n3",
        },
    }
    WORKFLOWS.mkdir(parents=True, exist_ok=True)
    path = WORKFLOWS / f"{dna_id}.dna.json"
    path.write_text(json.dumps(dna, indent=2) + "\n", encoding="utf-8")
    return path


def write_e2e_dna() -> Path:
    phases = [
        ("phase1_intent", "video.planner", "Intent & Planning"),
        ("phase2_creative", "video.director", "Creative"),
        ("phase3_prepro", "video.productiondesign", "Pre-production"),
        ("phase4_production", "video.promptengineer", "Production/gen"),
        ("phase5_post", "video.editor", "Post"),
        ("phase6_delivery", "video.socialmediastrategist", "Delivery"),
    ]
    steps = [_step("orchestrate", "video.orchestrator", ["audit_log_writer"], ["phase1_intent"])]
    for i, (sid, agent, _) in enumerate(phases):
        nxt = [phases[i + 1][0]] if i + 1 < len(phases) else ["qc"]
        tools = ["video_media_gen_stub"] if "prompt" in agent else ["audit_log_writer"]
        if agent == "video.editor":
            tools = ["video_script_format"]
        steps.append(_step(sid, agent, tools, nxt))
    steps.append(_step("qc", "video.aiqaconsistency", ["video_qc_stub"], ["package"]))
    steps.append(_step("package", "video.producer", ["video_package_stub"], ["complete"], gate=True))
    dna = {
        "id": "wf_video_production_e2e_v1",
        "name": "Video Production Six-Phase E2E",
        "domain": "video",
        "objective": "Orchestrator-down six-phase production skeleton (N3 process wiring).",
        "owner": "video.orchestrator",
        "version": "1.0.0",
        "risk_tier": "tier_3_execute_reversible",
        "production_ready": False,
        "inputs": ["brief"],
        "preconditions": ["brief is non-empty"],
        "steps": steps,
        "memory_reads": ["organization_memory", "past_failures"],
        "memory_writes": ["event_log", "lessons_learned"],
        "guardrails": {"human_approval_required_if": ["step.irreversible == true"]},
        "verification": {"required_checks": ["six_phase_complete", "qc_pass", "package_approved"]},
        "rollback": {"reversible": False, "rollback_steps": ["halt_delivery", "notify_producer"]},
        "fitness_metrics": ["phase_completion", "quality", "cycle_time"],
        "audit_log_write_required": True,
        "provenance": {
            "source_refs": [
                "va-agent-swarm/study/SYSTEM_REFERENCE.md#6.1",
                "improvements.md#wave-5",
            ],
            "captured_by": "wave-5-n3",
            "recorded_at": f"{TODAY}T00:00:00Z",
            "depth": "thin_stub_n3",
        },
    }
    path = WORKFLOWS / "wf_video_production_e2e_v1.dna.json"
    path.write_text(json.dumps(dna, indent=2) + "\n", encoding="utf-8")
    return path


def prepare_agents(roster: list[dict]) -> int:
    updated = 0
    for row in roster:
        pack_id = row["pack_id"]
        cat = row.get("category") or "unknown"
        spec_path = AGENTS / pack_id / "agent_spec.json"
        if not spec_path.is_file():
            continue
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        tools = list(spec.get("tools") or [])
        if "audit_log_writer" not in tools:
            tools = ["audit_log_writer"] + tools
        # category-ish stubs for specialists on media/script paths
        if pack_id in {
            "video.screenwriter",
            "video.copywriter",
            "video.comedywriter",
            "video.childrensauthor",
        }:
            if "video_script_format" not in tools:
                tools.append("video_script_format")
        if pack_id in {
            "video.promptengineer",
            "video.director",
            "video.cinematographer",
            "video.avatardesign",
        }:
            if "video_media_gen_stub" not in tools:
                tools.append("video_media_gen_stub")
        if pack_id in {"video.aiqaconsistency", "video.judge"}:
            if "video_qc_stub" not in tools:
                tools.append("video_qc_stub")
        if pack_id in {"video.producer", "video.trailereditor", "video.socialmediastrategist"}:
            if "video_package_stub" not in tools:
                tools.append("video_package_stub")
        maturity = "L2_runtime" if pack_id in SPINE_AGENTS else "L1_indexed"
        spec.update(
            {
                "status": "registered",
                "requires_alc": True,
                "allowed_memory_scopes": list(
                    dict.fromkeys((spec.get("allowed_memory_scopes") or []) + ["agent", "organization"])
                ),
                "alc_version": spec.get("alc_version") or "1.0",
                "hooks": {**(spec.get("hooks") or {}), "reflect": True},
                "tools": tools,
                "allowed_tools": list(tools),
                "n3_maturity": maturity,
                "activation_category": cat,
                "domain_id": "video",
            }
        )
        if "provenance" not in spec:
            spec["provenance"] = {}
        refs = list((spec.get("provenance") or {}).get("source_refs") or [])
        if "improvements.md#wave-5" not in refs:
            refs.append("improvements.md#wave-5")
        spec["provenance"]["source_refs"] = refs
        spec["provenance"]["wave5_prepared"] = TODAY
        spec_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        updated += 1
    return updated


def prepare_standby(roster: list[dict]) -> None:
    pool_path = VIDEO / "standby_pool.json"
    agents = []
    for row in roster:
        pack_id = row["pack_id"]
        agents.append(
            {
                "pack_id": pack_id,
                "va_id": row.get("id"),
                "category": row.get("category"),
                "route": "orchestrator_standby",
                "spine": pack_id in SPINE_AGENTS,
                "n3_reachable": True,
            }
        )
    payload = {
        "schema_version": "1.1",
        "description": "N3 orchestrator reachability — every roster agent listed (Wave 5)",
        "entry": "video.orchestrator",
        "agents": agents,
        "count": len(agents),
    }
    pool_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def prepare_router(roster: list[dict]) -> None:
    categories: dict[str, list[str]] = {}
    for row in roster:
        cat = row.get("category") or "unknown"
        categories.setdefault(cat, []).append(row["pack_id"])
    processes = {
        "video.spine.orchestrate": {
            "entry": "video.orchestrator",
            "agents": ["video.orchestrator", "video.planner", "video.router", "video.judge"],
        },
        "video.production.e2e": {
            "entry": "video.orchestrator",
            "agents": [
                "video.orchestrator",
                "video.planner",
                "video.director",
                "video.productiondesign",
                "video.promptengineer",
                "video.editor",
                "video.socialmediastrategist",
                "video.aiqaconsistency",
                "video.producer",
            ],
        },
        "video.lqr.overview": {
            "entry": "video.orchestrator",
            "agents": ["video.orchestrator", "video.aiqaconsistency", "video.editor", "video.producer"],
        },
        "video.delivery.package": {
            "entry": "video.orchestrator",
            "agents": [
                "video.orchestrator",
                "video.socialmediastrategist",
                "video.performancemarketer",
                "video.trailereditor",
                "video.producer",
            ],
        },
    }
    for letter, slug, title, specialists in ARCHETYPES:
        processes[f"video.arch.{letter}.{slug}"] = {
            "entry": "video.orchestrator",
            "agents": ["video.orchestrator", "video.planner"] + specialists + ["video.aiqaconsistency", "video.producer"],
        }
    processes["video.arch.a.viral_hook"] = {
        "entry": "video.orchestrator",
        "agents": [
            "video.orchestrator",
            "video.planner",
            "video.screenwriter",
            "video.director",
            "video.aiqaconsistency",
            "video.producer",
        ],
    }
    payload = {
        "schema_version": "1.0",
        "entry": "video.orchestrator",
        "categories": categories,
        "processes": processes,
        "provenance": {"source_refs": ["improvements.md#wave-5"], "recorded_at": TODAY},
    }
    (VIDEO / "router_table.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def prepare_process_coverage() -> list[dict]:
    docs = VIDEO / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    maps = docs / "process-maps.md"
    deep = docs / "deep-spec-modules.md"
    if not maps.is_file():
        maps.write_text(
            """# Video Process Maps (Pack-Linked)

Wave 5 N3: human vs AI production maps live **in-pack** (not va-only).

| process_id | summary |
|------------|---------|
| video.map.human_production | Human production workflow stages mirrored for handoff |
| video.map.ai_agent_production | Agent-native production map aligned to DNA families |

Sources retained as provenance only; authoritative pack paths are this file + DNA under `workflows/`.
""",
            encoding="utf-8",
        )
    if not deep.is_file():
        deep.write_text(
            """# Deep-Spec Modules (Pack-Linked)

Wave 5 N3: research, optimization, GCA/SSOR, agentic RAG, DIA/intent, aesthetics,
coding (sandbox-only), podcast dual-home, planner designs, agent loops.

These modules are **retained in-pack** via agent_specs + this index. Executable
paths enter through `video.orchestrator` / `video.planner` DNA families.
""",
            encoding="utf-8",
        )

    processes: list[dict] = [
        {
            "process_id": "video.spine.orchestrate",
            "representation": "dna",
            "path": "business/video/workflows/wf_video_spine_v1.dna.json",
            "status": "dna_ready",
        },
        {
            "process_id": "video.spine.plan",
            "representation": "dna",
            "path": "business/video/workflows/wf_video_spine_v1.dna.json",
            "status": "dna_ready",
        },
        {
            "process_id": "video.phase.1.intent_planning",
            "representation": "dna",
            "path": "business/video/workflows/wf_video_production_e2e_v1.dna.json",
            "status": "dna_ready",
        },
        {
            "process_id": "video.phase.2.creative",
            "representation": "dna",
            "path": "business/video/workflows/wf_video_production_e2e_v1.dna.json",
            "status": "dna_ready",
        },
        {
            "process_id": "video.phase.3.prepro",
            "representation": "dna",
            "path": "business/video/workflows/wf_video_production_e2e_v1.dna.json",
            "status": "dna_ready",
        },
        {
            "process_id": "video.phase.4.production",
            "representation": "dna",
            "path": "business/video/workflows/wf_video_production_e2e_v1.dna.json",
            "status": "dna_ready",
        },
        {
            "process_id": "video.phase.5.post",
            "representation": "dna",
            "path": "business/video/workflows/wf_video_production_e2e_v1.dna.json",
            "status": "dna_ready",
        },
        {
            "process_id": "video.phase.6.delivery",
            "representation": "dna",
            "path": "business/video/workflows/wf_video_production_e2e_v1.dna.json",
            "status": "dna_ready",
        },
        {
            "process_id": "video.arch.a.viral_hook",
            "representation": "dna",
            "path": "business/video/workflows/wf_video_arch_a_viral_hook_v1.dna.json",
            "status": "dna_ready",
        },
    ]
    for letter, slug, title, _ in ARCHETYPES:
        dna_id = f"wf_video_arch_{letter}_{slug}_v1"
        processes.append(
            {
                "process_id": f"video.arch.{letter}.{slug}",
                "representation": "dna",
                "path": f"business/video/workflows/{dna_id}.dna.json",
                "status": "dna_ready",
            }
        )
    for pid in (
        "video.lqr.overview",
        "video.lqr.scene_flow",
        "video.lqr.per_shot_loop",
        "video.lqr.character_consistency",
        "video.lqr.engine_routing",
        "video.lqr.quality_gates",
    ):
        processes.append(
            {
                "process_id": pid,
                "representation": "dna",
                "path": "business/video/workflows/wf_video_lqr_overview_v1.dna.json",
                "status": "dna_ready",
            }
        )
    processes.extend(
        [
            {
                "process_id": "video.qc.critique_bus",
                "representation": "dna",
                "path": "business/video/workflows/wf_video_lqr_overview_v1.dna.json",
                "status": "dna_ready",
            },
            {
                "process_id": "video.qc.consistency",
                "representation": "dna",
                "path": "business/video/workflows/wf_video_lqr_overview_v1.dna.json",
                "status": "dna_ready",
            },
            {
                "process_id": "video.delivery.package",
                "representation": "dna",
                "path": "business/video/workflows/wf_video_delivery_v1.dna.json",
                "status": "dna_ready",
            },
            {
                "process_id": "video.map.human_production",
                "representation": "pack_doc",
                "path": "business/video/docs/process-maps.md",
                "status": "pack_linked",
            },
            {
                "process_id": "video.map.ai_agent_production",
                "representation": "pack_doc",
                "path": "business/video/docs/process-maps.md",
                "status": "pack_linked",
            },
            {
                "process_id": "video.ui.agent_management",
                "representation": "pack_doc",
                "path": "business/video/docs/process-maps.md",
                "status": "pack_linked",
            },
            {
                "process_id": "video.ui.project_creation",
                "representation": "pack_doc",
                "path": "business/video/docs/process-maps.md",
                "status": "pack_linked",
            },
            {
                "process_id": "video.ui.architecture_comm",
                "representation": "pack_doc",
                "path": "business/video/docs/process-maps.md",
                "status": "pack_linked",
            },
            {
                "process_id": "video.module.deep_spec",
                "representation": "pack_doc",
                "path": "business/video/docs/deep-spec-modules.md",
                "status": "pack_linked",
            },
        ]
    )
    coverage = {
        "schema_version": "1.0",
        "wave": 5,
        "va_only_count": 0,
        "processes": processes,
        "provenance": {"source_refs": ["improvements.md#wave-5"], "recorded_at": TODAY},
    }
    (VIDEO / "process_coverage.json").write_text(json.dumps(coverage, indent=2) + "\n", encoding="utf-8")
    return processes


def prepare_retention() -> None:
    policies = VIDEO / "policies"
    policies.mkdir(parents=True, exist_ok=True)
    path = policies / "roster-retention.md"
    path.write_text(
        f"""# Video Roster Retention Policy (N3)

**Effective:** {TODAY}  
**Non-negotiable:** N3 — **all 114 agents retained forever** in this pack.

## Rules

1. **Never delete** a `ROSTER.json` pack_id or `business/video/agents/<pack_id>/` directory to “simplify” the host.
2. Inventory CI (`scripts/business/inventory_check.py`) **must fail** if count ≠ 114 or MAP/standby incomplete.
3. Agents may be `draft` / `registered` / `active` / standby-routed; **retirement ≠ deletion**. Deprecate via status only.
4. Upstream va-agent-swarm updates land as pack PRs with provenance — not as justification to drop agents.
5. Other domain packs (`example_*`) must not reduce video inventory.

## Evidence

- `business/video/ROSTER.json`
- `business/video/standby_pool.json`
- `business/video/MAP.md`
- GitHub workflow `n3-inventory.yml`
""",
        encoding="utf-8",
    )


def prepare_manifest(workflow_ids: list[str]) -> None:
    path = VIDEO / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["version"] = "1.0.0"
    manifest["workflows"] = sorted(set(workflow_ids))
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def prepare_processes_md() -> None:
    text = f"""# Video Domain Pack — Process Index (N3)

**Status:** Wave 5 N3 complete — DNA or pack-linked (no va-only)  
**Entry rule:** Executable DNA enters via **video.orchestrator** and/or **video.planner**.  
**Generated/updated:** {TODAY}

---

## 1. Orchestration spine

| process_id | target_dna_id | status |
|------------|---------------|--------|
| video.spine.orchestrate | wf_video_spine_v1 | **DNA ready** |
| video.spine.plan | wf_video_spine_v1 | **DNA ready** |

## 2. Six-phase E2E

| process_id | target_dna_id | status |
|------------|---------------|--------|
| video.phase.1–6.* | wf_video_production_e2e_v1 | **DNA ready (thin)** |

## 3. Archetypes A–J

| process_id | target_dna_id | status |
|------------|---------------|--------|
| video.arch.a.viral_hook | wf_video_arch_a_viral_hook_v1 | **DNA ready** |
| video.arch.b.ugc_ad | wf_video_arch_b_ugc_ad_v1 | **DNA ready (thin)** |
| video.arch.c.animated_explainer | wf_video_arch_c_animated_explainer_v1 | **DNA ready (thin)** |
| video.arch.d.personalized_birthday | wf_video_arch_d_personalized_birthday_v1 | **DNA ready (thin)** |
| video.arch.e.ai_short_film | wf_video_arch_e_ai_short_film_v1 | **DNA ready (thin)** |
| video.arch.f.corporate_training | wf_video_arch_f_corporate_training_v1 | **DNA ready (thin)** |
| video.arch.g.music_video | wf_video_arch_g_music_video_v1 | **DNA ready (thin)** |
| video.arch.h.ai_avatar | wf_video_arch_h_ai_avatar_v1 | **DNA ready (thin)** |
| video.arch.i.documentary | wf_video_arch_i_documentary_v1 | **DNA ready (thin)** |
| video.arch.j.feature_film | wf_video_arch_j_feature_film_v1 | **DNA ready (thin)** |

## 4. LQR family

All map to `wf_video_lqr_overview_v1` (thin family entry) — **DNA ready**.

## 5. Maps / UI / deep-spec

Pack-linked under `business/video/docs/process-maps.md` and `deep-spec-modules.md` — **not va-only**.

## 6. Delivery / QC

| process_id | DNA | status |
|------------|-----|--------|
| video.delivery.package | wf_video_delivery_v1 | **DNA ready** |
| video.qc.* | wf_video_lqr_overview_v1 | **DNA ready** |

## 7. Machine index

See `process_coverage.json`, `router_table.json`, `standby_pool.json` (114 agents).

*End PROCESSES.md (Wave 5 N3)*
"""
    (VIDEO / "PROCESSES.md").write_text(text, encoding="utf-8")


def main() -> int:
    roster = json.loads((VIDEO / "ROSTER.json").read_text(encoding="utf-8"))
    assert len(roster) == 114, len(roster)

    n_agents = prepare_agents(roster)
    prepare_standby(roster)
    prepare_router(roster)
    prepare_retention()

    workflow_ids = [
        "wf_video_spine_v1",
        "wf_video_arch_a_viral_hook_v1",
        "wf_video_production_e2e_v1",
        "wf_video_lqr_overview_v1",
        "wf_video_delivery_v1",
    ]
    write_e2e_dna()
    write_thin_dna(
        "wf_video_lqr_overview_v1",
        "Video LQR Overview",
        "Look-quality-review consistency loop entry (N3).",
        ["video.aiqaconsistency", "video.editor"],
        ["va-agent-swarm/study/workflows/lqr-pipeline-overview.svg"],
    )
    write_thin_dna(
        "wf_video_delivery_v1",
        "Video Delivery Fabric",
        "Delivery / distribution package path with human gate (N3).",
        ["video.socialmediastrategist", "video.performancemarketer", "video.trailereditor"],
        ["improvements.md#wave-5"],
    )
    for letter, slug, title, specialists in ARCHETYPES:
        dna_id = f"wf_video_arch_{letter}_{slug}_v1"
        write_thin_dna(
            dna_id,
            f"Archetype {letter.upper()} — {title}",
            f"Thin vertical archetype {letter.upper()} on orchestration spine (N3).",
            specialists,
            [f"va-agent-swarm/study/workflows/{letter.upper()}-{slug.replace('_', '-')}.svg"],
        )
        workflow_ids.append(dna_id)

    prepare_process_coverage()
    prepare_manifest(workflow_ids)
    prepare_processes_md()

    print(f"WAVE5 N3 PREPARE OK agents={n_agents} workflows={len(workflow_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
