from app.runtime import runtime


def run_pending() -> list[dict]:
    pending = []
    for run in runtime.list_collection("workflow_runs"):
        if run["status"] == "running":
            pending.append(run)
    return pending
