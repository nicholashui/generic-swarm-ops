# 22 — Production DNA Safety

| Field | Value |
|-------|-------|
| Spec ID | `BE-22` |
| Source | `backend.md` — §7.17 Production DNA Safety, structure_validators, business:validate |
| Related architecture | structure.md DNA production safety §12.3 |
| Priority order | 22 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Production DNA validators: risk tiers, human gates, rollback, provenance fields.
- business:validate integration and runtime activate_workflow_version / production_ready checks.
- structure_validators module behaviour.
- Rejection → lesson learning without production mutation.

### 1.2 Out of scope
- Authoring all business DNA content.
- Soft-warning-only production activate.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-22-01 | Governance | Unsafe DNA never activates. |
| STK-22-02 | Engineers | Deterministic validator errors. |
| STK-22-03 | Learning loop | Rejections become lessons. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-22-01 | Before a workflow version is activated or marked production_ready, the backend shall run structure-aligned production DNA validators. |
| FR-22-02 | Validators shall check risk tier presence, human gate requirements for high-risk/irreversible steps, rollback declarations, and provenance-related fields as specified by structure_validators. |
| FR-22-03 | The backend shall integrate with business:validate style checks for business corpus DNA where applicable. |
| FR-22-04 | If validation fails, then the backend shall reject activation/production_ready transition and shall not partially activate unsafe DNA. |
| FR-22-05 | When validation rejects DNA, the backend shall support recording a learnable rejection lesson without mutating production DNA. |
| FR-22-06 | Validator results shall be explicit and machine-readable for clients and tests. |
| FR-22-07 | Production DNA checks shall run in runtime paths for activate_workflow_version and production_ready create/update as implemented. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-22-01 | Validator suite for a single DNA document shall complete under 200ms local. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-22-02 | Clients cannot bypass validators via force flags unless a break-glass role is explicitly designed and audited (default: no bypass). |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-22-01 | Valid flagship DNA activates. |
| AC-22-02 | DNA missing required gates fails activation. |
| AC-22-03 | Negative DNA fixtures covered by unit tests. |
| AC-22-04 | Rejection can create lesson record. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-10, BE-12 | BE-20 promote, activate path |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-22-01 | test_structure_sdd_validators or equivalent. | Automated |
| TV-22-02 | Activate path integration tests. | Automated |
| TV-22-03 | Negative DNA fixtures. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.17 Production DNA Safety | FR-22-01 … FR-22-07 |
| backend.md §24.3 DNA production safety | FR-22-01, FR-22-07 |
