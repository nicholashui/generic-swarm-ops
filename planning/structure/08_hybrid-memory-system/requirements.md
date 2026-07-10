# 08 — Hybrid Memory System

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-08` |
| Source | `structure.md` §3.3 |
| Priority order | 08 |
| Status | Specification |
| Owner | Memory Steward |

---

## 1. Scope

### 1.1 In scope
- Differentiated memory types: event, episodic, semantic, procedural, decision, exception, evaluation, provenance.
- Scoped lookup and write controls.
- Provenance and poisoning defenses for high-impact writes.

### 1.2 Out of scope
- Infinite long-term personalization products.
- Cross-organization memory sharing without policy.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-08-01 | Agents / orchestrator | Right memory type for the task, not a single bag of text. |
| STK-08-02 | Security | No memory poisoning via untrusted writes. |
| STK-08-03 | Operators | Ability to inspect and correct stored decisions. |
| STK-08-04 | Compliance | Provenance on material memories. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|----|------------------|
| FR-08-01 | The system shall support distinct memory types: event, episodic, semantic, procedural, decision, exception, evaluation, and provenance. |
| FR-08-02 | When storing raw operational logs, the system shall classify them as event memory. |
| FR-08-03 | When storing case narratives, the system shall classify them as episodic memory. |
| FR-08-04 | When storing facts and rules, the system shall classify them as semantic memory. |
| FR-08-05 | When storing skills and how-to procedures, the system shall classify them as procedural memory. |
| FR-08-06 | When storing decisions and reasons, the system shall classify them as decision memory. |
| FR-08-07 | When storing edge cases, the system shall classify them as exception memory. |
| FR-08-08 | When storing test outcomes, the system shall classify them as evaluation memory. |
| FR-08-09 | When storing source attribution, the system shall classify them as provenance memory or attach provenance metadata to items. |
| FR-08-10 | When a memory read is requested, the system shall enforce scopes including organization, user, agent, workflow, sensitivity, and expiration where configured. |
| FR-08-11 | If an agent requests memory outside its allowed scopes, then the system shall deny the read or write. |
| FR-08-12 | When a high-impact memory write occurs, the system shall require provenance and apply policy review rules. |
| FR-08-13 | While a memory item is expired, the system shall not return it for operational decisioning. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-08-01 | Scoped memory read for a single key/query shall complete within 200 ms excluding cold-start database latency targets agreed for the environment. |
| NFR-08-02 | Memory writes shall be durable after successful commit to the primary store. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-08-03 | Memory items marked sensitive shall not appear in unrestricted search results. |
| NFR-08-04 | Memory poisoning defenses shall treat untrusted content as non-authoritative without provenance. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-08-01 | Memory API or store supports typed items and scopes. |
| AC-08-02 | Out-of-scope memory access fails closed for flagship agents. |
| AC-08-03 | Provenance present on high-impact writes in sample runs. |
| AC-08-04 | Expired items excluded from operational reads in tests. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-02, STRUCT-05, STRUCT-07 | STRUCT-09 retrieval, STRUCT-11 execution, STRUCT-14 lessons |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-08-01 | Unit: scope deny/allow matrix. | Automated |
| TV-08-02 | Integration: write decision memory with provenance. | Automated |
| TV-08-03 | Negative: agent without organization_memory cannot read org-scoped items (as configured). | Automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §3.3 Hybrid Memory table | FR-08-01 … FR-08-09 |
| Scoped lookup / poisoning | FR-08-10 … FR-08-13 |
| Memory Steward (§9) | Owner accountability |
