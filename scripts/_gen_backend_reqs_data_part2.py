"""Requirement detail payloads BE-05..BE-24."""

from __future__ import annotations


def _d(**kwargs):
    return kwargs


DETAILS = {}

DETAILS["05"] = _d(
    scope_in=[
        "- Login, logout, token refresh, me profile.",
        "- Password reset when password auth is used.",
        "- API key create/list/revoke for machine clients.",
        "- JWT access/refresh model; optional SSO/OAuth readiness.",
        "- Auth rate limiting on sensitive endpoints.",
    ],
    scope_out=["- Full enterprise IdP productization (optional later).", "- Frontend login page UI."],
    stk=[
        ("STK-05-01", "End users", "Secure login and session lifecycle."),
        ("STK-05-02", "Integrations", "API keys for machine access."),
        ("STK-05-03", "Security", "Token hygiene and rate limits."),
    ],
    fr=[
        ("FR-05-01", "The backend shall support authenticated users via login issuing access credentials."),
        ("FR-05-02", "When a user logs in with valid credentials, the backend shall return access token material suitable for subsequent API calls."),
        ("FR-05-03", "When a user logs out, the backend shall invalidate or reject further use of the session/refresh material according to the chosen token strategy."),
        ("FR-05-04", "When a valid refresh token is presented, the backend shall issue a new access token."),
        ("FR-05-05", "Where password authentication is used, the backend shall support password reset flows."),
        ("FR-05-06", "The backend shall support API key creation, listing, and revocation for machine clients."),
        ("FR-05-07", "When an API key is used, the backend shall authenticate the caller as the associated principal with constrained permissions."),
        ("FR-05-08", "The backend shall expose a current-user endpoint (e.g. GET /auth/me) returning identity and role claims needed by clients."),
        ("FR-05-09", "If authentication credentials are invalid or expired, then the backend shall reject the request with an authentication error."),
        ("FR-05-10", "While SSO/OAuth is optional, the backend design shall not preclude OAuth2/OIDC compatibility."),
        ("FR-05-11", "When sensitive auth endpoints are called repeatedly, the backend shall apply rate limiting."),
        ("FR-05-12", "Passwords shall be stored only as secure hashes, never as plaintext."),
    ],
    perf=[
        ("NFR-05-01", "Login handler p95 shall remain under 500ms excluding external IdP latency."),
        ("NFR-05-02", "Token validation on protected routes shall add minimal overhead (target under 10ms local)."),
    ],
    sec=[
        ("NFR-05-03", "JWT secrets and API key secrets shall not be logged."),
        ("NFR-05-04", "API keys shall be shown in full only at creation time and masked thereafter."),
        ("NFR-05-05", "Auth endpoints shall be rate limited to reduce credential stuffing risk."),
    ],
    ac=[
        ("AC-05-01", "POST login with seed users returns usable token."),
        ("AC-05-02", "Protected route without token returns 401."),
        ("AC-05-03", "API key can be created and used, then revoked."),
        ("AC-05-04", "Password hashes are not returned by /me."),
    ],
    tv=[
        ("TV-05-01", "Unit/e2e: login → /me.", "Automated"),
        ("TV-05-02", "Negative: bad password → 401.", "Automated"),
        ("TV-05-03", "API key revoke blocks subsequent use.", "Automated"),
    ],
    trace=[
        ("backend.md §7.1 Authentication", "FR-05-01 … FR-05-10"),
        ("backend.md §11.4 Auth endpoints", "FR-05-01 … FR-05-08"),
        ("backend.md §8.1 / rate limit", "FR-05-11, NFR-05-05"),
    ],
)

