"""Security helpers for LangGraph engine — LG-16."""

from __future__ import annotations

from typing import Any

from app.core.config import settings
from app.core.errors import PermissionDeniedError, ValidationError


def assert_thread_tenant(thread_id: str, organization_id: str) -> None:
    if not thread_id.startswith(f"{organization_id}:"):
        raise PermissionDeniedError("Cross-organization graph thread access denied")


def enforce_budgets(state: dict[str, Any]) -> str | None:
    """Return error message if budgets exceeded, else None."""
    visits = int(state.get("node_visits") or 0)
    handoffs = int(state.get("handoffs") or 0)
    if visits > settings.lg_max_nodes:
        return f"Budget exceeded: node_visits={visits} > {settings.lg_max_nodes}"
    if handoffs > settings.lg_max_handoffs:
        return f"Budget exceeded: handoffs={handoffs} > {settings.lg_max_handoffs}"
    effects = state.get("tool_effects") or []
    if len(effects) > settings.lg_max_nodes * 3:
        return f"Budget exceeded: tool_effects={len(effects)}"
    return None


def redact_state(state: dict[str, Any]) -> dict[str, Any]:
    banned = ("password", "token", "api_key", "secret", "authorization", "cookie")
    out: dict[str, Any] = {}
    for k, v in state.items():
        lk = str(k).lower()
        if any(b in lk for b in banned):
            continue
        if isinstance(v, dict):
            out[k] = redact_state(v)
        else:
            out[k] = v
    return out


def validate_engine_name(name: str) -> str:
    n = (name or "legacy").strip().lower()
    if n not in {"legacy", "langgraph"}:
        raise ValidationError(f"Unknown engine: {name}")
    return n
