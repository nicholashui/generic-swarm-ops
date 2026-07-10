from app.runtime import AuthenticatedUser, runtime


def summary(current_user: AuthenticatedUser) -> dict:
    return runtime.process_summary(current_user)


def metrics(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.process_metrics(current_user)


def workflow_performance(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.workflow_performance(current_user)


def bottlenecks(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.process_bottlenecks(current_user)


def approval_delays(current_user: AuthenticatedUser) -> dict:
    return runtime.approval_delays(current_user)


def costs(current_user: AuthenticatedUser) -> dict:
    return runtime.process_costs(current_user)


def failures(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.process_failures(current_user)
