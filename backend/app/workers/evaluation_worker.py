from app.runtime import runtime


def refresh_evaluations() -> int:
    return len(runtime.list_collection("evaluation_runs"))
