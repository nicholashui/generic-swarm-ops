"""Requirement detail payloads BE-12..BE-24."""

from __future__ import annotations


def _d(**kwargs):
    return kwargs


DETAILS = {}

DETAILS["12"] = _d(
    scope_in=[
        "- Governance layer decisions: allow, deny, require_approval, require_evaluation, require_redaction.",
        "- Risk levels low/medium/high/critical with meanings.",
        "- Policy CRUD and check endpoints.",
        "- Pre-check before run and per-step/tool checks.",
    ],
    scope_out=[
        "- Approval request lifecycle storage details owned jointly with BE-13.",
        "- Full legal compliance program management UI.",
    ],
    stk=[
        ("STK-12-01", "Risk owners", "Policies encode when work may proceed."),
        ("STK-12-02", "Operators", "Predictable deny/approve requirements."),
        ("STK-12-03", "Auditors", "Policy checks are explainable."),
    ],
    fr=[
        ("FR-12-01", "The backend shall include a governance layer that decides whether a workflow can run, a step can execute, a tool can be used, data can be accessed, human approval is required, and output can be released."),
        ("FR-12-02", "The backend shall support risk levels low, medium, high, and critical with documented meanings."),
        ("FR-12-03", "When a governance check runs, the backend shall return an action among allow, deny, require_approval, require_evaluation, and require_redaction."),
        ("FR-12-04", "The backend shall support governance policies with conditions and actions (e.g. require approval for external email)."),
        ("FR-12-05", "The backend shall expose policy list/create/get/update/archive and check/preview endpoints."),
        ("FR-12-06", "When starting a workflow run, the backend shall run a governance pre-check before execution proceeds to irreversible work."),
        ("FR-12-07", "If governance returns deny, then the backend shall block the action and record the decision reason."),
        ("FR-12-08", "If governance returns require_approval, then the backend shall create or require an approval gate before continuing."),
        ("FR-12-09", "Governance policy changes shall be restricted to authorized roles and audited."),
        ("FR-12-10", "The backend shall support mapping structure autonomy risk tiers into runtime policy enforcement where configured (runtime tier policy)."),
    ],
    perf=[("NFR-12-01", "Policy check for typical rule sets shall complete under 50ms local.")],
    sec=[
        ("NFR-12-02", "Clients shall not override governance deny via request flags."),
        ("NFR-12-03", "Policy documents shall be protected from unauthorized update."),
    ],
    ac=[
        ("AC-12-01", "Policy check endpoint returns allow/deny/require_approval."),
        ("AC-12-02", "External-email style policy can force approval."),
        ("AC-12-03", "Deny blocks tool invocation."),
        ("AC-12-04", "Policy update writes audit event."),
    ],
    tv=[
        ("TV-12-01", "Unit: policy engine table tests.", "Automated"),
        ("TV-12-02", "Integration: pre-check on run start.", "Automated"),
        ("TV-12-03", "Negative: unauthorized policy update.", "Automated"),
    ],
    trace=[
        ("backend.md §7.9 Governance", "FR-12-01, FR-12-07 … FR-12-08"),
        ("backend.md §13 Governance Design", "FR-12-02 … FR-12-04"),
        ("backend.md §11.11", "FR-12-05"),
    ],
)

DETAILS["13"] = _d(
    scope_in=[
        "- Approval request entity and statuses pending/approved/rejected/expired/cancelled.",
        "- Approve/reject/reassign/decision endpoints.",
        "- Integration with run waiting_for_approval state.",
        "- Decision reason capture.",
    ],
    scope_out=["- Email notification productization (optional).", "- Frontend approval inbox UX details."],
    stk=[
        ("STK-13-01", "Reviewers", "Clear queue of pending approvals."),
        ("STK-13-02", "Operators", "Runs resume only after decision."),
        ("STK-13-03", "Auditors", "Decisions and reasons retained."),
    ],
    fr=[
        ("FR-13-01", "When human approval is required, the backend shall create an approval request linked to workflow_run and step when applicable."),
        ("FR-13-02", "Approval requests shall store approval ID, run ID, step ID, requested action, risk level, requester, assigned reviewer, decision, decision reason, created_at, and decided_at."),
        ("FR-13-03", "The backend shall support approval statuses pending, approved, rejected, expired, and cancelled."),
        ("FR-13-04", "When a reviewer approves, the backend shall record decision reason and allow the run to continue if still valid."),
        ("FR-13-05", "When a reviewer rejects, the backend shall record decision reason and stop or fail the gated action according to policy."),
        ("FR-13-06", "The backend shall support reassigning reviewers when permitted."),
        ("FR-13-07", "The backend shall expose list/get/approve/reject/reassign/decision endpoints."),
        ("FR-13-08", "While an approval is pending for a required gate, the backend shall not execute the gated irreversible action."),
        ("FR-13-09", "Only principals with approvals:approve or approvals:reject (or equivalent) may decide approvals."),
        ("FR-13-10", "Approval decisions shall generate audit events."),
    ],
    perf=[("NFR-13-01", "Approval decision API p95 under 300ms local excluding resume execution time.")],
    sec=[
        ("NFR-13-02", "Users shall not approve their own requests when policy forbids self-approval."),
        ("NFR-13-03", "Approval tokens or IDs shall not grant access outside assigned org."),
    ],
    ac=[
        ("AC-13-01", "Gated flagship run creates pending approval."),
        ("AC-13-02", "Approve resumes run path."),
        ("AC-13-03", "Reject prevents completion of gated action."),
        ("AC-13-04", "Decision reason required/stored."),
    ],
    tv=[
        ("TV-13-01", "Integration: approve path.", "Automated"),
        ("TV-13-02", "Integration: reject path.", "Automated"),
        ("TV-13-03", "E1: human gate segment.", "E2E"),
    ],
    trace=[
        ("backend.md §6.4 HITL", "FR-13-01, FR-13-08"),
        ("backend.md §7.9 Approvals", "FR-13-02 … FR-13-06"),
        ("backend.md §11.8", "FR-13-07"),
    ],
)

