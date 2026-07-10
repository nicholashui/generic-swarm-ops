# Generate planning/frontend/nn_*/requirements.md from frontend.md decomposition.
from __future__ import annotations

from pathlib import Path

ROOT = Path("planning/frontend")
ROOT.mkdir(parents=True, exist_ok=True)

# (nn, slug, title, source_map, related, depends_on, provides_to)
SPECS: list[tuple[str, str, str, str, str, str, str]] = [
    (
        "01",
        "frontend-charter-scope-and-principles",
        "Frontend Charter, Scope, and Design Principles",
        "§1 Purpose, §2 Product Vision, §3 Core Design Principle, §4 Scope, §6 Runtime Responsibilities, §32 Final Frontend Rule, §33 Implementation Mapping",
        "structure.md §10–12; backend.md control-plane boundary",
        "None (root)",
        "All FE-02–FE-20",
    ),
    (
        "02",
        "nextjs-scaffold-stack-and-folder-structure",
        "Next.js Scaffold, Stack, and Folder Structure",
        "§5 Recommended Technology Stack, §7 Application Architecture, §18 Frontend Folder Structure, §19 Environment Variables, Phase 1 Project Setup",
        "structure.md §12.3 ops console entry",
        "FE-01",
        "FE-03+",
    ),
    (
        "03",
        "design-system-tokens-and-opendesign",
        "Design System, Tokens, and OpenDesign Workflow",
        "§3 Core Design Principle, §8–11 OpenDesign MCP / Trae rules, §14 Core Layout Design, §15 Visual Design, §17 Reusable Components, Phase 2–3",
        "OpenDesign MCP; docs/design/*",
        "FE-02",
        "FE-04–FE-19 page UIs",
    ),
    (
        "04",
        "app-shell-navigation-and-information-architecture",
        "App Shell, Navigation, and Information Architecture",
        "§7.3 Route Protection, §12 Information Architecture, §14 Core Layout Design, Phase 5 App Shell",
        "structure.md human-centered ops console",
        "FE-02, FE-03, FE-05",
        "All /app/* domain pages",
    ),
    (
        "05",
        "authentication-and-session-ui",
        "Authentication and Session UI",
        "§16.1–16.3a Public/Login/Register/Accept-invite, Phase 4 Authentication and Session UI, §20 API Integration auth",
        "backend BE-05 auth APIs",
        "FE-02, FE-07",
        "FE-04, FE-06, all protected routes",
    ),
    (
        "06",
        "permission-aware-navigation-and-ui",
        "Permission-Aware Navigation and UI",
        "§13 User Roles and Permissions, §6.3 Boundary Rule, permission-aware navigation in §4.1",
        "backend BE-06 RBAC",
        "FE-05",
        "All domain pages (UX gates only)",
    ),
    (
        "07",
        "typed-api-client-and-openapi-integration",
        "Typed API Client and OpenAPI Integration",
        "§20 API Integration, §33.3a Backend API contracts, pnpm api:generate, DEMO_MODE ops profile",
        "backend OpenAPI; planning/backend/",
        "FE-02",
        "All data-fetching pages FE-08–FE-18",
    ),
    (
        "08",
        "dashboard-page",
        "Dashboard Page",
        "§16.4 Dashboard Page, Phase 6 Dashboard, §12.1 /app",
        "structure.md operator path entry",
        "FE-04, FE-06, FE-07",
        "Operator entry to domain pages",
    ),
    (
        "09",
        "agents-and-tools-ui",
        "Agents and Tools UI",
        "§16.5–16.9 Agents/Tools pages, Phase 7 Agents and Tools",
        "backend BE-08, BE-09",
        "FE-04, FE-06, FE-07",
        "Workflow assignment UIs",
    ),
    (
        "10",
        "workflows-definition-ui",
        "Workflows Definition UI",
        "§16.10–16.12 Workflows list/create/detail, Phase 8 Workflows",
        "backend BE-10",
        "FE-04, FE-06, FE-07, FE-09",
        "FE-11 run detail",
    ),
    (
        "11",
        "workflow-run-realtime-ui",
        "Workflow Run Realtime UI",
        "§16.13 Workflow Run Detail, §21 Real-Time Updates, Phase 9, run pause/resume/expire §33.3a",
        "backend BE-11, BE-19 streaming",
        "FE-07, FE-10",
        "FE-12, FE-18 Improve",
    ),
    (
        "12",
        "approvals-and-human-gates-ui",
        "Approvals and Human Gates UI",
        "§16.14–16.15 Approvals list/detail, Phase 10 Approvals, human gates §33",
        "backend BE-13; structure §4/§10",
        "FE-06, FE-07, FE-11",
        "Operator gate completion path",
    ),
    (
        "13",
        "knowledge-and-memory-ui",
        "Knowledge and Memory UI",
        "§16.16–16.19 Knowledge/Memory pages, Phase 11",
        "backend BE-15, BE-16",
        "FE-04, FE-06, FE-07",
        "Shadow-learning / data ops surfaces",
    ),
    (
        "14",
        "evaluations-and-processes-ui",
        "Evaluations and Processes UI",
        "§16.20–16.22 Evaluations/Processes pages, Phase 12",
        "backend BE-17, BE-18",
        "FE-04, FE-06, FE-07",
        "Quality nav group",
    ),
    (
        "15",
        "audit-logs-ui",
        "Audit Logs UI",
        "§16.23 Audit Logs Page, Phase 13 (audit portion)",
        "backend BE-14",
        "FE-04, FE-06, FE-07",
        "Security / compliance review UX",
    ),
    (
        "16",
        "settings-users-org-and-api-keys-ui",
        "Settings, Users, Organization, and API Keys UI",
        "§16.24–16.28 Settings suite, Phase 13 Settings, §33.3a users/orgs/invitations",
        "backend BE-07",
        "FE-04, FE-05, FE-06, FE-07",
        "Admin lifecycle UX",
    ),
    (
        "17",
        "evolution-sandbox-archive-ui",
        "Evolution Sandbox Archive UI",
        "§16.13a Evolution Archive Page, §4.1 Evolution section, §33.3 Evolution UI",
        "backend BE-20; structure §5",
        "FE-04, FE-06, FE-07",
        "FE-18 canary/promote views",
    ),
    (
        "18",
        "improve-pipeline-ui",
        "Improve Pipeline UI (Reflect → Propose → Evaluate → Canary)",
        "§1 Improve pipeline, §16.13 Improve actions, §33.3 Self-improvement UI, Phase D evolution",
        "backend BE-21; structure §5/§8",
        "FE-11, FE-12, FE-14, FE-17",
        "E1 operator improve path",
    ),
    (
        "19",
        "accessibility-loading-empty-and-error-states",
        "Accessibility, Loading, Empty, and Error States",
        "§22 Loading/Empty/Error States, §23 Accessibility Requirements, §29 product ideas (UX quality)",
        "WCAG 2.2 AA target; structure human–AI interaction",
        "FE-03, FE-04",
        "All pages (cross-cutting UX quality)",
    ),
    (
        "20",
        "security-performance-testing-and-ops-profile",
        "Security, Performance, Testing, and Ops Profile",
        "§24 Security, §25 Performance, §26 Observability, §27 Testing, §28 Phase 14, §30–31 Acceptance/DoD, §33 non-goals & ops profile",
        "E1 path; mark ~100 evidence",
        "FE-01–FE-19",
        "Release gate / product-bar proof",
    ),
]


def doc_control(nn: str, title: str, source: str, related: str) -> str:
    return f"""# {nn} — {title}

| Field | Value |
|-------|-------|
| Spec ID | `FE-{nn}` |
| Source | `frontend.md` — {source} |
| Related architecture | {related} |
| Priority order | {nn} |
| Status | Specification |
| Owner | Frontend platform |

---
"""


CONTENT: dict[str, dict[str, str]] = {}

