"""LangGraph dual-engine + pipeline + topology tests (LG-01…07, 11)."""

from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.infrastructure.langgraph_engine.compiler import build_topology, resolve_pattern
from app.infrastructure.langgraph_engine.graph_builder import build_pipeline_graph
from app.infrastructure.langgraph_engine.patterns.catalog import PATTERN_CATALOG
from app.infrastructure.orchestration.registry import get_engine, list_engines, resolve_engine_name
from app.main import app
from app.runtime import runtime
from fastapi.testclient import TestClient


class LangGraphEngineTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        org = runtime.store.collection("organizations")[0]["id"]
        runtime._normalize_agents(org)
        runtime.store.save()

    def test_engines_registered(self):
        engines = {e["name"] for e in list_engines()}
        self.assertIn("legacy", engines)
        self.assertIn("langgraph", engines)
        self.assertEqual(get_engine("legacy").name, "legacy")
        self.assertEqual(get_engine("langgraph").name, "langgraph")

    def test_topology_pipeline(self):
        wf = {
            "id": "wf_demo",
            "steps": [
                {"id": "a", "agent": "x", "tools": ["crm"]},
                {"id": "b", "agent": "y", "tools": ["email"]},
            ],
            "orchestration": {"pattern": "pipeline"},
        }
        topo = build_topology(wf)
        self.assertEqual(topo["pattern"], "pipeline")
        ids = {n["id"] for n in topo["nodes"]}
        self.assertIn("a", ids)
        self.assertIn("b", ids)
        self.assertTrue(any(e["from"] == "a" and e["to"] == "b" for e in topo["edges"]))

    def test_stategraph_pipeline_compiles(self):
        seen: list[str] = []

        def make(sid: str):
            def _n(state: dict) -> dict:
                seen.append(sid)
                return {**state, "last": sid}

            return _n

        g = build_pipeline_graph(["s1", "s2"], make)
        out = g.invoke({})
        self.assertEqual(seen, ["s1", "s2"])
        self.assertEqual(out.get("last"), "s2")

    def test_langgraph_onboarding_with_gates(self):
        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "admin-password"},
        )
        self.assertEqual(login.status_code, 200)
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        case_id = f"case_lg_{uuid.uuid4().hex[:8]}"
        run_resp = self.client.post(
            "/api/v1/workflows/wf_customer_onboarding_v12/run",
            headers=headers,
            json={"input_payload": {"case_id": case_id, "triggered_from": "lg_test", "engine": "langgraph"}},
        )
        self.assertEqual(run_resp.status_code, 200, run_resp.text)
        run_id = run_resp.json()["id"]
        self.assertEqual(run_resp.json().get("engine"), "langgraph")

        dispatch = self.client.post("/api/v1/workflow-runs/dispatch", headers=headers, json={})
        self.assertEqual(dispatch.status_code, 200, dispatch.text)

        admin = runtime.authenticate(token)
        run = runtime.get_run(admin, run_id)
        safety = 0
        while run.get("status") == "waiting_for_approval" and safety < 8:
            appr = run.get("approval_request_id")
            self.assertTrue(appr)
            dec = self.client.post(
                f"/api/v1/approvals/{appr}/decision",
                headers=headers,
                json={"decision": "approved", "reason": "lg test"},
            )
            self.assertEqual(dec.status_code, 200, dec.text)
            run = runtime.get_run(admin, run_id)
            safety += 1

        self.assertEqual(run.get("status"), "completed", msg=run.get("error"))
        self.assertEqual(run.get("engine"), "langgraph")
        steps = {s["id"]: s["status"] for s in run.get("steps") or []}
        self.assertEqual(steps.get("activate_billing"), "completed")

        # topology API
        topo = self.client.get(
            "/api/v1/workflows/wf_customer_onboarding_v12/topology",
            headers=headers,
        )
        self.assertEqual(topo.status_code, 200)
        self.assertIn("nodes", topo.json())

        gs = self.client.get(f"/api/v1/workflow-runs/{run_id}/graph-state", headers=headers)
        self.assertEqual(gs.status_code, 200)
        self.assertEqual(gs.json().get("engine"), "langgraph")

        patterns = self.client.get("/api/v1/orchestration/patterns", headers=headers)
        self.assertEqual(patterns.status_code, 200)
        self.assertGreaterEqual(len(patterns.json().get("items") or []), 3)
        self.assertEqual(len(PATTERN_CATALOG), 6)

    def test_supervisor_pattern_run(self):
        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "admin-password"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        admin = runtime.authenticate(token)
        org = admin.organization_id
        wf_id = f"wf_sup_{uuid.uuid4().hex[:6]}"
        runtime.store.collection("workflows").append(
            {
                "id": wf_id,
                "organization_id": org,
                "name": "Supervisor Demo",
                "status": "active",
                "risk_tier": "tier_3_execute_reversible",
                "version": "1.0",
                "execution_engine": "langgraph",
                "orchestration": {
                    "pattern": "supervisor",
                    "config": {
                        "supervisor_agent": "business_orchestrator",
                        "specialists": ["business_orchestrator", "governance_officer"],
                        "max_handoffs": 4,
                    },
                },
                "input_schema": {
                    "type": "object",
                    "required": ["case_id"],
                    "properties": {"case_id": {"type": "string"}},
                },
                "steps": [
                    {
                        "id": "noop_seed",
                        "agent": "business_orchestrator",
                        "tools": ["audit_log_writer"],
                    }
                ],
            }
        )
        runtime.store.save()

        run_resp = self.client.post(
            f"/api/v1/workflows/{wf_id}/run",
            headers=headers,
            json={"input_payload": {"case_id": f"case_{uuid.uuid4().hex[:6]}", "engine": "langgraph"}},
        )
        self.assertEqual(run_resp.status_code, 200, run_resp.text)
        run_id = run_resp.json()["id"]
        self.client.post("/api/v1/workflow-runs/dispatch", headers=headers, json={})
        run = runtime.get_run(admin, run_id)
        self.assertEqual(run.get("status"), "completed", msg=run.get("error"))
        self.assertEqual(run.get("engine"), "langgraph")
        self.assertEqual(run.get("orchestration_pattern"), "supervisor")
        metrics = run.get("graph_metrics") or {}
        self.assertGreaterEqual(int(metrics.get("handoffs") or 0), 1)

    def test_resolve_engine_name(self):
        self.assertEqual(resolve_engine_name(explicit="langgraph"), "langgraph")
        self.assertEqual(resolve_engine_name(workflow={"execution_engine": "legacy"}), "legacy")
        p, _ = resolve_pattern({"orchestration": {"pattern": "supervisor"}})
        self.assertEqual(p, "supervisor")

    def test_health_reports_engines(self):
        r = self.client.get("/api/v1/health/ready")
        self.assertEqual(r.status_code, 200)
        deps = r.json().get("dependencies") or {}
        self.assertIn("orchestration_engines", deps)

    def test_patch_orchestration_pattern(self):
        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "admin-password"},
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        admin = runtime.authenticate(login.json()["access_token"])
        wf_id = f"wf_orch_{uuid.uuid4().hex[:6]}"
        runtime.store.collection("workflows").append(
            {
                "id": wf_id,
                "organization_id": admin.organization_id,
                "name": "Orch Patch",
                "status": "active",
                "risk_tier": "tier_3_execute_reversible",
                "version": "1.0",
                "owner": "business_orchestrator",
                "input_schema": {"type": "object", "properties": {}, "required": []},
                "steps": [
                    {"id": "s1", "agent": "business_orchestrator", "tools": ["audit_log_writer"]},
                ],
            }
        )
        runtime.store.save()
        patch = self.client.patch(
            f"/api/v1/workflows/{wf_id}",
            headers=headers,
            json={
                "execution_engine": "langgraph",
                "orchestration": {
                    "pattern": "supervisor",
                    "config": {
                        "supervisor_agent": "business_orchestrator",
                        "specialists": ["governance_officer"],
                        "max_handoffs": 6,
                    },
                },
            },
        )
        self.assertEqual(patch.status_code, 200, patch.text)
        body = patch.json()
        self.assertEqual(body.get("execution_engine"), "langgraph")
        self.assertEqual((body.get("orchestration") or {}).get("pattern"), "supervisor")
        topo = self.client.get(f"/api/v1/workflows/{wf_id}/topology", headers=headers)
        self.assertEqual(topo.status_code, 200)
        self.assertEqual(topo.json().get("pattern"), "supervisor")

    def test_pack_graphs_listed(self):
        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "admin-password"},
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        r = self.client.get("/api/v1/domains/video/graphs", headers=headers)
        self.assertEqual(r.status_code, 200, r.text)
        items = r.json().get("items") or []
        ids = {i.get("id") for i in items}
        self.assertIn("video_spine", ids)
        self.assertIn("viral_hook", ids)

    def test_critique_and_map_reduce_patterns(self):
        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "admin-password"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        admin = runtime.authenticate(token)
        org = admin.organization_id
        for pattern, config, extra_case in [
            ("critique", {"max_iterations": 2, "critic_agent": "governance_officer"}, {}),
            ("map_reduce", {"items_key": "items"}, {"items": [{"n": 1}, {"n": 2}]}),
            ("router", {"routes": {"default": ["s1"]}}, {"route": "default"}),
        ]:
            wf_id = f"wf_{pattern}_{uuid.uuid4().hex[:5]}"
            runtime.store.collection("workflows").append(
                {
                    "id": wf_id,
                    "organization_id": org,
                    "name": pattern,
                    "status": "active",
                    "risk_tier": "tier_3_execute_reversible",
                    "version": "1.0",
                    "execution_engine": "langgraph",
                    "orchestration": {"pattern": pattern, "config": config},
                    "input_schema": {
                        "type": "object",
                        "required": ["case_id"],
                        "properties": {"case_id": {"type": "string"}},
                    },
                    "steps": [
                        {
                            "id": "s1",
                            "agent": "business_orchestrator",
                            "tools": ["audit_log_writer"],
                        }
                    ],
                }
            )
            runtime.store.save()
            run_resp = self.client.post(
                f"/api/v1/workflows/{wf_id}/run",
                headers=headers,
                json={
                    "input_payload": {"case_id": f"c_{pattern}", **extra_case},
                    "engine": "langgraph",
                },
            )
            self.assertEqual(run_resp.status_code, 200, run_resp.text)
            run_id = run_resp.json()["id"]
            self.client.post("/api/v1/workflow-runs/dispatch", headers=headers, json={})
            run = runtime.get_run(admin, run_id)
            self.assertEqual(run.get("status"), "completed", msg=f"{pattern}: {run.get('error')}")
            traj = self.client.get(f"/api/v1/workflow-runs/{run_id}/trajectory", headers=headers)
            self.assertEqual(traj.status_code, 200)
            self.assertIn("score", (traj.json().get("trajectory") or {}))

    def test_approval_carries_graph_node(self):
        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "admin-password"},
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        run_resp = self.client.post(
            "/api/v1/workflows/wf_customer_onboarding_v12/run",
            headers=headers,
            json={"input_payload": {"case_id": f"case_apr_{uuid.uuid4().hex[:6]}"}, "engine": "langgraph"},
        )
        run_id = run_resp.json()["id"]
        self.client.post("/api/v1/workflow-runs/dispatch", headers=headers, json={})
        admin = runtime.authenticate(login.json()["access_token"])
        run = runtime.get_run(admin, run_id)
        if run.get("status") != "waiting_for_approval":
            self.skipTest("no gate on first steps")
        appr_id = run["approval_request_id"]
        detail = self.client.get(f"/api/v1/approvals/{appr_id}", headers=headers)
        self.assertEqual(detail.status_code, 200)
        body = detail.json()
        self.assertEqual(body.get("engine"), "langgraph")
        self.assertTrue(body.get("graph_node_id") or body.get("step_id"))
        self.assertIn("payload_preview", body)


if __name__ == "__main__":
    unittest.main()
