# 16 — Memory System

| Field | Value |
|-------|-------|
| Spec ID | `BE-16` |
| Source | `backend.md` — §7.11, §11.10, §14.3 Memory Rules |
| Related architecture | structure.md §3.3 hybrid memory |
| Priority order | 16 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Memory types/scopes: short_term, long_term, user/team/department/organization/workflow/agent memory.
- Memory CRUD/search with ACL and sensitivity.
- Expiration and embedding references.
- Department isolation rules.

### 1.2 Out of scope
- Unbounded personalization product.
- Cross-tenant memory sharing.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-16-01 | Agents | Read/write allowed scopes only. |
| STK-16-02 | Security | Restricted department memory isolation. |
| STK-16-03 | Operators | Inspect memory records in ops console. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-16-01 | The backend shall manage agent and workflow memory with access control. |
| FR-16-02 | The backend shall support memory scopes including short_term, long_term, user_memory, team_memory, department_memory, organization_memory, workflow_memory, and agent_memory. |
| FR-16-03 | Each memory entry shall store memory ID, scope, owner, organization ID, department, content, metadata, embedding reference, sensitivity, expiration, and created_at. |
| FR-16-04 | When an agent requests memory outside its allowed scopes or department policy, the backend shall deny access. |
| FR-16-05 | The backend shall expose list/create/get/update/delete/search memory endpoints. |
| FR-16-06 | If memory sensitivity is restricted and agent department mismatches, then the backend shall deny access (policy example in backend.md). |
| FR-16-07 | When memory is accessed or updated, the backend shall write audit events for sensitive operations. |
| FR-16-08 | Expired memory shall not be returned as active context after expiration processing. |
| FR-16-09 | Memory writes from untrusted sources shall be filterable/reviewable for high-impact scopes where policy requires. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-16-01 | Memory search within a scope p95 under 500ms local for small sets. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-16-02 | memory:read/write permissions shall be enforced. |
| NFR-16-03 | Memory content of other organizations shall never be returned. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-16-01 | Create memory and get by id. |
| AC-16-02 | Cross-department restricted deny path works. |
| AC-16-03 | Agent allowed scopes respected during run memory_reads. |
| AC-16-04 | Unauthorized memory:write denied. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-06, BE-03 | BE-08, BE-11 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-16-01 | Unit: scope policy matrix. | Automated |
| TV-16-02 | Integration: CRUD + search. | Automated |
| TV-16-03 | Flagship memory_reads do not fail mid-run for configured scopes. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.11 Memory | FR-16-01 … FR-16-05 |
| backend.md §14.3 Memory Rules | FR-16-04, FR-16-06 |
| backend.md §11.10 | FR-16-05 |