# ── FE-01 ──────────────────────────────────────────────────────────────────
CONTENT["01"] = {
    "scope": """### 1.1 In scope
- Frontend mission as the professional ops console for the Generic Swarm Business Operating System.
- Product vision: enterprise SaaS feel (trust, reliability, operational clarity, security, professionalism, speed, control, observability).
- System boundary: presentation, interaction, routing, layout, UI state, client validation, UX, client realtime display, design-system implementation.
- Explicit non-ownership of backend business logic, execution, secret storage, audit writes, silent production DNA mutation, host self-rewrite UI.
- Design priority inheritance: backend remains source of truth for authz, execution, and governance; OpenDesign-first major layouts.
- As-built relationship to `structure.md` §11.1/§12 and `planning/backend/` (FE never re-implements policy).

### 1.2 Out of scope
- Concrete page layouts and component APIs (later FE specs).
- Backend route implementation (planning/backend/*).
- Domain business corpus under `business/`.

### 1.3 System under specification
Generic Swarm Ops **frontend ops console** (`frontend/`), as specified in `frontend.md` and constrained by `structure.md` / `backend.md`.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-01-01 | Product / architecture | Console realizes structure.md human-centered ops path without becoming a second control plane. |
| STK-01-02 | Operators | Always understand agents, workflows, runs, failures, approvals, knowledge, data use, actions, and attention items. |
| STK-01-03 | Security / compliance | UI never treats hidden buttons as security; backend remains final authority. |
| STK-01-04 | Frontend engineers | Clear charter for what FE may and must not implement. |
| STK-01-05 | Backend consumers | Stable presentation layer that only mutates via versioned `/api/v1/*`. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-01-01 | The frontend shall deliver the user-facing web application for managing AI agents, workflows, tools, approvals, knowledge, memory, evaluations, audits, evolution sandbox variants, self-improvement actions, and organization settings. |
| FR-01-02 | The frontend shall communicate trust, reliability, operational clarity, security, professionalism, speed, control, and observability in its product presentation. |
| FR-01-03 | The frontend shall own presentation, interaction, routing, layout, UI state, frontend validation, UX, client-side realtime display, and design-system implementation. |
| FR-01-04 | If a capability requires workflow execution, agent execution, tool execution, permission enforcement as sole authority, direct database writes, background jobs, embedding/indexing, secret storage, provider API key handling in browser code, audit log creation, billing calculation, silent production DNA mutation, or host self-rewrite, then the frontend shall not implement that capability. |
| FR-01-05 | When the user requests an action, the frontend shall request it from the backend; the backend shall decide whether the action is allowed. |
| FR-01-06 | The frontend shall not assume that hiding a control is sufficient security. |
| FR-01-07 | When designing major page layouts, the frontend workflow shall prefer OpenDesign MCP references over generic AI memory alone. |
| FR-01-08 | The frontend shall treat `structure.md` as architecture source of truth and `backend.md` / planning/backend as the API control-plane contract. |
| FR-01-09 | When a design trade-off exists between operator clarity and decorative complexity, the frontend shall prefer operational clarity. |
| FR-01-10 | The frontend shall support both an ops profile (`NEXT_PUBLIC_DEMO_MODE=false` against live backend) and a demo profile for UI-only preview without treating demo as production authority. |
| FR-01-11 | The frontend shall remain a presentation and interaction layer so that authorization, execution, and governance stay on the backend. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-01-01 | Charter and boundary checks shall be enforceable by code review and architecture review without requiring online LLM calls. |
| NFR-01-02 | Frontend package boundaries shall keep domain pages free of backend business rules duplicated from Python services. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-01-03 | If a proposed UI feature would allow unattended direct production DNA mutation or host application self-rewrite, then the frontend shall reject that feature as out of charter. |
| NFR-01-04 | The frontend shall never store provider secrets or perform final authentication verification as sole authority. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-01-01 | frontend.md and this spec state frontend is presentation/interaction only; backend is control plane. |
| AC-01-02 | Out-of-scope list matches frontend.md §4.2 and §33.5 non-goals. |
| AC-01-03 | All downstream planning/frontend/* specs reference FE-01 priority order. |
| AC-01-04 | Evolution and improve specs explicitly require sandbox-only backend APIs. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-01-01 | Document review: map each §4.1 in-scope item to at least one later FE FR. | Review |
| TV-01-02 | Negative: client-side production DNA rewrite UI → reject against charter. | Spec gate |
| TV-01-03 | Traceability matrix FE-01 FR IDs → later FE FR IDs. | Traceability |
""",
    "trace": """| frontend.md / structure.md | This spec |
|---|---|
| frontend.md §1–2 Purpose/Vision | FR-01-01 … FR-01-02 |
| frontend.md §4 Scope | FR-01-03 … FR-01-04 |
| frontend.md §6 Runtime Responsibilities | FR-01-05 … FR-01-06 |
| frontend.md §3 OpenDesign principle | FR-01-07 |
| frontend.md §32–33 Final rule / mapping | FR-01-08 … FR-01-11 |
""",
}

# ── FE-02 ──────────────────────────────────────────────────────────────────
CONTENT["02"] = {
    "scope": """### 1.1 In scope
- Next.js + React + TypeScript + Tailwind CSS stack.
- Hybrid rendering strategy (server components for shell/metadata; client components for interactive widgets).
- Recommended frontend folder structure under `frontend/`.
- Environment variables and config loading (`NEXT_PUBLIC_*`, API base URL, DEMO_MODE).
- Tooling: ESLint, Prettier, path aliases, lint/typecheck/build scripts.
- Phase 1 project setup exit criteria.

### 1.2 Out of scope
- Visual token extraction (FE-03).
- Domain page implementations (FE-08+).
- Backend scaffold (planning/backend BE-02).

### 1.3 System under specification
Frontend application scaffold and runtime stack for the ops console.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-02-01 | Frontend engineers | Reproducible Next.js TypeScript app with known scripts. |
| STK-02-02 | Operators / deployers | Documented env vars for ops vs demo profiles. |
| STK-02-03 | CI | lint, typecheck, unit test, and build commands. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-02-01 | The frontend shall be implemented as a Next.js application using React and TypeScript. |
| FR-02-02 | The frontend shall use Tailwind CSS for styling integration with design tokens. |
| FR-02-03 | When a UI element is highly interactive (command palette, realtime timeline, modals, drawers, filterable tables, workflow builder, logs viewer), the frontend shall implement it as a client component. |
| FR-02-04 | When a surface is static layout, metadata, or secure initial composition, the frontend shall prefer server components where appropriate. |
| FR-02-05 | The frontend shall organize source under the recommended folder structure (app routes, components, lib/api, hooks, types, styles/tokens). |
| FR-02-06 | The frontend shall load configuration from environment variables including API base URL and `NEXT_PUBLIC_DEMO_MODE`. |
| FR-02-07 | The frontend project shall provide `pnpm install`, `pnpm dev`, `pnpm build`, `pnpm lint`, and `pnpm typecheck` (or equivalent documented scripts). |
| FR-02-08 | If the user is not authenticated and navigates to `/app/*`, the route layer shall redirect to `/login` (UX protection only). |
| FR-02-09 | The frontend shall document README startup instructions for local development against a live backend. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-02-01 | Local `pnpm dev` shall start the app for interactive development without requiring a full production build. |
| NFR-02-02 | Production `pnpm build` shall succeed for the scaffolded app shell before domain pages are complete. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-02-03 | Secrets used only on the server shall not be prefixed with `NEXT_PUBLIC_`. |
| NFR-02-04 | Client-exposed env shall be limited to non-secret configuration (API URL, demo flag, public app metadata). |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-02-01 | App starts locally with TypeScript and Tailwind working. |
| AC-02-02 | Lint and typecheck scripts pass on scaffold. |
| AC-02-03 | Folder structure matches frontend.md §18 intent (or documented as-built equivalent). |
| AC-02-04 | Env template documents API URL and DEMO_MODE. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-02-01 | Run install → lint → typecheck → build on clean checkout. | Automated |
| TV-02-02 | Review: no provider secrets in NEXT_PUBLIC_* sample env. | Review |
| TV-02-03 | Smoke: unauthenticated `/app` redirects to login. | Manual / E2E |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §5 Technology Stack | FR-02-01 … FR-02-02 |
| §7 Application Architecture | FR-02-03 … FR-02-04, FR-02-08 |
| §18 Folder Structure | FR-02-05 |
| §19 Environment Variables | FR-02-06, NFR-02-03 … NFR-02-04 |
| Phase 1 Project Setup | FR-02-07, FR-02-09, AC-02-* |
""",
}

