# 19 — Streaming, Health, and Observability

| Field | Value |
|-------|-------|
| Spec ID | `BE-19` |
| Source | `backend.md` — §7.18 Streaming, §8.4 Observability, §17 Health/Metrics/Logs |
| Related architecture | structure.md observability / operator proof |
| Priority order | 19 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- SSE streaming for run events and event types from §7.18.
- Health, liveness, readiness, metrics endpoints.
- Structured logs, request metrics, security headers, CORS.

### 1.2 Out of scope
- Full OpenTelemetry vendor lock.
- Bidirectional WebSocket agent chat product (optional later).

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-19-01 | Frontend | Live run progress. |
| STK-19-02 | Ops | Ready/live probes. |
| STK-19-03 | Support | Correlated logs via request_id. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-19-01 | The backend shall support real-time progress updates for workflow runs via Server-Sent Events (WebSocket optional later). |
| FR-19-02 | Streaming shall emit events including run.started, run.status_changed, step.started/completed/failed, approval.requested/approved/rejected, evaluation.completed, run.completed/failed, and log.message as applicable. |
| FR-19-03 | Each stream event shall include workflow_run_id, timestamps, and payload fields needed by clients. |
| FR-19-04 | The backend shall expose health, liveness, and readiness endpoints. |
| FR-19-05 | Readiness shall report database connectivity status (e.g. postgres) when configured. |
| FR-19-06 | The backend shall emit structured API request logs including request_id. |
| FR-19-07 | The backend shall expose basic metrics suitable for operational monitoring. |
| FR-19-08 | The backend shall apply basic security headers and configured CORS policy. |
| FR-19-09 | If a client is not authorized for a run, then the backend shall not stream that run's events. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-19-01 | SSE shall deliver step completion events promptly after persistence (target under 1s local). |
| NFR-19-02 | Health endpoints shall respond under 100ms when process is healthy. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-19-03 | Stream endpoints shall require authentication and authorization. |
| NFR-19-04 | Logs shall redact secrets and tokens. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-19-01 | Stream endpoint exists for workflow runs. |
| AC-19-02 | Ready reports database status. |
| AC-19-03 | Logs include request_id for sample requests. |
| AC-19-04 | Unauthorized stream denied. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-04, BE-11 | FE realtime, ops readiness |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-19-01 | Health/live/ready tests. | Automated |
| TV-19-02 | SSE or event emission unit tests. | Automated |
| TV-19-03 | Auth on stream. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.18 Streaming | FR-19-01 … FR-19-03 |
| backend.md §17 Observability | FR-19-04 … FR-19-07 |
| backend.md §8.4 | FR-19-06 … FR-19-08 |
