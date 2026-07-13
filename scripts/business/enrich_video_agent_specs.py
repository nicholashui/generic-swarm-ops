# -*- coding: utf-8 -*-
"""Build self-contained SPEC.md (+ local sources/) for every video agent.

Pulls related text from:
  1) business/video/corpus/**
  2) C:\\Project\\va-agent-swarm/** (if present; mirrored into agent folder)

No primary reliance on external refer links — bodies are embedded in SPEC.md and
related files are also copied under agents/<pack_id>/sources/.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "business" / "video"
CORPUS = VIDEO / "corpus"
STUDY = CORPUS / "study"
AGENTS_MD = STUDY / "agents.md"
ROSTER = VIDEO / "ROSTER.json"
AGENTS_DIR = VIDEO / "agents"
DEFAULT_VA = Path(r"C:\Project\va-agent-swarm")

ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$"
)

# corpus-relative EN deep docs → pack_ids that own them
DEEP_SPEC_MAP: dict[str, list[str]] = {
    "study/aesthetics_agent_functional_specification.md": [
        "video.aiqaconsistency",
        "video.judge",
        "video.critic",
    ],
    "study/research_agent_functional_specification.md": [
        "video.webresearch",
        "video.archiveresearch",
        "video.trendintelligence",
        "video.competitorintelligence",
        "video.citation",
        "video.interviewsynthesis",
        "video.benchmarkresearch",
        "video.analyst",
    ],
    "study/research_agent_technical_specification.md": [
        "video.webresearch",
        "video.archiveresearch",
        "video.benchmarkresearch",
        "video.citation",
    ],
    "study/optimization_agent_functional_specification.md": [
        "video.promptoptimizer",
        "video.costoptimizer",
        "video.latencyoptimizer",
        "video.retentionoptimizer",
        "video.roasoptimizer",
        "video.accessibilityoptimizer",
        "video.evaluationharness",
        "video.safetyredteam",
    ],
    "study/optimization_agent_technical_specification.md": [
        "video.promptoptimizer",
        "video.costoptimizer",
        "video.latencyoptimizer",
        "video.evaluationharness",
        "video.roasoptimizer",
        "video.retentionoptimizer",
    ],
    "study/general_creative_agent_functional_specification.md": [
        "video.ideation",
        "video.narrativearc",
        "video.styletransfer",
        "video.worldbuilding",
        "video.moodboard",
        "video.novelty",
        "video.emotionalarc",
        "video.director",
        "video.conceptartist",
        "video.creativedirector",
    ],
    "study/general_creative_agent_technical_specification.md": [
        "video.ideation",
        "video.narrativearc",
        "video.styletransfer",
        "video.moodboard",
        "video.novelty",
        "video.worldbuilding",
    ],
    "study/intent_analysis_agent_functional_specification.md": [
        "video.planner",
        "video.orchestrator",
        "video.producer",
        "video.gatekeeper",
    ],
    "study/agentic_rag_functional_specification.md": [
        "video.memory",
        "video.webresearch",
        "video.citation",
        "video.archiveresearch",
        "video.interviewsynthesis",
    ],
    "study/coding_agent_functional_specification.md": [
        "video.promptengineer",
        "video.evaluationharness",
        "video.templatedesign",
    ],
    "study/llm_usage_functional_specification.md": [
        "video.promptengineer",
        "video.promptoptimizer",
        "video.router",
        "video.costoptimizer",
        "video.latencyoptimizer",
    ],
    "study/screenwriter_strategic_goal_achievement_agent_functional_specification.md": [
        "video.screenwriter",
        "video.showrunner",
        "video.comedywriter",
        "video.childrensauthor",
        "video.journalist",
    ],
    "study/strategic_goal_achievement_agent_functional_specification.md": [
        "video.planner",
        "video.producer",
        "video.showrunner",
        "video.brandstrategist",
        "video.marketing",
    ],
    "study/psychological_profile_agent_functional_specifications.md": [
        "video.audiencesim",
        "video.personalizationengineer",
        "video.emotionalarc",
        "video.learnersim",
    ],
    "study/psychological_recommendation_agent_functional_specification.md": [
        "video.personalizationengineer",
        "video.audiencesim",
        "video.performancemarketer",
        "video.retentionoptimizer",
        "video.marketing",
        "video.seo",
    ],
    "study/podcast_agent_functional_specifcation.md": [
        "video.voiceover",
        "video.audiobooknarrator",
        "video.sounddesign",
        "video.composer",
        "video.soundmixer",
        "video.musicsupervisor",
    ],
    "plan/planner_agent_v2.1.md": [
        "video.planner",
        "video.orchestrator",
        "video.router",
        "video.gatekeeper",
    ],
    "plan/planner_agent_v2.0.md": [
        "video.planner",
        "video.orchestrator",
    ],
    "study/agent_loop_v3.md": [
        "video.orchestrator",
        "video.planner",
        "video.router",
        "video.judge",
        "video.memory",
        "video.gatekeeper",
    ],
    "study/SYSTEM_REFERENCE.md": [
        "video.orchestrator",
        "video.planner",
        "video.router",
        "video.judge",
        "video.producer",
        "video.gatekeeper",
    ],
    "study/ai_agent_video_production_workflow.md": [
        "video.orchestrator",
        "video.planner",
        "video.director",
        "video.producer",
        "video.screenwriter",
    ],
    "study/human_video_production_workflow.md": [
        "video.director",
        "video.producer",
        "video.editor",
        "video.cinematographer",
    ],
    "study/lifes_quiet_redemption_agent_workflow.md": [
        "video.aiqaconsistency",
        "video.continuity",
        "video.editor",
        "video.director",
        "video.lipsync",
        "video.avatardesign",
    ],
    "study/system_build_plan.md": [
        "video.orchestrator",
        "video.planner",
        "video.evaluationharness",
    ],
    "study/knowledge_router_agent.md": [
        "video.memory",
        "video.router",
        "video.citation",
    ],
    "study/thinking_model.md": [
        "video.planner",
        "video.ideation",
        "video.judge",
    ],
}

# Always scan these for name-based paragraph excerpts
SCAN_DOCS = [
    "study/SYSTEM_REFERENCE.md",
    "study/ai_agent_video_production_workflow.md",
    "study/human_video_production_workflow.md",
    "study/agent_loop_v3.md",
    "study/agent_loop_v2.md",
    "study/agent_loop.md",
    "study/lifes_quiet_redemption_agent_workflow.md",
    "study/system_build_plan.md",
    "study/thinking_model.md",
    "study/complex_problem_solution_process_model.md",
    "study/video_generation_techology_should_learn_now.md",
    "study/knowledge_router_agent.md",
]

MAX_FILE_EMBED = 250_000
MAX_EXCERPT = 12_000
MAX_SPEC = 800_000  # allow large self-contained SPECs


def strip_md(s: str) -> str:
    s = s.strip()
    return re.sub(r"\*\*(.+?)\*\*", r"\1", s).strip()


def parse_agent_rows(path: Path) -> dict[int, dict[str, str]]:
    by_id: dict[int, dict[str, str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        va_id = int(m.group(1))
        if not (1 <= va_id <= 114) or va_id in by_id:
            continue
        by_id[va_id] = {
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


def extract_section(text: str, start: str, end: str | None) -> str:
    i = text.find(start)
    if i < 0:
        return ""
    rest = text[i:]
    if end:
        j = rest.find(end, len(start))
        if j > 0:
            return rest[:j].strip()
    return rest.strip()


def load_common(agents_md: str) -> str:
    return extract_section(
        agents_md, "## 11. Common Structure of an AI Agent", "## 12. References"
    )


def load_category_section(agents_md: str, category: str) -> str:
    cat_map = {
        "1-ATL": ("## 1. Above-the-Line Agents", "## 2. Camera & Lighting Agents"),
        "2-Cam": ("## 2. Camera & Lighting Agents", "## 3. Editorial & Color Agents"),
        "3-Edit": ("## 3. Editorial & Color Agents", "## 4. Sound & Music Agents"),
        "4-Snd": ("## 4. Sound & Music Agents", "## 5. Performance & Choreography Agents"),
        "5-Perf": ("## 5. Performance & Choreography Agents", "## 6. Distribution & Marketing Agents"),
        "6-Dist": ("## 6. Distribution & Marketing Agents", "## 7. Education & Domain-Expert Agents"),
        "7-Edu": ("## 7. Education & Domain-Expert Agents", "## 8. AI-Era Specialist Agents"),
        "8-AI": ("## 8. AI-Era Specialist Agents", "## 9. Specialist Meta-Agents"),
        "9-Meta": ("## 9. Specialist Meta-Agents", "## 10. Workflow Support Agents"),
        "10-Sup": ("## 10. Workflow Support Agents", "## 11. Common Structure of an AI Agent"),
    }
    pair = cat_map.get(category)
    if not pair:
        return ""
    return extract_section(agents_md, pair[0], pair[1])


def load_references(agents_md: str) -> str:
    return extract_section(agents_md, "## 12. References", None)


def invert_deep() -> dict[str, list[str]]:
    inv: dict[str, list[str]] = {}
    for rel, packs in DEEP_SPEC_MAP.items():
        for p in packs:
            inv.setdefault(p, []).append(rel)
    return inv


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def truncate(s: str, n: int) -> str:
    if len(s) <= n:
        return s
    return s[: n - 80] + "\n\n…\n\n_(remainder truncated for single-file size; full original also under sources/)_\n"


def agent_name_variants(row: dict, table: dict[str, str]) -> list[str]:
    name = row.get("name") or table.get("agent_name") or ""
    variants = {
        name,
        table.get("agent_name") or "",
        name.split("/")[0].strip(),
        re.sub(r"\s*\([^)]*\)", "", name).strip(),
        row["pack_id"].replace("video.", ""),
        row["pack_id"].replace("video.", "").replace("_", " "),
    }
    for n in list(variants):
        if n.endswith("Agent"):
            variants.add(n[: -len("Agent")])
        if " " in n:
            variants.add(n.replace(" ", ""))
    return [v for v in variants if v and len(v) > 2]


def excerpt_mentions(doc: str, names: list[str], max_chars: int = MAX_EXCERPT) -> str:
    paras = re.split(r"\n\s*\n", doc)
    hits: list[str] = []
    total = 0
    for p in paras:
        if not any(n in p for n in names):
            continue
        chunk = p.strip()
        if len(chunk) < 50:
            continue
        if total + len(chunk) > max_chars:
            if max_chars - total > 200:
                hits.append(chunk[: max_chars - total] + "\n…")
            break
        hits.append(chunk)
        total += len(chunk) + 2
    return "\n\n".join(hits)


def resolve_sources(rel: str, va_root: Path | None) -> list[tuple[str, Path]]:
    """Return list of (label, path) to read: corpus first, then va mirror."""
    out: list[tuple[str, Path]] = []
    cpath = CORPUS / rel
    if cpath.is_file():
        out.append((f"corpus/{rel}", cpath))
    if va_root:
        # rel is study/... or plan/...
        vpath = va_root / rel
        if vpath.is_file() and (not cpath.is_file() or vpath.stat().st_size != cpath.stat().st_size):
            out.append((f"va/{rel}", vpath))
        elif vpath.is_file() and not cpath.is_file():
            out.append((f"va/{rel}", vpath))
    return out


def copy_into_sources(agent_dir: Path, rel: str, src: Path) -> str:
    """Copy file into agents/<pack>/sources/<rel> ; return relative path from agent dir."""
    dest = agent_dir / "sources" / rel.replace("/", "\\") if False else agent_dir / "sources" / Path(rel)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists() or dest.stat().st_size != src.stat().st_size:
        shutil.copy2(src, dest)
    return f"sources/{Path(rel).as_posix()}"


def collect_scan_hits(
    names: list[str], va_root: Path | None
) -> list[tuple[str, str, Path]]:
    """Return (label, excerpt, path) for SCAN_DOCS + opportunistic va scan of EN md."""
    results: list[tuple[str, str, Path]] = []
    seen_paths: set[Path] = set()

    def consider(label: str, path: Path) -> None:
        if path in seen_paths or not path.is_file():
            return
        text = read_text(path)
        if not text:
            return
        ex = excerpt_mentions(text, names)
        if not ex:
            return
        seen_paths.add(path)
        results.append((label, ex, path))

    for rel in SCAN_DOCS:
        for label, path in resolve_sources(rel, va_root):
            consider(label, path)

    # broader corpus EN md scan (skip huge already-embedded deep dumps later)
    if CORPUS.is_dir():
        for path in CORPUS.rglob("*.md"):
            if path.name.endswith("_hk.md"):
                continue
            if ".script" in path.name:
                continue
            rel = path.relative_to(CORPUS).as_posix()
            if rel in SCAN_DOCS or rel in DEEP_SPEC_MAP:
                continue
            if path.stat().st_size > 200_000:
                continue
            consider(f"corpus/{rel}", path)

    if va_root and va_root.is_dir():
        for sub in ("study", "plan"):
            d = va_root / sub
            if not d.is_dir():
                continue
            for path in d.rglob("*.md"):
                if path.name.endswith("_hk.md") or ".script" in path.name:
                    continue
                if path.stat().st_size > 200_000:
                    continue
                # skip if same relative already used from corpus
                try:
                    rel = path.relative_to(va_root).as_posix()
                except ValueError:
                    continue
                if (CORPUS / rel).is_file():
                    continue
                consider(f"va/{rel}", path)

    return results


def render(
    row: dict,
    table: dict[str, str],
    agents_md: str,
    common: str,
    references: str,
    deep_inv: dict[str, list[str]],
    va_root: Path | None,
    copy_sources: bool,
) -> str:
    pack_id = row["pack_id"]
    va_id = int(row["id"])
    name = row.get("name") or table.get("agent_name") or pack_id
    cat = row.get("category") or ""
    agent_dir = AGENTS_DIR / pack_id
    names = agent_name_variants(row, table)
    parts: list[str] = []

    parts.append(f"# {name}\n")
    parts.append(
        "> **Self-contained agent definition** for host `generic-swarm-ops`. "
        "Body text is embedded from in-pack corpus"
        + (" and va-agent-swarm when available" if va_root else "")
        + ". Do not require external repos to understand this agent.\n"
    )

    parts.append("## Identity\n")
    parts.append(
        f"| Field | Value |\n|-------|-------|\n"
        f"| **va_id** | {va_id} |\n"
        f"| **pack_id** | `{pack_id}` |\n"
        f"| **category** | `{cat}` |\n"
        f"| **domain_id** | `video` |\n"
        f"| **folder** | `business/video/agents/{pack_id}/` |\n"
    )

    cat_sec = load_category_section(agents_md, cat)
    if cat_sec:
        parts.append("## Category roster section (full, from agents.md)\n")
        parts.append(
            "_The following is the complete category section from the master roster "
            "(includes peers in the same craft category)._\n\n"
        )
        parts.append(truncate(cat_sec, 80_000))
        parts.append("\n")

    parts.append("## Responsibility\n")
    parts.append((table.get("responsibility") or "—") + "\n")
    parts.append("## Knowledge distillation sources\n")
    parts.append((table.get("knowledge_sources") or "—") + "\n")
    parts.append("## Self-quality criteria\n")
    parts.append((table.get("self_quality") or "—") + "\n")
    parts.append("## Surpass-human signal\n")
    parts.append((table.get("surpass_human") or "—") + "\n")
    parts.append("## Critique bus\n")
    parts.append(f"- **Accepts critique from:** {table.get('accepts_critique_from') or '—'}\n")
    parts.append(f"- **Comments on:** {table.get('comments_on') or '—'}\n")
    parts.append("## Tools (design-time documentation)\n")
    parts.append((table.get("tool_access_design") or "—") + "\n")
    parts.append(
        "**Runtime safety:** Host allow-lists are only `agent_spec.json` + "
        "`tool-permission-register.json`. CI uses video_* stubs. "
        "Do not treat design-time vendor names as enabled APIs.\n"
    )
    parts.append("## Architecture pattern\n")
    parts.append((table.get("architecture_pattern") or "—") + "\n")

    parts.append("## Common structure of an AI agent (full §11 from agents.md)\n")
    parts.append(common + "\n")

    if references:
        parts.append("## Shared references (from agents.md §12)\n")
        parts.append(truncate(references, 40_000) + "\n")

    # Deep specs — full body embed + copy to sources/
    deep_rels = deep_inv.get(pack_id, [])
    if deep_rels:
        parts.append("## Deep specifications (full embedded content)\n")
        for rel in deep_rels:
            sources = resolve_sources(rel, va_root)
            if not sources:
                parts.append(f"\n### Missing: `{rel}`\n")
                continue
            label, path = sources[0]
            body = read_text(path) or ""
            local_note = ""
            if copy_sources and body:
                local = copy_into_sources(agent_dir, rel, path)
                local_note = f" Also stored at `{local}` under this agent folder."
            # prefer corpus/va second if larger
            for lab, pth in sources[1:]:
                alt = read_text(pth)
                if alt and len(alt) > len(body):
                    body = alt
                    label = lab
                    if copy_sources:
                        copy_into_sources(agent_dir, rel, pth)
            parts.append(f"\n### Document: `{rel}`\n")
            parts.append(f"_Embedded from `{label}`.{local_note}_\n\n")
            parts.append(truncate(body, MAX_FILE_EMBED))
            parts.append("\n")

    # Name-based hits across corpus/va
    hits = collect_scan_hits(names, va_root)
    parts.append("## Additional corpus / va passages naming this agent\n")
    if not hits:
        parts.append("_No extra name-based passages found beyond deep specs and roster._\n")
    else:
        for label, ex, path in hits:
            # skip if this file already fully embedded as deep spec
            try:
                rel = path.relative_to(CORPUS).as_posix() if CORPUS in path.parents or path.is_relative_to(CORPUS) else ""
            except (ValueError, AttributeError):
                rel = ""
            if not rel and va_root:
                try:
                    rel = path.relative_to(va_root).as_posix()
                except ValueError:
                    rel = path.name
            if rel in deep_rels:
                continue
            local_note = ""
            if copy_sources and path.is_file() and rel:
                try:
                    local = copy_into_sources(agent_dir, f"excerpts/{Path(rel).name}", path)
                    local_note = f" Copy: `{local}`."
                except OSError:
                    pass
            parts.append(f"\n### From `{label}`{local_note}\n\n")
            parts.append(ex)
            parts.append("\n")

    # Always embed SVG common structure path as note + copy svg
    svg = STUDY / "common-agent-structure.svg"
    if svg.is_file() and copy_sources:
        copy_into_sources(agent_dir, "study/common-agent-structure.svg", svg)
        parts.append(
            "\n## Local binary assets in this agent folder\n\n"
            "- `sources/study/common-agent-structure.svg` — common architecture diagram\n"
        )

    parts.append("\n## Host runtime binding\n")
    parts.append(
        f"- **agent_spec.json** in this folder (ALC, tools, status)\n"
        f"- **standby_pool.json** — orchestrator-reachable\n"
        f"- **workflows/** — DNA JSON under `business/video/workflows/`\n"
        f"- **sources/** — copied related documents for offline use in this folder\n"
    )

    parts.append("\n## Provenance\n")
    parts.append(
        f"- Master roster row va_id={va_id} from embedded agents.md content above.\n"
        f"- Deep/extra text from `business/video/corpus/`"
        + (f" and `{va_root}`" if va_root else "")
        + ".\n"
        f"- Generator: `scripts/business/enrich_video_agent_specs.py`.\n"
        f"- Upstream project name (historical only): va-agent-swarm.\n"
    )
    parts.append(f"\n<!-- self_contained_spec · {pack_id} · va_id={va_id} -->\n")

    return truncate("\n".join(parts), MAX_SPEC)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--va-root", type=Path, default=DEFAULT_VA)
    ap.add_argument("--no-copy-sources", action="store_true")
    ap.add_argument("--no-va", action="store_true", help="do not read va-agent-swarm")
    args = ap.parse_args()

    if not AGENTS_MD.is_file():
        print(f"Missing {AGENTS_MD}", file=sys.stderr)
        return 1

    va_root = None if args.no_va else (args.va_root if args.va_root.is_dir() else None)
    agents_md = AGENTS_MD.read_text(encoding="utf-8")
    by_id = parse_agent_rows(AGENTS_MD)
    if len(by_id) != 114:
        print(f"agents.md rows={len(by_id)} expected 114", file=sys.stderr)
        return 1
    common = load_common(agents_md)
    refs = load_references(agents_md)
    deep_inv = invert_deep()
    roster = json.loads(ROSTER.read_text(encoding="utf-8"))
    copy_sources = not args.no_copy_sources

    sizes: list[int] = []
    written = 0
    for row in roster:
        pack_id = row["pack_id"]
        if args.only and pack_id != args.only:
            continue
        table = by_id[int(row["id"])]
        body = render(
            row,
            table,
            agents_md,
            common,
            refs,
            deep_inv,
            va_root,
            copy_sources and args.write,
        )
        sizes.append(len(body))
        if not args.write:
            continue
        (AGENTS_DIR / pack_id / "SPEC.md").write_text(body, encoding="utf-8")
        aj = AGENTS_DIR / pack_id / "agent_spec.json"
        if aj.is_file():
            try:
                spec = json.loads(aj.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                spec = {}
            if not spec.get("spec_lock"):
                prov = dict(spec.get("provenance") or {})
                prov["source_refs"] = [
                    f"business/video/agents/{pack_id}/SPEC.md",
                    f"business/video/agents/{pack_id}/sources/",
                    "business/video/corpus/study/agents.md",
                ]
                prov["spec_depth"] = "self_contained_folder_v3"
                spec["provenance"] = prov
                aj.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        # folder README
        (AGENTS_DIR / pack_id / "README.md").write_text(
            f"# `{pack_id}`\n\n"
            f"- **SPEC.md** — full self-contained definition (embedded corpus/va content)\n"
            f"- **agent_spec.json** — host runtime ALC/tools\n"
            f"- **sources/** — copied related documents for offline use\n",
            encoding="utf-8",
        )
        written += 1

    sizes.sort()
    print(
        f"{'WRITE' if args.write else 'DRY'} n={written or len(sizes)} "
        f"min={sizes[0]} med={sizes[len(sizes)//2]} max={sizes[-1]} "
        f"va={'yes' if va_root else 'no'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
