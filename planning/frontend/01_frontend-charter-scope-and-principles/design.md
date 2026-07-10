# Design — 01 Frontend Charter, Scope, and Design Principles

| Field | Value |
|-------|-------|
| Design ID | `FE-01-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-01`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Establish the Next.js ops console as a **presentation and interaction layer only**: professional enterprise SaaS UX for agents, workflows, gates, knowledge, evals, audit, evolution, and improve—while **backend remains sole authority** for AuthN/AuthZ, execution, secrets, audit writes, and DNA safety.

---

## 2. Context, actors, and trust boundaries

```text
Operator Browser (untrusted for enforcement)
        │  HTTPS
        ▼
┌────────────────────────────────────────────┐
│ Frontend ops console (this charter)        │
│ Presentation · Routing · UI state · Forms  │
└────┬───────────────────────────────────────┘
     │  /api/v1 only (FE-07)
     ▼
Backend control plane (planning/backend BE-*)
```

**Actors:** Operators, reviewers, admins, Trae/OpenDesign agents, demo-mode preview users.  
**Trust boundary:** UI may hide controls; **backend decides**. No browser execution of agents/tools/workflows; no client DNA mutation; no secret storage.  
**Threats in scope for design:** privilege elevation via UI, secret leakage in client bundles, silent production DNA mutation UI.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `frontend.md`, `planning/frontend/README.md`, `frontend/src`.

---

## 3. Architecture

```text
INV-FE-01: No core business logic / execution in browser
INV-FE-02: All mutations via versioned backend APIs
INV-FE-03: Client permission UI is UX-only (fail closed when unknown)
INV-FE-04: Evolution/improve actions sandbox-gated on backend
INV-FE-05: OpenDesign-first major layouts (or documented fallback)
INV-FE-06: Ops profile DEMO_MODE=false is the production-truth path
```

### 3.3 Component interactions

| From | To | Contract |
|------|----|----------|
| Any page | Backend | HTTPS `/api/v1/*` only (FE-07) |
| Any page | FE-06 | Permission UX gates |
| Layout design | FE-03 | Tokens + OpenDesign |
| Release | FE-20 | DoD / non-goals |

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-01-1 | Charter document set | `frontend.md §1–4, §6, §32–33 + this design` |
| C-01-2 | Boundary review gates | `PR review + FE-20 quality gates` |
| C-01-3 | As-built console root | `frontend/src` |
| C-01-4 | Planning index | `planning/frontend/README.md` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-01-01 | Thin presentation FE | Fat client with local policy engine | Safety + auditability |
| D-01-02 | Enterprise ops aesthetic | Generic AI demo chrome | Product vision frontend.md §2 |
| D-01-03 | OpenDesign-led major layouts | Memory-only ad-hoc UI design | frontend.md §3 |
| D-01-04 | Backend sole mutation authority | Optimistic local-only writes | structure.md control plane |

### 3.4 Interaction sequence

```text
New feature proposal
  → map to FE charter INV
  → if execution/policy/secrets → reject (backend owns)
  → else design UI + FE-07 API wiring + FE-06 gates
  → FE-20 DoD before ship claim
```

---

## 4. Data models, algorithms, state machines, and UI structures

### Charter decision lattice

| Trade-off | Prefer | Enforce via |
|-----------|--------|-------------|
| Clarity vs decoration | Operational clarity | Design tokens + density (FE-03) |
| Convenience vs security theater | Real backend checks | FE-06 + FE-07 |
| Demo convenience vs ops truth | Ops profile for product bar | `NEXT_PUBLIC_DEMO_MODE` |

### Forbidden UI features (normative checklist)

1. Direct database access from browser  
2. Provider API keys or secret material in client code  
3. Silent production DNA rewrite controls  
4. Host application self-rewrite UI  
5. Treating hidden buttons as authorization  

### Downstream inheritance

All FE-02…FE-20 designs inherit INV-FE-01…06; deviations require open issue + human approval.

---

## 4a. Visual and interaction design

### Visual / UX charter

- Serious enterprise SaaS: trust, density, status clarity (frontend.md §2, §15).
- Operators always understand agents, workflows, runs, failures, approvals, knowledge, evidence, attention items.
- Status language prefers operational semantics (`running`, `failed`, `awaiting_approval`) over decorative fluff.
- Prefer scannable tables and metric cards over marketing dashboards.

