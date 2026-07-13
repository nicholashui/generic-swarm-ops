#!/usr/bin/env python3
"""Prove generic-swarm-ops is an executable product (local control plane).

Runs integrity gates + drives shipped FastAPI health and (optional) pytest modules.
Exit 0 only if all required checks pass.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=str(cwd or ROOT), capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    return r.returncode, out


def check_health_via_testclient() -> dict:
    sys.path.insert(0, str(BACKEND))
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    health = client.get("/api/v1/health")
    ready = client.get("/api/v1/health/ready")
    live = client.get("/api/v1/health/live")
    assert health.status_code == 200, health.text
    assert ready.status_code == 200, ready.text
    assert live.status_code == 200, live.text
    h = health.json()
    r = ready.json()
    assert h.get("status") == "ok"
    assert r.get("status") in {"ready", "degraded"}
    deps = r.get("dependencies") or {}
    assert deps.get("database") in {"postgres", "json-file", "unknown"} or "database" in deps
    return {"health": h, "ready": r, "live": live.json()}


def main() -> int:
    report: dict = {"ok": True, "checks": {}}

    code, out = run([sys.executable, "scripts/business/inventory_check.py"])
    report["checks"]["inventory"] = {"exit": code, "out": out.strip()}
    if code != 0 or "INVENTORY PASS" not in out:
        report["ok"] = False

    code, out = run([sys.executable, "scripts/business/check_video_corpus_standalone.py"])
    report["checks"]["standalone"] = {"exit": code, "out": out.strip()}
    if code != 0 or "STANDALONE PASS" not in out:
        report["ok"] = False

    try:
        report["checks"]["health_testclient"] = check_health_via_testclient()
    except Exception as exc:  # noqa: BLE001
        report["ok"] = False
        report["checks"]["health_testclient"] = {"error": str(exc)}

    # optional pytest modules (real shipped paths)
    code, out = run(
        [
            sys.executable,
            "-m",
            "pytest",
            "app/tests/e2e/test_e1_operator_path.py",
            "app/tests/unit/test_video_spine_e2e.py",
            "-q",
            "--tb=line",
        ],
        cwd=BACKEND,
    )
    report["checks"]["product_tests"] = {"exit": code, "out": out.strip()[-2000:]}
    if code != 0:
        report["ok"] = False

    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
