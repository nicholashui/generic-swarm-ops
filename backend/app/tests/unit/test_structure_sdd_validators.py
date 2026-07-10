"""STRUCT-07 / STRUCT-10 negative fixtures and production validators."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from app.infrastructure.governance.structure_validators import (
    is_production_dna_valid,
    is_production_drc_valid,
    validate_decision_requirement_card,
    validate_production_workflow_dna,
)

ROOT = Path(__file__).resolve().parents[4]
FIXTURES = ROOT / "business" / "fixtures" / "negative"
EXAMPLES = ROOT / "business" / "examples"
PUBLISH_DRC = ROOT / "business" / "experts" / "decision-requirement-cards" / "drc_contract_exception_001.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class StructureSddValidatorsTest(unittest.TestCase):
    def test_good_flagship_dna_passes(self) -> None:
        dna = _load(EXAMPLES / "workflow-dna.example.json")
        self.assertEqual(validate_production_workflow_dna(dna), [])
        self.assertTrue(is_production_dna_valid(dna))

    def test_negative_dna_irreversible_without_gate_fails(self) -> None:
        dna = _load(FIXTURES / "dna-irreversible-without-gate.json")
        failures = validate_production_workflow_dna(dna)
        self.assertTrue(any("human_gate" in f for f in failures), failures)
        self.assertFalse(is_production_dna_valid(dna))

    def test_negative_dna_irreversible_without_rollback_fails(self) -> None:
        dna = _load(FIXTURES / "dna-irreversible-without-rollback.json")
        failures = validate_production_workflow_dna(dna)
        self.assertTrue(any("rollback" in f for f in failures), failures)
        self.assertFalse(is_production_dna_valid(dna))

    def test_publish_drc_passes(self) -> None:
        drc = _load(PUBLISH_DRC)
        self.assertEqual(validate_decision_requirement_card(drc), [])
        self.assertTrue(is_production_drc_valid(drc))

    def test_negative_drc_missing_experts_fails(self) -> None:
        drc = _load(FIXTURES / "drc-missing-expert-sources.json")
        failures = validate_decision_requirement_card(drc)
        self.assertTrue(any("expert_sources" in f for f in failures), failures)
        self.assertFalse(is_production_drc_valid(drc))

    def test_elicitation_templates_exist(self) -> None:
        base = ROOT / "business" / "experts" / "elicitation-methods"
        for name in (
            "01-shadow-mode.md",
            "02-critical-decision-interview.md",
            "03-think-aloud.md",
            "04-exception-interview.md",
            "05-retrospective-review.md",
            "06-apprentice-mode.md",
        ):
            self.assertTrue((base / name).is_file(), name)

    def test_role_realization_map_exists(self) -> None:
        path = ROOT / "business" / "governance" / "role-realization-map.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("Business Orchestrator", text)
        self.assertIn("Evolution Manager", text)

    def test_runtime_tier_policy_exists(self) -> None:
        path = ROOT / "business" / "governance" / "use-case-risk-tiering" / "runtime-tier-policy.json"
        data = _load(path)
        self.assertEqual(len(data.get("tiers") or []), 6)
        self.assertIn("drc_binding", data)

    def test_activate_rejects_unsafe_production_dna(self) -> None:
        import uuid

        from app.runtime import ValidationError, runtime

        token = runtime.issue_token("admin@example.com", "admin-password")
        user = runtime.authenticate(token["access_token"])
        wf_id = f"wf_unsafe_gate_{uuid.uuid4().hex[:8]}"
        unsafe = {
            "id": wf_id,
            "name": "Unsafe",
            "steps": [
                {
                    "id": "danger",
                    "state": "execution",
                    "next": ["complete"],
                    "agent": "business_orchestrator",
                    "tools": ["billing_system"],
                    "action_type": "irreversible_execution",
                    "human_gate_required": False,
                    "irreversible": True,
                }
            ],
            "risk_tier": "tier_4_execute_with_gate",
            "status": "draft",
            "rollback": {"reversible": False, "rollback_steps": []},
            "verification": {"required_checks": ["x"]},
            "guardrails": {"human_approval_required_if": ["never"], "forbidden_actions": ["x"]},
            "fitness_metrics": ["error_rate"],
            "audit_log_write_required": True,
            "production_ready": False,
            "input_schema": {"type": "object", "properties": {}, "required": []},
            "output_schema": {"type": "object", "properties": {}, "required": []},
        }
        created = runtime.create_workflow(user, unsafe)
        self.assertEqual(created["status"], "draft")
        with self.assertRaises(ValidationError):
            runtime.activate_workflow_version(user, wf_id, created["version"])

    def test_rejection_records_lesson(self) -> None:
        from app.runtime import runtime

        token = runtime.issue_token("admin@example.com", "admin-password")
        user = runtime.authenticate(token["access_token"])
        self.assertTrue(hasattr(runtime, "_record_rejection_lesson"))
        run = runtime.start_workflow_run(
            "wf_customer_onboarding_v12",
            user,
            {
                "case_id": "reject_lesson_case",
                "signed_contract": "c.pdf",
                "customer_profile": {"company": "Acme"},
                "billing_details": {"plan": "standard"},
            },
        )
        approval_id = run.get("approval_request_id")
        if run.get("status") == "awaiting_approval" and approval_id:
            rev = runtime.issue_token("reviewer@example.com", "reviewer-password")
            reviewer = runtime.authenticate(rev["access_token"])
            runtime.decide_approval(approval_id, "rejected", "test reject for lesson", reviewer)
            lessons = runtime.store.data.get("improvement_lessons") or []
            self.assertTrue(any(l.get("source") == "approval.rejected" for l in lessons), lessons)


if __name__ == "__main__":
    unittest.main()
