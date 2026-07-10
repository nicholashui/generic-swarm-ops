# 11 — Workflow Run Realtime UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-11` |
| Source | `frontend.md` — §16.13 Workflow Run Detail, §21 Real-Time Updates, Phase 9, run pause/resume/expire §33.3a |
| Related architecture | backend BE-11, BE-19 streaming |
| Priority order | 11 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
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


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-11-01 | Operators | Watch runs progress and intervene (cancel/pause) when allowed. |
| STK-11-02 | Support | See step failures with correlation IDs. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
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


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-11-01 | Realtime handlers shall avoid unbounded memory growth on long-running streams. |
| NFR-11-02 | Timeline rendering shall remain usable for typical step counts of MVP workflows. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-11-03 | Stream subscriptions shall require authenticated session. |
| NFR-11-04 | Run actions shall send only backend-defined payloads. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-11-01 | Run detail shows steps for a live run. |
| AC-11-02 | Status updates reflect backend changes (stream or poll). |
| AC-11-03 | Pause/resume/expire controls call documented APIs when enabled. |
| AC-11-04 | Cancel/retry respect permission UX. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-07, FE-10 | FE-12, FE-18 Improve |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-11-01 | Manual: start run → observe status transitions. | Manual |
| TV-11-02 | Unit: status badge mapping for paused. | Unit |
| TV-11-03 | Integration: lifecycle POST paths. | Integration |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.13 Run detail | FR-11-01 … FR-11-02, FR-11-05 … FR-11-07 |
| §21 Realtime | FR-11-03 … FR-11-04 |
| §33.3a Run lifecycle | FR-11-06 |
| Phase 9 | AC-11-* |


