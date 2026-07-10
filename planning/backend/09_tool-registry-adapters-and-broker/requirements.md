# 09 — Tool Registry, Adapters, and Broker

| Field | Value |
|-------|-------|
| Spec ID | `BE-09` |
| Source | `backend.md` — §7.5 Tool Registry, tool_effects as-built, tool permission broker |
| Related architecture | structure.md §7 tool broker; §12.3 adapters |
| Priority order | 09 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Tool registry metadata: schemas, risk, permissions, approval requirement, timeout, retry, enabled status.
- Tool categories (database, email, calendar, crm, file, web, internal_api, external_api, llm, code_execution, human_approval).
- Local tool adapters and durable tool_effects.
- Tool permission broker: allow-list ∩ DNA tools ∩ RBAC ∩ gates.

### 1.2 Out of scope
- Live external CRM/email/billing SaaS adapters (non-goal for mark ~100).
- Ephemeral OAuth per-tool broker (deferred).

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-09-01 | Security | Least-privilege tool access. |
| STK-09-02 | Operators | Understand tool risk and approval needs. |
| STK-09-03 | Engineers | Adapters produce durable side-effect records. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-09-01 | The backend shall maintain a registry of tools usable by agents only through backend-controlled permissions. |
| FR-09-02 | When a tool is registered, the backend shall store tool ID, name, description, category, input schema, output schema, risk level, required permissions, approval requirement, timeout, retry policy, and enabled/disabled status. |
| FR-09-03 | The backend shall support tool categories including database, email, calendar, crm, file, web, internal_api, external_api, llm, code_execution, and human_approval. |
| FR-09-04 | When a high-risk tool is invoked, the backend shall require explicit governance rules and/or approval as configured. |
| FR-09-05 | The backend shall execute tools via adapters and record durable tool_effects for side effects. |
| FR-09-06 | When authorizing a tool call, the backend shall intersect agent allow-list, workflow DNA tools, RBAC permissions, and gate requirements. |
| FR-09-07 | If a tool is disabled, then the backend shall reject new invocations of that tool. |
| FR-09-08 | The backend shall expose tool list/detail endpoints required by the ops console. |
| FR-09-09 | While live SaaS adapters are deferred, local adapters shall still exercise realistic side-effect paths for CRM/billing/email/audit/contract_parser/policy_retriever as implemented. |
| FR-09-10 | The backend shall not grant tools ambient credentials broader than the task scope (broker principle). |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-09-01 | Local adapter calls shall honor configured timeouts. |
| NFR-09-02 | tool_effects writes shall be durable before acknowledging tool success for mutating tools. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-09-03 | Tool credentials and secrets shall not be returned to clients. |
| NFR-09-04 | Tool outputs shall be treated as untrusted input to subsequent LLM prompts. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-09-01 | Tool registry lists expected local tools. |
| AC-09-02 | Mutating adapter writes tool_effects entry. |
| AC-09-03 | Invocation denied when tool not in DNA allow-list. |
| AC-09-04 | High-risk tool path can require approval. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-06, BE-08 | BE-11, BE-12 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-09-01 | Unit: broker intersection logic. | Automated |
| TV-09-02 | Integration: adapter + tool_effects persistence. | Automated |
| TV-09-03 | Negative: disabled tool invoke. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.5 Tool Registry | FR-09-01 … FR-09-04, FR-09-07 |
| backend.md §24.3 Tool adapters/broker | FR-09-05 … FR-09-06, FR-09-09 |
| backend.md §16 Security tools | FR-09-10, NFR-09-03 |
