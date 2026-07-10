"""P3: process-intelligence artifacts + evolution corpus/fitness/canary/rollback."""
from __future__ import annotations

import json
import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.runtime import PermissionDeniedError, ValidationError, runtime


class ProcessIntelligenceArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])
        cls.repo_root = runtime.repo_root

    def test_ingest_writes_disk_and_store_artifacts(self):
        marker = f"activity_p3_{uuid.uuid4().hex[:8]}"
        process_id = f"proc_p3_{uuid.uuid4().hex[:6]}"
        event = runtime.ingest_event_log(
            self.admin,
            {
                "process_id": process_id,
                "case_id": f"case_p3_{uuid.uuid4().hex[:6]}",
                "activity": marker,
                "outcome": {"status": "completed", "latency_minutes": 42},
            },
        )
        self.assertTrue(event.get("pi_artifacts"))
        # Disk artifacts
        disc_path = self.repo_root / "business" / "process-intelligence" / "discovered-processes" / f"{process_id}.json"
        conf_path = self.repo_root / "business" / "process-intelligence" / "conformance-reports" / f"{process_id}.json"
        bn_path = self.repo_root / "business" / "process-intelligence" / "bottlenecks" / "latest.json"
        self.assertTrue(disc_path.is_file(), f"missing {disc_path}")
        self.assertTrue(conf_path.is_file(), f"missing {conf_path}")
        self.assertTrue(bn_path.is_file(), f"missing {bn_path}")
        disc = json.loads(disc_path.read_text(encoding="utf-8"))
        self.assertEqual(disc["process_id"], process_id)
        self.assertIn(marker, disc["activities"])
        self.assertIn("provenance", disc)

        # Store artifacts (Postgres / runtime document)
        stored = runtime.list_pi_artifacts(self.admin)
        self.assertTrue(any(a.get("process_id") == process_id for a in stored))

        # APIs expose artifact_path
        discovered = runtime.discovered_processes(self.admin)
        hit = next(d for d in discovered if d["process_id"] == process_id)
        self.assertTrue(hit.get("artifact_path"))
        conf = runtime.conformance_report(self.admin, process_id=process_id)
        self.assertIn("conformance_score", conf)
        self.assertTrue(conf.get("artifact_path"))
        bottlenecks = runtime.process_bottlenecks(self.admin)
        self.assertTrue(any(b.get("activity") == marker for b in bottlenecks if b.get("type") == "activity_latency"))


class EvolutionLoopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])

    def _flagship_dna(self) -> dict:
        base = runtime.get_workflow(self.admin, "wf_customer_onboarding_v12")
        return {
            "id": "wf_customer_onboarding_v12",
            "name": base.get("name"),
            "risk_tier": base.get("risk_tier", "tier_4_execute_with_gate"),
            "steps": base.get("steps") or [],
            "rollback": base.get("rollback")
            or {
                "reversible": True,
                "rollback_steps": ["disable_customer_record", "void_initial_invoice"],
            },
            "production_ready": False,
            "auto_promote": False,
        }

    def test_sandbox_eval_loads_disk_corpus_and_fitness(self):
        dna = self._flagship_dna()
        variant = runtime.propose_evolution_variant(
            self.admin,
            {
                "base_workflow_id": "wf_customer_onboarding_v12",
                "name": f"p3_eval_{uuid.uuid4().hex[:6]}",
                "changes": ["p3 fitness test"],
                "dna": dna,
            },
        )
        base_before = runtime.get_workflow(self.admin, "wf_customer_onboarding_v12")
        evaluated = runtime.sandbox_evaluate_variant(self.admin, variant["id"])
        evaluation = evaluated["evaluation"]
        self.assertIn("fitness_metrics", evaluation)
        self.assertIn("corpus_loaded", evaluation)
        for suite in ("golden", "regression", "adversarial", "historical_replay"):
            self.assertGreaterEqual(evaluation["corpus_loaded"].get(suite, 0), 1, f"suite {suite} empty")
            self.assertIn(suite, evaluation["checks"])
        self.assertIn(evaluation["result"], {"passed", "failed"})
        self.assertEqual(evaluation.get("auto_promote"), False)
        self.assertNotEqual(evaluation.get("promotion_decision"), "promote")
        # Fitness recorded on variant
        self.assertTrue(evaluated.get("fitness_metrics") or evaluation.get("fitness_metrics"))
        # Production DNA unchanged by evaluate
        base_after = runtime.get_workflow(self.admin, "wf_customer_onboarding_v12")
        self.assertEqual(base_after.get("version"), base_before.get("version"))
        self.assertEqual(base_after.get("active_version"), base_before.get("active_version"))

    def test_canary_versioned_promote_and_rollback(self):
        dna = self._flagship_dna()
        # Ensure rollback metadata present for promote path
        dna["rollback"] = {
            "reversible": True,
            "rollback_steps": ["set_active_version_to_previous", "notify_ops_owner"],
        }
        base_before = runtime.get_workflow(self.admin, "wf_customer_onboarding_v12")
        steps_fingerprint = json.dumps(base_before.get("steps") or [], sort_keys=True)
        variant = runtime.propose_evolution_variant(
            self.admin,
            {
                "base_workflow_id": "wf_customer_onboarding_v12",
                "name": f"p3_canary_{uuid.uuid4().hex[:6]}",
                "dna": dna,
                "rollback_plan": ["set_active_version_to_previous", "notify_ops_owner"],
            },
        )
        evaluated = runtime.sandbox_evaluate_variant(self.admin, variant["id"])
        self.assertEqual(
            evaluated["evaluation"]["result"],
            "passed",
            msg=json.dumps(evaluated["evaluation"].get("suite_results"), indent=2),
        )
        canary = runtime.promote_evolution_variant(self.admin, variant["id"], mode="canary")
        self.assertEqual(canary["status"], "approved_for_canary")
        self.assertTrue(canary.get("rollback_plan"))

        # Propose must not have mutated production steps
        mid = runtime.get_workflow(self.admin, "wf_customer_onboarding_v12")
        self.assertEqual(json.dumps(mid.get("steps") or [], sort_keys=True), steps_fingerprint)

        promoted = runtime.promote_evolution_variant(self.admin, variant["id"], mode="promote")
        self.assertEqual(promoted["status"], "promoted_canary")
        self.assertTrue(promoted.get("promoted_version"))
        base_after = runtime.get_workflow(self.admin, "wf_customer_onboarding_v12")
        self.assertEqual(base_after["active_version"], promoted["promoted_version"])
        self.assertTrue(any(v.get("from_variant_id") == variant["id"] for v in base_after.get("versions") or []))
        # Base workflow id preserved (versioned, not replaced)
        self.assertEqual(base_after["id"], "wf_customer_onboarding_v12")

        rolled = runtime.rollback_evolution_variant(self.admin, variant["id"])
        self.assertEqual(rolled["status"], "rolled_back")
        restored = runtime.get_workflow(self.admin, "wf_customer_onboarding_v12")
        self.assertEqual(restored["active_version"], promoted.get("previous_version") or base_before.get("active_version") or base_before.get("version"))

    def test_direct_mutation_still_blocked(self):
        with self.assertRaises(PermissionDeniedError):
            runtime.propose_evolution_variant(
                self.admin,
                {
                    "base_workflow_id": "wf_customer_onboarding_v12",
                    "direct_production_mutation": True,
                    "name": "evil_p3",
                },
            )

    def test_failed_eval_blocks_promote(self):
        variant = runtime.propose_evolution_variant(
            self.admin,
            {
                "base_workflow_id": "wf_customer_onboarding_v12",
                "name": f"p3_fail_{uuid.uuid4().hex[:6]}",
                "dna": {
                    "id": "wf_customer_onboarding_v12",
                    "risk_tier": "tier_4_execute_with_gate",
                    "production_ready": True,  # fail closed in sandbox
                    "steps": [
                        {
                            "id": "activate_billing",
                            "tools": ["billing_system"],
                            "action_type": "irreversible_execution",
                            "human_gate_required": False,
                            "irreversible": False,
                        }
                    ],
                    "bypass_tool_allowlist": True,
                },
            },
        )
        evaluated = runtime.sandbox_evaluate_variant(self.admin, variant["id"])
        self.assertEqual(evaluated["evaluation"]["result"], "failed")
        with self.assertRaises(PermissionDeniedError):
            runtime.promote_evolution_variant(self.admin, variant["id"], mode="canary")


if __name__ == "__main__":
    unittest.main()
