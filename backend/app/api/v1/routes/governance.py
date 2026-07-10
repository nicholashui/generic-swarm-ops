from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.schemas.common import GovernanceCheckRequest, GovernancePolicyRequest
from app.services.governance_service import archive_policy, check, create_policy, get_policy, list_policies, preview, update_policy

router = APIRouter()


@router.get("/preview")
def governance_preview_route(workflow_id: str = Query(...), current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "governance:read")
    return preview(workflow_id, current_user)


@router.get("/policies")
def governance_policies_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "governance:read")
    return list_policies(current_user)


@router.post("/policies")
def create_governance_policy_route(payload: GovernancePolicyRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return create_policy(current_user, payload.model_dump(exclude_unset=True))


@router.get("/policies/{policy_id}")
def governance_policy_detail_route(policy_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "governance:read")
    return get_policy(current_user, policy_id)


@router.patch("/policies/{policy_id}")
def update_governance_policy_route(policy_id: str, payload: GovernancePolicyRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return update_policy(current_user, policy_id, payload.model_dump(exclude_unset=True))


@router.delete("/policies/{policy_id}")
def archive_governance_policy_route(policy_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return archive_policy(current_user, policy_id)


@router.post("/check")
def governance_check_route(payload: GovernanceCheckRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return check(current_user, payload.model_dump(exclude_unset=True))
