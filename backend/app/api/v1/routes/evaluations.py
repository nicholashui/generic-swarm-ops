from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.schemas.common import EvaluationRunRequest
from app.services.evaluation_service import get_evaluation, list_evaluations, list_run_evaluations, run_evaluation

router = APIRouter()


@router.get("")
def evaluations_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "evaluations:read")
    return list_evaluations(current_user)


@router.get("/{evaluation_id}")
def evaluation_detail_route(evaluation_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "evaluations:read")
    return get_evaluation(current_user, evaluation_id)


@router.post("/run")
def run_evaluation_route(payload: EvaluationRunRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return run_evaluation(current_user, payload.run_id)


@router.get("/workflow-runs/{run_id}")
def workflow_run_evaluations_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "evaluations:read")
    return list_run_evaluations(current_user, run_id)
