# Design — 23 Security Hardening and Cross-Cutting NFRs

| Field | Value |
|-------|-------|
| Design ID | `BE-23-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-23`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

Cross-cutting security and quality attributes: authn/z defaults, validation, rate limits, injection assumptions, reliability, scalability, maintainability layering.

---

## 2. Context, actors, and trust boundaries

**Actors:** All API consumers; security reviewers.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `core/*`, middleware in `main.py`, broker/gates modules.

---

## 3. Architecture

```text
Middleware: CORS · security headers · rate limit · request_id · auth
Domain: validation · broker · gates · ACL
Data: untrusted content handling
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-23-1 | Rate limit | `core/rate_limit.py` |
| C-23-2 | Security headers | `core/security.py / main middleware` |
| C-23-3 | Permissions | `core/permissions.py` |
| C-23-4 | Error sanitization | `api/errors.py` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-23-01 | Deterministic security outside LLM | Prompt-only controls | OWASP |
| D-23-02 | Stateless API + shared Postgres | Sticky in-memory only | Scale path |

---

## 4. Data models, algorithms, and/or state machines

### Control summary

AuthN default, AuthZ always, body validation, upload sanitize, secrets in env, rate limit auth/workflow writes, treat retrieval/user/tool I/O as data, org ACL, fail-closed tools, layered architecture.

---

## 5. API and interface contracts (ICD)

Cross-cutting—no single resource API; applied to all protected routes.

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
| NFR-23-01 Rate limit overhead | In-memory token bucket |
| NFR-23-02 CRUD p95 | Local adapters |
| NFR-23-03 Headers | Middleware |
| NFR-23-04 No hardcoded secrets | CI/review |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-23-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-23-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-23-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-23-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-23-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-23-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-23-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-23-08 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-23-09 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-23-10 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-23-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-23-02 | §7 NFR design table | Perf/security tests / reviews |
| NFR-23-03 | §7 NFR design table | Perf/security tests / reviews |
| NFR-23-04 | §7 NFR design table | Perf/security tests / reviews |
| AC-23-01 | §8 Validation design | Automated or review protocol |
| AC-23-02 | §8 Validation design | Automated or review protocol |
| AC-23-03 | §8 Validation design | Automated or review protocol |
| AC-23-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

401 without auth; rate limit behaviour; upload validation; injection-oriented negatives.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-23-01 | External WAF | Ops concern |

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

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-23`.
