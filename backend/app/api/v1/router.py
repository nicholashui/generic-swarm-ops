from fastapi import APIRouter

from app.api.v1.routes import (
    approvals,
    agents,
    audit_logs,
    auth,
    domains,
    evaluations,
    evolution,
    governance,
    health,
    improvement,
    knowledge,
    loops,
    memory,
    orchestration,
    organizations,
    processes,
    settings,
    tools,
    users,
    workflow_runs,
    workflows,
)

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(domains.router, prefix="/domains", tags=["domains"])
api_router.include_router(tools.router, prefix="/tools", tags=["tools"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(workflow_runs.router, prefix="/workflow-runs", tags=["workflow-runs"])
api_router.include_router(orchestration.router, prefix="/orchestration", tags=["orchestration"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["approvals"])
api_router.include_router(governance.router, prefix="/governance", tags=["governance"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["audit-logs"])
api_router.include_router(processes.router, prefix="/processes", tags=["processes"])
api_router.include_router(evolution.router, prefix="/evolution", tags=["evolution"])
api_router.include_router(improvement.router, prefix="/improvement", tags=["improvement"])
api_router.include_router(loops.router, prefix="/loops", tags=["loops"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
