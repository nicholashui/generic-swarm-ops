"""DNA / workflow → topology + runnable step plan — LG-04."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def resolve_pattern(workflow: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    orch = workflow.get("orchestration") if isinstance(workflow.get("orchestration"), dict) else {}
    pattern = str(orch.get("pattern") or workflow.get("pattern") or "pipeline").strip().lower()
    config = dict(orch.get("config") or {})
    return pattern, config


def content_hash(workflow: dict[str, Any]) -> str:
    payload = {
        "id": workflow.get("id"),
        "version": workflow.get("version") or workflow.get("active_version"),
        "steps": workflow.get("steps") or [],
        "orchestration": workflow.get("orchestration") or {},
    }
    raw = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def build_topology(workflow: dict[str, Any]) -> dict[str, Any]:
    """Static topology for FE (nodes + edges)."""
    pattern, config = resolve_pattern(workflow)
    steps = workflow.get("steps") or []
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    if pattern == "supervisor":
        supervisor = config.get("supervisor_agent") or workflow.get("owner") or "supervisor"
        specialists = list(config.get("specialists") or [])
        nodes.append({"id": "supervisor", "kind": "supervisor", "agent_id": supervisor, "label": supervisor})
        for spec in specialists:
            nodes.append({"id": f"spec_{spec}", "kind": "specialist", "agent_id": spec, "label": spec})
            edges.append({"from": "supervisor", "to": f"spec_{spec}", "kind": "handoff"})
            edges.append({"from": f"spec_{spec}", "to": "supervisor", "kind": "return"})
        nodes.append({"id": "END", "kind": "end", "label": "END"})
        edges.append({"from": "supervisor", "to": "END", "kind": "done"})
    else:
        # pipeline / pack_spine / others: linear DNA steps
        for step in steps:
            sid = step.get("id") or "step"
            nodes.append(
                {
                    "id": sid,
                    "kind": "step",
                    "agent_id": step.get("agent"),
                    "tools": list(step.get("tools") or []),
                    "label": sid,
                    "human_gate": bool(
                        step.get("human_gate_required")
                        or step.get("irreversible")
                        or step.get("action_type") in {"irreversible_execution", "external_write"}
                    ),
                }
            )
        for i in range(len(steps) - 1):
            a = steps[i].get("id")
            b = steps[i + 1].get("id")
            if a and b:
                edges.append({"from": a, "to": b, "kind": "next"})
        if steps:
            edges.insert(0, {"from": "START", "to": steps[0].get("id"), "kind": "start"})
            edges.append({"from": steps[-1].get("id"), "to": "END", "kind": "end"})
            nodes.insert(0, {"id": "START", "kind": "start", "label": "START"})
            nodes.append({"id": "END", "kind": "end", "label": "END"})

    return {
        "workflow_id": workflow.get("id"),
        "pattern": pattern,
        "config": config,
        "content_hash": content_hash(workflow),
        "engine": "langgraph",
        "nodes": nodes,
        "edges": edges,
    }


def step_plan(workflow: dict[str, Any]) -> list[dict[str, Any]]:
    """Ordered steps for pipeline-style graph execution."""
    return list(workflow.get("steps") or [])
