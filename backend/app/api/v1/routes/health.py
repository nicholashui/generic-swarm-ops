from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.core.metrics import metrics_store
from app.runtime import AuthenticatedUser, runtime

router = APIRouter()


@router.get("")
def health() -> dict:
    return {"status": "ok", "service": "generic-swarm-ops-backend"}


@router.get("/live")
def live() -> dict:
    return {"status": "alive", "service": "generic-swarm-ops-backend"}


@router.get("/ready")
def ready() -> dict:
    import os

    from fastapi import HTTPException

    from app.infrastructure.database.session import database_status

    db = database_status()
    store_backend = getattr(runtime.store, "backend", "unknown")
    require_pg = os.getenv("GENERIC_SWARM_REQUIRE_POSTGRES", "false").lower() == "true"
    ready_db = store_backend == "postgres" and db.get("reachable") is True
    # JSON fallback is still "ready" for local/dev; Postgres preferred when configured
    status = "ready" if store_backend in {"postgres", "json-file"} else "degraded"
    if db.get("configured") and db.get("reachable") is False and store_backend == "json-file":
        status = "degraded"
    if require_pg and not ready_db:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "reason": "Postgres required but not reachable",
                "dependencies": {
                    "database": store_backend,
                    "database_detail": db,
                },
            },
        )
    return {
        "status": status,
        "dependencies": {
            "database": store_backend,
            "database_detail": db,
            "postgres_preferred": ready_db,
            "redis": "not_configured",
            "queue": "local-inline-dispatch",
            "vector_store": "not_configured",
            "object_storage": store_backend,
            "tool_adapters": "local",
        },
    }


@router.get("/metrics")
def metrics(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "settings:read")
    return metrics_store.snapshot()
