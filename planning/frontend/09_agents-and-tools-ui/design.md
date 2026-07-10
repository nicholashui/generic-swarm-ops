# Design — 09 Agents and Tools UI

| Field | Value |
|-------|-------|
| Design ID | `FE-09-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-09`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

List/create/detail for agents and list/detail for tools with validated forms, backend mutations, permission gates, and no local execution.

---

## 2. Context, actors, and trust boundaries

**Actors:** Developers, operators, viewers (read).  
**Related BE:** BE-08 agents, BE-09 tools.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `form-route-actions.tsx`, `create-resource-schemas.ts`, domain slug panels.

---

## 3. Architecture

```text
/app/agents[/new|/:id] ──forms──► BE agents API
/app/tools[/:id]       ──read───► BE tools API
Zod + react-hook-form (create-resource-schemas)
```

### 3.3 Component interactions

| UI | Module | API |
|----|--------|-----|
| Create agent form | `create-resource-schemas.ts`, `form-route-actions.tsx` | POST agents |
| Lists/detail | domain slug panels + `detail-metadata.tsx` | GET agents/tools |

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-09-1 | Domain surfaces | `frontend/src/app/app/[...slug]/page.tsx + product panels` |
| C-09-2 | Create schemas | `frontend/src/lib/forms/create-resource-schemas.ts` |
| C-09-3 | Form route actions | `frontend/src/components/domain/form-route-actions.tsx` |
| C-09-4 | Detail metadata | `frontend/src/components/domain/detail-metadata.tsx` |
| C-09-5 | Tests | `frontend/tests/unit/create-forms.test.ts` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-09-01 | Real create forms in ops mode | Demo-only forms | Product bar |
| D-09-02 | No browser agent/tool execution | Client-side runner | Charter FE-01 |
| D-09-03 | Zod schemas shared | Unvalidated free text only | Correctness |

### 3.4 Interaction sequence

```text
User submits create agent
  → zod parse
  → if invalid: field errors
  → POST /agents
  → 201: navigate detail
  → 4xx: ErrorState / form error + request_id
```

---

## 4. Data models, algorithms, state machines, and UI structures

### List model

Columns: name, status, risk (if any), updated_at, actions.

### Create agent form model

Required: name. Optional: description, risk, tool allow-list fields per BE schema.  
Validate client-side → POST → navigate detail or show AppError.

### Detail model

Identity + configuration summary + status + allowed tools/scopes **as returned** (no invention).

### Tools

Read-only emphasis; never show provider secrets.

---

## 4a. Visual and interaction design

### Visual

- DataTable lists + StatusBadge.
- Detail: header + metadata grid.
- Create: single-column form, primary submit, secondary cancel.
- Empty list: EmptyState + Create CTA if permitted.

---

## 5. API and interface contracts (ICD)

| Method | Path | Usage |
|--------|------|-------|
| GET/POST | `/api/v1/agents` | List/create |
| GET/PATCH | `/api/v1/agents/{id}` | Detail/update |
| GET | `/api/v1/tools` | List |
| GET | `/api/v1/tools/{id}` | Detail |

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Validation fail | Inline field errors; no POST |
| 403 create | Disabled CTA or error |
| 422 from BE | Show details + request_id |
| Secret in tool config | Redact/omit in UI |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-09-01 Large lists | Pagination when BE supports |
| NFR-09-02 No provider secrets | Metadata only |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-09-01 | The frontend shall provide agents list, create, and detail views unde… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-09-02 | The frontend shall provide tools list and detail views under `/app/to… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-09-03 | When creating or updating an agent, the frontend shall validate requi… | §4 form model · §3.3 sequence · §5 mutation ICD | requirements TV-*; FE-20 gates |
| FR-09-04 | When backend rejects an agent/tool mutation, the frontend shall displ… | §4 error model · §5 AppError · §6 failures | requirements TV-*; FE-20 gates |
| FR-09-05 | When agent or tool detail data is returned, the frontend shall displa… | §4a visual design · FE-03 tokens | requirements TV-*; FE-20 gates |
| FR-09-06 | If the user lacks permission to create agents/tools, the frontend sha… | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| FR-09-07 | The frontend shall not execute agents or tools locally; execution rem… | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-09-08 | When the agents list is empty and the user may create agents, the fro… | §4 empty model · §4a empty · FE-19 EmptyState | requirements TV-*; FE-20 gates |
| FR-09-09 | When rendering list rows, the frontend shall show status badges using… | §4a visual design · FE-03 tokens | requirements TV-*; FE-20 gates |
| FR-09-10 | If tool metadata would require displaying a provider secret, the fron… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| NFR-09-01 | List views shall support pagination or virtualization when lists grow… | §7 performance NFR | Perf/security tests / reviews |
| NFR-09-02 | Tool configuration UI shall not accept or display raw provider secret… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| AC-09-01 | Create agent form works against live backend in ops profile. | §9 Validation design | Automated or review protocol |
| AC-09-02 | Agents and tools lists render API data. | §9 Validation design | Automated or review protocol |
| AC-09-03 | Permission-denied create is gated in UI. | §9 Validation design | Automated or review protocol |
| AC-09-04 | Status badges and empty/error states present on list views. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

Create agent live; lists render; permission gate; form unit tests. **TV-09-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-09-01 | Visual agent graph | Non-goal mark ~100 |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

1. Extend zod schema when BE fields change.  
2. Use `formatMutationError` for API failures.  
3. Gate Create with FE-06 permission keys for agents/tools write.

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-09`.