# ── FE-03 ──────────────────────────────────────────────────────────────────
CONTENT["03"] = {
    "scope": """### 1.1 In scope
- OpenDesign MCP mandatory workflow for major page layouts (with documented fallback when MCP unavailable).
- Design tokens: color, typography, spacing, status, elevation/radius as applicable.
- Base reusable UI components (buttons, inputs, badges, cards, tables shells, dialogs).
- Layout primitives (page header, content width, sidebar frame).
- Loading / empty / error presentational components foundations.
- Trae project rules and design reference documentation.

### 1.2 Out of scope
- Domain data wiring (FE-07+).
- Full page business logic.
- Backend design system.

### 1.3 System under specification
Visual and component design-system foundation for the ops console.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-03-01 | Design / product | Consistent enterprise SaaS visual language, not generic AI demo chrome. |
| STK-03-02 | Trae / agents | Mandatory OpenDesign call path before major layouts. |
| STK-03-03 | Engineers | Tokenized components reusable across all pages. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-03-01 | Before creating or significantly modifying a major page layout, Trae shall call the OpenDesign MCP server named `opendesign` when available. |
| FR-03-02 | If OpenDesign MCP is unavailable, the frontend shall use a documented design fallback and record the fallback in design documentation. |
| FR-03-03 | The frontend shall implement design tokens for color, typography, spacing, and status semantics. |
| FR-03-04 | The frontend shall implement base UI components for buttons, form controls, status badges, cards, tables, modals/drawers, and alerts. |
| FR-03-05 | The frontend shall implement layout components that support authenticated app shell composition. |
| FR-03-06 | The frontend shall implement reusable loading, empty, and error presentation components. |
| FR-03-07 | Status colors and badges shall encode operational states (running, succeeded, failed, awaiting approval, paused, cancelled) consistently. |
| FR-03-08 | The design system shall favor operational density and scannability appropriate to an enterprise ops console. |
| FR-03-09 | Design reference artifacts shall be documented under `docs/design/` (or equivalent) including token map and OpenDesign reference notes. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-03-01 | Base components shall avoid unnecessary client-side re-renders when used in lists and tables. |
| NFR-03-02 | CSS/token delivery shall not block first paint beyond normal Next.js/Tailwind practice. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-03-03 | Design tokens and components shall not embed secrets or live credentials. |
| NFR-03-04 | User-generated content displayed via design-system primitives shall be escaped/rendered safely (XSS-safe defaults). |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-03-01 | Token files and base components exist and are used by app shell. |
| AC-03-02 | OpenDesign process or documented fallback is written. |
| AC-03-03 | Status badge set covers primary run/approval states. |
| AC-03-04 | Loading/empty/error primitives exist for page adoption. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-03-01 | Component story or unit smoke for Button, Badge, EmptyState, ErrorState. | Unit |
| TV-03-02 | Review: major layout PRs cite OpenDesign or fallback note. | Review |
| TV-03-03 | Visual spot-check: status colors distinguishable in light theme. | Manual |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §3, §8–11 OpenDesign / Trae | FR-03-01 … FR-03-02, FR-03-09 |
| §14–15 Layout & visual | FR-03-03 … FR-03-05, FR-03-08 |
| §17 Reusable components | FR-03-04, FR-03-06 … FR-03-07 |
| Phase 2–3 | AC-03-* |
""",
}

# ── FE-04 ──────────────────────────────────────────────────────────────────
CONTENT["04"] = {
    "scope": """### 1.1 In scope
- Authenticated app shell: sidebar, header, content region.
- Information architecture routes (`/`, auth routes, `/app/*` domain paths).
- Navigation groups: Main, Data, Quality, Security, Admin.
- Global header: breadcrumbs, command palette trigger, environment indicator, org switcher, notifications placeholder, user menu.
- Command palette (Cmd/Ctrl+K) action catalog.
- Route protection UX for `/app/*`.
- As-built dynamic `/app/[...slug]` compatibility while preserving IA deep links.

### 1.2 Out of scope
- Domain panel data implementations (FE-08+).
- Auth form pages (FE-05).
- Backend routing.

### 1.3 System under specification
Authenticated application chrome and navigation system.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-04-01 | Operators | Predictable navigation and deep links to ops surfaces. |
| STK-04-02 | Multi-org users | Organization context visible and switchable when supported. |
| STK-04-03 | Power users | Command palette for frequent actions. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-04-01 | The frontend shall provide an authenticated app shell for all `/app/*` routes. |
| FR-04-02 | The sidebar shall group navigation into Main, Data, Quality, Security, and Admin as specified in frontend.md §12.2. |
| FR-04-03 | The frontend shall expose information architecture routes for dashboard, agents, tools, workflows, workflow runs, approvals, knowledge, memory, evaluations, processes, audit logs, evolution, and settings sub-routes. |
| FR-04-04 | When a user is not authenticated on `/app/*`, the frontend shall redirect to `/login`. |
| FR-04-05 | When a user lacks organization access, the frontend shall redirect to organization selection or an access-denied page. |
| FR-04-06 | When a user lacks permission for a route, the frontend shall display a 403 Access Denied state (UX only). |
| FR-04-07 | The global header shall include breadcrumbs, command/search trigger, non-production environment indicator when applicable, organization switcher, notifications entry, and user menu. |
| FR-04-08 | When the user presses Cmd/Ctrl+K, the frontend shall open a command palette with documented actions (create agent/workflow, search knowledge, open recent run, approvals, invite, API keys, audit, security, evaluation, knowledge source). |
| FR-04-09 | If the implementation uses a dynamic `/app/[...slug]` panel router, the frontend shall still present the §12.1 URLs in navigation and deep links. |
| FR-04-10 | Public root `/` shall land or redirect according to product rules (landing or to login/app). |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-04-01 | App shell chrome shall remain responsive during client navigations between domain panels. |
| NFR-04-02 | Command palette shall open without full page reload. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-04-03 | Client route guards shall not replace backend authorization. |
| NFR-04-04 | User menu and org switcher shall not expose tokens in the DOM beyond necessary display fields. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-04-01 | Authenticated shell renders sidebar + header + content. |
| AC-04-02 | Navigation groups match §12.2 labels. |
| AC-04-03 | Unauthenticated access to `/app` redirects to login. |
| AC-04-04 | Command palette opens via keyboard shortcut. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-04-01 | Manual: walk each nav group link. | Manual |
| TV-04-02 | Unit/integration: route guard redirect when session missing. | Automated |
| TV-04-03 | Keyboard: Cmd/Ctrl+K opens palette. | Manual / a11y |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §12 Information Architecture | FR-04-02 … FR-04-03, FR-04-07 … FR-04-10 |
| §7.3 Route Protection | FR-04-04 … FR-04-06, NFR-04-03 |
| §14 Core Layout | FR-04-01 |
| Phase 5 App Shell | AC-04-* |
""",
}

# ── FE-05 ──────────────────────────────────────────────────────────────────
CONTENT["05"] = {
    "scope": """### 1.1 In scope
- Public root behavior.
- Login page (credentials → backend auth).
- Register page (if enabled).
- Forgot/reset password pages (if backend supports).
- Accept-invite page (`/accept-invite`) calling backend invitation accept API.
- Session storage strategy for tokens/cookies as designed with backend.
- Logout and session expiry UX.
- Display of backend auth errors with `request_id` when present.

### 1.2 Out of scope
- Backend JWT/session validation implementation (BE-05).
- Full user admin (FE-16).
- RBAC matrix UI (FE-06).

### 1.3 System under specification
Authentication and session lifecycle UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-05-01 | End users | Sign in and start operating the console. |
| STK-05-02 | Invited users | Accept org invite and join. |
| STK-05-03 | Security | No client-side final auth authority; secure transport. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-05-01 | The frontend shall provide a login page that submits credentials to the backend authentication API. |
| FR-05-02 | On successful login, the frontend shall establish a session usable by subsequent `/api/v1` calls and route the user into `/app`. |
| FR-05-03 | On authentication failure, the frontend shall display the backend error message and `request_id` when provided, without inventing success. |
| FR-05-04 | When registration is enabled, the frontend shall provide a register page that calls the backend register endpoint. |
| FR-05-05 | The frontend shall provide an accept-invite page at `/accept-invite` that calls `POST /users/invitations/accept` (or documented equivalent). |
| FR-05-06 | When the user logs out, the frontend shall clear client session state and call backend logout when available. |
| FR-05-07 | If the session is expired or refresh fails, the frontend shall redirect to login and preserve a safe return path when appropriate. |
| FR-05-08 | The frontend shall not perform final authentication verification as the sole authority; backend remains authoritative. |
| FR-05-09 | Forgot-password and reset-password routes shall exist when backend supports them; otherwise they shall be documented as deferred. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-05-01 | Login submit shall show pending state and disable double-submit. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-05-02 | Passwords shall not be logged to console or analytics. |
| NFR-05-03 | Tokens shall not be placed in query strings or localStorage if httpOnly cookie strategy is selected; follow backend contract. |
| NFR-05-04 | Accept-invite shall not accept tokens solely from untrusted client mutation without backend validation. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-05-01 | Login against live backend succeeds for valid user (ops profile). |
| AC-05-02 | Invalid credentials show error UI. |
| AC-05-03 | Accept-invite form posts to invitation accept API. |
| AC-05-04 | Logout clears session and blocks `/app` until re-login. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-05-01 | E1 operator path: login step. | E2E / manual |
| TV-05-02 | Unit: form validation rejects empty credentials. | Unit |
| TV-05-03 | Negative: forged client “authenticated” flag without token still fails API calls. | Integration |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.1–16.3a Auth pages | FR-05-01 … FR-05-05, FR-05-09 |
| §6.2–6.3 Boundary | FR-05-08 |
| §33.3a Auth/invite APIs | FR-05-05, AC-05-03 |
| Phase 4 | AC-05-* |
""",
}

