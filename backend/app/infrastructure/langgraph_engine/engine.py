"""LangGraphWorkflowEngine — full multi-pattern host engine."""

from __future__ import annotations

from typing import Any

from app.core.config import settings
from app.infrastructure.langgraph_engine.checkpointer import get_checkpointer, thread_id_for
from app.infrastructure.langgraph_engine.compiler import build_topology, resolve_pattern
from app.infrastructure.langgraph_engine.graph_builder import build_pipeline_graph
from app.infrastructure.langgraph_engine.pack_loader import load_pack_graph
from app.infrastructure.langgraph_engine.patterns.runners import (
    run_critique,
    run_map_reduce,
    run_pack_spine,
    run_pipeline_steps,
    run_router,
    run_supervisor,
)
from app.infrastructure.langgraph_engine.security import assert_thread_tenant, enforce_budgets
from app.infrastructure.langgraph_engine.state import project_state_to_run, seed_state_from_run
from app.infrastructure.langgraph_engine.trajectory import score_trajectory


class LangGraphWorkflowEngine:
    name = "langgraph"

    def __init__(self) -> None:
        self._checkpointer = get_checkpointer()
        self._states: dict[str, dict[str, Any]] = {}

    def execute(self, runtime: Any, run: dict[str, Any], actor_user_id: str) -> None:
        try:
            self._execute_body(runtime, run, actor_user_id, resume=False)
        finally:
            try:
                if run.get("status") in {"completed", "failed", "waiting_for_approval"}:
                    runtime._auto_reflect_if_enabled(run, actor_user_id)
            except Exception:  # noqa: BLE001
                pass

    def resume_from_approval(
        self,
        runtime: Any,
        run: dict[str, Any],
        actor_user_id: str,
        *,
        decision: str,
        reason: str | None = None,
    ) -> None:
        if decision != "approved":
            return
        try:
            self._execute_body(runtime, run, actor_user_id, resume=True)
        finally:
            try:
                if run.get("status") in {"completed", "failed", "waiting_for_approval"}:
                    runtime._auto_reflect_if_enabled(run, actor_user_id)
            except Exception:  # noqa: BLE001
                pass

    def get_live_state(self, thread_id: str) -> dict[str, Any] | None:
        return self._states.get(thread_id)

    def _execute_body(self, runtime: Any, run: dict[str, Any], actor_user_id: str, *, resume: bool) -> None:
        workflow = next(
            (
                item
                for item in runtime._scoped_items("workflows", run["organization_id"])
                if item["id"] == run["workflow_id"]
            ),
            None,
        )
        if not workflow:
            run["status"] = "failed"
            run["error"] = f"Workflow not found: {run['workflow_id']}"
            return

        pattern, config = resolve_pattern(workflow)
        # Optional pack graph overlay by workflow metadata
        pack_graph_id = (workflow.get("pack_graph_id") or config.get("graph_id")) if isinstance(config, dict) else None
        domain = workflow.get("domain_id") or workflow.get("domain") or config.get("domain_id")
        if pack_graph_id or pattern == "pack_spine":
            g = load_pack_graph(str(domain or "video"), pack_graph_id if isinstance(pack_graph_id, str) else None)
            if g and g.get("orchestration"):
                pattern = g["orchestration"].get("pattern") or pattern
                config = {**config, **(g["orchestration"].get("config") or {})}
                run["pack_graph_id"] = g.get("id")

        run["engine"] = "langgraph"
        run["orchestration_pattern"] = pattern
        run["graph_id"] = f"g_{workflow['id']}"
        tid = thread_id_for(run["organization_id"], run["id"])
        assert_thread_tenant(tid, run["organization_id"])
        run["graph_thread_id"] = tid
        run["graph_topology"] = build_topology(workflow)

        state = self._states.get(tid) or seed_state_from_run(run, workflow, pattern=pattern)
        state["status"] = "running"
        state["interrupt"] = None
        state["pattern"] = pattern
        if resume:
            cur = run.get("current_step") or state.get("current_step_id")
            if cur:
                self._ensure_step_approved(runtime, run, cur)

        def pipeline_fn(workflow: dict[str, Any] = workflow) -> None:
            run_pipeline_steps(
                runtime=runtime,
                run=run,
                workflow=workflow,
                state=state,
                actor_user_id=actor_user_id,
                gate_required=self._gate_required,
                fail_step=self._fail_step,
                ensure_approved=self._ensure_step_approved,
            )

        if pattern == "supervisor":
            run_supervisor(
                runtime=runtime,
                run=run,
                workflow=workflow,
                state=state,
                actor_user_id=actor_user_id,
                config=config,
                pipeline_fallback=lambda: pipeline_fn(workflow=workflow),
            )
        elif pattern == "router":
            run_router(
                runtime=runtime,
                run=run,
                workflow=workflow,
                state=state,
                actor_user_id=actor_user_id,
                config=config,
                pipeline_fn=pipeline_fn,
            )
        elif pattern == "critique":
            run_critique(
                runtime=runtime,
                run=run,
                workflow=workflow,
                state=state,
                actor_user_id=actor_user_id,
                config=config,
                pipeline_fn=pipeline_fn,
            )
        elif pattern == "map_reduce":
            run_map_reduce(
                runtime=runtime,
                run=run,
                workflow=workflow,
                state=state,
                actor_user_id=actor_user_id,
                config=config,
                pipeline_fn=pipeline_fn,
            )
        elif pattern == "pack_spine":
            run_pack_spine(
                runtime=runtime,
                run=run,
                workflow=workflow,
                state=state,
                actor_user_id=actor_user_id,
                config={**config, "domain_id": domain or "video"},
                pipeline_fn=pipeline_fn,
                load_pack_graph=load_pack_graph,
            )
        else:
            pipeline_fn(workflow=workflow)
            try:
                self._invoke_compiled_pipeline_skeleton(workflow, tid, state)
            except Exception:  # noqa: BLE001
                pass

        budget_err = enforce_budgets(state)
        if budget_err and run.get("status") not in {"waiting_for_approval"}:
            run["status"] = "failed"
            run["error"] = budget_err
            state["status"] = "failed"
            state["error"] = {"message": budget_err}

        # Trajectory score on terminal
        if run.get("status") in {"completed", "failed"}:
            events = [
                e
                for e in runtime.store.collection("stream_events")
                if e.get("workflow_run_id") == run["id"]
            ]
            traj = score_trajectory(run, events, state)
            run["trajectory"] = traj
            state.setdefault("metrics", {})["trajectory"] = traj

        self._states[tid] = state
        project_state_to_run(run, state)

    def _invoke_compiled_pipeline_skeleton(self, workflow: dict[str, Any], tid: str, state: dict[str, Any]) -> None:
        steps = [s.get("id") for s in (workflow.get("steps") or []) if s.get("id")]
        if not steps:
            return

        def make_node(sid: str):
            def _node(s: dict) -> dict:
                return {**s, "node_visits": int(s.get("node_visits") or 0) + 1, "current_step_id": sid}

            return _node

        try:
            from langgraph.graph import END, START, StateGraph

            builder = StateGraph(dict)
            for sid in steps:
                builder.add_node(sid, make_node(sid))
            builder.add_edge(START, steps[0])
            for i in range(len(steps) - 1):
                builder.add_edge(steps[i], steps[i + 1])
            builder.add_edge(steps[-1], END)
            graph = builder.compile(checkpointer=self._checkpointer)
            out = graph.invoke(
                {"node_visits": 0},
                {"configurable": {"thread_id": f"{tid}:skeleton"}},
            )
            if isinstance(out, dict):
                state.setdefault("metrics", {})["langgraph_skeleton_visits"] = out.get("node_visits")
        except Exception:  # noqa: BLE001
            g = build_pipeline_graph(steps, make_node)
            g.invoke({"node_visits": 0})

    def _ensure_step_approved(self, runtime: Any, run: dict[str, Any], step_id: str) -> None:
        run.setdefault("approved_steps", [])
        if step_id not in run["approved_steps"]:
            run["approved_steps"].append(step_id)

    def _gate_required(
        self,
        runtime: Any,
        run: dict[str, Any],
        workflow: dict[str, Any],
        step_definition: dict[str, Any],
        agent: dict[str, Any],
    ) -> bool:
        tool_lookup = runtime._tool_lookup(run["organization_id"])
        tool_gate_required = False
        for tool_id in step_definition.get("tools") or []:
            tool = tool_lookup.get(tool_id)
            if tool and runtime._tool_requires_approval(tool):
                tool_gate_required = True
        tier = runtime._tier_level(run.get("risk_tier") or workflow.get("risk_tier"))
        critical_action = (
            step_definition.get("irreversible")
            or step_definition.get("action_type") in {"irreversible_execution", "external_write"}
        )
        tier_requires_gate = (tier >= 4 and critical_action) or (
            tier == 2
            and step_definition.get("action_type")
            in {"notification", "irreversible_execution", "external_write", "send"}
        )
        sensitive = (
            step_definition.get("human_gate_required")
            or step_definition.get("irreversible")
            or step_definition.get("action_type") == "irreversible_execution"
            or tool_gate_required
            or tier_requires_gate
        )
        if not sensitive:
            return False
        if step_definition["id"] in (run.get("approved_steps") or []):
            return False
        return not runtime._is_step_approved(run["id"], step_definition["id"])

    def _fail_step(
        self,
        runtime: Any,
        run: dict[str, Any],
        state: dict[str, Any],
        step_record: dict[str, Any] | None,
        sid: str,
        err: str,
        actor_user_id: str,
    ) -> None:
        if step_record:
            step_record["status"] = "failed"
            step_record["error"] = err
        state["status"] = "failed"
        state["error"] = {"message": err, "step_id": sid}
        run["status"] = "failed"
        run["error"] = err
        runtime._emit_event("step.failed", run["id"], sid, err)
        runtime._append_audit(
            run["organization_id"],
            actor_user_id,
            "workflow_step",
            "workflow_step.failed",
            "workflow_run",
            run["id"],
            {"step_id": sid, "reason": err, "engine": "langgraph"},
            "failed",
        )
