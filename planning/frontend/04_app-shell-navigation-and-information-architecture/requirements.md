# 04 — App Shell, Navigation, and Information Architecture

| Field | Value |
|-------|-------|
| Spec ID | `FE-04` |
| Source | `frontend.md` — §7.3 Route Protection, §12 Information Architecture, §14 Core Layout Design, Phase 5 App Shell |
| Related architecture | structure.md human-centered ops console |
| Priority order | 04 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
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


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-04-01 | Operators | Predictable navigation and deep links to ops surfaces. |
| STK-04-02 | Multi-org users | Organization context visible and switchable when supported. |
| STK-04-03 | Power users | Command palette for frequent actions. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
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


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-04-01 | App shell chrome shall remain responsive during client navigations between domain panels. |
| NFR-04-02 | Command palette shall open without full page reload. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-04-03 | Client route guards shall not replace backend authorization. |
| NFR-04-04 | User menu and org switcher shall not expose tokens in the DOM beyond necessary display fields. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-04-01 | Authenticated shell renders sidebar + header + content. |
| AC-04-02 | Navigation groups match §12.2 labels. |
| AC-04-03 | Unauthenticated access to `/app` redirects to login. |
| AC-04-04 | Command palette opens via keyboard shortcut. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-02, FE-03, FE-05 | All /app/* domain pages |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-04-01 | Manual: walk each nav group link. | Manual |
| TV-04-02 | Unit/integration: route guard redirect when session missing. | Automated |
| TV-04-03 | Keyboard: Cmd/Ctrl+K opens palette. | Manual / a11y |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §12 Information Architecture | FR-04-02 … FR-04-03, FR-04-07 … FR-04-10 |
| §7.3 Route Protection | FR-04-04 … FR-04-06, NFR-04-03 |
| §14 Core Layout | FR-04-01 |
| Phase 5 App Shell | AC-04-* |


