from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.schemas.common import (
    InvitationAcceptRequest,
    InvitationCreateRequest,
    UserCreateRequest,
    UserUpdateRequest,
)
from app.services.user_service import (
    accept_invitation,
    create_invitation,
    create_user,
    get_user,
    list_invitations,
    list_users,
    update_user,
)

router = APIRouter()


@router.get("")
def users_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "users:read")
    return list_users(current_user)


@router.post("")
def create_user_route(payload: UserCreateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return create_user(current_user, payload.model_dump())


@router.get("/invitations")
def list_invitations_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    return list_invitations(current_user)


@router.post("/invitations")
def create_invitation_route(
    payload: InvitationCreateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    return create_invitation(current_user, payload.model_dump())


@router.post("/invitations/accept")
def accept_invitation_route(payload: InvitationAcceptRequest) -> dict:
    """Public: accept invite token and set password (no bearer required)."""
    return accept_invitation(payload.model_dump())


@router.get("/{user_id}")
def get_user_route(user_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return get_user(current_user, user_id)


@router.patch("/{user_id}")
def update_user_route(
    user_id: str,
    payload: UserUpdateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    return update_user(current_user, user_id, data)
