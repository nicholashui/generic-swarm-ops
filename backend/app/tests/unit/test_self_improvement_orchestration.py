"""Self-improvement, loop engineering, and knowledge orchestration (K1-lite)."""
from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.infrastructure.loop_engineering.loop_dna import DEFAULT_LOOP_DNA, validate_loop_dna
from app.infrastructure.loop_engineering.runner import evaluate_stop
from app.infrastructure.knowledge_orchestration.extract import extract_document_graph
from app.infrastructure.knowledge_orchestration.operators import detect_gaps, resolve_seed
from app.runtime import runtime


class SelfImprovementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])

    def test_reflect_stores_lessons(self):
        # Force a failed tool-allow path
        wf_id = f"wf_si_{uuid.uuid4().hex[:8]}"
        runtime.create_workflow(
            self.admin,
            {
                "id": wf_id,
                "name": "SI fail",
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
                "output_schema": {"type": "object", "properties": {}, "required": []},
            },
        )
        run = runtime.start_workflow_run(wf_id, self.admin, {})
        runtime.dispatch_queued_runs(self.admin)
        run = runtime.get_run(self.admin, run["id"])
        self.assertEqual(run["status"], "failed")
        reflection = runtime.reflect_on_workflow_run(self.admin, run["id"])
        self.assertFalse(reflection["is_satisfactory"])
        self.assertTrue(reflection["lessons"])
        lessons = runtime.list_improvement_lessons(self.admin, workflow_id=wf_id)
        self.assertTrue(any(wf_id == (l.get("workflow_id")) for l in lessons) or lessons)
        # Auto-propose stays sandbox-only
        variant = runtime.auto_propose_from_failures(self.admin, workflow_id=wf_id, run_id=run["id"])
        self.assertTrue(variant.get("sandbox_only"))
        self.assertNotEqual(variant.get("status"), "active")
        base = runtime.get_workflow(self.admin, wf_id)
        self.assertEqual(base["id"], wf_id)


class LoopEngineeringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])

    def test_loop_dna_valid_and_stop_rules(self):
        self.assertEqual(validate_loop_dna(DEFAULT_LOOP_DNA), [])
        bad = {**DEFAULT_LOOP_DNA, "governance": {"auto_promote": True}}
        self.assertIn("auto_promote_forbidden", validate_loop_dna(bad))
        d = evaluate_stop(
            iteration=1,
            max_iterations=3,
            fail_count=0,
            fail_budget=2,
            last_run_status="completed",
        )
        self.assertEqual(d.action, "stop_success")
        d2 = evaluate_stop(
            iteration=2,
            max_iterations=3,
            fail_count=2,
            fail_budget=2,
            last_run_status="failed",
        )
        self.assertEqual(d2.action, "stop_fail")

    def test_start_improvement_loop_runs_iterations(self):
        # Use a simple analysis workflow that can complete without external deps
        wf_id = f"wf_loop_{uuid.uuid4().hex[:8]}"
        runtime.create_workflow(
            self.admin,
            {
                "id": wf_id,
                "name": "Loopable",
                "risk_tier": "tier_2_draft",
                "status": "active",
                "steps": [
                    {
                        "id": "audit",
                        "agent": "business_orchestrator",
                        "tools": ["audit_log_writer"],
                        "action_type": "audit",
                        "human_gate_required": False,
                        "irreversible": False,
                    }
                ],
                "input_schema": {"type": "object", "properties": {"case_id": {"type": "string"}}, "required": []},
                "output_schema": {"type": "object", "properties": {"outcome": {"type": "string"}}, "required": []},
                "evaluation_policy": {"block_on_fail": False, "auto_promote": False},
            },
        )
        loop = runtime.start_improvement_loop(
            self.admin,
            {
                "workflow_id": wf_id,
                "input_payload": {"case_id": f"c_{uuid.uuid4().hex[:6]}", "triggered_from": "test_loop"},
                "auto_approve_gates": False,
                "auto_propose_on_fail": False,
            },
        )
        self.assertTrue(loop["id"].startswith("loop_"))
        self.assertTrue(loop.get("iterations"))
        self.assertIn(loop["status"], {"stop_success", "stop_escalate", "stop_fail", "running"})
        fetched = runtime.get_loop_run(self.admin, loop["id"])
        self.assertEqual(fetched["id"], loop["id"])


class KnowledgeOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])

    def test_extract_graph_and_operators(self):
        doc_id = f"doc_k1_{uuid.uuid4().hex[:8]}"
        runtime.upload_knowledge_document(
            self.admin,
            {
                "id": doc_id,
                "title": "Onboarding policy and workflow",
                "content": (
                    "Workflow wf_customer_onboarding_v12 requires human gate. "
                    "Billing is governed by policy pol_onboarding_default. "
                    "The process builds on pol_onboarding_default for tier_4_execute_with_gate controls."
                ),
                "source": "business/materials/sops/customer-onboarding.md",
                "allowed_roles": ["owner", "admin", "manager", "operator", "viewer"],
            },
        )
        indexed = runtime.index_knowledge_document(self.admin, doc_id)
        self.assertGreaterEqual(indexed.get("graph_node_count") or 0, 1)
        graph = runtime.extract_knowledge_graph(self.admin, doc_id)
        self.assertTrue(graph.get("nodes"))
        self.assertIn("B", graph.get("modules_present") or [])
        q = runtime.query_knowledge_graph(self.admin, seed="pol_onboarding_default", max_hops=2)
        self.assertTrue(q.get("matches") or q.get("lineage") is not None)
        gaps = runtime.knowledge_graph_gaps(self.admin)
        self.assertIn("gap_count", gaps)
        # Unit extract + resolve
        g2 = extract_document_graph(
            {
                "id": "x",
                "title": "t",
                "content": "wf_customer_onboarding_v12 requires pol_onboarding_default.",
                "source": "s.md",
            }
        )
        seeds = resolve_seed(g2["nodes"], "wf_customer")
        self.assertTrue(seeds)
        self.assertIsInstance(detect_gaps(g2["nodes"], g2["edges"]), list)


if __name__ == "__main__":
    unittest.main()
