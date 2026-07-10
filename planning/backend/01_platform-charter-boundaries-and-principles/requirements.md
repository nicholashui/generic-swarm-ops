# 01 — Platform Charter, Boundaries, and Design Principles

| Field | Value |
|-------|-------|
| Spec ID | `BE-01` |
| Source | `backend.md` — §1 Purpose, §2 Primary Objective, §4 System Boundary, §5 High-Level Architecture, §6 Core Design Principles |
| Related architecture | structure.md design priorities; backend.md §24.1 |
| Priority order | 01 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Backend mission as governed API control plane for structure.md capabilities.
- System boundary: what backend owns vs frontend, agents, external systems.
- Core design principles: API first, secure by default, governance first, human-in-the-loop, audit everything important, workers for long-running work, frontend simplicity.
- Design priority order inherited from structure.md: Safety → Auditability → Correctness → Efficiency → Autonomy.

### 1.2 Out of scope
- Concrete route handlers and schemas (later BE specs).
- Frontend UX layout (frontend.md).
- Domain business corpus content under business/.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-01-01 | Product / architecture | Backend enforces architecture priorities and never becomes a thin ungoverned proxy. |
| STK-01-02 | Security / compliance | All agent, workflow, knowledge, and tool access is mediated and auditable. |
| STK-01-03 | Frontend consumers | A stable API control plane with no need to reach databases or LLM providers directly. |
| STK-01-04 | Operators | Backend remains source of truth for permissions, policy, and execution state. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-01-01 | The backend shall act as the governed control layer for the business operating system described in structure.md. |
| FR-01-02 | The backend shall expose system capabilities through versioned APIs for frontend, CLI, automation, and integrations. |
| FR-01-03 | If a client attempts to access agents, databases, workflow engines, LLM providers, vector stores, or internal tools without the backend, then the system shall treat that path as unsupported and out of scope. |
| FR-01-04 | The backend shall enforce permissions, policy, workflow rules, risk controls, auditability, data access boundaries, and evaluation checks rather than blindly proxying to agents. |
| FR-01-05 | When a design trade-off exists between safety and autonomy, the backend shall prefer the safer option. |
| FR-01-06 | When a design trade-off exists between auditability and efficiency, the backend shall prefer auditability. |
| FR-01-07 | When a design trade-off exists between correctness and efficiency, the backend shall prefer correctness. |
| FR-01-08 | The backend shall be API-first so that frontend depends only on the backend API contract. |
| FR-01-09 | When an endpoint is not explicitly public, the backend shall require authentication. |
| FR-01-10 | When a high-risk or irreversible action is requested, the backend shall apply governance and human-in-the-loop rules before completion. |
| FR-01-11 | When an important state-changing action occurs, the backend shall write an audit event. |
| FR-01-12 | When work is long-running, the backend shall support asynchronous execution patterns (queue/worker or equivalent) rather than blocking the API forever. |
| FR-01-13 | The backend shall keep business intelligence, control, security, and trust enforcement on the server so the frontend remains a presentation and interaction layer. |
| FR-01-14 | The backend shall support authentication, RBAC, agent orchestration requests, workflow execution, run tracking, governance gates, memory and knowledge retrieval, audit logging, evaluation, process intelligence, evolution sandbox controls, self-improvement loops, streaming updates, and extensible integrations as capability domains. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-01-01 | Charter and principle checks shall be enforceable by deterministic policy and code review gates without requiring online LLM calls. |
| NFR-01-02 | API contract changes that break frontend consumers shall require explicit versioning decisions. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-01-03 | The backend shall treat design principles as non-bypassable by prompt text alone. |
| NFR-01-04 | If a feature would allow unattended direct production DNA mutation, then the backend shall reject that feature as out of charter. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-01-01 | backend.md and this spec state backend is the sole control plane for agents/workflows/tools access. |
| AC-01-02 | All downstream planning/backend/* specs reference BE-01 priority order. |
| AC-01-03 | System boundary lists owned capabilities and forbidden thin-proxy behaviour. |
| AC-01-04 | Evolution and DNA safety specs explicitly forbid host self-rewrite and silent production DNA mutation. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| None (root) | All BE-02–BE-24 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-01-01 | Document review: map each principle in §6 to at least one later BE FR. | Review |
| TV-01-02 | Negative: specify auto-promote-to-production without gates → reject against charter. | Spec gate |
| TV-01-03 | Traceability matrix BE-01 FR IDs → later BE FR IDs. | Traceability |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §1–2 Purpose/Objective | FR-01-01 … FR-01-02, FR-01-14 |
| backend.md §4 System Boundary | FR-01-03 … FR-01-04 |
| backend.md §6 Core Design Principles | FR-01-08 … FR-01-13 |
| structure.md design priorities | FR-01-05 … FR-01-07 |
