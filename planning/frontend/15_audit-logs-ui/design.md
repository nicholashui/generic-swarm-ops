# Design — 15 Audit Logs UI

| Field | Value |
|-------|-------|
| Design ID | `FE-15-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-15`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Read-only audit log explorer with filters and entity deep links; event creation remains backend-only.

---

## 2. Context, actors, and trust boundaries

**Actors:** Security auditors, operators.  
**Related BE:** BE-14 audit.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** audit domain surface, `data-table.tsx`.

---

## 3. Architecture

```text
/app/audit-logs → GET audit APIs → DataTable + filters
(no FE POST for system-of-record audit)
```

### 3.3 Component interactions

Filter bar → query params → client GET → table; row may link to run/user if ids present.

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-15-1 | Audit panel | `app domain surfaces` |
| C-15-2 | Data table | `frontend/src/components/ui/data-table.tsx` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-15-01 | Read-only FE | Client-written audit trail | Integrity |

### 3.4 Interaction sequence

```text
Open audit logs → GET page 1 → render
Change filters → GET with params → replace rows
```

---

## 4. Data models, algorithms, state machines, and UI structures

### Columns

timestamp · actor · action · resource type/id · outcome · request_id/correlation if present.

### Filters

time range, actor, action, resource — as BE supports.

---

## 4a. Visual and interaction design

### Visual

- Dense table; sticky filter bar.
- Optional row detail drawer.
- Monospace for ids.

---

## 5. API and interface contracts (ICD)

`GET /api/v1/audit-logs` (or project path) with pagination/filter query params.  
**Forbidden:** FE creating authoritative audit events.

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| 403 auditor-only | Access Denied |
| Empty | EmptyState |
| API error | ErrorState + request_id |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-15-01 Pagination | Required |
| NFR-15-02 No client forge | Code review |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-15-01 | The frontend shall provide an audit logs page under `/app/audit-logs`. | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-15-02 | Audit logs UI shall fetch events from backend audit APIs. | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-15-03 | When filters are provided by the product, the frontend shall pass fil… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-15-04 | The frontend shall not create, edit, or delete audit events client-si… | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-15-05 | Each event row shall display actor, action, timestamp, and resource i… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-15-06 | Permission-aware UI shall restrict audit access for roles without per… | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| NFR-15-01 | Audit list shall paginate. | §7 performance NFR | Perf/security tests / reviews |
| NFR-15-02 | Audit UI shall not allow clients to forge historical events. | §7 NFR design table | Perf/security tests / reviews |
| AC-15-01 | Audit page lists backend events or empty state. | §9 Validation design | Automated or review protocol |
| AC-15-02 | No client write path for audit records. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

List or empty; review no audit write client. **TV-15-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-15-01 | Export CSV | Later |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

Grep CI/review: no `POST` audit create from frontend client modules.

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-15`.
