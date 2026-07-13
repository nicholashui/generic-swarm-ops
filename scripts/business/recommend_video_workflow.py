#!/usr/bin/env python3
"""CLI: recommend video archetype DNA from a brief.

  python scripts/business/recommend_video_workflow.py "15s TikTok viral hook"
  python scripts/business/recommend_video_workflow.py --duration 120 "short film drama"
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app.domain.workflows.archetype_selector import recommend_workflow  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="Recommend video workflow DNA for a brief")
    ap.add_argument("brief", nargs="+", help="Production brief text")
    ap.add_argument("--duration", type=int, default=None, help="Duration in seconds")
    ap.add_argument("--top-k", type=int, default=3)
    ap.add_argument("--channel", default=None)
    ap.add_argument("--budget", default=None)
    args = ap.parse_args()
    brief = " ".join(args.brief)
    out = recommend_workflow(
        brief,
        duration_sec=args.duration,
        top_k=args.top_k,
        repo_root=ROOT,
        channel_hint=args.channel,
        budget_hint=args.budget,
    )
    # compact view
    rec = out["recommendation"]
    print(
        json.dumps(
            {
                "recommendation": {
                    "code": rec.get("code"),
                    "name": rec.get("name"),
                    "dna_id": rec.get("dna_id"),
                    "process_id": rec.get("process_id"),
                    "scale": rec.get("recommended_scale"),
                    "score": rec.get("score"),
                    "reasons": rec.get("reasons"),
                },
                "confidence": out["confidence"],
                "hitl_confirm_required": out["hitl_confirm_required"],
                "alternatives": [
                    {
                        "code": a.get("code"),
                        "dna_id": a.get("dna_id"),
                        "score": a.get("score"),
                    }
                    for a in out.get("alternatives") or []
                ],
                "how_to_run": out.get("how_to_run"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
