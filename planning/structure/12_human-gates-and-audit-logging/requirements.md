# 12 — Human Gates and Audit Logging

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-12` |
| Source | `structure.md` §4 guardrails, §2 audit path, §6 approvals |
| Priority order | 12 |
| Status | Specification |
| Owner | Governance + Runtime |

---

## 1. Scope

### 1.1 In scope
- Human approval requests and resume/reject behavior.
- Gate triggers: high risk, exceptions, irreversible tools.
- Append-oriented audit logging for actions, tools, approvals, and security-relevant events.

### 1.2 Out of scope
- Full enterprise BPMN human workflow product.
- Email/SMS notification vendor specifics (channel optional).

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-12-01 | Reviewers | Clear approval queue with evidence and risk tier. |
| STK-12-02 | Operators | Runs pause safely and resume after decision. |
| STK-12-03 | Auditors | Complete, queryable audit trail. |
| STK-12-04 | Compliance | No silent completion of gated steps. |

---

## 3. Functional Requirements (EARS)

### 3.1 Human gates

| ID | Statement (EARS) |
|----|------------------|
| FR-12-01 | When DNA guardrails require human approval, the system shall create an approval request and pause the run. |
| FR-12-02 | When risk_tier is high or contract_exception_detected is true, the system shall require human approval before continuing gated steps. |
| FR-12-03 | When a tool action is irreversible, the system shall require human approval before execution of that action. |
| FR-12-04 | When a reviewer approves a pending request, the system shall resume the workflow from the gated step. |
| FR-12-05 | When a reviewer rejects a pending request, the system shall fail or cancel the run according to policy and record the reason. |
| FR-12-06 | While an approval is pending, the system shall not execute the gated irreversible action. |
| FR-12-07 | When presenting an approval, the system shall show risk tier, requesting context, and triggering run identity. |

### 3.2 Audit logging

| ID | Statement (EARS) |
|----|------------------|
| FR-12-08 | When a security-relevant action occurs, the system shall append an audit log entry. |
| FR-12-09 | When a tool executes, the system shall audit tool identity, actor, run/step, and outcome. |
| FR-12-10 | When an approval decision is made, the system shall audit reviewer, decision, and timestamp. |
| FR-12-11 | The audit log shall be queryable by actor, action, resource type, resource id, and time range. |
| FR-12-12 | If audit write fails for a required audited action, then the system shall treat the action as failed or incomplete per fail-closed policy. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-12-01 | Approval list queries shall return within 1 second for baseline data volumes. |
| NFR-12-02 | Audit append shall not block tool execution beyond 100 ms under normal conditions (async buffer acceptable if durability is guaranteed). |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-12-03 | Only authorized reviewer roles shall approve or reject gated requests. |
| NFR-12-04 | Audit logs shall be append-only from application clients (no user delete API for production audit). |
| NFR-12-05 | Audit entries shall include request correlation identifiers where available. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-12-01 | Flagship run pauses on irreversible billing/email-style step until approval. |
| AC-12-02 | Approve resumes and completes; reject stops gated progress. |
| AC-12-03 | Audit log contains tool and approval events for the run. |
| AC-12-04 | Non-reviewer cannot approve. |
| AC-12-05 | FE approvals page or API lists pending items with risk context. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-04, STRUCT-10, STRUCT-11 | STRUCT-13, STRUCT-16, STRUCT-17 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-12-01 | E2E: run → pending approval → approve → complete. | Automated |
| TV-12-02 | Unit: reject path. | Automated |
| TV-12-03 | RBAC: reviewer vs operator permissions. | Automated |
| TV-12-04 | Audit query filters. | Automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §4.1 guardrails human_approval_required_if | FR-12-01 … FR-12-03 |
| §2 Audit Log + Memory Write | FR-12-08 … FR-12-12 |
| §6 human approval policy | FR-12-04 … FR-12-07 |
