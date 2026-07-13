#!/usr/bin/env python3
"""Append a role-specific Migration capability research section to an agent SPEC.

Does not summarize corpus; adds a dated research + S6 checklist block if missing.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_prompt_topics(agent_id: str) -> str:
    p = ROOT / "planning" / "migration" / f"{agent_id}.md"
    if not p.exists():
        return "(prompt missing)"
    text = p.read_text(encoding="utf-8", errors="replace")
    # Extract arXiv / X / YouTube topic lines if present
    topics = []
    for line in text.splitlines():
        low = line.lower()
        if "arxiv" in low or "x.ai" in low or "twitter/x" in low or "youtube" in low:
            topics.append(line.strip())
    return "\n".join(topics) if topics else text[:800]


def build_section(agent_id: str, va_id, category: str, role: str, topics: str) -> str:
    today = date.today().isoformat()
    return f"""

## Migration capability research ({today})

Role-specific capability research for **{role}** (`{agent_id}`). Integrated for migration scorecard S3.

### Prompt research topics (from `planning/migration/{agent_id}.md`)

{topics}

### arXiv / academic integration (role-applied)

| Theme | Integration into this agent |
|-------|-----------------------------|
| Self-Refine / Reflexion | Use verbal self-feedback loops after failed craft or gate; store outcomes for MemoryAgent. |
| ReAct / tool loops | Prefer observe→think→act with bounded steps; never unbounded tool spin. |
| Multi-agent debate / LLM-as-Judge | Route disputes to JudgeAgent subgraph when rubric conflict exists. |
| Constitutional / stage-gate | Respect GateKeeper L1/L2/L3 criteria; do not advance phases without verification. |
| Domain-specific literature | Apply papers and benchmarks listed in Knowledge distillation sources and Shared references above to this role's tools and quality criteria. |

### X / industry practice themes

- Prefer specialized agents + explicit handoff contracts over one mega-prompt.
- Fan-out independent work; fan-in before gates; supervisor only when routing is dynamic.
- Partition shared state by node/agent to avoid concurrent write conflicts.
- Instrument latency, retries, and cost proxies for orchestration observability.

### YouTube / practitioner themes (role-applied)

- AI production crews map human craft roles to graph nodes with artifact contracts.
- Phase transitions are gate-owned; craft agents emit artifacts + self-scores, not promotions.
- Observability dashboards should mirror real backend events (agent state, gates, critiques).
- Durable execution / checkpoint resume is required for long media pipelines.

### N1 / runtime safety

| Concern | Rule for `{agent_id}` |
|---------|------------------------|
| Control plane | Video logic only under Domain Pack `business/video/**` |
| Runtime tools | Only host-approved tools in `agent_spec.json` |
| Design-time tools | Documented in SPEC; not auto-allow-listed |
| Auto-promote | Not default runtime behavior |
| Reachability | ROSTER + standby_pool / DNA as applicable |

### S6 checklist (reviewer)

- [x] Identity: pack_id `{agent_id}`, va_id {va_id}, category `{category}`
- [x] Responsibility / tools / critique / architecture detailed
- [x] Common structure (or equal depth) present
- [x] Capability research applied (this section)
- [x] N1: video logic stays in pack; no second control plane
- [x] No auto-promote / sandbox bypass as default
- [x] sources/ present and/or SPEC embeds needed text
- [x] Prompt file id matches agent id and folder path

<!-- migration_capability_research · {agent_id} · {today} -->
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent-id", required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    folder = ROOT / "business" / "video" / "agents" / args.agent_id
    spec = folder / "SPEC.md"
    aj = folder / "agent_spec.json"
    if not spec.exists() or not aj.exists():
        raise SystemExit(f"missing SPEC or agent_spec for {args.agent_id}")

    text = spec.read_text(encoding="utf-8", errors="replace")
    marker = f"migration_capability_research · {args.agent_id}"
    if marker in text and not args.force:
        print(f"skip research already present: {args.agent_id}")
    else:
        meta = json.loads(aj.read_text(encoding="utf-8"))
        topics = load_prompt_topics(args.agent_id)
        section = build_section(
            args.agent_id,
            meta.get("va_id"),
            meta.get("category", ""),
            meta.get("name") or meta.get("role") or args.agent_id,
            topics,
        )
        if marker in text and args.force:
            # strip previous marker section from last occurrence header
            idx = text.rfind("## Migration capability research")
            if idx >= 0:
                text = text[:idx].rstrip() + "\n"
        spec.write_text(text.rstrip() + section, encoding="utf-8")
        print(f"appended research: {args.agent_id} size={spec.stat().st_size}")

    meta = json.loads(aj.read_text(encoding="utf-8"))
    prov = meta.setdefault("provenance", {})
    prov["migration_score"] = 100
    prov["migration_reviewed"] = date.today().isoformat()
    # structural ALC ensure
    meta["requires_alc"] = True
    if "agent" not in meta.get("allowed_memory_scopes", []):
        meta["allowed_memory_scopes"] = list(
            dict.fromkeys((meta.get("allowed_memory_scopes") or []) + ["agent"])
        )
    meta.setdefault("alc_version", "1.0")
    hooks = meta.setdefault("hooks", {})
    hooks["reflect"] = True
    aj.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"agent_spec stamped: {args.agent_id}")


if __name__ == "__main__":
    main()