DETAILS["14"] = _d(
    scope_in=[
        "- Audit events for important actions listed in backend.md §7.13.",
        "- Audit fields and read-only query APIs.",
        "- Correlation with request_id and actor metadata.",
    ],
    scope_out=["- Long-term SIEM product integration (optional).", "- Immutable WORM storage vendor specifics."],
    stk=[
        ("STK-14-01", "Auditors", "Who did what, when, on which resource."),
        ("STK-14-02", "Security", "Forensics after incidents."),
        ("STK-14-03", "Operators", "Trace failed runs and approvals."),
    ],
    fr=[
        ("FR-14-01", "The backend shall generate audit logs for important actions including login, workflow create/update, run start/complete/fail, approval request/decision, knowledge upload/delete, memory access/update, governance rule change, agent tool use, API key create, and permission change."),
        ("FR-14-02", "Each audit log shall store audit ID, organization ID, actor user ID, actor type, action, resource type, resource ID, request ID, IP address, user agent, before/after state when applicable, metadata, status, and created_at."),
        ("FR-14-03", "Audit logs shall be read-only through the API (no client update/delete of audit history)."),
        ("FR-14-04", "The backend shall expose search/list and get audit endpoints restricted by audit:read."),
        ("FR-14-05", "When an important action succeeds or fails, the backend shall write audit status accordingly."),
        ("FR-14-06", "Audit writes shall not be skippable by clients via request parameters."),
        ("FR-14-07", "Sensitive audit metadata shall avoid storing secrets and raw credentials."),
    ],
    perf=[
        ("NFR-14-01", "Audit write shall not add more than 50ms p95 local to critical path under normal load."),
        ("NFR-14-02", "Audit search shall support filtering by time, actor, action, and resource."),
    ],
    sec=[
        ("NFR-14-03", "Only authorized roles may read audit logs."),
        ("NFR-14-04", "Audit storage integrity shall be protected from ordinary user APIs."),
    ],
    ac=[
        ("AC-14-01", "Starting a run creates audit event."),
        ("AC-14-02", "Approval decision creates audit event."),
        ("AC-14-03", "Audit update/delete endpoints are absent or forbidden."),
        ("AC-14-04", "Viewer without audit:read cannot list audits."),
    ],
    tv=[
        ("TV-14-01", "Integration: action → audit present.", "Automated"),
        ("TV-14-02", "Authz on audit read.", "Automated"),
        ("TV-14-03", "Review: no secrets in audit samples.", "Review"),
    ],
    trace=[
        ("backend.md §6.5 / §7.13", "FR-14-01 … FR-14-02"),
        ("backend.md §11.13", "FR-14-03 … FR-14-04"),
    ],
)

