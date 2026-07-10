from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.schemas.common import ApprovalDecisionRequest, ApprovalReassignRequest
from app.services.approval_service import decide, get_approval, list_approvals, reassign

router = APIRouter()


@router.get("")
def approvals_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "approvals:read")
    return list_approvals(current_user)


@router.get("/{approval_id}")
def approval_detail_route(approval_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "approvals:read")
    return get_approval(current_user, approval_id)


@router.post("/{approval_id}/approve")
def approval_approve_route(approval_id: str, payload: ApprovalDecisionRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return decide(approval_id, "approved", payload.reason, current_user)


@router.post("/{approval_id}/reject")
def approval_reject_route(approval_id: str, payload: ApprovalDecisionRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return decide(approval_id, "rejected", payload.reason, current_user)


@router.post("/{approval_id}/reassign")
def approval_reassign_route(approval_id: str, payload: ApprovalReassignRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return reassign(approval_id, payload.reviewer_user_id, current_user)


@router.post("/{approval_id}/decision")
def approval_decision_route(approval_id: str, payload: ApprovalDecisionRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return decide(approval_id, payload.decision, payload.reason, current_user)
