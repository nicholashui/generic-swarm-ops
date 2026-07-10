"""E1 operator path — login → lists → create → run → approve → complete → improve."""
from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from fastapi.testclient import TestClient

from app.main import app
from app.runtime import runtime


class E1OperatorPathTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Ensure seed agent scopes are current for flagship path
        org = runtime.store.collection("organizations")[0]["id"]
        runtime._normalize_agents(org)
        runtime.store.save()

    def test_e1_full_api_path(self):
        ready = self.client.get("/api/v1/health/ready")
        self.assertEqual(ready.status_code, 200)
        body = ready.json()
        db = (body.get("dependencies") or body).get("database")
        self.assertIn(db, {"postgres", "json-file"})

        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "admin-password"},
        )
        self.assertEqual(login.status_code, 200)
        token = login.json().get("access_token")
        self.assertTrue(token)
        headers = {"Authorization": f"Bearer {token}"}

        for path in ("/api/v1/workflows", "/api/v1/agents", "/api/v1/approvals"):
            r = self.client.get(path, headers=headers)
            self.assertEqual(r.status_code, 200, path)
            self.assertIsInstance(r.json(), list)

        agent_id = f"agent_e1_{uuid.uuid4().hex[:6]}"
        created = self.client.post(
            "/api/v1/agents",
            headers=headers,
            json={
                "id": agent_id,
                "name": "E1 Agent",
                "description": "E1 checklist",
                "status": "active",
                "allowed_tools": ["audit_log_writer"],
                "allowed_memory_scopes": ["workflow_memory", "organization_memory"],
                "risk_level": "tier_2_draft",
            },
        )
        self.assertEqual(created.status_code, 200)

        case_id = f"case_e1_{uuid.uuid4().hex[:8]}"
        run_resp = self.client.post(
            "/api/v1/workflows/wf_customer_onboarding_v12/run",
            headers=headers,
            json={"input_payload": {"case_id": case_id, "triggered_from": "e1_operator_path"}},
        )
        self.assertEqual(run_resp.status_code, 200, run_resp.text)
        run_id = run_resp.json()["id"]
        admin = runtime.authenticate(token)
        runtime.dispatch_queued_runs(admin)
        run = runtime.get_run(admin, run_id)

        safety = 0
        while run.get("status") == "waiting_for_approval" and safety < 6:
            reviewer = runtime.authenticate("reviewer-token")
            runtime.decide_approval(run["approval_request_id"], "approved", "e1 operator path", reviewer)
            run = runtime.get_run(admin, run_id)
            safety += 1

        self.assertEqual(run["status"], "completed", msg=run.get("error"))
        steps = {s["id"]: s["status"] for s in run.get("steps") or []}
        self.assertEqual(steps.get("activate_billing"), "completed")

        # Improve pipeline: reflect → propose → evaluate → canary
        reflection = runtime.reflect_on_workflow_run(admin, run_id)
        self.assertIn("lessons", reflection)
        variant = runtime.auto_propose_from_failures(
            admin, workflow_id="wf_customer_onboarding_v12", run_id=run_id
        )
        self.assertTrue(variant.get("sandbox_only"))
        evaluated = runtime.sandbox_evaluate_variant(admin, variant["id"])
        self.assertEqual(evaluated.get("evaluation", {}).get("result"), "passed")
        canary = runtime.promote_evolution_variant(admin, variant["id"], mode="canary")
        self.assertEqual(canary.get("status"), "approved_for_canary")

        audits = runtime.list_audit_logs(admin)
        self.assertTrue(any(a.get("action") in {"tool.executed", "workflow_run.completed", "improvement.reflected"} for a in audits))
        memory = runtime.list_collection("memory_items")
        self.assertTrue(memory)

        archive = runtime.evolution_archive(admin)
        self.assertGreaterEqual(archive.get("archive_size") or 0, 1)


if __name__ == "__main__":
    unittest.main()
