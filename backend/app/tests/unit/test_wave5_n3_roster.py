"""Wave 5: N3 full roster reachability + process wiring."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.runtime import runtime

# inventory script lives outside backend package
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts" / "business"))
from inventory_check import check_inventory  # type: ignore  # noqa: E402


class Wave5N3RosterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])
        cls.repo_root = runtime.repo_root
        cls.video = cls.repo_root / "business" / "video"

    def test_inventory_n3_pass(self):
        errs = check_inventory(self.repo_root)
        self.assertEqual(errs, [], errs)

    def test_roster_and_standby_114_no_orphans(self):
        roster = json.loads((self.video / "ROSTER.json").read_text(encoding="utf-8"))
        standby = json.loads((self.video / "standby_pool.json").read_text(encoding="utf-8"))
        r_ids = {r["pack_id"] for r in roster}
        s_ids = {a["pack_id"] for a in standby["agents"]}
        self.assertEqual(len(r_ids), 114)
        self.assertEqual(len(s_ids), 114)
        self.assertEqual(r_ids, s_ids)
        self.assertEqual(standby.get("entry"), "video.orchestrator")

    def test_all_agents_registered_alc(self):
        roster = json.loads((self.video / "ROSTER.json").read_text(encoding="utf-8"))
        for row in roster:
            pid = row["pack_id"]
            spec = json.loads((self.video / "agents" / pid / "agent_spec.json").read_text(encoding="utf-8"))
            self.assertIn(spec.get("status"), {"registered", "active"}, pid)
            self.assertTrue(spec.get("requires_alc"), pid)
            self.assertIn("agent", spec.get("allowed_memory_scopes") or [], pid)
            self.assertTrue(spec.get("alc_version"), pid)
            self.assertTrue((spec.get("hooks") or {}).get("reflect"), pid)

    def test_required_dna_exist_orchestrator_entry(self):
        required = [
            "wf_video_spine_v1.dna.json",
            "wf_video_arch_a_viral_hook_v1.dna.json",
            "wf_video_production_e2e_v1.dna.json",
            "wf_video_lqr_overview_v1.dna.json",
            "wf_video_delivery_v1.dna.json",
            "wf_video_arch_b_ugc_ad_v1.dna.json",
            "wf_video_arch_j_feature_film_v1.dna.json",
        ]
        for name in required:
            path = self.video / "workflows" / name
            self.assertTrue(path.is_file(), name)
            dna = json.loads(path.read_text(encoding="utf-8"))
            steps = dna.get("steps") or []
            self.assertTrue(steps, name)
            first_agent = steps[0].get("agent")
            self.assertIn(first_agent, {"video.orchestrator", "video.planner"}, name)
            # all step agents are pack ids
            for step in steps:
                agent = step.get("agent")
                self.assertTrue(str(agent).startswith("video."), f"{name} {agent}")

    def test_process_coverage_no_va_only(self):
        cov = json.loads((self.video / "process_coverage.json").read_text(encoding="utf-8"))
        self.assertEqual(cov.get("va_only_count"), 0)
        procs = cov.get("processes") or []
        self.assertGreaterEqual(len(procs), 20)
        for p in procs:
            self.assertIn(p.get("representation"), {"dna", "pack_doc"}, p)
            self.assertIn(p.get("status"), {"dna_ready", "pack_linked"}, p)
            path = self.repo_root / (p.get("path") or "")
            self.assertTrue(path.is_file(), p.get("path"))

    def test_router_table_categories(self):
        router = json.loads((self.video / "router_table.json").read_text(encoding="utf-8"))
        cats = router.get("categories") or {}
        self.assertEqual(router.get("entry"), "video.orchestrator")
        self.assertGreaterEqual(len(cats), 10)
        total = sum(len(v) for v in cats.values())
        self.assertEqual(total, 114)

    def test_runtime_n3_status(self):
        status = runtime.video_n3_roster_status(self.admin)
        self.assertEqual(status["roster_count"], 114)
        self.assertEqual(status["standby_count"], 114)
        self.assertEqual(status["orphans"], [])
        self.assertTrue(status["n3_complete"])
        self.assertGreaterEqual(status["dna_count"], 14)
        self.assertEqual(status["process_coverage"]["va_only"], 0)
        self.assertEqual(status["registered_or_active"], 114)

    def test_retention_policy_present(self):
        path = self.video / "policies" / "roster-retention.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("114", text)
        self.assertIn("Never delete", text)

    def test_register_video_pack_loads_roster(self):
        result = runtime.register_domain_pack(
            self.admin,
            manifest_path="business/video/manifest.json",
        )
        self.assertEqual(result["domain_id"], "video")
        self.assertGreaterEqual(result.get("agents_loaded") or result.get("agent_count") or 0, 100)


if __name__ == "__main__":
    unittest.main()
