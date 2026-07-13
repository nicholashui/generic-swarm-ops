# backend.md

# Backend API Server Requirements, Design, and Implementation Plan

**Architecture source of truth:** `structure.md` (implementation mapping §12)  
**Status:** Product bar mark ~100 — as-built under `backend/`  
**Last Updated:** 2026-07-10  
**Related:** `frontend.md` · `backend_hk.md` · `backend/README.md` · `status.md` · `planning/structure/` · `planning/backend/` · `planning/gap_analysis_for_structure.md` · `planning/gap_analysis_for_backend.md` · `docs/domain-packs.md`

**Domain Pack (Wave 0):** Inventory gate `scripts/business/inventory_check.py` + schema tests for domain-manifest/agent-spec/learning-log. Register stub is CLI-only (`register_domain.py`); full `/domains` + ALC runtime is Wave 1. Video pack data lives under `business/video/` — not hard-coded in the control plane.

This document is the **backend requirements, design, and implementation plan**. It refines how the architecture in `structure.md` becomes an API control plane. Executable **backend** sub-functional requirements live under `planning/backend/nn_*/requirements.md` (sequential order 01–24). Architecture SDD specs live under `planning/structure/`; **as-built realization and non-goals** are recorded in **§24** below and in `structure.md` §11.1 / §12. Those notes refine this document; they do not replace the architecture priorities: **Safety → Auditability → Correctness → Efficiency → Autonomy.**

## 1. Purpose

The backend API server is the governed control layer for the business operating system described in `structure.md`.

Its purpose is to expose the system’s internal capabilities through secure APIs so that a frontend application, admin console, CLI, automation tool, or external integration can safely interact with agents, workflows, knowledge, memory, governance, evaluations, audit logs, process intelligence, evolution sandbox controls, and self-improvement loops.

The frontend must not directly access agents, databases, workflow engines, LLM providers, vector stores, or internal tools. All access must go through the backend API server.

In short:

```text
Frontend = user experience layer
Backend API = governed intelligence and control layer
Agents = specialized workers
Workflows = structured business execution paths
Governance = risk and approval control
Audit = trust and traceability layer
```

---

## 2. Primary Objective

Build a backend server that encapsulates the full functionality of the system architecture and exposes it through versioned APIs.

The backend should support:

- secure authentication
- role-based access control
- agent orchestration
- workflow execution
- workflow run tracking
- governance approval gates
- memory and knowledge retrieval
- audit logging
- evaluation and quality checks
- process intelligence APIs
- evolution sandbox APIs (propose → evaluate → canary → promote / rollback)
- self-improvement APIs (reflect, lessons, auto-propose, skill sandbox, loop runner)
- production Workflow DNA safety checks before activate / production_ready
- background workers
- streaming updates to the frontend
- extensible integrations

---

## 3. Recommended Technology Stack

This document recommends the following stack:

```text
Backend Framework: FastAPI
Language: Python
Database: PostgreSQL (primary control-plane store; as-built: runtime_state JSONB)
Vector Search: pgvector (optional), Qdrant, Weaviate, or Pinecone
Queue: Redis + Celery/RQ/Arq, or Temporal for advanced workflows (as-built: in-process run engine)
Cache: Redis (optional)
Object Storage: S3-compatible storage (optional for document blobs)
LLM Provider Layer: Provider-agnostic abstraction (optional critic / generation)
Auth: JWT / OAuth2 / SSO-ready
API Style: REST first, WebSocket/SSE for streaming
Documentation: OpenAPI generated from FastAPI
Containerization: No Docker required for local product bar
Deployment: No Docker required for local product bar
Persistence note: JSON file snapshot = backup/seed only when Postgres is configured
```

Alternative backend stacks are acceptable, such as Node.js with NestJS, but the architecture should remain the same.

---

## 4. System Boundary

The backend API server owns and controls:

```text
- API access
- user authentication
- authorization
- agent execution requests
- workflow execution requests
- governance checks
- approval gates
- audit events
- knowledge access
- memory access
- process intelligence
- evaluations
- background jobs
- integrations
```

The backend API server must not be a thin proxy that blindly forwards requests to agents.

Instead, it must enforce:

```text
- permissions
- policy
- workflow rules
- risk controls
- auditability
- data access boundaries
- evaluation checks
```

---

## 5. High-Level Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                    Frontend Application                 │
│                                                         │
│  - Dashboard                                            │
│  - Workflow runner                                      │
│  - Agent activity view                                  │
│  - Approval console                                     │
│  - Knowledge browser                                    │
│  - Audit log viewer                                     │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ REST / SSE / WebSocket
                        v
┌─────────────────────────────────────────────────────────┐
│                  Backend API Server                     │
│                                                         │
│  - Auth                                                 │
│  - RBAC / ABAC                                          │
│  - API validation                                       │
│  - Workflow API                                         │
│  - Agent API                                            │
│  - Governance API                                       │
│  - Knowledge API                                        │
│  - Memory API                                           │
│  - Evaluation API                                       │
│  - Audit API                                            │
│  - Process Intelligence API                             │
└───────────────────────┬─────────────────────────────────┘
                        │
                        v
┌─────────────────────────────────────────────────────────┐
│                    Service Layer                        │
│                                                         │
│  - AgentService                                         │
│  - WorkflowService                                      │
│  - GovernanceService                                    │
│  - ApprovalService                                      │
│  - KnowledgeService                                     │
│  - MemoryService                                        │
│  - EvaluationService                                    │
│  - AuditService                                         │
│  - ProcessService                                       │
└───────────────────────┬─────────────────────────────────┘
                        │
                        v
┌─────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                   │
│                                                         │
│  - PostgreSQL                                           │
│  - Vector DB                                            │
│  - Redis                                                │
│  - Queue / Workers                                      │
│  - Object Storage                                       │
│  - LLM Providers                                        │
│  - External Integrations                                │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Core Design Principles

## 6.1 API First

All platform functionality should be accessible through documented APIs.

The frontend should depend only on the backend API contract, not on internal implementation details.

---

## 6.2 Secure by Default

Every endpoint must require authentication unless explicitly marked public.

Every sensitive operation must check authorization.

Every workflow execution must be auditable.

---

## 6.3 Governance First

The backend must decide whether an action is allowed before an agent or workflow executes.

Governance checks should include:

```text
- user permissions
- workflow permissions
- data access permissions
- risk level
- approval requirement
- tool access permissions
- policy compliance
```

---

## 6.4 Human-in-the-Loop

High-risk actions must pause and request human approval before execution.

Examples:

```text
- sending emails externally
- modifying customer records
- deleting data
- publishing content
- approving financial actions
- changing workflow definitions
- changing governance policies
```

---

## 6.5 Audit Everything Important

Every important action must generate an audit event.

Audit logs should be append-only where possible.

---

## 6.6 Workers for Long-Running Tasks

Agent workflows must not run fully inside normal API request threads.

Instead:

```text
Frontend -> Backend API -> Queue -> Worker -> Database -> Stream updates to frontend
```

---

## 6.7 Frontend Simplicity

The frontend should only need to know:

```text
- what APIs exist
- what input is required
- what status is returned
- where to stream progress
- where to fetch results
```

The frontend should not know internal agent routing, LLM provider logic, memory retrieval internals, or governance policy details.

---

# 7. Functional Requirements

## 7.1 Authentication

The backend must support authenticated users.

Minimum requirements:

```text
- user registration or admin-created users
- login
- logout
- token refresh
- password reset if password auth is used
- API key support for machine clients
- optional SSO/OAuth support
```

Recommended authentication methods:

```text
- JWT access tokens
- refresh tokens
- API keys for service integrations
- OAuth2/OIDC compatibility
```

