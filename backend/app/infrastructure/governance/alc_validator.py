"""Agent Learning Contract (ALC) readiness checks — Wave 1."""
from __future__ import annotations

from typing import Any


class AlcRequiredError(Exception):
    """Raised when agent activation is blocked for missing ALC bindings."""

    code = "alc_required"

    def __init__(self, message: str = "ALC bindings required before activation"):
        super().__init__(message)
        self.message = message


def is_alc_ready(agent: dict[str, Any] | None) -> bool:
    """Return True if agent may be activated under ALC rules."""
    if not agent:
        return False
    # Explicit opt-out for platform seed agents that predate packs
    if agent.get("requires_alc") is False:
        return True
    if agent.get("requires_alc") is not True:
        # Default: require ALC only when flag present true; legacy seed without flag OK
        return True
    scopes = agent.get("allowed_memory_scopes") or []
    # Normalize aliases
    scope_set = {str(s) for s in scopes}
    if "agent" not in scope_set and "agent_memory" not in scope_set:
        return False
    if not agent.get("alc_version"):
        return False
    hooks = agent.get("hooks") or {}
    if hooks.get("reflect") is False:
        return False
    # Missing hooks.reflect defaults to True when requires_alc (Wave 0 specs set true)
    if "reflect" in hooks and hooks.get("reflect") is not True:
        return False
    return True


def assert_alc_ready(agent: dict[str, Any] | None) -> None:
    if is_alc_ready(agent):
        return
    raise AlcRequiredError(
        "ALC bindings required before activation: requires_alc, alc_version, "
        "allowed_memory_scopes includes 'agent', hooks.reflect=true"
    )