DETAILS["15"] = _d(
    scope_in=[
        "- Knowledge document lifecycle: upload/create, index, chunk, embed, search, archive/delete.",
        "- Document statuses uploaded/processing/indexed/failed/archived/deleted.",
        "- Retrieval pipeline with ACL filtering and provenance.",
        "- Tier-0/1 retrieval as-built; optional federation export.",
    ],
    scope_out=["- Full commercial LightRAG/Neo4j mesh (non-goal).", "- Frontend document viewer UX."],
    stk=[
        ("STK-15-01", "Knowledge managers", "Ingest and search policies/SOPs."),
        ("STK-15-02", "Agents/workflows", "Retrieve allowed context with provenance."),
        ("STK-15-03", "Security", "ACL and sensitivity enforcement."),
    ],
    fr=[
        ("FR-15-01", "The backend shall expose controlled access to knowledge sources including uploaded documents and markdown/policy materials."),
        ("FR-15-02", "The backend shall support document lifecycle statuses uploaded, processing, indexed, failed, archived, and deleted."),
        ("FR-15-03", "When a document is ingested, the backend shall support store → index job → extract → chunk → embed → store chunks/vector refs → mark indexed."),
        ("FR-15-04", "When search is requested, the backend shall check permissions, filter by organization/department/sensitivity/ACL, retrieve results, optionally rerank, return only allowed results, and audit sensitive access."),
        ("FR-15-05", "The backend shall expose list/create/get/delete/index/search knowledge endpoints."),
        ("FR-15-06", "The backend shall implement tiered retrieval starting at Tier 0 (keyword/hash embed + provenance) and Tier 1 multi-hop lite where enabled."),
        ("FR-15-07", "When returning retrieval results, the backend shall include provenance/source references where available."),
        ("FR-15-08", "If a caller lacks knowledge:read, then the backend shall deny search and document access."),
        ("FR-15-09", "Where K1-lite knowledge graph features are enabled, the backend shall support extract/operators and optional federation export without requiring Neo4j for core product bar."),
        ("FR-15-10", "Retrieved content shall be marked untrusted for prompt-injection safety in downstream consumers."),
    ],
    perf=[
        ("NFR-15-01", "Tier-0 search p95 under 1s local for small corpora."),
        ("NFR-15-02", "Indexing a small document shall complete without blocking the upload API response (async job acceptable)."),
    ],
    sec=[
        ("NFR-15-03", "Knowledge ACL shall be enforced server-side."),
        ("NFR-15-04", "Uploads shall be validated/sanitized for type and size limits."),
    ],
    ac=[
        ("AC-15-01", "Create document and search returns it when indexed/available."),
        ("AC-15-02", "Cross-org document not visible."),
        ("AC-15-03", "Search without permission denied."),
        ("AC-15-04", "Provenance fields present on retrieval results when sources exist."),
    ],
    tv=[
        ("TV-15-01", "Integration: ingest + search.", "Automated"),
        ("TV-15-02", "ACL negative test.", "Automated"),
        ("TV-15-03", "Tier-0 retrieval unit tests.", "Automated"),
    ],
    trace=[
        ("backend.md §7.10 Knowledge", "FR-15-01 … FR-15-05"),
        ("backend.md §14.1–14.2", "FR-15-03 … FR-15-04"),
        ("backend.md §24.3 Retrieval/K1", "FR-15-06 … FR-15-09"),
    ],
)

DETAILS["16"] = _d(
    scope_in=[
        "- Memory types/scopes: short_term, long_term, user/team/department/organization/workflow/agent memory.",
        "- Memory CRUD/search with ACL and sensitivity.",
        "- Expiration and embedding references.",
        "- Department isolation rules.",
    ],
    scope_out=["- Unbounded personalization product.", "- Cross-tenant memory sharing."],
    stk=[
        ("STK-16-01", "Agents", "Read/write allowed scopes only."),
        ("STK-16-02", "Security", "Restricted department memory isolation."),
        ("STK-16-03", "Operators", "Inspect memory records in ops console."),
    ],
    fr=[
        ("FR-16-01", "The backend shall manage agent and workflow memory with access control."),
        ("FR-16-02", "The backend shall support memory scopes including short_term, long_term, user_memory, team_memory, department_memory, organization_memory, workflow_memory, and agent_memory."),
        ("FR-16-03", "Each memory entry shall store memory ID, scope, owner, organization ID, department, content, metadata, embedding reference, sensitivity, expiration, and created_at."),
        ("FR-16-04", "When an agent requests memory outside its allowed scopes or department policy, the backend shall deny access."),
        ("FR-16-05", "The backend shall expose list/create/get/update/delete/search memory endpoints."),
        ("FR-16-06", "If memory sensitivity is restricted and agent department mismatches, then the backend shall deny access (policy example in backend.md)."),
        ("FR-16-07", "When memory is accessed or updated, the backend shall write audit events for sensitive operations."),
        ("FR-16-08", "Expired memory shall not be returned as active context after expiration processing."),
        ("FR-16-09", "Memory writes from untrusted sources shall be filterable/reviewable for high-impact scopes where policy requires."),
    ],
    perf=[("NFR-16-01", "Memory search within a scope p95 under 500ms local for small sets.")],
    sec=[
        ("NFR-16-02", "memory:read/write permissions shall be enforced."),
        ("NFR-16-03", "Memory content of other organizations shall never be returned."),
    ],
    ac=[
        ("AC-16-01", "Create memory and get by id."),
        ("AC-16-02", "Cross-department restricted deny path works."),
        ("AC-16-03", "Agent allowed scopes respected during run memory_reads."),
        ("AC-16-04", "Unauthorized memory:write denied."),
    ],
    tv=[
        ("TV-16-01", "Unit: scope policy matrix.", "Automated"),
        ("TV-16-02", "Integration: CRUD + search.", "Automated"),
        ("TV-16-03", "Flagship memory_reads do not fail mid-run for configured scopes.", "Automated"),
    ],
    trace=[
        ("backend.md §7.11 Memory", "FR-16-01 … FR-16-05"),
        ("backend.md §14.3 Memory Rules", "FR-16-04, FR-16-06"),
        ("backend.md §11.10", "FR-16-05"),
    ],
)

