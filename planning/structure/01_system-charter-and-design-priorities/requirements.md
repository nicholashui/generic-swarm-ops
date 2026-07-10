# 01 — System Charter and Design Priorities

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-01` |
| Source | `structure.md` §0–1 |
| Priority order | 01 (first) |
| Status | Specification |
| Owner | Product + Architecture |

---

## 1. Scope

### 1.1 In scope
- System mission: learn business operations, distill knowledge, execute bounded workflows, evolve only in sandbox.
- Ordered design priorities: Safety → Auditability → Correctness → Efficiency → Autonomy.
- Seven core principles that constrain all downstream components.

### 1.2 Out of scope
- Concrete API routes, UI pages, database schemas (later components).
- Domain-specific workflow content.
- Vendor selection for LLM or vector databases.

### 1.3 System under specification
The Generic Swarm Business Operating System (GSO) as defined in `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-01-01 | Business owner | Autonomy only when earned by evidence; not default full autonomy. |
| STK-01-02 | Compliance / risk | Safety and auditability outrank efficiency and autonomy. |
| STK-01-03 | Operators | System behavior is explainable and correctable by humans. |
| STK-01-04 | Engineers | Principles are enforceable as acceptance gates for every feature. |
| STK-01-05 | Security | Sandbox evolution and bounded actions limit blast radius. |

---

## 3. Functional Requirements (EARS)

### 3.1 Mission capabilities

| ID | Statement (EARS) |
|----|------------------|
| FR-01-01 | The system shall learn how a business operates from documents, expert input, and real event logs. |
| FR-01-02 | The system shall distill learned knowledge into reusable rules, skills, workflows, and playbooks. |
| FR-01-03 | The system shall execute work through bounded, auditable agent workflows. |
| FR-01-04 | The system shall evolve workflows only inside a sandbox pathway and never by direct production mutation. |

### 3.2 Design priority enforcement

| ID | Statement (EARS) |
|----|------------------|
| FR-01-05 | When a design trade-off exists between safety and autonomy, the system shall prefer the safer option. |
| FR-01-06 | When a design trade-off exists between auditability and efficiency, the system shall prefer auditability. |
| FR-01-07 | When a design trade-off exists between correctness and efficiency, the system shall prefer correctness. |
| FR-01-08 | While a workflow lacks sufficient evaluation evidence, the system shall withhold elevated autonomy. |

### 3.3 Core principles

| ID | Statement (EARS) |
|----|------------------|
| FR-01-09 | The system shall prefer learning from real operational traces over unsupported opinion. |
| FR-01-10 | When the system performs an action, the system shall associate that action with a risk tier and a permission scope. |
| FR-01-11 | If a human gate is required by risk or irreversibility, then the system shall not complete the action without approval. |
| FR-01-12 | If an agent, prompt, or workflow has not passed required evaluation, then the system shall not promote it to production. |
| FR-01-13 | The evolution capability shall propose variants and shall not mutate production configuration directly. |
| FR-01-14 | When the system stores a rule, decision, or memory item, the system shall retain provenance to a source. |
| FR-01-15 | When an action is irreversible, the system shall require a declared rollback plan or a human gate. |
| FR-01-16 | When the system presents a recommendation or action preview, the system shall expose confidence and supporting evidence where available. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-01-01 | Principle checks shall not require online LLM calls; they shall be enforceable by deterministic policy code. |
| NFR-01-02 | Design-priority resolution shall be documentable in review artifacts within one human review cycle. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-01-03 | The system shall treat design principles as non-bypassable by prompt text alone. |
| NFR-01-04 | If a feature request would allow unattended production DNA mutation, then the system shall reject the feature as out of charter. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-01-01 | Charter document lists the four mission capabilities and ordered priorities. |
| AC-01-02 | Every downstream `planning/structure/*` spec references this charter’s priority order. |
| AC-01-03 | Governance and evolution specs explicitly forbid direct production mutation. |
| AC-01-04 | Review checklist includes “principle conflict resolution” for architecture changes. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| None (root) | All components 02–17 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-01-01 | Document review: map each principle to at least one enforceable control in later specs. | Review |
| TV-01-02 | Negative test design: attempt to specify auto-promote-to-production; expect rejection against FR-01-04 / FR-01-13. | Spec gate |
| TV-01-03 | Traceability matrix: charter FR IDs → later FR IDs (see `planning/structure/README.md`). | Traceability |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §0 What This Is | FR-01-01 … FR-01-04 |
| §1 Core Principles | FR-01-09 … FR-01-16 |
| Design priorities list | FR-01-05 … FR-01-08 |
