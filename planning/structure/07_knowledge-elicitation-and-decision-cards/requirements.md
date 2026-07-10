# 07 — Knowledge Elicitation and Decision Requirement Cards

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-07` |
| Source | `structure.md` §3.1–3.2 |
| Priority order | 07 |
| Status | Specification |
| Owner | Knowledge Distiller + Expert Shadow |

---

## 1. Scope

### 1.1 In scope
- Multi-method expert knowledge capture (shadow, critical decision interview, think-aloud, exception interview, retrospective, apprentice).
- Decision Requirement Card (DRC) schema and lifecycle fields.
- Distillation handoff into rules, skills, and playbooks (logical).

### 1.2 Out of scope
- Full multimedia interview product UI.
- Automatic legal certification of expert advice.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-07-01 | Domain experts | Capture tacit cues without free-form only notes. |
| STK-07-02 | Knowledge curator | Structured DRCs with provenance and validation tests. |
| STK-07-03 | Governance | High-stakes decisions tagged with risk and human approval. |
| STK-07-04 | Operators | Exception paths and red flags available at decision time. |

---

## 3. Functional Requirements (EARS)

### 3.1 Elicitation methods

| ID | Statement (EARS) |
|----|------------------|
| FR-07-01 | The system shall support shadow mode capture that yields event logs and action traces. |
| FR-07-02 | The system shall support critical decision interviews that yield decision requirement cards. |
| FR-07-03 | The system shall support think-aloud sessions that yield step-by-step heuristics. |
| FR-07-04 | The system shall support exception interviews that yield exception library entries. |
| FR-07-05 | The system shall support retrospective reviews that yield lessons learned. |
| FR-07-06 | The system shall support apprentice mode that yields skills and playbooks. |
| FR-07-07 | When expert capture is performed, the system shall record expert source identifiers for provenance. |

### 3.2 Decision requirement cards

| ID | Statement (EARS) |
|----|------------------|
| FR-07-08 | When a DRC is created, the system shall require id, domain, decision point, expert sources, and risk tier. |
| FR-07-09 | When a DRC is created, the system shall capture context signals, expert cues, normal action, and exception paths. |
| FR-07-10 | When a DRC includes red flags, the system shall surface those red flags to decision-support consumers. |
| FR-07-11 | When a DRC requires human approval, the system shall set human_approval_required true and enforce gating downstream. |
| FR-07-12 | When a DRC is published, the system shall include validation tests and last_reviewed metadata. |
| FR-07-13 | If a DRC lacks provenance to expert or source materials, then the system shall mark it incomplete and block production promotion. |

### 3.3 Distillation handoff

| ID | Statement (EARS) |
|----|------------------|
| FR-07-14 | When elicitation outputs are approved, the knowledge distiller pathway shall convert them into rules, skills, or playbooks under distilled assets. |
| FR-07-15 | When distillation completes, the knowledge curator pathway shall validate, deduplicate, and organize assets before operational use. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-07-01 | DRC schema validation shall complete in under 1 second per card. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-07-02 | Interview transcripts shall be access-controlled by sensitivity. |
| NFR-07-03 | Expert identifiers shall follow data-minimisation rules in exported reports. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-07-01 | DRC schema and example validate. |
| AC-07-02 | Expert capture folders exist under `business/experts/`. |
| AC-07-03 | At least one sample DRC includes risk tier and human_approval_required. |
| AC-07-04 | Incomplete DRC without provenance fails validation/promotion. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-02, STRUCT-04 | STRUCT-08 memory, STRUCT-09 retrieval, STRUCT-10 DNA, STRUCT-11 execution |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-07-01 | Schema validate DRC examples. | Automated |
| TV-07-02 | Review checklist for six elicitation methods coverage in docs/process. | Review |
| TV-07-03 | Negative: DRC missing expert_sources rejected. | Automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §3.1 Elicitation Methods | FR-07-01 … FR-07-07 |
| §3.2 Decision Requirement Card | FR-07-08 … FR-07-13 |
| Knowledge Distiller / Curator (§9) | FR-07-14 … FR-07-15 |
