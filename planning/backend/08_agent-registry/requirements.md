# 08 — Agent Registry

| Field | Value |
|-------|-------|
| Spec ID | `BE-08` |
| Source | `backend.md` — §7.4 Agent Registry, §10.4, §11.5, §15 Agent Runtime Design |
| Related architecture | structure.md §9 agent roster (API registry portion) |
| Priority order | 08 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Agent registry CRUD and metadata fields from backend.md §7.4 / §10.4.
- Agent statuses: draft, active, disabled, archived.
- Allowed tools, memory scopes, workflow types, risk level, input/output schema.
- Agent activity and tools listing endpoints.
- Agent execution contracts (input/output) at API/runtime boundary §15.

### 1.2 Out of scope
- Autonomous free-form swarm outside workflow engine.
- Frontend agent builder UX details.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-08-01 | Operators | See which agents exist and their constraints. |
| STK-08-02 | Governance | Agents carry risk and tool allow-lists. |
| STK-08-03 | Engineers | Stable agent IDs for workflow DNA references. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-08-01 | The backend shall maintain a registry of available agents. |
| FR-08-02 | When an agent is created or updated, the backend shall persist agent ID, name, description, version, owner, department, allowed tools, allowed memory scopes, allowed workflow types, risk level, input schema, output schema, runtime configuration, and status. |
| FR-08-03 | The backend shall support agent statuses draft, active, disabled, and archived. |
| FR-08-04 | When listing agents, the backend shall return only agents visible to the caller's organization and permissions. |
| FR-08-05 | When an agent is disabled or archived, the backend shall prevent new workflow steps from starting that agent unless an explicit override policy exists. |
| FR-08-06 | The backend shall expose endpoints to list, create, get, update, and delete/archive agents. |
| FR-08-07 | The backend shall expose agent activity and agent tools inspection endpoints as specified in the API design. |
| FR-08-08 | When an agent executes inside a workflow, the backend shall supply an input contract and accept an output contract conforming to §15 designs. |
| FR-08-09 | If an agent references a tool not in its allowed tools, then the backend shall deny tool use for that agent. |
| FR-08-10 | Agent definitions used in production workflows shall be versionable or otherwise immutable for historical runs. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-08-01 | Agent list for typical catalogs (<500) shall return within 300ms p95 local. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-08-02 | Only authorized roles may create or update agents. |
| NFR-08-03 | Agent runtime configuration shall not embed plaintext provider secrets; secrets shall be referenced securely. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-08-01 | Create agent then get by id succeeds. |
| AC-08-02 | Disabled agent cannot be newly executed in runs. |
| AC-08-03 | Allowed tools list is returned on get. |
| AC-08-04 | Unauthorized create returns 403. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-06, BE-07 | BE-09, BE-11 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-08-01 | CRUD unit/integration tests for agents. | Automated |
| TV-08-02 | Negative: tool outside allow-list. | Automated |
| TV-08-03 | Flagship agents seed present for E1. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.4 Agent Registry | FR-08-01 … FR-08-07 |
| backend.md §15 Agent Runtime | FR-08-08 … FR-08-10 |
| backend.md §11.5 | FR-08-06 … FR-08-07 |
