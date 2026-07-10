from app.runtime import runtime


def compact_memory() -> int:
    return len(runtime.list_collection("memory_items"))
