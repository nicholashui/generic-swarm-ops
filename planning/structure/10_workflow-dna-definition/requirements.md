# 10 — Workflow DNA Definition

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-10` |
| Source | `structure.md` §4.1 |
| Priority order | 10 |
| Status | Specification |
| Owner | Business Orchestrator + Workflow authors |

---

## 1. Scope

### 1.1 In scope
- Workflow DNA schema: identity, inputs, preconditions, steps, memory R/W, guardrails, verification, rollback, fitness metrics.
- Validation rules that reject unsafe production DNA.
- Flagship example structure (customer onboarding pattern).

### 1.2 Out of scope
- Runtime step execution engine internals (STRUCT-11).
- Evolution of DNA variants (STRUCT-14).

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-10-01 | Workflow author | Declarative, reviewable workflow contract. |
| STK-10-02 | Governance | Guardrails and verification declared up front. |
| STK-10-03 | Ops | Rollback plan visible before go-live. |
| STK-10-04 | Evaluation | Fitness metrics defined for scoring. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|----|------------------|
| FR-10-01 | The system shall represent production workflows as versioned Workflow DNA documents. |
| FR-10-02 | When DNA is authored, the system shall require id, name, domain, objective, owner, and version. |
| FR-10-03 | When DNA is authored, the system shall declare inputs and preconditions. |
| FR-10-04 | When DNA steps are defined, each step shall declare id, agent, and allowed tools. |
| FR-10-05 | When DNA is authored, the system shall declare memory_reads and memory_writes. |
| FR-10-06 | When DNA is authored, the system shall declare guardrails including human_approval_required_if conditions. |
| FR-10-07 | When DNA is authored, the system shall declare verification.required_checks. |
| FR-10-08 | When DNA is authored, the system shall declare rollback.reversible and rollback_steps where actions may need reversal. |
| FR-10-09 | When DNA is authored, the system shall declare fitness_metrics used for evaluation and evolution. |
| FR-10-10 | If a high-risk or irreversible step lacks a human gate declaration, then the validator shall reject the DNA for production. |
| FR-10-11 | If an irreversible action lacks a rollback plan, then the validator shall reject the DNA for production. |
| FR-10-12 | If provenance or audit-log write requirements are missing where policy demands them, then the validator shall reject the DNA for production. |
| FR-10-13 | The system shall provide a flagship onboarding-style DNA example matching the structure.md schema pattern. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-10-01 | DNA schema validation shall complete in under 2 seconds per workflow document. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-10-02 | DNA shall not embed secrets; secrets shall be referenced via secure configuration. |
| NFR-10-03 | Tool lists in DNA shall be least privilege (no unrestricted wildcards in production). |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-10-01 | Workflow DNA schema and example validate via business validation. |
| AC-10-02 | Invalid DNA missing gate on irreversible step fails validation. |
| AC-10-03 | Flagship DNA includes fitness metrics and verification checks. |
| AC-10-04 | Version field is present and immutable history is retained on change. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-01, STRUCT-04, STRUCT-05, STRUCT-08 | STRUCT-11, STRUCT-12, STRUCT-13, STRUCT-14 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-10-01 | Schema validation of examples. | Automated |
| TV-10-02 | Negative fixtures for missing gates/rollback. | Automated |
| TV-10-03 | `npm run business:validate` includes workflow DNA checks. | Automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §4.1 Schema fields | FR-10-01 … FR-10-09 |
| Guardrails / verification / rollback | FR-10-06 … FR-10-12 |
| Example onboarding DNA | FR-10-13 |
