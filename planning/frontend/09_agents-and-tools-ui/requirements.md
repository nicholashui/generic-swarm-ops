# 09 — Agents and Tools UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-09` |
| Source | `frontend.md` — §16.5–16.9 Agents/Tools pages, Phase 7 Agents and Tools |
| Related architecture | backend BE-08, BE-09 |
| Priority order | 09 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Agents list, create agent, agent detail pages.
- Tools list and tool detail pages.
- Forms with frontend validation (Zod/react-hook-form or equivalent) posting to backend.
- Display of agent/tool metadata, status, and backend errors.

### 1.2 Out of scope
- Agent/tool execution engines (backend).
- Tool adapter implementation.

### 1.3 System under specification
Agents and tools management UI.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-09-01 | Developers / operators | Register and inspect agents and tools. |
| STK-09-02 | Reviewers | Read-only visibility when permitted. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
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


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-09-01 | List views shall support pagination or virtualization when lists grow large. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-09-02 | Tool configuration UI shall not accept or display raw provider secrets beyond backend-safe metadata. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-09-01 | Create agent form works against live backend in ops profile. |
| AC-09-02 | Agents and tools lists render API data. |
| AC-09-03 | Permission-denied create is gated in UI. |
| AC-09-04 | Status badges and empty/error states present on list views. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-04, FE-06, FE-07 | Workflow assignment UIs |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-09-01 | Unit: form schema rejects empty name. | Unit |
| TV-09-02 | Integration/manual: create agent → appears in list. | Integration |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.5–16.9 Agents/Tools | FR-09-01 … FR-09-05 |
| §4.2 / §6.2 no execution | FR-09-07 |
| Phase 7 | AC-09-* |


