"""Scorecard control-plane tests — drive shipped runtime entry points only."""
from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.runtime import PermissionDeniedError, ValidationError, runtime, verify_password, hash_password


class ScorecardControlsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token_bundle = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token_bundle["access_token"])

    def test_password_hash_is_pbkdf2_and_verifies(self):
        hashed = hash_password("secret-password-xyz")
        self.assertTrue(hashed.startswith("pbkdf2$"))
        self.assertTrue(verify_password("secret-password-xyz", hashed))
        self.assertFalse(verify_password("wrong", hashed))

    def test_tier_5_start_denied(self):
        wf_id = f"wf_tier5_{uuid.uuid4().hex[:8]}"
        runtime.create_workflow(
            self.admin,
            {
                "id": wf_id,
                "name": "Restricted",
                "risk_tier": "tier_5_restricted",
                "status": "active",
                "steps": [
                    {
                        "id": "noop",
                        "agent": "business_orchestrator",
                        "tools": ["audit_log_writer"],
                        "action_type": "analysis",
                        "human_gate_required": False,
                        "irreversible": False,
                    }
                ],
                "input_schema": {"type": "object", "properties": {}, "required": []},
                "output_schema": {"type": "object", "properties": {}, "required": []},
            },
        )
        with self.assertRaises(PermissionDeniedError):
            runtime.start_workflow_run(wf_id, self.admin, {})

    def test_tool_not_on_allow_list_denied(self):
        # Agent quality_compliance_agent cannot use billing_system
        wf_id = f"wf_tool_{uuid.uuid4().hex[:8]}"
        runtime.create_workflow(
            self.admin,
            {
                "id": wf_id,
                "name": "Bad tool",
                "risk_tier": "tier_3_execute_reversible",
                "status": "active",
                "steps": [
                    {
                        "id": "bad",
                        "agent": "quality_compliance_agent",
                        "tools": ["billing_system"],
                        "action_type": "analysis",
                        "human_gate_required": False,
                        "irreversible": False,
                    }
                ],
                "input_schema": {"type": "object", "properties": {}, "required": []},
                "output_schema": {"type": "object", "properties": {"outcome": {"type": "string"}}, "required": []},
            },
        )
        run = runtime.start_workflow_run(wf_id, self.admin, {})
        runtime.dispatch_queued_runs(self.admin)
        run = runtime.get_run(self.admin, run["id"])
        self.assertEqual(run["status"], "failed")
        self.assertIn("not allowed", run.get("error") or "")

    def test_human_gate_on_irreversible_step(self):
        wf_id = f"wf_gate_{uuid.uuid4().hex[:8]}"
        runtime.create_workflow(
            self.admin,
            {
                "id": wf_id,
                "name": "Gated",
                "risk_tier": "tier_4_execute_with_gate",
                "status": "active",
                "steps": [
                    {
                        "id": "critical",
                        "agent": "finance_ops_agent",
                        "tools": ["billing_system"],
                        "action_type": "irreversible_execution",
                        "human_gate_required": True,
                        "irreversible": True,
                    }
                ],
                "input_schema": {"type": "object", "properties": {}, "required": []},
                "output_schema": {"type": "object", "properties": {}, "required": []},
            },
        )
        run = runtime.start_workflow_run(wf_id, self.admin, {})
        runtime.dispatch_queued_runs(self.admin)
        run = runtime.get_run(self.admin, run["id"])
        self.assertEqual(run["status"], "waiting_for_approval")
        self.assertTrue(run.get("approval_request_id"))

    def test_memory_write_outside_allowed_scope_denied(self):
        with self.assertRaises(PermissionDeniedError):
            runtime.create_memory_item(
                self.admin,
                {
                    "scope": "secret_restricted_scope",
                    "title": "Should fail",
                    "content": "nope",
                },
                acting_agent_id="quality_compliance_agent",
            )

    def test_memory_read_outside_allowed_scope_denied(self):
        # quality_compliance_agent only has organization_memory (or defaults without secret scopes)
        with self.assertRaises(PermissionDeniedError):
            runtime.search_memory(
                self.admin,
                scope="secret_restricted_scope",
                acting_agent_id="quality_compliance_agent",
            )

    def test_memory_write_allowed_scope_ok(self):
        item = runtime.create_memory_item(
            self.admin,
            {
                "scope": "organization_memory",
                "title": "Allowed mem",
                "content": "ok",
                "provenance": {"source_refs": ["test"], "captured_by": "unit", "recorded_at": "2026-07-09"},
            },
            acting_agent_id="quality_compliance_agent",
        )
        self.assertEqual(item["scope"], "organization_memory")
        self.assertIn("source_refs", item["provenance"])

    def test_eval_block_on_fail(self):
        wf_id = f"wf_eval_{uuid.uuid4().hex[:8]}"
        runtime.create_workflow(
            self.admin,
            {
                "id": wf_id,
                "name": "Eval block",
                "risk_tier": "tier_3_execute_reversible",
                "status": "active",
                "evaluation_policy": {"required": True, "block_on_fail": True},
                "steps": [
                    {
                        "id": "only",
                        "agent": "business_orchestrator",
                        "tools": ["audit_log_writer"],
                        "action_type": "analysis",
                        "human_gate_required": False,
                        "irreversible": False,
                    }
                ],
                "input_schema": {"type": "object", "properties": {}, "required": []},
                "output_schema": {"type": "object", "properties": {}, "required": []},
            },
        )
        # Force evaluation failure by monkey-patching _create_evaluation for this run path
        original = runtime._create_evaluation

        def failing_eval(run):
            evaluation = original(run)
            evaluation["status"] = "failed"
            evaluation["result"] = "failed"
            evaluation["promotion_decision"] = "blocked"
            return evaluation

        runtime._create_evaluation = failing_eval  # type: ignore[method-assign]
        try:
            run = runtime.start_workflow_run(wf_id, self.admin, {})
            runtime.dispatch_queued_runs(self.admin)
            run = runtime.get_run(self.admin, run["id"])
            self.assertEqual(run["status"], "failed")
            self.assertIn("block_on_fail", run.get("error") or "")
        finally:
            runtime._create_evaluation = original  # type: ignore[method-assign]

    def test_archive_and_reset_authz(self):
        with self.assertRaises(PermissionDeniedError):
            runtime.reset_password("admin@example.com", "another-password")
        # archive requires permission — admin has it
        tools = runtime.list_collection("tools")
        self.assertTrue(tools)

    def test_evolution_propose_blocks_direct_mutation(self):
        with self.assertRaises(PermissionDeniedError):
            runtime.propose_evolution_variant(
                self.admin,
                {
                    "base_workflow_id": "wf_customer_onboarding_v12",
                    "direct_production_mutation": True,
                    "name": "evil",
                },
            )

    def test_evolution_propose_evaluate_canary_no_prod_mutation(self):
        workflows_before = {w["id"]: w.get("version") for w in runtime.list_workflows(self.admin)}
        base_id = next(iter(workflows_before.keys()))
        base_before = runtime.get_workflow(self.admin, base_id)
        variant = runtime.propose_evolution_variant(
            self.admin,
            {
                "base_workflow_id": base_id,
                "name": "safe sandbox variant",
                "changes": ["prompt tweak"],
                "dna": {
                    **{k: base_before[k] for k in ("name", "steps", "risk_tier") if k in base_before},
                    "risk_tier": base_before.get("risk_tier", "tier_4_execute_with_gate"),
                    "steps": base_before.get("steps", []),
                    "production_ready": False,
                },
            },
        )
        self.assertTrue(variant["sandbox_only"])
        self.assertFalse(variant["direct_production_mutation"])
        evaluated = runtime.sandbox_evaluate_variant(self.admin, variant["id"])
        self.assertIn(evaluated["evaluation"]["result"], {"passed", "failed"})
        if evaluated["evaluation"]["result"] == "passed":
            canary = runtime.promote_evolution_variant(self.admin, variant["id"], mode="canary")
            self.assertEqual(canary["status"], "approved_for_canary")
        # Production workflow id still present; propose/eval alone must not drop it
        base_after = runtime.get_workflow(self.admin, base_id)
        self.assertEqual(base_after["id"], base_before["id"])

    def test_event_log_ingest_drives_analytics(self):
        marker = f"activity_{uuid.uuid4().hex[:8]}"
        event = runtime.ingest_event_log(
            self.admin,
            {
                "process_id": "customer_onboarding",
                "case_id": f"case_{uuid.uuid4().hex[:6]}",
                "activity": marker,
                "outcome": {"status": "completed", "latency_minutes": 55},
                "risk_tier": "tier_3_execute_reversible",
            },
        )
        self.assertEqual(event["activity"], marker)
        listed = runtime.list_event_logs(self.admin, process_id="customer_onboarding")
        self.assertTrue(any(e["activity"] == marker for e in listed))
        summary = runtime.process_summary(self.admin)
        self.assertGreaterEqual(summary["event_log_count"], 1)
        self.assertIn(marker, summary["activity_counts"])
        bottlenecks = runtime.process_bottlenecks(self.admin)
        self.assertTrue(any(b.get("activity") == marker for b in bottlenecks if b.get("type") == "activity_latency"))
        discovered = runtime.discovered_processes(self.admin)
        self.assertTrue(any(d["process_id"] == "customer_onboarding" for d in discovered))
        conf = runtime.conformance_report(self.admin, process_id="customer_onboarding")
        self.assertIn("conformance_score", conf)
        self.assertGreaterEqual(conf["event_count"], 1)

    def test_knowledge_search_returns_provenance(self):
        doc_id = f"doc_{uuid.uuid4().hex[:8]}"
        runtime.upload_knowledge_document(
            self.admin,
            {
                "id": doc_id,
                "title": "Onboarding SOP snippet",
                "content": "Customer onboarding requires human gate for billing activation.",
                "source": "business/materials/sops/customer-onboarding.md",
                "allowed_roles": ["owner", "admin", "manager", "operator", "viewer"],
            },
        )
        runtime.index_knowledge_document(self.admin, doc_id)
        hits = runtime.search_knowledge(self.admin, query="onboarding")
        self.assertTrue(hits)
        hit = next(h for h in hits if h["id"] == doc_id)
        self.assertTrue(hit.get("source_refs") or hit.get("provenance", {}).get("source_refs"))


if __name__ == "__main__":
    unittest.main()
