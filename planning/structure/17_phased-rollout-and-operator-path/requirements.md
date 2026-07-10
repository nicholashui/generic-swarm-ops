# 17 — Phased Rollout and Operator Path

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-17` |
| Source | `structure.md` §11 |
| Priority order | 17 (last integration) |
| Status | Specification |
| Owner | Delivery lead + Ops |

---

## 1. Scope

### 1.1 In scope
- 90-day phased rollout outcomes from structure.md.
- End-to-end operator path that stitches components 01–16 into a usable system.
- Exit criteria per phase.

### 1.2 Out of scope
- Calendar commitment to calendar days on a specific project (phases are sequential capability gates).
- Full enterprise data migration.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-17-01 | Leadership | Phased risk reduction with clear exits. |
| STK-17-02 | Operators | A single path from login to complete governed work. |
| STK-17-03 | Engineering | Integration order matches dependency sketch. |
| STK-17-04 | Compliance | No phase skips gates or evaluation. |

---

## 3. Functional Requirements (EARS)

### 3.1 Phase: Foundation (maps Days 1–14)

| ID | Statement (EARS) |
|----|------------------|
| FR-17-01 | When foundation phase completes, the system shall have business folder structure, event-log schema, AI inventory, risk tiers, audit logging, and at least 20 golden tasks. |

### 3.2 Phase: Shadow learning (maps Days 15–30)

| ID | Statement (EARS) |
|----|------------------|
| FR-17-02 | When shadow learning phase completes, the system shall support shadow mode capture, expert interview artifacts, event log collection, first decision cards, and a knowledge-ingestion pipeline. |

### 3.3 Phase: Controlled co-pilot (maps Days 31–60)

| ID | Statement (EARS) |
|----|------------------|
| FR-17-03 | When controlled co-pilot phase completes, the system shall provide retrieval with provenance, approval gates, first Workflow DNA execution, regression tests, and co-pilot behavior for low/medium-risk workflows. |

### 3.4 Phase: Evolution sandbox (maps Days 61–90)

| ID | Statement (EARS) |
|----|------------------|
| FR-17-04 | When evolution sandbox phase completes, the system shall provide variant generation, mutation of prompts/workflows in sandbox, eval harness integration, canary deploy, and rollback. |
| FR-17-05 | When promoting a variant after this phase, the system shall require passing safety, quality, and business tests. |

### 3.5 Integrated operator path

| ID | Statement (EARS) |
|----|------------------|
| FR-17-06 | When an authorized operator logs in, the system shall allow listing of agents and workflows from the live control plane. |
| FR-17-07 | When an operator starts a flagship workflow with valid inputs, the system shall execute bounded steps using tool adapters. |
| FR-17-08 | When a human gate is encountered, the system shall require approval before completion. |
| FR-17-09 | When a run completes, the system shall allow inspection of audit logs, memory, and evaluation results. |
| FR-17-10 | When improvement is desired, the system shall support sandbox propose → evaluate → canary without direct production mutation. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-17-01 | Full automated operator-path API test shall complete within 5 minutes excluding human think time. |
| NFR-17-02 | Phase exit reviews shall be documentable within a single working session using verification checklists. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-17-03 | No rollout phase shall disable authentication, audit, or approval gates to “go faster.” |
| NFR-17-04 | Production-like profiles shall use durable primary storage and secret-safe configuration. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-17-01 | Foundation checklist items from FR-17-01 verified. |
| AC-17-02 | Shadow learning artifacts exist for at least one process and one DRC. |
| AC-17-03 | Co-pilot: DNA run + gate + regression suite green. |
| AC-17-04 | Evolution: propose/eval/canary/rollback proven. |
| AC-17-05 | Operator path E2E test or checklist signed (login → run → approve → complete → improve). |
| AC-17-06 | Scorecard/verification artifacts updated for the release. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-01 … STRUCT-16 (all prior) | Release readiness, operator training |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-17-01 | Phase exit checklist review against structure.md §11. | Review |
| TV-17-02 | Automated E2E operator path. | Automated |
| TV-17-03 | Manual UI dogfood checklist with DEMO_MODE off. | Manual |
| TV-17-04 | Aggregate gates: `npm test`, business:*, backend unit/e2e, frontend tests. | Automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §11 Days 1–14 | FR-17-01 |
| §11 Days 15–30 | FR-17-02 |
| §11 Days 31–60 | FR-17-03 |
| §11 Days 61–90 | FR-17-04 … FR-17-05 |
| End-to-end system use | FR-17-06 … FR-17-10 |
