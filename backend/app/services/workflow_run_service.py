from app.runtime import AuthenticatedUser, runtime


def list_runs(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_runs(current_user)


def get_run(current_user: AuthenticatedUser, run_id: str) -> dict:
    return runtime.get_run(current_user, run_id)


def get_run_steps(current_user: AuthenticatedUser, run_id: str) -> list[dict]:
    return runtime.get_run_steps(current_user, run_id)


def start_run(workflow_id: str, requested_by: AuthenticatedUser, payload: dict, idempotency_key: str | None = None) -> dict:
    return runtime.start_workflow_run(workflow_id, requested_by, payload, idempotency_key=idempotency_key)


def dispatch_runs(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.dispatch_queued_runs(current_user)


def cancel_run(current_user: AuthenticatedUser, run_id: str) -> dict:
    return runtime.cancel_run(current_user, run_id)


def pause_run(current_user: AuthenticatedUser, run_id: str) -> dict:
    return runtime.pause_run(current_user, run_id)


def resume_run(current_user: AuthenticatedUser, run_id: str) -> dict:
    return runtime.resume_run(current_user, run_id)


def expire_run(current_user: AuthenticatedUser, run_id: str, reason: str | None = None) -> dict:
    return runtime.expire_run(current_user, run_id, reason=reason)


def retry_run(current_user: AuthenticatedUser, run_id: str) -> dict:
    return runtime.retry_run(current_user, run_id)
