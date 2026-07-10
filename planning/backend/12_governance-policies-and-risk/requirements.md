# 12 — Governance Policies and Risk

| Field | Value |
|-------|-------|
| Spec ID | `BE-12` |
| Source | `backend.md` — §7.9 (policy engine), §11.11, §13 Governance Design |
| Related architecture | structure.md §6 risk tiers and policies |
| Priority order | 12 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Governance layer decisions: allow, deny, require_approval, require_evaluation, require_redaction.
- Risk levels low/medium/high/critical with meanings.
- Policy CRUD and check endpoints.
- Pre-check before run and per-step/tool checks.

### 1.2 Out of scope
- Approval request lifecycle storage details owned jointly with BE-13.
- Full legal compliance program management UI.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-12-01 | Risk owners | Policies encode when work may proceed. |
| STK-12-02 | Operators | Predictable deny/approve requirements. |
| STK-12-03 | Auditors | Policy checks are explainable. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-12-01 | The backend shall include a governance layer that decides whether a workflow can run, a step can execute, a tool can be used, data can be accessed, human approval is required, and output can be released. |
| FR-12-02 | The backend shall support risk levels low, medium, high, and critical with documented meanings. |
| FR-12-03 | When a governance check runs, the backend shall return an action among allow, deny, require_approval, require_evaluation, and require_redaction. |
| FR-12-04 | The backend shall support governance policies with conditions and actions (e.g. require approval for external email). |
| FR-12-05 | The backend shall expose policy list/create/get/update/archive and check/preview endpoints. |
| FR-12-06 | When starting a workflow run, the backend shall run a governance pre-check before execution proceeds to irreversible work. |
| FR-12-07 | If governance returns deny, then the backend shall block the action and record the decision reason. |
| FR-12-08 | If governance returns require_approval, then the backend shall create or require an approval gate before continuing. |
| FR-12-09 | Governance policy changes shall be restricted to authorized roles and audited. |
| FR-12-10 | The backend shall support mapping structure autonomy risk tiers into runtime policy enforcement where configured (runtime tier policy). |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-12-01 | Policy check for typical rule sets shall complete under 50ms local. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-12-02 | Clients shall not override governance deny via request flags. |
| NFR-12-03 | Policy documents shall be protected from unauthorized update. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-12-01 | Policy check endpoint returns allow/deny/require_approval. |
| AC-12-02 | External-email style policy can force approval. |
| AC-12-03 | Deny blocks tool invocation. |
| AC-12-04 | Policy update writes audit event. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-06, BE-03 | BE-11, BE-13, BE-22 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-12-01 | Unit: policy engine table tests. | Automated |
| TV-12-02 | Integration: pre-check on run start. | Automated |
| TV-12-03 | Negative: unauthorized policy update. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.9 Governance | FR-12-01, FR-12-07 … FR-12-08 |
| backend.md §13 Governance Design | FR-12-02 … FR-12-04 |
| backend.md §11.11 | FR-12-05 |
