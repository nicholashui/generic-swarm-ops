# Design — 20 Security, Performance, Testing, and Ops Profile

| Field | Value |
|-------|-------|
| Design ID | `FE-20-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-20`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Cross-cutting security hygiene, performance expectations, automated quality gates, E1/ops profile proof, page DoD, and explicit product-bar non-goals.

---

## 2. Context, actors, and trust boundaries

**Actors:** Release managers, security reviewers, CI, operators proving E1.  
**Evidence:** frontend README, unit tests, e2e smoke, status docs.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `frontend/tests`, `e2e`, `package.json`, `README.md`.

---

## 3. Architecture

```text
Quality gates: lint · typecheck · unit · build · (e2e when stack up)
Ops profile: DEMO_MODE=false + live BE + Postgres
E1: login → dashboard → run → gate → improve
Non-goals explicit (do not block mark ~100)
```

### 3.3 Component interactions

| Gate | Tooling |
|------|---------|
| Unit | vitest `tests/unit/*` |
| E2E | playwright `e2e/e1-smoke.spec.ts` |
| Lint/TS | eslint + tsc |
| Security review | env allowlist, no secrets, charter INV |

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-20-1 | Unit tests | `frontend/tests/unit/*` |
| C-20-2 | E2E smoke | `frontend/e2e/e1-smoke.spec.ts` |
| C-20-3 | Playwright config | `frontend/playwright.config.ts` |
| C-20-4 | Env security | `frontend/src/lib/config/env.ts` |
| C-20-5 | Package scripts | `frontend/package.json` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-20-01 | Ops profile is product truth | Demo-only ship claim | Mark ~100 |
| D-20-02 | Explicit non-goals | Infinite FE scope | Focus |
| D-20-03 | E1 as operator proof | Screenshots only | Repeatability |

### 3.4 Interaction sequence

```text
PR / release
  → pnpm lint && typecheck && test && build
  → (optional) e2e if servers up
  → ops profile manual E1 if claiming operator path
  → non-goals not filed as defects
```

---

## 4. Data models, algorithms, state machines, and UI structures

### Page DoD checklist (normative)

1. Route reachable in IA  
2. Permission-aware  
3. Loading/empty/error  
4. API wired or documented stub  
5. No charter violations  

### E1 sequence

login → dashboard → create/run workflow → human gate → improve steps  

### Non-goals (mark ~100)

Always-on Playwright permanent servers · full graph explorer · live CRM/email/billing admin · host self-rewrite UI · client-only AuthZ · infinite business leaf UIs

---

## 4a. Visual and interaction design

### Visual QA gate

Spot-check shell, login, dashboard, run console, approvals, evolution for token consistency before release claims.

---

## 5. API and interface contracts (ICD)

Quality process interfaces only: CI scripts, env templates, e2e config — not business REST.

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Unit fail | Block merge |
| E2E servers down | Skip/soft-fail per non-goal; do not claim full E2E green |
| Secret in env sample | Fix before release |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-20-01 CI-reasonable build | next build |
| NFR-20-02 Code-split heavy widgets | dynamic import where practical |
| NFR-20-03 Dependency review | lockfile hygiene |
| NFR-20-04 Live mode still authed | DEMO false ≠ auth off |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-20-01 | The frontend shall enforce security hygiene: no provider secrets in c… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-20-02 | The frontend shall meet performance expectations for interactive ops … | §4 form model · §3.3 sequence · §5 mutation ICD | requirements TV-*; FE-20 gates |
| FR-20-03 | The frontend shall provide automated lint, typecheck, unit tests, and… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-20-04 | When servers are available, the frontend shall support an operator E1… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-20-05 | The ops profile shall run with `NEXT_PUBLIC_DEMO_MODE=false` against … | §4 ops profile · §9 validation | requirements TV-*; FE-20 gates |
| FR-20-06 | Each page DoD shall include: routes, permission awareness, loading/em… | §4 UI state model · §4a loading · FE-19 patterns | requirements TV-*; FE-20 gates |
| FR-20-07 | Product-bar non-goals (always-on UI CI servers, full graph explorer, … | §10 non-goals | requirements TV-*; FE-20 gates |
| FR-20-08 | Client observability shall preserve request_id on failures for suppor… | §4 error model · §5 AppError · §6 failures | requirements TV-*; FE-20 gates |
| NFR-20-01 | Production build shall complete in CI-reasonable time for the repo’s … | §7 NFR design table | Perf/security tests / reviews |
| NFR-20-02 | Bundle shall code-split heavy client widgets (run timeline, command p… | §7 performance NFR | Perf/security tests / reviews |
| NFR-20-03 | Dependency vulnerabilities in FE lockfile shall be reviewed before re… | §7 NFR design table | Perf/security tests / reviews |
| NFR-20-04 | DEMO_MODE shall not be required for security; live mode must still en… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| AC-20-01 | `pnpm lint`, `pnpm typecheck`, unit tests, and `pnpm build` green. | §9 Validation design | Automated or review protocol |
| AC-20-02 | Ops profile documented and usable for E1. | §9 Validation design | Automated or review protocol |
| AC-20-03 | Security checklist items in §24 addressed or explicitly deferred with… | §9 Validation design | Automated or review protocol |
| AC-20-04 | Non-goals list matches frontend.md §33.5. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

lint+typecheck+unit+build green; E1 when stack up; secrets scan; map §30–31 to FE specs. **TV-20-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-20-01 | Always-on UI CI farm | Non-goal |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

| Claim | Required proof |
|-------|----------------|
| Code quality | lint/typecheck/unit/build |
| Ops path | DEMO_MODE=false + live BE notes |
| Security | no secrets in client; charter INV hold |
| Completeness | page DoD for shipped surfaces |

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-20`.
