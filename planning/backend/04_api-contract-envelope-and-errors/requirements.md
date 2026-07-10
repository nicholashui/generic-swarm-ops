# 04 — API Contract, Envelope, and Errors

| Field | Value |
|-------|-------|
| Spec ID | `BE-04` |
| Source | `backend.md` — §6.1 API First, §11.1–11.3 Versioning / Response Format / Error Codes |
| Related architecture | structure.md operator API surface |
| Priority order | 04 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- API versioning under /api/v1.
- Standard success and error response envelopes.
- Common error codes and request_id correlation.
- Consistent pagination/meta patterns where applicable.

### 1.2 Out of scope
- Domain endpoint semantics (later specs).
- GraphQL alternative API.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-04-01 | Frontend engineers | Predictable envelopes and typed OpenAPI. |
| STK-04-02 | Support | request_id on errors for triage. |
| STK-04-03 | API consumers | Stable versioning strategy. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-04-01 | The backend shall version public HTTP APIs under a versioned prefix such as /api/v1. |
| FR-04-02 | When a successful response is returned for resource APIs, the backend shall use a consistent envelope including data and meta where specified in backend.md §11.2. |
| FR-04-03 | When an error occurs, the backend shall return a structured error envelope including error code, message, and request_id. |
| FR-04-04 | The backend shall assign a request_id to each handled request and propagate it to logs and error responses. |
| FR-04-05 | The backend shall document common error codes including authentication, authorization, validation, not found, conflict, rate limit, and internal errors. |
| FR-04-06 | When request body validation fails, the backend shall return a 422-class validation error with field-level detail where available. |
| FR-04-07 | When an unhandled exception occurs, the backend shall return a safe error envelope without leaking secrets or stack traces to clients in production profiles. |
| FR-04-08 | The backend shall publish OpenAPI that matches implemented routes and schemas. |
| FR-04-09 | When listing resources, the backend shall support consistent pagination parameters or documented defaults. |
| FR-04-10 | Breaking public contract changes shall require a new API version or explicit deprecation notice. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-04-01 | Envelope serialization overhead shall be negligible relative to handler work. |
| NFR-04-02 | OpenAPI generation shall complete as part of normal app startup or export command. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-04-03 | Error messages shall not include secrets, raw tokens, or password hashes. |
| NFR-04-04 | request_id alone shall not authorize access to resources. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-04-01 | Sample error responses include request_id. |
| AC-04-02 | OpenAPI lists /api/v1 routes. |
| AC-04-03 | Invalid body yields validation error envelope. |
| AC-04-04 | Production error path does not return stack traces. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-02, BE-03 | All route specs BE-05+ |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-04-01 | Unit: error handler formats envelope. | Automated |
| TV-04-02 | Contract: OpenAPI export includes version prefix. | Automated |
| TV-04-03 | Negative: 401/403/422 sample routes. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §6.1 API First | FR-04-01, FR-04-08 |
| backend.md §11.1–11.3 | FR-04-01 … FR-04-07 |
