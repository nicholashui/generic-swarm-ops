"""BE-07 residual admin: invitations, disable user, org update; BE-11 pause/expire."""
from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.runtime import PermissionDeniedError, ValidationError, runtime


class UsersOrgsLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token_bundle = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token_bundle["access_token"])
        cls.admin_token = token_bundle["access_token"]

    def test_invite_accept_and_login(self):
        email = f"invitee_{uuid.uuid4().hex[:8]}@example.com"
        inv = runtime.create_invitation(
            self.admin,
            {"email": email, "name": "Invitee", "role": "viewer", "department": "ops"},
        )
        self.assertEqual(inv["status"], "pending")
        self.assertTrue(inv["token"].startswith("inv_"))

        with self.assertRaises(PermissionDeniedError):
            runtime.issue_token(email, "anything-long")

        accepted = runtime.accept_invitation(inv["token"], "invitee-password-1", name="Invitee Active")
        self.assertEqual(accepted["message"], "invitation_accepted")
        self.assertIn("access_token", accepted)
        self.assertEqual(accepted["user"]["status"], "active")

        login = runtime.issue_token(email, "invitee-password-1")
        self.assertEqual(login["user"]["email"], email)

    def test_disable_user_blocks_login_and_auth(self):
        email = f"disable_{uuid.uuid4().hex[:8]}@example.com"
        created = runtime.create_user(
            self.admin,
            {"email": email, "name": "ToDisable", "role": "viewer", "password": "disable-pass-1"},
        )
        user_id = created["id"]
        login = runtime.issue_token(email, "disable-pass-1")
        tok = login["access_token"]
        runtime.authenticate(tok)

        updated = runtime.update_user(self.admin, user_id, {"status": "disabled"})
        self.assertEqual(updated["status"], "disabled")

        with self.assertRaises(PermissionDeniedError):
            runtime.issue_token(email, "disable-pass-1")
        with self.assertRaises(PermissionDeniedError):
            runtime.authenticate(tok)

    def test_update_organization_name(self):
        orgs = runtime.list_organizations(self.admin)
        self.assertTrue(orgs)
        org_id = orgs[0]["id"]
        new_name = f"Org {uuid.uuid4().hex[:6]}"
        updated = runtime.update_organization(self.admin, org_id, {"name": new_name})
        self.assertEqual(updated["name"], new_name)
        got = runtime.get_organization(self.admin, org_id)
        self.assertEqual(got["name"], new_name)

    def test_pause_resume_and_expire_run(self):
        workflows = runtime.list_workflows(self.admin)
        active = next((w for w in workflows if w.get("status") == "active"), workflows[0])
        # Create a synthetic queued run by starting then immediately pausing via status set
        run = runtime.start_workflow_run(
            active["id"],
            self.admin,
            {"case_id": f"case_{uuid.uuid4().hex[:8]}"},
            idempotency_key=f"idemp_{uuid.uuid4().hex[:10]}",
        )
        # After start, run may be terminal or waiting; force a non-terminal status for pause test
        stored = next(r for r in runtime.store.collection("workflow_runs") if r["id"] == run["id"])
        if stored["status"] in {"completed", "failed", "waiting_for_approval", "cancelled"}:
            stored["status"] = "running"
            runtime.store.save()

        paused = runtime.pause_run(self.admin, run["id"])
        self.assertEqual(paused["status"], "paused")

        resumed = runtime.resume_run(self.admin, run["id"])
        self.assertEqual(resumed["status"], "queued")

        # set running again then expire
        stored = next(r for r in runtime.store.collection("workflow_runs") if r["id"] == run["id"])
        stored["status"] = "running"
        runtime.store.save()
        expired = runtime.expire_run(self.admin, run["id"], reason="ttl")
        self.assertEqual(expired["status"], "expired")
        self.assertEqual(expired["error"], "ttl")

        with self.assertRaises(ValidationError):
            runtime.expire_run(self.admin, run["id"])


if __name__ == "__main__":
    unittest.main()
