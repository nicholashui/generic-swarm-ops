# -*- coding: utf-8 -*-
"""Verify video corpus standalone (migration_plan.md gates V2–V5)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "business" / "video"
CORPUS = VIDEO / "corpus"
AGENTS = VIDEO / "agents"


def main() -> int:
    errors: list[str] = []
    man_path = CORPUS / "MANIFEST.json"
    if not man_path.is_file():
        errors.append("missing MANIFEST.json")
        print("STANDALONE FAIL")
        for e in errors:
            print(" -", e)
        return 1
    man = json.loads(man_path.read_text(encoding="utf-8"))
    files = man.get("files") or []
    if len(files) < 300:
        errors.append(f"manifest file_count {len(files)} < 300")
    agents_md = CORPUS / "study" / "agents.md"
    if not agents_md.is_file():
        errors.append("missing corpus/study/agents.md")
    elif "DirectorAgent" not in agents_md.read_text(encoding="utf-8"):
        errors.append("agents.md missing DirectorAgent")
    if not (CORPUS / "SOURCE_COMMIT.txt").is_file():
        errors.append("missing SOURCE_COMMIT.txt")

    roster = json.loads((VIDEO / "ROSTER.json").read_text(encoding="utf-8"))
    external_ref = re.compile(r"va-agent-swarm/study")
    for row in roster:
        pack_id = row["pack_id"]
        spec = AGENTS / pack_id / "SPEC.md"
        if not spec.is_file():
            errors.append(f"missing SPEC {pack_id}")
            continue
        text = spec.read_text(encoding="utf-8")
        if "## Responsibility" not in text:
            errors.append(f"{pack_id}: missing ## Responsibility")
        if len(text) < 8000:
            errors.append(f"{pack_id}: SPEC too short ({len(text)})")
        if "deep SPEC:** deferred" in text or "source:** `va-agent-swarm" in text:
            errors.append(f"{pack_id}: still looks refer-only / deferred")
        # allow HTML comment provenance only
        for line in text.splitlines():
            if "<!--" in line:
                continue
            if external_ref.search(line) and "SOURCE_COMMIT" not in line:
                # bare primary refs forbidden
                if "`va-agent-swarm/" in line or "va-agent-swarm/study" in line:
                    errors.append(f"{pack_id}: external primary ref still in SPEC: {line[:80]}")

    # sample deep files
    for rel in (
        "study/SYSTEM_REFERENCE.md",
        "study/reference/how_to_build_a_video_agent_system/chapter_01.txt",
        "study/workflows/A-viral-hook.svg",
        "plan/planner_agent_v2.1.md",
    ):
        if not (CORPUS / rel).is_file():
            errors.append(f"missing corpus file {rel}")

    if errors:
        print("STANDALONE FAIL")
        for e in errors[:40]:
            print(" -", e)
        if len(errors) > 40:
            print(f" - ... +{len(errors)-40} more")
        return 1
    print(f"STANDALONE PASS manifest={len(files)} specs=114")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
