# -*- coding: utf-8 -*-
"""Expand business/video/agents/*/SPEC.md from corpus study/agents.md (join on va_id)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "business" / "video"
AGENTS_MD = VIDEO / "corpus" / "study" / "agents.md"
ROSTER = VIDEO / "ROSTER.json"
AGENTS_DIR = VIDEO / "agents"

ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$"
)


def strip_md(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    return s.strip()


def parse_agents_md(path: Path) -> dict[int, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    by_id: dict[int, dict[str, str]] = {}
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        va_id = int(m.group(1))
        if va_id < 1 or va_id > 114:
            continue
        # Prefer first full 10-column agent table row for each id
        if va_id in by_id and by_id[va_id].get("responsibility"):
            # section 11 may re-use numbers — keep first complete row
            continue
        by_id[va_id] = {
            "va_id": str(va_id),
            "agent_name": strip_md(m.group(2)),
            "responsibility": strip_md(m.group(3)),
            "knowledge_sources": strip_md(m.group(4)),
            "self_quality": strip_md(m.group(5)),
            "surpass_human": strip_md(m.group(6)),
            "accepts_critique_from": strip_md(m.group(7)),
            "comments_on": strip_md(m.group(8)),
            "tool_access_design": strip_md(m.group(9)),
            "architecture_pattern": strip_md(m.group(10)),
        }
    return by_id


def render_spec(roster_row: dict, table: dict[str, str], related: list[str]) -> str:
    pack_id = roster_row["pack_id"]
    va_id = roster_row["id"]
    name = roster_row.get("name") or table.get("agent_name") or pack_id
    cat = roster_row.get("category") or ""
    related_lines = "\n".join(f"- `{p}`" for p in related) if related else "- _(see corpus INDEX)_"
    return f"""# {name}

## Identity

| Field | Value |
|-------|-------|
| **va_id** | {va_id} |
| **pack_id** | `{pack_id}` |
| **category** | {cat} |
| **domain_id** | `video` |
| **host** | generic-swarm-ops Domain Pack |

## Responsibility

{table.get("responsibility") or "_(missing from agents.md parse)_"}

## Knowledge distillation sources (design-time)

{table.get("knowledge_sources") or "—"}

> Content for these sources is mirrored under `business/video/corpus/` where applicable.  
> **Do not** treat design-time vendor/tool names as automatic runtime allow-list entries.

## Self-quality criteria

{table.get("self_quality") or "—"}

## Surpass-human signal

{table.get("surpass_human") or "—"}

## Critique bus

- **Accepts critique from:** {table.get("accepts_critique_from") or "—"}
- **Comments on:** {table.get("comments_on") or "—"}

## Tools (design-time notes from va roster)

{table.get("tool_access_design") or "—"}

Runtime tools on this host are declared only in `agent_spec.json` / tool-permission-register (stubs first).

## Architecture pattern

{table.get("architecture_pattern") or "—"}

## Runtime binding (generic host)

- Spec file: `business/video/agents/{pack_id}/agent_spec.json`
- Standby: `business/video/standby_pool.json` (orchestrator-reachable)
- DNA steps: see `business/video/workflows/*.dna.json` and `process_coverage.json`

## Related local documents (in-pack corpus)

{related_lines}

## Provenance

- Embedded from in-pack copy of `business/video/corpus/study/agents.md` (table row **{va_id}**).
- Original upstream: va-agent-swarm (see `business/video/corpus/SOURCE_COMMIT.txt`).
- N3: do not delete this directory; full design text lives **in this repo**.