# ── FE-06 ──────────────────────────────────────────────────────────────────
CONTENT["06"] = {
    "scope": """### 1.1 In scope
- Role-aware UI for suggested roles (Owner, Admin, Developer, Operator, Reviewer, Viewer, Billing Manager, Security Auditor).
- Permission-aware navigation (hide/disable items lacking permission).
- Page-level 403 Access Denied presentation.
- Action-level gating (e.g., Run Workflow, Approve, Invite) as UX only.
- Consumption of backend `/auth/me` (or equivalent) permission payload.

### 1.2 Out of scope
- Server-side RBAC enforcement (BE-06).
- ABAC engine UI beyond displaying backend decisions.
- Implementing permissions in localStorage as authority.

### 1.3 System under specification
Client permission presentation and navigation filtering.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-06-01 | Operators with limited roles | Only see actions they can use; clear denial otherwise. |
| STK-06-02 | Security auditors | UI does not pretend client checks are enforcement. |
| STK-06-03 | Admins | Consistent mapping of backend permissions to controls. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-06-01 | The frontend shall load the authenticated user’s roles and permissions from the backend. |
| FR-06-02 | When the user lacks permission for a navigation item, the frontend shall hide or disable that item according to product rules. |
| FR-06-03 | When the user navigates to a route they cannot access, the frontend shall show Access Denied (403) UX. |
| FR-06-04 | When the user lacks permission for a mutating action, the frontend shall disable or hide the action control. |
| FR-06-05 | If the backend returns 403 for an action the UI allowed, the frontend shall surface the backend denial and not claim success. |
| FR-06-06 | The frontend shall treat permission-aware UI as UX-level only; backend authorization remains final. |
| FR-06-07 | Role labels displayed in UI shall match backend-provided role names without inventing elevated privileges. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-06-01 | Permission payload shall be cached for the session and refreshed on login/org switch. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-06-02 | Client-side permission caches shall not be writable by untrusted page scripts as a means to elevate access. |
| NFR-06-03 | Permission checks in UI shall fail closed (deny/hide) when permission data is missing. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-06-01 | Viewer-like role cannot see admin-only nav items (given backend payload). |
| AC-06-02 | 403 from API shows error state on attempted mutation. |
| AC-06-03 | Documentation states client gates are non-authoritative. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-06-01 | Fixture: mock /auth/me without admin → admin links hidden. | Unit |
| TV-06-02 | Integration: API 403 path displays denial. | Integration |
| TV-06-03 | Review: no “permission enforced only in FE” claims. | Review |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §13 Roles and Permissions | FR-06-01 … FR-06-04, FR-06-07 |
| §6.3 Boundary Rule | FR-06-05 … FR-06-06 |
| §4.1 Permission-aware navigation | FR-06-02 |
""",
}

# ── FE-07 ──────────────────────────────────────────────────────────────────
CONTENT["07"] = {
    "scope": """### 1.1 In scope
- Typed API client calling versioned `/api/v1/*` backend routes.
- OpenAPI type generation (`pnpm api:generate` → `src/lib/api/generated/openapi.d.ts` or equivalent).
- Standard error envelope handling (message, code, `request_id`).
- DEMO_MODE vs live mode client behavior.
- Auth header/cookie attachment for API calls.
- Regeneration policy after backend schema changes.

### 1.2 Out of scope
- Backend OpenAPI authoring (BE-04).
- Page-specific UI (FE-08+).
- Direct database access from frontend.

### 1.3 System under specification
Frontend data-access layer and contract integration.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-07-01 | Frontend engineers | Type-safe API calls aligned with FastAPI schema. |
| STK-07-02 | Operators | Clear errors with request IDs for support. |
| STK-07-03 | Backend engineers | FE regenerates types rather than hand-forking contracts. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-07-01 | The frontend shall call the backend only through versioned HTTP APIs under `/api/v1` (or documented base path). |
| FR-07-02 | The frontend shall maintain a typed API client layer for domain resources (auth, users, agents, tools, workflows, runs, approvals, knowledge, memory, evaluations, processes, audit, evolution, improvement). |
| FR-07-03 | When OpenAPI schema is available, the frontend shall generate TypeScript types via `pnpm api:generate` (or documented equivalent). |
| FR-07-04 | When a backend error response includes `request_id`, the frontend shall display or log it for operator support. |
| FR-07-05 | If `NEXT_PUBLIC_DEMO_MODE=true`, the frontend may use demo fixtures; if `false`, the frontend shall use the live backend. |
| FR-07-06 | After backend OpenAPI changes, implementers shall regenerate the client types before claiming API compatibility. |
| FR-07-07 | The frontend shall not write to databases or internal services except via backend APIs. |
| FR-07-08 | API client shall attach authentication credentials per the auth session design. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-07-01 | API client shall support abort/cancel for in-flight requests on navigation where practical. |
| NFR-07-02 | List endpoints shall support pagination parameters when provided by backend. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-07-03 | API client shall not embed long-lived secrets in source. |
| NFR-07-04 | Cross-origin calls shall rely on documented CORS/credentials settings from backend. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-07-01 | Generated OpenAPI types exist and are imported by client modules. |
| AC-07-02 | Live mode login + at least one authenticated GET succeed against backend. |
| AC-07-03 | Error UI can show request_id from a forced 4xx/5xx. |
| AC-07-04 | README documents `pnpm api:generate`. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-07-01 | Unit: error parser extracts request_id. | Unit |
| TV-07-02 | Integration: client hits backend health/me. | Integration |
| TV-07-03 | Contract: regenerate types after OpenAPI export. | Tooling |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §20 API Integration | FR-07-01 … FR-07-05, FR-07-08 |
| §33.3a Backend contracts | FR-07-02, FR-07-06 |
| §19 DEMO_MODE | FR-07-05 |
""",
}

# ── FE-08 ──────────────────────────────────────────────────────────────────
CONTENT["08"] = {
    "scope": """### 1.1 In scope
- Main dashboard at `/app`.
- Summary cards / attention items (runs needing approval, failed runs, recent activity) per frontend.md §16.4.
- Entry links into domain sections.
- Health-aware empty/error when backend unavailable.

### 1.2 Out of scope
- Full domain CRUD (later specs).
- Backend metrics aggregation design.

### 1.3 System under specification
Operator dashboard home surface.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-08-01 | Operators | Immediate view of what needs attention. |
| STK-08-02 | New users | Clear entry points into agents, workflows, approvals. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-08-01 | The frontend shall provide a dashboard page at `/app` for authenticated users. |
| FR-08-02 | When dashboard data is available, the dashboard shall surface operational attention items including pending approvals and recent or failed workflow runs. |
| FR-08-03 | The dashboard shall provide navigation affordances into primary domains (agents, workflows, approvals, knowledge, evaluations). |
| FR-08-04 | When dashboard data is loading, the frontend shall show loading states (skeletons or equivalent). |
| FR-08-05 | When dashboard data is empty (no agents/workflows), the frontend shall show empty states with an onboarding checklist guidance. |
| FR-08-06 | When dashboard API calls fail, the frontend shall show error states with retry and request_id when available. |
| FR-08-07 | The dashboard shall include a header/summary region and a metric card grid for operational counters when data exists (e.g., active agents, workflows running, pending approvals, failed runs). |
| FR-08-08 | When the user selects a quick action (create agent, create workflow, review approvals, or equivalent), the frontend shall navigate to the corresponding domain route. |
| FR-08-09 | If a dashboard section’s API fails while others succeed, the frontend shall isolate the failure to that section without blanking the entire shell. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-08-01 | Dashboard shall prioritize above-the-fold attention metrics over secondary widgets. |
| NFR-08-03 | Dashboard initial content shall remain interactive within the shell without full-app blocking spinners. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-08-02 | Dashboard shall only show data returned for the authenticated org/user scope. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-08-01 | Authenticated user lands on dashboard after login. |
| AC-08-02 | Loading/empty/error states are implemented. |
| AC-08-03 | Links from dashboard reach domain routes. |
| AC-08-04 | Metric/attention regions match frontend.md §16.4 intent when data is present. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-08-01 | Manual E1: post-login dashboard visible. | Manual |
| TV-08-02 | Unit: empty state when API returns empty lists. | Unit |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.4 Dashboard | FR-08-01 … FR-08-06 |
| Phase 6 | AC-08-* |
""",
}

