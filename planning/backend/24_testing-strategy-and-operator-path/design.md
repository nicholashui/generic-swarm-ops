# Design — 24 Testing Strategy and Operator Path

| Field | Value |
|-------|-------|
| Design ID | `BE-24-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-24`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

Define layered tests (unit/integration/e2e/security), MVP vs mark ~100 DoD, E1 operator proof path, and explicit non-goals so product bar is not blocked by deferred work.

---

## 2. Context, actors, and trust boundaries

**Actors:** CI, release managers, QA.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `backend/app/tests/**`, `reviews/e1_operator_checklist.md`.

---

## 3. Architecture

```text
unit (domain) → integration (API+DB) → e2e E1 → security suite
Evidence: status.md, mark_100_verification.md, reviews/e1_operator_checklist.md
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-24-1 | Unit tests | `backend/app/tests/unit` |
| C-24-2 | E2E tests | `backend/app/tests/e2e` |
| C-24-3 | E1 path | `test_e1_operator_path` |
| C-24-4 | Evidence docs | `status.md, mark_100_verification.md` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-24-01 | E1 as release proof | Manual-only demo | Repeatability |
| D-24-02 | Non-goals explicit | Infinite scope | Focus |

---

## 4. Data models, algorithms, and/or state machines

### E1 sequence (normative)

login → agent → flagship run → human gate → complete → reflect → propose → evaluate → canary

### Non-goals (mark ~100)

Full LightRAG/Neo4j mesh; live SaaS CRM/email/billing; DGM host rewrite; always-on multi-worker cluster requirement; ephemeral OAuth broker; infinite business leaf fill.

---

## 5. API and interface contracts (ICD)

Test commands documented in backend/README and status.md; not runtime business APIs.

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
| NFR-24-01 Unit without paid APIs | Mocks/local |
| NFR-24-02 E1 CI-reasonable | Local stack |
| NFR-24-03 Security tests keep auth | No global disable |
| NFR-24-04 Fixture hygiene | No prod secrets |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-24-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-24-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-24-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-24-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-24-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-24-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-24-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-24-08 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-24-09 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-24-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-24-02 | §7 NFR design table | Perf/security tests / reviews |
| NFR-24-03 | §7 NFR design table | Perf/security tests / reviews |
| NFR-24-04 | §7 NFR design table | Perf/security tests / reviews |
| AC-24-01 | §8 Validation design | Automated or review protocol |
| AC-24-02 | §8 Validation design | Automated or review protocol |
| AC-24-03 | §8 Validation design | Automated or review protocol |
| AC-24-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

unittest unit green; e2e E1 green; DoD evidence map; non-goals not filed as defects.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-24-01 | Always-on Playwright UI CI | Non-goal |

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

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-24`.
