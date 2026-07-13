"""Wave 1 ALC + domain pack tests — drive shipped runtime entry points."""
from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.infrastructure.governance.alc_validator import AlcRequiredError, assert_alc_ready, is_alc_ready
from app.infrastructure.self_improvement.lessons import Lesson, LessonLibrary
from app.runtime import ValidationError, runtime


class AlcValidatorTests(unittest.TestCase):
    def test_alc_ready_true(self):
        agent = {
            "requires_alc": True,
            "alc_version": "1.0",
            "allowed_memory_scopes": ["agent"],
            "hooks": {"reflect": True},
        }
        self.assertTrue(is_alc_ready(agent))
        assert_alc_ready(agent)

    def test_alc_ready_false_missing_scope(self):
        agent = {
            "requires_alc": True,
            "alc_version": "1.0",
            "allowed_memory_scopes": ["organization"],
            "hooks": {"reflect": True},
        }
        self.assertFalse(is_alc_ready(agent))
        with self.assertRaises(AlcRequiredError):
            assert_alc_ready(agent)


class LessonAgentIdTests(unittest.TestCase):
    def test_retrieve_filters_agent(self):
        lib = LessonLibrary(
            [
                {"id": "1", "text": "a", "agent_id": "agent_a", "workflow_id": "wf"},
                {"id": "2", "text": "b", "agent_id": "agent_b", "workflow_id": "wf"},
            ]
        )
        got = lib.retrieve(agent_id="agent_a", increment_uses=False)
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0].agent_id, "agent_a")

    def test_legacy_without_agent_id_loads(self):
        lib = LessonLibrary([{"id": "1", "text": "legacy", "workflow_id": "wf"}])
        self.assertEqual(len(lib.lessons), 1)
        self.assertIsNone(lib.lessons[0].agent_id)


class AlcRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])

    def test_activate_without_alc_denied(self):
        agent_id = f"agent_noalc_{uuid.uuid4().hex[:6]}"
        runtime.create_agent(
            self.admin,
            {
                "id": agent_id,
                "name": "No ALC",
                "role": "tester",
                "status": "draft",
                "requires_alc": True,
                "allowed_memory_scopes": ["organization"],
                "alc_version": "",
                "hooks": {"reflect": False},
                "allowed_tools": ["audit_log_writer"],
            },
        )
        with self.assertRaises(ValidationError) as ctx:
            runtime.update_agent_status(self.admin, agent_id, "active")
        self.assertIn("ALC", str(ctx.exception))

    def test_activate_with_alc_ok(self):
        agent_id = f"agent_alc_{uuid.uuid4().hex[:6]}"
        runtime.create_agent(
            self.admin,
            {
                "id": agent_id,
                "name": "ALC Ready",
                "role": "tester",
                "status": "draft",
                "requires_alc": True,
                "allowed_memory_scopes": ["agent", "organization_memory"],
                "alc_version": "1.0",
                "hooks": {"reflect": True},
                "allowed_tools": ["audit_log_writer"],
            },
        )
        updated = runtime.update_agent_status(self.admin, agent_id, "active")
        self.assertEqual(updated["status"], "active")

    def test_reflect_tags_agent_id(self):
        agent_id = f"agent_ref_{uuid.uuid4().hex[:6]}"
        runtime.create_agent(
            self.admin,
            {
                "id": agent_id,
                "name": "Reflect Agent",
                "role": "tester",
                "status": "active",
                "requires_alc": True,
                "allowed_memory_scopes": ["agent", "organization_memory"],
                "alc_version": "1.0",
                "hooks": {"reflect": True},
                "allowed_tools": ["audit_log_writer"],
            },
        )
        # Ensure agent is active (seed may force requires_alc false on create)
        agent = runtime.get_agent(self.admin, agent_id)
        agent_store = next(
            a
            for a in runtime.store.collection("agents")
            if a["id"] == agent_id and a.get("organization_id") == self.admin.organization_id
        )
        agent_store["requires_alc"] = True
        agent_store["allowed_memory_scopes"] = ["agent", "organization_memory"]
        agent_store["alc_version"] = "1.0"
        agent_store["hooks"] = {"reflect": True}
        agent_store["status"] = "active"
        runtime.store.save()

        wf_id = f"wf_alc_{uuid.uuid4().hex[:8]}"
        runtime.create_workflow(
            self.admin,
            {
                "id": wf_id,
                "name": "alc reflect",
                "risk_tier": "tier_1_recommend",
                "status": "active",
                "steps": [
                    {
                        "id": "s1",
                        "agent": agent_id,
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
        run = runtime.start_workflow_run(wf_id, self.admin, {})
        runtime.dispatch_queued_runs(self.admin)
        run = runtime.get_run(self.admin, run["id"])
        # Force terminal for reflect if still queued
        if run["status"] == "queued":
            run_store = next(r for r in runtime.store.collection("workflow_runs") if r["id"] == run["id"])
            run_store["status"] = "completed"
            for s in run_store["steps"]:
                s["status"] = "completed"
                s["agent_id"] = agent_id
            runtime.store.save()
        reflection = runtime.reflect_on_workflow_run(self.admin, run["id"])
        stored = reflection.get("stored_lessons") or []
        self.assertTrue(stored)
        self.assertTrue(any(l.get("agent_id") == agent_id for l in stored))
        lessons = runtime.list_improvement_lessons(self.admin, agent_id=agent_id)
        self.assertTrue(lessons)
        other = runtime.list_improvement_lessons(self.admin, agent_id="agent_does_not_exist_xyz")
        self.assertEqual(other, [])

    def test_isolation_agent_episodes(self):
        runtime.store.collection("agent_episodes").append(
            {
                "id": "ep_a",
                "organization_id": self.admin.organization_id,
                "agent_id": "agent_iso_a",
                "text": "secret A",
                "created_at": "t",
            }
        )
        runtime.store.collection("agent_episodes").append(
            {
                "id": "ep_b",
                "organization_id": self.admin.organization_id,
                "agent_id": "agent_iso_b",
                "text": "secret B",
                "created_at": "t",
            }
        )
        runtime.store.save()
        a = runtime.list_agent_episodes(self.admin, agent_id="agent_iso_a")
        self.assertTrue(all(e["agent_id"] == "agent_iso_a" for e in a))
        self.assertFalse(any(e["agent_id"] == "agent_iso_b" for e in a))

    def test_register_domain_example_research(self):
        result = runtime.register_domain_pack(
            self.admin,
            manifest_path="business/example_research/manifest.json",
        )
        self.assertEqual(result["domain_id"], "example_research")
        self.assertGreaterEqual(result["agents_loaded"], 2)
        agents = runtime.list_agents(self.admin)
        ids = {a["id"] for a in agents}
        self.assertIn("example.researcher", ids)
        packs = runtime.list_domain_packs(self.admin)
        self.assertTrue(any(p["domain_id"] == "example_research" for p in packs))

    def test_register_invalid_manifest_fails(self):
        with self.assertRaises(ValidationError):
            runtime.register_domain_pack(self.admin, manifest={"domain_id": "x"})

    def test_agent_genome_sandbox_only(self):
        variant = runtime.propose_evolution_variant(
            self.admin,
            {
                "variant_type": "agent_genome",
                "agent_id": "example.researcher",
                "name": "genome test",
                "genome": {"prompt": "be better"},
            },
        )
        self.assertTrue(variant.get("sandbox_only"))
        self.assertEqual(variant.get("variant_type"), "agent_genome")
        with self.assertRaises(Exception):
            runtime.propose_evolution_variant(
                self.admin,
                {
                    "variant_type": "agent_genome",
                    "agent_id": "example.researcher",
                    "direct_production_mutation": True,
                },
            )

    def test_metrics_endpoint_shape(self):
        metrics = runtime.improvement_metrics(self.admin, agent_id="example.researcher")
        self.assertIn("knowledge_growth_count", metrics)
        self.assertIn("lesson_reuse_rate", metrics)


if __name__ == "__main__":
    unittest.main()
