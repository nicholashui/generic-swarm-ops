from app.runtime import runtime


def list_approvals():
    return runtime.list_collection("approvals")
