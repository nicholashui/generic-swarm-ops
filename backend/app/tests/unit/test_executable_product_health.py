"""Executable product: health/ready via real FastAPI app entrypoint."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from fastapi.testclient import TestClient

from app.main import app


def test_health_live_ready_from_shipped_app():
    client = TestClient(app)
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json().get("status") == "ok"
    assert "generic-swarm" in (health.json().get("service") or "")

    live = client.get("/api/v1/health/live")
    assert live.status_code == 200
    assert live.json().get("status") == "alive"

    ready = client.get("/api/v1/health/ready")
    assert ready.status_code == 200
    body = ready.json()
    assert body.get("status") in {"ready", "degraded"}
    deps = body.get("dependencies") or {}
    assert "database" in deps
    # Local executable product accepts json-file or postgres
    assert deps["database"] in {"postgres", "json-file"} or body.get("status") == "degraded"


def test_openapi_available():
    client = TestClient(app)
    r = client.get("/api/v1/openapi.json")
    assert r.status_code == 200
    data = r.json()
    assert "paths" in data
    assert any("/health" in p for p in data["paths"])
