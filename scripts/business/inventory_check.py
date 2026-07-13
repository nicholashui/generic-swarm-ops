# -*- coding: utf-8 -*-
"""N3 video pack inventory gate — fail if roster incomplete."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "business" / "video"
ROSTER_PATH = VIDEO / "ROSTER.json"
AGENTS = VIDEO / "agents"
MAP_PATH = VIDEO / "MAP.md"

REQUIRED_SPEC_KEYS = (
    "id",
    "domain_id",
    "name",
    "status",
    "requires_alc",
    "allowed_memory_scopes",
    "alc_version",
)


def check_inventory(repo_root: Path | None = None) -> list[str]:
    root = repo_root or ROOT
    video = root / "business" / "video"
    roster_path = video / "ROSTER.json"
    agents = video / "agents"
    map_path = video / "MAP.md"
    errors: list[str] = []

    if not roster_path.is_file():
        return [f"missing {roster_path}"]
    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    if not isinstance(roster, list):
        return ["ROSTER.json must be an array"]
    if len(roster) != 114:
        errors.append(f"ROSTER length {len(roster)} != 114")

    pack_ids = []
    for row in roster:
        pid = row.get("pack_id")
        if not pid:
            errors.append(f"roster row missing pack_id: {row}")
            continue
        pack_ids.append(pid)
        d = agents / pid
        if not d.is_dir():
            errors.append(f"missing agent dir: {pid}")
            continue
        spec_path = d / "agent_spec.json"
        if not spec_path.is_file():
            errors.append(f"missing agent_spec.json: {pid}")
            continue
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"invalid agent_spec.json {pid}: {e}")
            continue
        for key in REQUIRED_SPEC_KEYS:
            if key not in spec:
                errors.append(f"{pid}: agent_spec missing {key}")
        if spec.get("requires_alc") is not True:
            errors.append(f"{pid}: requires_alc must be true")
        scopes = spec.get("allowed_memory_scopes") or []
        if "agent" not in scopes:
            errors.append(f"{pid}: allowed_memory_scopes must include 'agent'")
        if spec.get("domain_id") != "video":
            errors.append(f"{pid}: domain_id must be video")
        if not (d / "SPEC.md").is_file():
            errors.append(f"{pid}: missing SPEC.md")

    if len(set(pack_ids)) != len(pack_ids):
        errors.append("duplicate pack_id in ROSTER")

    dirs = [p.name for p in agents.iterdir() if p.is_dir()] if agents.is_dir() else []
    if len(dirs) != 114:
        errors.append(f"agent dir count {len(dirs)} != 114")
    extra = set(dirs) - set(pack_ids)
    missing = set(pack_ids) - set(dirs)
    if missing:
        errors.append(f"dirs missing for pack_ids: {sorted(missing)[:5]}...")
    if extra:
        errors.append(f"unexpected dirs not in ROSTER: {sorted(extra)[:5]}")

    if map_path.is_file():
        text = map_path.read_text(encoding="utf-8")
        data_rows = [ln for ln in text.splitlines() if ln.startswith("|") and "va_id" not in ln and "---" not in ln and "pack_id" not in ln.lower()]
        # header + separator excluded; count rows with video.
        map_rows = [ln for ln in text.splitlines() if ln.startswith("|") and "`video." in ln]
        if len(map_rows) != 114:
            errors.append(f"MAP.md pack rows {len(map_rows)} != 114")
    else:
        errors.append("missing MAP.md")

    # --- Wave 5 N3 gates ---
    standby_path = video / "standby_pool.json"
    if not standby_path.is_file():
        errors.append("missing standby_pool.json")
    else:
        try:
            standby = json.loads(standby_path.read_text(encoding="utf-8"))
            s_agents = standby.get("agents") if isinstance(standby, dict) else standby
            if not isinstance(s_agents, list):
                errors.append("standby_pool.agents must be a list")
            else:
                if len(s_agents) != 114:
                    errors.append(f"standby_pool agents {len(s_agents)} != 114")
                s_ids = {a.get("pack_id") for a in s_agents if isinstance(a, dict)}
                if s_ids != set(pack_ids):
                    missing_s = set(pack_ids) - s_ids
                    extra_s = s_ids - set(pack_ids)
                    if missing_s:
                        errors.append(f"standby missing pack_ids: {sorted(missing_s)[:5]}")
                    if extra_s:
                        errors.append(f"standby extra pack_ids: {sorted(extra_s)[:5]}")
        except json.JSONDecodeError as e:
            errors.append(f"invalid standby_pool.json: {e}")

    required_dna = [
        "wf_video_spine_v1.dna.json",
        "wf_video_arch_a_viral_hook_v1.dna.json",
        "wf_video_production_e2e_v1.dna.json",
        "wf_video_lqr_overview_v1.dna.json",
        "wf_video_delivery_v1.dna.json",
        "wf_video_arch_b_ugc_ad_v1.dna.json",
        "wf_video_arch_c_animated_explainer_v1.dna.json",
        "wf_video_arch_d_personalized_birthday_v1.dna.json",
        "wf_video_arch_e_ai_short_film_v1.dna.json",
        "wf_video_arch_f_corporate_training_v1.dna.json",
        "wf_video_arch_g_music_video_v1.dna.json",
        "wf_video_arch_h_ai_avatar_v1.dna.json",
        "wf_video_arch_i_documentary_v1.dna.json",
        "wf_video_arch_j_feature_film_v1.dna.json",
    ]
    wf_dir = video / "workflows"
    for name in required_dna:
        if not (wf_dir / name).is_file():
            errors.append(f"missing required DNA: {name}")

    coverage_path = video / "process_coverage.json"
    if not coverage_path.is_file():
        errors.append("missing process_coverage.json")
    else:
        try:
            coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
            procs = coverage.get("processes") or []
            if not procs:
                errors.append("process_coverage has no processes")
            va_only = [
                p
                for p in procs
                if (p.get("status") or "").lower() in {"va-only", "va_only", "index"}
                or p.get("representation") == "va_only"
            ]
            # Wave 5: disallow explicit va-only; allow dna_ready / pack_linked only
            bad = [
                p
                for p in procs
                if p.get("status") not in {"dna_ready", "pack_linked"}
                or p.get("representation") not in {"dna", "pack_doc"}
            ]
            if bad:
                errors.append(f"process_coverage incomplete/va-only count={len(bad)} e.g. {bad[0].get('process_id')}")
            if coverage.get("va_only_count", 0) not in (0, None):
                errors.append(f"va_only_count must be 0, got {coverage.get('va_only_count')}")
            for p in procs:
                rel = p.get("path") or ""
                if rel and not (root / rel).is_file():
                    errors.append(f"process path missing: {rel}")
        except json.JSONDecodeError as e:
            errors.append(f"invalid process_coverage.json: {e}")

    if not (video / "router_table.json").is_file():
        errors.append("missing router_table.json")
    if not (video / "policies" / "roster-retention.md").is_file():
        errors.append("missing policies/roster-retention.md")

    # Registered readiness: every agent_spec status registered or active
    for pid in pack_ids:
        spec_path = agents / pid / "agent_spec.json"
        if not spec_path.is_file():
            continue
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        st = (spec.get("status") or "").lower()
        if st not in {"registered", "active"}:
            errors.append(f"{pid}: status must be registered|active for N3, got {st!r}")

    return errors


def main() -> int:
    errs = check_inventory()
    if errs:
        print("INVENTORY FAIL")
        for e in errs:
            print(" -", e)
        return 1
    print("INVENTORY PASS count=114 n3=complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
