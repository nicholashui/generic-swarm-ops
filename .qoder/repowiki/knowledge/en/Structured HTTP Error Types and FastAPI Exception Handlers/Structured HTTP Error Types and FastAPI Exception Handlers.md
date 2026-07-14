---
kind: error_handling
name: Structured HTTP Error Types and FastAPI Exception Handlers
category: error_handling
scope:
    - '**'
source_files:
    - backend/app/runtime.py
    - backend/app/api/errors.py
    - backend/app/core/errors.py
    - backend/app/main.py
    - backend/app/infrastructure/tools/adapters.py
    - backend/app/infrastructure/governance/alc_validator.py
---

The backend uses a layered error-handling approach centered on a small hierarchy of domain-specific exception classes, registered as FastAPI exception handlers that normalize all responses into a uniform JSON envelope.

Core error type hierarchy — All API-visible errors inherit from RuntimeErrorBase defined in backend/app/runtime.py. The base class exposes status_code, error_code, and a message attribute; subclasses specialize the HTTP code and machine-readable code:
- NotFoundError → 404 / not_found
- PermissionDeniedError → 403 / permission_denied
- ApprovalRequiredError → 409 / approval_required
- ValidationError → 422 / validation_error
- RateLimitedError → 429 / rate_limited (adds a retry_after integer)

These are re-exported via app/core/errors.py so other packages import from a stable surface. Domain-layer exceptions such as ToolAdapterError (infrastructure/tools/adapters.py) and AlcRequiredError (infrastructure/governance/alc_validator.py) are not part of this hierarchy and are not globally handled by the same handler.

FastAPI exception registration — register_error_handlers(app) in backend/app/api/errors.py installs two handlers:
1. A RuntimeErrorBase handler that maps each subclass to its status_code and error_code, attaches a Retry-After header when present, and returns a body shaped as { error: { code, message, details }, meta: { request_id } }.
2. A catch-all Exception handler that logs via log_exception, then returns 500 with code: internal_error.

Request-scoped context — main.py registers an HTTP middleware that injects a request_id (from X-Request-ID or generated), stores it in both runtime.set_request_id and request.state.request_id, and echoes it back in the response header. The error handlers include this ID in the meta field for correlation.

Where errors are raised — Business logic in runtime.RuntimeServices raises the typed errors directly (e.g., PermissionDeniedError on bad tokens, NotFoundError on missing users). Rate limiting is enforced in core/rate_limit.py by raising RateLimitedError. Infrastructure adapters wrap third-party calls in ToolAdapterError, which is not caught by the global handler and therefore surfaces as a 500 unless callers catch it.

Frontend handling — The Next.js frontend consumes the OpenAPI contract generated from the backend; no dedicated error-display framework was found in the scanned files, so client-side error presentation relies on standard fetch/HTTP error codes returned by the server's envelope.