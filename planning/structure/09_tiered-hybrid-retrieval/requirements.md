# 09 — Tiered Hybrid Retrieval

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-09` |
| Source | `structure.md` §3.4 |
| Priority order | 09 |
| Status | Specification |
| Owner | Knowledge platform |

---

## 1. Scope

### 1.1 In scope
- Cost-tiered retrieval: Tier 0 default, Tier 1 relational/multi-hop, Tier 2 hierarchical summaries on demand.
- Always-on provenance / citations.
- Escalation rules to keep most traffic on cheap tiers.
- Separate retrieval evaluation (context relevance, answer relevance, faithfulness).

### 1.2 Out of scope
- Full GraphRAG community-report pipelines (explicitly avoided).
- Mandatory commercial RAG vendor (AnythingLLM/RAGFlow optional).

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-09-01 | Operators | Fast default answers with sources. |
| STK-09-02 | Domain experts | Multi-hop relational answers when needed. |
| STK-09-03 | Finance / platform | Cost control; avoid expensive re-index on every document. |
| STK-09-04 | Compliance | Every answer cites sources. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|----|------------------|
| FR-09-01 | When a knowledge query arrives, the system shall start retrieval at Tier 0 by default. |
| FR-09-02 | While serving Tier 0, the system shall use vector and/or keyword similarity over chunked documents without mandatory graph expansion. |
| FR-09-03 | When a query requires relationships or multi-hop reasoning, the system shall escalate to Tier 1 graph/entity retrieval. |
| FR-09-04 | Where Tier 1 is enabled, the system shall support incremental updates of entities/relations without full corpus rebuild. |
| FR-09-05 | When a query requires corpus-wide synthesis and Tier 2 is enabled, the system shall use hierarchical summaries built lazily for that corpus. |
| FR-09-06 | The system shall not require GraphRAG-style community summarization as a default indexing path. |
| FR-09-07 | When any tier returns results, the system shall include source citations (documents, experts, events, or decisions). |
| FR-09-08 | If provenance cannot be attached to a hit, then the system shall not treat that hit as a grounded production answer. |
| FR-09-09 | The system shall evaluate retrieval quality separately on context relevance, answer relevance, and faithfulness. |
| FR-09-10 | Where an off-the-shelf RAG front-end is used, the system shall still enforce provenance and tier escalation policy. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-09-01 | Tier 0 queries shall meet a p95 latency target of ≤ 1.5 s for baseline corpora on the reference environment, excluding cold start. |
| NFR-09-02 | At least 80% of production queries shall remain on Tier 0 under normal load assumptions. |
| NFR-09-03 | Tier 1 escalation shall only run when relational cues or explicit multi-hop flags are present. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-09-04 | Retrieval shall enforce ACL/sensitivity filters before returning chunks. |
| NFR-09-05 | Vector indexes shall isolate tenants where multi-tenant mode is enabled. |
| NFR-09-06 | Retrieved content shall remain untrusted data relative to tool authority (cross-ref STRUCT-05). |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-09-01 | Default search returns provenance fields on every hit. |
| AC-09-02 | Multi-hop/relational queries escalate to Tier 1 and return expanded entity links. |
| AC-09-03 | Retrieval evaluation fixtures exist and pass for Tier 0 provenance and Tier 1 multi-hop. |
| AC-09-04 | Documentation states Tier 2 is optional/on-demand. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-02, STRUCT-05, STRUCT-07, STRUCT-08 | STRUCT-11 execution research nodes, STRUCT-16 UI knowledge pages |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-09-01 | Unit: Tier 0 hits include source_refs / provenance. | Automated |
| TV-09-02 | Unit: multi_hop=true triggers Tier 1 expansion. | Automated |
| TV-09-03 | Fixtures under `business/evals/retrieval/`. | Automated |
| TV-09-04 | Latency smoke for Tier 0 on seed corpus. | Performance |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §3.4 Tier 0/1/2 | FR-09-01 … FR-09-06 |
| Always-on provenance | FR-09-07 … FR-09-08 |
| Escalation + evaluation | FR-09-03, FR-09-09, NFR-09-02 |
