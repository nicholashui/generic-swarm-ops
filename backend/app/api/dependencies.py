from __future__ import annotations

from fastapi import Depends, Header

from app.core.auth import authenticate_bearer_token
from app.runtime import AuthenticatedUser, runtime


def get_runtime():
    return runtime


def get_current_user(authorization: str | None = Header(default=None)) -> AuthenticatedUser:
    if not authorization or not authorization.startswith("Bearer "):
        return authenticate_bearer_token(None)
    token = authorization.split(" ", 1)[1]
    return authenticate_bearer_token(token)