DETAILS["17"] = _d(
    scope_in=[
        "- Evaluation types: schema, business rules, policy, hallucination risk, completeness, formatting, safety, cost, human review.",
        "- Result statuses passed/failed/warning/requires_review.",
        "- Linkage to runs/steps/outputs.",
        "- Manual run evaluation endpoints and corpus evaluation for evolution.",
    ],
    scope_out=["- External public leaderboard hosting.", "- Replacing governance deny with soft eval warnings only."],
    stk=[
        ("STK-17-01", "Quality owners", "Block unsafe outputs."),
        ("STK-17-02", "Evolution", "Corpus scores for variants."),
        ("STK-17-03", "Operators", "See eval results on runs."),
    ],
    fr=[
        ("FR-17-01", "The backend shall evaluate important outputs before returning or releasing them when evaluation policy requires."),
        ("FR-17-02", "The backend shall support evaluation types including schema validation, business rule validation, policy compliance, hallucination risk check, completeness check, formatting check, safety check, cost check, and human review."),
        ("FR-17-03", "Evaluation results shall use statuses passed, failed, warning, and requires_review."),
        ("FR-17-04", "Evaluation results shall link to workflow run, step, agent output, and/or final output as applicable."),
        ("FR-17-05", "The backend shall expose list/get evaluations, run evaluation manually, and get evaluations for a workflow run."),
        ("FR-17-06", "If a required evaluation fails, then the backend shall block release/promotion paths that depend on that evaluation."),
        ("FR-17-07", "The backend shall support corpus evaluation used by evolution sandbox fitness scoring."),
        ("FR-17-08", "Evaluation runs shall be persisted for auditability and comparison."),
    ],
    perf=[
        ("NFR-17-01", "Schema/business rule evals shall complete under 200ms local for typical payloads."),
        ("NFR-17-02", "Corpus evaluation may be asynchronous for large sets but shall report status."),
    ],
    sec=[
        ("NFR-17-03", "Evaluation configuration shall not be mutable by unauthorized roles."),
        ("NFR-17-04", "Eval results shall not expose secrets from fixtures."),
    ],
    ac=[
        ("AC-17-01", "Manual evaluation endpoint returns persisted result."),
        ("AC-17-02", "Failed required eval blocks unsafe release path in tests."),
        ("AC-17-03", "Run-linked evaluations queryable by run id."),
        ("AC-17-04", "Corpus eval callable for a sandbox variant."),
    ],
    tv=[
        ("TV-17-01", "Unit: schema eval pass/fail.", "Automated"),
        ("TV-17-02", "Integration: evaluations on run.", "Automated"),
        ("TV-17-03", "Corpus eval smoke for evolution.", "Automated"),
    ],
    trace=[
        ("backend.md §7.12 Evaluation", "FR-17-01 … FR-17-06"),
        ("backend.md §11.12", "FR-17-05"),
        ("backend.md §24.3 Evolution corpus", "FR-17-07"),
    ],
)