DETAILS["06"] = _d(
    scope_in=[
        "- Role-based access control roles: Owner, Admin, Manager, Operator, Reviewer, Viewer, ServiceAccount.",
        "- Permission strings for agents, workflows, runs, knowledge, memory, governance, approvals, audit, evaluations, settings.",
        "- Enforcement on every protected resource.",
        "- Design readiness for future ABAC rules.",
    ],
    scope_out=["- Full ABAC policy language product.", "- Frontend permission matrix UI."],
    stk=[
        ("STK-06-01", "Admins", "Assign roles with least privilege."),
        ("STK-06-02", "Auditors", "Permission checks are consistent and logged on failures."),
        ("STK-06-03", "Developers", "Declarative permission dependencies on routes."),
    ],
    fr=[
        ("FR-06-01", "The backend shall implement role-based access control for protected operations."),
        ("FR-06-02", "The backend shall support roles including Owner, Admin, Manager, Operator, Reviewer, Viewer, and ServiceAccount (or equivalent mapped set)."),
        ("FR-06-03", "When a caller lacks a required permission, the backend shall deny the operation with an authorization error."),
        ("FR-06-04", "The backend shall enforce permissions for agents:read/create/update/delete as applicable to agent routes."),
        ("FR-06-05", "The backend shall enforce permissions for workflows:read/create/update/run as applicable to workflow routes."),
        ("FR-06-06", "The backend shall enforce permissions for workflow_runs:read/cancel as applicable to run routes."),
        ("FR-06-07", "The backend shall enforce permissions for knowledge:read/write, memory:read/write, governance:read/update, approvals:read/approve/reject, audit:read, evaluations:read, and settings:update on corresponding resources."),
        ("FR-06-08", "While ABAC is not fully required for product bar, the authorization design shall allow future rules such as organization match and max risk level."),
        ("FR-06-09", "When authorization fails, the backend shall not leak whether a resource exists beyond what policy allows."),
        ("FR-06-10", "Service accounts and API keys shall be constrained by the same permission model as interactive users."),
    ],
    perf=[
        ("NFR-06-01", "Permission checks shall be deterministic and not require external network calls."),
        ("NFR-06-02", "Permission evaluation p95 shall remain under 5ms local for in-memory role maps."),
    ],
    sec=[
        ("NFR-06-03", "Authorization shall be enforced server-side on every protected resource; client claims alone are insufficient."),
        ("NFR-06-04", "Privilege escalation paths (self-assign Owner) shall be restricted to appropriately privileged roles."),
    ],
    ac=[
        ("AC-06-01", "Viewer cannot create workflows when permission matrix forbids it."),
        ("AC-06-02", "Operator can run workflows if granted workflows:run."),
        ("AC-06-03", "Reviewer can approve when granted approvals:approve."),
        ("AC-06-04", "Cross-role matrix unit tests cover deny paths."),
    ],
    tv=[
        ("TV-06-01", "Unit: permission matrix table-driven tests.", "Automated"),
        ("TV-06-02", "Integration: role tokens against sample routes.", "Automated"),
        ("TV-06-03", "Negative: missing permission → 403.", "Automated"),
    ],
    trace=[
        ("backend.md §7.2 Authorization", "FR-06-01 … FR-06-08"),
        ("backend.md §6.2 Secure by Default", "FR-06-03, NFR-06-03"),
    ],
)

