from app.runtime import AuthenticatedUser, runtime


def list_evaluations(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_evaluations(current_user)


def get_evaluation(current_user: AuthenticatedUser, evaluation_id: str) -> dict:
    return runtime.get_evaluation(current_user, evaluation_id)


def run_evaluation(current_user: AuthenticatedUser, run_id: str) -> dict:
    return runtime.run_evaluation(current_user, run_id)


def list_run_evaluations(current_user: AuthenticatedUser, run_id: str) -> list[dict]:
    return runtime.list_run_evaluations(current_user, run_id)
