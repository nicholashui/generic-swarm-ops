# 10 — Workflow Definition and Versioning

| Field | Value |
|-------|-------|
| Spec ID | `BE-10` |
| Source | `backend.md` — §7.6 Workflow Management, §10.5–10.6, §11.6 |
| Related architecture | structure.md §4.1 Workflow DNA |
| Priority order | 10 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Workflow definitions and versions.
- Metadata: risk, schemas, steps, governance/evaluation policy, status.
- Statuses draft/active/disabled/archived.
- Create/update/disable/list/get endpoints.
- Workflow DNA structural fields needed for execution and safety validation.

### 1.2 Out of scope
- Run execution (BE-11).
- Evolution mutation of DNA (BE-20).

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-10-01 | Business owners | Versioned process definitions. |
| STK-10-02 | Operators | Activate only validated workflows. |
| STK-10-03 | Auditors | Historical version used by each run is known. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-10-01 | The backend shall support workflow definitions representing structured multi-step business processes. |
| FR-10-02 | When a workflow is created, the backend shall store workflow ID, name, description, version lineage, owner, department, risk level, input schema, output schema, steps, governance policy references, evaluation policy references, and status. |
| FR-10-03 | The backend shall support workflow statuses draft, active, disabled, and archived. |
| FR-10-04 | The backend shall support workflow versioning such that runs reference a specific workflow version. |
| FR-10-05 | When a workflow version is updated, historical runs shall continue to reference the version they executed. |
| FR-10-06 | The backend shall expose list/create/get/update/disable (and version activate) endpoints for workflows. |
| FR-10-07 | Workflow steps may include agents, tools, conditions, approvals, memory retrieval, knowledge search, evaluation, and outputs as defined in execution design. |
| FR-10-08 | If a workflow is disabled or archived, then the backend shall reject new run starts for that workflow. |
| FR-10-09 | When a workflow definition includes DNA-like structure, the backend shall persist guardrails, verification, rollback, and memory read/write declarations when provided. |
| FR-10-10 | The backend shall validate workflow payloads against schema before accepting create/update. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-10-01 | Workflow get by id p95 under 100ms local. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-10-02 | Only authorized roles may create, update, or activate workflows. |
| NFR-10-03 | Workflow definitions shall not embed raw secrets. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-10-01 | Create workflow version and retrieve it. |
| AC-10-02 | Run references workflow version id. |
| AC-10-03 | Disabled workflow cannot start runs. |
| AC-10-04 | Invalid schema rejected on create. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-06–BE-09 | BE-11, BE-22 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-10-01 | CRUD + version tests. | Automated |
| TV-10-02 | Negative: start disabled workflow. | Automated |
| TV-10-03 | Flagship workflow seed available. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.6 Workflow Management | FR-10-01 … FR-10-08 |
| backend.md §10.5–10.6 | FR-10-02 … FR-10-05 |
| backend.md §11.6 | FR-10-06 |
