from app.runtime import AuthenticatedUser, runtime


def list_approvals(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_approvals(current_user)


def get_approval(current_user: AuthenticatedUser, approval_id: str) -> dict:
    return runtime.get_approval(current_user, approval_id)


def decide(approval_id: str, decision: str, reason: str | None, decided_by: AuthenticatedUser) -> dict:
    return runtime.decide_approval(approval_id, decision, reason, decided_by)


def reassign(approval_id: str, reviewer_user_id: str, decided_by: AuthenticatedUser) -> dict:
    return runtime.reassign_approval(approval_id, reviewer_user_id, decided_by)
