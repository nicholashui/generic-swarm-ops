"""Sandboxed skill/prompt evolution — never writes production skills without approval.

Proposals live in runtime store + business/evolution/successful-variants or
business/distilled/skills/_sandbox/ only.
"""
from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _safe_name(name: str) -> str:
    return re.sub(r"[^a-z0-9_-]+", "-", name.lower()).strip("-")[:48] or "skill"


def propose_skill_patch(
    *,
    skill_name: str,
    content: str,
    rationale: str,
    source_run_id: str | None,
    organization_id: str,
    actor_id: str,
) -> dict[str, Any]:
    proposal = {
        "id": f"skillprop_{_safe_name(skill_name)}_{int(datetime.now(UTC).timestamp())}",
        "kind": "skill_prompt_patch",
        "skill_name": skill_name,
        "content": content,
        "rationale": rationale,
        "source_run_id": source_run_id,
        "organization_id": organization_id,
        "created_by": actor_id,
        "created_at": _now(),
        "status": "sandbox_proposed",
        "sandbox_only": True,
        "production_path": f"business/distilled/skills/{_safe_name(skill_name)}.md",
        "sandbox_path": f"business/distilled/skills/_sandbox/{_safe_name(skill_name)}.md",
        "provenance": {
            "source_refs": [source_run_id or "manual", "docs/self-improvement-and-orchestration.md"],
            "captured_by": actor_id,
            "recorded_at": _now(),
            "framework": "dgm_lite_skill_only",
        },
    }
    return proposal


def _repo_relative(repo_root: Path, path: Path) -> str:
    """Return POSIX path relative to repo_root when possible (portable product paths)."""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix().replace("genetic-swarm-ops", "generic-swarm-ops")


def write_skill_sandbox(repo_root: Path, proposal: dict[str, Any]) -> str:
    sandbox_rel = proposal.get("sandbox_path") or "business/distilled/skills/_sandbox/skill.md"
    path = repo_root / sandbox_rel
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"<!-- SANDBOX ONLY — not production. proposal_id={proposal.get('id')} -->\n"
        f"<!-- rationale: {proposal.get('rationale')} -->\n\n"
    )
    path.write_text(header + str(proposal.get("content") or ""), encoding="utf-8")
    return _repo_relative(repo_root, path)


def promote_skill_to_production(repo_root: Path, proposal: dict[str, Any]) -> str:
    """Copy sandbox skill to production path (explicit promote only)."""
    sandbox = repo_root / (proposal.get("sandbox_path") or "")
    prod = repo_root / (proposal.get("production_path") or "")
    if not sandbox.is_file():
        raise FileNotFoundError(f"Sandbox skill missing: {sandbox}")
    prod.parent.mkdir(parents=True, exist_ok=True)
    body = sandbox.read_text(encoding="utf-8")
    # Strip sandbox banner lines
    lines = [ln for ln in body.splitlines() if not ln.startswith("<!-- SANDBOX")]
    prod.write_text("\n".join(lines).lstrip() + "\n", encoding="utf-8")
    return _repo_relative(repo_root, prod)
