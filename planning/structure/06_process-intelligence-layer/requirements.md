# 06 — Process Intelligence Layer

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-06` |
| Source | `structure.md` §2.3 |
| Priority order | 06 |
| Status | Specification |
| Owner | Process Mining + Ops Analytics |

---

## 1. Scope

### 1.1 In scope
- Learning from operational traces (tickets, CRM/ERP, calendar, email, approvals, file edits, API calls, completions).
- Event log schema and ingestion.
- Process mining outputs: discovered processes, conformance, bottlenecks, causal improvement hypotheses.
- Roles of Process Miner, Task Mining, Conformance, Bottleneck Analyzer, Causal Improvement agents (logical services).

### 1.2 Out of scope
- Full enterprise connector suite for every source system.
- UI task mining browser extensions (may be later).

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-06-01 | Operations | Evidence of how work actually happens. |
| STK-06-02 | Process owners | Conformance vs SOPs and bottleneck visibility. |
| STK-06-03 | Evolution manager | Causal hypotheses as sandbox experiment inputs. |
| STK-06-04 | Auditor | Structured event logs with risk and approval fields. |

---

## 3. Functional Requirements (EARS)

### 3.1 Event capture

| ID | Statement (EARS) |
|----|------------------|
| FR-06-01 | The system shall accept operational events from tickets, CRM/ERP actions, calendar, email, approvals, file edits, API calls, and completion records where connectors exist. |
| FR-06-02 | When an event is ingested, the system shall validate required fields of the event log schema including id, timestamp, actor, process, case, and activity. |
| FR-06-03 | When an event is a decision point, the system shall capture decision reason summary, confidence, risk tier, and human approval status where applicable. |
| FR-06-04 | When an event completes, the system shall store outcome status, latency, and quality score when provided. |

### 3.2 Mining and analysis

| ID | Statement (EARS) |
|----|------------------|
| FR-06-05 | When sufficient events exist for a process, the process miner capability shall produce discovered workflow models. |
| FR-06-06 | Where UI/human observation is permitted, the task mining capability shall record permitted human-level step traces. |
| FR-06-07 | When SOPs exist for a process, the conformance capability shall compare observed work against documented SOPs. |
| FR-06-08 | The bottleneck analyzer shall identify delays, loops, rework, and handoff failures from event data. |
| FR-06-09 | The causal improvement capability shall propose interventions that may improve outcomes without applying them to production DNA. |

### 3.3 Artifacts and handoff

| ID | Statement (EARS) |
|----|------------------|
| FR-06-10 | When process-intelligence analysis completes, the system shall write artifacts under `business/process-intelligence/`. |
| FR-06-11 | When causal hypotheses are generated, the system shall route them only as inputs to evaluation or evolution sandbox pathways. |
| FR-06-12 | If event schema validation fails, then the system shall reject or quarantine the event and record the failure. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-06-01 | Single-event ingest validation shall complete in under 100 ms excluding storage I/O contention. |
| NFR-06-02 | Batch analysis for baseline sample logs shall complete within 5 minutes on a developer machine. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-06-03 | Event logs shall respect sensitivity and access controls when exposed via APIs. |
| NFR-06-04 | PII in event logs shall be minimised or protected per data-retention policy. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-06-01 | Event schema example validates against published schema. |
| AC-06-02 | Ingest path produces discovered/conformance/bottleneck artifacts (or equivalent structured outputs). |
| AC-06-03 | Process summary APIs expose metrics and bottlenecks for operators. |
| AC-06-04 | Causal outputs do not mutate production workflow DNA. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-02, STRUCT-04 | STRUCT-13 evaluation, STRUCT-14 evolution, STRUCT-11 (case evidence) |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-06-01 | Schema validation of sample events. | Automated |
| TV-06-02 | Ingest → artifact write integration test. | Automated |
| TV-06-03 | API: process summary / bottlenecks non-empty after seed. | Automated |
| TV-06-04 | Negative: invalid event rejected. | Automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §2.3 agents | FR-06-05 … FR-06-09 |
| §2.3 event schema | FR-06-02 … FR-06-04 |
| Shadow Mode empirical learning | FR-06-01, FR-06-10 |
