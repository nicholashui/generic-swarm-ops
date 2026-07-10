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


if __name__ == "__main__":
    unittest.main()
