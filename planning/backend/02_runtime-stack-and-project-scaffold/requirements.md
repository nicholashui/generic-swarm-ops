# 02 — Runtime Stack and Project Scaffold

| Field | Value |
|-------|-------|
| Spec ID | `BE-02` |
| Source | `backend.md` — §3 Recommended Technology Stack, §9 Recommended Backend Folder Structure, §8.5 Maintainability |
| Related architecture | structure.md §12.5 Backend entry |
| Priority order | 02 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Recommended technology stack (FastAPI, Python, PostgreSQL primary, optional Redis/queue/vector/object storage).
- Project layout under backend/ (app layers: api, core, domain, infrastructure).
- Local development without Docker as a hard requirement.
- Layered maintainability: routes → services → domain → infrastructure adapters.

### 1.2 Out of scope
- Final vendor lock to a specific queue or vector product.
- Frontend package layout.
- Production multi-region deployment topology details beyond stack recommendations.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-02-01 | Engineers | Reproducible scaffold and clear module boundaries. |
| STK-02-02 | Ops | Runnable locally with documented env vars. |
| STK-02-03 | Architects | Stack choices remain replaceable behind adapters. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-02-01 | The backend shall be implemented primarily with FastAPI and Python unless an approved alternative preserves the same architecture boundaries. |
| FR-02-02 | The backend shall use PostgreSQL as the primary durable control-plane database when DATABASE_URL is configured. |
| FR-02-03 | Where vector search is required, the backend shall support a pluggable vector provider (including optional pgvector). |
| FR-02-04 | Where asynchronous work is required, the backend shall support a worker or in-process execution path without mandating Docker for local product-bar operation. |
| FR-02-05 | The backend shall generate OpenAPI documentation from the FastAPI application. |
| FR-02-06 | The backend shall organize code into API, core, domain, and infrastructure layers as described in backend.md §9. |
| FR-02-07 | When infrastructure dependencies are optional (Redis, object storage, external LLM), the backend shall degrade or feature-flag rather than hard-fail unrelated core routes when those deps are absent in local mode. |
| FR-02-08 | The backend shall document required and optional environment variables including APP_ENV, DATABASE_URL, JWT secrets, CORS, and feature flags. |
| FR-02-09 | The backend shall keep JSON file snapshots as backup/seed only when Postgres is the primary store (not dual-write source of truth). |
| FR-02-10 | The backend shall expose a clear entrypoint (e.g. app.main:app) for uvicorn or equivalent ASGI server. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-02-01 | Cold start of the API process for local development shall complete within a developer-acceptable window (target under 30 seconds excluding dependency installs). |
| NFR-02-02 | Module import graph shall avoid circular dependencies between domain and infrastructure. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-02-03 | Secrets shall be loaded from environment or secret stores and shall not be hardcoded in source. |
| NFR-02-04 | CORS allowed origins shall be explicit configuration, not unrestricted wildcard in production profiles. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-02-01 | backend/ tree matches layered layout (api/core/domain/infrastructure). |
| AC-02-02 | OpenAPI schema is exportable from running app. |
| AC-02-03 | .env.example or docs list DATABASE_URL and JWT-related settings. |
| AC-02-04 | README documents local uvicorn start without Docker. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-01 | BE-03+ |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-02-01 | Import/smoke: app.main loads. | Automated |
| TV-02-02 | OpenAPI /docs or export path returns schema. | Automated |
| TV-02-03 | Review: no secrets committed in scaffold files. | Review |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §3 Stack | FR-02-01 … FR-02-05 |
| backend.md §9 Folder Structure | FR-02-06, FR-02-10 |
| backend.md §18.3 Environment Variables | FR-02-08 |
| backend.md §24.3 Control plane | FR-02-02, FR-02-09 |
