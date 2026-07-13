"""Wave 0 N3 inventory gate — drives scripts/business/inventory_check.py."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "scripts" / "business"
sys.path.insert(0, str(SCRIPTS))

from inventory_check import check_inventory  # noqa: E402


class DomainPackInventoryTests(unittest.TestCase):
    def test_video_pack_inventory_passes(self):
        errors = check_inventory(ROOT)
        self.assertEqual(errors, [], msg="; ".join(errors))

    def test_missing_agent_dir_detected(self):
        roster_path = ROOT / "business" / "video" / "ROSTER.json"
        roster = json.loads(roster_path.read_text(encoding="utf-8"))
        self.assertEqual(len(roster), 114)
        # Simulate incomplete tree via temp copy of roster with fake pack_id
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            video = tmp_root / "business" / "video"
            agents = video / "agents"
            agents.mkdir(parents=True)
            # only one agent
            pid = roster[0]["pack_id"]
            d = agents / pid
            d.mkdir()
            (d / "agent_spec.json").write_text(
                json.dumps(
                    {
                        "id": pid,
                        "domain_id": "video",
                        "name": "x",
                        "status": "draft",
                        "requires_alc": True,
                        "allowed_memory_scopes": ["agent"],
                        "alc_version": "1.0",
                    }
                ),
                encoding="utf-8",
            )
            (d / "SPEC.md").write_text("# x\n", encoding="utf-8")
            (video / "ROSTER.json").write_text(json.dumps(roster), encoding="utf-8")
            (video / "MAP.md").write_text("| va_id |\n", encoding="utf-8")
            errors = check_inventory(tmp_root)
            self.assertTrue(any("114" in e or "missing" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