---

## 7.2 Authorization

The backend must support role-based access control.

Recommended roles:

```text
Owner
Admin
Manager
Operator
Reviewer
Viewer
ServiceAccount
```

Example permission groups:

```text
agents:read
agents:create
agents:update
agents:delete
workflows:read
workflows:create
workflows:update
workflows:run
workflow_runs:read
workflow_runs:cancel
knowledge:read
knowledge:write
memory:read
memory:write
governance:read
governance:update
approvals:read
approvals:approve
approvals:reject
audit:read
evaluations:read
settings:update
```

The authorization system should support future ABAC rules such as:

```text
user.department == resource.department
user.organization_id == resource.organization_id
workflow.risk_level <= user.max_risk_level
```

---

## 7.3 User and Organization Management

The backend should support:

```text
- organizations
- users
- teams
- roles
- permissions
- invitations
- service accounts
- API keys
```

If the system is initially single-tenant, still include `organization_id` or `tenant_id` in the database design to make future multi-tenancy easier.

---

## 7.4 Agent Registry

The backend must maintain a registry of available agents.

Each agent should define:

```text
- agent ID
- name
- description
- version
- owner
- department
- allowed tools
- allowed memory scopes
- allowed workflow types
- risk level
- input schema
- output schema
- runtime configuration
- status
```

Agent statuses:

```text
draft
active
disabled
archived
```

The frontend should be able to list agents, inspect agent metadata, and view agent activity.

---

## 7.5 Tool Registry

Agents may use tools, but only through backend-controlled permissions.

Each tool should define:

```text
- tool ID
- name
- description
- category
- input schema
- output schema
- risk level
- required permissions
- approval requirement
- timeout
- retry policy
- enabled/disabled status
```

Tool categories may include:

```text
database
email
calendar
crm
file
web
internal_api
external_api
llm
code_execution
human_approval
```

High-risk tools must require explicit governance rules.

---

## 7.6 Workflow Management

The backend must support workflow definitions.

A workflow represents a structured business process that may involve:

```text
- one or more agents
- multiple steps
- conditions
- approvals
- memory retrieval
- tool execution
- evaluation checks
- final output generation
```

Workflow metadata should include:

```text
- workflow ID
- name
- description
- version
- owner
- department
- risk level
- input schema
- output schema
- steps
- governance policy
- evaluation policy
- status
```

Workflow statuses:

```text
draft
active
disabled
archived
```

---

## 7.7 Workflow Run Management

Every execution of a workflow must create a `workflow_run`.

Workflow run statuses:

```text
queued
running
waiting_for_approval
paused
completed
failed
cancelled
expired
```

Each workflow run should store:

```text
- workflow_run ID
- workflow ID
- workflow version
- requested by user
- organization ID
- input
- status
- current step
- output
- error
- timestamps
- token/cost usage
- approval state
- evaluation results
```

The frontend must be able to:

```text
- start a workflow run
- view run status
- view run steps
- cancel a run
- retry a failed run if allowed
- stream progress
- view final output
```

---

## 7.8 Workflow Step Tracking

Each workflow run should contain step records.

Step statuses:

```text
pending
running
waiting_for_approval
completed
failed
skipped
cancelled
```

Each step should store:

```text
- step ID
- workflow_run ID
- step name
- step type
- agent ID if applicable
- tool ID if applicable
- input
- output
- error
- started_at
- completed_at
- duration
- retry_count
```

---

## 7.9 Governance and Approval System

The backend must include a governance layer.

The governance system decides:

```text
- whether a workflow can run
- whether a step can execute
- whether a tool can be used
- whether data can be accessed
- whether human approval is required
- whether output can be released
```

Approval request statuses:

```text
pending
approved
rejected
expired
cancelled
```

Approval requests should store:

```text
- approval ID
- workflow_run ID
- step ID
- requested action
- risk level
- requested by
- assigned reviewer
- decision
- decision reason
- created_at
- decided_at
```

---

## 7.10 Knowledge Base

The backend must expose controlled access to knowledge.

Knowledge sources may include:

```text
- uploaded documents
- markdown files
- PDFs
- internal policies
- process documentation
- database records
- support articles
- SOPs
- meeting notes
```

Knowledge features:

```text
- upload document
- index document
- chunk document
- embed chunks
- search documents
- retrieve document metadata
- delete or archive documents
- enforce ACL permissions
```

Document statuses:

```text
uploaded
processing
indexed
failed
archived
deleted
```

---

## 7.11 Memory System

The backend must manage agent and workflow memory.

Memory types:

```text
short_term
long_term
user_memory
team_memory
department_memory
organization_memory
workflow_memory
agent_memory
```

Memory must have access control.

Example rule:

```text
Sales Agent can access sales memory.
Finance Agent can access finance memory.
HR Agent can access HR memory.
General agents cannot access restricted department memory.
```

Memory entries should include:

```text
- memory ID
- scope
- owner
- organization ID
- department
- content
- metadata
- embedding reference
- sensitivity level
- expiration date
- created_at
```

---

## 7.12 Evaluation System

The backend should evaluate important outputs before returning or releasing them.

Evaluation types:

```text
- schema validation
- business rule validation
- policy compliance
- hallucination risk check
- completeness check
- formatting check
- safety check
- cost check
- human review
```

Evaluation result statuses:

```text
passed
failed
warning
requires_review
```

Evaluation results should be linked to:

```text
- workflow run
- workflow step
- agent output
- final output
```

---

## 7.13 Audit Logging

The backend must generate audit logs for important actions.

Audit events should include:

```text
- user login
- workflow created
- workflow updated
- workflow run started
- workflow run completed
- workflow run failed
- approval requested
- approval approved
- approval rejected
- knowledge uploaded
- knowledge deleted
- memory accessed
- memory updated
- governance rule changed
- agent tool used
- API key created
- permission changed
```

Audit log fields:

```text
- audit ID
- organization ID
- actor user ID
- actor type
- action
- resource type
- resource ID
- request ID
- IP address
- user agent
- before state
- after state
- metadata
- status
- created_at
```

---

## 7.14 Process Intelligence

The backend should expose APIs for process intelligence.

Process intelligence can include:

```text
- workflow performance analytics
- bottleneck detection
- failure patterns
- average duration
- approval delays
- agent performance
- cost by workflow
- cost by department
- task success rate
- automation opportunities
```

Initial process APIs may simply aggregate workflow run data.

As-built also writes process-intelligence **disk artifacts** under `business/process-intelligence/` (services + artifacts, not five independent long-running LLM PI agents). See `structure.md` §12.3.

---

## 7.15 Evolution Sandbox APIs

The backend must expose evolution controls that enforce **sandbox-only** mutation of production Workflow DNA (`structure.md` §5 / §12.3):

```text
- list / propose evolution variants (sandbox_only)
- evaluate variants against corpus / fitness
- canary promote to limited scope
- full promote only after gates
- rollback
- fitness / population archive
```

Evolution Manager behaviour is API-enforced: never rewrite host application code; never silently replace production DNA.

---

## 7.16 Self-Improvement APIs

Aligned with reflective / GEPA-style loops in `structure.md`:

```text
- reflect on a completed or failed run
- lesson library list / score
- auto-propose sandbox variant from lessons
- optional LLM critic (feature-flagged)
- skill sandbox (write under _sandbox, explicit promote)
- loop DNA runner start / status
```

---

## 7.17 Production DNA Safety

Before a workflow version is activated or marked production-ready, the backend must run structure-aligned validators (risk tiers, human gates, rollback, provenance fields) via `business:validate` and runtime production DNA checks (`structure_validators`). Rejections should be learnable (e.g. recorded as lessons) without mutating production DNA.

