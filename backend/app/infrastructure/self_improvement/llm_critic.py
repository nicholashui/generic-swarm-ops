"""Optional LLM critic — disabled by default; falls back to rule reflection."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


def llm_critique_available(settings: Any) -> bool:
    return bool(
        getattr(settings, "llm_critic_enabled", False)
        and getattr(settings, "llm_api_base", None)
    )


def llm_critique_run(run: dict[str, Any], workflow: dict[str, Any] | None, settings: Any) -> dict[str, Any] | None:
    """Call OpenAI-compatible chat API for structured critique. Returns None on skip/failure."""
    if not llm_critique_available(settings):
        return None
    base = str(settings.llm_api_base).rstrip("/")
    url = f"{base}/chat/completions"
    payload = {
        "model": getattr(settings, "llm_model", "gpt-4o-mini"),
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a governed workflow critic. Return JSON with keys: "
                    "is_satisfactory (bool), issues (string[]), lessons (string[]), "
                    "suggested_changes (array of {type, description}). "
                    "Never recommend bypassing human gates or auto_promote."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "run_status": run.get("status"),
                        "error": run.get("error"),
                        "steps": [
                            {
                                "id": s.get("id"),
                                "status": s.get("status"),
                                "error": s.get("error"),
                            }
                            for s in (run.get("steps") or [])
                        ],
                        "workflow_id": run.get("workflow_id"),
                        "risk_tier": (workflow or {}).get("risk_tier"),
                    }
                ),
            },
        ],
    }
    headers = {"Content-Type": "application/json"}
    key = getattr(settings, "llm_api_key", None)
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
            body = json.loads(resp.read().decode("utf-8"))
        content = body["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            return None
        return {
            "is_satisfactory": bool(parsed.get("is_satisfactory")),
            "issues": list(parsed.get("issues") or []),
            "lessons": list(parsed.get("lessons") or []),
            "suggested_changes": list(parsed.get("suggested_changes") or []),
            "how": "llm_critic",
            "when": "inter_episode",
            "what_evolves": ["memory", "workflow_dna_proposal"],
        }
    except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError, TypeError, IndexError):
        return None
