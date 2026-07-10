from app.runtime import runtime


def refresh_knowledge_index() -> int:
    return len(runtime.list_collection("knowledge_documents"))
