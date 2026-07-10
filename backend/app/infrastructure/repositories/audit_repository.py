from app.runtime import runtime


def list_audit_logs():
    return runtime.list_collection("audit_logs")
