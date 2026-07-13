"""Standalone video corpus (migration_plan) — real filesystem + check script."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
VIDEO = ROOT / "business" / "video"
CORPUS = VIDEO / "corpus"


class VideoCorpusStandaloneTests(unittest.TestCase):
    def test_manifest_and_agents_md(self):
        man_path = CORPUS / "MANIFEST.json"
        self.assertTrue(man_path.is_file(), "corpus MANIFEST.json missing — run migrate_va_corpus.py")
        man = json.loads(man_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(man.get("file_count") or len(man.get("files") or []), 300)
        agents_md = CORPUS / "study" / "agents.md"
        self.assertTrue(agents_md.is_file())
        text = agents_md.read_text(encoding="utf-8")
        self.assertIn("DirectorAgent", text)
        self.assertIn("OrchestratorAgent", text)

    def test_all_specs_have_responsibility(self):
        roster = json.loads((VIDEO / "ROSTER.json").read_text(encoding="utf-8"))
        self.assertEqual(len(roster), 114)
        for row in roster:
            pack_id = row["pack_id"]
            spec = VIDEO / "agents" / pack_id / "SPEC.md"
            self.assertTrue(spec.is_file(), pack_id)
            body = spec.read_text(encoding="utf-8")
            self.assertIn("## Responsibility", body, pack_id)
            self.assertTrue(
                "## Common structure" in body or "Common Structure" in body,
                pack_id,
            )
            self.assertGreaterEqual(len(body), 8000, pack_id)
            # self-contained: not a refer-only stub
            self.assertNotIn("deep SPEC:** deferred", body, pack_id)
            sources = VIDEO / "agents" / pack_id / "sources"
            self.assertTrue(sources.is_dir() or len(body) > 20000, pack_id)
            # no bare external study refs outside comments
            for line in body.splitlines():
                if "<!--" in line:
                    continue
                self.assertNotIn("va-agent-swarm/study", line, f"{pack_id}: {line}")

    def test_check_script_exit_zero(self):
        script = ROOT / "scripts" / "business" / "check_video_corpus_standalone.py"
        self.assertTrue(script.is_file())
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("STANDALONE PASS", proc.stdout)

    def test_key_corpus_files_exist(self):
        for rel in (
            "study/SYSTEM_REFERENCE.md",
            "study/workflows/A-viral-hook.svg",
            "study/reference/how_to_build_a_video_agent_system/chapter_01.txt",
            "plan/planner_agent_v2.1.md",
            "SOURCE_COMMIT.txt",
        ):
            self.assertTrue((CORPUS / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()
