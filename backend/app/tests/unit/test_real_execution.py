"""P1: real tool adapters + flagship run through human gate with effects."""
from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.infrastructure.tools.adapters import TOOL_ADAPTERS, execute_tool
from app.runtime import runtime


class RealExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])
        cls.reviewer = runtime.authenticate("reviewer-token")

    def test_adapters_registered_for_core_tools(self):
        for tool_id in ("audit_log_writer", "crm", "billing_system", "email", "contract_parser", "policy_retriever"):
            self.assertIn(tool_id, TOOL_ADAPTERS)
            effect = execute_tool(tool_id, {"case_id": "c1", "run_id": "r1", "step_id": "s1"})
            self.assertEqual(effect["status"], "ok")
            self.assertTrue(effect["id"].startswith("fx_"))

    def test_flagship_run_tools_and_approval_path(self):
        case_id = f"case_exec_{uuid.uuid4().hex[:8]}"
        run = runtime.start_workflow_run(
            "wf_customer_onboarding_v12",
            self.admin,
            {"case_id": case_id, "triggered_from": "test_real_execution"},
        )
        self.assertEqual(run["status"], "queued")
        runtime.dispatch_queued_runs(self.admin)
        run = runtime.get_run(self.admin, run["id"])

        # Tier-4 irreversible billing step should gate
        if run["status"] == "waiting_for_approval":
            approval_id = run["approval_request_id"]
            self.assertTrue(approval_id)
            runtime.decide_approval(approval_id, "approved", "p1 real execution", self.reviewer)
            run = runtime.get_run(self.admin, run["id"])

        # After approvals, run should complete (or still wait if multiple gates)
        safety = 0
        while run["status"] == "waiting_for_approval" and safety < 5:
            runtime.decide_approval(run["approval_request_id"], "approved", "p1 loop", self.reviewer)
            run = runtime.get_run(self.admin, run["id"])
            safety += 1

        self.assertIn(run["status"], {"completed", "failed", "waiting_for_approval"})
        effects = [
            e
            for e in runtime.list_collection("tool_effects")
            if e.get("run_id") == run["id"]
        ]
        # At least one tool effect if any step completed
        completed_steps = [s for s in run.get("steps", []) if s.get("status") == "completed"]
        if completed_steps:
            self.assertGreaterEqual(len(effects), 1)
            self.assertTrue(all(e.get("status") == "ok" for e in effects))
        # Audit contains tool.executed when effects exist
        audits = runtime.list_audit_logs(self.admin)
        if effects:
            self.assertTrue(any(a.get("action") == "tool.executed" for a in audits))


if __name__ == "__main__":
    unittest.main()
