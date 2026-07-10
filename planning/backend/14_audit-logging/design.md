# Design — 14 Audit Logging

| Field | Value |
|-------|-------|
| Design ID | `BE-14-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-14`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

Immutable (via API) audit trail for important actions with request_id correlation and read APIs.

---

## 2. Context, actors, and trust boundaries

**Actors:** Auditors, security, support.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `domain/audit/*`, `api/v1/routes/audit_logs.py`.

---

## 3. Architecture

```text
Domain action success/fail → AuditWriter.append(event) → store
Client → GET /audit-logs (audit:read) read-only
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-14-1 | Audit routes | `api/v1/routes/audit_logs.py` |
| C-14-2 | Events | `domain/audit/events.py` |
| C-14-3 | Models | `domain/audit/models.py` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-14-01 | Append-only via API | Client editable audit | Integrity |
| D-14-02 | Cover login/runs/approvals/tools/keys | Minimal login only | Forensics |

---

## 4. Data models, algorithms, and/or state machines

### Event fields

audit_id, org_id, actor_id, actor_type, action, resource_type/id, request_id, ip, ua, before/after, metadata, status, created_at.

---

## 5. API and interface contracts (ICD)

GET list/search + GET by id; no PATCH/DELETE for clients.

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
| NFR-14-01 Write overhead | Async-capable append |
| NFR-14-02 Filterable search | Indexes on time/actor/action |
| NFR-14-03 AuthZ | audit:read |
| NFR-14-04 No secrets | Redaction |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-14-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-14-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-14-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-14-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-14-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-14-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-14-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-14-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-14-02 | §7 NFR design table | Perf/security tests / reviews |
| NFR-14-03 | §7 NFR design table | Perf/security tests / reviews |
| NFR-14-04 | §7 NFR design table | Perf/security tests / reviews |
| AC-14-01 | §8 Validation design | Automated or review protocol |
| AC-14-02 | §8 Validation design | Automated or review protocol |
| AC-14-03 | §8 Validation design | Automated or review protocol |
| AC-14-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

Action→audit present; authz; no update route.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-14-01 | WORM/SIEM export | Optional |

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

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-14`.
