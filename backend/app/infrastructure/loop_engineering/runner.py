"""Loop stop/continue decisions (prompt → observe → verify → iterate)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class LoopDecision:
    action: str  # continue | stop_success | stop_escalate | stop_fail
    reason: str
    iteration: int


def evaluate_stop(
    *,
    iteration: int,
    max_iterations: int,
    fail_count: int,
    fail_budget: int,
    last_run_status: str | None,
    success_statuses: list[str] | None = None,
) -> LoopDecision:
    success = set(success_statuses or ["completed"])
    if last_run_status in success:
        return LoopDecision("stop_success", f"goal_met:{last_run_status}", iteration)
    if last_run_status == "waiting_for_approval":
        return LoopDecision("stop_escalate", "human_gate_required", iteration)
    if fail_count >= fail_budget:
        return LoopDecision("stop_fail", "fail_budget_exhausted", iteration)
    if iteration >= max_iterations:
        return LoopDecision("stop_escalate", "max_iterations", iteration)
    return LoopDecision("continue", "iterate", iteration)