DETAILS["07"] = _d(
    scope_in=[
        "- Organizations, users, teams, roles, permissions, invitations, service accounts, API keys association.",
        "- User lifecycle statuses (active, invited, disabled).",
        "- Organization settings endpoints as provided by backend.",
    ],
    scope_out=["- Full HR identity directory sync.", "- Billing calculations."],
    stk=[
        ("STK-07-01", "Org admins", "Manage users and invitations."),
        ("STK-07-02", "Security", "Disable users and rotate access."),
        ("STK-07-03", "Platform", "Tenant isolation fields always present."),
    ],
    fr=[
        ("FR-07-01", "The backend shall support organization records with status active or disabled."),
        ("FR-07-02", "The backend shall support user records linked to an organization with status active, invited, or disabled."),
        ("FR-07-03", "The backend shall support assigning roles/permissions to users within an organization."),
        ("FR-07-04", "Where invitations are enabled, the backend shall support creating invitations for new users."),
        ("FR-07-05", "The backend shall support service accounts as non-human principals within an organization."),
        ("FR-07-06", "The backend shall associate API keys with a principal and organization."),
        ("FR-07-07", "When a user is disabled, the backend shall reject new authenticated API access for that user."),
        ("FR-07-08", "The backend shall expose user and organization management endpoints required by the ops console (list/get/update as implemented)."),
        ("FR-07-09", "If the deployment is single-tenant, then the backend shall still persist organization_id on tenant-scoped rows."),
        ("FR-07-10", "When listing users, the backend shall enforce admin/owner (or equivalent) authorization."),
    ],
    perf=[("NFR-07-01", "User list for a typical org (<1k users) shall return within 500ms p95 local.")],
    sec=[
        ("NFR-07-02", "User list endpoints shall not return password hashes or full API key secrets."),
        ("NFR-07-03", "Only privileged roles may invite users or create service accounts."),
    ],
    ac=[
        ("AC-07-01", "Seed organizations and users load after bootstrap."),
        ("AC-07-02", "Disabled user cannot call protected APIs."),
        ("AC-07-03", "organization_id present on user entity."),
        ("AC-07-04", "Non-admin cannot list all users."),
    ],
    tv=[
        ("TV-07-01", "Unit: user status transitions.", "Automated"),
        ("TV-07-02", "Authz: admin vs operator on user admin routes.", "Automated"),
        ("TV-07-03", "Seed credentials login for documented roles.", "Automated"),
    ],
    trace=[
        ("backend.md §7.3 User/Org", "FR-07-01 … FR-07-06"),
        ("backend.md §10.2–10.3", "FR-07-01 … FR-07-02"),
    ],
)

DETAILS["08"] = _d(
    scope_in=[
        "- Agent registry CRUD and metadata fields from backend.md §7.4 / §10.4.",
        "- Agent statuses: draft, active, disabled, archived.",
        "- Allowed tools, memory scopes, workflow types, risk level, input/output schema.",
        "- Agent activity and tools listing endpoints.",
        "- Agent execution contracts (input/output) at API/runtime boundary §15.",
    ],
    scope_out=["- Autonomous free-form swarm outside workflow engine.", "- Frontend agent builder UX details."],
    stk=[
        ("STK-08-01", "Operators", "See which agents exist and their constraints."),
        ("STK-08-02", "Governance", "Agents carry risk and tool allow-lists."),
        ("STK-08-03", "Engineers", "Stable agent IDs for workflow DNA references."),
    ],
    fr=[
        ("FR-08-01", "The backend shall maintain a registry of available agents."),
        ("FR-08-02", "When an agent is created or updated, the backend shall persist agent ID, name, description, version, owner, department, allowed tools, allowed memory scopes, allowed workflow types, risk level, input schema, output schema, runtime configuration, and status."),
        ("FR-08-03", "The backend shall support agent statuses draft, active, disabled, and archived."),
        ("FR-08-04", "When listing agents, the backend shall return only agents visible to the caller's organization and permissions."),
        ("FR-08-05", "When an agent is disabled or archived, the backend shall prevent new workflow steps from starting that agent unless an explicit override policy exists."),
        ("FR-08-06", "The backend shall expose endpoints to list, create, get, update, and delete/archive agents."),
        ("FR-08-07", "The backend shall expose agent activity and agent tools inspection endpoints as specified in the API design."),
        ("FR-08-08", "When an agent executes inside a workflow, the backend shall supply an input contract and accept an output contract conforming to §15 designs."),
        ("FR-08-09", "If an agent references a tool not in its allowed tools, then the backend shall deny tool use for that agent."),
        ("FR-08-10", "Agent definitions used in production workflows shall be versionable or otherwise immutable for historical runs."),
    ],
    perf=[("NFR-08-01", "Agent list for typical catalogs (<500) shall return within 300ms p95 local.")],
    sec=[
        ("NFR-08-02", "Only authorized roles may create or update agents."),
        ("NFR-08-03", "Agent runtime configuration shall not embed plaintext provider secrets; secrets shall be referenced securely."),
    ],
    ac=[
        ("AC-08-01", "Create agent then get by id succeeds."),
        ("AC-08-02", "Disabled agent cannot be newly executed in runs."),
        ("AC-08-03", "Allowed tools list is returned on get."),
        ("AC-08-04", "Unauthorized create returns 403."),
    ],
    tv=[
        ("TV-08-01", "CRUD unit/integration tests for agents.", "Automated"),
        ("TV-08-02", "Negative: tool outside allow-list.", "Automated"),
        ("TV-08-03", "Flagship agents seed present for E1.", "Automated"),
    ],
    trace=[
        ("backend.md §7.4 Agent Registry", "FR-08-01 … FR-08-07"),
        ("backend.md §15 Agent Runtime", "FR-08-08 … FR-08-10"),
        ("backend.md §11.5", "FR-08-06 … FR-08-07"),
    ],
)

