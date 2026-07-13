"""Local tool adapters — real side-effect records, not invented silent success.

Adapters write durable effect payloads that the runtime stores in ``tool_effects``
and audit metadata. External systems may be substituted later without changing
the control-plane contract.
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, Callable


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _effect(tool_id: str, action: str, payload: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"fx_{uuid.uuid4().hex[:12]}",
        "tool_id": tool_id,
        "action": action,
        "status": "ok",
        "input": payload,
        "result": result,
        "created_at": _now(),
    }


def audit_log_writer(payload: dict[str, Any]) -> dict[str, Any]:
    record = {
        "message": payload.get("message") or "audit entry",
        "run_id": payload.get("run_id"),
        "step_id": payload.get("step_id"),
        "recorded_at": _now(),
    }
    return _effect("audit_log_writer", "write_audit", payload, record)


def crm(payload: dict[str, Any]) -> dict[str, Any]:
    customer = {
        "customer_id": payload.get("customer_id") or f"cust_{uuid.uuid4().hex[:8]}",
        "case_id": payload.get("case_id"),
        "name": payload.get("customer_name") or payload.get("name") or "Unknown",
        "crm_status": "created",
        "created_at": _now(),
    }
    return _effect("crm", "create_customer_record", payload, customer)


def billing_system(payload: dict[str, Any]) -> dict[str, Any]:
    invoice = {
        "billing_id": f"bill_{uuid.uuid4().hex[:8]}",
        "case_id": payload.get("case_id"),
        "status": "activated",
        "amount": payload.get("amount", 0),
        "currency": payload.get("currency", "USD"),
        "activated_at": _now(),
    }
    return _effect("billing_system", "activate_billing", payload, invoice)


def email(payload: dict[str, Any]) -> dict[str, Any]:
    message = {
        "message_id": f"msg_{uuid.uuid4().hex[:8]}",
        "to": payload.get("to") or payload.get("customer_name") or "customer@example.com",
        "subject": payload.get("subject") or "Welcome",
        "template": payload.get("template") or "welcome_packet",
        "status": "queued_local",
        "queued_at": _now(),
    }
    return _effect("email", "send_email", payload, message)


def contract_parser(payload: dict[str, Any]) -> dict[str, Any]:
    parsed = {
        "contract_id": payload.get("contract_id") or f"ctr_{uuid.uuid4().hex[:8]}",
        "case_id": payload.get("case_id"),
        "clauses_found": payload.get("clauses_found") or ["standard_terms"],
        "exception_detected": bool(payload.get("exception_detected", False)),
        "parsed_at": _now(),
    }
    return _effect("contract_parser", "parse_contract", payload, parsed)


def policy_retriever(payload: dict[str, Any]) -> dict[str, Any]:
    policy = {
        "policy_id": payload.get("policy_id") or "pol_onboarding_default",
        "matched_rules": payload.get("matched_rules") or ["require_signed_contract", "billing_human_gate"],
        "source_refs": payload.get("source_refs") or ["business/materials/sops/customer-onboarding.md"],
        "retrieved_at": _now(),
    }
    return _effect("policy_retriever", "retrieve_policy", payload, policy)


def video_media_gen_stub(payload: dict[str, Any]) -> dict[str, Any]:
    """CI-safe media generation stub (no external Sora/Veo/Kling calls)."""
    asset = {
        "asset_id": f"vid_{uuid.uuid4().hex[:10]}",
        "provider": "stub",
        "prompt": payload.get("prompt") or payload.get("hook_concept") or payload.get("message") or "video stub",
        "duration_sec": payload.get("duration_sec") or 8,
        "uri": f"stub://media/{uuid.uuid4().hex[:8]}.mp4",
        "budget_tokens": 0,
        "generated_at": _now(),
    }
    return _effect("video_media_gen_stub", "generate_media_stub", payload, asset)


def video_script_format(payload: dict[str, Any]) -> dict[str, Any]:
    script = {
        "script_id": f"scr_{uuid.uuid4().hex[:10]}",
        "format": "fountain_lite",
        "title": payload.get("title") or "Hook Draft",
        "body": payload.get("body") or payload.get("message") or "HOOK: attention beat\nCTA: watch more",
        "formatted_at": _now(),
    }
    return _effect("video_script_format", "format_script", payload, script)


def video_qc_stub(payload: dict[str, Any]) -> dict[str, Any]:
    qc = {
        "qc_id": f"qc_{uuid.uuid4().hex[:10]}",
        "pass": True,
        "consistency_score": float(payload.get("consistency_score") or 0.92),
        "checks": ["character_consistency_stub", "audio_sync_stub", "brand_safe_stub"],
        "checked_at": _now(),
    }
    return _effect("video_qc_stub", "qc_pass", payload, qc)


def video_package_stub(payload: dict[str, Any]) -> dict[str, Any]:
    package = {
        "package_id": f"pkg_{uuid.uuid4().hex[:10]}",
        "status": "packaged_pending_approval",
        "platform": payload.get("platform") or "generic",
        "artifacts": payload.get("artifacts") or ["script", "media_stub", "qc_report"],
        "packaged_at": _now(),
    }
    return _effect("video_package_stub", "package_deliverable", payload, package)


TOOL_ADAPTERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "audit_log_writer": audit_log_writer,
    "crm": crm,
    "billing_system": billing_system,
    "email": email,
    "contract_parser": contract_parser,
    "policy_retriever": policy_retriever,
    "video_media_gen_stub": video_media_gen_stub,
    "video_script_format": video_script_format,
    "video_qc_stub": video_qc_stub,
    "video_package_stub": video_package_stub,
}


class ToolAdapterError(Exception):
    def __init__(self, tool_id: str, message: str):
        super().__init__(message)
        self.tool_id = tool_id
        self.message = message


def execute_tool(tool_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    adapter = TOOL_ADAPTERS.get(tool_id)
    if adapter is None:
        raise ToolAdapterError(tool_id, f"No adapter registered for tool: {tool_id}")
    try:
        result = adapter(dict(payload or {}))
    except ToolAdapterError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise ToolAdapterError(tool_id, f"Adapter failed: {exc}") from exc
    if not isinstance(result, dict) or result.get("status") != "ok" or "id" not in result:
        raise ToolAdapterError(tool_id, "Adapter returned invalid result")
    return result
