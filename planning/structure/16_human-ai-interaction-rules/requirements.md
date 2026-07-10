# 16 — Human–AI Interaction Rules

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-16` |
| Source | `structure.md` §10 |
| Priority order | 16 |
| Status | Specification |
| Owner | Product + Frontend ops console |

---

## 1. Scope

### 1.1 In scope
- Interaction rules synthesizing human-AI guidelines: confidence, evidence, previews, correction, override, rejected-suggestion capture, clarification, honest uncertainty.
- Operator-facing surfaces for runs, approvals, knowledge, and improvement actions.

### 1.2 Out of scope
- Pixel-perfect marketing design system.
- Voice/AR modalities.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-16-01 | Operators | Understand what the system will do before it does it. |
| STK-16-02 | Reviewers | Evidence and risk context for decisions. |
| STK-16-03 | End users of co-pilot modes | Easy correction and override. |
| STK-16-04 | Product | UX does not invent backend authority. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|----|------------------|
| FR-16-01 | When the system presents a recommendation or decision support, the system shall show confidence or uncertainty when available. |
| FR-16-02 | When the system presents a recommendation, the system shall explain the evidence used (sources, events, or rules). |
| FR-16-03 | When the system is about to execute a consequential action, the system shall preview the action before execution where interaction mode is co-pilot or gated. |
| FR-16-04 | When a user corrects a suggestion, the system shall apply the correction path in one primary action where feasible. |
| FR-16-05 | When a user overrides a recommendation, the system shall allow the override subject to authorization policy. |
| FR-16-06 | When a user rejects a suggestion, the system shall store the rejection as learning/training feedback data where policy permits. |
| FR-16-07 | When context is insufficient, the system shall ask for clarification rather than inventing critical facts. |
| FR-16-08 | The system shall not hide uncertainty behind falsely confident language in operator-facing copy. |
| FR-16-09 | While rendering operator UI, the system shall treat UI permission checks as convenience only and shall rely on backend authorization for enforcement. |
| FR-16-10 | When a workflow run is active, the system shall show status, current step, and pending approvals clearly. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-16-01 | Primary ops pages shall reach interactive state within 3 seconds on a local network against a healthy API. |
| NFR-16-02 | Run detail updates shall reflect new events within 2 seconds when streaming is enabled. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-16-03 | Frontend shall not store long-lived secrets in localStorage for production profiles. |
| NFR-16-04 | Destructive actions shall require confirmation. |
| NFR-16-05 | Error messages may include request_id but shall not leak stack traces or secrets to end users. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-16-01 | Run detail shows status, steps, and approval wait state. |
| AC-16-02 | Approvals show risk tier and evidence context. |
| AC-16-03 | Knowledge results show sources/citations. |
| AC-16-04 | Improve/evolution actions are explicit and reversible at policy level. |
| AC-16-05 | UI cannot approve without backend authorization. |
| AC-16-06 | Uncertainty/empty/error states exist on major pages. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-09, STRUCT-11, STRUCT-12, STRUCT-14 | STRUCT-17 operator path |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-16-01 | Frontend unit tests for forms, errors, live client. | Automated |
| TV-16-02 | Playwright smoke for critical routes. | Automated |
| TV-16-03 | UX review checklist against FR-16-01 … FR-16-08. | Review |
| TV-16-04 | Authz negative: hide button still blocked by API. | Automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §10 Human-AI Interaction Rules | FR-16-01 … FR-16-08 |
| Backend final authority (architecture practice) | FR-16-09 |
| Operational visibility | FR-16-10 |