DETAILS["09"] = _d(
    scope_in=[
        "- Tool registry metadata: schemas, risk, permissions, approval requirement, timeout, retry, enabled status.",
        "- Tool categories (database, email, calendar, crm, file, web, internal_api, external_api, llm, code_execution, human_approval).",
        "- Local tool adapters and durable tool_effects.",
        "- Tool permission broker: allow-list ∩ DNA tools ∩ RBAC ∩ gates.",
    ],
    scope_out=[
        "- Live external CRM/email/billing SaaS adapters (non-goal for mark ~100).",
        "- Ephemeral OAuth per-tool broker (deferred).",
    ],
    stk=[
        ("STK-09-01", "Security", "Least-privilege tool access."),
        ("STK-09-02", "Operators", "Understand tool risk and approval needs."),
        ("STK-09-03", "Engineers", "Adapters produce durable side-effect records."),
    ],
    fr=[
        ("FR-09-01", "The backend shall maintain a registry of tools usable by agents only through backend-controlled permissions."),
        ("FR-09-02", "When a tool is registered, the backend shall store tool ID, name, description, category, input schema, output schema, risk level, required permissions, approval requirement, timeout, retry policy, and enabled/disabled status."),
        ("FR-09-03", "The backend shall support tool categories including database, email, calendar, crm, file, web, internal_api, external_api, llm, code_execution, and human_approval."),
        ("FR-09-04", "When a high-risk tool is invoked, the backend shall require explicit governance rules and/or approval as configured."),
        ("FR-09-05", "The backend shall execute tools via adapters and record durable tool_effects for side effects."),
        ("FR-09-06", "When authorizing a tool call, the backend shall intersect agent allow-list, workflow DNA tools, RBAC permissions, and gate requirements."),
        ("FR-09-07", "If a tool is disabled, then the backend shall reject new invocations of that tool."),
        ("FR-09-08", "The backend shall expose tool list/detail endpoints required by the ops console."),
        ("FR-09-09", "While live SaaS adapters are deferred, local adapters shall still exercise realistic side-effect paths for CRM/billing/email/audit/contract_parser/policy_retriever as implemented."),
        ("FR-09-10", "The backend shall not grant tools ambient credentials broader than the task scope (broker principle)."),
    ],
    perf=[
        ("NFR-09-01", "Local adapter calls shall honor configured timeouts."),
        ("NFR-09-02", "tool_effects writes shall be durable before acknowledging tool success for mutating tools."),
    ],
    sec=[
        ("NFR-09-03", "Tool credentials and secrets shall not be returned to clients."),
        ("NFR-09-04", "Tool outputs shall be treated as untrusted input to subsequent LLM prompts."),
    ],
    ac=[
        ("AC-09-01", "Tool registry lists expected local tools."),
        ("AC-09-02", "Mutating adapter writes tool_effects entry."),
        ("AC-09-03", "Invocation denied when tool not in DNA allow-list."),
        ("AC-09-04", "High-risk tool path can require approval."),
    ],
    tv=[
        ("TV-09-01", "Unit: broker intersection logic.", "Automated"),
        ("TV-09-02", "Integration: adapter + tool_effects persistence.", "Automated"),
        ("TV-09-03", "Negative: disabled tool invoke.", "Automated"),
    ],
    trace=[
        ("backend.md §7.5 Tool Registry", "FR-09-01 … FR-09-04, FR-09-07"),
        ("backend.md §24.3 Tool adapters/broker", "FR-09-05 … FR-09-06, FR-09-09"),
        ("backend.md §16 Security tools", "FR-09-10, NFR-09-03"),
    ],
)