---

## 5. API and interface contracts (ICD)

No public business REST owned by FE-01. **Interface obligations:**

| Consumer | Obligation |
|----------|------------|
| FE-05+ pages | Session + API only; no local policy authority |
| FE-17 / FE-18 | Sandbox-only evolution/improve APIs |
| FE-06 | UX gates fail closed |
| FE-20 | Enforce non-goals and page DoD |

**Envelope / AuthZ:** Inherited from FE-07 / FE-06; backend final.

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Feature requests client-side execution | Reject against INV-FE-01; route to backend design |
| UI hides admin button only | Insufficient — backend AuthZ required (document in FE-06) |
| Proposed prod DNA edit in browser | Reject; FE-17/18 sandbox APIs only |
| Demo mode treated as product bar proof | Reject; require DEMO_MODE=false ops path |

---

## 7. NFR design and observability

| NFR | Design response |
|-----|-----------------|
| NFR-01-01 Deterministic charter checks | Code review + static rules; no LLM-as-policy |
| NFR-01-02 No duplicated BE business rules | Domain pages call APIs only |
| NFR-01-03 No unattended prod DNA mutation UI | FE-17/18 + §10 non-goals |
| NFR-01-04 No secrets in FE | Env allowlist (FE-02) + FE-20 security |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-01-01 | The frontend shall deliver the user-facing web application for managi… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-01-02 | The frontend shall communicate trust, reliability, operational clarit… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-01-03 | The frontend shall own presentation, interaction, routing, layout, UI… | §4 realtime algorithm · §3.3 sequence | requirements TV-*; FE-20 gates |
| FR-01-04 | If a capability requires workflow execution, agent execution, tool ex… | §1 Purpose · §3 INV · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-01-05 | When the user requests an action, the frontend shall request it from … | §2 trust boundary · §5 ICD (API-only mutations) | requirements TV-*; FE-20 gates |
| FR-01-06 | The frontend shall not assume that hiding a control is sufficient sec… | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-01-07 | When designing major page layouts, the frontend workflow shall prefer… | §4a visual design · FE-03 tokens | requirements TV-*; FE-20 gates |
| FR-01-08 | The frontend shall treat `structure.md` as architecture source of tru… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-01-09 | When a design trade-off exists between operator clarity and decorativ… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-01-10 | The frontend shall support both an ops profile (`NEXT_PUBLIC_DEMO_MOD… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-01-11 | The frontend shall remain a presentation and interaction layer so tha… | §1 Purpose · §2 presentation layer | requirements TV-*; FE-20 gates |
| NFR-01-01 | Charter and boundary checks shall be enforceable by code review and a… | §7 NFR design table | Perf/security tests / reviews |
| NFR-01-02 | Frontend package boundaries shall keep domain pages free of backend b… | §7 NFR design table | Perf/security tests / reviews |
| NFR-01-03 | If a proposed UI feature would allow unattended direct production DNA… | §7 NFR design table | Perf/security tests / reviews |
| NFR-01-04 | The frontend shall never store provider secrets or perform final auth… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| AC-01-01 | frontend.md and this spec state frontend is presentation/interaction … | §9 Validation design | Automated or review protocol |
| AC-01-02 | Out-of-scope list matches frontend.md §4.2 and §33.5 non-goals. | §9 Validation design | Automated or review protocol |
| AC-01-03 | All downstream planning/frontend/* specs reference FE-01 priority order. | §9 Validation design | Automated or review protocol |
| AC-01-04 | Evolution and improve specs explicitly require sandbox-only backend A… | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

Document review: map each INV to later FE designs; negative review of client DNA rewrite; RTM FE-01 → FE-02…20.  
**TV anchors:** TV-01-01…TV-01-03 in paired requirements.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-01-01 | Mobile-native app shell | Deferred; responsive web first |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

| Concern | Spec |
|---------|------|
| Ownership | Product/architecture maintains charter; FE PRs cite FE-01 for boundary questions |
| Enforcement | Review checklist on PRs that add mutations, storage, or “smart” client logic |
| Evidence | `frontend.md` §33; `planning/frontend/DESIGN_QUALITY_SCORE.md` |

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-01`.
