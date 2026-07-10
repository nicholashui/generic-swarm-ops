from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.schemas.common import AgentCreateRequest, StatusUpdateRequest
from app.services.agent_service import agent_activity, agent_tools, archive_agent, create_agent, get_agent, list_agents, update_agent_status

router = APIRouter()


@router.get("")
def agents_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "agents:read")
    return list_agents(current_user)


@router.post("")
def create_agent_route(payload: AgentCreateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return create_agent(current_user, payload.model_dump())


@router.get("/{agent_id}")
def agent_detail_route(agent_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "agents:read")
    return get_agent(current_user, agent_id)


@router.patch("/{agent_id}")
def update_agent_route(agent_id: str, payload: StatusUpdateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return update_agent_status(current_user, agent_id, payload.status or "draft")


@router.delete("/{agent_id}")
def archive_agent_route(agent_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return archive_agent(current_user, agent_id)


@router.get("/{agent_id}/activity")
def agent_activity_route(agent_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "agents:read")
    return agent_activity(current_user, agent_id)


@router.get("/{agent_id}/tools")
def agent_tools_route(agent_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "agents:read")
    return agent_tools(current_user, agent_id)
