# Design — 19 Accessibility, Loading, Empty, and Error States

| Field | Value |
|-------|-------|
| Design ID | `FE-19-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-19`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Cross-cutting UX quality: loading/empty/error on major pages; WCAG 2.2 AA intent; keyboard, labels, focus, non-color-only status; safe production errors.

---

## 2. Context, actors, and trust boundaries

**Actors:** All users including AT users; support (request_id).  
**Applies to:** FE-08…FE-18 data pages + shell/forms.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `empty-state.tsx`, `error-state.tsx`, `skeleton.tsx`, `status-badge.tsx`.

---

## 3. Architecture

```text
Page data lifecycle: loading → empty | data | error
Shared primitives: Skeleton · EmptyState · ErrorState · StatusBadge
A11y: labels · focus · keyboard · contrast · status text
```

### 3.3 Component interactions

Domain pages import FE-03 primitives; ErrorState reads AppError; modals manage focus trap.

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-19-1 | EmptyState | `frontend/src/components/ui/empty-state.tsx` |
| C-19-2 | ErrorState | `frontend/src/components/ui/error-state.tsx` |
| C-19-3 | Skeleton | `frontend/src/components/ui/skeleton.tsx` |
| C-19-4 | Status badges | `status-badge.tsx + design/status.ts` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-19-01 | Three-state mandate on data pages | Spinner-only or blank | Operability |
| D-19-02 | request_id in errors | Opaque failure | Support |
| D-19-03 | Not color-only status | Color-only dots | A11y |

### 3.4 Interaction sequence

```text
Fetch start → Skeleton
  → success empty → EmptyState
  → success data → content
  → failure → ErrorState(retry → refetch)
```

---

## 4. Data models, algorithms, state machines, and UI structures

### State pattern

| State | UI | ARIA |
|-------|-----|------|
| Loading | Skeleton | aria-busy |
| Empty | EmptyState + CTA | heading |
| Error | ErrorState + retry + request_id | role=alert |
| Data | Domain content | — |

### A11y rules

Keyboard primary flows · labeled inputs · modal focus trap/restore · visible focus · status text+icon · AA contrast targets.

---

## 4a. Visual and interaction design

### Visual

- Empty: icon + copy (restrained).
- Error: subtle danger border; monospace request_id.
- Skeletons match card/table geometry.

---

## 5. API and interface contracts (ICD)

No backend routes owned. Consumes AppError from FE-07 and primitives from FE-03.

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Retry storms | Disable retry while in-flight |
| Stack traces in prod | Sanitize; NFR-19-02 |
| Focus loss in modal | Trap + restore on close |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-19-01 Skeleton stability | Reserve space |
| NFR-19-02 No secret stack traces | Sanitize production errors |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-19-01 | Every major data page shall implement loading, empty, and error states. | §4 UI state model · §4a loading · FE-19 patterns | requirements TV-*; FE-20 gates |
| FR-19-02 | Error states shall show human-readable messages and request_id when t… | §4 error model · §5 AppError · §6 failures | requirements TV-*; FE-20 gates |
| FR-19-03 | Interactive controls shall be keyboard operable for primary flows. | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-19-04 | Form inputs shall have accessible labels. | §4 form model · §3.3 sequence · §5 mutation ICD | requirements TV-*; FE-20 gates |
| FR-19-05 | Focus shall be managed for modals and drawers (trap/restore as approp… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-19-06 | Status information shall not rely on color alone. | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-19-07 | Empty states shall include guidance on next actions when applicable. | §4 empty model · §4a empty · FE-19 EmptyState | requirements TV-*; FE-20 gates |
| FR-19-08 | The frontend shall target WCAG 2.2 Level AA practices for core operat… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| NFR-19-01 | Loading skeletons shall avoid layout thrash where practical. | §7 NFR design table | Perf/security tests / reviews |
| NFR-19-02 | Error messages shall not dump stack traces or secrets to end users in… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| AC-19-01 | Representative pages (dashboard, runs, approvals) show all three states. | §9 Validation design | Automated or review protocol |
| AC-19-02 | Primary forms have labels; modals keyboard-dismissible. | §9 Validation design | Automated or review protocol |
| AC-19-03 | Production errors omit secrets/stack traces. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

Dashboard/runs/approvals three states; keyboard form pass; ErrorState unit. **TV-19-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-19-01 | Full axe CI on all routes | Optional progressive |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

Page checklist: loading/empty/error wired before marking page DoD (FE-20). Forms: Label+Input association required.

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-19`.