# ── FE-09 ──────────────────────────────────────────────────────────────────
CONTENT["09"] = {
    "scope": """### 1.1 In scope
- Agents list, create agent, agent detail pages.
- Tools list and tool detail pages.
- Forms with frontend validation (Zod/react-hook-form or equivalent) posting to backend.
- Display of agent/tool metadata, status, and backend errors.

### 1.2 Out of scope
- Agent/tool execution engines (backend).
- Tool adapter implementation.

### 1.3 System under specification
Agents and tools management UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-09-01 | Developers / operators | Register and inspect agents and tools. |
| STK-09-02 | Reviewers | Read-only visibility when permitted. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-09-01 | The frontend shall provide agents list, create, and detail views under `/app/agents`. |
| FR-09-02 | The frontend shall provide tools list and detail views under `/app/tools`. |
| FR-09-03 | When creating or updating an agent, the frontend shall validate required fields client-side and submit to backend agent APIs. |
| FR-09-04 | When backend rejects an agent/tool mutation, the frontend shall display the error and request_id. |
| FR-09-05 | When agent or tool detail data is returned, the frontend shall display identity, configuration summary, and status fields. |
| FR-09-06 | If the user lacks permission to create agents/tools, the frontend shall hide or disable create actions. |
| FR-09-07 | The frontend shall not execute agents or tools locally; execution remains a backend responsibility. |
| FR-09-08 | When the agents list is empty and the user may create agents, the frontend shall show an empty state with a create affordance. |
| FR-09-09 | When rendering list rows, the frontend shall show status badges using the shared status vocabulary (not color alone). |
| FR-09-10 | If tool metadata would require displaying a provider secret, the frontend shall omit or redact it and show only backend-safe fields. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-09-01 | List views shall support pagination or virtualization when lists grow large. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-09-02 | Tool configuration UI shall not accept or display raw provider secrets beyond backend-safe metadata. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-09-01 | Create agent form works against live backend in ops profile. |
| AC-09-02 | Agents and tools lists render API data. |
| AC-09-03 | Permission-denied create is gated in UI. |
| AC-09-04 | Status badges and empty/error states present on list views. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-09-01 | Unit: form schema rejects empty name. | Unit |
| TV-09-02 | Integration/manual: create agent → appears in list. | Integration |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.5–16.9 Agents/Tools | FR-09-01 … FR-09-05 |
| §4.2 / §6.2 no execution | FR-09-07 |
| Phase 7 | AC-09-* |
""",
}

# ── FE-10 ──────────────────────────────────────────────────────────────────
CONTENT["10"] = {
    "scope": """### 1.1 In scope
- Workflows list, create workflow, workflow detail pages.
- Run-now entry points from workflow surfaces.
- Display of workflow versions/definitions metadata from backend.
- Frontend validation of create/edit forms.

### 1.2 Out of scope
- Workflow execution engine (BE-11).
- Realtime run timeline (FE-11).
- DNA mutation outside backend sandbox APIs.

### 1.3 System under specification
Workflow definition management UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-10-01 | Operators | Create and inspect workflow definitions. |
| STK-10-02 | Developers | Configure workflow structure via backend-supported fields. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-10-01 | The frontend shall provide workflows list, create, and detail views under `/app/workflows`. |
| FR-10-02 | When creating a workflow, the frontend shall validate input and POST to backend workflow APIs. |
| FR-10-03 | Workflow detail shall show definition metadata, version information, and available actions returned/allowed by backend. |
| FR-10-04 | When the user triggers Run Now, the frontend shall request run creation from the backend with a valid payload. |
| FR-10-05 | If run creation fails, the frontend shall show backend errors without claiming a run started. |
| FR-10-06 | The frontend shall not implement workflow execution logic in the browser. |
| FR-10-07 | Permission-aware controls shall gate create/run actions as UX only. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-10-01 | Workflow list load shall not block the entire app shell. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-10-02 | Workflow payloads shall not include secrets; references only as backend allows. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-10-01 | Create workflow form works in ops profile. |
| AC-10-02 | Run now creates a backend run and navigates to run detail when successful. |
| AC-10-03 | Lists show backend workflows. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-10-01 | Unit: create form validation. | Unit |
| TV-10-02 | E1: run-now path from workflow. | E2E / manual |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.10–16.12 Workflows | FR-10-01 … FR-10-05 |
| §4.2 no execution logic | FR-10-06 |
| Phase 8 | AC-10-* |
""",
}

# ── FE-11 ──────────────────────────────────────────────────────────────────
CONTENT["11"] = {
    "scope": """### 1.1 In scope
- Workflow run detail page (`/app/workflow-runs/[runId]`).
- Steps/timeline visualization.
- Realtime updates via SSE/WebSocket/polling per backend contract (§21).
- Run actions: cancel, retry when supported; pause/resume/expire controls wired to backend lifecycle routes.
- Status badges including paused/expired semantics.
- Error and request_id display for failed steps.

### 1.2 Out of scope
- Backend run engine (BE-11).
- Improve pipeline controls (FE-18) beyond placement hooks.
- Approval decision API details (FE-12).

### 1.3 System under specification
Live workflow run observation and lifecycle UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-11-01 | Operators | Watch runs progress and intervene (cancel/pause) when allowed. |
| STK-11-02 | Support | See step failures with correlation IDs. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-11-01 | The frontend shall provide a workflow run detail page for a given runId. |
| FR-11-02 | When run data is loaded, the run detail page shall display run status, steps/timeline, and timestamps from backend data. |
| FR-11-03 | When realtime events are available, the frontend shall update the run UI without full page reload. |
| FR-11-04 | If realtime transport fails, the frontend shall fall back to polling or show a degraded-live indicator. |
| FR-11-05 | When the user is permitted and the run status allows, the frontend shall offer cancel and retry actions that call backend APIs. |
| FR-11-06 | When backend supports pause/resume/expire and the run status allows, the frontend shall expose controls calling those lifecycle endpoints. |
| FR-11-07 | The frontend shall render status badges for running, succeeded, failed, awaiting approval, paused, cancelled (and expired when returned). |
| FR-11-08 | The frontend shall not execute workflow steps in the browser. |
| FR-11-09 | When a step fails, the frontend shall display the failure context and request_id/correlation when provided by the backend. |
| FR-11-10 | If the run is waiting for approval, the frontend shall surface a human-gate callout with navigation or embedded actions to the approvals flow. |
| FR-11-11 | When the Improve pipeline is available for the run, the frontend shall reserve UI space for Improve controls (FE-18) without auto-starting improve steps. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-11-01 | Realtime handlers shall avoid unbounded memory growth on long-running streams. |
| NFR-11-02 | Timeline rendering shall remain usable for typical step counts of MVP workflows. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-11-03 | Stream subscriptions shall require authenticated session. |
| NFR-11-04 | Run actions shall send only backend-defined payloads. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-11-01 | Run detail shows steps for a live run. |
| AC-11-02 | Status updates reflect backend changes (stream or poll). |
| AC-11-03 | Pause/resume/expire controls call documented APIs when enabled. |
| AC-11-04 | Cancel/retry respect permission UX. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-11-01 | Manual: start run → observe status transitions. | Manual |
| TV-11-02 | Unit: status badge mapping for paused. | Unit |
| TV-11-03 | Integration: lifecycle POST paths. | Integration |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.13 Run detail | FR-11-01 … FR-11-02, FR-11-05 … FR-11-07 |
| §21 Realtime | FR-11-03 … FR-11-04 |
| §33.3a Run lifecycle | FR-11-06 |
| Phase 9 | AC-11-* |
""",
}

