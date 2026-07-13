"""Deterministic video archetype (A–J) + scale recommender.

Maps a free-text production brief to Workflow DNA ids defined in the video
Domain Pack. Does not expand host tool allow-lists. HiTL confirm is recommended
before starting a paid run.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def default_registry_path(repo_root: Path | None = None) -> Path:
    root = repo_root or Path(__file__).resolve().parents[4]
    return root / "business" / "video" / "archetype_registry.json"


def load_registry(path: Path | None = None, repo_root: Path | None = None) -> dict[str, Any]:
    p = path or default_registry_path(repo_root)
    if not p.is_file():
        raise FileNotFoundError(f"archetype registry not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _duration_seconds(brief: str, explicit: int | None) -> int | None:
    if explicit is not None and explicit > 0:
        return int(explicit)
    b = _normalize(brief)
    # 90s / 90 sec / 90 seconds
    m = re.search(r"\b(\d{1,4})\s*(s|sec|secs|second|seconds)\b", b)
    if m:
        return int(m.group(1))
    m = re.search(r"\b(\d{1,3})\s*(m|min|mins|minute|minutes)\b", b)
    if m:
        return int(m.group(1)) * 60
    m = re.search(r"\b(\d{1,2})\s*(h|hr|hrs|hour|hours)\b", b)
    if m:
        return int(m.group(1)) * 3600
    if "15s" in b or "15-second" in b:
        return 15
    if "30s" in b or "30-second" in b:
        return 30
    if "60s" in b or "1-minute" in b or "1 minute" in b:
        return 60
    return None


def _infer_scale(duration_sec: int | None, brief: str, profiles: dict[str, Any]) -> str:
    b = _normalize(brief)
    if any(k in b for k in ("feature film", "feature-length", "theatrical", "feature length")):
        return "S7"
    if any(k in b for k in ("documentary", "long-form", "long form", "enterprise learning")):
        return "S5"
    if any(k in b for k in ("lms", "training library", "course series")):
        return "S6"
    if duration_sec is None:
        if any(k in b for k in ("tiktok", "reels", "shorts", "hook", "meme")):
            return "S1"
        return "S2"
    # pick smallest profile whose max covers duration
    order = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
    for code in order:
        prof = profiles.get(code) or {}
        mx = prof.get("duration_sec_max")
        if mx is None or duration_sec <= int(mx):
            return code
    return "S7"


def _keyword_score(brief: str, keywords: list[str], weight: float = 1.0) -> tuple[float, list[str]]:
    b = _normalize(brief)
    hits: list[str] = []
    score = 0.0
    for kw in keywords:
        k = kw.lower()
        if k and k in b:
            hits.append(kw)
            # longer phrases weigh more
            score += weight * (1.0 + min(2.0, len(k.split()) * 0.35))
    return score, hits


def score_archetype(
    brief: str,
    arch: dict[str, Any],
    *,
    duration_sec: int | None,
    scale: str,
) -> dict[str, Any]:
    pos, pos_hits = _keyword_score(brief, list(arch.get("keywords") or []), weight=1.0)
    neg, neg_hits = _keyword_score(brief, list(arch.get("negative_keywords") or []), weight=1.2)
    score = pos - neg

    # duration band bonus
    hint = arch.get("duration_sec_hint") or [None, None]
    if duration_sec is not None and hint[0] is not None and hint[1] is not None:
        lo, hi = int(hint[0]), int(hint[1])
        if lo <= duration_sec <= hi:
            score += 2.5
        elif duration_sec < lo * 0.5 or duration_sec > hi * 2.5:
            score -= 1.5

    allowed = list(arch.get("allowed_scales") or [])
    default_scale = arch.get("default_scale") or (allowed[0] if allowed else scale)
    if scale in allowed:
        score += 1.0
    elif allowed:
        score -= 0.75

    # depth preference when scores tie-ish: prefer deeper DNA slightly
    depth = arch.get("depth") or ""
    if depth in {"runnable_spine", "phased_v1"}:
        score += 0.35

    reasons: list[str] = []
    if pos_hits:
        reasons.append("matched keywords: " + ", ".join(pos_hits[:6]))
    if neg_hits:
        reasons.append("negative keywords: " + ", ".join(neg_hits[:4]))
    if duration_sec is not None:
        reasons.append(f"duration_sec={duration_sec}")
    reasons.append(f"scale={scale}; default_scale={default_scale}")

    return {
        "code": arch.get("code"),
        "name": arch.get("name"),
        "process_id": arch.get("process_id"),
        "dna_id": arch.get("dna_id"),
        "dna_path": arch.get("dna_path"),
        "depth": depth,
        "score": round(score, 3),
        "matched_keywords": pos_hits,
        "negative_hits": neg_hits,
        "recommended_scale": scale if scale in allowed else default_scale,
        "allowed_scales": allowed,
        "lead_agents": arch.get("lead_agents") or [],
        "critic_agents": arch.get("critic_agents") or [],
        "reasons": reasons,
    }


def recommend_workflow(
    brief: str,
    *,
    duration_sec: int | None = None,
    top_k: int = 3,
    registry: dict[str, Any] | None = None,
    registry_path: Path | None = None,
    repo_root: Path | None = None,
    budget_hint: str | None = None,
    channel_hint: str | None = None,
) -> dict[str, Any]:
    """Return ranked archetype recommendations for a production brief."""
    reg = registry or load_registry(registry_path, repo_root)
    text = " ".join(
        x for x in [brief or "", budget_hint or "", channel_hint or ""] if x
    ).strip()
    if not text:
        raise ValueError("brief is required")

    profiles = reg.get("scale_profiles") or {}
    dur = _duration_seconds(text, duration_sec)
    scale = _infer_scale(dur, text, profiles)
    policy = reg.get("selection_policy") or {}

    ranked = [
        score_archetype(text, arch, duration_sec=dur, scale=scale)
        for arch in (reg.get("archetypes") or [])
        if isinstance(arch, dict)
    ]
    ranked.sort(key=lambda r: r["score"], reverse=True)
    top = ranked[: max(1, min(top_k, len(ranked)))]

    best = top[0] if top else None
    # confidence: softmax-ish on top scores
    if best and len(ranked) >= 2:
        s0 = max(0.0, float(best["score"]))
        s1 = max(0.0, float(ranked[1]["score"]))
        conf = s0 / (s0 + s1 + 1e-6) if (s0 + s1) > 0 else 0.0
        # map to 0.35–0.95
        confidence = round(min(0.95, max(0.35, 0.45 + conf * 0.5)), 3)
    elif best:
        confidence = 0.55 if float(best["score"]) > 0 else 0.4
    else:
        confidence = 0.0

    min_auto = float(policy.get("min_confidence_auto") or 0.72)
    require_hitl = bool(policy.get("require_hitl_confirm", True))
    auto_ok = (not require_hitl) and confidence >= min_auto and best and float(best["score"]) > 0

    if not best or float(best["score"]) <= 0:
        # fallback spine
        recommendation = {
            "code": None,
            "name": "Orchestration spine (fallback)",
            "process_id": policy.get("fallback_process_id") or "video.spine.orchestrate",
            "dna_id": policy.get("fallback_dna_id") or "wf_video_spine_v1",
            "dna_path": "business/video/workflows/wf_video_spine_v1.dna.json",
            "recommended_scale": scale,
            "score": 0.0,
            "reasons": ["no positive archetype match; use spine DNA"],
        }
        confidence = min(confidence, 0.4)
        auto_ok = False
    else:
        recommendation = {
            "code": best["code"],
            "name": best["name"],
            "process_id": best["process_id"],
            "dna_id": best["dna_id"],
            "dna_path": best["dna_path"],
            "depth": best.get("depth"),
            "recommended_scale": best["recommended_scale"],
            "score": best["score"],
            "lead_agents": best.get("lead_agents"),
            "critic_agents": best.get("critic_agents"),
            "reasons": best.get("reasons"),
        }

    return {
        "domain_id": reg.get("domain_id") or "video",
        "brief": brief,
        "duration_sec": dur,
        "inferred_scale": scale,
        "scale_profile": profiles.get(recommendation.get("recommended_scale") or scale),
        "recommendation": recommendation,
        "alternatives": top[1:],
        "ranked_all": ranked,
        "confidence": confidence,
        "hitl_confirm_required": require_hitl or not auto_ok,
        "auto_start_allowed": auto_ok,
        "entry_agents": reg.get("entry_agents") or ["video.orchestrator", "video.planner"],
        "selection_policy": policy,
        "how_to_run": {
            "1": "Confirm archetype/DNA with human (recommended)",
            "2": f"Start workflow run with dna_id={recommendation.get('dna_id')}",
            "3": "Entry agents: video.planner (decompose) → video.orchestrator (execute DNA)",
            "4": "Router uses router_table/standby for per-node specialists",
        },
    }
