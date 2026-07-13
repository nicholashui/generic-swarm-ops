"""Cross-pack isolation helpers (Wave 4 / N2).

Pure functions for domain prefixing, tool namespace checks, and allow-list
immutability assertions used by multipack load/security tests.
"""
from __future__ import annotations

from typing import Iterable


# Ops / platform tools that must not be granted to foreign domain packs via injection.
OPS_SENSITIVE_TOOLS = frozenset(
    {
        "billing_system",
        "crm",
        "email",
    }
)

# Known domain pack prefixes (agent_id first segment or domain_id).
KNOWN_PACK_DOMAINS = frozenset(
    {
        "video",
        "example_research",
        "example_education",
        "example",  # example.* agents
    }
)


def domain_prefix(agent_id: str | None, domain_id: str | None = None) -> str | None:
    """Return pack domain for an agent (explicit domain_id wins, else id prefix)."""
    if domain_id and str(domain_id).strip():
        return str(domain_id).strip().lower()
    if not agent_id:
        return None
    aid = str(agent_id).strip()
    if "." in aid:
        return aid.split(".", 1)[0].lower()
    return None


def is_cross_namespace_tool(
    agent_domain: str | None,
    tool_id: str,
    *,
    agent_allowed: Iterable[str] | None = None,
) -> bool:
    """True if tool looks like a cross-pack / ops escape for the agent domain.

    Video/example packs using ops sensitive tools without prior allow-list
    membership are treated as cross-namespace for red-team classification.
    """
    tool = str(tool_id or "").strip()
    if not tool:
        return False
    allowed = set(agent_allowed or [])
    if tool in allowed:
        return False
    domain = (agent_domain or "").lower() or None
    if tool in OPS_SENSITIVE_TOOLS and domain in {"video", "example_research", "example_education", "example"}:
        return True
    if domain == "video" and tool.startswith("example"):
        return True
    if domain in {"example_research", "example_education", "example"} and tool.startswith("video_"):
        return True
    return False


def allowlists_equal(before: Iterable[str] | None, after: Iterable[str] | None) -> bool:
    """Order-insensitive allow-list equality (injection must not expand tools)."""
    return set(before or []) == set(after or [])


def snapshot_allowlist(tools: Iterable[str] | None) -> list[str]:
    return sorted({str(t) for t in (tools or []) if t})
