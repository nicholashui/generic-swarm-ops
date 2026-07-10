from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.schemas.common import StatusUpdateRequest, ToolCreateRequest
from app.services.tool_service import archive_tool, create_tool, get_tool, list_tools, update_tool_status

router = APIRouter()


@router.get("")
def tools_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "tools:read")
    return list_tools(current_user)


@router.post("")
def create_tool_route(payload: ToolCreateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return create_tool(current_user, payload.model_dump())


@router.get("/{tool_id}")
def tool_detail_route(tool_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "tools:read")
    return get_tool(current_user, tool_id)


@router.patch("/{tool_id}")
def update_tool_route(tool_id: str, payload: StatusUpdateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return update_tool_status(current_user, tool_id, True if payload.enabled is None else payload.enabled)


@router.delete("/{tool_id}")
def archive_tool_route(tool_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return archive_tool(current_user, tool_id)
