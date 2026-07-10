"""Reflexion-style post-run reflection (self-evolving agents §7.2 spirit).

Produces structured lessons without calling an external LLM — rule-based so
offline/tests stay deterministic. LLM critique can replace extractors later.
"""
from __future__ import annotations

from typing import Any


def reflect_on_run(
    run: dict[str, Any],
    workflow: dict[str, Any] | None = None,
    *,
    llm_overlay: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Analyze a completed/failed/waiting run and emit lessons + suggested DNA tweaks."""
    lessons: list[str] = []
    suggested_changes: list[dict[str, Any]] = []
    issues: list[str] = []

    status = run.get("status") or "unknown"
    error = run.get("error") or ""
    steps = run.get("steps") or []
    failed_steps = [s for s in steps if s.get("status") == "failed"]
    waiting_steps = [s for s in steps if s.get("status") == "waiting_for_approval"]

    if status == "failed" or failed_steps:
        issues.append(f"run_status:{status}")
        for step in failed_steps:
            sid = step.get("id") or step.get("step_id") or "unknown"
            err = step.get("error") or error or "step_failed"
            lessons.append(f"Step '{sid}' failed: {err}. Fail closed and audit before retry.")
            if "not allowed" in str(err).lower():
                lessons.append(
                    f"Tool allow-list violation on step '{sid}'. Align workflow tools with agent allowed_tools."
                )
                suggested_changes.append(
                    {
                        "type": "align_tool_allowlist",
                        "step_id": sid,
                        "description": "Ensure step tools ⊆ agent.allowed_tools",
                    }
                )
            if "unavailable" in str(err).lower():
                lessons.append(f"Missing agent/tool for step '{sid}'. Seed or enable dependency before re-run.")

    if status == "waiting_for_approval" or waiting_steps:
        for step in waiting_steps:
            sid = step.get("id") or "gated"
            lessons.append(
                f"Human gate pending on '{sid}'. Ensure reviewer SLA and rollback plan are documented."
            )
            suggested_changes.append(
                {
                    "type": "human_gate_ops",
                    "step_id": sid,
                    "description": "Keep human_gate_required; improve approval routing metadata",
                }
            )

    if status == "completed":
        lessons.append("Run completed. Capture successful path as procedural memory if novel.")
        # Soft suggestion: ensure evaluation_policy.block_on_fail remains
        if workflow and not (workflow.get("evaluation_policy") or {}).get("block_on_fail"):
            suggested_changes.append(
                {
                    "type": "evaluation_policy",
                    "description": "Enable evaluation_policy.block_on_fail for promotion safety",
                }
            )

    if error and "Evaluation failed" in error:
        lessons.append("Evaluation block_on_fail stopped promotion path. Fix eval failures before canary.")
        suggested_changes.append(
            {
                "type": "eval_hardening",
                "description": "Review golden/regression failures for this workflow",
            }
        )

    if not lessons:
        lessons.append(f"Run status '{status}' produced no critical lessons; continue monitoring.")

    how = "textual_reflection_rule_based"
    if llm_overlay:
        # Merge optional LLM critic lessons (never drop rule-based safety lessons)
        for lesson in llm_overlay.get("lessons") or []:
            if lesson and lesson not in lessons:
                lessons.append(str(lesson))
        for issue in llm_overlay.get("issues") or []:
            if issue and issue not in issues:
                issues.append(str(issue))
        for change in llm_overlay.get("suggested_changes") or []:
            if change and change not in suggested_changes:
                suggested_changes.append(change)
        how = "rule_based+llm_critic"

    satisfactory = status == "completed" and not failed_steps
    if llm_overlay and "is_satisfactory" in llm_overlay and status != "completed":
        satisfactory = bool(llm_overlay.get("is_satisfactory")) and satisfactory

    return {
        "is_satisfactory": satisfactory,
        "run_id": run.get("id"),
        "workflow_id": run.get("workflow_id"),
        "status": status,
        "issues": issues,
        "lessons": lessons,
        "suggested_changes": suggested_changes,
        "what_evolves": ["memory", "workflow_dna_proposal"] if suggested_changes else ["memory"],
        "when": "inter_episode",
        "how": how,
        "llm_critic_used": bool(llm_overlay),
    }
