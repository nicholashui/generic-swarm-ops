from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime

router = APIRouter()


@router.post("/reflect/{run_id}")
def reflect_run(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.reflect_on_workflow_run(current_user, run_id)


@router.post("/reflect/agent/{agent_id}")
def reflect_agent(
    agent_id: str,
    payload: dict | None = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    body = payload or {}
    return runtime.reflect_on_agent(current_user, agent_id, run_id=body.get("run_id"))


@router.get("/lessons")
def list_lessons(
    workflow_id: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> list[dict]:
    return runtime.list_improvement_lessons(
        current_user, workflow_id=workflow_id, agent_id=agent_id, limit=limit
    )


@router.get("/metrics")
def improvement_metrics(
    agent_id: str | None = Query(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    return runtime.improvement_metrics(current_user, agent_id=agent_id)


@router.get("/lesson-utility")
def lesson_utility_dashboard(
    agent_id: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=200),
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    """Ranked lesson utility dashboard (Wave 3)."""
    return runtime.lesson_utility_dashboard(current_user, agent_id=agent_id, limit=limit)


@router.post("/auto-propose")
def auto_propose(payload: dict, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.auto_propose_from_failures(
        current_user,
        workflow_id=payload.get("workflow_id") or "",
        run_id=payload.get("run_id"),
    )


@router.post("/skills/propose")
def propose_skill(payload: dict, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.propose_skill_sandbox(current_user, payload)


@router.get("/skills")
def list_skills(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    return runtime.list_skill_proposals(current_user)


@router.post("/skills/{proposal_id}/promote")
def promote_skill(proposal_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.promote_skill_sandbox(current_user, proposal_id)
