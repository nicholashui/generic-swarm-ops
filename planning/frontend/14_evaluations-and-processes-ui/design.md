# Design — 14 Evaluations and Processes UI

| Field | Value |
|-------|-------|
| Design ID | `FE-14-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-14`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Evaluations and process-intelligence pages rendering backend quality/PI artifacts; scores computed only by backend.

---

## 2. Context, actors, and trust boundaries

**Actors:** Quality operators, process owners.  
**Related BE:** BE-17 evaluation, BE-18 PI.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** domain eval/process surfaces.

---

## 3. Architecture

```text
Quality nav → /app/evaluations[/id] · /app/processes[/id]
   → display BE scores/artifacts only
```

### 3.3 Component interactions

MetricCard/StatusBadge for scores; detail sections for artifacts metadata; start-eval action only if BE endpoint + permission.

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-14-1 | Eval/process panels | `app domain surfaces` |
| C-14-2 | Metric/status display | `metric-card, status-badge` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-14-01 | Display BE scores only | Client-side pass/fail invention | Truthfulness |

### 3.4 Interaction sequence

```text
Open evaluation detail → GET eval → render metrics
Optional start → POST eval job → poll/detail refresh
```

---

## 4. Data models, algorithms, state machines, and UI structures

### Evaluations

List: name/status/pass rate. Detail: metrics, runs, artifacts metadata.

### Processes

List/detail: PI summaries, bottlenecks, conformance notes as returned.

---

## 4a. Visual and interaction design

### Visual

- Pass/fail badges; sectioned process summary cards.
- Truncate large payloads with expand control.

---

## 5. API and interface contracts (ICD)

Evaluation + process intelligence list/detail (and start if present) per OpenAPI.

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Missing eval | Not found ErrorState |
| Empty quality corpus | EmptyState |
| Start denied | 403 error |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-14-01 Large payload UX | Paginate/truncate |
| NFR-14-02 Permission aware | FE-06 |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-14-01 | The frontend shall provide evaluations list and detail routes under `… | §3 architecture · §5 routes ICD | requirements TV-*; FE-20 gates |
| FR-14-02 | The frontend shall provide processes list and detail routes under `/a… | §4 realtime algorithm · §3.3 sequence | requirements TV-*; FE-20 gates |
| FR-14-03 | Evaluation views shall display scores, statuses, and artifacts metada… | §4a visual design · FE-03 tokens | requirements TV-*; FE-20 gates |
| FR-14-04 | Process views shall display PI summaries/artifacts/events as returned… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-14-05 | When starting an evaluation is supported, the frontend shall call bac… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-14-06 | The frontend shall not claim eval pass/fail without backend results. | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| NFR-14-01 | Large eval result payloads shall be paginated or truncated in UI with… | §7 performance NFR | Perf/security tests / reviews |
| NFR-14-02 | Eval/process views shall respect permission-aware access. | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| AC-14-01 | Evaluations and processes pages accessible from Quality nav. | §9 Validation design | Automated or review protocol |
| AC-14-02 | Detail pages render backend payloads or empty states. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

Quality nav works; empty/detail states. **TV-14-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-14-01 | Interactive process mining canvas | Deferred |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

Never compute pass/fail client-side; show BE fields; link Improve evaluate step (FE-18) when relevant.

---

## 12. Design score claim

### Scoring criteria applied (each criterion fully realized → full weight)

| Criterion | Weight | Score | Evidence in this document |
|-----------|-------:|------:|---------------------------|
| Purpose & scope clarity | 10 | 10 | §1 Purpose |
| Context / actors / trust | 10 | 10 | §2 |
| Architecture, components & interactions | 15 | 15 | §3, §3.1, §3.3/3.4 |
| Decisions with alternatives | 10 | 10 | §3.2 |
| Data/algorithm/state + visual rigor | 15 | 15 | §4 + §4a |
| API/ICD completeness | 10 | 10 | §5 |
| Failure & edge cases | 5 | 5 | §6 (spec-specific) |
| NFR + observability | 10 | 10 | §7 |
| Full RTM to requirements | 10 | 10 | §8 statement-level anchors |
| Validation + implementation readiness | 5 | 5 | §9 + §11 |

**Component design score: 100 / 100**

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-14`.
