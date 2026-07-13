"""Unit tests for video archetype A–J workflow selection."""
from __future__ import annotations

from pathlib import Path

import pytest

from app.domain.workflows.archetype_selector import load_registry, recommend_workflow

REPO = Path(__file__).resolve().parents[4]


def test_registry_loads_ten_archetypes() -> None:
    reg = load_registry(repo_root=REPO)
    arches = reg.get("archetypes") or []
    assert len(arches) == 10
    codes = {a["code"] for a in arches}
    assert codes == set("ABCDEFGHIJ")
    for a in arches:
        dna = REPO / a["dna_path"]
        assert dna.is_file(), f"missing DNA {dna}"


def test_recommend_viral_hook() -> None:
    out = recommend_workflow(
        "Make a 15s viral TikTok hook meme about coffee",
        duration_sec=15,
        repo_root=REPO,
    )
    assert out["recommendation"]["code"] == "A"
    assert out["recommendation"]["dna_id"] == "wf_video_arch_a_viral_hook_v1"
    assert out["hitl_confirm_required"] is True
    assert out["inferred_scale"] in {"S1", "S2"}


def test_recommend_ugc_ad() -> None:
    out = recommend_workflow(
        "UGC performance ad for Meta ads, optimize ROAS, creator testimonial CTA",
        duration_sec=30,
        repo_root=REPO,
        channel_hint="paid social",
    )
    assert out["recommendation"]["code"] == "B"
    assert "ugc" in out["recommendation"]["dna_id"]


def test_recommend_training() -> None:
    out = recommend_workflow(
        "Corporate LMS onboarding compliance training module for new hires",
        duration_sec=600,
        repo_root=REPO,
    )
    assert out["recommendation"]["code"] == "F"


def test_recommend_short_film() -> None:
    out = recommend_workflow(
        "Cinematic multi-scene short film narrative drama with character arc",
        duration_sec=120,
        repo_root=REPO,
    )
    assert out["recommendation"]["code"] == "E"


def test_recommend_feature_film_scale() -> None:
    out = recommend_workflow(
        "Feature-length theatrical feature film movie, 100 minutes",
        duration_sec=6000,
        repo_root=REPO,
    )
    assert out["recommendation"]["code"] == "J"
    assert out["recommendation"]["recommended_scale"] == "S7"


def test_empty_brief_raises() -> None:
    with pytest.raises(ValueError):
        recommend_workflow("", repo_root=REPO)


def test_ugc_and_short_film_dna_phased() -> None:
    import json

    b = json.loads((REPO / "business/video/workflows/wf_video_arch_b_ugc_ad_v1.dna.json").read_text(encoding="utf-8"))
    e = json.loads((REPO / "business/video/workflows/wf_video_arch_e_ai_short_film_v1.dna.json").read_text(encoding="utf-8"))
    assert b["provenance"]["depth"] == "phased_v1"
    assert e["provenance"]["depth"] == "phased_v1"
    assert any(s["agent"] == "video.ugccreator" for s in b["steps"])
    assert any(s["agent"] == "video.storyboard" for s in e["steps"])
    assert b["steps"][-1]["human_gate_required"] is True
