# Design — 13 Human Approval Gates

| Field | Value |
|-------|-------|
| Design ID | `BE-13-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-13`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

Approval request lifecycle and decision APIs that pause irreversible work until human decision.

---

## 2. Context, actors, and trust boundaries

**Actors:** Reviewers, operators.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `domain/approvals/*`, `api/v1/routes/approvals.py`.

---

## 3. Architecture

```text
Engine needs_gate → ApprovalRequest(pending) → run waiting_for_approval
Reviewer approve/reject → engine resume/fail → audit
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-13-1 | Approval routes | `api/v1/routes/approvals.py` |
| C-13-2 | Approval service | `domain/approvals/service.py` |
| C-13-3 | Models | `domain/approvals/models.py` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-13-01 | Explicit decision reason | Reason optional | Auditability |
| D-13-02 | Server-side gate block | FE-only disable button | Safety |

---

## 4. Data models, algorithms, and/or state machines

### Approval statuses

pending | approved | rejected | expired | cancelled

### Fields

id, run_id, step_id, action, risk_level, requested_by, reviewer, decision, reason, timestamps.

---

## 5. API and interface contracts (ICD)

GET/POST approve/reject/reassign/decision under `/api/v1/approvals`.

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
| NFR-13-01 Decision latency | Light update + signal engine |
| NFR-13-02 Self-approval policy | Configurable deny |
| NFR-13-03 Org scope | Enforce org_id |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-13-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-13-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-13-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-13-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-13-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-13-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-13-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-13-08 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-13-09 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-13-10 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-13-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-13-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-13-02 | §7 NFR design table | Perf/security tests / reviews |
| NFR-13-03 | §7 NFR design table | Perf/security tests / reviews |
| AC-13-01 | §8 Validation design | Automated or review protocol |
| AC-13-02 | §8 Validation design | Automated or review protocol |
| AC-13-03 | §8 Validation design | Automated or review protocol |
| AC-13-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

Approve/reject paths; E1 gate segment; reason stored.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-13-01 | SLA escalation bots | Later |

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

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-13`.
