from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.errors import RuntimeErrorBase
from app.core.logging import log_exception


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RuntimeErrorBase)
    async def runtime_error_handler(request: Request, exc: RuntimeErrorBase):
        request_id = getattr(request.state, "request_id", None)
        headers = {}
        if hasattr(exc, "retry_after"):
            headers["Retry-After"] = str(exc.retry_after)
        return JSONResponse(
            status_code=exc.status_code,
            headers=headers,
            content={
                "error": {
                    "code": getattr(exc, "error_code", "bad_request"),
                    "message": exc.message,
                    "details": {},
                },
                "meta": {
                    "request_id": request_id,
                },
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", None)
        log_exception(request_id, request.method, request.url.path, str(exc))
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_error",
                    "message": "Internal server error",
                    "details": {},
                },
                "meta": {
                    "request_id": request_id,
                },
            },
        )
