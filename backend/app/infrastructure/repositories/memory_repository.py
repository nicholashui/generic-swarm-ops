from app.runtime import runtime


def list_memory():
    return runtime.list_collection("memory_items")
