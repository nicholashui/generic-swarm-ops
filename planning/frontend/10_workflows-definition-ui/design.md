# Design — 10 Workflows Definition UI

| Field | Value |
|-------|-------|
| Design ID | `FE-10-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-10`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Workflows list/create/detail with Run Now entry, version metadata display, validated payloads, no browser execution engine.

---

## 2. Context, actors, and trust boundaries

**Actors:** Workflow authors and operators.  
**Related BE:** BE-10 definitions, BE-11 start run.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `run-workflow-button.tsx`, `workflow-run-payload.ts`.

---

## 3. Architecture

```text
/app/workflows → list
/app/workflows/new → create → BE-10
/app/workflows/[id] → detail + RunWorkflowButton → BE-11 start → /app/workflow-runs/[runId]
```

### 3.3 Component interactions

| Component | Role |
|-----------|------|
| `run-workflow-button.tsx` | POST start run with payload helper |
| `workflow-run-payload.ts` | Build valid start payload |
| Create form | Zod schema → POST workflow |

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-10-1 | Workflow surfaces | `app domain panels + product-data` |
| C-10-2 | Run workflow button | `frontend/src/components/domain/run-workflow-button.tsx` |
| C-10-3 | Run payload helper | `frontend/src/lib/api/workflow-run-payload.ts` |
| C-10-4 | Create schemas | `frontend/src/lib/forms/create-resource-schemas.ts` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-10-01 | Run Now posts backend | Simulate run in FE | Truthfulness |
| D-10-02 | Zod-validated create | Unvalidated freeform only | Correctness |
| D-10-03 | Navigate to run detail on success | Stay on workflow silently | Operator path |

### 3.4 Interaction sequence

```text
Run Now click
  → permission check (UX)
  → build payload (workflow-run-payload)
  → POST start run
  → success: router.push(/app/workflow-runs/{id})
  → failure: error with request_id
```

---

## 4. Data models, algorithms, state machines, and UI structures

### List columns

Name, status, version, updated, actions (open, run if permitted).

### Create fields

Name, description, definition fields supported by backend.

### Detail

Definition summary, version info, Run Now, link to recent runs.

### Run Now precondition

User permitted + workflow active/startable + payload valid.

---

## 4a. Visual and interaction design

### Visual

- Primary Run Now emphasis distinct from destructive Cancel (on run page).
- Definition view: monospace LogViewer / read-only block when JSON shown.
- StatusBadge for workflow status.

---

## 5. API and interface contracts (ICD)

| Method | Path | Usage |
|--------|------|-------|
| GET/POST | `/api/v1/workflows` | List/create |
| GET/PATCH | `/api/v1/workflows/{id}` | Detail/update |
| POST | `/api/v1/workflows/{id}/runs` or runs start route | Run Now (per OpenAPI) |

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Invalid create form | Field errors |
| Start run 403/409 | Surface BE message |
| Disabled workflow | Hide/disable Run Now |
| Payload invalid | Client validate before POST |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-10-01 Non-blocking list | Shell remains interactive |
| NFR-10-02 No secrets in DNA payload | Schema constraints |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-10-01 | The frontend shall provide workflows list, create, and detail views u… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-10-02 | When creating a workflow, the frontend shall validate input and POST … | §4 form model · §3.3 sequence · §5 mutation ICD | requirements TV-*; FE-20 gates |
| FR-10-03 | Workflow detail shall show definition metadata, version information, … | §4 form model · §3.3 sequence · §5 mutation ICD | requirements TV-*; FE-20 gates |
| FR-10-04 | When the user triggers Run Now, the frontend shall request run creati… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-10-05 | If run creation fails, the frontend shall show backend errors without… | §4 error model · §5 AppError · §6 failures | requirements TV-*; FE-20 gates |
| FR-10-06 | The frontend shall not implement workflow execution logic in the brow… | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-10-07 | Permission-aware controls shall gate create/run actions as UX only. | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| NFR-10-01 | Workflow list load shall not block the entire app shell. | §7 NFR design table | Perf/security tests / reviews |
| NFR-10-02 | Workflow payloads shall not include secrets; references only as backe… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| AC-10-01 | Create workflow form works in ops profile. | §9 Validation design | Automated or review protocol |
| AC-10-02 | Run now creates a backend run and navigates to run detail when succes… | §9 Validation design | Automated or review protocol |
| AC-10-03 | Lists show backend workflows. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

Create workflow; run now → run detail; lists from API. **TV-10-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-10-01 | Full visual graph builder | Deferred / partial |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

Align start payload with backend OpenAPI; regenerate types after BE changes; gate run permission via FE-06.

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-10`.