---

## 7.18 Streaming Updates

The backend should support real-time progress updates.

Recommended options:

```text
Server-Sent Events for simple one-way updates
WebSocket for two-way interactive agent sessions
```

For the first version, Server-Sent Events is usually simpler.

Streaming event types:

```text
run.started
run.status_changed
step.started
step.completed
step.failed
approval.requested
approval.approved
approval.rejected
evaluation.completed
run.completed
run.failed
log.message
```

Example stream event:

```json
{
  "event": "step.completed",
  "workflow_run_id": "run_123",
  "step_id": "step_456",
  "status": "completed",
  "message": "Knowledge retrieval completed",
  "timestamp": "2026-07-07T12:00:00Z"
}
```

---

# 8. Non-Functional Requirements

## 8.1 Security

The backend must:

```text
- require authentication for protected routes
- enforce authorization on every protected resource
- validate all request bodies
- sanitize file uploads
- protect secrets
- rate limit sensitive endpoints
- log security-relevant events
- avoid leaking internal errors
- encrypt sensitive data where required
- protect against prompt injection in agent workflows
```

---

## 8.2 Reliability

The backend should:

```text
- use background workers for long tasks
- retry recoverable failures
- use idempotency keys for workflow creation
- persist workflow state
- handle worker crashes
- allow workflow recovery where possible
- expose health checks
```

---

## 8.3 Scalability

The backend should be designed so these components can scale independently:

```text
- API server
- worker processes
- database
- vector store
- cache
- queue
```

---

## 8.4 Observability

The backend must provide:

```text
- structured logs
- request IDs
- audit logs
- metrics
- traces if possible
- workflow run history
- worker job logs
- error reports
```

Important metrics:

```text
- API request latency
- workflow run duration
- workflow failure rate
- queue depth
- approval wait time
- LLM token usage
- LLM cost
- database latency
- vector search latency
- active users
```

---

## 8.5 Maintainability

The backend should use layered architecture:

```text
API routes -> Services -> Domain logic -> Infrastructure adapters
```

Routes must stay thin.

Business logic should live in services and domain modules.

External providers should be abstracted behind interfaces.

---

# 9. Recommended Backend Folder Structure

```text
backend/
  app/
    main.py

    api/
      __init__.py
      dependencies.py
      errors.py
      v1/
        __init__.py
        router.py
        routes/
          auth.py
          users.py
          organizations.py
          agents.py
          tools.py
          workflows.py
          workflow_runs.py
          approvals.py
          governance.py
          knowledge.py
          memory.py
          evaluations.py
          audit_logs.py
          processes.py
          settings.py
          health.py

    core/
      __init__.py
      config.py
      security.py
      auth.py
      permissions.py
      logging.py
      errors.py
      pagination.py
      idempotency.py
      rate_limit.py

    domain/
      __init__.py
      agents/
        models.py
        policies.py
        runtime.py
      workflows/
        models.py
        engine.py
        states.py
        policies.py
      governance/
        models.py
        policy_engine.py
        risk.py
      approvals/
        models.py
        service.py
      knowledge/
        models.py
        chunking.py
        retrieval.py
      memory/
        models.py
        scopes.py
        retrieval.py
      evaluations/
        models.py
        evaluators.py
      audit/
        models.py
        events.py
      processes/
        analytics.py

    services/
      __init__.py
      auth_service.py
      user_service.py
      organization_service.py
      agent_service.py
      tool_service.py
      workflow_service.py
      workflow_run_service.py
      governance_service.py
      approval_service.py
      knowledge_service.py
      memory_service.py
      evaluation_service.py
      audit_service.py
      process_service.py
      notification_service.py

    infrastructure/
      __init__.py
      database/
        __init__.py
        session.py
        models.py
        migrations/
      repositories/
        user_repository.py
        agent_repository.py
        workflow_repository.py
        workflow_run_repository.py
        approval_repository.py
        knowledge_repository.py
        memory_repository.py
        audit_repository.py
      vector_store/
        __init__.py
        base.py
        pgvector_store.py
        qdrant_store.py
      object_storage/
        __init__.py
        base.py
        s3_storage.py
        local_storage.py
      queue/
        __init__.py
        broker.py
        tasks.py
      llm/
        __init__.py
        base.py
        openai_provider.py
        mock_provider.py
      integrations/
        __init__.py
        email.py
        crm.py
        calendar.py

    schemas/
      __init__.py
      common.py
      auth.py
      users.py
      organizations.py
      agents.py
      tools.py
      workflows.py
      workflow_runs.py
      approvals.py
      governance.py
      knowledge.py
      memory.py
      evaluations.py
      audit_logs.py
      processes.py

    workers/
      __init__.py
      workflow_worker.py
      knowledge_worker.py
      evaluation_worker.py
      memory_worker.py

    tests/
      unit/
      integration/
      e2e/
      security/
      load/

  scripts/
    seed.py
    create_admin.py
    migrate.py

  pyproject.toml
  README.md
  backend.md
```

---

# 10. Data Model

## 10.1 Core Entities

The system should include these main entities:

```text
Organization
User
Role
Permission
APIKey
Agent
Tool
Workflow
WorkflowVersion
WorkflowRun
WorkflowRunStep
ApprovalRequest
GovernancePolicy
KnowledgeDocument
KnowledgeChunk
MemoryItem
EvaluationRun
AuditLog
ProcessMetric
Notification
```

---

## 10.2 Organization

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| name | String | Yes | Organization name |
| slug | String | Yes | Unique slug |
| status | String | Yes | active, disabled |
| settings | JSON | No | Organization settings |
| created_at | DateTime | Yes | Creation time |
| updated_at | DateTime | Yes | Update time |

---

## 10.3 User

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| organization_id | UUID | Yes | Tenant boundary |
| email | String | Yes | Unique per organization |
| name | String | Yes | Display name |
| password_hash | String | No | Required only for password auth |
| status | String | Yes | active, invited, disabled |
| role_id | UUID | Yes | Primary role |
| department | String | No | Optional department |
| last_login_at | DateTime | No | Last login |
| created_at | DateTime | Yes | Creation time |
| updated_at | DateTime | Yes | Update time |

---

## 10.4 Agent

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| organization_id | UUID | Yes | Tenant boundary |
| name | String | Yes | Agent name |
| description | Text | No | Agent description |
| version | String | Yes | Agent version |
| status | String | Yes | draft, active, disabled, archived |
| owner_user_id | UUID | No | Owner |
| department | String | No | Department scope |
| allowed_tools | JSON | Yes | Tool IDs or permission rules |
| allowed_memory_scopes | JSON | Yes | Memory access rules |
| input_schema | JSON | No | JSON schema |
| output_schema | JSON | No | JSON schema |
| runtime_config | JSON | No | Model, temperature, limits |
| risk_level | String | Yes | low, medium, high, critical |
| created_at | DateTime | Yes | Creation time |
| updated_at | DateTime | Yes | Update time |

---

## 10.5 Workflow

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| organization_id | UUID | Yes | Tenant boundary |
| name | String | Yes | Workflow name |
| description | Text | No | Workflow description |
| status | String | Yes | draft, active, disabled, archived |
| current_version_id | UUID | No | Active version |
| owner_user_id | UUID | No | Owner |
| department | String | No | Department scope |
| risk_level | String | Yes | low, medium, high, critical |
| created_at | DateTime | Yes | Creation time |
| updated_at | DateTime | Yes | Update time |

---

