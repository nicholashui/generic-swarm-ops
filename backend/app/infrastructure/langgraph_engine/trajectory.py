"""Trajectory scoring for graph runs — LG-15."""

from __future__ import annotations

from typing import Any


def score_trajectory(run: dict[str, Any], events: list[dict[str, Any]], state: dict[str, Any]) -> dict[str, Any]:
    """Deterministic trajectory metrics (no LLM)."""
    handoffs = sum(1 for e in events if e.get("event") == "handoff")
    interrupts = sum(1 for e in events if e.get("event") in {"interrupt", "approval.requested"})
    node_starts = sum(1 for e in events if e.get("event") == "node.started")
    node_done = sum(1 for e in events if e.get("event") == "node.completed")
    failures = sum(1 for e in events if e.get("event") in {"step.failed", "error"})
    tool_denials = sum(1 for e in events if "not allowed" in str(e.get("message") or "").lower())

    completed = run.get("status") == "completed"
    efficiency = 1.0
    if node_starts > 0:
        efficiency = min(1.0, node_done / max(node_starts, 1))
    safety = 1.0 if tool_denials == 0 and failures == 0 else max(0.0, 1.0 - 0.2 * (tool_denials + failures))
    completion = 1.0 if completed else 0.0
    # Prefer fewer interrupts for efficiency but not zero if tier-4
    hitl_penalty = min(0.3, 0.05 * max(0, interrupts - 2))
    score = round(0.45 * completion + 0.25 * safety + 0.20 * efficiency + 0.10 * (1.0 - hitl_penalty), 4)

    return {
        "score": score,
        "completion": completion,
        "safety": round(safety, 4),
        "efficiency": round(efficiency, 4),
        "handoffs": handoffs,
        "interrupts": interrupts,
        "node_starts": node_starts,
        "node_completed": node_done,
        "failures": failures,
        "tool_denials": tool_denials,
        "pattern": state.get("pattern") or run.get("orchestration_pattern"),
        "engine": run.get("engine") or "langgraph",
    }
