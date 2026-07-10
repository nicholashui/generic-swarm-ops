from app.runtime import ROLE_PERMISSIONS


def allowed_permissions(role: str) -> set[str]:
    return ROLE_PERMISSIONS.get(role, set())
