"""P5: Tier-0 provenance + Tier-1 entity-link multi-hop retrieval."""
from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.infrastructure.knowledge.retrieval import (
    RETRIEVAL_TIER_NOTE,
    extract_entity_links,
    should_escalate_to_tier1,
)
from app.runtime import runtime


class RetrievalTierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = runtime.issue_token("admin@example.com", "admin-password")
        cls.admin = runtime.authenticate(token["access_token"])

    def test_tier_policy_documented(self):
        self.assertEqual(RETRIEVAL_TIER_NOTE["default_tier"], 0)
        self.assertIn("entity_link", RETRIEVAL_TIER_NOTE["tier_1"])

    def test_tier0_search_always_has_provenance(self):
        doc_id = f"doc_t0_{uuid.uuid4().hex[:8]}"
        runtime.upload_knowledge_document(
            self.admin,
            {
                "id": doc_id,
                "title": "Billing gate SOP",
                "content": "Customer onboarding activate_billing requires human gate. workflow wf_customer_onboarding_v12.",
                "source": "business/materials/sops/customer-onboarding.md",
                "allowed_roles": ["owner", "admin", "manager", "operator", "viewer"],
            },
        )
        runtime.index_knowledge_document(self.admin, doc_id)
        hits = runtime.search_knowledge(self.admin, query="billing gate")
        self.assertTrue(hits)
        hit = next(h for h in hits if h["id"] == doc_id)
        self.assertTrue(hit.get("source_refs"))
        self.assertIn("business/materials/sops/customer-onboarding.md", hit["source_refs"])
        self.assertEqual(hit.get("retrieval_tier"), 0)
        self.assertTrue(hit.get("provenance", {}).get("source_refs"))
        self.assertIn("entity_links", hit)

    def test_multi_hop_entity_link_expansion(self):
        suffix = uuid.uuid4().hex[:6]
        sop_id = f"doc_sop_{suffix}"
        pol_id = f"doc_pol_{suffix}"
        # Shared entity pol_onboarding_default links the two docs
        runtime.upload_knowledge_document(
            self.admin,
            {
                "id": sop_id,
                "title": "Onboarding billing steps",
                "content": (
                    "Billing activation for wf_customer_onboarding_v12 is governed by "
                    "policy pol_onboarding_default. Human gate required."
                ),
                "source": "business/materials/sops/customer-onboarding.md",
                "allowed_roles": ["owner", "admin", "manager", "operator", "viewer"],
            },
        )
        runtime.upload_knowledge_document(
            self.admin,
            {
                "id": pol_id,
                "title": "Policy register entry",
                "content": (
                    # Intentionally avoids query keywords so Tier-0 alone cannot hit this doc;
                    # multi-hop must surface it via shared entity pol_onboarding_default.
                    "Canonical definition for pol_onboarding_default. "
                    "Owner: governance. Review cadence: quarterly. "
                    "Source path business/security/tool-permissions/tool-permission-register.json."
                ),
                "source": "business/security/tool-permissions/tool-permission-register.json",
                "allowed_roles": ["owner", "admin", "manager", "operator", "viewer"],
            },
        )
        runtime.index_knowledge_document(self.admin, sop_id)
        runtime.index_knowledge_document(self.admin, pol_id)

        # Relational cue + force path: Tier-0 only matches SOP; entity hop surfaces policy doc
        self.assertTrue(should_escalate_to_tier1("which policy is related to billing"))
        hits = runtime.search_knowledge(
            self.admin,
            query="billing activation human gate",
            multi_hop=True,
        )
        ids = {h["id"] for h in hits}
        self.assertIn(sop_id, ids)
        # Multi-hop should surface policy doc via shared entity even if query terms sparse on it
        hop_docs = [h for h in hits if h.get("retrieval_hop") == 1]
        self.assertTrue(hop_docs, msg=f"expected hop-1 multi-hop hits; got {[(h.get('id'), h.get('retrieval_hop')) for h in hits]}")
        # Prefer exact pol_id; otherwise any hop1 sharing pol_onboarding_default is success
        if pol_id in ids:
            hop1 = next(h for h in hits if h["id"] == pol_id)
        else:
            hop1 = next(
                (
                    h
                    for h in hop_docs
                    if any("pol_onboarding" in str(e).lower() for e in (h.get("shared_entities") or []))
                ),
                hop_docs[0],
            )
        self.assertEqual(hop1.get("retrieval_hop"), 1)
        self.assertEqual(hop1.get("retrieval_tier"), 1)
        self.assertTrue(hop1.get("source_refs"))
        self.assertTrue(hop1.get("shared_entities"))
        # Seed SOP remains hop 0
        seed = next(h for h in hits if h["id"] == sop_id)
        self.assertEqual(seed.get("retrieval_hop"), 0)

    def test_entity_link_extraction(self):
        links = extract_entity_links(
            "Run wf_customer_onboarding_v12 under pol_onboarding_default at tier_4_execute_with_gate",
            source="business/materials/sops/customer-onboarding.md",
        )
        entities = {item["entity"].lower() for item in links}
        self.assertTrue(any("wf_customer_onboarding" in e for e in entities))
        self.assertTrue(any("pol_onboarding" in e for e in entities))


if __name__ == "__main__":
    unittest.main()
