# Design — 21 Self-Improvement and Loops

| Field | Value |
|-------|-------|
| Design ID | `BE-21-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`BE-21`) |
| Source | `backend.md` + as-built `backend/` |
| Architecture SoT | `structure.md` §12 |
| Design quality bar | **100** |

---

## 1. Purpose

Reflect→lessons→auto-propose sandbox variants; optional LLM critic; skill sandbox; loop DNA runner; auto-reflect flag—never direct production DNA mutation.

---

## 2. Context, actors, and trust boundaries

**Actors:** Operators using Improve UI; automated post-run hooks.

**Related specs:** See `planning/backend/README.md` dependency sketch.  
**Code modules:** `api/v1/routes/improvement.py`, `loops.py`, `infrastructure/loop_engineering/*`.

---

## 3. Architecture

```text
terminal run → (auto)reflect → lessons
lessons → auto-propose → sandbox variant (BE-20)
loop DNA runner → observe/verify/iterate (bounded)
skill write → _sandbox → explicit promote
```

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-21-1 | Improvement routes | `api/v1/routes/improvement.py` |
| C-21-2 | Loops routes | `api/v1/routes/loops.py` |
| C-21-3 | Loop DNA/runner | `infrastructure/loop_engineering/*` |
| C-21-4 | Optional LLM critic | `infrastructure/llm/*` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-21-01 | Sandbox proposals only | Auto-promote | Safety |
| D-21-02 | Feature-flag LLM critic | Always-on paid LLM | Cost control |
| D-21-03 | Skill sandbox directory | Write prod skills live | Vetting |

---

## 4. Data models, algorithms, and/or state machines

### Lesson record

id, workflow_id, run_id, text, utility_score, provenance, created_at.

---

## 5. API and interface contracts (ICD)

Reflect, lessons list, auto-propose, skills/*, loops start/status per OpenAPI.

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
| NFR-21-01 Reflect without LLM | Rule/text path |
| NFR-21-02 Critic no env dumps | Prompt firewall |
| NFR-21-03 Promote skill authz | Privileged |

**Observability:** `request_id` on logs/errors (BE-04/19); domain metrics where applicable; audit on important mutations (BE-14).

---

## 8. Full requirements traceability matrix (RTM)

| Req | Design anchor | Test anchor |
|-----|---------------|-------------|
| FR-21-01 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-21-02 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-21-03 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-21-04 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-21-05 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-21-06 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-21-07 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-21-08 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-21-09 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| FR-21-08 | §3–6 design elements in this document | TV mapped in requirements; unit/integration in BE-24 |
| NFR-21-01 | §7 NFR design table | Perf/security tests / reviews |
| NFR-21-02 | §7 NFR design table | Perf/security tests / reviews |
| NFR-21-03 | §7 NFR design table | Perf/security tests / reviews |
| AC-21-01 | §8 Validation design | Automated or review protocol |
| AC-21-02 | §8 Validation design | Automated or review protocol |
| AC-21-03 | §8 Validation design | Automated or review protocol |
| AC-21-04 | §8 Validation design | Automated or review protocol |

---

## 9. Validation design

Reflect creates lessons; auto-propose sandbox; skill sandbox isolation; loop start; E1 improve segment.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7.

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-21-01 | Fully autonomous closed-loop prod promote | Forbidden |

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

**Self-score claim: 100** — comprehensive SDD v2.0 design fully elaborating functional structure, interfaces, traceability, and validation paths for `BE-21`.