DETAILS["18"] = _d(
    scope_in=[
        "- Process intelligence APIs: metrics, workflow performance, bottlenecks, costs, failures, approval delays.",
        "- Aggregation from workflow run data.",
        "- Disk artifacts under business/process-intelligence/.",
    ],
    scope_out=["- Five independent always-on LLM PI agents.", "- Full commercial process mining suite."],
    stk=[
        ("STK-18-01", "Ops leads", "See bottlenecks and failure patterns."),
        ("STK-18-02", "Architects", "Empirical traces not only opinions."),
        ("STK-18-03", "Evolution", "Signals for improvement opportunities."),
    ],
    fr=[
        ("FR-18-01", "The backend shall expose process intelligence APIs for workflow performance analytics, bottleneck detection, failure patterns, average duration, approval delays, agent performance, cost by workflow/department, task success rate, and automation opportunities as data allows."),
        ("FR-18-02", "Initial process APIs may aggregate workflow run data without requiring external process mining clusters."),
        ("FR-18-03", "When events are ingested or runs complete, the backend shall be able to write process-intelligence disk artifacts under business/process-intelligence/."),
        ("FR-18-04", "The backend shall expose endpoints for metrics, workflow-performance, bottlenecks, costs, and failures (and related summaries as implemented)."),
        ("FR-18-05", "Process intelligence services shall not directly mutate production workflow DNA."),
        ("FR-18-06", "Access to process intelligence summaries shall require appropriate authorization."),
    ],
    perf=[("NFR-18-01", "Aggregate metrics for small histories shall return under 1s p95 local.")],
    sec=[("NFR-18-02", "PI APIs shall not leak cross-organization run details.")],
    ac=[
        ("AC-18-01", "Metrics endpoint returns structured summary."),
        ("AC-18-02", "Bottlenecks/failures endpoints respond for seeded data."),
        ("AC-18-03", "PI artifacts directory receives outputs on ingest/run paths as implemented."),
        ("AC-18-04", "Unauthorized access denied."),
    ],
    tv=[
        ("TV-18-01", "API smoke for processes routes.", "Automated"),
        ("TV-18-02", "Artifact write path unit/integration.", "Automated"),
        ("TV-18-03", "Authz negative test.", "Automated"),
    ],
    trace=[
        ("backend.md §7.14 Process Intelligence", "FR-18-01 … FR-18-05"),
        ("backend.md §11.14", "FR-18-04"),
        ("backend.md §24.3 PI", "FR-18-03"),
    ],
)

DETAILS["19"] = _d(
    scope_in=[
        "- SSE streaming for run events and event types from §7.18.",
        "- Health, liveness, readiness, metrics endpoints.",
        "- Structured logs, request metrics, security headers, CORS.",
    ],
    scope_out=["- Full OpenTelemetry vendor lock.", "- Bidirectional WebSocket agent chat product (optional later)."],
    stk=[
        ("STK-19-01", "Frontend", "Live run progress."),
        ("STK-19-02", "Ops", "Ready/live probes."),
        ("STK-19-03", "Support", "Correlated logs via request_id."),
    ],
    fr=[
        ("FR-19-01", "The backend shall support real-time progress updates for workflow runs via Server-Sent Events (WebSocket optional later)."),
        ("FR-19-02", "Streaming shall emit events including run.started, run.status_changed, step.started/completed/failed, approval.requested/approved/rejected, evaluation.completed, run.completed/failed, and log.message as applicable."),
        ("FR-19-03", "Each stream event shall include workflow_run_id, timestamps, and payload fields needed by clients."),
        ("FR-19-04", "The backend shall expose health, liveness, and readiness endpoints."),
        ("FR-19-05", "Readiness shall report database connectivity status (e.g. postgres) when configured."),
        ("FR-19-06", "The backend shall emit structured API request logs including request_id."),
        ("FR-19-07", "The backend shall expose basic metrics suitable for operational monitoring."),
        ("FR-19-08", "The backend shall apply basic security headers and configured CORS policy."),
        ("FR-19-09", "If a client is not authorized for a run, then the backend shall not stream that run's events."),
    ],
    perf=[
        ("NFR-19-01", "SSE shall deliver step completion events promptly after persistence (target under 1s local)."),
        ("NFR-19-02", "Health endpoints shall respond under 100ms when process is healthy."),
    ],
    sec=[
        ("NFR-19-03", "Stream endpoints shall require authentication and authorization."),
        ("NFR-19-04", "Logs shall redact secrets and tokens."),
    ],
    ac=[
        ("AC-19-01", "Stream endpoint exists for workflow runs."),
        ("AC-19-02", "Ready reports database status."),
        ("AC-19-03", "Logs include request_id for sample requests."),
        ("AC-19-04", "Unauthorized stream denied."),
    ],
    tv=[
        ("TV-19-01", "Health/live/ready tests.", "Automated"),
        ("TV-19-02", "SSE or event emission unit tests.", "Automated"),
        ("TV-19-03", "Auth on stream.", "Automated"),
    ],
    trace=[
        ("backend.md §7.18 Streaming", "FR-19-01 … FR-19-03"),
        ("backend.md §17 Observability", "FR-19-04 … FR-19-07"),
        ("backend.md §8.4", "FR-19-06 … FR-19-08"),
    ],
)

