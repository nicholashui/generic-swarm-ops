# 03 — Intake and Risk Router

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-03` |
| Source | `structure.md` §2 high-level architecture |
| Priority order | 03 |
| Status | Specification |
| Owner | Orchestration + Governance |

---

## 1. Scope

### 1.1 In scope
- Entry point for events and user requests.
- Risk classification prior to orchestration.
- Routing into bounded execution paths.

### 1.2 Out of scope
- Full step execution of workflow DNA (STRUCT-11).
- Evolution of routing logic (STRUCT-14).
- Frontend form design details (STRUCT-16).

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-03-01 | Operator | Clear entry for work requests with predictable routing. |
| STK-03-02 | Risk owner | No high-risk work enters unrestricted paths. |
| STK-03-03 | Auditor | Classification decisions are logged with reasons. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|----|------------------|
| FR-03-01 | When an event or request arrives, the system shall pass it through intake before workflow execution. |
| FR-03-02 | When intake receives a request, the system shall classify risk using defined autonomy risk tiers. |
| FR-03-03 | When risk classification completes, the system shall attach the assigned risk tier to the case or run context. |
| FR-03-04 | The system shall route classified work to the business orchestrator for state-graph execution. |
| FR-03-05 | If classification signals high risk or restricted use, then the system shall select a path that requires elevated human oversight. |
| FR-03-06 | When intake rejects a request for policy reasons, the system shall record the rejection reason in the audit trail. |
| FR-03-07 | While a request is unclassified, the system shall not execute irreversible tool actions for that request. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-03-01 | Synchronous intake classification for standard requests shall complete within 2 seconds excluding external network I/O. |
| NFR-03-02 | Intake shall accept idempotency keys where clients may retry without creating duplicate cases. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-03-03 | Intake shall authenticate and authorize the caller before accepting work. |
| NFR-03-04 | If payload content is untrusted, then the system shall treat it as data, not as instructions that expand privileges. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-03-01 | Every started workflow run has a recorded risk tier. |
| AC-03-02 | Unauthenticated callers cannot start production runs. |
| AC-03-03 | Audit log contains intake classification or routing events for sample runs. |
| AC-03-04 | Restricted-tier paths cannot skip human gates defined by governance. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-01, STRUCT-04 (tiers) | STRUCT-11 execution, STRUCT-12 audit |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-03-01 | Unit/integration: classify sample payloads into tiers 0–5. | Automated |
| TV-03-02 | Negative: start run without auth → reject. | Automated |
| TV-03-03 | Trace: intake → orchestrator handoff for flagship workflow. | E2E |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §2 Intake + Risk Router | FR-03-01 … FR-03-07 |
| §6.1 Risk tiers (consumer) | FR-03-02, FR-03-05 |
