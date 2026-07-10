from __future__ import annotations

from app.runtime import AuthenticatedUser, runtime


def authenticate_bearer_token(token: str | None) -> AuthenticatedUser:
    return runtime.authenticate(token)
