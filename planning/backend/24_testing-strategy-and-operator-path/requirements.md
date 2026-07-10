# 24 — Testing Strategy and Operator Path

| Field | Value |
|-------|-------|
| Spec ID | `BE-24` |
| Source | `backend.md` — §19 Testing Strategy, §21 MVP, §22 Definition of Done, §24 E1/non-goals |
| Related architecture | structure.md §11.1 / §12.4–12.5, E1 path |
| Priority order | 24 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Testing strategy: unit, integration, e2e, security, load (as applicable).
- MVP minimum backend capabilities.
- Definition of Done including product bar mark ~100 additions.
- E1 operator path proof.
- Explicit non-goals list alignment with structure.md §12.4.

### 1.2 Out of scope
- Always-on multi-worker Temporal cluster as hard requirement.
- Infinite business leaf content.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-24-01 | Release managers | Clear DoD and evidence. |
| STK-24-02 | QA | Layered test protocols. |
| STK-24-03 | Product | Non-goals do not block mark ~100. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-24-01 | The backend shall maintain unit tests for permission logic, governance evaluation, workflow state transitions, schema validation, memory rules, knowledge filtering, evaluation rules, and audit event creation. |
| FR-24-02 | The backend shall maintain integration tests for API routes with database, workflow execution, approvals, knowledge/memory, workers, and audit creation. |
| FR-24-03 | The backend shall maintain end-to-end tests for login → start workflow → approval → completion → evaluation/audit paths. |
| FR-24-04 | The backend shall maintain security tests for unauthorized access, cross-org access, role failures, invalid/expired tokens, restricted memory/knowledge, and tool permission failures. |
| FR-24-05 | The MVP backend shall include authentication, users/orgs/RBAC, audit logs, agent registry, workflow definitions/runs, worker/execution, basic governance, approvals, run status/steps, basic knowledge, and OpenAPI. |
| FR-24-06 | For product bar mark ~100, the backend shall additionally provide Postgres primary persistence, local tool adapters with tool_effects, evolution sandbox APIs, self-improvement APIs, production DNA validation, and a passing E1 operator path test. |
| FR-24-07 | The E1 path shall cover login → create/use agent → flagship run → human gate → complete → reflect → propose → evaluate → canary (as implemented in test_e1_operator_path). |
| FR-24-08 | The following shall be treated as non-goals for mark ~100: full commercial LightRAG/Neo4j mesh, live external CRM/email/billing SaaS adapters, DGM host self-rewrite, always-on multi-worker cluster requirement, ephemeral per-tool OAuth broker, infinite business leaf fill. |
| FR-24-09 | Test evidence and status shall be linkable from status.md / mark verification docs. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-24-01 | Unit suite shall be runnable in local dev without external paid APIs. |
| NFR-24-02 | E2E E1 shall complete within CI-reasonable time on local stack. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-24-03 | Security tests shall not require disabling auth globally. |
| NFR-24-04 | Test fixtures shall not embed real production secrets. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-24-01 | Unit discover suite green. |
| AC-24-02 | E2E E1 path green. |
| AC-24-03 | DoD checklist items 1–26 from backend.md §22 (including product bar additions) are evidenced. |
| AC-24-04 | Non-goals documented and not filed as product-bar defects. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| All prior BE specs | Release gate / product bar |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-24-01 | python -m unittest discover unit. | Automated |
| TV-24-02 | python -m unittest discover e2e. | Automated |
| TV-24-03 | Review: map DoD to tests/docs. | Review |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §19 Testing | FR-24-01 … FR-24-04 |
| backend.md §21–22 MVP/DoD | FR-24-05 … FR-24-06 |
| backend.md §24 Implementation Mapping | FR-24-07 … FR-24-09 |
