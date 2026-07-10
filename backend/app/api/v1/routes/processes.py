from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.services.process_service import approval_delays, bottlenecks, costs, failures, metrics, summary, workflow_performance

router = APIRouter()


@router.post("/event-logs")
def ingest_event_log_route(payload: dict, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.ingest_event_log(current_user, payload)


@router.get("/event-logs")
def list_event_logs_route(
    process_id: str | None = Query(default=None),
    case_id: str | None = Query(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> list[dict]:
    return runtime.list_event_logs(current_user, process_id=process_id, case_id=case_id)


@router.get("/discovered")
def discovered_processes_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    return runtime.discovered_processes(current_user)


@router.get("/conformance")
def conformance_route(process_id: str | None = Query(default=None), current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.conformance_report(current_user, process_id=process_id)


@router.get("/artifacts")
def pi_artifacts_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    return runtime.list_pi_artifacts(current_user)


@router.get("/summary")
def processes_summary_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "processes:read")
    return summary(current_user)


@router.get("/metrics")
def processes_metrics_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "processes:read")
    return metrics(current_user)


@router.get("/workflow-performance")
def workflow_performance_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "processes:read")
    return workflow_performance(current_user)


@router.get("/bottlenecks")
def process_bottlenecks_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "processes:read")
    return bottlenecks(current_user)


@router.get("/approval-delays")
def process_approval_delays_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "processes:read")
    return approval_delays(current_user)


@router.get("/costs")
def process_costs_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "processes:read")
    return costs(current_user)


@router.get("/failures")
def process_failures_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "processes:read")
    return failures(current_user)
