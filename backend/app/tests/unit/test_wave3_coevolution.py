"""Wave 3: coevolution, lesson utility, governance review, video corpus, skill sandbox."""
from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.infrastructure.evolution.coevolution import composite_fitness, enrich_fitness_with_alc
from app.infrastructure.evolution.corpus_eval import load_eval_corpus
from app.runtime import runtime


class Wave3CoevolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])
        cls.repo_root = runtime.repo_root
        cls.org_id = cls.admin.organization_id

    def _seed_lesson(self, agent_id: str, *, uses: int = 4, wins: int = 3, text: str | None = None) -> dict:
        lesson = {
            "id": f"lesson_w3_{uuid.uuid4().hex[:10]}",
            "organization_id": self.org_id,
            "text": text or f"Wave3 lesson for {agent_id}: keep hooks consistent {uuid.uuid4().hex[:6]}",
            "agent_id": agent_id,
            "workflow_id": "wf_video_arch_a_viral_hook_v1",
            "uses": uses,
            "wins": wins,
            "tags": ["wave3", "lqr"],
            "provenance": {"source_refs": ["test_wave3_coevolution"]},
        }
        runtime.store.state.setdefault("improvement_lessons", [])
        runtime.store.collection("improvement_lessons").append(lesson)
        runtime.store.save()
        return lesson

    def test_composite_fitness_helper(self):
        m = composite_fitness(1.0, knowledge_growth_count=10, lesson_reuse_rate=5.0)
        self.assertEqual(m["composite_fitness"], 1.0)
        self.assertEqual(m["suite_pass_rate"], 1.0)
        enriched = enrich_fitness_with_alc(
            {"suite_pass_rate": 0.5, "step_count": 3},
            {"knowledge_growth_count": 5, "lesson_reuse_rate": 2.5},
        )
        self.assertIn("composite_fitness", enriched)
        self.assertEqual(enriched["step_count"], 3)
        self.assertGreater(enriched["composite_fitness"], 0.3)

    def test_corpus_loads_video_pack_goldens(self):
        platform = load_eval_corpus(self.repo_root)
        video = load_eval_corpus(self.repo_root, domain_id="video")
        self.assertGreaterEqual(len(video["golden"]), len(platform["golden"]))
        ids = {g.get("id") for g in video["golden"]}
        self.assertIn("golden_video_lqr_consistency_v1", ids)
        # non-video domain should not pull video-only fixture via domain overlay
        other = load_eval_corpus(self.repo_root, domain_id="example_research")
        other_ids = {g.get("id") for g in other["golden"]}
        self.assertNotIn("golden_video_lqr_consistency_v1", other_ids)

    def test_coevolution_multi_generation_sandbox_only(self):
        # Production baseline for a known host workflow (version stability)
        base_before = runtime.get_workflow(self.admin, "wf_customer_onboarding_v12")
        run = runtime.run_coevolution_experiment(
            self.admin,
            generations=2,
            domain_id="video",
            base_workflow_id="wf_video_arch_a_viral_hook_v1",
        )
        self.assertGreaterEqual(run.get("generations_requested"), 2)
        self.assertGreaterEqual(len(run.get("generations") or []), 2)
        self.assertTrue(run.get("sandbox_only"))
        self.assertFalse(run.get("auto_promote"))
        self.assertEqual(len(run.get("variant_ids") or []), 4)  # 2 agents × 2 gens
        for gen in run["generations"]:
            self.assertIn("elite_fitness", gen)
            self.assertIn("fitness_metrics", gen)
            self.assertTrue(gen.get("variant_ids"))
        # Variants audited as sandbox
        for vid in run["variant_ids"]:
            variant = next(
                v
                for v in runtime.store.collection("evolution_variants")
                if v.get("id") == vid
            )
            self.assertTrue(variant.get("sandbox_only"))
            self.assertEqual(variant.get("variant_type"), "agent_genome")
            self.assertIsNotNone(variant.get("fitness_metrics"))
            self.assertIn("composite_fitness", variant.get("fitness_metrics") or {})
        # Host production DNA unchanged
        base_after = runtime.get_workflow(self.admin, "wf_customer_onboarding_v12")
        self.assertEqual(base_after.get("version"), base_before.get("version"))
        # Audit trail
        audits = [
            a
            for a in runtime.store.collection("audit_logs")
            if a.get("action") == "evolution.coevolution_completed" and a.get("resource_id") == run["id"]
        ]
        self.assertTrue(audits, "coevolution_completed audit missing")

    def test_fitness_includes_alc_when_lessons(self):
        agent_id = f"video.planner"
        self._seed_lesson(agent_id, uses=6, wins=5)
        from app.infrastructure.evolution.coevolution import load_pack_workflow_dna

        dna = load_pack_workflow_dna(self.repo_root, "video", "wf_video_arch_a_viral_hook_v1") or {
            "id": "wf_video_arch_a_viral_hook_v1",
            "domain": "video",
            "production_ready": False,
            "steps": [],
        }
        dna = dict(dna)
        dna["domain"] = "video"
        dna["production_ready"] = False
        variant = runtime.propose_evolution_variant(
            self.admin,
            {
                "variant_type": "agent_genome",
                "agent_id": agent_id,
                "name": f"alc_fit_{uuid.uuid4().hex[:6]}",
                "genome": {"generation": 1, "version": 1, "sandbox_only": True},
                "dna": dna,
                "changes": ["alc fitness"],
            },
        )
        evaluated = runtime.sandbox_evaluate_variant(self.admin, variant["id"])
        fm = evaluated.get("fitness_metrics") or {}
        self.assertIn("suite_pass_rate", fm)
        self.assertIn("knowledge_growth", fm)
        self.assertIn("lesson_reuse", fm)
        self.assertIn("composite_fitness", fm)
        self.assertGreaterEqual(float(fm.get("knowledge_growth") or 0), 1)

    def test_lesson_utility_dashboard_ranked(self):
        # Unique agent_id so ranking is not drowned by other tests' seeded lessons
        agent_id = f"video.rank_{uuid.uuid4().hex[:8]}"
        low = self._seed_lesson(agent_id, uses=10, wins=1, text=f"low util {uuid.uuid4().hex[:6]}")
        high = self._seed_lesson(agent_id, uses=2, wins=2, text=f"high util {uuid.uuid4().hex[:6]}")
        dash = runtime.lesson_utility_dashboard(self.admin, agent_id=agent_id, limit=50)
        self.assertIn("lessons", dash)
        self.assertIn("aggregates", dash)
        self.assertGreaterEqual(dash["aggregates"]["total_lessons"], 2)
        lessons = dash["lessons"]
        ids = [l.get("id") for l in lessons]
        self.assertIn(high["id"], ids)
        self.assertIn(low["id"], ids)
        # Ranked by utility descending
        utilities = [float(l.get("utility") or 0) for l in lessons]
        self.assertEqual(utilities, sorted(utilities, reverse=True))
        high_u = next(l for l in lessons if l["id"] == high["id"])
        low_u = next(l for l in lessons if l["id"] == low["id"])
        self.assertGreaterEqual(float(high_u["utility"]), float(low_u["utility"]))

    def test_governance_review_lists_pending(self):
        variant = runtime.propose_evolution_variant(
            self.admin,
            {
                "variant_type": "agent_genome",
                "agent_id": "video.aiqaconsistency",
                "name": f"gov_rev_{uuid.uuid4().hex[:6]}",
                "genome": {"generation": 0, "version": 1},
                "dna": {"id": "wf_video_arch_a_viral_hook_v1", "domain": "video", "production_ready": False, "steps": []},
                "changes": ["governance"],
            },
        )
        skill = runtime.propose_skill_sandbox(
            self.admin,
            {
                "skill_name": f"video-hook-prompt-{uuid.uuid4().hex[:6]}",
                "content": "# Video hook prompt sandbox\n\nAlways lead with curiosity, never auto-publish.",
                "rationale": "wave3 skill sandbox",
                "domain": "video",
                "agent_id": "video.screenwriter",
            },
        )
        review = runtime.governance_review_learned_artifacts(self.admin)
        self.assertFalse(review.get("auto_promote"))
        self.assertEqual(review.get("policy"), "human_signoff_required")
        v_ids = {v.get("id") for v in review.get("pending_variants") or []}
        s_ids = {s.get("id") for s in review.get("pending_skills") or []}
        self.assertIn(variant["id"], v_ids)
        self.assertIn(skill["id"], s_ids)

    def test_video_skill_sandbox_propose(self):
        name = f"video-lqr-prompt-{uuid.uuid4().hex[:6]}"
        proposal = runtime.propose_skill_sandbox(
            self.admin,
            {
                "skill_name": name,
                "content": "Video LQR sandbox skill content — consistency and hook clarity checks.",
                "rationale": "wave3 video skill",
                "domain": "video",
            },
        )
        self.assertTrue(proposal.get("sandbox_only"))
        self.assertEqual(proposal.get("domain"), "video")
        path = str(proposal.get("written_path") or proposal.get("sandbox_path") or "")
        self.assertIn("_sandbox", path)
        # File exists under repo
        written = self.repo_root / path if not Path(path).is_absolute() else Path(path)
        self.assertTrue(written.is_file(), f"missing sandbox skill file {written}")


if __name__ == "__main__":
    unittest.main()
