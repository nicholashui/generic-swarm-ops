from app.runtime import runtime


def list_knowledge():
    return runtime.list_collection("knowledge_documents")
