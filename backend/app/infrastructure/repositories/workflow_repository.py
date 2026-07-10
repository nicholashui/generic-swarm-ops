from app.runtime import runtime


def list_workflows():
    return runtime.list_collection("workflows")
