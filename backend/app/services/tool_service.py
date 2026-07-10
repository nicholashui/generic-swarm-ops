from app.runtime import AuthenticatedUser, runtime


def list_tools(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_tools(current_user)


def get_tool(current_user: AuthenticatedUser, tool_id: str) -> dict:
    return runtime.get_tool(current_user, tool_id)


def create_tool(current_user: AuthenticatedUser, payload: dict) -> dict:
    return runtime.create_tool(current_user, payload)


def update_tool_status(current_user: AuthenticatedUser, tool_id: str, enabled: bool) -> dict:
    return runtime.update_tool_status(current_user, tool_id, enabled)


def archive_tool(current_user: AuthenticatedUser, tool_id: str) -> dict:
    return runtime.archive_tool(current_user, tool_id)