DETAILS["10"] = _d(
    scope_in=[
        "- Workflow definitions and versions.",
        "- Metadata: risk, schemas, steps, governance/evaluation policy, status.",
        "- Statuses draft/active/disabled/archived.",
        "- Create/update/disable/list/get endpoints.",
        "- Workflow DNA structural fields needed for execution and safety validation.",
    ],
    scope_out=["- Run execution (BE-11).", "- Evolution mutation of DNA (BE-20)."],
    stk=[
        ("STK-10-01", "Business owners", "Versioned process definitions."),
        ("STK-10-02", "Operators", "Activate only validated workflows."),
        ("STK-10-03", "Auditors", "Historical version used by each run is known."),
    ],
    fr=[
        ("FR-10-01", "The backend shall support workflow definitions representing structured multi-step business processes."),
        ("FR-10-02", "When a workflow is created, the backend shall store workflow ID, name, description, version lineage, owner, department, risk level, input schema, output schema, steps, governance policy references, evaluation policy references, and status."),
        ("FR-10-03", "The backend shall support workflow statuses draft, active, disabled, and archived."),
        ("FR-10-04", "The backend shall support workflow versioning such that runs reference a specific workflow version."),
        ("FR-10-05", "When a workflow version is updated, historical runs shall continue to reference the version they executed."),
        ("FR-10-06", "The backend shall expose list/create/get/update/disable (and version activate) endpoints for workflows."),
        ("FR-10-07", "Workflow steps may include agents, tools, conditions, approvals, memory retrieval, knowledge search, evaluation, and outputs as defined in execution design."),
        ("FR-10-08", "If a workflow is disabled or archived, then the backend shall reject new run starts for that workflow."),
        ("FR-10-09", "When a workflow definition includes DNA-like structure, the backend shall persist guardrails, verification, rollback, and memory read/write declarations when provided."),
        ("FR-10-10", "The backend shall validate workflow payloads against schema before accepting create/update."),
    ],
    perf=[("NFR-10-01", "Workflow get by id p95 under 100ms local.")],
    sec=[
        ("NFR-10-02", "Only authorized roles may create, update, or activate workflows."),
        ("NFR-10-03", "Workflow definitions shall not embed raw secrets."),
    ],
    ac=[
        ("AC-10-01", "Create workflow version and retrieve it."),
        ("AC-10-02", "Run references workflow version id."),
        ("AC-10-03", "Disabled workflow cannot start runs."),
        ("AC-10-04", "Invalid schema rejected on create."),
    ],
    tv=[
        ("TV-10-01", "CRUD + version tests.", "Automated"),
        ("TV-10-02", "Negative: start disabled workflow.", "Automated"),
        ("TV-10-03", "Flagship workflow seed available.", "Automated"),
    ],
    trace=[
        ("backend.md §7.6 Workflow Management", "FR-10-01 … FR-10-08"),
        ("backend.md §10.5–10.6", "FR-10-02 … FR-10-05"),
        ("backend.md §11.6", "FR-10-06"),
    ],
)

