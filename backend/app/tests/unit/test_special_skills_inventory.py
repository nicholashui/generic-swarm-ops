"""Inventory + score integrity for planning/special skills host integrations."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "backend"))

# Import scoring helpers from the shipped implementer module path via exec load
IMPL_SCRIPT = ROOT / "scripts" / "business" / "implement_and_score_special_skills.py"


def _load_impl_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "implement_and_score_special_skills", IMPL_SCRIPT
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_seventeen_skill_plans_exist() -> None:
    plans = sorted(
        p.stem
        for p in (ROOT / "planning" / "special").glob("*.md")
        if p.name not in {"README.md", "special_skill_impl_score.md"}
    )
    assert len(plans) == 17, plans


def test_each_skill_has_integration_not_plan_only() -> None:
    mod = _load_impl_module()
    skills = mod.list_skill_plans()
    assert len(skills) == 17
    for sid in skills:
        integ = ROOT / "business" / "video" / "special_skills" / sid / "integration.json"
        skill_md = ROOT / "business" / "video" / "special_skills" / sid / "SKILL.md"
        assert integ.is_file(), f"missing integration for {sid}"
        assert skill_md.is_file(), f"missing SKILL.md for {sid}"
        data = json.loads(integ.read_text(encoding="utf-8"))
        assert data.get("skill_id") == sid
        assert data.get("status") == "mvp_integrated"
        # evidence not empty: plan + at least agents or modules or dna
        assert data.get("plan")
        has_binding = bool(data.get("agents") or data.get("dna") or data.get("modules"))
        assert has_binding, f"{sid} has no binding targets"


def test_bound_agents_and_dna_exist_on_disk() -> None:
    mod = _load_impl_module()
    for sid in mod.list_skill_plans():
        binding = mod.BINDINGS[sid]
        for a in binding.get("agents") or []:
            folder = ROOT / "business" / "video" / "agents" / a
            assert folder.is_dir(), f"{sid}: missing agent {a}"
            assert (folder / "agent_spec.json").is_file()
            assert (folder / "SPEC.md").is_file()
        for d in binding.get("dna") or []:
            path = ROOT / "business" / "video" / "workflows" / f"{d}.dna.json"
            assert path.is_file(), f"{sid}: missing DNA {d}"
            data = json.loads(path.read_text(encoding="utf-8"))
            assert data.get("id") == d
            assert isinstance(data.get("steps"), list) and len(data["steps"]) >= 1
        for m in binding.get("modules") or []:
            assert (ROOT / m).exists(), f"{sid}: missing module {m}"


def test_score_file_has_seventeen_rows_and_rubric() -> None:
    path = ROOT / "planning" / "special" / "special_skill_impl_score.md"
    assert path.is_file(), "score file missing — run implement_and_score_special_skills.py"
    text = path.read_text(encoding="utf-8")
    assert "100 = full mark" in text or "**100 = full mark**" in text
    assert "## Rubric" in text or "Rubric (max 100)" in text
    # count skill rows in master table: lines with `skill_id` backticks after table header
    rows = re.findall(r"^\| `([a-z0-9_]+)` \|", text, re.M)
    # filter only those that are known skills
    mod = _load_impl_module()
    skills = set(mod.list_skill_plans())
    found = [r for r in rows if r in skills]
    assert len(set(found)) == 17, found


def test_score_skill_function_uses_real_bindings() -> None:
    """Drive shipped scorer; totals must be in 0..100 and reflect real agent existence."""
    mod = _load_impl_module()
    # pick agent-heavy skill
    sid = "research_agent"
    plan = ROOT / "planning" / "special" / f"{sid}.md"
    # ensure integration written
    mod.write_integration(sid, mod.BINDINGS[sid], plan)
    result = mod.score_skill(sid, mod.BINDINGS[sid], plan)
    assert 0 <= result["total"] <= 100
    assert result["skill_id"] == sid
    assert "dims" in result and set(result["dims"]) == {"D1", "D2", "D3", "D4", "D5", "D6"}
    # research agents exist → D3 should be strong
    assert result["dims"]["D3"] >= 15
    # full_mark only if total 100 and all max
    if result["full_mark"]:
        assert result["total"] == 100


def test_registry_json_count() -> None:
    reg = ROOT / "business" / "video" / "special_skills" / "REGISTRY.json"
    assert reg.is_file()
    data = json.loads(reg.read_text(encoding="utf-8"))
    assert data.get("skill_count") == 17
    assert len(data.get("skills") or []) == 17
