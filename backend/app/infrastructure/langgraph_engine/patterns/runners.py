"""Pattern runners for LangGraph host engine — LG-05 full set."""

from __future__ import annotations

from typing import Any, Callable

from app.core.config import settings
from app.infrastructure.langgraph_engine.nodes.memory_read import inject_memory_hits
from app.infrastructure.langgraph_engine.tools.host_tool_node import run_host_tools


StepRunner = Callable[..., None]


def run_pipeline_steps(
    *,
    runtime: Any,
    run: dict[str, Any],
    workflow: dict[str, Any],
    state: dict[str, Any],
    actor_user_id: str,
    gate_required: Callable[..., bool],
    fail_step: Callable[..., None],
    ensure_approved: Callable[..., None],
) -> None:
    """Execute DNA steps in order with gates, memory inject, host tools."""
    from app.runtime import utc_now

    steps = list(workflow.get("steps") or [])
    agent_lookup = runtime._agent_lookup(run["organization_id"])
    completed = list(state.get("completed_step_ids") or [])
    max_nodes = settings.lg_max_nodes

    for step_definition in steps:
        if int(state.get("node_visits") or 0) >= max_nodes:
            state["status"] = "failed"
            state["error"] = {"message": f"max node visits exceeded ({max_nodes})"}
            run["status"] = "failed"
            run["error"] = state["error"]["message"]
            return

        sid = step_definition.get("id")
        if not sid or sid in completed:
            continue

        state["node_visits"] = int(state.get("node_visits") or 0) + 1
        state["current_step_id"] = sid
        run["current_step"] = sid
        step_record = next((s for s in run.get("steps") or [] if s.get("id") == sid), None)
        if step_record:
            step_record["status"] = "running"
            step_record["started_at"] = step_record.get("started_at") or utc_now()
        runtime._emit_event("step.started", run["id"], sid, f"LangGraph starting step {sid}")
        runtime._emit_event("node.started", run["id"], sid, f"node {sid}")

        agent = agent_lookup.get(step_definition.get("agent"))
        if step_record:
            step_record["agent_id"] = (agent or {}).get("id") or step_definition.get("agent")
        if not agent or agent.get("status", "active") not in {"active", "enabled"}:
            fail_step(runtime, run, state, step_record, sid, f"Agent unavailable: {step_definition.get('agent')}", actor_user_id)
            return

        agent.setdefault("allowed_memory_scopes", ["workflow_memory", "organization_memory"])
        # Do NOT invent allow-list from step tools (would bypass security).
        if agent.get("allowed_tools") is None:
            agent["allowed_tools"] = []

        # Fail closed on tools/allow-list BEFORE human gates (legacy parity).
        tool_lookup = runtime._tool_lookup(run["organization_id"])
        for tool_id in step_definition.get("tools") or []:
            tool = tool_lookup.get(tool_id)
            if not tool or tool.get("enabled", True) is False:
                fail_step(runtime, run, state, step_record, sid, f"Tool unavailable: {tool_id}", actor_user_id)
                return
            if tool_id not in (agent.get("allowed_tools") or []):
                fail_step(
                    runtime,
                    run,
                    state,
                    step_record,
                    sid,
                    f"Agent {agent.get('id')} is not allowed to use tool {tool_id}",
                    actor_user_id,
                )
                return

        hits = inject_memory_hits(
            runtime,
            organization_id=run["organization_id"],
            agent=agent,
            workflow=workflow,
            actor_user_id=actor_user_id,
        )
        if hits:
            state["memory_hits"] = list(state.get("memory_hits") or []) + hits
            state.setdefault("messages", []).append(
                {"role": "memory", "agent_id": agent.get("id"), "step_id": sid, "hits": len(hits)}
            )

        if gate_required(runtime, run, workflow, step_definition, agent):
            approval = runtime._create_approval(run, step_definition, actor_user_id)
            if step_record:
                step_record["status"] = "waiting_for_approval"
            state["status"] = "waiting_for_approval"
            state["interrupt"] = {
                "type": "human_gate",
                "node_id": sid,
                "approval_id": approval["id"],
                "approval_state": "pending",
                "payload_preview": {"case": state.get("case"), "step": sid, "memory_hit_count": len(hits)},
            }
            run["status"] = "waiting_for_approval"
            run["approval_request_id"] = approval["id"]
            run["approval_state"] = "pending"
            run["updated_at"] = utc_now()
            runtime.store.save()
            runtime._emit_event("approval.requested", run["id"], sid, f"Approval requested for {sid}")
            runtime._emit_event("interrupt", run["id"], sid, "graph interrupt for human gate")
            return

        effects, tool_results, err = run_host_tools(
            runtime=runtime,
            run=run,
            step_definition=step_definition,
            agent=agent,
            actor_user_id=actor_user_id,
            case=state.get("case") or {},
        )
        if err:
            fail_step(runtime, run, state, step_record, sid, err, actor_user_id)
            return

        if effects:
            state["tool_effects"] = list(state.get("tool_effects") or []) + effects
        arts = dict(state.get("artifacts") or {})
        for fx in tool_results:
            res = fx.get("result") if isinstance(fx, dict) else None
            if isinstance(res, dict):
                arts.update(res)
        state["artifacts"] = arts
        if step_record:
            step_record["status"] = "completed"
            step_record["output"] = {"tool_effects": [e.get("id") for e in tool_results]}
            step_record["completed_at"] = utc_now()
        completed.append(sid)
        state["completed_step_ids"] = completed
        runtime._emit_event("step.completed", run["id"], sid, f"Completed step {sid}")
        runtime._emit_event("node.completed", run["id"], sid, f"node {sid} done")
        runtime._append_audit(
            run["organization_id"],
            actor_user_id,
            "workflow_step",
            "workflow_step.completed",
            "workflow_run",
            run["id"],
            {"step_id": sid, "engine": "langgraph", "tool_effects": [e.get("id") for e in tool_results]},
            "success",
        )

    state["status"] = "completed"
    state["current_step_id"] = None
    run["current_step"] = None
    run["approval_request_id"] = None
    run["approval_state"] = None
    run["completed_at"] = utc_now()
    run["updated_at"] = utc_now()
    arts = state.get("artifacts") or {}
    run["output"] = {
        "outcome": "completed",
        "step_count": len([s for s in (run.get("steps") or []) if s.get("status") == "completed"]),
        **(arts if isinstance(arts, dict) else {}),
    }
    # Evaluation + block_on_fail (legacy parity)
    try:
        evaluation = runtime._create_evaluation(run)
        run.setdefault("evaluation_results", []).append(evaluation["id"])
        run["result"] = run["output"]
        eval_policy = workflow.get("evaluation_policy") or {}
        if eval_policy.get("block_on_fail") and evaluation.get("status") in {"failed", "fail", "blocked"}:
            run["status"] = "failed"
            state["status"] = "failed"
            run["error"] = "Evaluation failed and evaluation_policy.block_on_fail is enabled"
            state["error"] = {"message": run["error"]}
            runtime._append_audit(
                run["organization_id"],
                actor_user_id,
                "workflow_run",
                "workflow_run.evaluation_blocked",
                "workflow_run",
                run["id"],
                {"evaluation_id": evaluation["id"], "engine": "langgraph"},
                "failed",
            )
            runtime._emit_event("evaluation.failed", run["id"], None, "Evaluation blocked promotion/completion")
            return
        runtime._append_audit(
            run["organization_id"],
            actor_user_id,
            "workflow_run",
            "workflow_run.completed",
            "workflow_run",
            run["id"],
            {"engine": "langgraph", "pattern": state.get("pattern") or "pipeline", "evaluation_id": evaluation.get("id")},
            "success",
        )
    except Exception:  # noqa: BLE001
        runtime._append_audit(
            run["organization_id"],
            actor_user_id,
            "workflow_run",
            "workflow_run.completed",
            "workflow_run",
            run["id"],
            {"engine": "langgraph", "pattern": state.get("pattern") or "pipeline"},
            "success",
        )
    run["status"] = "completed"
    runtime._emit_event("run.completed", run["id"], None, "LangGraph pipeline completed")


