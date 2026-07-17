"""Legacy linear DNA runner wrapper — LG-01."""

from __future__ import annotations

from typing import Any


class LegacyWorkflowEngine:
    name = "legacy"

    def execute(self, runtime: Any, run: dict[str, Any], actor_user_id: str) -> None:
        runtime._execute_run(run, actor_user_id)

    def resume_from_approval(
        self,
        runtime: Any,
        run: dict[str, Any],
        actor_user_id: str,
        *,
        decision: str,
        reason: str | None = None,
    ) -> None:
        if decision == "approved":
            runtime._execute_run(run, actor_user_id)
        # reject handled by caller before resume