## 10.6 WorkflowVersion

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| workflow_id | UUID | Yes | Parent workflow |
| version | String | Yes | Version label |
| input_schema | JSON | No | Input validation |
| output_schema | JSON | No | Output validation |
| steps | JSON | Yes | Workflow DNA |
| governance_policy | JSON | No | Approval/risk rules |
| evaluation_policy | JSON | No | Output checks |
| created_by_user_id | UUID | Yes | Version creator |
| created_at | DateTime | Yes | Creation time |

---

## 10.7 WorkflowRun

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| organization_id | UUID | Yes | Tenant boundary |
| workflow_id | UUID | Yes | Workflow |
| workflow_version_id | UUID | Yes | Exact version executed |
| requested_by_user_id | UUID | Yes | User who started run |
| status | String | Yes | queued, running, waiting_for_approval, completed, failed, cancelled |
| input | JSON | Yes | Submitted input |
| output | JSON | No | Final output |
| error | JSON | No | Failure info |
| current_step_id | UUID | No | Current step |
| idempotency_key | String | No | Prevent duplicate runs |
| cost_summary | JSON | No | Token/cost usage |
| started_at | DateTime | No | Start time |
| completed_at | DateTime | No | End time |
| created_at | DateTime | Yes | Creation time |
| updated_at | DateTime | Yes | Update time |

---

## 10.8 WorkflowRunStep

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| workflow_run_id | UUID | Yes | Parent run |
| step_key | String | Yes | Step key from workflow definition |
| name | String | Yes | Step name |
| type | String | Yes | agent, tool, approval, evaluation, condition |
| status | String | Yes | pending, running, completed, failed, skipped |
| agent_id | UUID | No | Agent used |
| tool_id | UUID | No | Tool used |
| input | JSON | No | Step input |
| output | JSON | No | Step output |
| error | JSON | No | Step error |
| retry_count | Integer | Yes | Retry count |
| started_at | DateTime | No | Start time |
| completed_at | DateTime | No | End time |
| created_at | DateTime | Yes | Creation time |

---

## 10.9 ApprovalRequest

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| organization_id | UUID | Yes | Tenant boundary |
| workflow_run_id | UUID | Yes | Parent run |
| workflow_run_step_id | UUID | No | Step requiring approval |
| requested_by_user_id | UUID | Yes | Requesting user |
| reviewer_user_id | UUID | No | Assigned reviewer |
| status | String | Yes | pending, approved, rejected, expired, cancelled |
| risk_level | String | Yes | low, medium, high, critical |
| requested_action | JSON | Yes | Action to approve |
| reason | Text | No | Reason approval is needed |
| decision_reason | Text | No | Reviewer notes |
| decided_at | DateTime | No | Decision time |
| created_at | DateTime | Yes | Creation time |

---

## 10.10 KnowledgeDocument

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| organization_id | UUID | Yes | Tenant boundary |
| title | String | Yes | Document title |
| source_type | String | Yes | upload, url, database, manual |
| storage_uri | String | No | Object storage path |
| status | String | Yes | uploaded, processing, indexed, failed, archived |
| sensitivity | String | Yes | public, internal, confidential, restricted |
| acl | JSON | No | Access rules |
| metadata | JSON | No | Document metadata |
| uploaded_by_user_id | UUID | No | Uploader |
| created_at | DateTime | Yes | Creation time |
| updated_at | DateTime | Yes | Update time |

---

## 10.11 KnowledgeChunk

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| document_id | UUID | Yes | Parent document |
| organization_id | UUID | Yes | Tenant boundary |
| chunk_index | Integer | Yes | Order |
| content | Text | Yes | Chunk text |
| embedding_id | String | No | Vector DB reference |
| metadata | JSON | No | Chunk metadata |
| created_at | DateTime | Yes | Creation time |

---

## 10.12 MemoryItem

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| organization_id | UUID | Yes | Tenant boundary |
| scope | String | Yes | user, team, department, organization, agent, workflow |
| owner_id | UUID | No | User/agent/workflow owner |
| department | String | No | Department scope |
| content | Text | Yes | Memory content |
| metadata | JSON | No | Metadata |
| sensitivity | String | Yes | public, internal, confidential, restricted |
| expires_at | DateTime | No | Expiration |
| created_by | UUID | No | Creator |
| created_at | DateTime | Yes | Creation time |

---

## 10.13 EvaluationRun

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| organization_id | UUID | Yes | Tenant boundary |
| workflow_run_id | UUID | No | Parent run |
| workflow_run_step_id | UUID | No | Parent step |
| evaluator_type | String | Yes | schema, policy, llm, human, rule |
| status | String | Yes | passed, failed, warning, requires_review |
| score | Float | No | Numeric score |
| input | JSON | No | Evaluation input |
| output | JSON | No | Evaluation output |
| reason | Text | No | Explanation |
| created_at | DateTime | Yes | Creation time |

---

## 10.14 AuditLog

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| organization_id | UUID | Yes | Tenant boundary |
| actor_user_id | UUID | No | User actor |
| actor_type | String | Yes | user, agent, service_account, system |
| action | String | Yes | Action name |
| resource_type | String | Yes | Resource type |
| resource_id | UUID | No | Resource ID |
| request_id | String | No | Request correlation |
| ip_address | String | No | Client IP |
| user_agent | String | No | Client user agent |
| before_state | JSON | No | Before change |
| after_state | JSON | No | After change |
| metadata | JSON | No | Extra metadata |
| status | String | Yes | success, failure |
| created_at | DateTime | Yes | Creation time |

---

# 11. API Design

## 11.1 API Versioning

All public APIs must be versioned.

```text
/api/v1/...
```

Future breaking changes should use:

```text
/api/v2/...
```

---

## 11.2 Response Format

Successful response example:

```json
{
  "data": {
    "id": "example_id"
  },
  "meta": {
    "request_id": "req_123"
  }
}
```

List response example:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 25,
    "total": 100
  },
  "meta": {
    "request_id": "req_123"
  }
}
```

Error response example:

```json
{
  "error": {
    "code": "permission_denied",
    "message": "You do not have permission to run this workflow.",
    "details": {}
  },
  "meta": {
    "request_id": "req_123"
  }
}
```

---

## 11.3 Common Error Codes

```text
bad_request
unauthorized
permission_denied
not_found
validation_error
conflict
rate_limited
approval_required
workflow_not_active
workflow_run_failed
agent_not_available
tool_not_allowed
knowledge_access_denied
memory_access_denied
evaluation_failed
internal_error
```

---

## 11.4 Authentication Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/auth/login` | Login |
| POST | `/api/v1/auth/logout` | Logout |
| POST | `/api/v1/auth/refresh` | Refresh token |
| GET | `/api/v1/auth/me` | Current user |
| POST | `/api/v1/auth/api-keys` | Create API key |
| GET | `/api/v1/auth/api-keys` | List API keys |
| DELETE | `/api/v1/auth/api-keys/{key_id}` | Revoke API key |

---

## 11.5 Agent Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/agents` | List agents |
| POST | `/api/v1/agents` | Create agent |
| GET | `/api/v1/agents/{agent_id}` | Get agent |
| PATCH | `/api/v1/agents/{agent_id}` | Update agent |
| DELETE | `/api/v1/agents/{agent_id}` | Archive agent |
| GET | `/api/v1/agents/{agent_id}/activity` | Agent activity |
| GET | `/api/v1/agents/{agent_id}/tools` | Allowed tools |

---