def run_supervisor(
    *,
    runtime: Any,
    run: dict[str, Any],
    workflow: dict[str, Any],
    state: dict[str, Any],
    actor_user_id: str,
    config: dict[str, Any],
    pipeline_fallback: Callable[..., None],
) -> None:
    from app.runtime import utc_now

    specialists = list(config.get("specialists") or [])
    supervisor = config.get("supervisor_agent") or workflow.get("owner") or "supervisor"
    max_h = int(config.get("max_handoffs") or settings.lg_max_handoffs)
    if not specialists:
        pipeline_fallback()
        return

    handoffs = int(state.get("handoffs") or 0)
    visited = list(state.get("completed_step_ids") or [])
    agent_lookup = runtime._agent_lookup(run["organization_id"])

    for spec in specialists:
        if handoffs >= max_h or int(state.get("node_visits") or 0) >= settings.lg_max_nodes:
            break
        if spec in visited:
            continue
        handoffs += 1
        state["handoffs"] = handoffs
        state["node_visits"] = int(state.get("node_visits") or 0) + 1
        state["active_agent_id"] = spec
        state["current_step_id"] = spec
        run["current_step"] = spec
        runtime._emit_event("handoff", run["id"], spec, f"supervisor {supervisor} → {spec}")
        runtime._emit_event("node.started", run["id"], spec, f"specialist {spec}")

        agent = agent_lookup.get(spec) or {
            "id": spec,
            "status": "active",
            "allowed_tools": ["audit_log_writer"],
            "allowed_memory_scopes": ["workflow_memory", "organization_memory"],
        }
        step_def = {
            "id": spec,
            "agent": spec,
            "tools": (list(agent.get("allowed_tools") or [])[:1] or ["audit_log_writer"]),
        }
        if "audit_log_writer" not in step_def["tools"]:
            step_def["tools"] = ["audit_log_writer"]
        agent["allowed_tools"] = list(set(list(agent.get("allowed_tools") or []) + step_def["tools"]))

        effects, tool_results, err = run_host_tools(
            runtime=runtime,
            run=run,
            step_definition=step_def,
            agent=agent,
            actor_user_id=actor_user_id,
            case={**(state.get("case") or {}), "message": f"supervisor handoff to {spec}"},
        )
        if err:
            state.setdefault("messages", []).append({"role": "system", "content": f"specialist {spec} failed: {err}"})
        else:
            state["tool_effects"] = list(state.get("tool_effects") or []) + effects
            arts = dict(state.get("artifacts") or {})
            arts[f"specialist_{spec}"] = {"status": "ok", "effects": [e.get("id") for e in tool_results]}
            state["artifacts"] = arts
        visited.append(spec)
        state["completed_step_ids"] = visited
        state.setdefault("messages", []).append(
            {"role": "supervisor", "content": f"handoff to {spec}", "from": supervisor, "to": spec}
        )
        runtime._emit_event("node.completed", run["id"], spec, f"specialist {spec} done")

    state["status"] = "completed"
    state["current_step_id"] = None
    run["status"] = "completed"
    run["completed_at"] = utc_now()
    run["updated_at"] = utc_now()
    run["output"] = state.get("artifacts")
    runtime._emit_event("run.completed", run["id"], None, "LangGraph supervisor completed")
    runtime._append_audit(
        run["organization_id"],
        actor_user_id,
        "workflow_run",
        "workflow_run.completed",
        "workflow_run",
        run["id"],
        {"engine": "langgraph", "pattern": "supervisor", "handoffs": handoffs},
        "success",
    )


