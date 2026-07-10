"""P2: prove control-plane state survives a fresh RuntimeStore load from Postgres."""
from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.core.config import settings
from app.runtime import RuntimeStore, runtime


class PostgresRestartTests(unittest.TestCase):
    def test_marker_survives_new_store_instance(self):
        if not settings.use_postgres:
            self.skipTest("Postgres not configured (set DATABASE_URL / unset FORCE_JSON)")
        from app.infrastructure.database.session import database_status

        status = database_status()
        if not status.get("reachable"):
            self.skipTest(f"Postgres not reachable: {status}")

        marker = f"restart_{uuid.uuid4().hex}"
        # Use a list collection for the marker
        runtime.store.state.setdefault("restart_markers", [])
        if not isinstance(runtime.store.state["restart_markers"], list):
            runtime.store.state["restart_markers"] = []
        runtime.store.state["restart_markers"].append(
            {"id": marker, "organization_id": "org_default", "note": "p2_restart"}
        )
        runtime.store.save()
        self.assertEqual(runtime.store.backend, "postgres")

        # New store instance = process restart for the document store
        data_file = runtime.store.data_file
        reloaded = RuntimeStore(data_file)
        self.assertEqual(reloaded.backend, "postgres", "reload should hit Postgres")
        markers = reloaded.state.get("restart_markers") or []
        ids = [item.get("id") for item in markers if isinstance(item, dict)]
        self.assertIn(marker, ids)

        # Auth still works after reload path used by login
        user = runtime.authenticate("admin-token")
        workflows = runtime.list_workflows(user)
        self.assertTrue(any(w.get("id") == "wf_customer_onboarding_v12" for w in workflows))


if __name__ == "__main__":
    unittest.main()
