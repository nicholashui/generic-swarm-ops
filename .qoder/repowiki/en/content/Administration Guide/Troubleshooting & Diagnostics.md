# Troubleshooting & Diagnostics

<cite>
**Referenced Files in This Document**
- [backend/app/main.py](file://backend/app/main.py)
- [backend/app/core/logging.py](file://backend/app/core/logging.py)
- [backend/app/core/metrics.py](file://backend/app/core/metrics.py)
- [backend/app/api/errors.py](file://backend/app/api/errors.py)
- [backend/app/runtime.py](file://backend/app/runtime.py)
- [backend/app/api/v1/routes/health.py](file://backend/app/api/v1/routes/health.py)
- [backend/app/services/audit_service.py](file://backend/app/services/audit_service.py)
- [docs/troubleshooting.md](file://docs/troubleshooting.md)
</cite>

## Table of Contents
1. Introduction
2. Project Structure
3. Core Components
4. Architecture Overview
5. Detailed Component Analysis
6. Dependency Analysis
7. Performance Considerations
8. Troubleshooting Guide
9. Conclusion

## Introduction
This document provides comprehensive troubleshooting and diagnostic guidance for the system. It covers common issues, error patterns, resolution steps, and operational procedures for log analysis, performance profiling, memory leak detection, resource utilization, API failures, workflow execution problems, integration issues, security incidents, audit log review, and forensic analysis. The content is grounded in the backend’s logging, metrics, error handling, runtime store, health endpoints, and audit services.

## Project Structure
The backend exposes a FastAPI application with:
- Central request middleware that injects request IDs, records metrics, logs requests, and sets security headers.
- Global exception handlers that normalize errors and log exceptions.
- A runtime store that persists state to Postgres (preferred) or JSON file fallback.
- Health endpoints for liveness/readiness checks and an authenticated metrics endpoint.
- Audit service methods to list and retrieve audit logs and stream run events.

```mermaid
graph TB
Client["Client"] --> MW["Request Context Middleware<br/>main.py"]
MW --> Router["API Router<br/>main.py"]
Router --> Handlers["Route Handlers"]
Handlers --> Errors["Error Handlers<br/>api/errors.py"]
Handlers --> Runtime["Runtime Store<br/>runtime.py"]
Handlers --> Metrics["Metrics Store<br/>core/metrics.py"]
Handlers --> Logging["Structured Logger<br/>core/logging.py"]
Handlers --> Audit["Audit Service<br/>services/audit_service.py"]
Handlers --> Health["Health Endpoints<br/>api/v1/routes/health.py"]
```

**Diagram sources**
- [backend/app/main.py:27-48](file://backend/app/main.py#L27-L48)
- [backend/app/api/errors.py:8-47](file://backend/app/api/errors.py#L8-L47)
- [backend/app/core/metrics.py:7-49](file://backend/app/core/metrics.py#L7-L49)
- [backend/app/core/logging.py:11-46](file://backend/app/core/logging.py#L11-L46)
- [backend/app/runtime.py:258-384](file://backend/app/runtime.py#L258-L384)
- [backend/app/api/v1/routes/health.py:10-67](file://backend/app/api/v1/routes/health.py#L10-L67)
- [backend/app/services/audit_service.py:1-14](file://backend/app/services/audit_service.py#L1-L14)

**Section sources**
- [backend/app/main.py:1-52](file://backend/app/main.py#L1-L52)
- [backend/app/api/errors.py:1-47](file://backend/app/api/errors.py#L1-L47)
- [backend/app/core/metrics.py:1-49](file://backend/app/core/metrics.py#L1-L49)
- [backend/app/core/logging.py:1-46](file://backend/app/core/logging.py#L1-L46)
- [backend/app/runtime.py:258-384](file://backend/app/runtime.py#L258-L384)
- [backend/app/api/v1/routes/health.py:1-67](file://backend/app/api/v1/routes/health.py#L1-L67)
- [backend/app/services/audit_service.py:1-14](file://backend/app/services/audit_service.py#L1-L14)

## Core Components
- Request context middleware: Generates and propagates request IDs, measures latency, records metrics, writes structured request logs, and attaches security headers.
- Error handling: Normalizes domain and unexpected exceptions into consistent JSON envelopes; includes retry hints when applicable.
- Metrics store: Thread-safe counters for total requests, errors, average duration, and per-route breakdowns.
- Structured logger: Emits JSON-formatted request and exception logs with correlation via request ID.
- Runtime store: Persists application state to Postgres (preferred) or JSON file fallback; performs migrations and sanitization.
- Health endpoints: Provide liveness, readiness (including database reachability), and authenticated metrics snapshot.
- Audit service: Provides listing, retrieval, and streaming of audit logs and run events.

**Section sources**
- [backend/app/main.py:27-48](file://backend/app/main.py#L27-L48)
- [backend/app/api/errors.py:8-47](file://backend/app/api/errors.py#L8-L47)
- [backend/app/core/metrics.py:7-49](file://backend/app/core/metrics.py#L7-L49)
- [backend/app/core/logging.py:11-46](file://backend/app/core/logging.py#L11-L46)
- [backend/app/runtime.py:258-384](file://backend/app/runtime.py#L258-L384)
- [backend/app/api/v1/routes/health.py:10-67](file://backend/app/api/v1/routes/health.py#L10-L67)
- [backend/app/services/audit_service.py:1-14](file://backend/app/services/audit_service.py#L1-L14)

## Architecture Overview
End-to-end flow for a typical API request, including diagnostics and observability hooks.

```mermaid
sequenceDiagram
participant C as "Client"
participant M as "Middleware<br/>main.py"
participant H as "Handler"
participant E as "Error Handler<br/>api/errors.py"
participant R as "Runtime Store<br/>runtime.py"
participant L as "Logger<br/>core/logging.py"
participant S as "Metrics Store<br/>core/metrics.py"
participant A as "Audit Service<br/>services/audit_service.py"
participant HP as "Health Endpoint<br/>routes/health.py"
C->>M : HTTP Request
M->>M : Generate request_id, measure start
M->>H : call_next(request)
alt Success
H-->>M : Response
M->>S : record(method,path,status,duration)
M->>L : log_api_request(...)
M-->>C : Response + X-Request-ID + Security Headers
else Exception
H-->>E : Raise RuntimeErrorBase or Exception
E->>L : log_exception(...)
E-->>M : JSONResponse envelope
M->>S : record(method,path,status,duration)
M->>L : log_api_request(...)
M-->>C : Error Response + X-Request-ID
end
Note over C,A : Audit operations use Audit Service
C->>A : List/Get Audit Logs, Stream Run Events
A-->>C : Results
Note over C,HP : Health checks
C->>HP : GET /health/live | /health/ready | /health/metrics
HP-->>C : Status + Dependencies or Metrics Snapshot
```

**Diagram sources**
- [backend/app/main.py:27-48](file://backend/app/main.py#L27-L48)
- [backend/app/api/errors.py:8-47](file://backend/app/api/errors.py#L8-L47)
- [backend/app/core/metrics.py:15-45](file://backend/app/core/metrics.py#L15-L45)
- [backend/app/core/logging.py:11-46](file://backend/app/core/logging.py#L11-L46)
- [backend/app/runtime.py:258-384](file://backend/app/runtime.py#L258-L384)
- [backend/app/api/v1/routes/health.py:10-67](file://backend/app/api/v1/routes/health.py#L10-L67)
- [backend/app/services/audit_service.py:1-14](file://backend/app/services/audit_service.py#L1-L14)

## Detailed Component Analysis

### Error Handling and Envelope
- Domain errors derive from a base class and map to specific HTTP status codes and error codes.
- Global exception handler returns a consistent JSON envelope with code, message, details, and meta.request_id.
- RateLimitedError can include Retry-After header.
- Unhandled exceptions are logged and returned as internal server error.

```mermaid
classDiagram
class RuntimeErrorBase {
+int status_code
+string error_code
+string message
}
class NotFoundError {
+status_code = 404
+error_code = "not_found"
}
class PermissionDeniedError {
+status_code = 403
+error_code = "permission_denied"
}
class ApprovalRequiredError {
+status_code = 409
+error_code = "approval_required"
}
class ValidationError {
+status_code = 422
+error_code = "validation_error"
}
class RateLimitedError {
+int retry_after
}
RuntimeErrorBase <|-- NotFoundError
RuntimeErrorBase <|-- PermissionDeniedError
RuntimeErrorBase <|-- ApprovalRequiredError
RuntimeErrorBase <|-- ValidationError
RuntimeErrorBase <|-- RateLimitedError
```

**Diagram sources**
- [backend/app/runtime.py:93-129](file://backend/app/runtime.py#L93-L129)
- [backend/app/api/errors.py:8-47](file://backend/app/api/errors.py#L8-L47)

**Section sources**
- [backend/app/runtime.py:93-129](file://backend/app/runtime.py#L93-L129)
- [backend/app/api/errors.py:8-47](file://backend/app/api/errors.py#L8-L47)

### Request Lifecycle and Observability
- Middleware generates request ID, measures duration, records metrics, logs request, and adds security headers.
- Metrics store tracks counts and averages globally and per route.
- Structured logger emits JSON lines with request correlation.

```mermaid
flowchart TD
Start(["Incoming Request"]) --> GenID["Generate/propagate request_id"]
GenID --> MeasureStart["Record start time"]
MeasureStart --> CallNext["Invoke handler"]
CallNext --> RecordMetrics["Record method/path/status/duration"]
RecordMetrics --> LogRequest["Write structured request log"]
LogRequest --> SetHeaders["Attach security headers"]
SetHeaders --> End(["Return Response"])
```

**Diagram sources**
- [backend/app/main.py:27-48](file://backend/app/main.py#L27-L48)
- [backend/app/core/metrics.py:15-45](file://backend/app/core/metrics.py#L15-L45)
- [backend/app/core/logging.py:11-31](file://backend/app/core/logging.py#L11-L31)

**Section sources**
- [backend/app/main.py:27-48](file://backend/app/main.py#L27-L48)
- [backend/app/core/metrics.py:7-49](file://backend/app/core/metrics.py#L7-L49)
- [backend/app/core/logging.py:1-46](file://backend/app/core/logging.py#L1-L46)

### Health and Readiness Checks
- Liveness: simple alive check.
- Readiness: checks configured storage backend and database reachability; can enforce Postgres requirement via environment variable.
- Metrics endpoint: requires authentication and permission.

```mermaid
flowchart TD
Req["GET /health/ready"] --> CheckDB["Check database_status()"]
CheckDB --> StoreBackend["Read runtime.store.backend"]
StoreBackend --> RequirePG{"GENERIC_SWARM_REQUIRE_POSTGRES=true?"}
RequirePG --> |Yes and DB not reachable| NotReady["HTTP 503 not_ready"]
RequirePG --> |No or DB reachable| Ready["Return status 'ready'/'degraded' + dependencies"]
```

**Diagram sources**
- [backend/app/api/v1/routes/health.py:20-60](file://backend/app/api/v1/routes/health.py#L20-L60)

**Section sources**
- [backend/app/api/v1/routes/health.py:10-67](file://backend/app/api/v1/routes/health.py#L10-L67)

### Audit and Run Event Access
- Audit service exposes list/get audit logs and stream run events, delegating to runtime.

```mermaid
sequenceDiagram
participant U as "Caller"
participant AS as "Audit Service"
participant RT as "Runtime"
U->>AS : list_audit_logs(action?, resource_type?)
AS->>RT : runtime.list_audit_logs(...)
RT-->>AS : list[dict]
AS-->>U : list[dict]
U->>AS : get_audit_log(audit_id)
AS->>RT : runtime.get_audit_log(...)
RT-->>AS : dict
AS-->>U : dict
U->>AS : stream_run_events(run_id)
AS->>RT : runtime.stream_run_events(...)
RT-->>AS : list[dict]
AS-->>U : list[dict]
```

**Diagram sources**
- [backend/app/services/audit_service.py:1-14](file://backend/app/services/audit_service.py#L1-L14)

**Section sources**
- [backend/app/services/audit_service.py:1-14](file://backend/app/services/audit_service.py#L1-L14)

## Dependency Analysis
Key runtime and infrastructure dependencies:
- Storage backend selection: Postgres preferred; JSON file fallback used if Postgres unavailable or disabled.
- Database connectivity influences readiness status.
- Metrics and logging are always active regardless of storage backend.

```mermaid
graph LR
App["FastAPI App<br/>main.py"] --> Err["Error Handlers<br/>api/errors.py"]
App --> Log["Logger<br/>core/logging.py"]
App --> Met["Metrics Store<br/>core/metrics.py"]
App --> RT["Runtime Store<br/>runtime.py"]
RT --> PG["Postgres (optional)<br/>session.py"]
RT --> JF["JSON File Fallback<br/>runtime.json"]
App --> HL["Health Endpoints<br/>routes/health.py"]
App --> AUD["Audit Service<br/>services/audit_service.py"]
```

**Diagram sources**
- [backend/app/main.py:1-52](file://backend/app/main.py#L1-L52)
- [backend/app/api/errors.py:1-47](file://backend/app/api/errors.py#L1-L47)
- [backend/app/core/logging.py:1-46](file://backend/app/core/logging.py#L1-L46)
- [backend/app/core/metrics.py:1-49](file://backend/app/core/metrics.py#L1-L49)
- [backend/app/runtime.py:258-384](file://backend/app/runtime.py#L258-L384)
- [backend/app/api/v1/routes/health.py:1-67](file://backend/app/api/v1/routes/health.py#L1-L67)
- [backend/app/services/audit_service.py:1-14](file://backend/app/services/audit_service.py#L1-L14)

**Section sources**
- [backend/app/runtime.py:258-384](file://backend/app/runtime.py#L258-L384)
- [backend/app/api/v1/routes/health.py:20-60](file://backend/app/api/v1/routes/health.py#L20-L60)

## Performance Considerations
- Use the metrics endpoint to identify slow or error-prone routes by examining per-route counts and average durations.
- Correlate high-latency requests using the request ID across logs and metrics.
- Prefer Postgres for production workloads to avoid JSON file I/O bottlenecks and ensure durability.
- Monitor error rates and 4xx/5xx spikes via metrics snapshot and structured logs.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide

### Common System Issues and Resolutions
- Backend shows no Postgres on readiness:
  - Verify DATABASE_URL configuration and that Postgres is running.
  - Check GET /health/ready response for database detail and status.
- Empty data after restart:
  - Confirm Postgres is the primary store; JSON file is backup only.
- Authentication failures:
  - Use password-based login for admin accounts; static tokens are smoke-only.
- Tool step fails closed:
  - Inspect tool_effects and audit tool.executed entries; adapters reject missing inputs.
- Flagship run fails mid-run due to memory:
  - Ensure agents have correct allowed_memory_scopes (seed/normalize union includes organization scopes).
- Import/PYTHONPATH errors:
  - From backend directory, set PYTHONPATH=. then re-run tests or uvicorn.

**Section sources**
- [docs/troubleshooting.md:13-24](file://docs/troubleshooting.md#L13-L24)

### API Failures Investigation
- Step-by-step:
  1. Capture the request ID from the response header X-Request-ID.
  2. Search logs for the request ID to locate the full trace.
  3. Review the error envelope for code, message, and details.
  4. For rate limiting, check Retry-After header and backoff strategy.
  5. Validate input schemas and permissions; verify user role and required permissions.
  6. If unhandled exception occurred, expect internal_error and inspect server logs.

**Section sources**
- [backend/app/main.py:27-48](file://backend/app/main.py#L27-L48)
- [backend/app/api/errors.py:8-47](file://backend/app/api/errors.py#L8-L47)
- [backend/app/core/logging.py:34-46](file://backend/app/core/logging.py#L34-L46)

### Workflow Execution Issues
- Step-by-step:
  1. Retrieve run events via audit service stream_run_events(run_id).
  2. Correlate run events with request IDs and structured logs.
  3. Check governance gates and approval requirements; confirm human gate steps.
  4. Validate agent allowed_tools and allowed_memory_scopes.
  5. Inspect tool_effects for adapter-level failures.

**Section sources**
- [backend/app/services/audit_service.py:12-14](file://backend/app/services/audit_service.py#L12-L14)
- [backend/app/runtime.py:730-755](file://backend/app/runtime.py#L730-L755)

### Integration Problems
- Step-by-step:
  1. Confirm external dependency status via /health/ready and its dependencies object.
  2. For Postgres-required deployments, ensure GENERIC_SWARM_REQUIRE_POSTGRES=false unless Postgres is reachable.
  3. Validate network access and credentials for external integrations.
  4. Review structured logs for connection errors and retries.

**Section sources**
- [backend/app/api/v1/routes/health.py:20-60](file://backend/app/api/v1/routes/health.py#L20-L60)

### Security Incidents and Forensics
- Step-by-step:
  1. Collect all audit logs filtered by action/resource_type relevant to the incident.
  2. Retrieve specific audit entries by ID for detailed context.
  3. Stream run events for affected runs to reconstruct timeline.
  4. Correlate with request IDs and IP addresses from request logs.
  5. Preserve evidence and maintain chain-of-custody for logs and artifacts.

**Section sources**
- [backend/app/services/audit_service.py:4-14](file://backend/app/services/audit_service.py#L4-L14)
- [backend/app/core/logging.py:11-31](file://backend/app/core/logging.py#L11-L31)

### Diagnostic Tools and Techniques
- Health checks:
  - GET /health/live for liveness.
  - GET /health/ready for readiness and dependency status.
  - GET /health/metrics for authenticated metrics snapshot.
- Metrics:
  - Use metrics snapshot to analyze request_count, error_count, average_duration_ms, and per-route breakdowns.
- Logs:
  - Parse JSON logs for request_id, method, path, status_code, duration_ms, client_ip.
  - Filter by error messages and stack traces for exceptions.

**Section sources**
- [backend/app/api/v1/routes/health.py:10-67](file://backend/app/api/v1/routes/health.py#L10-L67)
- [backend/app/core/metrics.py:27-45](file://backend/app/core/metrics.py#L27-L45)
- [backend/app/core/logging.py:11-46](file://backend/app/core/logging.py#L11-L46)

### Performance Profiling and Resource Utilization
- Use metrics endpoint to identify hotspots and regressions.
- Correlate high average_duration_ms with specific routes and times.
- Monitor error_count trends to detect cascading failures.
- Prefer Postgres-backed runtime for reduced I/O contention and better concurrency.

**Section sources**
- [backend/app/api/v1/routes/health.py:63-67](file://backend/app/api/v1/routes/health.py#L63-L67)
- [backend/app/core/metrics.py:15-45](file://backend/app/core/metrics.py#L15-L45)

### Memory Leak Detection
- Indicators:
  - Gradual increase in process memory without corresponding metric spikes.
  - Elevated GC pressure or frequent long pauses.
- Actions:
  - Profile allocations during representative workloads.
  - Inspect long-lived collections in runtime store and ensure proper cleanup.
  - Validate that large payloads are streamed or paginated where possible.

[No sources needed since this section provides general guidance]

### Operational Runbooks
- Quick verification commands and checks are available in the repository’s troubleshooting guide.
- Use the provided scripts and validation commands to ensure prerequisites and business seeds are correctly initialized.

**Section sources**
- [docs/troubleshooting.md:1-12](file://docs/troubleshooting.md#L1-L12)
- [docs/troubleshooting.md:41-48](file://docs/troubleshooting.md#L41-L48)

## Conclusion
By leveraging structured logs, metrics, health endpoints, and audit services, operators can rapidly diagnose API failures, workflow execution issues, integration problems, and security incidents. Consistent use of request IDs, careful attention to error envelopes, and periodic review of metrics snapshots form the foundation of effective troubleshooting and continuous improvement.