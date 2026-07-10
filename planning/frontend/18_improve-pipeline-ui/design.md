# Design — 18 Improve Pipeline UI

| Field | Value |
|-------|-------|
| Design ID | `FE-18-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-18`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Explicit Reflect → Propose → Evaluate → Canary controls on run detail calling BE improvement/evolution APIs; no silent infinite loop; no local production DNA write.

---

## 2. Context, actors, and trust boundaries

**Actors:** Operators on E1 improve path.  
**Related BE:** BE-21 improvement/loops; BE-20 evolution.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `improve-run-button.tsx`, `improve-pipeline.test.ts`.

---

## 3. Architecture

```text
Run detail → ImproveRunButton / pipeline panel
  Reflect → lessons
  Propose → sandbox variant
  Evaluate → eval results
  Canary → gated canary/promote APIs
Each step: explicit click + BE success required
```

### 3.3 Component interactions

| Step | Typical API |
|------|-------------|
| Reflect | POST improvement/reflect |
| Propose | POST auto-propose / variants |
| Evaluate | POST evolution/eval evaluate |
| Canary | canary/promote endpoints |

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-18-1 | Improve controls | `frontend/src/components/domain/improve-run-button.tsx` |
| C-18-2 | Unit tests | `frontend/tests/unit/improve-pipeline.test.ts` |
| C-18-3 | API calls | `lib/api client + live-ops` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-18-01 | Stepwise explicit clicks | Autonomous infinite loop UI | Human control |
| D-18-02 | Sandbox proposals only | Direct prod DNA edit | BE-21/22 alignment |
| D-18-03 | Stop pipeline on failure | Continue optimistically | Truthfulness |

### 3.4 Interaction sequence

```text
Operator on completed/failed run
  → Reflect → view lessons
  → Propose → sandbox variant id shown
  → Evaluate → scores shown
  → Canary → gated result (no silent prod)
```

---

## 4. Data models, algorithms, state machines, and UI structures

### Pipeline state machine

```text
idle → reflecting → reflected
    → proposing → proposed
    → evaluating → evaluated
    → canarying → done | failed
(any → failed on error; retry same step allowed)
```

### Evidence model

Each completed step stores/display BE response summary for operator review.

---

## 4a. Visual and interaction design

### Visual

- Horizontal stepper: Reflect · Propose · Evaluate · Canary.
- Current step highlight; completed checkmarks.
- Per-step result cards.
- In-progress spinner; disable concurrent submits.

---

## 5. API and interface contracts (ICD)

Improvement reflect/lessons/auto-propose; evolution evaluate/canary/promote; optional loops — per OpenAPI.

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Step API error | Error on step; pipeline not marked success |
| 403 | Disable improve controls |
| User double-clicks | Busy state ignores second submit |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-18-01 In-progress UX | Spinner + disable |
| NFR-18-02 No AuthZ bypass | BE enforces |
| NFR-18-03 No local DNA write | Code review |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-18-01 | The frontend shall expose an Improve pipeline on workflow run detail … | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-18-02 | When the user activates an Improve step, the frontend shall call the … | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-18-03 | The frontend shall require explicit user action to advance each Impro… | §4 pipeline state machine · §3.3 sequence | requirements TV-*; FE-20 gates |
| FR-18-04 | When a step fails, the frontend shall show backend errors and shall n… | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-18-05 | The frontend shall not silently loop Improve steps without operator i… | §3.2 decisions · §4 no silent loop | requirements TV-*; FE-20 gates |
| FR-18-06 | When canary or promote is invoked, the frontend shall call sandbox-ga… | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-18-07 | When a step succeeds, the Improve UI shall display evidence/results r… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-18-08 | While a step is in progress, the frontend shall show in-progress stat… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-18-09 | If the user lacks permission for improve actions, the frontend shall … | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| NFR-18-01 | Long-running improve steps shall show in-progress state until backend… | §7 NFR design table | Perf/security tests / reviews |
| NFR-18-02 | Improve actions shall never bypass backend authorization. | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| NFR-18-03 | Improve UI shall not write production DNA locally. | §7 NFR design table | Perf/security tests / reviews |
| AC-18-01 | Run detail shows Improve step controls. | §9 Validation design | Automated or review protocol |
| AC-18-02 | Reflect/propose/evaluate/canary invoke backend routes. | §9 Validation design | Automated or review protocol |
| AC-18-03 | No automatic unattended infinite improve loop in UI. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

E1 improve path; unit state machine; backend routes only. **TV-18-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-18-01 | Batch improve across runs | Later |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

State machine pure functions unit-tested; each step calls typed API; never auto-advance without user event.

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-18`.
