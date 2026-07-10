from app.runtime import runtime


def list_agents():
    return runtime.list_collection("agents")
