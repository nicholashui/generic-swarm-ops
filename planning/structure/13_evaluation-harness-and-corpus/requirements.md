# 13 — Evaluation Harness and Corpus

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-13` |
| Source | `structure.md` §8 |
| Priority order | 13 |
| Status | Specification |
| Owner | Evaluation Harness role |

---

## 1. Scope

### 1.1 In scope
- Eight evaluation ownership classes for agents, skills, workflows, and prompts.
- Evaluation card schema and metrics.
- Realistic multi-step, tool-using evaluation environments.
- Manual promotion decisions (no silent auto-promote).

### 1.2 Out of scope
- Replacing unit/integration tests of the host application.
- Unsupervised production promotion.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-13-01 | Product quality | Golden and regression coverage before ship. |
| STK-13-02 | Security | Adversarial evaluation of injection and tool misuse. |
| STK-13-03 | Business owners | Business-outcome and cycle-time metrics. |
| STK-13-04 | Compliance | Safety/compliance scores on evaluation cards. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|----|------------------|
| FR-13-01 | The system shall maintain golden task sets for material workflows and agents. |
| FR-13-02 | The system shall maintain regression tests that prevent known-good behavior from regressing. |
| FR-13-03 | The system shall maintain adversarial tests covering injection, tool misuse, and unsafe autonomy scenarios. |
| FR-13-04 | The system shall maintain human-review sets for cases requiring expert judgment. |
| FR-13-05 | The system shall maintain historical-replay sets for completed cases or fixtures. |
| FR-13-06 | The system shall maintain cost/latency benchmark measurements for evaluated targets. |
| FR-13-07 | The system shall record business-outcome metrics for evaluated workflows. |
| FR-13-08 | The system shall record safety/compliance scores for evaluated targets. |
| FR-13-09 | When an evaluation runs, the system shall produce an evaluation card including target, eval_type, test_set, metrics, result, and promotion_decision. |
| FR-13-10 | When evaluation metrics are recorded, the system shall include quality, compliance, cycle time, escalation, hallucination, unauthorized tool attempts, and cost per case where applicable. |
| FR-13-11 | The evaluation harness shall run in multi-step tool-using scenarios rather than isolated prompt-only checks for workflow targets. |
| FR-13-12 | If evaluation result is fail, then the system shall not set promotion_decision to full production promote. |
| FR-13-13 | The harness shall never automatically promote production DNA solely because an evaluation passed. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-13-01 | Baseline golden corpus (≥20 tasks) shall complete via harness within 10 minutes on a developer machine for dry/local modes. |
| NFR-13-02 | Evaluation artifacts shall be written to durable storage under `business/evals/`. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-13-03 | Adversarial tests shall not require disabling authentication in shared environments. |
| NFR-13-04 | Evaluation fixtures shall not embed live secrets. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-13-01 | ≥20 golden tasks exist and harness reports pass for baseline. |
| AC-13-02 | Regression, adversarial, and historical-replay suites exist. |
| AC-13-03 | Sample evaluation card fields match structure.md. |
| AC-13-04 | Auto-promote to production is blocked in harness and evolution paths. |
| AC-13-05 | `npm run business:eval` succeeds for baseline corpus. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-02, STRUCT-10, STRUCT-11, STRUCT-12 | STRUCT-14 evolution gates, STRUCT-17 rollout |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-13-01 | `npm run business:eval` | Automated |
| TV-13-02 | Count golden tasks ≥ 20. | Automated |
| TV-13-03 | Assert promotion decision never `auto_production` without human. | Automated |
| TV-13-04 | Spot-check evaluation card schema. | Review + automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §8 eight eval classes | FR-13-01 … FR-13-08 |
| Evaluation card YAML | FR-13-09 … FR-13-10 |
| Realistic multi-step eval | FR-13-11 |
| Promotion discipline | FR-13-12 … FR-13-13 |
