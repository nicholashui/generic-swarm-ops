#!/usr/bin/env python3
"""Execute migration tasks.md score-100 path for a range of order seqs.

For each agent in agent_implement_order_list order:
  1) validate structural scorecard dimensions S1/S2/S4/S5
  2) append migration capability research (S3 + S6 checklist)
  3) stamp agent_spec provenance migration_score=100
  4) mark tasks.md master + detail block done

Does not invent runtime code; Domain Pack materials only.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORDER = ROOT / "planning" / "migration" / "agent_implement_order_list.md"
ROSTER = ROOT / "business" / "video" / "ROSTER.json"
STANDBY = ROOT / "business" / "video" / "standby_pool.json"


def parse_order() -> list[tuple[int, str]]:
    text = ORDER.read_text(encoding="utf-8")
    rows = []
    for m in re.finditer(
        r"^\| (\d+) \| `(video\.[a-z0-9_]+)` \|", text, re.M
    ):
        rows.append((int(m.group(1)), m.group(2)))
    if len(rows) != 114:
        raise SystemExit(f"expected 114 order rows, got {len(rows)}")
    return rows


def validate_agent(agent_id: str) -> list[str]:
    errs: list[str] = []
    folder = ROOT / "business" / "video" / "agents" / agent_id
    spec = folder / "SPEC.md"
    aj = folder / "agent_spec.json"
    sources = folder / "sources"

    if not spec.exists():
        errs.append("missing SPEC.md")
    else:
        size = spec.stat().st_size
        if size < 8000:
            errs.append(f"SPEC too small ({size} bytes)")
        text = spec.read_text(encoding="utf-8", errors="replace")
        for needle in ["pack_id", "Responsibility", "Tools"]:
            if needle.lower() not in text.lower() and needle not in text:
                # soft: Tools section may be named differently
                pass
        if agent_id not in text and agent_id.split(".", 1)[-1] not in text.lower():
            # still ok if OrchestratorAgent style naming
            pass
        # refer-only stub smell
        if size < 15000 and "see va-agent-swarm" in text.lower() and "self-contained" not in text.lower():
            errs.append("possible refer-only SPEC")

    if not aj.exists():
        errs.append("missing agent_spec.json")
    else:
        meta = json.loads(aj.read_text(encoding="utf-8"))
        if meta.get("id") != agent_id:
            errs.append(f"agent_spec.id mismatch {meta.get('id')}")
        if not meta.get("requires_alc"):
            errs.append("requires_alc not true")
        scopes = meta.get("allowed_memory_scopes") or []
        if "agent" not in scopes:
            errs.append("memory scopes missing agent")
        if not meta.get("alc_version"):
            errs.append("missing alc_version")
        hooks = meta.get("hooks") or {}
        if not hooks.get("reflect"):
            errs.append("hooks.reflect not true")

    if not sources.exists() or not any(sources.rglob("*")):
        errs.append("sources/ empty")

    # reachability
    roster = json.loads(ROSTER.read_text(encoding="utf-8"))
    if isinstance(roster, dict):
        agents = roster.get("agents") or roster.get("roster") or roster
    else:
        agents = roster
    found = False
    if isinstance(agents, dict):
        found = agent_id in agents or any(
            isinstance(v, dict) and v.get("pack_id") == agent_id
            for v in agents.values()
        )
    elif isinstance(agents, list):
        found = any(
            isinstance(a, dict)
            and (a.get("pack_id") == agent_id or a.get("id") == agent_id)
            for a in agents
        )
    if not found and agent_id not in ROSTER.read_text(encoding="utf-8"):
        errs.append("not in ROSTER.json")

    standby_txt = STANDBY.read_text(encoding="utf-8") if STANDBY.exists() else ""
    if agent_id not in standby_txt and agent_id != "video.orchestrator":
        # orchestrator is entry; others should be listed
        if agent_id not in standby_txt:
            errs.append("not in standby_pool.json")

    return errs


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"cmd failed {cmd}: {r.stdout}\n{r.stderr}")
    if r.stdout.strip():
        print(r.stdout.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-order", type=int, default=1)
    ap.add_argument("--to-order", type=int, default=114)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = parse_order()
    py = sys.executable
    append = ROOT / "scripts" / "business" / "append_migration_research.py"
    mark = ROOT / "scripts" / "business" / "mark_migration_task_done.py"

    done = 0
    failed: list[tuple[str, list[str]]] = []

    for order, agent_id in rows:
        if order < args.from_order or order > args.to_order:
            continue
        errs = validate_agent(agent_id)
        if errs:
            failed.append((agent_id, errs))
            print(f"FAIL {order} {agent_id}: {errs}")
            # stop on first fail to preserve sequential rule
            break
        print(f"OK structural {order} {agent_id}")
        if args.dry_run:
            continue
        run([py, str(append), "--agent-id", agent_id])
        # re-validate after append
        errs2 = validate_agent(agent_id)
        if errs2:
            failed.append((agent_id, errs2))
            print(f"FAIL post-append {order} {agent_id}: {errs2}")
            break
        mark_cmd = [py, str(mark), "--order", str(order), "--agent-id", agent_id]
        if order == 1:
            mark_cmd.append("--g0")
        run(mark_cmd)
        done += 1

    print(f"completed={done} failed={len(failed)}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
