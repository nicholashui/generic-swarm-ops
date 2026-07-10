from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime
from app.schemas.common import KnowledgeSearchRequest, KnowledgeUploadRequest
from app.services.knowledge_service import archive_document, get_document, index_document, search, upload

router = APIRouter()


@router.get("")
def knowledge_route(
    query: str | None = Query(default=None),
    multi_hop: bool = Query(default=False),
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> list[dict]:
    runtime.assert_permission(current_user, "knowledge:read")
    return search(current_user, query, multi_hop=multi_hop)


@router.get("/documents")
def knowledge_documents_route(
    query: str | None = Query(default=None),
    multi_hop: bool = Query(default=False),
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> list[dict]:
    runtime.assert_permission(current_user, "knowledge:read")
    return search(current_user, query, multi_hop=multi_hop)


@router.post("")
def upload_knowledge_route(payload: KnowledgeUploadRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return upload(current_user, payload.model_dump())


@router.post("/documents")
def upload_knowledge_document_route(payload: KnowledgeUploadRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return upload(current_user, payload.model_dump())


@router.get("/documents/{document_id}")
def knowledge_document_detail_route(document_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "knowledge:read")
    return get_document(current_user, document_id)


@router.delete("/documents/{document_id}")
def archive_knowledge_document_route(document_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return archive_document(current_user, document_id)


@router.post("/documents/{document_id}/index")
def index_knowledge_document_route(document_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return index_document(current_user, document_id)


@router.post("/search")
def knowledge_search_route(payload: KnowledgeSearchRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    runtime.assert_permission(current_user, "knowledge:read")
    results = search(current_user, payload.query, multi_hop=payload.multi_hop)
    for key, value in payload.filters.items():
        results = [item for item in results if item.get(key) == value]
    return results[: payload.limit]


@router.post("/graph/extract/{document_id}")
def extract_graph_route(document_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.extract_knowledge_graph(current_user, document_id)


@router.get("/graph/query")
def graph_query_route(
    seed: str = Query(...),
    max_hops: int = Query(default=2, ge=1, le=5),
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    return runtime.query_knowledge_graph(current_user, seed=seed, max_hops=max_hops)


@router.get("/graph/gaps")
def graph_gaps_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.knowledge_graph_gaps(current_user)


@router.post("/graph/federate")
def graph_federate_route(
    payload: dict | None = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    push = bool((payload or {}).get("push_neo4j"))
    return runtime.federate_knowledge_graph(current_user, push_neo4j=push)
