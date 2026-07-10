"""Loop DNA — the eight Loop Engineering components as structured config."""
from __future__ import annotations

from typing import Any

DEFAULT_LOOP_DNA: dict[str, Any] = {
    "id": "loop_workflow_improvement_default",
    "name": "Workflow improvement loop",
    "version": "1.0.0",
    # 1. Trigger
    "trigger": {"type": "api", "event": "loops.run"},
    # 2. Isolation
    "isolation": {"mode": "loop_run_id", "sandbox_variants_only": True},
    # 3. Generator
    "generator": {"kind": "workflow_runtime", "workflow_id_field": "workflow_id"},
    # 4. Evaluator
    "evaluator": {
        "kind": "composite",
        "checks": ["run_status", "failed_steps", "evaluation_result"],
    },
    # 5. State / memory
    "state": {"persist_lessons": True, "persist_loop_runs": True},
    # 6. Skills / knowledge
    "skills": {
        "source_refs": [
            "AGENTS.md",
            "business/materials/sops",
            "docs/self-improvement-and-orchestration.md",
        ]
    },
    # 7. Connectors
    "connectors": {"tools": "local_adapters", "knowledge": "tiered_retrieval"},
    # 8. Stopping condition
    "stopping": {
        "max_iterations": 3,
        "success_statuses": ["completed"],
        "fail_budget": 2,
        "escalate_on": ["waiting_for_approval", "max_iterations", "fail_budget"],
    },
    "governance": {
        "never_mutate_production_dna": True,
        "auto_promote": False,
        "require_sandbox_for_dna_changes": True,
    },
}


def validate_loop_dna(dna: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in (
        "trigger",
        "isolation",
        "generator",
        "evaluator",
        "state",
        "skills",
        "connectors",
        "stopping",
    ):
        if key not in dna:
            errors.append(f"missing_component:{key}")
    stopping = dna.get("stopping") or {}
    if int(stopping.get("max_iterations") or 0) < 1:
        errors.append("stopping.max_iterations must be >= 1")
    if (dna.get("governance") or {}).get("auto_promote") is True:
        errors.append("auto_promote_forbidden")
    return errors