DETAILS["20"] = _d(
    scope_in=[
        "- Evolution variants list/propose/evaluate/promote/rollback.",
        "- Fitness/population archive.",
        "- sandbox_only enforcement; no host code rewrite.",
        "- Canary then promote gates.",
    ],
    scope_out=["- DGM-style host application self-rewrite (non-goal).", "- Silent production DNA replacement."],
    stk=[
        ("STK-20-01", "Evolution manager role", "Propose and test safely."),
        ("STK-20-02", "Risk owners", "No direct prod mutation."),
        ("STK-20-03", "Operators", "Canary and rollback controls."),
    ],
    fr=[
        ("FR-20-01", "The backend shall expose evolution controls that enforce sandbox-only mutation of production Workflow DNA."),
        ("FR-20-02", "The backend shall support listing and proposing evolution variants marked sandbox_only."),
        ("FR-20-03", "When a variant is evaluated, the backend shall run corpus/fitness evaluation and persist scores."),
        ("FR-20-04", "The backend shall support canary promote to limited scope and full promote only after gates."),
        ("FR-20-05", "The backend shall support rollback of canary/promoted changes."),
        ("FR-20-06", "The backend shall expose a fitness/population archive endpoint."),
        ("FR-20-07", "The evolution manager path shall never rewrite host application source code."),
        ("FR-20-08", "The evolution manager path shall never silently replace production DNA without versioned promote gates."),
        ("FR-20-09", "If safety or evaluation gates fail, then the backend shall refuse promotion."),
        ("FR-20-10", "Evolution actions shall be authorized and audited."),
    ],
    perf=[("NFR-20-01", "Propose variant API returns quickly; heavy eval may be async but must be trackable.")],
    sec=[
        ("NFR-20-02", "Only authorized roles may promote variants."),
        ("NFR-20-03", "Sandbox variants shall not execute as production DNA until promoted."),
    ],
    ac=[
        ("AC-20-01", "Propose creates sandbox_only variant."),
        ("AC-20-02", "Evaluate persists fitness result."),
        ("AC-20-03", "Promote without eval gates fails."),
        ("AC-20-04", "Rollback restores prior version path."),
        ("AC-20-05", "Archive lists ranked variants."),
    ],
    tv=[
        ("TV-20-01", "Evolution API unit/integration suite.", "Automated"),
        ("TV-20-02", "Negative: direct prod mutation attempt rejected.", "Automated"),
        ("TV-20-03", "Canary/rollback path test.", "Automated"),
    ],
    trace=[
        ("backend.md §7.15 Evolution", "FR-20-01 … FR-20-08"),
        ("backend.md §11.15", "FR-20-02 … FR-20-06"),
        ("backend.md §24.3 / non-goals", "FR-20-07, scope_out"),
    ],
)

DETAILS["21"] = _d(
    scope_in=[
        "- Reflect on runs, lesson library, auto-propose sandbox variants.",
        "- Optional LLM critic feature flag.",
        "- Skill sandbox write under _sandbox with explicit promote.",
        "- Loop DNA runner start/status.",
        "- Auto-reflect configuration flag.",
    ],
    scope_out=["- Unsupervised auto-promote to production.", "- Host code rewriting loops."],
    stk=[
        ("STK-21-01", "Operators", "Improve pipeline after runs."),
        ("STK-21-02", "Researchers", "Lessons and reflective loops."),
        ("STK-21-03", "Risk", "All proposals remain sandboxed."),
    ],
    fr=[
        ("FR-21-01", "The backend shall support reflecting on a completed or failed run to extract lessons."),
        ("FR-21-02", "The backend shall maintain a lesson library listable and scorable by utility."),
        ("FR-21-03", "The backend shall support auto-propose of sandbox DNA variants from lessons without mutating production DNA directly."),
        ("FR-21-04", "Where GENERIC_SWARM_LLM_CRITIC_ENABLED (or equivalent) is enabled and configured, the backend shall allow an optional LLM critic path."),
        ("FR-21-05", "The backend shall support skill sandbox writes under a _sandbox area with explicit promote only."),
        ("FR-21-06", "The backend shall support loop DNA runner start and status endpoints."),
        ("FR-21-07", "When GENERIC_SWARM_AUTO_REFLECT is enabled, the backend shall auto-reflect on terminal run statuses."),
        ("FR-21-08", "If a self-improvement action would mutate production DNA directly, then the backend shall reject it and require sandbox proposal instead."),
        ("FR-21-09", "Self-improvement actions shall be authorized and produce audit/lesson provenance."),
    ],
    perf=[("NFR-21-01", "Reflect on a single run shall complete within a few seconds local without optional LLM critic.")],
    sec=[
        ("NFR-21-02", "LLM critic shall not receive secrets from env dumps."),
        ("NFR-21-03", "Skill promote shall require privileged authorization."),
    ],
    ac=[
        ("AC-21-01", "POST reflect creates lessons for a run."),
        ("AC-21-02", "Auto-propose creates sandbox variant only."),
        ("AC-21-03", "Skill sandbox write not visible as promoted until promote."),
        ("AC-21-04", "Loop runner start returns run/loop id."),
    ],
    tv=[
        ("TV-21-01", "test_full_improvement_backlog or equivalent.", "Automated"),
        ("TV-21-02", "Reflect → propose chain.", "Automated"),
        ("TV-21-03", "E1 improve segment.", "E2E"),
    ],
    trace=[
        ("backend.md §7.16 Self-Improvement", "FR-21-01 … FR-21-07"),
        ("backend.md §11.16", "FR-21-01 … FR-21-06"),
        ("backend.md §24.3 Self-improvement", "FR-21-08"),
    ],
)

