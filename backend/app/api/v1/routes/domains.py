from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime

router = APIRouter()


@router.get("")
def list_domains(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    return runtime.list_domain_packs(current_user)


@router.post("/register")
def register_domain(payload: dict, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.register_domain_pack(
        current_user,
        manifest=payload.get("manifest"),
        manifest_path=payload.get("manifest_path"),
    )


@router.get("/video/n3-status")
def video_n3_status(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    """Wave 5 N3 roster/process completeness for the video pack."""
    return runtime.video_n3_roster_status(current_user)


@router.get("/video/archetypes")
def video_archetypes(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    """List video production archetypes A–J and scale profiles (selection registry)."""
    return runtime.list_video_archetypes(current_user)


@router.post("/video/recommend-workflow")
def video_recommend_workflow(
    payload: dict,
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    """Recommend Workflow DNA (A–J) + scale for a free-text production brief.

    Body: { brief, duration_sec?, top_k?, budget_hint?, channel_hint? }
    Always returns hitl_confirm_required unless policy allows auto-start.
    """
    return runtime.recommend_video_workflow(
        current_user,
        brief=str(payload.get("brief") or ""),
        duration_sec=payload.get("duration_sec"),
        top_k=int(payload.get("top_k") or 3),
        budget_hint=payload.get("budget_hint"),
        channel_hint=payload.get("channel_hint"),
    )
