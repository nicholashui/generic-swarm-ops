from fastapi import APIRouter, Depends, Header

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.rate_limit import build_rate_limit_dependency
from app.runtime import AuthenticatedUser, runtime
from app.schemas.common import WorkflowCreateRequest, WorkflowStartRequest, WorkflowUpdateRequest, WorkflowVersionCreateRequest
from app.services.workflow_run_service import start_run
from app.services.workflow_service import activate_workflow_version, add_workflow_version, archive_workflow, create_workflow, disable_workflow, get_workflow, list_workflow_versions, list_workflows, update_workflow

router = APIRouter()
workflow_write_rate_limit = build_rate_limit_dependency(settings.workflow_write_rate_limit_per_minute, 60, "workflow-write") if settings.rate_limit_enabled else None


@router.get("")
def workflows_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "workflows:read")
    return list_workflows(current_user)


@router.get("/{workflow_id}")
def workflow_detail_route(workflow_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "workflows:read")
    return get_workflow(current_user, workflow_id)


@router.get("/{workflow_id}/topology")
def workflow_topology_route(workflow_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    """LangGraph / DNA topology for FE graph canvas (LG-11)."""
    runtime.assert_permission(current_user, "workflows:read")
    workflow = get_workflow(current_user, workflow_id)
    from app.infrastructure.langgraph_engine.compiler import build_topology

    return build_topology(workflow)


@router.post("", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def create_workflow_route(payload: WorkflowCreateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return create_workflow(current_user, payload.model_dump())


@router.patch("/{workflow_id}", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def update_workflow_route(workflow_id: str, payload: WorkflowUpdateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    data = payload.model_dump(exclude_unset=True)
    # Avoid wiping steps when client only patches orchestration
    if "steps" in data and not data["steps"]:
        data.pop("steps")
    return update_workflow(current_user, workflow_id, data)


@router.post("/{workflow_id}/versions", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def create_workflow_version_route(workflow_id: str, payload: WorkflowVersionCreateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return add_workflow_version(current_user, workflow_id, payload.model_dump())


@router.get("/{workflow_id}/versions")
def workflow_versions_route(workflow_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "workflows:read")
    return list_workflow_versions(current_user, workflow_id)


@router.post("/{workflow_id}/activate/{version}", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def activate_workflow_version_route(workflow_id: str, version: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return activate_workflow_version(current_user, workflow_id, version)


@router.post("/{workflow_id}/activate", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def activate_workflow_route(workflow_id: str, payload: WorkflowVersionCreateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return activate_workflow_version(current_user, workflow_id, payload.version)


@router.post("/{workflow_id}/disable", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def disable_workflow_route(workflow_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return disable_workflow(current_user, workflow_id)


@router.delete("/{workflow_id}", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def archive_workflow_route(workflow_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return archive_workflow(current_user, workflow_id)


@router.post("/{workflow_id}/run", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def workflow_run_route(workflow_id: str, payload: WorkflowStartRequest, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"), current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    body = dict(payload.input_payload or {})
    if payload.engine:
        body["engine"] = payload.engine
    return start_run(workflow_id, current_user, body, idempotency_key=idempotency_key)


@router.post("/{workflow_id}/runs", dependencies=[Depends(workflow_write_rate_limit)] if workflow_write_rate_limit else [])
def workflow_runs_alias_route(workflow_id: str, payload: WorkflowStartRequest, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"), current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    body = dict(payload.input_payload or {})
    if payload.engine:
        body["engine"] = payload.engine
    return start_run(workflow_id, current_user, body, idempotency_key=idempotency_key)
