# 11 — Bounded Workflow Execution

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-11` |
| Source | `structure.md` §4.2, §2 Business Orchestrator |
| Priority order | 11 |
| Status | Specification |
| Owner | Business Orchestrator runtime |

---

## 1. Scope

### 1.1 In scope
- Bounded state-graph execution (not free-form swarm authority).
- Pattern: Event → Intake → Risk → Orchestrator → Research → Execution → Verification → Compliance → Human Gate → Audit/Memory → Evaluation → Evolution handoff.
- Tool invocation via allow-listed adapters with durable effects.
- ReAct-style reasoning only inside nodes, not as global authority.

### 1.2 Out of scope
- Free-form multi-agent chat without DNA.
- Live external vendor adapters beyond local/stub adapters (may be extended later).

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-11-01 | Operators | Predictable run lifecycle with status and steps. |
| STK-11-02 | Security | Tools only run when graph + allow-list permit. |
| STK-11-03 | Customers / process owners | Work completes with verification checks. |
| STK-11-04 | Engineers | Deterministic graph control over model creativity. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|----|------------------|
| FR-11-01 | The system shall execute workflows as bounded state graphs defined by Workflow DNA. |
| FR-11-02 | When a run starts, the business orchestrator shall own run state transitions and global objective tracking for that run. |
| FR-11-03 | When a step executes, the system shall allow only the tools declared for that step and agent. |
| FR-11-04 | When a tool executes successfully, the system shall persist durable tool effects suitable for audit and verification. |
| FR-11-05 | When a tool execution fails closed, the system shall mark the step failed or blocked and shall not invent success. |
| FR-11-06 | While a step is in research mode, the system may use retrieval and reasoning inside the node without granting extra tools. |
| FR-11-07 | When verification checks are required, the system shall evaluate required_checks before marking the run complete. |
| FR-11-08 | If a required verification check fails and block_on_fail is set, then the system shall not mark the run successful. |
| FR-11-09 | When memory_reads are declared, the system shall perform scoped memory reads before or during the step as specified. |
| FR-11-10 | When memory_writes are declared, the system shall write only to allowed scopes with provenance rules. |
| FR-11-11 | The system shall not grant free-form swarm authority that bypasses graph state or permissions. |
| FR-11-12 | When a run completes or fails, the system shall hand off artifacts to evaluation and optionally to evolution observation pathways. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-11-01 | Simple multi-step runs with local adapters shall complete within 30 seconds under unloaded local conditions excluding human wait time. |
| NFR-11-02 | Run status reads shall be available within 500 ms of request under normal load. |
| NFR-11-03 | Long-running work shall support queued/async execution patterns. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-11-04 | Execution shall enforce authentication and RBAC on start, cancel, and retry operations. |
| NFR-11-05 | Model output shall not execute tools without graph and allow-list validation. |
| NFR-11-06 | Irreversible tools shall be reachable only through gated paths defined in DNA and governance. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-11-01 | Flagship DNA run progresses through steps with tool_effects recorded. |
| AC-11-02 | Unauthorized tool attempt is blocked. |
| AC-11-03 | Verification failure prevents success when configured. |
| AC-11-04 | Run status stream or polling reflects step transitions. |
| AC-11-05 | E2E operator path can complete after human gate (cross-ref STRUCT-12). |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-03, STRUCT-04, STRUCT-05, STRUCT-08, STRUCT-09, STRUCT-10 | STRUCT-12, STRUCT-13, STRUCT-14, STRUCT-16 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-11-01 | Unit/integration: real tool adapters write tool_effects. | Automated |
| TV-11-02 | Live ASGI run tests for start → step progress. | Automated |
| TV-11-03 | E2E: flagship onboarding path. | Automated |
| TV-11-04 | Negative: tool not allow-listed. | Automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §4.2 Execution Pattern | FR-11-01 … FR-11-12 |
| Business Orchestrator (§2, §9) | FR-11-02 |
| Graph vs free-form swarm | FR-11-11 |
