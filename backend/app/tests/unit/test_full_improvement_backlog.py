"""Full backlog: auto-reflect, embeddings, archive, federation, skill sandbox."""
from __future__ import annotations

import json
import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.core.config import settings
from app.infrastructure.knowledge.embeddings import cosine_similarity, embed_text
from app.runtime import runtime


class FullImprovementBacklogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])

    def test_auto_reflect_on_terminal_run(self):
        self.assertTrue(settings.auto_reflect)
        wf_id = f"wf_ar_{uuid.uuid4().hex[:8]}"
        runtime.create_workflow(
            self.admin,
            {
                "id": wf_id,
                "name": "auto reflect",
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
                "input_schema": {"type": "object", "properties": {}, "required": []},
                "output_schema": {"type": "object", "properties": {"outcome": {"type": "string"}}, "required": []},
                "evaluation_policy": {"block_on_fail": False},
            },
        )
        run = runtime.start_workflow_run(wf_id, self.admin, {"case_id": "c1"})
        runtime.dispatch_queued_runs(self.admin)
        run = runtime.get_run(self.admin, run["id"])
        self.assertIn(run["status"], {"completed", "failed", "waiting_for_approval"})
        self.assertTrue(run.get("auto_reflected"), msg=f"expected auto_reflected on {run}")
        lessons = runtime.list_improvement_lessons(self.admin, workflow_id=wf_id)
        self.assertTrue(lessons)

    def test_embeddings_and_index(self):
        a = embed_text("customer onboarding human gate billing")
        b = embed_text("customer onboarding human gate billing activation")
        c = embed_text("unrelated astronomy nebula")
        self.assertGreater(cosine_similarity(a, b), cosine_similarity(a, c))
        doc_id = f"doc_emb_{uuid.uuid4().hex[:8]}"
        runtime.upload_knowledge_document(
            self.admin,
            {
                "id": doc_id,
                "title": "Embedding SOP",
                "content": "Customer onboarding requires human gate for billing activation.",
                "source": "business/materials/sops/customer-onboarding.md",
                "allowed_roles": ["owner", "admin", "manager", "operator", "viewer"],
            },
        )
        indexed = runtime.index_knowledge_document(self.admin, doc_id)
        self.assertTrue(indexed.get("embedding"))
        self.assertEqual(indexed.get("embedding_dims"), 64)

    def test_evolution_archive(self):
        archive = runtime.evolution_archive(self.admin)
        self.assertIn("variants", archive)
        self.assertIn("archive_size", archive)
        self.assertEqual(archive.get("framework"), "dgm_population_archive_lite")

    def test_federation_export(self):
        # Ensure at least one graph node exists
        doc_id = f"doc_fed_{uuid.uuid4().hex[:8]}"
        runtime.upload_knowledge_document(
            self.admin,
            {
                "id": doc_id,
                "title": "Fed graph",
                "content": "wf_customer_onboarding_v12 requires pol_onboarding_default.",
                "source": "business/materials/sops/customer-onboarding.md",
                "allowed_roles": ["owner", "admin", "manager", "operator", "viewer"],
            },
        )
        runtime.index_knowledge_document(self.admin, doc_id)
        result = runtime.federate_knowledge_graph(self.admin, push_neo4j=False)
        self.assertTrue(result.get("cypher_path") or result.get("latest_cypher"))
        self.assertTrue(result.get("json_path") or result.get("latest_json"))
        latest = Path(result["latest_json"])
        self.assertTrue(latest.is_file())

    def _resolve_repo_path(self, value: str) -> Path:
        path = Path(value)
        if path.is_file():
            return path
        return runtime.repo_root / value

    def test_skill_sandbox_propose_and_promote(self):
        prop = runtime.propose_skill_sandbox(
            self.admin,
            {
                "skill_name": f"test-skill-{uuid.uuid4().hex[:6]}",
                "content": "# Test skill\n\nAlways require human gate on billing steps.\n\nProvenance required.",
                "rationale": "unit test sandbox skill",
            },
        )
        self.assertTrue(prop.get("sandbox_only"))
        self.assertTrue(prop.get("written_path"))
        written = self._resolve_repo_path(prop["written_path"])
        self.assertTrue(written.is_file())
        # Product naming: no legacy genetic typo in stored skill paths
        blob = json.dumps(prop)
        self.assertNotIn("genetic-swarm-ops", blob)
        self.assertNotIn("GENETIC_SWARM", blob)
        promoted = runtime.promote_skill_sandbox(self.admin, prop["id"])
        self.assertEqual(promoted.get("status"), "promoted")
        self.assertTrue(self._resolve_repo_path(promoted["promoted_path"]).is_file())
        self.assertNotIn("genetic-swarm-ops", json.dumps(promoted))


if __name__ == "__main__":
    unittest.main()
