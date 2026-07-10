from app.runtime import AuthenticatedUser, runtime


def preview(workflow_id: str, requested_by: AuthenticatedUser) -> dict:
    workflow = runtime.get_workflow(requested_by, workflow_id)
    return runtime.governance_preview(workflow, requested_by)


def list_policies(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_governance_policies(current_user)


def create_policy(current_user: AuthenticatedUser, payload: dict) -> dict:
    return runtime.create_governance_policy(current_user, payload)


def get_policy(current_user: AuthenticatedUser, policy_id: str) -> dict:
    return runtime.get_governance_policy(current_user, policy_id)


def update_policy(current_user: AuthenticatedUser, policy_id: str, payload: dict) -> dict:
    return runtime.update_governance_policy(current_user, policy_id, payload)


def archive_policy(current_user: AuthenticatedUser, policy_id: str) -> dict:
    return runtime.archive_governance_policy(current_user, policy_id)


def check(current_user: AuthenticatedUser, payload: dict) -> dict:
    return runtime.governance_check(current_user, payload)