## 11.6 Workflow Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/workflows` | List workflows |
| POST | `/api/v1/workflows` | Create workflow |
| GET | `/api/v1/workflows/{workflow_id}` | Get workflow |
| PATCH | `/api/v1/workflows/{workflow_id}` | Update workflow |
| DELETE | `/api/v1/workflows/{workflow_id}` | Archive workflow |
| POST | `/api/v1/workflows/{workflow_id}/versions` | Create version |
| GET | `/api/v1/workflows/{workflow_id}/versions` | List versions |
| POST | `/api/v1/workflows/{workflow_id}/activate` | Activate workflow |
| POST | `/api/v1/workflows/{workflow_id}/disable` | Disable workflow |

---

## 11.7 Workflow Run Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/workflows/{workflow_id}/runs` | Start workflow run |
| GET | `/api/v1/workflow-runs` | List workflow runs |
| GET | `/api/v1/workflow-runs/{run_id}` | Get run |
| GET | `/api/v1/workflow-runs/{run_id}/steps` | Get run steps |
| POST | `/api/v1/workflow-runs/{run_id}/cancel` | Cancel run |
| POST | `/api/v1/workflow-runs/{run_id}/retry` | Retry run |
| GET | `/api/v1/workflow-runs/{run_id}/stream` | Stream run events |

Example start workflow request:

```json
{
  "input": {
    "customer_id": "cust_123",
    "task": "analyze onboarding process"
  }
}
```

Example start workflow response:

```json
{
  "data": {
    "workflow_run_id": "run_123",
    "status": "queued"
  },
  "meta": {
    "request_id": "req_123"
  }
}
```

---

## 11.8 Approval Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/approvals` | List approval requests |
| GET | `/api/v1/approvals/{approval_id}` | Get approval request |
| POST | `/api/v1/approvals/{approval_id}/approve` | Approve request |
| POST | `/api/v1/approvals/{approval_id}/reject` | Reject request |
| POST | `/api/v1/approvals/{approval_id}/reassign` | Reassign reviewer |

Approve request example:

```json
{
  "decision_reason": "Approved because the output was reviewed and is safe to send."
}
```

Reject request example:

```json
{
  "decision_reason": "Rejected because customer data appears incomplete."
}
```

---

## 11.9 Knowledge Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/knowledge/documents` | List documents |
| POST | `/api/v1/knowledge/documents` | Upload/create document |
| GET | `/api/v1/knowledge/documents/{document_id}` | Get document |
| DELETE | `/api/v1/knowledge/documents/{document_id}` | Archive/delete document |
| POST | `/api/v1/knowledge/documents/{document_id}/index` | Start indexing |
| POST | `/api/v1/knowledge/search` | Search knowledge |

Knowledge search example:

```json
{
  "query": "customer onboarding process",
  "filters": {
    "department": "sales",
    "sensitivity": "internal"
  },
  "limit": 10
}
```

---

## 11.10 Memory Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/memory` | List memory items |
| POST | `/api/v1/memory` | Create memory |
| GET | `/api/v1/memory/{memory_id}` | Get memory |
| PATCH | `/api/v1/memory/{memory_id}` | Update memory |
| DELETE | `/api/v1/memory/{memory_id}` | Delete memory |
| POST | `/api/v1/memory/search` | Search memory |

---

## 11.11 Governance Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/governance/policies` | List policies |
| POST | `/api/v1/governance/policies` | Create policy |
| GET | `/api/v1/governance/policies/{policy_id}` | Get policy |
| PATCH | `/api/v1/governance/policies/{policy_id}` | Update policy |
| DELETE | `/api/v1/governance/policies/{policy_id}` | Archive policy |
| POST | `/api/v1/governance/check` | Run policy check |

---

## 11.12 Evaluation Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/evaluations` | List evaluations |
| GET | `/api/v1/evaluations/{evaluation_id}` | Get evaluation |
| POST | `/api/v1/evaluations/run` | Run evaluation manually |
| GET | `/api/v1/workflow-runs/{run_id}/evaluations` | Get run evaluations |

---

## 11.13 Audit Log Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/audit-logs` | Search audit logs |
| GET | `/api/v1/audit-logs/{audit_id}` | Get audit event |

Audit logs should be read-only through the API.

---

## 11.14 Process Intelligence Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/processes/metrics` | Process metrics |
| GET | `/api/v1/processes/workflow-performance` | Workflow performance |
| GET | `/api/v1/processes/bottlenecks` | Bottleneck detection |
| GET | `/api/v1/processes/costs` | Cost analysis |
| GET | `/api/v1/processes/failures` | Failure analysis |

---

## 11.15 Evolution Endpoints (as-built)

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/evolution/variants` | List sandbox variants |
| POST | `/api/v1/evolution/variants` | Propose sandbox variant |
| GET | `/api/v1/evolution/archive` | Fitness / population archive |
| POST | `/api/v1/evolution/variants/{variant_id}/evaluate` | Corpus / fitness evaluate |
| POST | `/api/v1/evolution/variants/{variant_id}/promote` | Canary or promote (gated) |
| POST | `/api/v1/evolution/variants/{variant_id}/rollback` | Rollback canary / promote |

---

## 11.16 Improvement / Loop Endpoints (as-built)

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/improvement/reflect/{run_id}` | Reflect lessons from a run |
| GET | `/api/v1/improvement/lessons` | Lesson library |
| POST | `/api/v1/improvement/auto-propose` | Propose sandbox DNA changes |
| `*` | `/api/v1/improvement/skills/*` | Skill sandbox write / promote |
| POST | `/api/v1/loops/...` | Loop DNA runner (start / status) |

Exact paths follow OpenAPI generated from FastAPI; frontend consumes them via typed client / `openapi.d.ts`.

---

# 12. Workflow Execution Design

## 12.1 Workflow Run Lifecycle

```text
queued
  -> running
    -> waiting_for_approval
      -> running
        -> completed

queued
  -> running
    -> failed

queued
  -> cancelled

running
  -> cancelled
```

---

## 12.2 Workflow Start Flow

```text
1. Frontend sends POST /api/v1/workflows/{workflow_id}/runs
2. Backend authenticates user
3. Backend checks user permission
4. Backend loads workflow
5. Backend validates input schema
6. Backend runs governance pre-check
7. Backend creates workflow_run with status queued
8. Backend writes audit log
9. Backend enqueues worker job
10. Backend returns workflow_run_id
11. Worker executes workflow
12. Frontend polls or streams status
```

---

## 12.3 Worker Execution Flow

```text
1. Worker receives workflow_run_id
2. Worker loads workflow run
3. Worker marks run as running
4. Worker loads workflow version
5. Worker iterates through steps
6. For each step:
   - check cancellation
   - check permissions
   - check governance
   - request approval if required
   - execute agent/tool/evaluation/condition
   - save step output
   - emit event
   - write audit log
7. Run final evaluation
8. Save final output
9. Mark run completed or failed
10. Emit final event
```

---

## 12.4 Step Types

Supported workflow step types:

```text
agent
tool
approval
condition
knowledge_search
memory_search
evaluation
transform
notification
human_input
```

---

## 12.5 Idempotency

Workflow start requests should support an `Idempotency-Key` header.

If the same user sends the same idempotency key for the same workflow, the backend should return the existing workflow run instead of creating a duplicate.

---

# 13. Governance Design

## 13.1 Risk Levels

Use standard risk levels:

```text
low
medium
high
critical
```

Example meaning:

```text
low       = read-only, internal, reversible
medium    = internal update, limited impact
high      = external action, customer-visible, sensitive data
critical  = financial, legal, destructive, production-impacting
```

---

## 13.2 Governance Policy Examples

Example policy:

```json
{
  "name": "Require approval for external emails",
  "conditions": {
    "tool_category": "email",
    "recipient_type": "external"
  },
  "action": "require_approval",
  "reviewer_role": "Manager",
  "risk_level": "high"
}
```

Example policy:

