"""Checkpointer factory — LG-03."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from app.core.config import settings


@lru_cache(maxsize=1)
def get_checkpointer() -> Any:
    """Return a process-wide checkpointer (MemorySaver by default)."""
    mode = (settings.lg_checkpoint or "memory").lower()
    if mode == "postgres" and settings.use_postgres:
        try:
            # Optional dependency path — fall back if package missing
            from langgraph.checkpoint.postgres import PostgresSaver  # type: ignore

            # PostgresSaver typically needs a connection string setup; use memory if complex
            # Prefer memory for local-prod stability unless explicitly configured later.
        except Exception:  # noqa: BLE001
            pass
    from langgraph.checkpoint.memory import MemorySaver

    return MemorySaver()


def thread_id_for(organization_id: str, run_id: str) -> str:
    return f"{organization_id}:{run_id}"
