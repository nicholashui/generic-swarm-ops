from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.schemas.common import MemoryCreateRequest, MemorySearchRequest, MemoryUpdateRequest
from app.services.memory_service import create, delete, get, search, update

router = APIRouter()


@router.get("")
def memory_route(
    query: str | None = Query(default=None),
    scope: str | None = Query(default=None),
    acting_agent_id: str | None = Query(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> list[dict]:
    runtime.assert_permission(current_user, "memory:read")
    return search(current_user, query=query, scope=scope, acting_agent_id=acting_agent_id)


@router.post("")
def create_memory_route(payload: MemoryCreateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return create(current_user, payload.model_dump())


@router.get("/{memory_id}")
def memory_detail_route(memory_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "memory:read")
    return get(current_user, memory_id)


@router.patch("/{memory_id}")
def update_memory_route(memory_id: str, payload: MemoryUpdateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return update(current_user, memory_id, payload.model_dump(exclude_unset=True))


@router.delete("/{memory_id}")
def delete_memory_route(memory_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return delete(current_user, memory_id)


@router.post("/search")
def memory_search_route(payload: MemorySearchRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "memory:read")
    acting = getattr(payload, "acting_agent_id", None)
    return search(current_user, query=payload.query, scope=payload.scope, acting_agent_id=acting)
