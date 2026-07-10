from app.runtime import runtime


def list_users():
    return runtime.list_collection("users")
