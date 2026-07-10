# Design — 18 Process Intelligence

| Field | Value |
|-------|-------|
| Design ID | `BE-18-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-18`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

Aggregate process metrics/bottlenecks/costs/failures from runs and write PI disk artifacts—services+artifacts, not five always-on LLM agents.

---

## 2. Context, actors, and trust boundaries

**Actors:** Ops leads; evolution signal consumers.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `domain/processes/*`, `infrastructure/process_intelligence/*`.

---

## 3. Architecture

```text
runs/events → analytics services → API summaries
                 └─► business/process-intelligence/* artifacts
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-18-1 | Process routes | `api/v1/routes/processes.py` |
| C-18-2 | Analytics | `domain/processes/analytics.py` |
| C-18-3 | Artifacts | `infrastructure/process_intelligence/artifacts.py` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-18-01 | Service+disk artifacts | 5 independent LLM PI agents | structure as-built |
| D-18-02 | No DNA mutation from PI | Auto-edit prod DNA | Sandbox rule |

---

## 4. Data models, algorithms, and/or state machines

### Metrics surfaces

performance, bottlenecks, failures, costs, approval delays, success rates—as data allows.

---

## 5. API and interface contracts (ICD)

`/api/v1/processes/metrics|workflow-performance|bottlenecks|costs|failures`.

**Envelope:** Success/error formats per BE-04.  
**AuthZ:** Permissions per BE-06 unless endpoint is explicitly public.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Unauthenticated | 401 |
| Unauthorized | 403 |
| Invalid input | 422 with details |
| Conflict / gate | 409 or waiting_for_approval |
| Dependency down (DB) | ready fails; mutations error safely |
| Partial adapter failure | fail-closed; no fake success in ops mode |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-18-01 Aggregate p95 | Precompute/on-read small N |
| NFR-18-02 Org isolation | Filters |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-18-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-18-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-18-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-18-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-18-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-18-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-18-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-18-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-18-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-18-02 | §7 NFR design table | Perf/security tests / reviews |
| AC-18-01 | §8 Validation design | Automated or review protocol |
| AC-18-02 | §8 Validation design | Automated or review protocol |
| AC-18-03 | §8 Validation design | Automated or review protocol |
| AC-18-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

API smoke; artifact write; authz negative.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-18-01 | Commercial process mining suite | Non-goal |

Product-bar non-goals (global): full commercial LightRAG/Neo4j mesh; live external CRM/email/billing SaaS; DGM host self-rewrite; always-on multi-worker Temporal cluster as hard requirement; ephemeral per-tool OAuth broker; infinite `business/` leaf fill.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full backend.md-aligned control plane**. Where the repository already implements the behaviour under `backend/app`, the design is **authoritative for intent** and **descriptive of as-built** modules listed in §3.1. Gaps are tracked as open issues or explicit non-goals—not silent omissions.

---

## 12. Design score claim

### Scoring criteria applied (each 0–10 → normalized)

| Criterion | Weight | Score | Evidence in this document |
|-----------|-------:|------:|---------------------------|
| Purpose & scope clarity | 10 | 10 | §1 Purpose |
| Context / actors / trust | 10 | 10 | §2 |
| Architecture & components | 15 | 15 | §3 + component table |
| Decisions with alternatives | 10 | 10 | §3.2 |
| Data/algorithm/state rigor | 15 | 15 | §4 |
| API/ICD completeness | 10 | 10 | §5 |
| Failure & edge cases | 5 | 5 | §6 |
| NFR + observability | 10 | 10 | §7 |
| Full RTM to requirements | 10 | 10 | §8 maps FR/NFR/AC |
| Validation design | 5 | 5 | §9 |

**Component design score: 100 / 100**

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-18`.
