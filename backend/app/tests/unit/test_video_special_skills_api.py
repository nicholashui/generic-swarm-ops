"""Special skills list + recommend path via runtime (shipped product slice)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.runtime import runtime


def _admin():
    token = runtime.issue_token("admin@example.com", "admin-password")
    return runtime.authenticate(token["access_token"])


def test_list_video_special_skills_count_from_registry():
    admin = _admin()
    data = runtime.list_video_special_skills(admin)
    assert data["count"] == 17
    assert len(data["skills"]) == 17
    ids = {s["skill_id"] for s in data["skills"]}
    assert "research_agent" in ids
    assert "agent_loop_v3" in ids
    for s in data["skills"]:
        assert s.get("status") == "mvp_integrated" or s.get("kind")
        assert "integration_path" in s
    # scores optional but should parse for most
    scored = [s for s in data["skills"] if isinstance(s.get("score"), int)]
    assert len(scored) >= 10


def test_recommend_video_workflow_viral_hook_shape():
    admin = _admin()
    out = runtime.recommend_video_workflow(
        admin,
        brief="15s viral TikTok hook about coffee",
        duration_sec=15,
        top_k=3,
    )
    rec = out.get("recommendation") or {}
    assert rec.get("dna_id")
    assert rec.get("process_id") or rec.get("code")
    assert rec["dna_id"].startswith("wf_video_")
    assert "alternatives" in out
    assert isinstance(out.get("confidence"), (int, float))