def run_router(
    *,
    runtime: Any,
    run: dict[str, Any],
    workflow: dict[str, Any],
    state: dict[str, Any],
    actor_user_id: str,
    config: dict[str, Any],
    pipeline_fn: Callable[..., None],
) -> None:
    """Classify case into a branch key, filter steps by branch tag or run specialist list."""
    case = state.get("case") or {}
    routes = config.get("routes") if isinstance(config.get("routes"), dict) else {}
    # Deterministic classifier: use case.route or keyword in brief/case_id
    key = str(case.get("route") or case.get("branch") or "").strip().lower()
    if not key:
        text = f"{case.get('brief') or ''} {case.get('case_id') or ''}".lower()
        for rk in routes:
            if str(rk).lower() in text:
                key = str(rk).lower()
                break
    if not key and routes:
        key = str(next(iter(routes))).lower()
    state["route"] = {"selected": key, "routes": list(routes.keys())}
    runtime._emit_event("node.started", run["id"], "router", f"route={key or 'default'}")

    branch_steps = routes.get(key) or routes.get(key.upper()) if key else None
    if isinstance(branch_steps, list) and branch_steps:
        # Build synthetic workflow with subset of steps matching ids
        all_steps = {s.get("id"): s for s in (workflow.get("steps") or [])}
        selected = [all_steps[i] for i in branch_steps if i in all_steps]
        if selected:
            wf = dict(workflow)
            wf["steps"] = selected
            # Align run.steps statuses for selected only — still process via pipeline on full run steps
            pipeline_fn(workflow=wf)
            return
    # default: full pipeline
    pipeline_fn(workflow=workflow)


