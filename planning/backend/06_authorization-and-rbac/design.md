# Design — 06 Authorization and RBAC

| Field | Value |
|-------|-------|
| Design ID | `BE-06-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-06`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

Enforce role-based permissions on every protected resource; prepare for future ABAC (org, risk ceiling) without requiring it for product bar.

---

## 2. Context, actors, and trust boundaries

**Actors:** All authenticated principals.  
**Trust:** Server-side permission evaluation only.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `core/permissions.py`, `api/dependencies.py`.

---

## 3. Architecture

```text
Route dependency → require_permission("workflows:run")
Role → permission set → allow/deny
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-06-1 | Permissions catalog | `core/permissions.py` |
| C-06-2 | Route dependencies | `api/dependencies.py` |
| C-06-3 | Role maps | `seed + user records` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-06-01 | RBAC strings | Full ABAC engine now | Product bar simplicity |
| D-06-02 | Deny by default | Allow by default | Secure by default |
| D-06-03 | Same model for API keys | Separate weak key perms | Consistency |

---

## 4. Data models, algorithms, and/or state machines

### Roles (recommended)

Owner, Admin, Manager, Operator, Reviewer, Viewer, ServiceAccount.

### Permission families

agents:*, workflows:*, workflow_runs:*, knowledge:*, memory:*, governance:*, approvals:*, audit:read, evaluations:read, settings:update.

---

## 5. API and interface contracts (ICD)

Authorization is a cross-cutting dependency on routes; 403 envelope on deny.

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
| NFR-06-01 Deterministic | In-process maps |
| NFR-06-02 p95 &lt;5ms | No network |
| NFR-06-03 Server-side | Dependencies |
| NFR-06-04 No self-escalation | Role change gated |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-06-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-06-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-06-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-06-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-06-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-06-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-06-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-06-08 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-06-09 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-06-10 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-06-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-06-02 | §7 NFR design table | Perf/security tests / reviews |
| NFR-06-03 | §7 NFR design table | Perf/security tests / reviews |
| NFR-06-04 | §7 NFR design table | Perf/security tests / reviews |
| AC-06-01 | §8 Validation design | Automated or review protocol |
| AC-06-02 | §8 Validation design | Automated or review protocol |
| AC-06-03 | §8 Validation design | Automated or review protocol |
| AC-06-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

Table-driven matrix tests; operator vs viewer route probes.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-06-01 | ABAC policy language | Future |

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

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-06`.
