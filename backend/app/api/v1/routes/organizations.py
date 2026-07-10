from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.schemas.common import OrganizationUpdateRequest
from app.services.organization_service import get_organization, list_organizations, update_organization

router = APIRouter()


@router.get("")
def organizations_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "organizations:read")
    return list_organizations(current_user)


@router.get("/{organization_id}")
def get_organization_route(organization_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return get_organization(current_user, organization_id)


@router.patch("/{organization_id}")
def update_organization_route(
    organization_id: str,
    payload: OrganizationUpdateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    return update_organization(current_user, organization_id, data)
