from app.runtime import AuthenticatedUser, runtime


def search(
    current_user: AuthenticatedUser,
    query: str | None = None,
    *,
    multi_hop: bool | None = None,
) -> list[dict]:
    return runtime.search_knowledge(current_user, query, multi_hop=multi_hop)


def get_document(current_user: AuthenticatedUser, document_id: str) -> dict:
    return runtime.get_knowledge_document(current_user, document_id)


def upload(current_user: AuthenticatedUser, payload: dict) -> dict:
    return runtime.upload_knowledge_document(current_user, payload)


def index_document(current_user: AuthenticatedUser, document_id: str) -> dict:
    return runtime.index_knowledge_document(current_user, document_id)


def archive_document(current_user: AuthenticatedUser, document_id: str) -> dict:
    return runtime.archive_knowledge_document(current_user, document_id)
