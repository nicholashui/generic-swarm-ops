"""Orchestration patterns + graph topology/state APIs — LG-11."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.core.errors import NotFoundError, ValidationError
from app.infrastructure.langgraph_engine.compiler import build_topology
from app.infrastructure.langgraph_engine.patterns.catalog import PATTERN_CATALOG
from app.infrastructure.orchestration.registry import list_engines
from app.runtime import AuthenticatedUser, runtime

router = APIRouter()


@router.get("/patterns")
def orchestration_patterns_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "workflows:read")
    return {"items": PATTERN_CATALOG, "engines": list_engines()}


@router.get("/engines")
def orchestration_engines_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    runtime.assert_permission(current_user, "workflows:read")
    return {"items": list_engines()}
