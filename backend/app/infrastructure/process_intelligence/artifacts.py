"""Process-intelligence artifact builders — disk + store-ready records.

Writes under ``business/process-intelligence/`` so traces become first-class
business artifacts (structure.md / plan P3).
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _safe_name(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in value)
    return cleaned[:80] or "unknown"


def build_discovered_artifact(
    process_id: str,
    *,
    activities: list[str],
    case_count: int,
    event_count: int,
    organization_id: str,
) -> dict[str, Any]:
    return {
        "id": f"disc_{_safe_name(process_id)}",
        "artifact_type": "discovered_process",
        "process_id": process_id,
        "organization_id": organization_id,
        "activities": list(activities),
        "case_count": case_count,
        "event_count": event_count,
        "discovered_from": "event_logs",
        "updated_at": _now(),
        "provenance": {
            "source_refs": ["event_logs", "api/v1/processes/event-logs"],
            "captured_by": "process_intelligence",
            "recorded_at": _now(),
        },
    }


def build_conformance_artifact(report: dict[str, Any], *, organization_id: str) -> dict[str, Any]:
    process_id = report.get("process_id") or "all"
    return {
        "id": f"conf_{_safe_name(str(process_id))}",
        "artifact_type": "conformance_report",
        "organization_id": organization_id,
        **report,
        "updated_at": _now(),
        "provenance": {
            "source_refs": ["event_logs", "business/materials/sops"],
            "captured_by": "process_intelligence",
            "recorded_at": _now(),
        },
    }


def build_bottleneck_artifact(
    bottlenecks: list[dict[str, Any]],
    *,
    organization_id: str,
    process_id: str | None = None,
) -> dict[str, Any]:
    key = process_id or "org"
    return {
        "id": f"bn_{_safe_name(str(key))}",
        "artifact_type": "bottleneck_report",
        "organization_id": organization_id,
        "process_id": process_id or "all",
        "bottlenecks": bottlenecks,
        "count": len(bottlenecks),
        "updated_at": _now(),
        "provenance": {
            "source_refs": ["event_logs", "workflow_runs"],
            "captured_by": "process_intelligence",
            "recorded_at": _now(),
        },
    }


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return str(path.as_posix())


def write_pi_artifacts(
    repo_root: Path,
    *,
    organization_id: str,
    discovered: list[dict[str, Any]],
    conformance_by_process: dict[str, dict[str, Any]],
    bottlenecks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Write PI artifacts under business/process-intelligence/ and return store records."""
    base = repo_root / "business" / "process-intelligence"
    written: list[dict[str, Any]] = []

    for item in discovered:
        pid = item.get("process_id") or "unknown"
        artifact = build_discovered_artifact(
            str(pid),
            activities=list(item.get("activities") or []),
            case_count=int(item.get("case_count") or 0),
            event_count=int(item.get("event_count") or 0),
            organization_id=organization_id,
        )
        rel = f"business/process-intelligence/discovered-processes/{_safe_name(str(pid))}.json"
        artifact["artifact_path"] = _write_json(repo_root / rel, artifact)
        artifact["relative_path"] = rel
        written.append(artifact)

    for pid, report in conformance_by_process.items():
        artifact = build_conformance_artifact(report, organization_id=organization_id)
        rel = f"business/process-intelligence/conformance-reports/{_safe_name(str(pid))}.json"
        artifact["artifact_path"] = _write_json(repo_root / rel, artifact)
        artifact["relative_path"] = rel
        written.append(artifact)

    bn = build_bottleneck_artifact(bottlenecks, organization_id=organization_id)
    rel = "business/process-intelligence/bottlenecks/latest.json"
    bn["artifact_path"] = _write_json(repo_root / rel, bn)
    bn["relative_path"] = rel
    written.append(bn)

    # Keep base tree present even if empty
    for sub in ("discovered-processes", "conformance-reports", "bottlenecks"):
        (base / sub).mkdir(parents=True, exist_ok=True)

    return written
