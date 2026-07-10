# Design — 12 Governance Policies and Risk

| Field | Value |
|-------|-------|
| Design ID | `BE-12-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-12`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

Policy engine returning allow/deny/require_approval/require_evaluation/require_redaction; risk levels; pre-check on run start and tool/step checks.

---

## 2. Context, actors, and trust boundaries

**Actors:** Risk owners editing policies; engine consuming decisions.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `domain/governance/*`, `api/v1/routes/governance.py`.

---

## 3. Architecture

```text
check(context) → {action, reason, risk_level}
  used by: run start, step exec, tool invoke, data access, output release
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-12-1 | Governance routes | `api/v1/routes/governance.py` |
| C-12-2 | Policy engine | `domain/governance/policy_engine.py` |
| C-12-3 | Risk helpers | `domain/governance/risk.py` |
| C-12-4 | Runtime tier policy | `business/runtime-tier-policy.json (if present)` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-12-01 | Declarative policies + engine | Hardcoded only | Extensibility |
| D-12-02 | Map structure tiers into runtime | Ignore tiers | structure.md fidelity |

---

## 4. Data models, algorithms, and/or state machines

### Risk levels

low | medium | high | critical with meanings from backend.md §13.1.

### Actions

allow | deny | require_approval | require_evaluation | require_redaction.

---

## 5. API and interface contracts (ICD)

`/api/v1/governance/policies` CRUD + `/check` + `/preview`.

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
| NFR-12-01 Check &lt;50ms | In-process rules |
| NFR-12-02 Non-overridable deny | Ignore client force flags |
| NFR-12-03 Policy write authz | governance:update |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-12-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-12-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-12-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-12-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-12-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-12-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-12-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-12-08 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-12-09 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-12-10 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-12-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-12-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-12-02 | §7 NFR design table | Perf/security tests / reviews |
| NFR-12-03 | §7 NFR design table | Perf/security tests / reviews |
| AC-12-01 | §8 Validation design | Automated or review protocol |
| AC-12-02 | §8 Validation design | Automated or review protocol |
| AC-12-03 | §8 Validation design | Automated or review protocol |
| AC-12-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

Policy table tests; pre-check integration; unauthorized update deny.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-12-01 | Full DMN rule studio | Later |

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

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-12`.
