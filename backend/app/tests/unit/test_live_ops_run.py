"""Cross-stack live ops gate: real ASGI app + persisted flagship workflow run-start."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from fastapi.testclient import TestClient

from app.main import app
from app.runtime import runtime


class LiveOpsRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        # Ensure store normalization applied for this process
        orgs = runtime.list_collection("organizations")
        if orgs:
            runtime._normalize_workflows(orgs[0]["id"])
            runtime.store.save()

    def test_flagship_workflow_run_start_via_http(self):
        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "admin-password"},
        )
        self.assertEqual(login.status_code, 200, login.text)
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        workflows = self.client.get("/api/v1/workflows", headers=headers)
        self.assertEqual(workflows.status_code, 200, workflows.text)
        ids = [item["id"] for item in workflows.json()]
        self.assertIn("wf_customer_onboarding_v12", ids)

        # Missing required case_id must fail closed with validation, not KeyError/500
        bad = self.client.post(
            "/api/v1/workflows/wf_customer_onboarding_v12/run",
            headers=headers,
            json={"input_payload": {"triggered_from": "test_missing_case"}},
        )
        self.assertIn(bad.status_code, {400, 422}, bad.text)

        started = self.client.post(
            "/api/v1/workflows/wf_customer_onboarding_v12/run",
            headers=headers,
            json={"input_payload": {"case_id": "ac1_demo", "triggered_from": "test"}},
        )
        self.assertEqual(started.status_code, 200, started.text)
        body = started.json()
        self.assertTrue(body.get("id"), body)
        self.assertEqual(body.get("status"), "queued", body)
        self.assertEqual(body.get("workflow_id"), "wf_customer_onboarding_v12")

        # Runtime entry point agrees with HTTP
        user = runtime.authenticate(token)
        run = runtime.get_run(user, body["id"])
        self.assertEqual(run["status"], "queued")
        self.assertEqual(run["input_payload"].get("case_id"), "ac1_demo")

    def test_start_workflow_run_no_keyerror_on_dna_only_record(self):
        """Inject a DNA-only workflow then start it after normalization path."""
        org_id = runtime.list_collection("organizations")[0]["id"]
        dna_only = {
            "id": "wf_dna_only_live_ops",
            "name": "DNA only",
            "objective": "prove normalize",
            "production_ready": True,
            "risk_tier": "tier_2_draft",
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
        }
        # Strip execution fields intentionally
        workflows = [w for w in runtime.list_collection("workflows") if w.get("id") != "wf_dna_only_live_ops"]
        workflows.append(dna_only)
        runtime.store.state["workflows"] = workflows
        runtime.store.save()

        user = runtime.authenticate("admin-token")
        run = runtime.start_workflow_run(
            "wf_dna_only_live_ops",
            user,
            {"case_id": "normalize_demo", "triggered_from": "unit"},
        )
        self.assertEqual(run["status"], "queued")
        self.assertTrue(run["id"].startswith("run_"))


if __name__ == "__main__":
    unittest.main()