# ── FE-12 ──────────────────────────────────────────────────────────────────
CONTENT["12"] = {
    "scope": """### 1.1 In scope
- Approvals list and approval detail pages.
- Approve / reject (and decision notes) actions via backend.
- Human-gate surfaces on run detail linkage.
- Queue prioritization UX for items needing attention.

### 1.2 Out of scope
- Backend policy engine (BE-12/13).
- Silent auto-approve in the client.

### 1.3 System under specification
Human approval gates UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-12-01 | Reviewers / operators | Clear approve/reject with context. |
| STK-12-02 | Compliance | Evidence of human decision stays on backend audit. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-12-01 | The frontend shall provide approvals list and detail routes under `/app/approvals`. |
| FR-12-02 | When approval data is loaded, the frontend shall show request context, risk/tier hints when provided, and related run/workflow references. |
| FR-12-03 | When the user explicitly approves or rejects, the frontend shall call backend approval APIs and refresh state. |
| FR-12-04 | If the backend denies the decision, the frontend shall display the error and leave local state consistent with server. |
| FR-12-05 | The frontend shall not auto-approve high-risk actions without an explicit user action. |
| FR-12-06 | When a run has a pending gate, run detail shall deep-link or embed gate actions for that approval. |
| FR-12-07 | If the user lacks approve/reject permission, the frontend shall hide or disable decision controls. |
| FR-12-08 | When the user submits a decision, the frontend shall allow optional decision notes if the backend accepts them. |
| FR-12-09 | If decision submission is in progress, the frontend shall disable double-submit on approve/reject controls. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-12-01 | Approvals list shall load pending items preferentially. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-12-02 | Approval decisions shall require authenticated session and backend authorization. |
| NFR-12-03 | Client shall not forge approval records offline as authoritative. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-12-01 | Pending approval appears in list when backend has one. |
| AC-12-02 | Approve/reject updates status via API. |
| AC-12-03 | No silent auto-approve path in UI. |
| AC-12-04 | In-progress decision disables double-submit. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-12-01 | E1: human gate approve/reject. | E2E / manual |
| TV-12-02 | Unit: decision form requires explicit action. | Unit |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.14–16.15 Approvals | FR-12-01 … FR-12-04, FR-12-07 |
| §33.3 Human gates | FR-12-05 … FR-12-06 |
| Phase 10 | AC-12-* |
""",
}

# ── FE-13 ──────────────────────────────────────────────────────────────────
CONTENT["13"] = {
    "scope": """### 1.1 In scope
- Knowledge overview, sources, documents, and search pages.
- Memory list/detail inspection pages.
- Read-oriented ops UX over backend knowledge/memory APIs.
- Source connection forms only insofar as backend supports (no live CRM requirement for product bar).

### 1.2 Out of scope
- Embedding/indexing engines (backend).
- Full commercial LightRAG/Neo4j explorer product (§33.5 non-goal).
- Direct vector DB access from browser.

### 1.3 System under specification
Knowledge and memory operator UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-13-01 | Operators | See what knowledge sources and memories exist. |
| STK-13-02 | Reviewers | Inspect provenance fields when backend returns them. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-13-01 | The frontend shall provide knowledge routes for overview, sources, documents, and search. |
| FR-13-02 | The frontend shall provide memory list and detail routes under `/app/memory`. |
| FR-13-03 | Knowledge/memory views shall render backend-returned metadata and shall not invent index contents. |
| FR-13-04 | When search is invoked, the frontend shall call backend retrieval APIs and display results with available provenance. |
| FR-13-05 | The frontend shall not perform embedding or indexing in the browser. |
| FR-13-06 | Mutations (add source, delete memory) shall only occur through backend APIs when exposed and permitted. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-13-01 | Search UI shall debounce queries to avoid request storms. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-13-02 | Knowledge UI shall not exfiltrate full corpora beyond what backend returns to the caller. |
| NFR-13-03 | Memory detail shall respect permission UX for sensitive records. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-13-01 | Knowledge and memory pages render in app shell. |
| AC-13-02 | Search calls backend and shows results or empty state. |
| AC-13-03 | No client-side vector store dependency. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-13-01 | Manual: open knowledge/memory sections. | Manual |
| TV-13-02 | Unit: search debounce. | Unit |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.16–16.19 Knowledge/Memory | FR-13-01 … FR-13-04 |
| §4.2 no embedding | FR-13-05 |
| Phase 11 | AC-13-* |
""",
}

# ── FE-14 ──────────────────────────────────────────────────────────────────
CONTENT["14"] = {
    "scope": """### 1.1 In scope
- Evaluations list/detail and evaluation run views.
- Processes list/detail for process intelligence artifacts.
- Display of quality metrics and PI summaries returned by backend.
- Links from quality nav group.

### 1.2 Out of scope
- Running eval engines in the browser.
- Full process mining product beyond backend artifacts.

### 1.3 System under specification
Evaluations and process intelligence UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-14-01 | Quality operators | Inspect evaluation outcomes. |
| STK-14-02 | Process owners | View process intelligence summaries. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-14-01 | The frontend shall provide evaluations list and detail routes under `/app/evaluations`. |
| FR-14-02 | The frontend shall provide processes list and detail routes under `/app/processes`. |
| FR-14-03 | Evaluation views shall display scores, statuses, and artifacts metadata returned by backend. |
| FR-14-04 | Process views shall display PI summaries/artifacts/events as returned by backend. |
| FR-14-05 | When starting an evaluation is supported, the frontend shall call backend evaluation APIs rather than computing scores locally. |
| FR-14-06 | The frontend shall not claim eval pass/fail without backend results. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-14-01 | Large eval result payloads shall be paginated or truncated in UI with expand options. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-14-02 | Eval/process views shall respect permission-aware access. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-14-01 | Evaluations and processes pages accessible from Quality nav. |
| AC-14-02 | Detail pages render backend payloads or empty states. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-14-01 | Manual: navigate Quality group. | Manual |
| TV-14-02 | Unit: empty state components. | Unit |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.20–16.22 Evals/Processes | FR-14-01 … FR-14-06 |
| Phase 12 | AC-14-* |
""",
}

# ── FE-15 ──────────────────────────────────────────────────────────────────
CONTENT["15"] = {
    "scope": """### 1.1 In scope
- Audit logs list page with filters (time, actor, action, resource) as backend supports.
- Read-only presentation of audit events.
- Deep links to related entities when IDs are present.

### 1.2 Out of scope
- Creating audit events in the frontend (backend only).
- Tamper-evident store implementation.

### 1.3 System under specification
Audit log review UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-15-01 | Security auditors | Review who did what. |
| STK-15-02 | Operators | Diagnose recent sensitive actions. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-15-01 | The frontend shall provide an audit logs page under `/app/audit-logs`. |
| FR-15-02 | Audit logs UI shall fetch events from backend audit APIs. |
| FR-15-03 | When filters are provided by the product, the frontend shall pass filter query params to the backend. |
| FR-15-04 | The frontend shall not create, edit, or delete audit events client-side as system of record. |
| FR-15-05 | Each event row shall display actor, action, timestamp, and resource identifiers when returned. |
| FR-15-06 | Permission-aware UI shall restrict audit access for roles without permission. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-15-01 | Audit list shall paginate. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-15-02 | Audit UI shall not allow clients to forge historical events. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-15-01 | Audit page lists backend events or empty state. |
| AC-15-02 | No client write path for audit records. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-15-01 | Manual: open audit logs as permitted user. | Manual |
| TV-15-02 | Review: no POST audit from FE client modules. | Review |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.23 Audit Logs | FR-15-01 … FR-15-06 |
| §4.2 no audit creation | FR-15-04 |
| Phase 13 (audit) | AC-15-* |
""",
}

# ── FE-16 ──────────────────────────────────────────────────────────────────
CONTENT["16"] = {
    "scope": """### 1.1 In scope
- Settings hub and subpages: organization, users, roles (as supported), billing placeholder, API keys, security, integrations, profile.
- User management list/invite/disable UX calling BE-07 APIs.
- Organization settings GET/PATCH.
- API key management UI via backend key endpoints.
- Security settings presentation.
- Accept-invite linkage for invitations created from settings.

### 1.2 Out of scope
- Billing calculation engines.
- Backend tenancy enforcement (BE-07).
- Live external billing SaaS admin consoles (§33.5 non-goal).

### 1.3 System under specification
Organization administration and settings UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-16-01 | Org admins | Manage users, org profile, API keys. |
| STK-16-02 | Billing managers | See billing placeholder or backend-supported billing page. |
| STK-16-03 | Security admins | View/configure security settings exposed by backend. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-16-01 | The frontend shall provide a settings hub under `/app/settings` with sub-routes for organization, users, roles, billing, API keys, security, integrations, and profile as specified. |
| FR-16-02 | User management UI shall list users via backend and support invite/disable/update actions through BE-07 APIs when permitted. |
| FR-16-03 | Organization settings UI shall load and save organization fields via GET/PATCH organization APIs. |
| FR-16-04 | API keys UI shall create/list/revoke keys only through backend auth/API key endpoints. |
| FR-16-05 | Billing page may be a placeholder if backend lacks billing; it shall not invent charges. |
| FR-16-06 | Security settings UI shall display backend-provided security configuration and not store secrets in browser code. |
| FR-16-07 | Invitation creation from settings shall use backend invitation APIs; accept flow remains on `/accept-invite` (FE-05). |
| FR-16-08 | Permission-aware UI shall restrict admin settings to authorized roles. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-16-01 | Settings forms shall avoid full app remounts on save success. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-16-02 | Newly created API key secrets shall be shown once (if backend returns plaintext once) and not re-fetchable from FE cache. |
| NFR-16-03 | User disable/invite actions require confirmation where destructive. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-16-01 | Settings nav links resolve to settings surfaces. |
| AC-16-02 | Users invite/list wired to backend invitations/users APIs (or documented gap). |
| AC-16-03 | Organization save calls PATCH when implemented. |
| AC-16-04 | API keys page uses backend endpoints. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-16-01 | Manual: admin opens settings users/org. | Manual |
| TV-16-02 | Integration: invite POST path. | Integration |
| TV-16-03 | Review: no billing math in FE. | Review |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.24–16.28 Settings suite | FR-16-01 … FR-16-08 |
| §33.3a Users/Orgs/Invitations | FR-16-02 … FR-16-03, FR-16-07 |
| Phase 13 Settings | AC-16-* |
""",
}

