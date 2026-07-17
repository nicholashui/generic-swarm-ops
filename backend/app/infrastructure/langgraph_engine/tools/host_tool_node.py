"""Host tool execution for graph nodes — LG-07."""

from __future__ import annotations

from typing import Any

from app.infrastructure.tools.adapters import ToolAdapterError, execute_tool


def run_host_tools(
    *,
    runtime: Any,
    run: dict[str, Any],
    step_definition: dict[str, Any],
    agent: dict[str, Any],
    actor_user_id: str,
    case: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str | None]:
    """Execute step tools via host adapters. Returns (effects, tool_results, error)."""
    tool_lookup = runtime._tool_lookup(run["organization_id"])
    tool_results: list[dict[str, Any]] = []
    effects: list[dict[str, Any]] = []
    agent.setdefault("allowed_tools", list(step_definition.get("tools") or []))

    for tool_id in step_definition.get("tools") or []:
        tool = tool_lookup.get(tool_id)
        if not tool or tool.get("enabled", True) is False:
            return effects, tool_results, f"Tool unavailable: {tool_id}"
        if tool_id not in (agent.get("allowed_tools") or []):
            return effects, tool_results, f"Agent {agent.get('id')} is not allowed to use tool {tool_id}"
        payload = {
            **(case or {}),
            "run_id": run["id"],
            "step_id": step_definition.get("id"),
            "workflow_id": run.get("workflow_id"),
            "organization_id": run.get("organization_id"),
        }
        try:
            effect = execute_tool(tool_id, payload)
        except ToolAdapterError as exc:
            return effects, tool_results, str(exc)
        except Exception as exc:  # noqa: BLE001
            return effects, tool_results, f"Tool {tool_id} failed: {exc}"
        # Match legacy runtime fields so tool_effects are queryable by run_id
        effect["organization_id"] = run["organization_id"]
        effect["run_id"] = run["id"]
        effect["step_id"] = step_definition.get("id")
        tool_results.append(effect)
        effects.append(effect)
        runtime.store.collection("tool_effects").append(effect)
        runtime._append_audit(
            run["organization_id"],
            actor_user_id,
            "tool",
            "tool.executed",
            "tool_effect",
            effect.get("id") or tool_id,
            {"tool_id": tool_id, "run_id": run["id"], "step_id": step_definition.get("id")},
            "success",
        )
    return effects, tool_results, None
