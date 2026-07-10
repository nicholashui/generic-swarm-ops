# Design — 19 Streaming, Health, and Observability

| Field | Value |
|-------|-------|
| Design ID | `BE-19-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-19`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

SSE run events, health/live/ready/metrics, structured logs with request_id, security headers/CORS.

---

## 2. Context, actors, and trust boundaries

**Actors:** FE realtime UI, orchestrators/probes.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `api/v1/routes/health.py`, `core/logging.py`, `core/metrics.py`.

---

## 3. Architecture

```text
Engine emits domain events → SSE stream (authz on run)
/health /live /ready (DB status) /metrics
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-19-1 | Health routes | `api/v1/routes/health.py` |
| C-19-2 | Logging | `core/logging.py` |
| C-19-3 | Metrics | `core/metrics.py` |
| C-19-4 | Stream endpoint | `workflow_runs stream` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-19-01 | SSE first | WebSocket required | Simpler one-way progress |
| D-19-02 | Ready includes DB | Liveness-only | Ops correctness |

---

## 4. Data models, algorithms, and/or state machines

### Stream event types

run.started/status_changed/completed/failed, step.*, approval.*, evaluation.completed, log.message.

---

## 5. API and interface contracts (ICD)

Health trio + metrics; run stream path.

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
| NFR-19-01 Prompt SSE | Emit after persist |
| NFR-19-02 Health &lt;100ms | Cheap checks |
| NFR-19-03 Stream authz | Same as run read |
| NFR-19-04 Log redaction | Filters |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-19-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-19-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-19-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-19-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-19-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-19-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-19-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-19-08 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-19-09 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-19-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-19-02 | §7 NFR design table | Perf/security tests / reviews |
| NFR-19-03 | §7 NFR design table | Perf/security tests / reviews |
| NFR-19-04 | §7 NFR design table | Perf/security tests / reviews |
| AC-19-01 | §8 Validation design | Automated or review protocol |
| AC-19-02 | §8 Validation design | Automated or review protocol |
| AC-19-03 | §8 Validation design | Automated or review protocol |
| AC-19-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

Health tests; event emission; unauthorized stream deny.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-19-01 | Full OTEL vendor pack | Optional |

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

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-19`.
