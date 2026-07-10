from app.runtime import AuthenticatedUser, runtime


def list_workflows(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_workflows(current_user)


def get_workflow(current_user: AuthenticatedUser, workflow_id: str) -> dict:
    return runtime.get_workflow(current_user, workflow_id)


def list_workflow_versions(current_user: AuthenticatedUser, workflow_id: str) -> list[dict]:
    return runtime.list_workflow_versions(current_user, workflow_id)


def create_workflow(current_user: AuthenticatedUser, payload: dict) -> dict:
    return runtime.create_workflow(current_user, payload)


def update_workflow(current_user: AuthenticatedUser, workflow_id: str, payload: dict) -> dict:
    return runtime.update_workflow(current_user, workflow_id, payload)


def add_workflow_version(current_user: AuthenticatedUser, workflow_id: str, payload: dict) -> dict:
    return runtime.add_workflow_version(current_user, workflow_id, payload)


def activate_workflow_version(current_user: AuthenticatedUser, workflow_id: str, version: str) -> dict:
    return runtime.activate_workflow_version(current_user, workflow_id, version)


def disable_workflow(current_user: AuthenticatedUser, workflow_id: str) -> dict:
    return runtime.disable_workflow(current_user, workflow_id)


def archive_workflow(current_user: AuthenticatedUser, workflow_id: str) -> dict:
    return runtime.archive_workflow(current_user, workflow_id)
