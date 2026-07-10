"""Requirement detail payloads for planning/backend generation."""

from __future__ import annotations

DETAILS: dict[str, dict] = {}


def _d(**kwargs):
    return kwargs


DETAILS["01"] = _d(
    scope_in=[
        "- Backend mission as governed API control plane for structure.md capabilities.",
        "- System boundary: what backend owns vs frontend, agents, external systems.",
        "- Core design principles: API first, secure by default, governance first, human-in-the-loop, audit everything important, workers for long-running work, frontend simplicity.",
        "- Design priority order inherited from structure.md: Safety → Auditability → Correctness → Efficiency → Autonomy.",
    ],
    scope_out=[
        "- Concrete route handlers and schemas (later BE specs).",
        "- Frontend UX layout (frontend.md).",
        "- Domain business corpus content under business/.",
    ],
    stk=[
        ("STK-01-01", "Product / architecture", "Backend enforces architecture priorities and never becomes a thin ungoverned proxy."),
        ("STK-01-02", "Security / compliance", "All agent, workflow, knowledge, and tool access is mediated and auditable."),
        ("STK-01-03", "Frontend consumers", "A stable API control plane with no need to reach databases or LLM providers directly."),
        ("STK-01-04", "Operators", "Backend remains source of truth for permissions, policy, and execution state."),
    ],
    fr=[
        ("FR-01-01", "The backend shall act as the governed control layer for the business operating system described in structure.md."),
        ("FR-01-02", "The backend shall expose system capabilities through versioned APIs for frontend, CLI, automation, and integrations."),
        ("FR-01-03", "If a client attempts to access agents, databases, workflow engines, LLM providers, vector stores, or internal tools without the backend, then the system shall treat that path as unsupported and out of scope."),
        ("FR-01-04", "The backend shall enforce permissions, policy, workflow rules, risk controls, auditability, data access boundaries, and evaluation checks rather than blindly proxying to agents."),
        ("FR-01-05", "When a design trade-off exists between safety and autonomy, the backend shall prefer the safer option."),
        ("FR-01-06", "When a design trade-off exists between auditability and efficiency, the backend shall prefer auditability."),
        ("FR-01-07", "When a design trade-off exists between correctness and efficiency, the backend shall prefer correctness."),
        ("FR-01-08", "The backend shall be API-first so that frontend depends only on the backend API contract."),
        ("FR-01-09", "When an endpoint is not explicitly public, the backend shall require authentication."),
        ("FR-01-10", "When a high-risk or irreversible action is requested, the backend shall apply governance and human-in-the-loop rules before completion."),
        ("FR-01-11", "When an important state-changing action occurs, the backend shall write an audit event."),
        ("FR-01-12", "When work is long-running, the backend shall support asynchronous execution patterns (queue/worker or equivalent) rather than blocking the API forever."),
        ("FR-01-13", "The backend shall keep business intelligence, control, security, and trust enforcement on the server so the frontend remains a presentation and interaction layer."),
        ("FR-01-14", "The backend shall support authentication, RBAC, agent orchestration requests, workflow execution, run tracking, governance gates, memory and knowledge retrieval, audit logging, evaluation, process intelligence, evolution sandbox controls, self-improvement loops, streaming updates, and extensible integrations as capability domains."),
    ],
    perf=[
        ("NFR-01-01", "Charter and principle checks shall be enforceable by deterministic policy and code review gates without requiring online LLM calls."),
        ("NFR-01-02", "API contract changes that break frontend consumers shall require explicit versioning decisions."),
    ],
    sec=[
        ("NFR-01-03", "The backend shall treat design principles as non-bypassable by prompt text alone."),
        ("NFR-01-04", "If a feature would allow unattended direct production DNA mutation, then the backend shall reject that feature as out of charter."),
    ],
    ac=[
        ("AC-01-01", "backend.md and this spec state backend is the sole control plane for agents/workflows/tools access."),
        ("AC-01-02", "All downstream planning/backend/* specs reference BE-01 priority order."),
        ("AC-01-03", "System boundary lists owned capabilities and forbidden thin-proxy behaviour."),
        ("AC-01-04", "Evolution and DNA safety specs explicitly forbid host self-rewrite and silent production DNA mutation."),
    ],
    tv=[
        ("TV-01-01", "Document review: map each principle in §6 to at least one later BE FR.", "Review"),
        ("TV-01-02", "Negative: specify auto-promote-to-production without gates → reject against charter.", "Spec gate"),
        ("TV-01-03", "Traceability matrix BE-01 FR IDs → later BE FR IDs.", "Traceability"),
    ],
    trace=[
        ("backend.md §1–2 Purpose/Objective", "FR-01-01 … FR-01-02, FR-01-14"),
        ("backend.md §4 System Boundary", "FR-01-03 … FR-01-04"),
        ("backend.md §6 Core Design Principles", "FR-01-08 … FR-01-13"),
        ("structure.md design priorities", "FR-01-05 … FR-01-07"),
    ],
)

