from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.runtime import AuthenticatedUser, runtime

router = APIRouter()


@router.get("/variants")
def list_variants(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    return runtime.list_evolution_variants(current_user)


@router.get("/archive")
def evolution_archive(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    """Population archive of variants ranked by fitness (DGM-lite)."""
    return runtime.evolution_archive(current_user)


@router.post("/variants")
def propose_variant(payload: dict, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.propose_evolution_variant(current_user, payload)


@router.post("/variants/{variant_id}/evaluate")
def evaluate_variant(variant_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.sandbox_evaluate_variant(current_user, variant_id)


@router.post("/variants/{variant_id}/promote")
def promote_variant(variant_id: str, payload: dict | None = None, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    mode = (payload or {}).get("mode", "canary")
    return runtime.promote_evolution_variant(current_user, variant_id, mode=mode)


@router.post("/variants/{variant_id}/rollback")
def rollback_variant(variant_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    return runtime.rollback_evolution_variant(current_user, variant_id)


@router.post("/coevolution/run")
def run_coevolution(payload: dict | None = None, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    """Multi-generation sandbox coevolution (Wave 3). Never auto-promotes."""
    body = payload or {}
    agent_ids = body.get("agent_ids")
    if agent_ids is not None and not isinstance(agent_ids, list):
        agent_ids = None
    return runtime.run_coevolution_experiment(
        current_user,
        generations=int(body.get("generations") or 2),
        domain_id=str(body.get("domain_id") or body.get("domain") or "video"),
        agent_ids=agent_ids,
        base_workflow_id=str(body.get("base_workflow_id") or "wf_video_arch_a_viral_hook_v1"),
    )


@router.get("/governance/review")
def governance_review(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    """List pending learned artifacts for human sign-off (no promote)."""
    return runtime.governance_review_learned_artifacts(current_user)
