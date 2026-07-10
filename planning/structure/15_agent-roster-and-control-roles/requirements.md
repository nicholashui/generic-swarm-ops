# 15 — Agent Roster and Control Roles

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-15` |
| Source | `structure.md` §9 |
| Priority order | 15 |
| Status | Specification |
| Owner | Architecture + Runtime seed |

---

## 1. Scope

### 1.1 In scope
- Control/meta agent roles and learning agent roles.
- Mapping roles to responsibilities and permission boundaries.
- Registration of agents in inventory and runtime.

### 1.2 Out of scope
- Requiring each role to be a separate distributed microservice.
- Full autonomy of every learning agent on day one (may be services/stubs).

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-15-01 | Operators | Know which agent owns which responsibility. |
| STK-15-02 | Security | Clear least-privilege per agent. |
| STK-15-03 | Product | Learning vs control separation is visible. |
| STK-15-04 | Governance | Agents appear in AI inventory. |

---

## 3. Functional Requirements (EARS)

### 3.1 Control / meta agents

| ID | Statement (EARS) |
|----|------------------|
| FR-15-01 | The system shall define a Business Orchestrator role that routes work, manages state, and owns the global objective for runs. |
| FR-15-02 | The system shall define an Evolution Manager role that proposes and tests variants only in sandbox. |
| FR-15-03 | The system shall define an Evaluation Harness role that runs golden, regression, adversarial, and replay suites. |
| FR-15-04 | The system shall define a Governance Officer role that applies risk tiers, approval rules, and audit requirements. |
| FR-15-05 | The system shall define a Security Red-Team role that tests injection, tool misuse, leakage, and unsafe autonomy. |
| FR-15-06 | The system shall define a Memory Steward role that maintains memory quality, provenance, and expiration. |
| FR-15-07 | The system shall define a Tool Permission Broker role that grants scoped, temporary tool access. |
| FR-15-08 | The system shall define an Incident Commander role that handles failures, rollbacks, and postmortems. |

### 3.2 Learning agents

| ID | Statement (EARS) |
|----|------------------|
| FR-15-09 | The system shall define an Expert Shadow role for observing experts with permission. |
| FR-15-10 | The system shall define a Cognitive Task Analyst role that turns interviews into decision cards and heuristics. |
| FR-15-11 | The system shall define Process Miner, Task Mining, Conformance, Bottleneck Analyzer, and Causal Improvement roles aligned with process intelligence. |
| FR-15-12 | The system shall define Knowledge Distiller and Knowledge Curator roles for converting and validating knowledge assets. |

### 3.3 Registration and boundaries

| ID | Statement (EARS) |
|----|------------------|
| FR-15-13 | When an agent is registered, the system shall record allowed tools and allowed memory scopes. |
| FR-15-14 | If an agent attempts actions outside its role permissions, then the system shall deny the action. |
| FR-15-15 | When agents are material to production use cases, the system shall list them in the AI inventory. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-15-01 | Agent registry list API shall return within 500 ms for baseline seed agents. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-15-02 | Agent credentials shall not be shared across roles with different privilege levels. |
| NFR-15-03 | Evolution Manager permissions shall exclude direct production DNA write. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-15-01 | Seed/runtime includes orchestrator and supporting flagship agents with tool allow-lists. |
| AC-15-02 | AI inventory references control and learning roles. |
| AC-15-03 | Documentation maps each structure.md roster row to implementation (service, agent record, or process). |
| AC-15-04 | Out-of-scope tool use by an agent is denied. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-04, STRUCT-05, STRUCT-06, STRUCT-07 | STRUCT-11, STRUCT-14, STRUCT-16 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-15-01 | Seed agents present with allow-lists. | Automated |
| TV-15-02 | Inventory completeness review. | Review |
| TV-15-03 | Permission denial for wrong tool. | Automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §9 Control / Meta table | FR-15-01 … FR-15-08 |
| §9 Learning table | FR-15-09 … FR-15-12 |
| Permission boundaries | FR-15-13 … FR-15-15 |
