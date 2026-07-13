"""Wave 2 video spine E2E — register pack, activate spine, run DNA, approve, reflect."""
from __future__ import annotations

import json
import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.infrastructure.tools.adapters import execute_tool
from app.runtime import runtime

ROOT = Path(__file__).resolve().parents[4]
SPINE_AGENTS = {
    "video.orchestrator": ["audit_log_writer"],
    "video.planner": ["audit_log_writer"],
    "video.director": ["audit_log_writer", "video_media_gen_stub"],
    "video.screenwriter": ["video_script_format"],
    "video.webresearch": ["audit_log_writer"],
    "video.aiqaconsistency": ["video_qc_stub"],
    "video.producer": ["video_package_stub", "audit_log_writer"],
}


class VideoSpineE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])
        # Refresh tools so video stubs are present
        org = cls.admin.organization_id
        tools = runtime.loader.load_tools(org)
        by_id = {t["id"]: t for t in runtime.store.collection("tools") if t.get("organization_id") == org}
        for t in tools:
            if t["id"] not in by_id:
                runtime.store.collection("tools").append(t)
            else:
                by_id[t["id"]].update(t)
        runtime.store.save()

    def test_video_tool_stubs_execute(self):
        for tid in (
            "video_media_gen_stub",
            "video_script_format",
            "video_qc_stub",
            "video_package_stub",
        ):
            effect = execute_tool(tid, {"message": "wave2", "run_id": "t"})
            self.assertEqual(effect.get("status"), "ok")
            self.assertEqual(effect.get("tool_id"), tid)

    def test_standby_pool_covers_roster(self):
        roster = json.loads((ROOT / "business/video/ROSTER.json").read_text(encoding="utf-8"))
        pool = json.loads((ROOT / "business/video/standby_pool.json").read_text(encoding="utf-8"))
        self.assertEqual(len(roster), 114)
        self.assertEqual(len(pool["agents"]), 114)
        pack_ids = {a["pack_id"] for a in pool["agents"]}
        self.assertEqual(pack_ids, {r["pack_id"] for r in roster})

    def test_viral_hook_spine_run_with_gate_and_alc(self):
        # Register video pack (loads agents as draft)
        reg = runtime.register_domain_pack(
            self.admin,
            manifest_path="business/video/manifest.json",
        )
        self.assertEqual(reg["domain_id"], "video")
        self.assertGreaterEqual(reg["agents_loaded"], 7)

        # Activate spine agents with ALC + tools
        for agent_id, tools in SPINE_AGENTS.items():
            agent = next(
                (
                    a
                    for a in runtime.store.collection("agents")
                    if a.get("id") == agent_id
                    and a.get("organization_id") == self.admin.organization_id
                ),
                None,
            )
            self.assertIsNotNone(agent, agent_id)
            agent["requires_alc"] = True
            agent["alc_version"] = "1.0"
            agent["allowed_memory_scopes"] = ["agent", "organization_memory", "workflow_memory"]
            agent["hooks"] = {"reflect": True}
            agent["allowed_tools"] = list(tools)
            agent["domain_id"] = "video"
            runtime.store.save()
            updated = runtime.update_agent_status(self.admin, agent_id, "active")
            self.assertEqual(updated["status"], "active", agent_id)

        dna = json.loads(
            (ROOT / "business/video/workflows/wf_video_arch_a_viral_hook_v1.dna.json").read_text(
                encoding="utf-8"
            )
        )
        wf_id = f"{dna['id']}_{uuid.uuid4().hex[:6]}"
        runtime.create_workflow(
            self.admin,
            {
                "id": wf_id,
                "name": dna["name"],
                "description": dna["objective"],
                "risk_tier": dna["risk_tier"],
                "status": "active",
                "production_ready": False,
                "steps": dna["steps"],
                "memory_reads": dna.get("memory_reads") or ["organization_memory"],
                "memory_writes": dna.get("memory_writes") or ["event_log"],
                "guardrails": dna.get("guardrails"),
                "verification": dna.get("verification"),
                "rollback": dna.get("rollback"),
                "fitness_metrics": dna.get("fitness_metrics"),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "hook_concept": {"type": "string"},
                        "platform": {"type": "string"},
                    },
                    "required": [],
                },
                "output_schema": {"type": "object", "properties": {}, "required": []},
                "provenance": dna.get("provenance"),
            },
        )

        run = runtime.start_workflow_run(
            wf_id,
            self.admin,
            {"hook_concept": "AI curiosity open", "platform": "short_form"},
        )
        runtime.dispatch_queued_runs(self.admin)
        run = runtime.get_run(self.admin, run["id"])

        safety = 0
        while run.get("status") == "waiting_for_approval" and safety < 8:
            reviewer = runtime.authenticate(
                runtime.issue_token("reviewer@example.com", "reviewer-password")["access_token"]
            )
            runtime.decide_approval(
                run["approval_request_id"],
                "approved",
                "wave2 spine package gate",
                reviewer,
            )
            run = runtime.get_run(self.admin, run["id"])
            safety += 1

        self.assertEqual(run.get("status"), "completed", msg=run.get("error"))
        steps = {s["id"]: s for s in run.get("steps") or []}
        self.assertEqual(steps.get("publish_hook", {}).get("status"), "completed")
        # Injected lessons field present on at least one step after first reflect cycle
        reflection = runtime.reflect_on_workflow_run(self.admin, run["id"])
        stored = reflection.get("stored_lessons") or []
        self.assertTrue(stored)
        agent_ids = {l.get("agent_id") for l in stored if l.get("agent_id")}
        self.assertTrue(agent_ids & set(SPINE_AGENTS.keys()))

        metrics = runtime.improvement_metrics(self.admin, agent_id="video.orchestrator")
        self.assertIn("knowledge_growth_count", metrics)


if __name__ == "__main__":
    unittest.main()
