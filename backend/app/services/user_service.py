from app.runtime import AuthenticatedUser, runtime


def list_users(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_users(current_user)


def get_user(current_user: AuthenticatedUser, user_id: str) -> dict:
    return runtime.get_user(current_user, user_id)


def create_user(current_user: AuthenticatedUser, payload: dict) -> dict:
    return runtime.create_user(current_user, payload)


def update_user(current_user: AuthenticatedUser, user_id: str, payload: dict) -> dict:
    return runtime.update_user(current_user, user_id, payload)


def create_invitation(current_user: AuthenticatedUser, payload: dict) -> dict:
    return runtime.create_invitation(current_user, payload)


def list_invitations(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_invitations(current_user)


def accept_invitation(payload: dict) -> dict:
    return runtime.accept_invitation(
        token=payload["token"],
        password=payload["password"],
        name=payload.get("name"),
    )
