from app.runtime import AuthenticatedUser, runtime


def list_organizations(current_user: AuthenticatedUser) -> list[dict]:
    return runtime.list_organizations(current_user)


def get_organization(current_user: AuthenticatedUser, organization_id: str) -> dict:
    return runtime.get_organization(current_user, organization_id)


def update_organization(current_user: AuthenticatedUser, organization_id: str, payload: dict) -> dict:
    return runtime.update_organization(current_user, organization_id, payload)
