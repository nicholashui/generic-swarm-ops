from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime

router = APIRouter()


@router.post("/run")
def start_loop(payload: dict, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.start_improvement_loop(current_user, payload)


@router.get("")
def list_loops(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    return runtime.list_loop_runs(current_user)


@router.get("/{loop_id}")
def get_loop(loop_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.get_loop_run(current_user, loop_id)
