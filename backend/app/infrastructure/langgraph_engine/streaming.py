"""Event normalization for graph streams — LG-09."""

from __future__ import annotations

from typing import Any


GRAPH_EVENT_TYPES = {
    "node.started",
    "node.completed",
    "handoff",
    "interrupt",
    "approval.requested",
    "approval.approved",
    "approval.rejected",
    "step.started",
    "step.completed",
    "step.failed",
    "run.completed",
    "run.started",
    "run.status_changed",
    "tool_call.started",
    "tool_call.completed",
}


def normalize_event(raw: dict[str, Any]) -> dict[str, Any]:
    event = raw.get("event") or raw.get("type") or "log"
    return {
        "id": raw.get("id"),
        "type": event if event in GRAPH_EVENT_TYPES else event,
        "runId": raw.get("workflow_run_id") or raw.get("run_id"),
        "nodeId": raw.get("step_id") or raw.get("node_id"),
        "message": raw.get("message") or "",
        "timestamp": raw.get("timestamp") or raw.get("created_at"),
        "payload": {
            k: v
            for k, v in raw.items()
            if k
            not in {
                "id",
                "event",
                "type",
                "workflow_run_id",
                "run_id",
                "step_id",
                "node_id",
                "message",
                "timestamp",
                "created_at",
            }
        },
    }


def filter_run_events(events: list[dict[str, Any]], run_id: str) -> list[dict[str, Any]]:
    return [normalize_event(e) for e in events if e.get("workflow_run_id") == run_id]
