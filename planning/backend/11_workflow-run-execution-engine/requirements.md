# 11 — Workflow Run Execution Engine

| Field | Value |
|-------|-------|
| Spec ID | `BE-11` |
| Source | `backend.md` — §7.7–7.8 Runs/Steps, §11.7, §12 Workflow Execution Design, idempotency |
| Related architecture | structure.md §4.2 bounded execution; §2 Intake pre-check |
| Priority order | 11 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Workflow run lifecycle: queued, running, waiting_for_approval, paused, completed, failed, cancelled, expired.
- Step tracking and step types.
- Start flow: auth, permission, load, validate, governance pre-check, create run, audit, execute, return id.
- Worker execution loop, cancellation, retry, idempotency key.
- Streaming hooks (events produced for BE-19).

### 1.2 Out of scope
- Approval decision UX (BE-13 owns decision APIs).
- Evolution of DNA (BE-20).

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-11-01 | Operators | Start, observe, cancel, retry runs. |
| STK-11-02 | Frontend | Stable run/step APIs and status model. |
| STK-11-03 | Risk | No irreversible tools before gates. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-11-01 | When a workflow is started, the backend shall create a workflow_run record. |
| FR-11-02 | The backend shall support run statuses queued, running, waiting_for_approval, paused, completed, failed, cancelled, and expired. |
| FR-11-03 | Each workflow run shall store run ID, workflow ID, workflow version, requester, organization ID, input, status, current step, output, error, timestamps, usage metrics, approval state, and evaluation results as available. |
| FR-11-04 | The backend shall create step records for run steps with statuses pending, running, waiting_for_approval, completed, failed, skipped, and cancelled. |
| FR-11-05 | Each step shall store step identity, run ID, name, type, agent/tool IDs if applicable, input/output/error, timestamps, duration, and retry_count. |
| FR-11-06 | When starting a run, the backend shall authenticate, authorize workflows:run, load workflow, validate input schema, run governance pre-check, create queued run, write audit log, and return workflow_run_id. |
| FR-11-07 | While a run is executing, the backend shall iterate steps checking cancellation, permissions, governance, approvals, then execute agent/tool/evaluation/condition as applicable, persist outputs, emit events, and audit. |
| FR-11-08 | The backend shall support step types agent, tool, approval, condition, knowledge_search, memory_search, evaluation, transform, notification, and human_input (as implemented subset at minimum covering flagship DNA). |
| FR-11-09 | When an Idempotency-Key is supplied for the same user and workflow start, the backend shall return the existing run instead of creating a duplicate. |
| FR-11-10 | The backend shall support cancel and retry operations according to policy. |
| FR-11-11 | If governance requires approval mid-run, then the backend shall transition the run to waiting_for_approval and pause irreversible progress. |
| FR-11-12 | When a run completes or fails, the backend shall persist terminal status, final output or error, and emit final events. |
| FR-11-13 | The backend shall expose list/get run, get steps, start, cancel, retry, and stream endpoints. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-11-01 | Start-run API shall return run id quickly (target p95 under 1s local) even if execution continues asynchronously. |
| NFR-11-02 | Step state transitions shall be persisted before emitting completion events. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-11-03 | Run inputs/outputs shall be access-controlled by organization and permissions. |
| NFR-11-04 | While run is unclassified or pre-check failed, the backend shall not execute irreversible tool actions. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-11-01 | Start flagship workflow creates run with version pin. |
| AC-11-02 | Steps appear with status transitions. |
| AC-11-03 | Duplicate Idempotency-Key returns same run id. |
| AC-11-04 | Cancel transitions run to cancelled when allowed. |
| AC-11-05 | Gate wait sets waiting_for_approval. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-10, BE-12, BE-13 | BE-14, BE-17, BE-19–BE-21 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-11-01 | Integration: start → running → complete happy path. | Automated |
| TV-11-02 | Idempotency key test. | Automated |
| TV-11-03 | E1 path segment: run + gate wait. | E2E |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.7–7.8 | FR-11-01 … FR-11-05 |
| backend.md §12 Execution Design | FR-11-06 … FR-11-12 |
| backend.md §11.7 | FR-11-13 |