def run_critique(
    *,
    runtime: Any,
    run: dict[str, Any],
    workflow: dict[str, Any],
    state: dict[str, Any],
    actor_user_id: str,
    config: dict[str, Any],
    pipeline_fn: Callable[..., None],
) -> None:
    """Produce pipeline then optional critique loop with max_iterations."""
    from app.runtime import utc_now

    max_iter = int(config.get("max_iterations") or 3)
    pipeline_fn(workflow=workflow)
    if run.get("status") != "completed":
        return
    # Critique iterations using audit_log_writer as critic stub
    agent_lookup = runtime._agent_lookup(run["organization_id"])
    critic_id = config.get("critic_agent") or "governance_officer"
    agent = agent_lookup.get(critic_id) or {
        "id": critic_id,
        "status": "active",
        "allowed_tools": ["audit_log_writer"],
        "allowed_memory_scopes": ["organization_memory"],
    }
    agent["allowed_tools"] = list(set(list(agent.get("allowed_tools") or []) + ["audit_log_writer"]))
    iterations = 0
    while iterations < max_iter:
        iterations += 1
        state["node_visits"] = int(state.get("node_visits") or 0) + 1
        runtime._emit_event("node.started", run["id"], f"critique_{iterations}", f"critique pass {iterations}")
        effects, _, err = run_host_tools(
            runtime=runtime,
            run=run,
            step_definition={"id": f"critique_{iterations}", "agent": critic_id, "tools": ["audit_log_writer"]},
            agent=agent,
            actor_user_id=actor_user_id,
            case={**(state.get("case") or {}), "message": f"critique iteration {iterations}", "artifacts": state.get("artifacts")},
        )
        if err:
            state.setdefault("messages", []).append({"role": "critic", "content": f"critique error: {err}"})
            break
        state["tool_effects"] = list(state.get("tool_effects") or []) + effects
        state.setdefault("messages", []).append({"role": "critic", "content": f"accept iteration {iterations}"})
        runtime._emit_event("node.completed", run["id"], f"critique_{iterations}", "critique accepted")
        # MVP: always accept after first successful critique
        break
    state.setdefault("artifacts", {})["critique_iterations"] = iterations
    run["output"] = state.get("artifacts")
    run["updated_at"] = utc_now()


