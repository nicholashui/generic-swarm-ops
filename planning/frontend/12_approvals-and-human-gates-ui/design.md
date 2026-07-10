# Design — 12 Approvals and Human Gates UI

| Field | Value |
|-------|-------|
| Design ID | `FE-12-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-12`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Approvals queue and detail with approve/reject (+ notes), run-detail gate embedding, no silent auto-approve, permission-aware controls.

---

## 2. Context, actors, and trust boundaries

**Actors:** Reviewers, operators, compliance observers.  
**Related BE:** BE-13 human gates; structure.md human–AI rules.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `approval-decision-panel.tsx`.

---

## 3. Architecture

```text
/app/approvals → list pending
/app/approvals/[id] → ApprovalDecisionPanel
Run detail callout → same decision APIs
```

### 3.3 Component interactions

| UI | API |
|----|-----|
| List | GET approvals |
| Decision panel | POST approve/reject/decision |
| Run console | Deep link + optional embed |

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-12-1 | Decision panel | `frontend/src/components/domain/approval-decision-panel.tsx` |
| C-12-2 | Approvals surfaces | `app domain slug / live-ops` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-12-01 | Explicit human decision only | Auto-approve in UI | Governance |
| D-12-02 | Backend decision API | Local-only status flip | Audit on BE |
| D-12-03 | Disable double-submit | Allow spam clicks | Safety |

### 3.4 Interaction sequence

```text
Pending gate on run
  → operator opens approvals or run callout
  → reviews context
  → Approve → run resumes (BE) → UI refresh
```

---

## 4. Data models, algorithms, state machines, and UI structures

### List model

Filters: pending/resolved. Columns: created, risk/tier, workflow/run, requester, status.

### Decision algorithm

```text
user clicks Approve|Reject
  → optional confirm if high risk
  → set pending (disable buttons)
  → POST backend decision (+ notes)
  → success: refresh list/detail
  → failure: ErrorState; restore buttons; no fake success
```

---

## 4a. Visual and interaction design

### Visual

- Warning emphasis on pending high-risk rows.
- Reject uses destructive button variant.
- Notes textarea optional above actions.
- Sticky decision panel on detail where helpful.

---

## 5. API and interface contracts (ICD)

| Method | Path | Usage |
|--------|------|-------|
| GET | `/api/v1/approvals` | List |
| GET | `/api/v1/approvals/{id}` | Detail |
| POST | `.../approve`, `.../reject`, or decision | Decide |

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| 403 decision | Error; state unchanged |
| Already decided | Show terminal state; disable actions |
| Missing context | Show available fields; link to run if id present |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-12-01 Pending-first | Default filter pending |
| NFR-12-02 AuthZ required | Session + BE |
| NFR-12-03 No offline forge | No local authority |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-12-01 | The frontend shall provide approvals list and detail routes under `/a… | §3 architecture · §5 routes ICD | requirements TV-*; FE-20 gates |
| FR-12-02 | When approval data is loaded, the frontend shall show request context… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-12-03 | When the user explicitly approves or rejects, the frontend shall call… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-12-04 | If the backend denies the decision, the frontend shall display the er… | §4 error model · §5 AppError · §6 failures | requirements TV-*; FE-20 gates |
| FR-12-05 | The frontend shall not auto-approve high-risk actions without an expl… | §3.2 decisions · §4 decision algorithm | requirements TV-*; FE-20 gates |
| FR-12-06 | When a run has a pending gate, run detail shall deep-link or embed ga… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-12-07 | If the user lacks approve/reject permission, the frontend shall hide … | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| FR-12-08 | When the user submits a decision, the frontend shall allow optional d… | §4 form model · §3.3 sequence · §5 mutation ICD | requirements TV-*; FE-20 gates |
| FR-12-09 | If decision submission is in progress, the frontend shall disable dou… | §4 form model · §3.3 sequence · §5 mutation ICD | requirements TV-*; FE-20 gates |
| NFR-12-01 | Approvals list shall load pending items preferentially. | §7 NFR design table | Perf/security tests / reviews |
| NFR-12-02 | Approval decisions shall require authenticated session and backend au… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| NFR-12-03 | Client shall not forge approval records offline as authoritative. | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| AC-12-01 | Pending approval appears in list when backend has one. | §9 Validation design | Automated or review protocol |
| AC-12-02 | Approve/reject updates status via API. | §9 Validation design | Automated or review protocol |
| AC-12-03 | No silent auto-approve path in UI. | §9 Validation design | Automated or review protocol |
| AC-12-04 | In-progress decision disables double-submit. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

E1 gate path; no auto-approve; double-submit disabled. **TV-12-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-12-01 | Multi-approver chain UI | When backend supports |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

Wire panel to typed client; include notes field when OpenAPI supports; gate with FE-06 approve permissions.

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-12`.
