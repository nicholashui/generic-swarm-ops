from app.runtime import AuthenticatedUser, runtime


def list_audit_logs(current_user: AuthenticatedUser, action: str | None = None, resource_type: str | None = None) -> list[dict]:
    return runtime.list_audit_logs(current_user, action=action, resource_type=resource_type)


def get_audit_log(current_user: AuthenticatedUser, audit_id: str) -> dict:
    return runtime.get_audit_log(current_user, audit_id)


def stream_run_events(current_user: AuthenticatedUser, run_id: str) -> list[dict]:
    return runtime.stream_run_events(current_user, run_id)
