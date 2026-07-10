from app.runtime import runtime


def list_notifications() -> list[dict]:
    return runtime.list_collection("notifications")
