from fastapi import APIRouter, Depends, Header

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.rate_limit import build_rate_limit_dependency
from app.runtime import AuthenticatedUser
from app.schemas.common import ApiKeyCreateRequest, LoginRequest, PasswordResetRequest, RefreshRequest
from app.services.auth_service import create_api_key, list_api_keys, login, logout, refresh, reset_password, revoke_api_key

router = APIRouter()
auth_rate_limit = build_rate_limit_dependency(settings.auth_rate_limit_per_minute, 60, "auth") if settings.rate_limit_enabled else None
management_rate_limit = build_rate_limit_dependency(max(settings.auth_rate_limit_per_minute // 2, 1), 60, "auth-management") if settings.rate_limit_enabled else None


@router.post("/login", dependencies=[Depends(auth_rate_limit)] if auth_rate_limit else [])
def login_route(payload: LoginRequest) -> dict:
    return login(payload.email, payload.password)


@router.post("/refresh", dependencies=[Depends(auth_rate_limit)] if auth_rate_limit else [])
def refresh_route(payload: RefreshRequest) -> dict:
    return refresh(payload.refresh_token)


@router.post("/logout")
def logout_route(authorization: str | None = Header(default=None)) -> dict:
    token = authorization.split(" ", 1)[1] if authorization and authorization.startswith("Bearer ") else None
    return logout(token)


@router.get("/me")
def me_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return {
        "id": current_user.id,
        "organization_id": current_user.organization_id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
    }


@router.get("/api-keys")
def api_keys_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    return list_api_keys(current_user)


@router.post("/api-keys", dependencies=[Depends(management_rate_limit)] if management_rate_limit else [])
def create_api_key_route(payload: ApiKeyCreateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return create_api_key(current_user, payload.name)


@router.delete("/api-keys/{key_id}", dependencies=[Depends(management_rate_limit)] if management_rate_limit else [])
def revoke_api_key_route(key_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return revoke_api_key(current_user, key_id)


@router.post("/reset-password", dependencies=[Depends(auth_rate_limit)] if auth_rate_limit else [])
def reset_password_route(
    payload: PasswordResetRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    """Authenticated password reset only (self or org admin)."""
    return reset_password(payload.email, payload.new_password, acting_user=current_user)
