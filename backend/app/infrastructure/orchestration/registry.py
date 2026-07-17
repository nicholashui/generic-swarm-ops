"""Engine selection and registry — LG-01."""

from __future__ import annotations

from typing import Any

from app.core.config import settings
from app.infrastructure.orchestration.legacy_engine import LegacyWorkflowEngine

_ENGINES: dict[str, Any] | None = None


def _build_engines() -> dict[str, Any]:
    engines: dict[str, Any] = {"legacy": LegacyWorkflowEngine()}
    if settings.langgraph_enabled:
        try:
            from app.infrastructure.langgraph_engine.engine import LangGraphWorkflowEngine

            engines["langgraph"] = LangGraphWorkflowEngine()
        except Exception:  # noqa: BLE001 — optional until deps present
            pass
    return engines


def list_engines() -> list[dict[str, Any]]:
    engines = _ensure()
    return [
        {
            "name": name,
            "available": True,
            "default": name == settings.engine_default,
        }
        for name in engines
    ]


def _ensure() -> dict[str, Any]:
    global _ENGINES
    if _ENGINES is None:
        _ENGINES = _build_engines()
    return _ENGINES


def get_engine(name: str | None = None) -> Any:
    engines = _ensure()
    key = (name or settings.engine_default or "legacy").strip().lower()
    if key not in engines:
        if key == "langgraph" and "langgraph" not in engines:
            from app.core.errors import ValidationError

            raise ValidationError(
                "LangGraph engine is not available (install langgraph or set GENERIC_SWARM_LANGGRAPH_ENABLED=true)"
            )
        key = "legacy"
    return engines[key]


def resolve_engine_name(
    *,
    workflow: dict[str, Any] | None = None,
    explicit: str | None = None,
    run: dict[str, Any] | None = None,
) -> str:
    """Pick engine name: run sticky → explicit request → workflow meta → default."""
    if run and run.get("engine"):
        return str(run["engine"]).strip().lower()
    if explicit:
        return str(explicit).strip().lower()
    if workflow:
        meta = workflow.get("execution_engine") or workflow.get("engine")
        if meta:
            return str(meta).strip().lower()
        orch = workflow.get("orchestration") or {}
        if isinstance(orch, dict) and orch.get("pattern") and orch.get("pattern") != "pipeline":
            # multi-pattern workflows prefer langgraph when enabled
            if settings.langgraph_enabled and "langgraph" in _ensure():
                return "langgraph"
        dna_engine = (workflow.get("metadata") or {}).get("engine") if isinstance(workflow.get("metadata"), dict) else None
        if dna_engine:
            return str(dna_engine).strip().lower()
    return (settings.engine_default or "legacy").strip().lower()