# ── FE-17 ──────────────────────────────────────────────────────────────────
CONTENT["17"] = {
    "scope": """### 1.1 In scope
- Evolution archive page at `/app/evolution`.
- Display of sandbox variants, fitness ranking, archive metadata from backend.
- Actions that call backend evolution APIs only (evaluate, promote, rollback as exposed).
- Explicit sandbox-only messaging; no production DNA rewrite UI.

### 1.2 Out of scope
- Evolution engine implementation (BE-20).
- DGM-style host self-rewrite UI (§33.5).
- Silent production activation from FE.

### 1.3 System under specification
Evolution sandbox archive operator UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-17-01 | Evolution operators | Browse sandbox population and fitness. |
| STK-17-02 | Governance | No path to silent production DNA mutation from UI. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-17-01 | The frontend shall provide an evolution archive page under `/app/evolution`. |
| FR-17-02 | The page shall list sandbox variants and fitness/ranking data returned by backend evolution APIs. |
| FR-17-03 | When evaluate/promote/rollback actions are available, the frontend shall call backend evolution endpoints only. |
| FR-17-04 | The frontend shall not implement client-side production DNA mutation or host application self-rewrite. |
| FR-17-05 | UI copy shall communicate sandbox / gated promotion semantics when promoting variants. |
| FR-17-06 | Permission-aware UI shall gate evolution admin actions. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-17-01 | Archive lists shall paginate when populations grow. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-17-02 | Evolution mutations shall require authenticated, authorized backend calls. |
| NFR-17-03 | If a UI path would skip backend sandbox validation, it shall be rejected in design. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-17-01 | `/app/evolution` renders archive from backend or empty state. |
| AC-17-02 | No client DNA rewrite module exists. |
| AC-17-03 | Promote/rollback only via backend APIs. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-17-01 | Manual: open evolution archive. | Manual |
| TV-17-02 | Review: grep FE for production DNA write — none. | Review |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §16.13a Evolution Archive | FR-17-01 … FR-17-03 |
| §4.2 / §33.3 Evolution UI | FR-17-04 … FR-17-05 |
| structure.md §5 | FR-17-04 |
""",
}

# ── FE-18 ──────────────────────────────────────────────────────────────────
CONTENT["18"] = {
    "scope": """### 1.1 In scope
- Improve pipeline controls on workflow run detail: Reflect → Propose → Evaluate → Canary.
- Calls to backend improvement/loop APIs (reflect, lessons, auto-propose, evaluate, canary-related).
- Explicit operator-triggered steps (no silent infinite self-improve loop in UI).
- Display of intermediate results and errors.

### 1.2 Out of scope
- Backend self-improvement engines (BE-21).
- Automatic production promotion without gates.
- Host code rewrite.

### 1.3 System under specification
Self-improvement operator pipeline UI.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-18-01 | Operators | Drive improve steps deliberately on a run. |
| STK-18-02 | Governance | Each step visible, gated, backend-enforced. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-18-01 | The frontend shall expose an Improve pipeline on workflow run detail with ordered steps Reflect, Propose, Evaluate, and Canary. |
| FR-18-02 | When the user activates an Improve step, the frontend shall call the corresponding backend improvement/evolution APIs. |
| FR-18-03 | The frontend shall require explicit user action to advance each Improve step. |
| FR-18-04 | When a step fails, the frontend shall show backend errors and shall not mark the pipeline successful. |
| FR-18-05 | The frontend shall not silently loop Improve steps without operator intent. |
| FR-18-06 | When canary or promote is invoked, the frontend shall call sandbox-gated backend APIs only and shall not write production DNA in the browser. |
| FR-18-07 | When a step succeeds, the Improve UI shall display evidence/results returned by backend for operator review. |
| FR-18-08 | While a step is in progress, the frontend shall show in-progress state and prevent concurrent duplicate step submissions. |
| FR-18-09 | If the user lacks permission for improve actions, the frontend shall hide or disable the Improve controls. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-18-01 | Long-running improve steps shall show in-progress state until backend completes or times out gracefully. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-18-02 | Improve actions shall never bypass backend authorization. |
| NFR-18-03 | Improve UI shall not write production DNA locally. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-18-01 | Run detail shows Improve step controls. |
| AC-18-02 | Reflect/propose/evaluate/canary invoke backend routes. |
| AC-18-03 | No automatic unattended infinite improve loop in UI. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-18-01 | E1: improve path on run detail. | E2E / manual |
| TV-18-02 | Unit: step state machine requires explicit next. | Unit |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §1 Improve pipeline | FR-18-01 |
| §16.13 Improve actions | FR-18-02 … FR-18-07 |
| §33.3 Self-improvement UI | AC-18-* |
""",
}

# ── FE-19 ──────────────────────────────────────────────────────────────────
CONTENT["19"] = {
    "scope": """### 1.1 In scope
- Cross-cutting loading, empty, and error state patterns (§22).
- Accessibility requirements (§23): keyboard, focus, labels, contrast targets (WCAG 2.2 AA intent).
- Consistent error presentation including request_id.
- Preferential use of design-system state components (FE-03).

### 1.2 Out of scope
- Full legal compliance certification.
- Domain-specific content for every empty state narrative beyond patterns.

### 1.3 System under specification
UX quality system for states and accessibility.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-19-01 | All users | Understand loading, empty, and failure conditions. |
| STK-19-02 | Users of assistive tech | Keyboard and screen-reader operable console. |
| STK-19-03 | Support | Errors include correlatable request IDs. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-19-01 | Every major data page shall implement loading, empty, and error states. |
| FR-19-02 | Error states shall show human-readable messages and request_id when the API provides one. |
| FR-19-03 | Interactive controls shall be keyboard operable for primary flows. |
| FR-19-04 | Form inputs shall have accessible labels. |
| FR-19-05 | Focus shall be managed for modals and drawers (trap/restore as appropriate). |
| FR-19-06 | Status information shall not rely on color alone. |
| FR-19-07 | Empty states shall include guidance on next actions when applicable. |
| FR-19-08 | The frontend shall target WCAG 2.2 Level AA practices for core operator flows. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-19-01 | Loading skeletons shall avoid layout thrash where practical. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-19-02 | Error messages shall not dump stack traces or secrets to end users in production builds. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-19-01 | Representative pages (dashboard, runs, approvals) show all three states. |
| AC-19-02 | Primary forms have labels; modals keyboard-dismissible. |
| AC-19-03 | Production errors omit secrets/stack traces. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-19-01 | Manual keyboard pass on shell + one form. | Manual / a11y |
| TV-19-02 | Unit: ErrorState renders request_id. | Unit |
| TV-19-03 | Optional axe scan on key routes. | Automated |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §22 Loading/Empty/Error | FR-19-01 … FR-19-02, FR-19-07 |
| §23 Accessibility | FR-19-03 … FR-19-06, FR-19-08 |
| §25/§24 message safety | NFR-19-02 |
""",
}

