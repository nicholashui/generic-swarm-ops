#!/usr/bin/env python3
"""Generate public/docs/<route>/spec.md and user_guide.md for each ops console route.

Content is grounded in structure.md / backend.md / frontend.md product model:
Safety > Auditability > Correctness > Efficiency > Autonomy.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "public" / "docs"

# Each entry: (route path under /app, title, permission, surface summary, api surface, operator steps)
ROUTES: list[dict] = [
    {
        "path": "app",
        "title": "Dashboard",
        "permission": "workflows:read (and related read scopes for tiles)",
        "purpose": "Command surface for governed automation: metrics, pending approvals, recent workflows, knowledge freshness, and onboarding checklist.",
        "ui": [
            "Metric cards (agents, workflows, pending approvals, audit volume)",
            "Pending approvals table with deep links",
            "Recent workflows / knowledge status",
            "Onboarding checklist for first-time operators",
            "Primary actions: Create agent, Create workflow",
        ],
        "backend": [
            "Aggregates live lists via product-data facade when not in demo mode",
            "GET /agents, /workflows, /approvals, /knowledge, /audit-logs, /memory, /evaluations, /processes",
            "Auth: bearer via same-origin /api/proxy (httpOnly cookie on BFF login)",
        ],
        "architecture": [
            "Maps to structure.md Execution + Governance + Knowledge visibility",
            "Does not execute agents directly; backend remains control plane",
            "Design priorities: Safety → Auditability → Correctness → Efficiency → Autonomy",
        ],
        "guide_steps": [
            "Sign in at /login (POST credentials; never put password in the URL).",
            "Confirm metrics load (live mode requires backend health ready with Postgres).",
            "Open a pending approval or workflow from the tables when attention is needed.",
            "Use header help (panel icon) for Spec / User guide tabs on this screen.",
            "Use the book icon for a full-page document view of the same markdown.",
        ],
    },
    {
        "path": "app/agents",
        "title": "Agents catalog",
        "permission": "agents:read",
        "purpose": "List organization AI workers with status, tools, knowledge access, and ownership before exposing them to live workflows.",
        "ui": [
            "Domain pack summary panel (optional domain context)",
            "Searchable agent table (name, owner, tools, knowledge, status, updated)",
            "Metrics: total / active / draft / knowledge-linked",
            "Create agent action → /app/agents/new",
        ],
        "backend": [
            "GET /api/v1/agents",
            "Agents declare allowed tools and memory scopes; ALC fields may gate activation",
            "No direct LLM calls from the UI",
        ],
        "architecture": [
            "Execution layer roster (structure.md §4)",
            "Domain packs may register additional agents (business/<domain_id>/)",
        ],
        "guide_steps": [
            "Open Agents from the sidebar.",
            "Filter or search by owner, status, or knowledge access.",
            "Inspect an agent row for tool count and knowledge linkage.",
            "Click Create agent when you have agents:write (or admin) rights.",
            "Prefer draft → review → active; do not activate high-risk agents without governance checks.",
        ],
    },
    {
        "path": "app/agents/new",
        "title": "Create agent",
        "permission": "agents:write (or create)",
        "purpose": "Form to register a new agent with deliberate tool, memory, and knowledge scope.",
        "ui": [
            "Create form (name, description, tools, memory scopes, knowledge sources, approval threshold)",
            "Submit via FormRouteActions → POST /agents",
            "Validation errors surfaced with request_id when available",
        ],
        "backend": [
            "POST /api/v1/agents",
            "Server enforces RBAC and schema; least-privilege tools recommended",
        ],
        "architecture": [
            "Bounded autonomy: agents only receive tools listed in DNA/runtime config",
            "Memory scopes must match allowed_memory_scopes for ALC-gated agents",
        ],
        "guide_steps": [
            "Enter a clear agent name and objective description.",
            "Select only the tools required for the role (least privilege).",
            "Attach knowledge/memory scopes intentionally.",
            "Submit and verify the agent appears in the catalog as draft or registered.",
            "Activate only after ALC / inventory gates pass when required.",
        ],
    },
    {
        "path": "app/domains",
        "title": "Domains",
        "permission": "workflows:read",
        "purpose": "Multi-domain pack surface: domain inventory, video N3 roster, workflow recommendation, and special-skill registry views.",
        "ui": [
            "DomainPackPanel — pack/agent inventory context",
            "VideoN3RosterPanel — N3 retention roster status",
            "RecommendWorkflowPanel — free-text brief → ranked DNA recommendation",
            "SpecialSkillsPanel — pack special-skill integrations from REGISTRY",
        ],
        "backend": [
            "GET /domains/video/n3-status, /domains/video/archetypes",
            "POST /domains/video/recommend-workflow",
            "GET /domains/video/special-skills",
            "Domain registration APIs / inventory gates (CLI + API waves)",
        ],
        "architecture": [
            "Domain pack extension layer (structure.md §0 Domain Pack)",
            "business/<domain_id>/ with manifest, agents, evals; video pack is first rich pack",
            "Recommend path is real selector logic — not mock when live mode is on",
        ],
        "guide_steps": [
            "Open Domains from the sidebar.",
            "Review pack inventory and N3 roster health.",
            "Paste a production brief into Recommend Workflow and inspect ranked DNA options.",
            "Browse special skills available to the pack; do not enable skills that fail security vetting.",
            "Register new packs only through approved inventory + schema gates.",
        ],
    },
    {
        "path": "app/tools",
        "title": "Tools",
        "permission": "tools:read",
        "purpose": "Catalog of tool adapters available to workflow steps (CRM, billing, email, parsers, etc.).",
        "ui": [
            "Tool list with category, status, last used, usage",
            "Detail deep links for individual tools",
        ],
        "backend": [
            "GET /api/v1/tools",
            "Tool execution only through runtime adapters producing tool_effects",
            "Permission broker scopes credentials per task",
        ],
        "architecture": [
            "Execution layer tool adapters; durable tool_effects for audit/rollback",
            "System prompts are not security controls — permissions enforced outside the LLM",
        ],
        "guide_steps": [
            "Open Tools to review connected integrations.",
            "Check status (connected / error) before assigning tools to agents.",
            "Open a tool detail when diagnosing failed workflow steps.",
            "Never grant irreversible tools without human gates in Workflow DNA.",
        ],
    },
    {
        "path": "app/workflows",
        "title": "Workflows",
        "permission": "workflows:read",
        "purpose": "List Workflow DNA definitions available for governed execution.",
        "ui": [
            "Workflow table / cards with status and metadata",
            "Create workflow → /app/workflows/new",
            "Run now on detail (separate route)",
            "Flagship example: wf_customer_onboarding_v12",
        ],
        "backend": [
            "GET /api/v1/workflows",
            "POST /api/v1/workflows/{id}/run with input_payload",
            "DNA validation: human gates, rollback, provenance, audit writes",
        ],
        "architecture": [
            "Workflow DNA is a bounded state graph (structure.md Execution layer)",
            "Evolution never mutates production DNA directly",
        ],
        "guide_steps": [
            "Open Workflows and locate the process you need (e.g. customer onboarding).",
            "Open detail to review steps, gates, and fitness metrics.",
            "Use Run now with a valid payload (flagship requires case_id).",
            "Monitor the run under Workflow runs; approve human gates as required.",
            "Create new DNA only with rollback and verification declared.",
        ],
    },
    {
        "path": "app/workflows/new",
        "title": "Create workflow",
        "permission": "workflows:write",
        "purpose": "Form to create a new Workflow DNA record through the live API.",
        "ui": [
            "Create form fields for identity and configuration",
            "POST via FormRouteActions → /workflows",
        ],
        "backend": [
            "POST /api/v1/workflows",
            "Server-side schema and governance constraints",
        ],
        "architecture": [
            "New DNA should follow bounded steps + guardrails + rollback pattern",
            "Prefer validation commands: npm run business:validate (repo root)",
        ],
        "guide_steps": [
            "Fill identity (id/name/domain/objective) carefully; encode version in id when appropriate.",
            "Declare steps, tools, and human gates for irreversible actions.",
            "Submit and open the new workflow to verify it lists correctly.",
            "Do not promote untested DNA to high autonomy tiers.",
        ],
    },
    {
        "path": "app/workflow-runs",
        "title": "Workflow runs",
        "permission": "workflows:read",
        "purpose": "Template for run detail screens (/app/workflow-runs/{runId}) — events, improve pipeline, pause/resume/cancel.",
        "ui": [
            "WorkflowRunConsole with event stream",
            "ImproveRunButton (reflect → propose → evaluate → canary)",
            "Lifecycle: pause / resume / cancel / expire when allowed",
        ],
        "backend": [
            "GET /workflow-runs, /workflow-runs/{id}/stream",
            "POST improve/reflect, improvement/auto-propose, evolution evaluate/promote",
            "POST pause/resume/cancel/expire",
        ],
        "architecture": [
            "Runtime walks DNA graph; tool_effects + audit on each step",
            "Self-improvement writes lessons; variants stay sandbox until approved",
        ],
        "guide_steps": [
            "Open a run from a workflow detail or dashboard link.",
            "Watch events for step progress and human-gate waits.",
            "Approve blocking gates from Approvals when status is awaiting_approval.",
            "Use Improve only to propose sandbox variants — never expect silent production mutation.",
            "Cancel or expire stuck runs per ops policy.",
        ],
    },
    {
        "path": "app/evolution",
        "title": "Evolution archive",
        "permission": "workflows:read",
        "purpose": "Sandbox population archive: variants ranked by fitness; evaluate/canary without silent production mutation. Lesson utility feeds coevolution fitness.",
        "ui": [
            "EvolutionArchivePanel",
            "LessonUtilityPanel",
            "Evaluate / canary promote actions when authorized",
        ],
        "backend": [
            "GET /evolution/archive, /evolution/variants",
            "POST /evolution/variants/{id}/evaluate, /promote",
            "POST /evolution/coevolution/run",
            "GET /improvement/lesson-utility",
        ],
        "architecture": [
            "Evolution layer: propose → test → canary → promote/rollback (structure.md §5)",
            "Non-negotiable: never mutate production DNA directly",
            "Fitness combines quality, safety, compliance, efficiency, human satisfaction minus risk/latency/cost",
        ],
        "guide_steps": [
            "Open Evolution to browse sandbox variants.",
            "Inspect fitness and evaluation evidence before canary.",
            "Run evaluate on a variant; only canary/promote with sufficient evidence and permissions.",
            "Review lesson utility for coevolution signals.",
            "If a canary fails metrics, roll back — do not force promote.",
        ],
    },
    {
        "path": "app/approvals",
        "title": "Approvals queue",
        "permission": "approvals:read",
        "purpose": "Human decision gates for high-risk or irreversible workflow steps.",
        "ui": [
            "Queue table (title, workflow, requester, risk, status)",
            "Detail with ApprovalDecisionPanel (approve/reject + reason)",
        ],
        "backend": [
            "GET /api/v1/approvals",
            "POST /api/v1/approvals/{id}/decision",
            "Audit events recorded for every decision",
        ],
        "architecture": [
            "Governance risk tiers 0–5; irreversible tools require gates",
            "Approvals implement human-in-the-loop for Safety priority",
        ],
        "guide_steps": [
            "Open Approvals when a run is waiting.",
            "Read risk, workflow context, and proposed action carefully.",
            "Approve only when policy and evidence support the action; otherwise reject with a clear reason.",
            "Confirm the workflow run continues or fails closed after your decision.",
        ],
    },
    {
        "path": "app/knowledge",
        "title": "Knowledge hub",
        "permission": "knowledge:read",
        "purpose": "Hub for sources, indexed documents, and search — grounded retrieval for agents.",
        "ui": [
            "Cards linking to sources, documents, search",
            "Freshness and failure signals",
        ],
        "backend": [
            "GET /knowledge, /knowledge/search",
            "Tiered retrieval (vector → graph → hierarchical) per structure.md Knowledge layer",
            "Provenance required for trusted rules",
        ],
        "architecture": [
            "Eight memory types + retrieval tiers 0–2",
            "Escalation: start cheap (tier 0), escalate only when needed",
        ],
        "guide_steps": [
            "Open Knowledge to assess corpus health.",
            "Use Sources to manage connectors; Documents for corpus rows; Search for ad-hoc queries.",
            "Investigate failed ingestions before relying on agents that need those sources.",
            "Prefer documents with clear provenance for compliance-sensitive workflows.",
        ],
    },
    {
        "path": "app/knowledge/sources",
        "title": "Knowledge sources",
        "permission": "knowledge:read",
        "purpose": "Connected knowledge sources with type, status, document counts, last sync, errors.",
        "ui": [
            "Sources table + metrics",
            "Detail routes for individual sources",
        ],
        "backend": [
            "Knowledge source inventory via knowledge APIs / service layer",
            "Sync status drives freshness indicators",
        ],
        "architecture": [
            "Sources feed semantic/procedural knowledge with provenance records",
        ],
        "guide_steps": [
            "Review source status and last sync times.",
            "Open a source with elevated errorCount to diagnose ingestion.",
            "Do not mark workflows production_ready if critical sources are failing.",
        ],
    },
    {
        "path": "app/knowledge/documents",
        "title": "Indexed documents",
        "permission": "knowledge:read",
        "purpose": "Document corpus used for grounded retrieval.",
        "ui": [
            "Document table (title, source, status, updated)",
            "Detail view for a single document",
        ],
        "backend": [
            "Document index entries from knowledge service",
            "Chunking and embeddings when enabled",
        ],
        "architecture": [
            "Chunked content supports tier-0 retrieval; provenance links back to sources",
        ],
        "guide_steps": [
            "Search documents by title or source.",
            "Verify ingestion state is healthy for high-value policies and SOPs.",
            "Open detail when agents cite unexpected content.",
        ],
    },
    {
        "path": "app/knowledge/search",
        "title": "Knowledge search",
        "permission": "knowledge:read",
        "purpose": "Ad-hoc search across the knowledge corpus.",
        "ui": [
            "Search input and result list",
            "Uses GET /knowledge/search?query=",
        ],
        "backend": [
            "GET /api/v1/knowledge/search?query=...",
            "Optional graph federate POST /knowledge/graph/federate",
        ],
        "architecture": [
            "Default tier-0 keyword/vector; escalate for multi-hop only when needed",
        ],
        "guide_steps": [
            "Enter a precise query (policy name, entity, procedure).",
            "Inspect citations/snippets for provenance before acting.",
            "If results are empty, check Sources sync health first.",
        ],
    },
    {
        "path": "app/memory",
        "title": "Memory",
        "permission": "memory:read",
        "purpose": "Inspect scoped memory items (event, episodic, semantic, procedural, decision, exception, evaluation, provenance).",
        "ui": [
            "Memory list / filters by scope and type",
            "Detail for individual items when selected",
        ],
        "backend": [
            "GET /api/v1/memory",
            "Runtime enforces allowed_memory_scopes on agent reads/writes",
        ],
        "architecture": [
            "Memory stewardship: provenance, retention, quality controls",
            "High-impact writes may require human review (memory-poisoning defense)",
        ],
        "guide_steps": [
            "Open Memory to audit what agents can recall.",
            "Filter by scope (organization, agent, case) when diagnosing wrong decisions.",
            "Treat unprovenanced high-impact memories as untrusted.",
            "Retention and deletion follow org data-retention policy.",
        ],
    },
    {
        "path": "app/evaluations",
        "title": "Evaluations",
        "permission": "evaluations:read",
        "purpose": "Golden / regression / adversarial / historical-replay evaluation results for workflows and variants.",
        "ui": [
            "Evaluation runs table",
            "Detail under /app/evaluations/runs/{id}",
        ],
        "backend": [
            "GET /api/v1/evaluations",
            "Eval corpus under business/evals/",
            "Promotion blocked without passing required checks",
        ],
        "architecture": [
            "Everything is testable (structure.md principles)",
            "Evaluation layer gates evolution promotion",
        ],
        "guide_steps": [
            "Review recent evaluation runs for regressions.",
            "Open a run detail for score breakdown and failures.",
            "Do not canary/promote variants with failed adversarial or golden suites.",
        ],
    },
    {
        "path": "app/evaluations/runs",
        "title": "Evaluation run detail",
        "permission": "evaluations:read",
        "purpose": "Template for /app/evaluations/runs/{runId} detail of a single evaluation execution.",
        "ui": [
            "Scores, suite type, timestamps, failure details",
        ],
        "backend": [
            "Evaluation service records per-run outcomes",
        ],
        "architecture": [
            "Evidence for fitness function components (quality, safety, compliance)",
        ],
        "guide_steps": [
            "Open from the evaluations list.",
            "Note which suite failed (golden vs adversarial vs regression).",
            "Link failures back to workflow DNA or prompts before re-running improve.",
        ],
    },
    {
        "path": "app/processes",
        "title": "Process intelligence",
        "permission": "processes:read",
        "purpose": "Process mining outputs: discovered processes, conformance, bottlenecks from real event logs.",
        "ui": [
            "Process summary metrics",
            "Process list / detail cards",
        ],
        "backend": [
            "GET /api/v1/processes/summary and related process endpoints",
            "Artifacts under business/process-intelligence/",
        ],
        "architecture": [
            "Process Intelligence layer (structure.md §2.3)",
            "Learn from actual traces, not only SOPs",
        ],
        "guide_steps": [
            "Open Processes to see mined workflow models and bottlenecks.",
            "Compare conformance gaps (SOP vs actual) before redesigning DNA.",
            "Feed bottleneck insights into evolution hypotheses — still sandbox first.",
        ],
    },
    {
        "path": "app/audit-logs",
        "title": "Audit logs",
        "permission": "audit:read",
        "purpose": "Immutable-style operational audit trail for auth, workflow, approval, and tool actions.",
        "ui": [
            "Chronological audit table with actor, action, resource, outcome",
            "Filters by type when provided",
        ],
        "backend": [
            "GET /api/v1/audit-logs",
            "Runtime appends audit events on login, DNA steps, approvals, tool effects",
        ],
        "architecture": [
            "Auditability is priority #2 after Safety",
            "Supports EU AI Act / assurance case evidence trails",
        ],
        "guide_steps": [
            "Use Audit Logs for forensics after incidents or customer disputes.",
            "Filter by actor or resource when reconstructing a run.",
            "Export/share only under org compliance rules.",
        ],
    },
    {
        "path": "app/settings",
        "title": "Settings hub",
        "permission": "settings:read",
        "purpose": "Organization administration hub: profile, org, users, roles, billing, API keys, security, integrations.",
        "ui": [
            "Card grid of settings destinations",
        ],
        "backend": [
            "GET /settings and nested admin APIs",
            "RBAC enforced server-side",
        ],
        "architecture": [
            "Admin plane separate from execution; still fully audited",
        ],
        "guide_steps": [
            "Open Settings only with admin/settings permissions.",
            "Prefer least privilege when inviting users and minting API keys.",
            "Review Security and Integrations after any org change.",
        ],
    },
    {
        "path": "app/settings/organization",
        "title": "Organization settings",
        "permission": "settings:update (org)",
        "purpose": "Brand, locale, retention posture for the tenant.",
        "ui": [
            "OrganizationSettingsForm — name/slug/status fields",
            "PATCH organization",
        ],
        "backend": [
            "GET/PATCH /organizations/{id}",
        ],
        "architecture": [
            "Multi-tenant org boundary for agents, memory, and audit",
        ],
        "guide_steps": [
            "Update display name carefully; slug changes may break integrations.",
            "Align retention fields with legal data-retention policy.",
            "Save and verify the org card reflects new values.",
        ],
    },
    {
        "path": "app/settings/users",
        "title": "Users",
        "permission": "users:read",
        "purpose": "User roster, invitations, role assignment, disable lifecycle.",
        "ui": [
            "UserAdminPanel — invite, role/status updates",
        ],
        "backend": [
            "GET /users, POST invitations, PATCH users",
            "Accept invite via /users/invitations/accept (public with token)",
        ],
        "architecture": [
            "RBAC roles map to permission strings used by API dependencies",
        ],
        "guide_steps": [
            "Invite users with the minimum role required.",
            "Disable accounts promptly on offboarding.",
            "Share invite links securely; accept-invite sets session cookies via BFF.",
        ],
    },
    {
        "path": "app/settings/roles",
        "title": "Roles",
        "permission": "settings:read",
        "purpose": "Permission matrix and responsibility boundaries for RBAC roles.",
        "ui": [
            "Roles explanation / matrix view",
        ],
        "backend": [
            "Role definitions enforced in backend permissions module",
        ],
        "architecture": [
            "Least privilege; high-risk actions need elevated roles + gates",
        ],
        "guide_steps": [
            "Review which roles can approve, run workflows, or manage settings.",
            "Do not grant admin by default for operators who only need run/approve.",
        ],
    },
    {
        "path": "app/settings/billing",
        "title": "Billing",
        "permission": "settings:read",
        "purpose": "Commercial plan and invoicing posture (feature-flag aware).",
        "ui": [
            "Plan / billing status cards",
        ],
        "backend": [
            "Billing feature may be gated by NEXT_PUBLIC_ENABLE_BILLING",
            "No payment secrets in the frontend",
        ],
        "architecture": [
            "Commercial metadata only; not part of execution safety core",
        ],
        "guide_steps": [
            "Confirm plan status with finance owners.",
            "Do not store card data in this console.",
        ],
    },
    {
        "path": "app/settings/api-keys",
        "title": "API keys",
        "permission": "settings:read / settings:update",
        "purpose": "Machine credentials for automation; masked display after mint.",
        "ui": [
            "ApiKeyTable — list, create, revoke",
            "Secret shown once at creation",
        ],
        "backend": [
            "GET/POST /auth/api-keys, DELETE /auth/api-keys/{id}",
            "Keys authenticate as bearer tokens",
        ],
        "architecture": [
            "Service accounts still subject to RBAC and audit",
        ],
        "guide_steps": [
            "Create keys with descriptive names and store secrets in a vault immediately.",
            "Revoke unused or leaked keys without delay.",
            "Never commit API keys to git or docs.",
        ],
    },
    {
        "path": "app/settings/security",
        "title": "Security settings",
        "permission": "settings:read",
        "purpose": "Session, MFA posture, allowed domains, and security controls summary.",
        "ui": [
            "Security configuration panels",
        ],
        "backend": [
            "Security policies + OWASP LLM/agentic controls at runtime",
            "Auth rate limits on login",
        ],
        "architecture": [
            "Security layer: tool broker, memory-poisoning defense, skill vetting",
            "Blast-radius control over pure prompt trust",
        ],
        "guide_steps": [
            "Review session and domain allowlists with security owners.",
            "Enable MFA when offered by the deployment.",
            "Treat security settings changes as high-impact and audit them.",
        ],
    },
    {
        "path": "app/settings/integrations",
        "title": "Integrations",
        "permission": "settings:read",
        "purpose": "Connected systems and automation endpoints configuration overview.",
        "ui": [
            "Integration list / status",
        ],
        "backend": [
            "Tool adapters and external systems behind the API",
        ],
        "architecture": [
            "Integrations execute only through governed tool adapters",
        ],
        "guide_steps": [
            "Verify integration health before critical workflow runs.",
            "Rotate credentials via secure ops processes, not chat logs.",
        ],
    },
    {
        "path": "app/settings/profile",
        "title": "User profile",
        "permission": "authenticated user",
        "purpose": "Current user profile display and self-service profile fields when enabled.",
        "ui": [
            "Profile summary for the session user",
        ],
        "backend": [
            "GET /auth/me",
            "Optional PATCH user self fields",
        ],
        "architecture": [
            "Session established via password login BFF cookies",
        ],
        "guide_steps": [
            "Confirm your name and email are correct.",
            "Sign out from the header when finished on shared machines.",
        ],
    },
    {
        "path": "app/docs",
        "title": "Full-page document viewer",
        "permission": "authenticated (app shell)",
        "purpose": "Dedicated markdown viewer for static files under public/docs via ?md= path.",
        "ui": [
            "FullPageMarkdownDocument",
            "Query parameter md=/docs/...",
        ],
        "backend": [
            "No API — static files from Next public/",
        ],
        "architecture": [
            "Help system per help_spec.md: route-derived docs + full page + drawer",
        ],
        "guide_steps": [
            "Prefer opening docs from the header book icon (pre-fills md for current route).",
            "You may also navigate to /app/docs?md=/docs/app/workflows/spec.md.",
            "Missing files show a neutral empty state, not a crash.",
        ],
    },
]


def write_spec(route: dict) -> str:
    path = route["path"]
    lines = [
        f"# Spec: {route['title']}",
        "",
        f"**Route:** `/{path}`  ",
        f"**Permission (typical):** {route['permission']}  ",
        f"**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`",
        "",
        "## Purpose",
        "",
        route["purpose"],
        "",
        "## Design priorities",
        "",
        "```text",
        "Safety > Auditability > Correctness > Efficiency > Autonomy",
        "```",
        "",
        "Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.",
        "",
        "## UI surface",
        "",
    ]
    for item in route["ui"]:
        lines.append(f"- {item}")
    lines += ["", "## Backend / API contracts", ""]
    for item in route["backend"]:
        lines.append(f"- {item}")
    lines += ["", "## Architecture mapping", ""]
    for item in route["architecture"]:
        lines.append(f"- {item}")
    lines += [
        "",
        "## Non-goals",
        "",
        "- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.",
        "- Help markdown here is documentation only; it does not change runtime policy.",
        "",
        "## Related paths",
        "",
        f"- User guide: `/docs/{path}/user_guide.md`",
        f"- Full-page view: `/app/docs?md=/docs/{path}/spec.md`",
        "",
    ]
    return "\n".join(lines)


def write_user_guide(route: dict) -> str:
    path = route["path"]
    lines = [
        f"# User guide: {route['title']}",
        "",
        f"**Screen:** `/{path}`  ",
        f"**Who:** Operators with `{route['permission']}` (or stronger)",
        "",
        "## Before you start",
        "",
        "- Backend healthy: `GET /api/v1/health/ready` reports Postgres when using live mode.",
        "- Frontend live mode: `NEXT_PUBLIC_DEMO_MODE=false`.",
        "- You are signed in (session cookies set by `POST /api/auth/login`).",
        "",
        "## What this screen is for",
        "",
        route["purpose"],
        "",
        "## Step-by-step",
        "",
    ]
    for i, step in enumerate(route["guide_steps"], 1):
        lines.append(f"{i}. {step}")
    lines += [
        "",
        "## UI checklist",
        "",
    ]
    for item in route["ui"]:
        lines.append(f"- [ ] {item}")
    lines += [
        "",
        "## Safety notes",
        "",
        "- Prefer reversible actions; require human approval for irreversible tool effects.",
        "- Do not promote evolution variants without golden/adversarial evaluation evidence.",
        "- Keep secrets out of chat, tickets, and git; use API keys vaulting for machines.",
        "",
        "## Troubleshooting",
        "",
        "| Symptom | What to check |",
        "|---------|----------------|",
        "| Empty / demo data | `NEXT_PUBLIC_DEMO_MODE`, backend up, login cookies |",
        "| 403 on load | Sign in again; role permissions for this screen |",
        "| Stale numbers | Hard refresh; verify API proxy `/api/proxy/*` |",
        "| Help drawer empty | Missing `public/docs/...` markdown for this route |",
        "",
        "## Related",
        "",
        f"- Spec: `/docs/{path}/spec.md`",
        f"- Architecture: `structure.md`",
        f"- Backend plan: `backend.md`",
        f"- Frontend plan: `frontend.md`",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    written = 0
    for route in ROUTES:
        folder = DOCS.joinpath(*route["path"].split("/"))
        folder.mkdir(parents=True, exist_ok=True)
        spec_path = folder / "spec.md"
        guide_path = folder / "user_guide.md"
        spec_path.write_text(write_spec(route), encoding="utf-8")
        guide_path.write_text(write_user_guide(route), encoding="utf-8")
        written += 2
        print(f"wrote {spec_path.relative_to(ROOT)}")
        print(f"wrote {guide_path.relative_to(ROOT)}")
    # Remove obsolete userguide.md if present under docs tree
    for old in DOCS.rglob("userguide.md"):
        old.unlink()
        print(f"removed obsolete {old.relative_to(ROOT)}")
    print(f"done: {written} files across {len(ROUTES)} routes")


if __name__ == "__main__":
    main()