DETAILS["22"] = _d(
    scope_in=[
        "- Production DNA validators: risk tiers, human gates, rollback, provenance fields.",
        "- business:validate integration and runtime activate_workflow_version / production_ready checks.",
        "- structure_validators module behaviour.",
        "- Rejection → lesson learning without production mutation.",
    ],
    scope_out=["- Authoring all business DNA content.", "- Soft-warning-only production activate."],
    stk=[
        ("STK-22-01", "Governance", "Unsafe DNA never activates."),
        ("STK-22-02", "Engineers", "Deterministic validator errors."),
        ("STK-22-03", "Learning loop", "Rejections become lessons."),
    ],
    fr=[
        ("FR-22-01", "Before a workflow version is activated or marked production_ready, the backend shall run structure-aligned production DNA validators."),
        ("FR-22-02", "Validators shall check risk tier presence, human gate requirements for high-risk/irreversible steps, rollback declarations, and provenance-related fields as specified by structure_validators."),
        ("FR-22-03", "The backend shall integrate with business:validate style checks for business corpus DNA where applicable."),
        ("FR-22-04", "If validation fails, then the backend shall reject activation/production_ready transition and shall not partially activate unsafe DNA."),
        ("FR-22-05", "When validation rejects DNA, the backend shall support recording a learnable rejection lesson without mutating production DNA."),
        ("FR-22-06", "Validator results shall be explicit and machine-readable for clients and tests."),
        ("FR-22-07", "Production DNA checks shall run in runtime paths for activate_workflow_version and production_ready create/update as implemented."),
    ],
    perf=[("NFR-22-01", "Validator suite for a single DNA document shall complete under 200ms local.")],
    sec=[("NFR-22-02", "Clients cannot bypass validators via force flags unless a break-glass role is explicitly designed and audited (default: no bypass).")],
    ac=[
        ("AC-22-01", "Valid flagship DNA activates."),
        ("AC-22-02", "DNA missing required gates fails activation."),
        ("AC-22-03", "Negative DNA fixtures covered by unit tests."),
        ("AC-22-04", "Rejection can create lesson record."),
    ],
    tv=[
        ("TV-22-01", "test_structure_sdd_validators or equivalent.", "Automated"),
        ("TV-22-02", "Activate path integration tests.", "Automated"),
        ("TV-22-03", "Negative DNA fixtures.", "Automated"),
    ],
    trace=[
        ("backend.md §7.17 Production DNA Safety", "FR-22-01 … FR-22-07"),
        ("backend.md §24.3 DNA production safety", "FR-22-01, FR-22-07"),
    ],
)

DETAILS["23"] = _d(
    scope_in=[
        "- Cross-cutting security NFRs: authn/z on protected routes, validation, upload sanitization, secrets, rate limits.",
        "- Prompt injection protections.",
        "- Data access control rules.",
        "- Reliability/scalability/observability maintainability NFRs from §8.",
    ],
    scope_out=["- Full red-team program operations (process), though tests may exist.", "- External WAF vendor configuration."],
    stk=[
        ("STK-23-01", "Security team", "Defense in depth beyond model alignment."),
        ("STK-23-02", "Ops", "Rate limits and reliability basics."),
        ("STK-23-03", "All API consumers", "Safe defaults."),
    ],
    fr=[
        ("FR-23-01", "The backend shall require authentication for protected routes and enforce authorization on every protected resource."),
        ("FR-23-02", "The backend shall validate all request bodies and sanitize file uploads."),
        ("FR-23-03", "The backend shall protect secrets and never commit them to source or return them in APIs."),
        ("FR-23-04", "The backend shall rate limit sensitive endpoints including auth and workflow-write paths."),
        ("FR-23-05", "When handling retrieved or user content for LLMs, the backend shall treat content as untrusted data, separate instructions from data, and limit blast radius."),
        ("FR-23-06", "The backend shall assume prompt injection remains possible and shall enforce security outside the LLM with deterministic controls."),
        ("FR-23-07", "The backend shall apply data access control so users only access authorized org/department resources."),
        ("FR-23-08", "The backend shall meet reliability expectations for graceful error handling and non-corrupt state on failures."),
        ("FR-23-09", "The backend shall support horizontal scaling of stateless API processes when shared durable state is in Postgres."),
        ("FR-23-10", "The backend shall maintain layered architecture for maintainability (routes → services → domain → infrastructure)."),
    ],
    perf=[
        ("NFR-23-01", "Rate limiter shall not add more than 5ms p95 local overhead when enabled."),
        ("NFR-23-02", "p95 API latency targets for simple CRUD remain under 300ms local excluding external LLM calls."),
    ],
    sec=[
        ("NFR-23-03", "Security headers shall be applied on API responses."),
        ("NFR-23-04", "Dependency and secret scanning are recommended in CI; secrets must not be hardcoded."),
    ],
    ac=[
        ("AC-23-01", "Protected route without auth → 401."),
        ("AC-23-02", "Rate limit triggers on abusive auth attempts in tests or documented behaviour."),
        ("AC-23-03", "Upload validation rejects disallowed types/sizes where implemented."),
        ("AC-23-04", "Prompt/tool path treats retrieved content as untrusted in design tests."),
    ],
    tv=[
        ("TV-23-01", "Security unit tests: authz, validation.", "Automated"),
        ("TV-23-02", "Rate limit tests for sensitive routes.", "Automated"),
        ("TV-23-03", "Injection-oriented negative tests for tool/knowledge path.", "Automated"),
    ],
    trace=[
        ("backend.md §8 NFRs", "FR-23-01 … FR-23-10"),
        ("backend.md §16 Security Design", "FR-23-05 … FR-23-07"),
    ],
)

