# 02 — Next.js Scaffold, Stack, and Folder Structure

| Field | Value |
|-------|-------|
| Spec ID | `FE-02` |
| Source | `frontend.md` — §5 Recommended Technology Stack, §7 Application Architecture, §18 Frontend Folder Structure, §19 Environment Variables, Phase 1 Project Setup |
| Related architecture | structure.md §12.3 ops console entry |
| Priority order | 02 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
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


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-02-01 | Frontend engineers | Reproducible Next.js TypeScript app with known scripts. |
| STK-02-02 | Operators / deployers | Documented env vars for ops vs demo profiles. |
| STK-02-03 | CI | lint, typecheck, unit test, and build commands. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
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


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-02-01 | Local `pnpm dev` shall start the app for interactive development without requiring a full production build. |
| NFR-02-02 | Production `pnpm build` shall succeed for the scaffolded app shell before domain pages are complete. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-02-03 | Secrets used only on the server shall not be prefixed with `NEXT_PUBLIC_`. |
| NFR-02-04 | Client-exposed env shall be limited to non-secret configuration (API URL, demo flag, public app metadata). |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-02-01 | App starts locally with TypeScript and Tailwind working. |
| AC-02-02 | Lint and typecheck scripts pass on scaffold. |
| AC-02-03 | Folder structure matches frontend.md §18 intent (or documented as-built equivalent). |
| AC-02-04 | Env template documents API URL and DEMO_MODE. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-01 | FE-03+ |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-02-01 | Run install → lint → typecheck → build on clean checkout. | Automated |
| TV-02-02 | Review: no provider secrets in NEXT_PUBLIC_* sample env. | Review |
| TV-02-03 | Smoke: unauthenticated `/app` redirects to login. | Manual / E2E |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §5 Technology Stack | FR-02-01 … FR-02-02 |
| §7 Application Architecture | FR-02-03 … FR-02-04, FR-02-08 |
| §18 Folder Structure | FR-02-05 |
| §19 Environment Variables | FR-02-06, NFR-02-03 … NFR-02-04 |
| Phase 1 Project Setup | FR-02-07, FR-02-09, AC-02-* |


