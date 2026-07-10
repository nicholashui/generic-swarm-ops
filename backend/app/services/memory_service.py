from app.runtime import AuthenticatedUser, runtime


def search(
    requested_by: AuthenticatedUser,
    query: str | None = None,
    scope: str | None = None,
    acting_agent_id: str | None = None,
) -> list[dict]:
    return runtime.search_memory(requested_by, query=query, scope=scope, acting_agent_id=acting_agent_id)


def get(requested_by: AuthenticatedUser, memory_id: str) -> dict:
    return runtime.get_memory_item(requested_by, memory_id)


def create(requested_by: AuthenticatedUser, payload: dict) -> dict:
    return runtime.create_memory_item(requested_by, payload)


def update(requested_by: AuthenticatedUser, memory_id: str, payload: dict) -> dict:
    return runtime.update_memory_item(requested_by, memory_id, payload)


def delete(requested_by: AuthenticatedUser, memory_id: str) -> dict:
    return runtime.delete_memory_item(requested_by, memory_id)
