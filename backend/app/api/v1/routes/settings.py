from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime

router = APIRouter()


@router.get("")
def settings_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "settings:read")
    return runtime.settings()
