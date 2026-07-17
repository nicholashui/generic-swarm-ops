"""HostGraphState — LG-02."""

from __future__ import annotations

from typing import Annotated, Any, TypedDict


def _append_list(left: list | None, right: list | None) -> list:
    return list(left or []) + list(right or [])


class HostGraphState(TypedDict, total=False):
    state_schema_version: str
    organization_id: str
    run_id: str
    workflow_id: str
    domain_id: str | None
    case: dict[str, Any]
    risk: dict[str, Any]
    messages: Annotated[list[dict[str, Any]], _append_list]
    route: dict[str, Any]
    active_agent_id: str | None
    artifacts: dict[str, Any]
    tool_effects: Annotated[list[dict[str, Any]], _append_list]
    memory_hits: list[dict[str, Any]]
    interrupt: dict[str, Any] | None
    metrics: dict[str, Any]
    error: dict[str, Any] | None
    status: str
    completed_step_ids: list[str]
    current_step_id: str | None
    node_visits: int
    handoffs: int
    pattern: str


STATE_SCHEMA_VERSION = "1.0"


def seed_state_from_run(
    run: dict[str, Any],
    workflow: dict[str, Any],
    *,
    pattern: str = "pipeline",
) -> dict[str, Any]:
    return {
        "state_schema_version": STATE_SCHEMA_VERSION,
        "organization_id": run["organization_id"],
        "run_id": run["id"],
        "workflow_id": run["workflow_id"],
        "domain_id": workflow.get("domain_id") or workflow.get("domain"),
        "case": dict(run.get("input_payload") or {}),
        "risk": {"risk_tier": run.get("risk_tier") or workflow.get("risk_tier")},
        "messages": [],
        "route": {},
        "active_agent_id": None,
        "artifacts": dict(run.get("output") or {}) if isinstance(run.get("output"), dict) else {},
        "tool_effects": [],
        "memory_hits": [],
        "interrupt": None,
        "metrics": {"token_usage": run.get("token_usage") or 0, "cost_usage": run.get("cost_usage") or 0},
        "error": None,
        "status": "running",
        "completed_step_ids": [
            s["id"] for s in (run.get("steps") or []) if s.get("status") == "completed"
        ],
        "current_step_id": run.get("current_step"),
        "node_visits": int((run.get("graph_metrics") or {}).get("node_visits") or 0),
        "handoffs": int((run.get("graph_metrics") or {}).get("handoffs") or 0),
        "pattern": pattern,
    }


def project_state_to_run(run: dict[str, Any], state: dict[str, Any]) -> None:
    """Mutate run record from graph state (in-place)."""
    run["current_step"] = state.get("current_step_id")
    run["output"] = state.get("artifacts") or run.get("output")
    if state.get("error"):
        run["error"] = state["error"].get("message") if isinstance(state["error"], dict) else str(state["error"])
    status = state.get("status")
    if status:
        run["status"] = status
    interrupt = state.get("interrupt")
    if interrupt and isinstance(interrupt, dict):
        run["approval_request_id"] = interrupt.get("approval_id") or run.get("approval_request_id")
        run["approval_state"] = interrupt.get("approval_state") or run.get("approval_state")
    run["graph_metrics"] = {
        "node_visits": state.get("node_visits") or 0,
        "handoffs": state.get("handoffs") or 0,
        "pattern": state.get("pattern"),
    }
    metrics = state.get("metrics") or {}
    if "token_usage" in metrics:
        run["token_usage"] = metrics["token_usage"]
    if "cost_usage" in metrics:
        run["cost_usage"] = metrics["cost_usage"]
    # sync step statuses
    completed = set(state.get("completed_step_ids") or [])
    current = state.get("current_step_id")
    for step in run.get("steps") or []:
        sid = step.get("id")
        if sid in completed:
            step["status"] = "completed"
        elif status == "waiting_for_approval" and sid == current:
            step["status"] = "waiting_for_approval"
        elif status == "failed" and sid == current:
            step["status"] = "failed"
        elif step.get("status") not in {"completed", "waiting_for_approval"}:
            if status == "completed":
                pass
            elif sid == current and status == "running":
                step["status"] = "running"
