# 01 — Frontend Charter, Scope, and Design Principles

| Field | Value |
|-------|-------|
| Spec ID | `FE-01` |
| Source | `frontend.md` — §1 Purpose, §2 Product Vision, §3 Core Design Principle, §4 Scope, §6 Runtime Responsibilities, §32 Final Frontend Rule, §33 Implementation Mapping |
| Related architecture | structure.md §10–12; backend.md control-plane boundary |
| Priority order | 01 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Frontend mission as the professional ops console for the Generic Swarm Business Operating System.
- Product vision: enterprise SaaS feel (trust, reliability, operational clarity, security, professionalism, speed, control, observability).
- System boundary: presentation, interaction, routing, layout, UI state, client validation, UX, client realtime display, design-system implementation.
- Explicit non-ownership of backend business logic, execution, secret storage, audit writes, silent production DNA mutation, host self-rewrite UI.
- Design priority inheritance: backend remains source of truth for authz, execution, and governance; OpenDesign-first major layouts.
- As-built relationship to `structure.md` §11.1/§12 and `planning/backend/` (FE never re-implements policy).

### 1.2 Out of scope
- Concrete page layouts and component APIs (later FE specs).
- Backend route implementation (planning/backend/*).
- Domain business corpus under `business/`.

### 1.3 System under specification
Generic Swarm Ops **frontend ops console** (`frontend/`), as specified in `frontend.md` and constrained by `structure.md` / `backend.md`.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-01-01 | Product / architecture | Console realizes structure.md human-centered ops path without becoming a second control plane. |
| STK-01-02 | Operators | Always understand agents, workflows, runs, failures, approvals, knowledge, data use, actions, and attention items. |
| STK-01-03 | Security / compliance | UI never treats hidden buttons as security; backend remains final authority. |
| STK-01-04 | Frontend engineers | Clear charter for what FE may and must not implement. |
| STK-01-05 | Backend consumers | Stable presentation layer that only mutates via versioned `/api/v1/*`. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-01-01 | The frontend shall deliver the user-facing web application for managing AI agents, workflows, tools, approvals, knowledge, memory, evaluations, audits, evolution sandbox variants, self-improvement actions, and organization settings. |
| FR-01-02 | The frontend shall communicate trust, reliability, operational clarity, security, professionalism, speed, control, and observability in its product presentation. |
| FR-01-03 | The frontend shall own presentation, interaction, routing, layout, UI state, frontend validation, UX, client-side realtime display, and design-system implementation. |
| FR-01-04 | If a capability requires workflow execution, agent execution, tool execution, permission enforcement as sole authority, direct database writes, background jobs, embedding/indexing, secret storage, provider API key handling in browser code, audit log creation, billing calculation, silent production DNA mutation, or host self-rewrite, then the frontend shall not implement that capability. |
| FR-01-05 | When the user requests an action, the frontend shall request it from the backend; the backend shall decide whether the action is allowed. |
| FR-01-06 | The frontend shall not assume that hiding a control is sufficient security. |
| FR-01-07 | When designing major page layouts, the frontend workflow shall prefer OpenDesign MCP references over generic AI memory alone. |
| FR-01-08 | The frontend shall treat `structure.md` as architecture source of truth and `backend.md` / planning/backend as the API control-plane contract. |
| FR-01-09 | When a design trade-off exists between operator clarity and decorative complexity, the frontend shall prefer operational clarity. |
| FR-01-10 | The frontend shall support both an ops profile (`NEXT_PUBLIC_DEMO_MODE=false` against live backend) and a demo profile for UI-only preview without treating demo as production authority. |
| FR-01-11 | The frontend shall remain a presentation and interaction layer so that authorization, execution, and governance stay on the backend. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-01-01 | Charter and boundary checks shall be enforceable by code review and architecture review without requiring online LLM calls. |
| NFR-01-02 | Frontend package boundaries shall keep domain pages free of backend business rules duplicated from Python services. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-01-03 | If a proposed UI feature would allow unattended direct production DNA mutation or host application self-rewrite, then the frontend shall reject that feature as out of charter. |
| NFR-01-04 | The frontend shall never store provider secrets or perform final authentication verification as sole authority. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-01-01 | frontend.md and this spec state frontend is presentation/interaction only; backend is control plane. |
| AC-01-02 | Out-of-scope list matches frontend.md §4.2 and §33.5 non-goals. |
| AC-01-03 | All downstream planning/frontend/* specs reference FE-01 priority order. |
| AC-01-04 | Evolution and improve specs explicitly require sandbox-only backend APIs. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| None (root) | All FE-02–FE-20 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-01-01 | Document review: map each §4.1 in-scope item to at least one later FE FR. | Review |
| TV-01-02 | Negative: client-side production DNA rewrite UI → reject against charter. | Spec gate |
| TV-01-03 | Traceability matrix FE-01 FR IDs → later FE FR IDs. | Traceability |


---

## 8. Traceability

| frontend.md / structure.md | This spec |
|---|---|
| frontend.md §1–2 Purpose/Vision | FR-01-01 … FR-01-02 |
| frontend.md §4 Scope | FR-01-03 … FR-01-04 |
| frontend.md §6 Runtime Responsibilities | FR-01-05 … FR-01-06 |
| frontend.md §3 OpenDesign principle | FR-01-07 |
| frontend.md §32–33 Final rule / mapping | FR-01-08 … FR-01-11 |


