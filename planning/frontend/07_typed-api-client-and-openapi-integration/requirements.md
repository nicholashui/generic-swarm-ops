# 07 — Typed API Client and OpenAPI Integration

| Field | Value |
|-------|-------|
| Spec ID | `FE-07` |
| Source | `frontend.md` — §20 API Integration, §33.3a Backend API contracts, pnpm api:generate, DEMO_MODE ops profile |
| Related architecture | backend OpenAPI; planning/backend/ |
| Priority order | 07 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
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


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-07-01 | Frontend engineers | Type-safe API calls aligned with FastAPI schema. |
| STK-07-02 | Operators | Clear errors with request IDs for support. |
| STK-07-03 | Backend engineers | FE regenerates types rather than hand-forking contracts. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-07-01 | The frontend shall call the backend only through versioned HTTP APIs under `/api/v1` (or documented base path). |
| FR-07-02 | The frontend shall maintain a typed API client layer for domain resources (auth, users, agents, tools, workflows, runs, approvals, knowledge, memory, evaluations, processes, audit, evolution, improvement). |
| FR-07-03 | When OpenAPI schema is available, the frontend shall generate TypeScript types via `pnpm api:generate` (or documented equivalent). |
| FR-07-04 | When a backend error response includes `request_id`, the frontend shall display or log it for operator support. |
| FR-07-05 | If `NEXT_PUBLIC_DEMO_MODE=true`, the frontend may use demo fixtures; if `false`, the frontend shall use the live backend. |
| FR-07-06 | After backend OpenAPI changes, implementers shall regenerate the client types before claiming API compatibility. |
| FR-07-07 | The frontend shall not write to databases or internal services except via backend APIs. |
| FR-07-08 | API client shall attach authentication credentials per the auth session design. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-07-01 | API client shall support abort/cancel for in-flight requests on navigation where practical. |
| NFR-07-02 | List endpoints shall support pagination parameters when provided by backend. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-07-03 | API client shall not embed long-lived secrets in source. |
| NFR-07-04 | Cross-origin calls shall rely on documented CORS/credentials settings from backend. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-07-01 | Generated OpenAPI types exist and are imported by client modules. |
| AC-07-02 | Live mode login + at least one authenticated GET succeed against backend. |
| AC-07-03 | Error UI can show request_id from a forced 4xx/5xx. |
| AC-07-04 | README documents `pnpm api:generate`. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-02 | All data-fetching pages FE-08–FE-18 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-07-01 | Unit: error parser extracts request_id. | Unit |
| TV-07-02 | Integration: client hits backend health/me. | Integration |
| TV-07-03 | Contract: regenerate types after OpenAPI export. | Tooling |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §20 API Integration | FR-07-01 … FR-07-05, FR-07-08 |
| §33.3a Backend contracts | FR-07-02, FR-07-06 |
| §19 DEMO_MODE | FR-07-05 |


