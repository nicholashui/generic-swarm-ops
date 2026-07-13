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
