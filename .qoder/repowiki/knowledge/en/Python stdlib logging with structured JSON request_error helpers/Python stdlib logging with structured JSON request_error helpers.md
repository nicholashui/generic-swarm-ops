---
kind: logging_system
name: Python stdlib logging with structured JSON request/error helpers
category: logging_system
scope:
    - '**'
source_files:
    - backend/app/core/logging.py
    - backend/app/main.py
    - backend/app/api/errors.py
---

The backend uses Python's built-in `logging` module as the sole logging framework. There is no third-party logger (structlog, loguru, etc.) and no dedicated log-level configuration file — level and format are set once at import time.

**Core setup**
- `backend/app/core/logging.py` calls `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")` and exposes a single root logger named `generic-swarm-ops-backend`.
- Two helper functions provide structured JSON payloads:
  - `log_api_request(...)` — emits an INFO event with fields `request_id`, `method`, `path`, `status_code`, `duration_ms`, `client_ip`.
  - `log_exception(request_id, method, path, message)` — emits an ERROR event with fields `request_id`, `method`, `path`, `message`.

**Request tracing integration**
- `backend/app/main.py` installs a FastAPI HTTP middleware that generates/propagates a `X-Request-ID` header, stores it on `request.state.request_id`, measures latency via `perf_counter`, records metrics, and calls `log_api_request` for every inbound request. The same ID is echoed back in the response header.
- Error handlers in `backend/app/api/errors.py` call `log_exception` for unhandled exceptions, attaching the current `request_id` so failures can be correlated with the originating request.

**Sinks / output**
- Logs go to stdout/stderr via `basicConfig`; there are no custom handlers, file sinks, or external log shippers configured in code. Log rotation or collection is expected to be handled by the runtime/container orchestrator (e.g., Docker/Kubernetes stdout capture).

**Conventions observed**
- All structured API logs are emitted through the two helpers rather than calling `logger.info`/`logger.error` directly, ensuring consistent field names and JSON serialization (`sort_keys=True`).
- The default level is `INFO`; no environment-based override exists in this file (level would need to be changed at `basicConfig` time or via `LOG_LEVEL` env consumed elsewhere).
- Only the backend defines logging; the Next.js frontend does not appear to use a comparable structured logging layer.