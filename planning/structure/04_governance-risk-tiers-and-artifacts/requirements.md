# 04 — Governance Risk Tiers and Artifacts

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-04` |
| Source | `structure.md` §6 |
| Priority order | 04 |
| Status | Specification |
| Owner | Governance Officer role |

---

## 1. Scope

### 1.1 In scope
- Autonomy risk tiers 0–5 and allowed behaviors.
- Mandatory governance artifacts (inventory, policies, model cards, assurance cases).
- Alignment anchors: NIST AI RMF, ISO/IEC 42001, EU AI Act awareness for high-risk uses.

### 1.2 Out of scope
- Certification audits against ISO/EU (organizational process outside software).
- Implementation of every legal control for all jurisdictions.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-04-01 | Compliance | Risk-tiered autonomy with documented policies. |
| STK-04-02 | Legal / privacy | High-risk employment-related uses flagged for extra controls. |
| STK-04-03 | Operators | Clear when human approval is mandatory. |
| STK-04-04 | Leadership | AI inventory of agents and use cases. |

---

## 3. Functional Requirements (EARS)

### 3.1 Risk tiers

| ID | Statement (EARS) |
|----|------------------|
| FR-04-01 | The system shall define autonomy risk tiers 0 through 5 with the allowed behaviors specified in structure.md §6.1. |
| FR-04-02 | While a workflow is at tier 0 (observe), the system shall only log and summarize and shall not act on external systems. |
| FR-04-03 | While a workflow is at tier 1 (recommend), the system shall produce suggestions and shall require a human to act. |
| FR-04-04 | While a workflow is at tier 2 (draft), the system shall prepare artifacts and shall require human approval before send or execute. |
| FR-04-05 | While a workflow is at tier 3 (execute reversible), the system shall allow action only when a rollback path exists and risk is low. |
| FR-04-06 | While a workflow is at tier 4 (execute + gate), the system shall pause for human approval on the critical step before completion. |
| FR-04-07 | While a workflow is at tier 5 (restricted), the system shall block autonomous action until an assurance case exists. |

### 3.2 Mandatory artifacts

| ID | Statement (EARS) |
|----|------------------|
| FR-04-08 | The system shall maintain an AI inventory of registered agents and use cases. |
| FR-04-09 | The system shall maintain use-case risk tiering records. |
| FR-04-10 | The system shall maintain a human-approval policy defining gate triggers and responsibilities. |
| FR-04-11 | The system shall maintain model cards for material models/orchestrators in use. |
| FR-04-12 | When a use case is tier 4 or higher for irreversible impact, the system shall require an assurance case artifact before elevated autonomy. |
| FR-04-13 | The system shall maintain tool-permission register entries for tools available to agents. |
| FR-04-14 | If a mandatory governance artifact is missing for a production workflow, then the system shall fail governance validation. |

### 3.3 Framework anchoring

| ID | Statement (EARS) |
|----|------------------|
| FR-04-15 | Governance documentation shall reference NIST AI RMF map/measure/manage concepts for risk handling. |
| FR-04-16 | Where the system may affect EU users or employment-related decisions, governance documentation shall identify EU AI Act high-risk implications and required human oversight. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-04-01 | Governance validation of the business tree shall complete in under 60 seconds for baseline artifacts. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-04-02 | Governance policies shall be enforced by backend authorization, not by UI hiding alone. |
| NFR-04-03 | Assurance cases and inventory shall be integrity-protected via version control and review. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-04-01 | Human-approval policy document exists under `business/governance/`. |
| AC-04-02 | AI inventory and at least one model card exist. |
| AC-04-03 | Tier-4 assurance case exists for flagship high-impact path. |
| AC-04-04 | `npm run business:governance` passes. |
| AC-04-05 | Tier 5 workflows cannot execute tools without assurance evidence. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-01, STRUCT-02 | STRUCT-03, STRUCT-05, STRUCT-11, STRUCT-12, STRUCT-14 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-04-01 | `npm run business:governance` | Automated |
| TV-04-02 | Policy table review for tiers 0–5 completeness | Review |
| TV-04-03 | Runtime test: tier-4 step waits for approval | Automated / E2E |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §6.1 Autonomy Risk Tiers | FR-04-01 … FR-04-07 |
| §6.2 Mandatory Artifacts | FR-04-08 … FR-04-14 |
| Framework anchors | FR-04-15 … FR-04-16 |
