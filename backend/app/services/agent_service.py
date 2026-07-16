from app.runtime import AuthenticatedUser, runtime


def list_agents(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_agents(current_user)


def get_agent(current_user: AuthenticatedUser, agent_id: str) -> dict:
    return runtime.get_agent(current_user, agent_id)


def get_agent_spec(current_user: AuthenticatedUser, agent_id: str) -> dict:
    return runtime.get_agent_spec_markdown(current_user, agent_id)


def create_agent(current_user: AuthenticatedUser, payload: dict) -> dict:
    return runtime.create_agent(current_user, payload)


def update_agent_status(current_user: AuthenticatedUser, agent_id: str, status: str) -> dict:
    return runtime.update_agent_status(current_user, agent_id, status)


def archive_agent(current_user: AuthenticatedUser, agent_id: str) -> dict:
    return runtime.archive_agent(current_user, agent_id)


def agent_activity(current_user: AuthenticatedUser, agent_id: str) -> list[dict]:
    return runtime.agent_activity(current_user, agent_id)


def agent_tools(current_user: AuthenticatedUser, agent_id: str) -> list[dict]:
    return runtime.agent_tools(current_user, agent_id)