<!-- migration: expand_video_agent_specs.py · va_id={va_id} · pack_id={pack_id} -->
"""


def default_related(pack_id: str, va_id: int) -> list[str]:
    base = [
        "business/video/corpus/study/agents.md",
        "business/video/corpus/study/SYSTEM_REFERENCE.md",
        "business/video/corpus/study/ai_agent_video_production_workflow.md",
        "business/video/corpus/study/human_video_production_workflow.md",
        "business/video/corpus/study/agent_loop_v3.md",
    ]
    extra: list[str] = []
    if pack_id in {"video.orchestrator", "video.planner", "video.router", "video.judge", "video.gatekeeper"}:
        extra += [
            "business/video/corpus/study/SYSTEM_REFERENCE.md",
            "business/video/corpus/plan/planner_agent_v2.1.md",
        ]
    if "research" in pack_id or pack_id in {"video.webresearch", "video.archiveresearch"}:
        extra += [
            "business/video/corpus/study/research_agent_functional_specification.md",
            "business/video/corpus/study/research_agent_technical_specification.md",
        ]
    if pack_id in {"video.screenwriter", "video.showrunner"}:
        extra.append(
            "business/video/corpus/study/screenwriter_strategic_goal_achievement_agent_functional_specification.md"
        )
    if "aiqa" in pack_id or "aesthetics" in pack_id or pack_id == "video.aiqaconsistency":
        extra.append("business/video/corpus/study/aesthetics_agent_functional_specification.md")
    if va_id >= 46:  # meta-ish often use loops
        extra.append("business/video/corpus/study/agent_loop_v3.md")
    # dedupe preserve order
    seen: set[str] = set()
    out: list[str] = []
    for p in base + extra:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="write SPEC.md files")
    ap.add_argument("--agents-md", type=Path, default=AGENTS_MD)
    ap.add_argument("--roster", type=Path, default=ROSTER)
    ap.add_argument("--agents-dir", type=Path, default=AGENTS_DIR)
    args = ap.parse_args()

    if not args.agents_md.is_file():
        print(f"Missing agents.md: {args.agents_md}", file=sys.stderr)
        return 1
    roster = json.loads(args.roster.read_text(encoding="utf-8"))
    if len(roster) != 114:
        print(f"ROSTER length {len(roster)} != 114", file=sys.stderr)
        return 1
    by_id = parse_agents_md(args.agents_md)
    missing = [i for i in range(1, 115) if i not in by_id]
    if missing:
        print(f"agents.md missing va_ids: {missing[:20]}... count={len(missing)}", file=sys.stderr)
        return 1

    written = 0
    for row in roster:
        va_id = int(row["id"])
        pack_id = row["pack_id"]
        table = by_id[va_id]
        related = default_related(pack_id, va_id)
        # only list related that exist
        related = [p for p in related if (ROOT / p).is_file() or p.endswith("agents.md")]
        body = render_spec(row, table, related)
        spec_path = args.agents_dir / pack_id / "SPEC.md"
        agent_json = args.agents_dir / pack_id / "agent_spec.json"
        if not args.write:
            if len(body) < 400:
                print(f"too short draft for {pack_id}", file=sys.stderr)
                return 1
            continue
        if agent_json.is_file():
            try:
                spec = json.loads(agent_json.read_text(encoding="utf-8"))
                if spec.get("spec_lock") is True:
                    print(f"skip locked {pack_id}")
                    continue
            except json.JSONDecodeError:
                pass
        spec_path.parent.mkdir(parents=True, exist_ok=True)
        spec_path.write_text(body, encoding="utf-8")
        if agent_json.is_file():
            try:
                spec = json.loads(agent_json.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                spec = {}
            prov = dict(spec.get("provenance") or {})
            prov["source_refs"] = [
                "business/video/corpus/study/agents.md",
                f"business/video/agents/{pack_id}/SPEC.md",
                "business/video/corpus/SOURCE_COMMIT.txt",
            ]
            prov["spec_depth"] = "agents_md_embedded"
            prov["upstream_name"] = "va-agent-swarm"
            spec["provenance"] = prov
            agent_json.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written += 1

    if not args.write:
        print(f"DRY_OK parsed_ids={len(by_id)} roster={len(roster)}")
        return 0
    print(f"EXPAND_OK written={written}")
    return 0 if written == 114 else 2


if __name__ == "__main__":
    raise SystemExit(main())