```json
{
  "name": "Block restricted memory for general agents",
  "conditions": {
    "resource_type": "memory",
    "sensitivity": "restricted",
    "agent_department_mismatch": true
  },
  "action": "deny",
  "risk_level": "critical"
}
```

---

## 13.3 Governance Actions

Governance check results:

```text
allow
deny
require_approval
require_evaluation
require_redaction
```

---

# 14. Knowledge and Memory Design

## 14.1 Knowledge Ingestion Pipeline

```text
1. User uploads document
2. Backend stores original file in object storage
3. Backend creates KnowledgeDocument
4. Backend enqueues indexing job
5. Worker extracts text
6. Worker chunks text
7. Worker creates embeddings
8. Worker stores chunks and vector references
9. Document status becomes indexed
```

---

## 14.2 Retrieval Pipeline

```text
1. User, agent, or workflow requests search
2. Backend checks permissions
3. Backend filters by organization, department, sensitivity, ACL
4. Backend performs vector search
5. Backend optionally reranks results
6. Backend returns allowed results only
7. Backend writes audit event for sensitive access
```

---

## 14.3 Memory Rules

Memory should not be globally available by default.

Every memory lookup must consider:

```text
- organization
- user
- agent
- workflow
- department
- sensitivity
- expiration
- policy
```

---

# 15. Agent Runtime Design

## 15.1 Agent Execution Principles

Agents must execute inside backend-controlled boundaries.

The backend controls:

```text
- which agent can run
- which workflow can call the agent
- which tools the agent can use
- which memory the agent can access
- which knowledge the agent can retrieve
- which outputs require evaluation
- which actions require approval
```

---

## 15.2 Agent Input Contract

Every agent execution should receive structured input:

```json
{
  "agent_id": "agent_123",
  "workflow_run_id": "run_123",
  "step_id": "step_123",
  "input": {},
  "context": {
    "user_id": "user_123",
    "organization_id": "org_123",
    "allowed_tools": [],
    "allowed_memory_scopes": [],
    "risk_level": "medium"
  }
}
```

---

## 15.3 Agent Output Contract

Every agent should return structured output:

```json
{
  "status": "completed",
  "output": {},
  "usage": {
    "input_tokens": 1000,
    "output_tokens": 500,
    "cost": 0.0
  },
  "metadata": {
    "model": "provider_model_name",
    "duration_ms": 1000
  }
}
```

---

# 16. Security Design

## 16.1 Required Security Controls

The backend must implement:

```text
- HTTPS in production
- password hashing
- JWT expiration
- refresh token rotation
- API key hashing
- permission checks
- request validation
- rate limiting
- file upload validation
- malware scanning if available
- audit logs
- secret management
- CORS restrictions
- security headers
```

---

## 16.2 Prompt Injection Protection

Because agents may read documents and use tools, the backend should protect against prompt injection.

Recommended controls:

```text
- separate trusted system instructions from untrusted retrieved content
- mark retrieved content as untrusted
- prevent retrieved text from granting tool permissions
- require policy checks before tool calls
- require approval for external or destructive actions
- log tool requests
- evaluate suspicious outputs
```

---

## 16.3 Data Access Control

Every query must include organization scoping.

Example rule:

```text
A user from organization A must never access organization B data.
```

Sensitive resources must also enforce:

```text
- department restrictions
- ACL rules
- role permissions
- policy checks
```

---

# 17. Observability and Monitoring

## 17.1 Logs

All logs should include:

```text
- timestamp
- request_id
- organization_id if available
- user_id if available
- action
- status
- duration
- error code if failed
```

---

## 17.2 Health Checks

Required endpoints:

```text
GET /api/v1/health
GET /api/v1/health/ready
GET /api/v1/health/live
```

`live` checks whether the API process is running.

`ready` checks whether dependencies are available:

```text
- database
- Redis
- queue
- vector store
- object storage
```

---

## 17.3 Metrics

Track:

```text
- request count
- request latency
- error rate
- workflow run count
- workflow duration
- workflow failure rate
- worker job duration
- queue depth
- approval wait time
- document indexing time
- search latency
- evaluation pass/fail rate
- LLM token usage
- LLM cost
```

---

# 18. Deployment Design

## 18.1 Local Development

Local environment should include:

```text
- API server
- PostgreSQL
- Redis
- worker process
- optional vector database
- optional object storage emulator
```

Do not use any Docker for local development.

---

## 18.2 Production Deployment

Production should separate:

```text
- API containers
- worker containers
- PostgreSQL
- Redis
- vector store
- object storage
- monitoring
```

Recommended production services:

```text
api
worker-workflows
worker-knowledge
worker-evaluations
scheduler
postgres
redis
vector-db
object-storage
```

---

## 18.3 Environment Variables

Required environment variables:

```text
APP_ENV
APP_NAME
API_HOST
API_PORT
DATABASE_URL
REDIS_URL
JWT_SECRET
JWT_ACCESS_TOKEN_EXPIRE_MINUTES
JWT_REFRESH_TOKEN_EXPIRE_DAYS
CORS_ALLOWED_ORIGINS
OBJECT_STORAGE_PROVIDER
OBJECT_STORAGE_BUCKET
VECTOR_STORE_PROVIDER
LLM_PROVIDER
LLM_API_KEY
LOG_LEVEL
RATE_LIMIT_ENABLED
```

Optional:

```text
SENTRY_DSN
OTEL_EXPORTER_ENDPOINT
SMTP_HOST
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
SSO_CLIENT_ID
SSO_CLIENT_SECRET
```

---

# 19. Testing Strategy

## 19.1 Unit Tests

Test:

```text
- permission logic
- governance policy evaluation
- workflow state transitions
- schema validation
- memory access rules
- knowledge filtering
- evaluation rules
- audit event creation
```

---

## 19.2 Integration Tests

Test:

```text
- API routes with database
- workflow creation and execution
- approval flow
- knowledge indexing
- memory search
- worker job execution
- audit log creation
```

---

## 19.3 End-to-End Tests

Test full flows:

```text
- user logs in
- user starts workflow
- workflow requires approval
- reviewer approves
- worker continues
- evaluation passes
- final output is returned
- audit logs are created
```

---

## 19.4 Security Tests

Test:

```text
- unauthorized access
- cross-organization data access
- role permission failures
- invalid tokens
- expired tokens
- restricted memory access
- restricted knowledge access
- tool permission failures
```

---

## 19.5 Load Tests

Test:

```text
- many workflow runs
- many concurrent users
- large document indexing
- vector search latency
- queue backlog behavior
```

---

# 20. Implementation Plan

## Phase 0: Project Setup

Goal: Create the backend project foundation.

Tasks:

```text
1. Create backend directory.
2. Initialize Python project.
3. Add FastAPI.
4. Add database library.
5. Add migration tool.
6. Add configuration system.
7. Add logging.
8. Add basic health endpoint.
```

Deliverables:

```text
- backend app starts locally
- health endpoint works
- PostgreSQL connection works
- Redis connection works
- OpenAPI docs available
```

Acceptance criteria:

```text
GET /api/v1/health returns success.
API starts with one command.
Database migrations can run.
```

---

## Phase 1: Authentication and Users

Goal: Secure the backend.

Tasks:

```text
1. Create user model.
2. Create organization model.
3. Create role and permission models.
4. Implement password hashing.
5. Implement login endpoint.
6. Implement JWT access tokens.
7. Implement refresh tokens.
8. Implement current user dependency.
9. Implement permission checks.
10. Add seed script for first admin user.
```

Deliverables:

```text
- login works
- authenticated routes work
- users belong to organizations
- basic RBAC works
```

Acceptance criteria:

```text
Unauthenticated users cannot access protected endpoints.
Users cannot access another organization’s data.
Admin can create users.
```