DETAILS["11"] = _d(
    scope_in=[
        "- Workflow run lifecycle: queued, running, waiting_for_approval, paused, completed, failed, cancelled, expired.",
        "- Step tracking and step types.",
        "- Start flow: auth, permission, load, validate, governance pre-check, create run, audit, execute, return id.",
        "- Worker execution loop, cancellation, retry, idempotency key.",
        "- Streaming hooks (events produced for BE-19).",
    ],
    scope_out=["- Approval decision UX (BE-13 owns decision APIs).", "- Evolution of DNA (BE-20)."],
    stk=[
        ("STK-11-01", "Operators", "Start, observe, cancel, retry runs."),
        ("STK-11-02", "Frontend", "Stable run/step APIs and status model."),
        ("STK-11-03", "Risk", "No irreversible tools before gates."),
    ],
    fr=[
        ("FR-11-01", "When a workflow is started, the backend shall create a workflow_run record."),
        ("FR-11-02", "The backend shall support run statuses queued, running, waiting_for_approval, paused, completed, failed, cancelled, and expired."),
        ("FR-11-03", "Each workflow run shall store run ID, workflow ID, workflow version, requester, organization ID, input, status, current step, output, error, timestamps, usage metrics, approval state, and evaluation results as available."),
        ("FR-11-04", "The backend shall create step records for run steps with statuses pending, running, waiting_for_approval, completed, failed, skipped, and cancelled."),
        ("FR-11-05", "Each step shall store step identity, run ID, name, type, agent/tool IDs if applicable, input/output/error, timestamps, duration, and retry_count."),
        ("FR-11-06", "When starting a run, the backend shall authenticate, authorize workflows:run, load workflow, validate input schema, run governance pre-check, create queued run, write audit log, and return workflow_run_id."),
        ("FR-11-07", "While a run is executing, the backend shall iterate steps checking cancellation, permissions, governance, approvals, then execute agent/tool/evaluation/condition as applicable, persist outputs, emit events, and audit."),
        ("FR-11-08", "The backend shall support step types agent, tool, approval, condition, knowledge_search, memory_search, evaluation, transform, notification, and human_input (as implemented subset at minimum covering flagship DNA)."),
        ("FR-11-09", "When an Idempotency-Key is supplied for the same user and workflow start, the backend shall return the existing run instead of creating a duplicate."),
        ("FR-11-10", "The backend shall support cancel and retry operations according to policy."),
        ("FR-11-11", "If governance requires approval mid-run, then the backend shall transition the run to waiting_for_approval and pause irreversible progress."),
        ("FR-11-12", "When a run completes or fails, the backend shall persist terminal status, final output or error, and emit final events."),
        ("FR-11-13", "The backend shall expose list/get run, get steps, start, cancel, retry, and stream endpoints."),
    ],
    perf=[
        ("NFR-11-01", "Start-run API shall return run id quickly (target p95 under 1s local) even if execution continues asynchronously."),
        ("NFR-11-02", "Step state transitions shall be persisted before emitting completion events."),
    ],
    sec=[
        ("NFR-11-03", "Run inputs/outputs shall be access-controlled by organization and permissions."),
        ("NFR-11-04", "While run is unclassified or pre-check failed, the backend shall not execute irreversible tool actions."),
    ],
    ac=[
        ("AC-11-01", "Start flagship workflow creates run with version pin."),
        ("AC-11-02", "Steps appear with status transitions."),
        ("AC-11-03", "Duplicate Idempotency-Key returns same run id."),
        ("AC-11-04", "Cancel transitions run to cancelled when allowed."),
        ("AC-11-05", "Gate wait sets waiting_for_approval."),
    ],
    tv=[
        ("TV-11-01", "Integration: start → running → complete happy path.", "Automated"),
        ("TV-11-02", "Idempotency key test.", "Automated"),
        ("TV-11-03", "E1 path segment: run + gate wait.", "E2E"),
    ],
    trace=[
        ("backend.md §7.7–7.8", "FR-11-01 … FR-11-05"),
        ("backend.md §12 Execution Design", "FR-11-06 … FR-11-12"),
        ("backend.md §11.7", "FR-11-13"),
    ],
)
