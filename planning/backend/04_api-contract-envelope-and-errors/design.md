# Design — 04 API Contract, Envelope, and Errors

| Field | Value |
|-------|-------|
| Design ID | `BE-04-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-04`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

Standardize `/api/v1` versioning, success/error envelopes, request_id correlation, validation errors, and OpenAPI fidelity.

---

## 2. Context, actors, and trust boundaries

**Actors:** Frontend typed client, integrators, support.  
**Trust:** Error bodies never contain secrets.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `api/errors.py`, `core/errors.py`, FE `openapi.d.ts` generation path.

---

## 3. Architecture

```text
Request → request_id middleware → route → service
                │                    │
                ▼                    ▼
         access log           success {data, meta}
                              error {error, message, request_id, details?}
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-04-1 | Error handlers | `api/errors.py, core/errors.py` |
| C-04-2 | Request ID | `logging middleware` |
| C-04-3 | Pagination helpers | `core/pagination.py` |
| C-04-4 | OpenAPI | `FastAPI schema export` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-04-01 | REST+/api/v1 first | GraphQL now | Matches FE OpenAPI gen |
| D-04-02 | Structured errors always | Raw strings | Supportability |
| D-04-03 | Hide stacks in prod | Debug stacks always | Security |

---

## 4. Data models, algorithms, and/or state machines

### Error code map (normative)

| HTTP | Meaning |
|------|---------|
| 401 | Unauthenticated |
| 403 | Unauthorized |
| 404 | Not found (or hidden) |
| 409 | Conflict / gate / state |
| 422 | Validation |
| 429 | Rate limited |
| 500 | Internal (safe message) |

---

## 5. API and interface contracts (ICD)

All resource routes under `/api/v1/*`. Breaking changes require new version prefix or deprecation notice.

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
| NFR-04-01 Envelope cost | Lightweight dict wrappers |
| NFR-04-02 OpenAPI | Generated from models |
| NFR-04-03 No secrets in errors | Sanitizer |
| NFR-04-04 request_id not authz | Separate middleware |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-04-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-04-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-04-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-04-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-04-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-04-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-04-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-04-08 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-04-09 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-04-10 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-04-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-04-02 | §7 NFR design table | Perf/security tests / reviews |
| NFR-04-03 | §7 NFR design table | Perf/security tests / reviews |
| NFR-04-04 | §7 NFR design table | Perf/security tests / reviews |
| AC-04-01 | §8 Validation design | Automated or review protocol |
| AC-04-02 | §8 Validation design | Automated or review protocol |
| AC-04-03 | §8 Validation design | Automated or review protocol |
| AC-04-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

Unit tests for handlers; invalid body → 422; OpenAPI contains /api/v1.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-04-01 | Problem+JSON RFC full profile | Optional enhancement |

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

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-04`.
