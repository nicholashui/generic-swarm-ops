from app.runtime import AuthenticatedUser, runtime


def login(email: str, password: str) -> dict:
    return runtime.issue_token(email, password)


def refresh(refresh_token: str) -> dict:
    return runtime.refresh_access_token(refresh_token)


def logout(token: str | None) -> dict:
    return runtime.logout(token)


def list_api_keys(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_api_keys(current_user)


def create_api_key(current_user: AuthenticatedUser, name: str) -> dict:
    return runtime.create_api_key(current_user, name)


def revoke_api_key(current_user: AuthenticatedUser, key_id: str) -> dict:
    return runtime.revoke_api_key(current_user, key_id)


def reset_password(email: str, new_password: str, acting_user: AuthenticatedUser | None = None, reset_token: str | None = None) -> dict:
    return runtime.reset_password(email, new_password, acting_user=acting_user, reset_token=reset_token)