DETAILS["02"] = _d(
    scope_in=[
        "- Recommended technology stack (FastAPI, Python, PostgreSQL primary, optional Redis/queue/vector/object storage).",
        "- Project layout under backend/ (app layers: api, core, domain, infrastructure).",
        "- Local development without Docker as a hard requirement.",
        "- Layered maintainability: routes → services → domain → infrastructure adapters.",
    ],
    scope_out=[
        "- Final vendor lock to a specific queue or vector product.",
        "- Frontend package layout.",
        "- Production multi-region deployment topology details beyond stack recommendations.",
    ],
    stk=[
        ("STK-02-01", "Engineers", "Reproducible scaffold and clear module boundaries."),
        ("STK-02-02", "Ops", "Runnable locally with documented env vars."),
        ("STK-02-03", "Architects", "Stack choices remain replaceable behind adapters."),
    ],
    fr=[
        ("FR-02-01", "The backend shall be implemented primarily with FastAPI and Python unless an approved alternative preserves the same architecture boundaries."),
        ("FR-02-02", "The backend shall use PostgreSQL as the primary durable control-plane database when DATABASE_URL is configured."),
        ("FR-02-03", "Where vector search is required, the backend shall support a pluggable vector provider (including optional pgvector)."),
        ("FR-02-04", "Where asynchronous work is required, the backend shall support a worker or in-process execution path without mandating Docker for local product-bar operation."),
        ("FR-02-05", "The backend shall generate OpenAPI documentation from the FastAPI application."),
        ("FR-02-06", "The backend shall organize code into API, core, domain, and infrastructure layers as described in backend.md §9."),
        ("FR-02-07", "When infrastructure dependencies are optional (Redis, object storage, external LLM), the backend shall degrade or feature-flag rather than hard-fail unrelated core routes when those deps are absent in local mode."),
        ("FR-02-08", "The backend shall document required and optional environment variables including APP_ENV, DATABASE_URL, JWT secrets, CORS, and feature flags."),
        ("FR-02-09", "The backend shall keep JSON file snapshots as backup/seed only when Postgres is the primary store (not dual-write source of truth)."),
        ("FR-02-10", "The backend shall expose a clear entrypoint (e.g. app.main:app) for uvicorn or equivalent ASGI server."),
    ],
    perf=[
        ("NFR-02-01", "Cold start of the API process for local development shall complete within a developer-acceptable window (target under 30 seconds excluding dependency installs)."),
        ("NFR-02-02", "Module import graph shall avoid circular dependencies between domain and infrastructure."),
    ],
    sec=[
        ("NFR-02-03", "Secrets shall be loaded from environment or secret stores and shall not be hardcoded in source."),
        ("NFR-02-04", "CORS allowed origins shall be explicit configuration, not unrestricted wildcard in production profiles."),
    ],
    ac=[
        ("AC-02-01", "backend/ tree matches layered layout (api/core/domain/infrastructure)."),
        ("AC-02-02", "OpenAPI schema is exportable from running app."),
        ("AC-02-03", ".env.example or docs list DATABASE_URL and JWT-related settings."),
        ("AC-02-04", "README documents local uvicorn start without Docker."),
    ],
    tv=[
        ("TV-02-01", "Import/smoke: app.main loads.", "Automated"),
        ("TV-02-02", "OpenAPI /docs or export path returns schema.", "Automated"),
        ("TV-02-03", "Review: no secrets committed in scaffold files.", "Review"),
    ],
    trace=[
        ("backend.md §3 Stack", "FR-02-01 … FR-02-05"),
        ("backend.md §9 Folder Structure", "FR-02-06, FR-02-10"),
        ("backend.md §18.3 Environment Variables", "FR-02-08"),
        ("backend.md §24.3 Control plane", "FR-02-02, FR-02-09"),
    ],
)

