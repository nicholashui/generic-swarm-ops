"""WorkflowEngine protocol — LG-01."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class WorkflowEngine(Protocol):
    name: str

    def execute(self, runtime: Any, run: dict[str, Any], actor_user_id: str) -> None:
        """Drive a run until terminal, waiting_for_approval, or failure."""
        ...

    def resume_from_approval(
        self,
        runtime: Any,
        run: dict[str, Any],
        actor_user_id: str,
        *,
        decision: str,
        reason: str | None = None,
    ) -> None:
        """Continue after a human gate decision."""
        ...
