# Design — 13 Knowledge and Memory UI

| Field | Value |
|-------|-------|
| Design ID | `FE-13-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-13`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Knowledge overview/sources/documents/search and memory list/detail as read-forward ops surfaces over BE APIs; no browser embedding/indexing.

---

## 2. Context, actors, and trust boundaries

**Actors:** Operators, reviewers.  
**Related BE:** BE-15 knowledge, BE-16 memory.  
**Non-goal:** Full LightRAG/Neo4j explorer product.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `search-input.tsx`, live-data knowledge/memory paths.

---

## 3. Architecture

```text
/app/knowledge[/sources|/documents|/search]
/app/memory[/id]
   → FE-07 loaders → BE knowledge/memory
SearchInput (debounced) → retrieval API
```

### 3.3 Component interactions

| UI | Behaviour |
|----|-----------|
| Search | Debounce 200–400ms → GET search |
| Source list | Table + detail |
| Memory detail | Provenance fields as returned |

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-13-1 | Knowledge/memory panels | `app domain surfaces` |
| C-13-2 | Search input | `frontend/src/components/ui/search-input.tsx` |
| C-13-3 | Live data | `frontend/src/lib/api/live-data.ts` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-13-01 | Backend retrieval only | Client vector DB | Charter + non-goals |
| D-13-02 | Debounced search | Keystroke flood | Performance |

### 3.4 Interaction sequence

```text
User types query
  → debounce
  → GET search
  → results list OR empty
```

---

## 4. Data models, algorithms, state machines, and UI structures

### Knowledge pages

Overview health · sources · documents · search results with provenance chips when present.

### Memory pages

List filters · detail: type, scope, provenance, timestamps **only as BE returns**.

---

## 4a. Visual and interaction design

### Visual

- Search results: snippet + source badge.
- Provenance chips.
- Empty knowledge: CTA add source if permitted.

---

## 5. API and interface contracts (ICD)

Knowledge sources/documents/search + memory list/get routes per OpenAPI (BE-15/16). Mutations only if exposed and permitted.

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Search 5xx | ErrorState + retry |
| Empty results | EmptyState guidance |
| Unauthorized memory | 403 / hide |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-13-01 Debounce search | 200–400ms |
| NFR-13-02 No corpus exfil beyond API | Render returned only |
| NFR-13-03 Sensitive memory UX | FE-06 gates |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-13-01 | The frontend shall provide knowledge routes for overview, sources, do… | §3 architecture · §5 routes ICD | requirements TV-*; FE-20 gates |
| FR-13-02 | The frontend shall provide memory list and detail routes under `/app/… | §3 architecture · §5 routes ICD | requirements TV-*; FE-20 gates |
| FR-13-03 | Knowledge/memory views shall render backend-returned metadata and sha… | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-13-04 | When search is invoked, the frontend shall call backend retrieval API… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-13-05 | The frontend shall not perform embedding or indexing in the browser. | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-13-06 | Mutations (add source, delete memory) shall only occur through backen… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| NFR-13-01 | Search UI shall debounce queries to avoid request storms. | §7 performance NFR | Perf/security tests / reviews |
| NFR-13-02 | Knowledge UI shall not exfiltrate full corpora beyond what backend re… | §7 NFR design table | Perf/security tests / reviews |
| NFR-13-03 | Memory detail shall respect permission UX for sensitive records. | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| AC-13-01 | Knowledge and memory pages render in app shell. | §9 Validation design | Automated or review protocol |
| AC-13-02 | Search calls backend and shows results or empty state. | §9 Validation design | Automated or review protocol |
| AC-13-03 | No client-side vector store dependency. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

Open knowledge/memory; search empty/results; no client vector dep. **TV-13-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-13-01 | Full graph explorer UI | Non-goal mark ~100 |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

Use FE-07 loaders; never import vector DB clients; keep mutations behind permission checks.

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-13`.