# ── FE-20 ──────────────────────────────────────────────────────────────────
CONTENT["20"] = {
    "scope": """### 1.1 In scope
- Frontend security requirements (§24): XSS hygiene, no secrets in client, CSRF/credentials per design, dependency hygiene notes.
- Performance requirements (§25) for navigation and list responsiveness.
- Observability hooks (§26): client error reporting hooks if present; correlation with request_id.
- Testing requirements (§27): unit, lint, typecheck, build; E2E smoke/E1 path as practical.
- Phase 14 quality/security/release gates.
- Acceptance criteria and definition of done for pages (§30–31).
- Ops profile proof: `NEXT_PUBLIC_DEMO_MODE=false` + live backend + Postgres.
- Explicit non-goals for product bar (§33.5).

### 1.2 Out of scope
- Always-on Playwright CI with permanent servers (non-goal if servers down).
- Backend security hardening (BE-23).
- Full load test suite.

### 1.3 System under specification
Cross-cutting quality, security, testing, and operator-path proof for the frontend.
""",
    "stakeholders": """| ID | Stakeholder | Need |
|---|---|---|
| STK-20-01 | Release managers | Clear DoD for frontend ship. |
| STK-20-02 | Security | Client-side threat mitigations documented and tested at smoke level. |
| STK-20-03 | Operators | E1 path works on ops profile. |
""",
    "fr": """| ID | Statement (EARS) |
|---|---|
| FR-20-01 | The frontend shall enforce security hygiene: no provider secrets in client bundles, safe rendering of untrusted text, and auth credentials handled per backend contract. |
| FR-20-02 | The frontend shall meet performance expectations for interactive ops use (responsive navigation, non-blocking lists for MVP data sizes). |
| FR-20-03 | The frontend shall provide automated lint, typecheck, unit tests, and production build as quality gates. |
| FR-20-04 | When servers are available, the frontend shall support an operator E1 path: login → dashboard → run → gate → improve as applicable. |
| FR-20-05 | The ops profile shall run with `NEXT_PUBLIC_DEMO_MODE=false` against a live backend and Postgres. |
| FR-20-06 | Each page DoD shall include: routes, permission awareness, loading/empty/error, API wiring or documented stub, and no charter violations. |
| FR-20-07 | Product-bar non-goals (always-on UI CI servers, full graph explorer, live CRM/email/billing admin, host self-rewrite UI, client-only authz) shall not be treated as missing requirements for mark ~100. |
| FR-20-08 | Client observability shall preserve request_id on failures for support correlation when available. |
""",
    "nfr": """### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-20-01 | Production build shall complete in CI-reasonable time for the repo’s frontend package. |
| NFR-20-02 | Bundle shall code-split heavy client widgets (run timeline, command palette) where practical. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-20-03 | Dependency vulnerabilities in FE lockfile shall be reviewed before release claims. |
| NFR-20-04 | DEMO_MODE shall not be required for security; live mode must still enforce backend auth. |
""",
    "ac": """| ID | Criterion |
|---|---|
| AC-20-01 | `pnpm lint`, `pnpm typecheck`, unit tests, and `pnpm build` green. |
| AC-20-02 | Ops profile documented and usable for E1. |
| AC-20-03 | Security checklist items in §24 addressed or explicitly deferred with owner. |
| AC-20-04 | Non-goals list matches frontend.md §33.5. |
""",
    "tv": """| ID | Protocol | Type |
|---|---|---|
| TV-20-01 | CI: lint + typecheck + unit + build. | Automated |
| TV-20-02 | Manual/E2E: E1 operator path when stack up. | E2E |
| TV-20-03 | Review: secrets scan on frontend env samples. | Review |
| TV-20-04 | Document review: §30–31 acceptance mapped to FE specs. | Traceability |
""",
    "trace": """| frontend.md | This spec |
|---|---|
| §24 Security | FR-20-01, NFR-20-03 … NFR-20-04 |
| §25 Performance | FR-20-02, NFR-20-01 … NFR-20-02 |
| §26 Observability | FR-20-08 |
| §27 Testing | FR-20-03 |
| §28 Phase 14 / §30–31 | FR-20-06, AC-20-* |
| §33.5–33.7 | FR-20-04 … FR-20-05, FR-20-07 |
""",
}


def render(nn: str, slug: str, title: str, source: str, related: str, depends: str, provides: str) -> str:
    c = CONTENT[nn]
    return (
        doc_control(nn, title, source, related)
        + f"""
## 1. Scope

{c['scope']}

---

## 2. Stakeholder Requirements

{c['stakeholders']}

---

## 3. Functional Requirements (EARS)

{c['fr']}

---

## 4. Non-Functional Requirements

{c['nfr']}

---

## 5. Acceptance Criteria

{c['ac']}

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| {depends} | {provides} |

---

## 7. Test Validation Protocols

{c['tv']}

---

## 8. Traceability

{c['trace']}
"""
    )


def write_readme() -> None:
    rows = []
    for nn, slug, title, source, related, depends, provides in SPECS:
        rows.append(f"| {nn} | {title} | {source} |")
    table = "\n".join(rows)
    readme = f"""# frontend.md — Sub-Functional Specifications

**Source:** `frontend.md` (Frontend Server / Ops Console Requirements, Design, and Implementation Plan)  
**Architecture SoT:** `structure.md` (§10–§12; implementation mapping)  
**Backend control plane:** `backend.md` + `planning/backend/` (FE never re-implements policy)  
**Path pattern:** `planning/frontend/nn_<sub-func-spec>/requirements.md`  
**Requirement style:** EARS (Easy Approach to Requirements Syntax)  
**Ordering:** `nn` is the sequential implementation priority (charter → scaffold → design system → shell/auth → API client → domain pages → evolution/improve → cross-cutting quality)

## Execution order

| nn | Component | frontend.md mapping |
|----|-----------|---------------------|
{table}

## Dependency sketch

```text
01 charter
 └── 02 Next.js scaffold/stack
      └── 03 design system / OpenDesign
           ├── 07 typed API client / OpenAPI
           ├── 05 auth & session UI
           │     └── 06 permission-aware UI
           └── 04 app shell / IA / navigation
                ├── 08 dashboard
                ├── 09 agents & tools
                ├── 10 workflows ──► 11 run realtime
                │                      ├── 12 approvals / human gates
                │                      └── 18 improve pipeline
                ├── 13 knowledge & memory
                ├── 14 evaluations & processes
                ├── 15 audit logs
                ├── 16 settings / users / org / API keys
                ├── 17 evolution archive ──► 18 improve
                ├── 19 a11y + loading/empty/error (cross-cutting)
                └── 20 security / performance / testing / ops profile
```

## Document set (per component)

| File | Role |
|------|------|
| `requirements.md` | EARS requirements + scope, stakeholders, NFR, acceptance, dependencies, test protocols |
| `design.md` | SDD design v2.0: architecture, visual/UI, ICD, RTM (**score 100**; see `DESIGN_QUALITY_SCORE.md`) |
| `tasks.md` | *(optional next)* implementation backlog with code deliverables |
| `DESIGN_QUALITY_SCORE.md` | Portfolio design quality assessment report (**100/100**) |

## Document template (each `requirements.md`)

1. Document control  
2. Scope  
3. Stakeholder requirements  
4. Functional requirements (EARS)  
5. Non-functional requirements (performance & security)  
6. Acceptance criteria  
7. Integration dependencies  
8. Test validation protocols  
9. Traceability to `frontend.md` / `structure.md` / backend contracts  

## Recommended global build order

```text
01 charter → 02 scaffold → 03 design system
→ 07 API client → 05 auth UI → 06 permissions → 04 app shell
→ 08 dashboard → 09 agents/tools → 10 workflows → 11 run realtime
→ 12 approvals → 13 knowledge/memory → 14 evals/processes
→ 15 audit → 16 settings → 17 evolution → 18 improve
→ 19 a11y/states → 20 security/testing/ops proof
```

## EARS patterns used

| Pattern | Template |
|---------|----------|
| Ubiquitous | The frontend shall … |
| Event-driven | When <event>, the frontend shall … |
| State-driven | If <precondition>, the frontend shall … |
| Unwanted | If <unwanted>, the frontend shall not … / shall reject … |

## Related indexes

| Artifact | Path |
|----------|------|
| Parent plan | `frontend.md` |
| As-built code | `frontend/` |
| Backend SDD | `planning/backend/` |
| Structure SDD | `planning/structure/` |
| Backend API contracts (FE must honor) | `frontend.md` §33.3a, `planning/backend/TASK_TO_CODE_TRACEABILITY.md` |

## Generator

Regenerate requirements from this script:

```bash
python scripts/_gen_frontend_reqs.py
```
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    assert set(CONTENT) == {s[0] for s in SPECS}, "CONTENT keys must match SPECS nn"
    for nn, slug, title, source, related, depends, provides in SPECS:
        folder = ROOT / f"{nn}_{slug}"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "requirements.md"
        path.write_text(
            render(nn, slug, title, source, related, depends, provides).lstrip() + "\n",
            encoding="utf-8",
        )
        print(f"wrote {path}")
    write_readme()
    print(f"wrote {ROOT / 'README.md'}")
    print(f"OK: {len(SPECS)} frontend sub-functional requirements packs")


if __name__ == "__main__":
    main()