---

## Phase 2: Audit Logging

Goal: Make important actions traceable.

Tasks:

```text
1. Create audit log table.
2. Add AuditService.
3. Add request ID middleware.
4. Log login events.
5. Log create/update/delete events.
6. Log workflow run events.
7. Add audit search endpoint.
```

Deliverables:

```text
- audit events are created
- audit logs are searchable
- request IDs connect API logs to audit logs
```

Acceptance criteria:

```text
Starting a workflow creates an audit event.
Approving a request creates an audit event.
Changing permissions creates an audit event.
```

---

## Phase 3: Agent and Tool Registry

Goal: Register agents and tools.

Tasks:

```text
1. Create agent model.
2. Create tool model.
3. Create agent CRUD endpoints.
4. Create tool CRUD endpoints.
5. Add allowed tools to agents.
6. Add allowed memory scopes to agents.
7. Add risk levels.
8. Add status management.
```

Deliverables:

```text
- agents can be created
- tools can be created
- agents can be activated/disabled
- tool permissions can be assigned
```

Acceptance criteria:

```text
Disabled agents cannot be used.
Agents cannot use tools they are not allowed to use.
```

---

## Phase 4: Workflow Definitions

Goal: Create and version workflows.

Tasks:

```text
1. Create workflow model.
2. Create workflow version model.
3. Create workflow CRUD endpoints.
4. Add workflow version creation.
5. Add JSON schema validation for input/output.
6. Add workflow activation.
7. Add workflow disabling.
```

Deliverables:

```text
- workflows can be created
- versions can be created
- active version can be selected
- input schemas are stored
```

Acceptance criteria:

```text
Only active workflows can be run.
Invalid workflow input is rejected.
Workflow versions are immutable after activation.
```

---

## Phase 5: Workflow Run Engine

Goal: Execute workflows through workers.

Tasks:

```text
1. Create workflow_run model.
2. Create workflow_run_step model.
3. Implement start run endpoint.
4. Add queue integration.
5. Add workflow worker.
6. Implement step execution loop.
7. Implement status transitions.
8. Implement cancellation.
9. Implement retry for failed runs.
10. Persist step outputs.
```

Deliverables:

```text
- workflow runs can be queued
- workers execute runs
- run status updates are persisted
- steps are tracked
```

Acceptance criteria:

```text
POST /workflows/{id}/runs creates a queued run.
Worker picks up queued run.
Run becomes completed or failed.
Frontend can fetch run status and steps.
```

---

## Phase 6: Governance and Approvals

Goal: Add risk controls and human approval gates.

Tasks:

```text
1. Create governance policy model.
2. Create policy engine.
3. Add pre-run governance checks.
4. Add pre-step governance checks.
5. Create approval request model.
6. Add approval endpoints.
7. Pause workflow when approval is required.
8. Resume workflow after approval.
9. Fail or cancel workflow after rejection.
```

Deliverables:

```text
- policies can allow, deny, or require approval
- approval requests are created
- workflows pause for approvals
- reviewers can approve or reject
```

Acceptance criteria:

```text
High-risk tool action creates approval request.
Workflow status becomes waiting_for_approval.
Approval resumes workflow.
Rejection stops workflow.
```

---

## Phase 7: Knowledge System

Goal: Upload, index, and search knowledge.

Tasks:

```text
1. Create knowledge document model.
2. Create knowledge chunk model.
3. Add document upload endpoint.
4. Store original documents.
5. Add indexing worker.
6. Extract text.
7. Chunk text.
8. Generate embeddings.
9. Store vector references.
10. Add knowledge search endpoint.
11. Enforce ACL and sensitivity filtering.
```

Deliverables:

```text
- documents can be uploaded
- documents can be indexed
- knowledge can be searched
- restricted documents are protected
```

Acceptance criteria:

```text
Indexed documents return search results.
Users cannot search restricted documents without permission.
Document indexing failures are visible.
```

---

## Phase 8: Memory System

Goal: Add controlled memory storage and retrieval.

Tasks:

```text
1. Create memory item model.
2. Add memory CRUD endpoints.
3. Add memory search endpoint.
4. Add memory scopes.
5. Add expiration handling.
6. Add sensitivity levels.
7. Add memory access policies.
8. Connect memory retrieval to workflow steps.
```

Deliverables:

```text
- memory can be stored
- memory can be searched
- memory access is scoped
- workflows can retrieve allowed memory
```

Acceptance criteria:

```text
Agents cannot access memory outside allowed scopes.
Expired memory is not returned.
Sensitive memory access is audited.
```

---

## Phase 9: Evaluation System

Goal: Check outputs before completion.

Tasks:

```text
1. Create evaluation run model.
2. Implement schema evaluator.
3. Implement rule evaluator.
4. Implement policy evaluator.
5. Optional: implement LLM evaluator.
6. Add evaluation step type.
7. Add final output evaluation.
8. Add evaluation API.
```

Deliverables:

```text
- outputs can be evaluated
- failed evaluations can block completion
- warnings are visible
```

Acceptance criteria:

```text
Invalid output schema fails evaluation.
Workflow requiring evaluation cannot complete until evaluation passes.
Evaluation results are linked to runs and steps.
```

---

## Phase 10: Streaming Updates

Goal: Let frontend observe live workflow progress.

Tasks:

```text
1. Add workflow event table or event stream.
2. Emit events during workflow execution.
3. Add SSE endpoint.
4. Stream run status changes.
5. Stream step events.
6. Stream approval events.
7. Stream final output event.
```

Deliverables:

```text
- frontend can subscribe to run events
- users see real-time progress
```

Acceptance criteria:

```text
GET /workflow-runs/{id}/stream streams events.
Step completion appears without page refresh.
Run completion appears without polling.
```

---

## Phase 11: Process Intelligence

Goal: Provide analytics from workflow execution history.

Tasks:

```text
1. Add aggregate queries.
2. Add workflow performance endpoint.
3. Add bottleneck endpoint.
4. Add failure analysis endpoint.
5. Add cost analysis endpoint.
6. Add approval delay endpoint.
```

Deliverables:

```text
- workflow metrics are available
- bottlenecks can be detected
- costs can be analyzed
```

Acceptance criteria:

```text
Admin can view average workflow duration.
Admin can view most failed workflows.
Admin can view approval wait time.
```

---

## Phase 12: Hardening and Production Readiness

Goal: Prepare for production.

Tasks:

```text
1. Add rate limiting.
2. Add CORS restrictions.
3. Add security headers.
4. Add structured logs.
5. Add metrics.
6. Add error monitoring.
7. Add backup strategy.
8. Add database indexes.
9. Add load tests.
10. Add security tests.
11. Add deployment manifests.
12. Add CI/CD pipeline.
```

Deliverables:

```text
- production deployment ready
- monitoring ready
- tests passing
- documentation complete
```

Acceptance criteria:

```text
All critical endpoints have tests.
No protected endpoint is accessible without auth.
Workflow execution survives worker restart where possible.
API documentation is complete.
```

---

# 21. Minimum Viable Backend

The first usable version should include:

```text
- authentication
- users
- organizations
- RBAC
- audit logs
- agent registry
- workflow definitions
- workflow runs
- background worker
- basic governance checks
- approval requests
- run status API
- run step API
- basic knowledge upload/search
- OpenAPI docs
```

The MVP does not need advanced analytics, advanced memory, or complex process intelligence on day one.

---

# 22. Definition of Done

The backend server is considered complete for the first production-ready version when:

