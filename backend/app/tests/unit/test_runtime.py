import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.runtime import PermissionDeniedError, runtime


class RuntimeSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token_bundle = runtime.issue_token("admin@example.com", "admin-password")
        cls.current_user = runtime.authenticate(token_bundle["access_token"])

    def test_seeded_workflow_exists(self):
        workflows = runtime.list_workflows(self.current_user)
        self.assertTrue(workflows)
        self.assertTrue(any(item["id"] for item in workflows))

    def test_process_summary_has_counts(self):
        summary = runtime.process_summary(self.current_user)
        self.assertIn("workflow_run_count", summary)
        self.assertIn("processes", summary)

    def test_list_collection_helper(self):
        workflows = runtime.list_collection("workflows")
        self.assertIsInstance(workflows, list)

    def test_password_reset_requires_auth(self):
        with self.assertRaises(PermissionDeniedError):
            runtime.reset_password("admin@example.com", "new-password-123")

    def test_tier_level_mapping(self):
        self.assertEqual(runtime._tier_level("tier_5_restricted"), 5)
        self.assertEqual(runtime._tier_level("high"), 4)

    def test_issue_token_mints_unique_access_tokens_per_login(self):
        first = runtime.issue_token("admin@example.com", "admin-password")
        second = runtime.issue_token("admin@example.com", "admin-password")
        self.assertIn("access_token", first)
        self.assertIn("access_token", second)
        self.assertNotEqual(first["access_token"], second["access_token"])
        self.assertTrue(str(first["access_token"]).startswith("tok_"))
        self.assertTrue(str(second["access_token"]).startswith("tok_"))
        # Both tokens must authenticate until revoked
        u1 = runtime.authenticate(first["access_token"])
        u2 = runtime.authenticate(second["access_token"])
        self.assertEqual(u1.email, "admin@example.com")
        self.assertEqual(u2.email, "admin@example.com")
        # Logout revokes only the presented token
        runtime.logout(first["access_token"])
        with self.assertRaises(PermissionDeniedError):
            runtime.authenticate(first["access_token"])
        still = runtime.authenticate(second["access_token"])
        self.assertEqual(still.email, "admin@example.com")


if __name__ == "__main__":
    unittest.main()
