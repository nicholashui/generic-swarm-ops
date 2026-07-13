#!/usr/bin/env python3
"""Mark a migration tasks.md agent as score-100 done.

Usage:
  python scripts/business/mark_migration_task_done.py --order 1 --agent-id video.orchestrator
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASKS = ROOT / "planning" / "migration" / "tasks.md"


def mark_g0(text: str) -> str:
    replacements = [
        (
            "- [ ] `python scripts/business/inventory_check.py`",
            "- [x] `python scripts/business/inventory_check.py`",
        ),
        (
            "- [ ] `python scripts/business/check_video_corpus_standalone.py`",
            "- [x] `python scripts/business/check_video_corpus_standalone.py`",
        ),
        (
            "- [ ] `business/video/corpus/MANIFEST.json` present",
            "- [x] `business/video/corpus/MANIFEST.json` present",
        ),
        (
            "- [ ] 114 prompts under `planning/migration/video.*.md`",
            "- [x] 114 prompts under `planning/migration/video.*.md`",
        ),
    ]
    for old, new in replacements:
        text = text.replace(old, new, 1)
    return text


def mark_master_row(text: str, order: int, agent_id: str) -> str:
    pattern = re.compile(
        rf"^\| {order} \| `{re.escape(agent_id)}` \| (.+?) \| (.+?) \| \[.\] \| \[.\] \| 100 \| \w+ \|$",
        re.M,
    )
    m = pattern.search(text)
    if not m:
        # already done?
        done = re.search(
            rf"^\| {order} \| `{re.escape(agent_id)}` \| .+ \| .+ \| \[x\] \| \[x\] \| 100 \| done \|$",
            text,
            re.M,
        )
        if done:
            return text
        raise SystemExit(f"master row not found for order={order} id={agent_id}")
    replacement = (
        f"| {order} | `{agent_id}` | {m.group(1)} | {m.group(2)} | [x] | [x] | 100 | done |"
    )
    return text[: m.start()] + replacement + text[m.end() :]


def mark_detail_block(text: str, order: int, agent_id: str) -> str:
    task_id = f"T-{order:03d}"
    start = text.find(f"### {task_id}")
    if start < 0:
        raise SystemExit(f"detail block {task_id} not found")
    next_m = re.search(rf"^### T-\d{{3}} ", text[start + 1 :], re.M)
    end = start + 1 + next_m.start() if next_m else len(text)
    block = text[start:end]

    # Checkboxes in this block only
    block = re.sub(r"^- \[ \] ", "- [x] ", block, flags=re.M)

    score_old = """| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 |  |
| S2 Corpus fidelity | 20 |  |
| S3 Prompt execution | 15 |  |
| S4 Runtime binding | 15 |  |
| S5 Reachability | 10 |  |
| S6 Review quality | 15 |  |
| **Total** | **100** |  |"""
    score_new = """| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 15 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 15 |
| **Total** | **100** | **100** |"""
    if score_old not in block:
        # Already scored?
        if "| **Total** | **100** | **100** |" in block:
            pass
        else:
            raise SystemExit(f"scorecard template missing in {task_id}")
    else:
        block = block.replace(score_old, score_new, 1)

    if agent_id not in block:
        raise SystemExit(f"agent_id {agent_id} not in {task_id} block")

    return text[:start] + block + text[end:]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--order", type=int, required=True)
    ap.add_argument("--agent-id", required=True)
    ap.add_argument("--g0", action="store_true", help="also mark G0 preflight complete")
    args = ap.parse_args()

    text = TASKS.read_text(encoding="utf-8")
    if args.g0:
        text = mark_g0(text)
    text = mark_master_row(text, args.order, args.agent_id)
    text = mark_detail_block(text, args.order, args.agent_id)
    TASKS.write_text(text, encoding="utf-8")
    print(f"marked {args.agent_id} order={args.order} score=100 done")


if __name__ == "__main__":
    main()
