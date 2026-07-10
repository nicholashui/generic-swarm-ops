# 03 — Persistence Control Plane

| Field | Value |
|-------|-------|
| Spec ID | `BE-03` |
| Source | `backend.md` — §10 Data Model (infra), §18 env DATABASE_URL, §24.3 Postgres runtime_state |
| Related architecture | structure.md §12.3 Control plane |
| Priority order | 03 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Durable persistence for runtime state (organizations, users, agents, workflows, runs, approvals, knowledge, memory, evaluations, audit, evolution variants as applicable).
- Postgres runtime_state JSONB primary model as as-built control plane.
- JSON backup/seed and migrate-from-JSON on empty DB behaviour.
- Core entity relationships from backend.md §10.

### 1.2 Out of scope
- Domain business rules for each entity (later BE specs).
- Full multi-region replication topology.
- Commercial Neo4j mesh as primary store.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-03-01 | Operators | State survives process restarts. |
| STK-03-02 | Engineers | Single primary store with clear backup path. |
| STK-03-03 | Auditors | Durable audit and run history. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-03-01 | When DATABASE_URL is set, the backend shall persist control-plane state primarily in PostgreSQL. |
| FR-03-02 | The backend shall store runtime control state in a durable schema including JSONB runtime_state (or equivalent) capable of holding versioned domain objects. |
| FR-03-03 | When the database is empty and a JSON seed/backup exists, the backend shall support migrate-from-JSON to initialize state. |
| FR-03-04 | While Postgres is primary, the backend shall treat JSON files as backup/seed only and not as the authoritative write path for live mutations. |
| FR-03-05 | The backend data model shall include core entities: Organization, User, Agent, Workflow, WorkflowVersion, WorkflowRun, WorkflowRunStep, ApprovalRequest, KnowledgeDocument, KnowledgeChunk, MemoryItem, EvaluationRun, AuditLog. |
| FR-03-06 | When multi-tenancy is not fully enabled, the backend shall still include organization_id or tenant_id on tenant-scoped entities. |
| FR-03-07 | When a write succeeds, subsequent reads from another request shall observe the committed state after transaction completion. |
| FR-03-08 | If the database is unavailable, then health/ready checks shall report degraded or not-ready status. |
| FR-03-09 | The backend shall support snapshot backup of runtime state for disaster recovery and local portability. |
| FR-03-10 | The backend shall isolate tenant data by organization_id on queries for multi-tenant-ready entities. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-03-01 | Primary key lookups for run/agent/workflow by ID shall complete within 100ms p95 under local load excluding network to remote DB. |
| NFR-03-02 | Migrations or schema bootstrap shall be documented and repeatable. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-03-03 | Database credentials shall not appear in logs. |
| NFR-03-04 | The backend shall use parameterized queries / ORM bindings to prevent SQL injection. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-03-01 | GET health/ready reports database postgres when DATABASE_URL configured. |
| AC-03-02 | Restarting API retains previously created agents/workflows/runs. |
| AC-03-03 | Empty DB can be seeded from JSON backup path when present. |
| AC-03-04 | Tenant-scoped entities include organization_id field. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-02 | BE-04–BE-22 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-03-01 | Unit/integration: create entity, restart store session, read back. | Automated |
| TV-03-02 | Ready endpoint with/without DB. | Automated |
| TV-03-03 | Seed/migrate-from-JSON path on empty DB. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §10 Data Model | FR-03-05 … FR-03-06 |
| backend.md §24.3 Control plane | FR-03-01 … FR-03-04 |
| backend.md §17.2 Health | FR-03-08 |
