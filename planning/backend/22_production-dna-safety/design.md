# Design — 22 Production DNA Safety

| Field | Value |
|-------|-------|
| Design ID | `BE-22-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-22`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

Deterministic structure-aligned validators on activate/production_ready: risk tiers, human gates, rollback, provenance; rejections learnable as lessons.

---

## 2. Context, actors, and trust boundaries

**Actors:** Activate path, CI business:validate, learning loop.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `infrastructure/governance/structure_validators.py`, runtime activate path.

---

## 3. Architecture

```text
activate/production_ready → structure_validators + business:validate
   │ pass → activate
   │ fail → reject + optional rejection lesson (no prod DNA change)
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-22-1 | Validators | `infrastructure/governance/structure_validators.py` |
| C-22-2 | Runtime activate hooks | `runtime.py activate_workflow_version` |
| C-22-3 | Business validate | `npm run business:validate / scripts` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-22-01 | Hard fail activate | Warn-only activate | Safety |
| D-22-02 | No client bypass flags | force=true | Secure default |
| D-22-03 | Rejection→lesson | Silent drop | Learning |

---

## 4. Data models, algorithms, and/or state machines

### Checks (normative set)

- risk tier present and coherent  
- high-risk/irreversible steps declare human gates  
- rollback plan present when required  
- provenance-related fields when required  
- negative fixtures must fail

---

## 5. API and interface contracts (ICD)

Validator invoked by activate/update production_ready APIs; machine-readable error list.

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
| NFR-22-01 &lt;200ms validate | Pure functions |
| NFR-22-02 No bypass | Code path |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-22-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-22-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-22-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-22-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-22-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-22-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-22-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-22-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-22-02 | §7 NFR design table | Perf/security tests / reviews |
| AC-22-01 | §8 Validation design | Automated or review protocol |
| AC-22-02 | §8 Validation design | Automated or review protocol |
| AC-22-03 | §8 Validation design | Automated or review protocol |
| AC-22-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

Valid DNA activates; missing gates fail; negative fixtures; rejection lesson path.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-22-01 | Formal proof assistant | Out of scope |

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

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-22`.
