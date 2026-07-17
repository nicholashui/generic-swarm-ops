from __future__ import annotations

import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.rate_limit import build_rate_limit_dependency
from app.runtime import AuthenticatedUser, runtime
from app.services.audit_service import stream_run_events
from app.services.evaluation_service import list_run_evaluations
from app.schemas.common import RunExpireRequest
from app.services.workflow_run_service import (
    cancel_run,
    dispatch_runs,
    expire_run,
    get_run,
    get_run_steps,
    list_runs,
    pause_run,
    resume_run,
    retry_run,
)

router = APIRouter()
workflow_write_rate_limit = build_rate_limit_dependency(settings.workflow_write_rate_limit_per_minute, 60, "workflow-run-write") if settings.rate_limit_enabled else None


@router.get("")
def workflow_runs_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "workflow_runs:read")
    return list_runs(current_user)


@router.get("/{run_id}")
def workflow_run_detail_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "workflow_runs:read")
    return get_run(current_user, run_id)


@router.get("/{run_id}/steps")
def workflow_run_steps_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "workflow_runs:read")
    return get_run_steps(current_user, run_id)


@router.get("/{run_id}/graph-state")
def workflow_run_graph_state_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    """Redacted HostGraphState projection for a run (LG-11)."""
    runtime.assert_permission(current_user, "workflow_runs:read")
    run = get_run(current_user, run_id)
    # Prefer live engine memory if langgraph
    state: dict = {
        "run_id": run.get("id"),
        "workflow_id": run.get("workflow_id"),
        "engine": run.get("engine") or "legacy",
        "status": run.get("status"),
        "current_step_id": run.get("current_step"),
        "pattern": run.get("orchestration_pattern"),
        "graph_thread_id": run.get("graph_thread_id"),
        "graph_id": run.get("graph_id"),
        "artifacts": run.get("output") if isinstance(run.get("output"), dict) else {},
        "metrics": run.get("graph_metrics") or {},
        "interrupt": {
            "approval_id": run.get("approval_request_id"),
            "approval_state": run.get("approval_state"),
            "node_id": run.get("current_step"),
        }
        if run.get("status") == "waiting_for_approval"
        else None,
        "completed_step_ids": [s.get("id") for s in (run.get("steps") or []) if s.get("status") == "completed"],
        "steps": [
            {"id": s.get("id"), "status": s.get("status"), "agent_id": s.get("agent_id")}
            for s in (run.get("steps") or [])
        ],
    }
    try:
        from app.infrastructure.orchestration.registry import get_engine

        if (run.get("engine") or "") == "langgraph":
            eng = get_engine("langgraph")
            tid = run.get("graph_thread_id")
            if tid and hasattr(eng, "_states") and tid in eng._states:
                from app.infrastructure.langgraph_engine.security import redact_state

                live = redact_state(dict(eng._states[tid]))
                state["live"] = {
                    k: live[k]
                    for k in (
                        "status",
                        "current_step_id",
                        "completed_step_ids",
                        "artifacts",
                        "messages",
                        "handoffs",
                        "node_visits",
                        "pattern",
                        "interrupt",
                        "metrics",
                        "memory_hits",
                        "tool_effects",
                    )
                    if k in live
                }
                if run.get("trajectory"):
                    state["trajectory"] = run["trajectory"]
    except Exception:  # noqa: BLE001
        pass
    return state


@router.get("/{run_id}/evaluations")
def workflow_run_evaluations_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "evaluations:read")
    return list_run_evaluations(current_user, run_id)


@router.post("/dispatch", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def workflow_run_dispatch_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    return dispatch_runs(current_user)


@router.post("/{run_id}/cancel", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def workflow_run_cancel_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return cancel_run(current_user, run_id)


@router.post("/{run_id}/pause", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def workflow_run_pause_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return pause_run(current_user, run_id)


@router.post("/{run_id}/resume", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def workflow_run_resume_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return resume_run(current_user, run_id)


@router.post("/{run_id}/expire", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def workflow_run_expire_route(
    run_id: str,
    payload: RunExpireRequest | None = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    reason = payload.reason if payload else None
    return expire_run(current_user, run_id, reason=reason)


@router.post("/{run_id}/retry", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def workflow_run_retry_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return retry_run(current_user, run_id)


@router.get("/{run_id}/stream")
def workflow_run_stream_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> StreamingResponse:
    runtime.assert_permission(current_user, "workflow_runs:read")
    events = stream_run_events(current_user, run_id)
    from app.infrastructure.langgraph_engine.streaming import normalize_event

    def iter_events():
        for event in events:
            yield f"data: {json.dumps(normalize_event(event))}\n\n"

    return StreamingResponse(iter_events(), media_type="text/event-stream")


@router.get("/{run_id}/trajectory")
def workflow_run_trajectory_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    """LG-15 trajectory score for a completed or in-flight graph run."""
    runtime.assert_permission(current_user, "workflow_runs:read")
    run = get_run(current_user, run_id)
    if run.get("trajectory"):
        return {"run_id": run_id, "trajectory": run["trajectory"]}
    from app.infrastructure.langgraph_engine.trajectory import score_trajectory
    from app.services.audit_service import stream_run_events as _events

    events = _events(current_user, run_id)
    state = {"pattern": run.get("orchestration_pattern")}
    return {"run_id": run_id, "trajectory": score_trajectory(run, events, state)}
