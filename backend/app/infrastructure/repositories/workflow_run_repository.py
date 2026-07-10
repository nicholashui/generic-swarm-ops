from app.runtime import runtime


def list_runs():
    return runtime.list_collection("workflow_runs")