DETAILS["03"] = _d(
    scope_in=[
        "- Durable persistence for runtime state (organizations, users, agents, workflows, runs, approvals, knowledge, memory, evaluations, audit, evolution variants as applicable).",
        "- Postgres runtime_state JSONB primary model as as-built control plane.",
        "- JSON backup/seed and migrate-from-JSON on empty DB behaviour.",
        "- Core entity relationships from backend.md §10.",
    ],
    scope_out=[
        "- Domain business rules for each entity (later BE specs).",
        "- Full multi-region replication topology.",
        "- Commercial Neo4j mesh as primary store.",
    ],
    stk=[
        ("STK-03-01", "Operators", "State survives process restarts."),
        ("STK-03-02", "Engineers", "Single primary store with clear backup path."),
        ("STK-03-03", "Auditors", "Durable audit and run history."),
    ],
    fr=[
        ("FR-03-01", "When DATABASE_URL is set, the backend shall persist control-plane state primarily in PostgreSQL."),
        ("FR-03-02", "The backend shall store runtime control state in a durable schema including JSONB runtime_state (or equivalent) capable of holding versioned domain objects."),
        ("FR-03-03", "When the database is empty and a JSON seed/backup exists, the backend shall support migrate-from-JSON to initialize state."),
        ("FR-03-04", "While Postgres is primary, the backend shall treat JSON files as backup/seed only and not as the authoritative write path for live mutations."),
        ("FR-03-05", "The backend data model shall include core entities: Organization, User, Agent, Workflow, WorkflowVersion, WorkflowRun, WorkflowRunStep, ApprovalRequest, KnowledgeDocument, KnowledgeChunk, MemoryItem, EvaluationRun, AuditLog."),
        ("FR-03-06", "When multi-tenancy is not fully enabled, the backend shall still include organization_id or tenant_id on tenant-scoped entities."),
        ("FR-03-07", "When a write succeeds, subsequent reads from another request shall observe the committed state after transaction completion."),
        ("FR-03-08", "If the database is unavailable, then health/ready checks shall report degraded or not-ready status."),
        ("FR-03-09", "The backend shall support snapshot backup of runtime state for disaster recovery and local portability."),
        ("FR-03-10", "The backend shall isolate tenant data by organization_id on queries for multi-tenant-ready entities."),
    ],
    perf=[
        ("NFR-03-01", "Primary key lookups for run/agent/workflow by ID shall complete within 100ms p95 under local load excluding network to remote DB."),
        ("NFR-03-02", "Migrations or schema bootstrap shall be documented and repeatable."),
    ],
    sec=[
        ("NFR-03-03", "Database credentials shall not appear in logs."),
        ("NFR-03-04", "The backend shall use parameterized queries / ORM bindings to prevent SQL injection."),
    ],
    ac=[
        ("AC-03-01", "GET health/ready reports database postgres when DATABASE_URL configured."),
        ("AC-03-02", "Restarting API retains previously created agents/workflows/runs."),
        ("AC-03-03", "Empty DB can be seeded from JSON backup path when present."),
        ("AC-03-04", "Tenant-scoped entities include organization_id field."),
    ],
    tv=[
        ("TV-03-01", "Unit/integration: create entity, restart store session, read back.", "Automated"),
        ("TV-03-02", "Ready endpoint with/without DB.", "Automated"),
        ("TV-03-03", "Seed/migrate-from-JSON path on empty DB.", "Automated"),
    ],
    trace=[
        ("backend.md §10 Data Model", "FR-03-05 … FR-03-06"),
        ("backend.md §24.3 Control plane", "FR-03-01 … FR-03-04"),
        ("backend.md §17.2 Health", "FR-03-08"),
    ],
)

