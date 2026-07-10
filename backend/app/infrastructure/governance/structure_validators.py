"""Production DNA / DRC validators for structure.md SDD tasks (STRUCT-07, STRUCT-10)."""

from __future__ import annotations

from typing import Any


def validate_production_workflow_dna(dna: dict[str, Any]) -> list[str]:
    """Return failure messages; empty list means production-safe under structure rules."""
    failures: list[str] = []
    steps = dna.get("steps") or []
    if not isinstance(steps, list) or not steps:
        failures.append("workflow DNA must declare steps")
        return failures

    irreversible_steps = [
        s for s in steps if isinstance(s, dict) and (s.get("irreversible") or s.get("action_type") == "irreversible_execution")
    ]
    for step in irreversible_steps:
        sid = step.get("id", "?")
        if not step.get("human_gate_required"):
            failures.append(f"step {sid}: irreversible action requires human_gate_required=true")
        rollback = dna.get("rollback") or {}
        rollback_steps = rollback.get("rollback_steps") if isinstance(rollback, dict) else None
        if not rollback_steps:
            failures.append(f"step {sid}: irreversible action requires rollback.rollback_steps")

    risk = str(dna.get("risk_tier") or "")
    high_risk = risk.startswith("tier_4") or risk.startswith("tier_5")
    if high_risk and not any(isinstance(s, dict) and s.get("human_gate_required") for s in steps):
        failures.append("high-risk DNA must include at least one human-gated step")

    if dna.get("production_ready") and not dna.get("audit_log_write_required", True):
        failures.append("production_ready DNA must require audit log writes")

    return failures


def validate_decision_requirement_card(drc: dict[str, Any], *, for_production: bool = True) -> list[str]:
    """Return failure messages for DRC publish rules."""
    failures: list[str] = []
    experts = drc.get("expert_sources")
    if not isinstance(experts, list) or len(experts) < 1:
        failures.append("DRC requires non-empty expert_sources for production")
    prov = drc.get("provenance") or {}
    refs = prov.get("source_refs") if isinstance(prov, dict) else None
    if for_production and (not isinstance(refs, list) or len(refs) < 1):
        failures.append("DRC requires provenance.source_refs for production")
    if for_production and not drc.get("last_reviewed"):
        failures.append("DRC requires last_reviewed for production")
    if for_production and not drc.get("validation_tests"):
        failures.append("DRC requires validation_tests for production")
    return failures


def is_production_dna_valid(dna: dict[str, Any]) -> bool:
    return not validate_production_workflow_dna(dna)


def is_production_drc_valid(drc: dict[str, Any]) -> bool:
    return not validate_decision_requirement_card(drc, for_production=True)