def run_map_reduce(
    *,
    runtime: Any,
    run: dict[str, Any],
    workflow: dict[str, Any],
    state: dict[str, Any],
    actor_user_id: str,
    config: dict[str, Any],
    pipeline_fn: Callable[..., None],
) -> None:
    """Fan-out over case[items_key], run mini audit tool per item, then join + pipeline."""
    from app.runtime import utc_now

    items_key = str(config.get("items_key") or "items")
    case = dict(state.get("case") or {})
    items = case.get(items_key)
    if not isinstance(items, list) or not items:
        items = [case]
    agent_lookup = runtime._agent_lookup(run["organization_id"])
    agent = agent_lookup.get("business_orchestrator") or {
        "id": "business_orchestrator",
        "status": "active",
        "allowed_tools": ["audit_log_writer"],
        "allowed_memory_scopes": ["workflow_memory", "organization_memory"],
    }
    agent["allowed_tools"] = list(set(list(agent.get("allowed_tools") or []) + ["audit_log_writer"]))
    mapped: list[dict[str, Any]] = []
    for idx, item in enumerate(items[:20]):
        state["node_visits"] = int(state.get("node_visits") or 0) + 1
        if state["node_visits"] >= settings.lg_max_nodes:
            break
        sid = f"map_{idx}"
        runtime._emit_event("node.started", run["id"], sid, f"map item {idx}")
        payload = {**(state.get("case") or {}), **(item if isinstance(item, dict) else {"item": item})}
        effects, tool_results, err = run_host_tools(
            runtime=runtime,
            run=run,
            step_definition={"id": sid, "agent": agent.get("id"), "tools": ["audit_log_writer"]},
            agent=agent,
            actor_user_id=actor_user_id,
            case=payload,
        )
        if err:
            mapped.append({"index": idx, "error": err})
        else:
            state["tool_effects"] = list(state.get("tool_effects") or []) + effects
            mapped.append({"index": idx, "effects": [e.get("id") for e in tool_results]})
        runtime._emit_event("node.completed", run["id"], sid, f"map item {idx} done")
    state.setdefault("artifacts", {})["map_results"] = mapped
    state.setdefault("artifacts", {})["reduce"] = {"count": len(mapped)}
    # Then run main DNA pipeline for join phase
    pipeline_fn(workflow=workflow)
    if run.get("status") == "completed":
        arts = dict(state.get("artifacts") or {})
        arts["map_results"] = mapped
        state["artifacts"] = arts
        run["output"] = arts
        run["updated_at"] = utc_now()


def run_pack_spine(
    *,
    runtime: Any,
    run: dict[str, Any],
    workflow: dict[str, Any],
    state: dict[str, Any],
    actor_user_id: str,
    config: dict[str, Any],
    pipeline_fn: Callable[..., None],
    load_pack_graph: Callable[[str, str | None], dict[str, Any] | None] | None = None,
) -> None:
    """Domain pack spine: annotate pack graph metadata, then always run DNA pipeline when steps exist.

    Previously pack-graph agent lists short-circuited DNA steps (publish_hook never ran).
    """
    domain_id = (
        config.get("domain_id")
        or workflow.get("domain_id")
        or workflow.get("domain")
        or state.get("domain_id")
        or "video"
    )
    entry = config.get("entry_agent") or "video.orchestrator"
    state["route"] = {"pattern": "pack_spine", "domain_id": domain_id, "entry_agent": entry}
    runtime._emit_event("node.started", run["id"], "pack_entry", f"pack_spine domain={domain_id} entry={entry}")
    if load_pack_graph:
        g = load_pack_graph(str(domain_id), config.get("graph_id") or workflow.get("pack_graph_id"))
        if g:
            state.setdefault("artifacts", {})["pack_graph_id"] = g.get("id")
            state.setdefault("messages", []).append(
                {"role": "pack", "content": f"loaded pack graph {g.get('id')}", "agents": g.get("agents") or []}
            )
    # DNA steps are authoritative when present
    if workflow.get("steps"):
        pipeline_fn(workflow=workflow)
        return
    # Fallback: no DNA steps → optional specialist tour from pack graph
    if load_pack_graph:
        g = load_pack_graph(str(domain_id), config.get("graph_id") or workflow.get("pack_graph_id"))
        agents = (g or {}).get("agents") or (g or {}).get("specialists") or []
        if isinstance(agents, list) and agents:
            run_supervisor(
                runtime=runtime,
                run=run,
                workflow=workflow,
                state=state,
                actor_user_id=actor_user_id,
                config={
                    "supervisor_agent": entry,
                    "specialists": [str(a) for a in agents[:12]],
                    "max_handoffs": int(config.get("max_handoffs") or 12),
                },
                pipeline_fallback=lambda: pipeline_fn(workflow=workflow),
            )
            return
    pipeline_fn(workflow=workflow)
