from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.services.audit_service import get_audit_log, list_audit_logs

router = APIRouter()


@router.get("")
def audit_logs_route(
    action: str | None = None,
    resource_type: str | None = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> list[dict]:
    runtime.assert_permission(current_user, "audit:read")
    return list_audit_logs(current_user, action=action, resource_type=resource_type)


@router.get("/{audit_id}")
def audit_log_detail_route(audit_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "audit:read")
    return get_audit_log(current_user, audit_id)