DETAILS["04"] = _d(
    scope_in=[
        "- API versioning under /api/v1.",
        "- Standard success and error response envelopes.",
        "- Common error codes and request_id correlation.",
        "- Consistent pagination/meta patterns where applicable.",
    ],
    scope_out=["- Domain endpoint semantics (later specs).", "- GraphQL alternative API."],
    stk=[
        ("STK-04-01", "Frontend engineers", "Predictable envelopes and typed OpenAPI."),
        ("STK-04-02", "Support", "request_id on errors for triage."),
        ("STK-04-03", "API consumers", "Stable versioning strategy."),
    ],
    fr=[
        ("FR-04-01", "The backend shall version public HTTP APIs under a versioned prefix such as /api/v1."),
        ("FR-04-02", "When a successful response is returned for resource APIs, the backend shall use a consistent envelope including data and meta where specified in backend.md §11.2."),
        ("FR-04-03", "When an error occurs, the backend shall return a structured error envelope including error code, message, and request_id."),
        ("FR-04-04", "The backend shall assign a request_id to each handled request and propagate it to logs and error responses."),
        ("FR-04-05", "The backend shall document common error codes including authentication, authorization, validation, not found, conflict, rate limit, and internal errors."),
        ("FR-04-06", "When request body validation fails, the backend shall return a 422-class validation error with field-level detail where available."),
        ("FR-04-07", "When an unhandled exception occurs, the backend shall return a safe error envelope without leaking secrets or stack traces to clients in production profiles."),
        ("FR-04-08", "The backend shall publish OpenAPI that matches implemented routes and schemas."),
        ("FR-04-09", "When listing resources, the backend shall support consistent pagination parameters or documented defaults."),
        ("FR-04-10", "Breaking public contract changes shall require a new API version or explicit deprecation notice."),
    ],
    perf=[
        ("NFR-04-01", "Envelope serialization overhead shall be negligible relative to handler work."),
        ("NFR-04-02", "OpenAPI generation shall complete as part of normal app startup or export command."),
    ],
    sec=[
        ("NFR-04-03", "Error messages shall not include secrets, raw tokens, or password hashes."),
        ("NFR-04-04", "request_id alone shall not authorize access to resources."),
    ],
    ac=[
        ("AC-04-01", "Sample error responses include request_id."),
        ("AC-04-02", "OpenAPI lists /api/v1 routes."),
        ("AC-04-03", "Invalid body yields validation error envelope."),
        ("AC-04-04", "Production error path does not return stack traces."),
    ],
    tv=[
        ("TV-04-01", "Unit: error handler formats envelope.", "Automated"),
        ("TV-04-02", "Contract: OpenAPI export includes version prefix.", "Automated"),
        ("TV-04-03", "Negative: 401/403/422 sample routes.", "Automated"),
    ],
    trace=[
        ("backend.md §6.1 API First", "FR-04-01, FR-04-08"),
        ("backend.md §11.1–11.3", "FR-04-01 … FR-04-07"),
    ],
)

# Remaining specs loaded from companion part files for maintainability.
from _gen_backend_reqs_data_part2 import DETAILS as _P2  # noqa: E402
from _gen_backend_reqs_data_part3 import DETAILS as _P3  # noqa: E402

DETAILS.update(_P2)
DETAILS.update(_P3)