DETAILS["24"] = _d(
    scope_in=[
        "- Testing strategy: unit, integration, e2e, security, load (as applicable).",
        "- MVP minimum backend capabilities.",
        "- Definition of Done including product bar mark ~100 additions.",
        "- E1 operator path proof.",
        "- Explicit non-goals list alignment with structure.md §12.4.",
    ],
    scope_out=["- Always-on multi-worker Temporal cluster as hard requirement.", "- Infinite business leaf content."],
    stk=[
        ("STK-24-01", "Release managers", "Clear DoD and evidence."),
        ("STK-24-02", "QA", "Layered test protocols."),
        ("STK-24-03", "Product", "Non-goals do not block mark ~100."),
    ],
    fr=[
        ("FR-24-01", "The backend shall maintain unit tests for permission logic, governance evaluation, workflow state transitions, schema validation, memory rules, knowledge filtering, evaluation rules, and audit event creation."),
        ("FR-24-02", "The backend shall maintain integration tests for API routes with database, workflow execution, approvals, knowledge/memory, workers, and audit creation."),
        ("FR-24-03", "The backend shall maintain end-to-end tests for login → start workflow → approval → completion → evaluation/audit paths."),
        ("FR-24-04", "The backend shall maintain security tests for unauthorized access, cross-org access, role failures, invalid/expired tokens, restricted memory/knowledge, and tool permission failures."),
        ("FR-24-05", "The MVP backend shall include authentication, users/orgs/RBAC, audit logs, agent registry, workflow definitions/runs, worker/execution, basic governance, approvals, run status/steps, basic knowledge, and OpenAPI."),
        ("FR-24-06", "For product bar mark ~100, the backend shall additionally provide Postgres primary persistence, local tool adapters with tool_effects, evolution sandbox APIs, self-improvement APIs, production DNA validation, and a passing E1 operator path test."),
        ("FR-24-07", "The E1 path shall cover login → create/use agent → flagship run → human gate → complete → reflect → propose → evaluate → canary (as implemented in test_e1_operator_path)."),
        ("FR-24-08", "The following shall be treated as non-goals for mark ~100: full commercial LightRAG/Neo4j mesh, live external CRM/email/billing SaaS adapters, DGM host self-rewrite, always-on multi-worker cluster requirement, ephemeral per-tool OAuth broker, infinite business leaf fill."),
        ("FR-24-09", "Test evidence and status shall be linkable from status.md / mark verification docs."),
    ],
    perf=[
        ("NFR-24-01", "Unit suite shall be runnable in local dev without external paid APIs."),
        ("NFR-24-02", "E2E E1 shall complete within CI-reasonable time on local stack."),
    ],
    sec=[
        ("NFR-24-03", "Security tests shall not require disabling auth globally."),
        ("NFR-24-04", "Test fixtures shall not embed real production secrets."),
    ],
    ac=[
        ("AC-24-01", "Unit discover suite green."),
        ("AC-24-02", "E2E E1 path green."),
        ("AC-24-03", "DoD checklist items 1–26 from backend.md §22 (including product bar additions) are evidenced."),
        ("AC-24-04", "Non-goals documented and not filed as product-bar defects."),
    ],
    tv=[
        ("TV-24-01", "python -m unittest discover unit.", "Automated"),
        ("TV-24-02", "python -m unittest discover e2e.", "Automated"),
        ("TV-24-03", "Review: map DoD to tests/docs.", "Review"),
    ],
    trace=[
        ("backend.md §19 Testing", "FR-24-01 … FR-24-04"),
        ("backend.md §21–22 MVP/DoD", "FR-24-05 … FR-24-06"),
        ("backend.md §24 Implementation Mapping", "FR-24-07 … FR-24-09"),
    ],
)
