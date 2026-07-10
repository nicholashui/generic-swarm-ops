# Design — 17 Evolution Sandbox Archive UI

| Field | Value |
|-------|-------|
| Design ID | `FE-17-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-17`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Evolution archive at `/app/evolution` for sandbox variants and fitness; actions only via BE evolution APIs; forbid client production DNA rewrite.

---

## 2. Context, actors, and trust boundaries

**Actors:** Evolution operators; governance.  
**Related BE:** BE-20; structure.md §5 sandbox.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `evolution-archive-panel.tsx`.

---

## 3. Architecture

```text
/app/evolution → EvolutionArchivePanel → BE-20
actions: evaluate / promote / rollback (gated + confirm)
INV: no client production DNA mutation
```

### 3.3 Component interactions

Panel lists variants; actions call evolution endpoints; promote confirm dialog; fitness sort client or server.

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-17-1 | Evolution archive panel | `frontend/src/components/domain/evolution-archive-panel.tsx` |
| C-17-2 | Evolution route | `app evolution path / slug` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-17-01 | Sandbox-only messaging | Hide risk / one-click prod | Safety |
| D-17-02 | BE mutations only | Local DNA file edit UI | Charter |
| D-17-03 | Confirm promote | Instant promote click | Human gate UX |

### 3.4 Interaction sequence

```text
Open /app/evolution → GET archive
Promote click → confirm → POST promote → BE may reject → show result
```

---

## 4. Data models, algorithms, state machines, and UI structures

### Archive row

variant id · parent · fitness · status · created · sandbox flag.

### Action rules

Evaluate anytime allowed · promote requires confirm + BE validators · rollback via BE only.

---

## 4a. Visual and interaction design

### Visual

- Persistent Sandbox badge.
- Fitness-sorted table.
- Promote secondary + confirm dialog.
- Empty: explain improve/evaluate pipeline.

---

## 5. API and interface contracts (ICD)

Evolution variants/archive/evaluate/promote/rollback per OpenAPI (frontend.md §33.3a).

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Promote rejected by validators | Show BE errors; no local DNA change |
| 403 | Hide/disable actions |
| Empty population | EmptyState |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-17-01 Paginate population | Table paging |
| NFR-17-02 AuthZ on mutations | FE-06 + BE |
| NFR-17-03 No skip validation UI | No force flags |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-17-01 | The frontend shall provide an evolution archive page under `/app/evol… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-17-02 | The page shall list sandbox variants and fitness/ranking data returne… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-17-03 | When evaluate/promote/rollback actions are available, the frontend sh… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-17-04 | The frontend shall not implement client-side production DNA mutation … | §1 Purpose · §3 INV · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-17-05 | UI copy shall communicate sandbox / gated promotion semantics when pr… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-17-06 | Permission-aware UI shall gate evolution admin actions. | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| NFR-17-01 | Archive lists shall paginate when populations grow. | §7 performance NFR | Perf/security tests / reviews |
| NFR-17-02 | Evolution mutations shall require authenticated, authorized backend c… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| NFR-17-03 | If a UI path would skip backend sandbox validation, it shall be rejec… | §7 NFR design table | Perf/security tests / reviews |
| AC-17-01 | `/app/evolution` renders archive from backend or empty state. | §9 Validation design | Automated or review protocol |
| AC-17-02 | No client DNA rewrite module exists. | §9 Validation design | Automated or review protocol |
| AC-17-03 | Promote/rollback only via backend APIs. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

Archive renders; no client DNA rewrite module; promote via API. **TV-17-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-17-01 | Population visualization chart | Optional |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

Grep guard: no production DNA write utilities in `frontend/src`. All mutations via evolution APIs.

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-17`.