```text
1. Frontend can authenticate users.
2. Frontend can list workflows.
3. Frontend can start workflow runs.
4. Backend validates inputs.
5. Backend enforces permissions.
6. Backend creates audit logs.
7. Backend queues long-running work.
8. Worker executes workflow steps.
9. Workflow status can be fetched.
10. Workflow progress can be streamed.
11. Approval gates work.
12. Knowledge search works with access control.
13. Memory access is controlled.
14. Evaluations can block unsafe or invalid outputs.
15. Admin can view audit logs.
16. Admin can view workflow performance.
17. API documentation is generated.
18. Tests cover critical flows.
19. Deployment is documented.
20. Secrets are not hardcoded.
```

Product bar mark ~100 (see §24) additionally requires:

```text
21. Postgres is primary runtime persistence when DATABASE_URL is set.
22. Local tool adapters record durable tool_effects.
23. Evolution APIs enforce sandbox_only propose / evaluate / canary / rollback.
24. Self-improvement reflect / lessons / auto-propose are available.
25. Production DNA validation runs on activate / production_ready.
26. E1 operator path e2e test passes (login → run → gate → complete → improve).
```

---

# 23. Final Backend Purpose Statement

The backend API server transforms the architecture from `structure.md` into an executable platform.

It provides the secure, governed, auditable, and scalable layer that allows a frontend application to interact with agents, workflows, memory, knowledge, governance, evaluations, process intelligence, evolution sandbox controls, and self-improvement loops.

The frontend should remain simple.

The backend should enforce intelligence, control, security, and trust.

Final system relationship:

```text
Frontend
  -> Backend API
    -> Services
      -> Governance
      -> Workflow Engine
      -> Agent Runtime
      -> Knowledge and Memory
      -> Evaluation
      -> Evolution Sandbox (sandbox_only)
      -> Self-improvement (reflect / lessons / propose)
      -> Audit
        -> Postgres control plane (+ optional queue / vector / LLM / object storage)
```

---

# 24. Implementation Mapping (structure.md §11.1 / §12 alignment)

This section records **how this backend plan is realized today** for product bar mark ~100. It does not weaken architecture intent in `structure.md`. Evidence: `status.md`, `structure_scorecard_100.md`, `mark_100_verification.md`, `reviews/e1_operator_checklist.md`, `planning/gap_analysis_for_structure.md`, `planning/gap_analysis_for_backend.md`, `backend/README.md`.

## 24.1 Document relationship

| Document | Role |
|----------|------|
| `structure.md` | Architecture vision and source of truth |
| `planning/structure/nn_*/` | Architecture SDD requirements / design / tasks (01–17) |
| `backend.md` (this file) | Backend API requirements and design plan |
| `planning/backend/nn_*/requirements.md` | Backend sub-functional EARS specs (01–24, sequential) |
| `planning/backend/nn_*/design.md` | Backend SDD designs v2.0 (portfolio score 100; see `DESIGN_QUALITY_SCORE.md`) |
| `planning/backend/nn_*/tasks.md` | Backend SDD tasks **v2.2** with **Deliverable (code paths)** per task (see `TASK_TO_CODE_TRACEABILITY.md`) |
| `backend/` | As-built FastAPI control plane |
| `frontend.md` / `frontend/` | Ops console contract and as-built UI |

## 24.2 Capability gates (backend share of structure §11.1)

| Phase | structure.md band | Backend as-built |
|-------|-------------------|------------------|
| A Foundation | Days 1–14 | Auth, RBAC, audit events, health/ready, seed data, business corpus validation hooks |
| B Shadow learning | Days 15–30 | Event/process APIs; PI disk artifacts under `business/process-intelligence/`; knowledge ingest/search |
| C Controlled co-pilot | Days 31–60 | Postgres `runtime_state` JSONB primary store; DNA runs; human approval gates; Tier-0/1 retrieval; tool adapters + `tool_effects`; production DNA checks on activate |
| D Evolution sandbox | Days 61–90 | Corpus eval, canary/promote/rollback, fitness archive; auto-reflect, lessons, auto-propose, loop runner, skill sandbox |

## 24.3 As-built realization (backend topics from structure §12.3)

| Topic | Architecture intent | Backend as-built |
|-------|---------------------|------------------|
| Control plane | API + durable state | FastAPI + **Postgres** `runtime_state` JSONB; JSON file = backup/seed only |
| Tool adapters | Real execution | Local adapters + durable `tool_effects`; live CRM/email SaaS = later |
| Tool broker | Scoped permissions | Allow-list ∩ DNA tools ∩ RBAC ∩ gates; ephemeral OAuth per tool = later |
| PI | Miner / conformance / bottleneck / causal | PI **services + disk artifacts** (not five independent LLM agents) |
| Retrieval | Tier 0 / 1 / 2 | Tier 0 keyword+hash embed + provenance; Tier 1 entity multi-hop (LightRAG-**lite**); Tier 2 + full LightRAG vendor = later |
| Knowledge graph | Agent-native graph | K1-lite extract/operators + optional federation export |
| Evolution | Sandbox only | Variants `sandbox_only`; corpus eval; canary; versioned promote; rollback; **no** host code self-rewrite |
| Self-improvement | Reflective loops | Auto-reflect, lessons, auto-propose, Loop runner, skill sandbox APIs |
| DNA production safety | Gates + rollback | `business:validate` + runtime `activate_workflow_version` / production DNA checks (`structure_validators`) |
| Operator proof | End-to-end path | E1: login → run → human gate → complete → improve (`test_e1_operator_path`) |

## 24.4 structure.md sections primarily realized in backend

| structure.md | Spec folder (planning/structure) | Backend surface |
|--------------|----------------------------------|-----------------|
| §2 Intake + Risk Router | `03_intake-and-risk-router` | Run start governance pre-check / risk classification |
| §6 Governance | `04_governance-risk-tiers-and-gates` | Policies, approval gates, tier enforcement |
| §7 Security | `05_security-controls-and-tool-broker` | AuthZ, tool allow-list, rate limits, audit |
| §2.3 Process Intelligence | `06_process-intelligence-layer` | Process APIs + disk artifacts |
| §3 Knowledge / memory / retrieval | `07`–`09` | Knowledge, memory, tiered retrieval, K1-lite |
| §4 Workflow DNA + execution | `10`–`12` | DNA models, engine, human gates, audit path |
| §8 Evaluation | `13_evaluation-harness-and-corpus` | Evaluation routes + corpus eval |
| §5 Evolution sandbox | `14_evolution-sandbox-engine` | `/api/v1/evolution/*` |
| §9 Agent roster (control roles) | `15_agent-roster-and-control-roles` | Agent registry + control-plane services |
| §11 Rollout / operator path | `17_phased-rollout-and-operator-path` | E1 e2e path + health/ready |

## 24.5 Explicit non-goals (current product bar)

Do **not** treat as missing `backend.md` / `structure.md` requirements for mark ~100:

- Full commercial LightRAG / Neo4j production mesh  
- Live external CRM / email / billing SaaS adapters  
- DGM-style host application self-rewrite  
- Always-on multi-worker Temporal/Celery cluster as a hard requirement  
- Ephemeral per-tool OAuth credential broker (when live SaaS adapters land)  
- Infinite enterprise content fill of every `business/` leaf  

## 24.6 Runtime entry points

| Layer | Entry |
|-------|--------|
| Backend code | `backend/` — FastAPI `app/main.py`, `runtime.py`, `infrastructure/*` |
| Persistence | `DATABASE_URL` → Postgres; see `docs/postgres-runbook.md` |
| Business corpus | `business/` |
| Continuity / evidence | `memory/handoff.md`, `memory/project.md`, `status.md` |
| Ops UI | `frontend/` (consumes this API; see `frontend.md` §33) |
