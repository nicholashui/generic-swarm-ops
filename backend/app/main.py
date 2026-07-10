from __future__ import annotations

from time import perf_counter
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import register_error_handlers
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import log_api_request
from app.core.metrics import metrics_store
from app.runtime import runtime

app = FastAPI(title=settings.app_name, version="0.1.0", openapi_url=f"{settings.api_prefix}/openapi.json")
register_error_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    started_at = perf_counter()
    request_id = request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex[:12]}"
    runtime.set_request_id(request_id)
    request.state.request_id = request_id
    response = await call_next(request)
    duration_ms = (perf_counter() - started_at) * 1000
    client_ip = request.client.host if request.client and request.client.host else "unknown"
    metrics_store.record(request.method, request.url.path, response.status_code, duration_ms)
    log_api_request(request_id, request.method, request.url.path, response.status_code, duration_ms, client_ip)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'"
    response.headers["Permissions-Policy"] = "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
    response.headers["Cache-Control"] = "no-store"
    if settings.environment == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    runtime.set_request_id(None)
    return response


app.include_router(api_router, prefix=settings.api_prefix)
