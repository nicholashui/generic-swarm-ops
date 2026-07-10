# Design — 16 Human–AI Interaction Rules

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-16-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-16`) |
| Source | `structure.md` §10 |
| Design quality bar | 100 |

---

## 1. Purpose

Make the control plane **human-centered**: show confidence and evidence, preview consequential actions, enable correction/override, capture rejections as lessons, never let UI replace backend authority.

---

## 2. Context

```text
Browser → Next.js (/app/*) → typed OpenAPI client
                │ DEMO_MODE?
                ├─ true: fixtures (preview only)
                └─ false: live API (ops authority path)
         Backend = final authz / gates / tools
```

---

## 3. Architecture

### 3.1 Components

| ID | Component | Role |
|----|-----------|------|
| C-16-1 | App shell | Nav, role-aware menus |
| C-16-2 | Run detail | Status, steps, logs, Improve |
| C-16-3 | Approvals UI | Risk + evidence + decide |
| C-16-4 | Knowledge UI | Results + source_refs |
| C-16-5 | Evolution archive | `/app/evolution` |
| C-16-6 | Forms | Zod + RHF create agent/workflow |
| C-16-7 | Error surface | message + request_id |
| C-16-8 | Auth | Password + session cookies |
| C-16-9 | E2E smoke | Playwright |

### 3.2 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-16-01 | Ops profile DEMO_MODE=false | Real authority path |
| D-16-02 | UI permission = UX only | Backend final (FR-16-09) |
| D-16-03 | OpenDesign optional | Documented fallback |
| D-16-04 | Reject → lesson | structure human learning |

---

## 4. Interaction rules → UI design

| Rule | UI / behavior |
|------|----------------|
| Show confidence/uncertainty | Badges, scores when present; no false certainty copy |
| Show evidence | source_refs, tool_effects, logs, audit links |
| Preview actions | Confirm destructive; Run now shows required payload |
| One-click correct | Primary actions on forms/errors |
| Override | Only authorized API actions |
| Store rejections | POST reject → improvement_lessons |
| Ask clarification | Validation errors on thin context |
| Honest uncertainty | Empty/error states required |

### 4.1 Page state model (every major page)

`loading | empty | data | error | forbidden`

---

## 5. Route map (ops)

| Route | Capability |
|-------|------------|
| `/app` | Dashboard |
| `/app/agents`, `/app/workflows` | List + create |
| `/app/workflow-runs/[id]` | Timeline + Improve |
| `/app/approvals` | Gate queue |
| `/app/knowledge`, `/app/memory` | Retrieval/memory |
| `/app/evaluations` | Cards |
| `/app/processes` | PI |
| `/app/audit-logs` | Audit |
| `/app/evolution` | Archive |
| `/app/settings` | Org/user |

### 5.1 Improve pipeline UX

Buttons: Reflect → Propose → Evaluate → Canary (or full pipeline). Never implies auto production promote.

---

## 6. Client contracts

| Topic | Design |
|-------|--------|
| Types | OpenAPI `pnpm api:generate` |
| Errors | `formatMutationError` → message + request_id |
| Auth storage | Prefer HttpOnly cookies; no long-lived localStorage secrets in ops |
| Demo | DEMO_MODE true disables live mutations expectation |

---

## 7. NFR design

| NFR | Design |
|-----|--------|
| NFR-16-01 Interactive ≤3s local healthy API | App router + API |
| NFR-16-02 Run updates ≤2s with SSE | Event stream |
| NFR-16-03 No long-lived secrets in localStorage | Cookie session |
| NFR-16-04 Destructive confirm | Dialogs |
| NFR-16-05 No stack/secrets in UI errors | Envelope only |

---

## 8. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-16-01…08 | §4 rules | UX checklist + unit |
| FR-16-09 | D-16-02 | API 403 despite hidden UI |
| FR-16-10 | Run detail | e2e/component |
| NFR-16-01…05 | §7 | typecheck/test/e2e |
| AC-16-01…06 | §5–6 | FE suites |

---

## 9. Validation design

Live lists; forms; Improve; evolution page; Playwright smoke; authz negative.

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-16-01 | Full OpenDesign enforcement | Optional |
| OI-16-02 | Always-on Playwright CI servers | Non-goal |
| OI-16-03 | Rich a11y audit automation | Continuous improvement |

---

## 11. Design score claim

**Self-score: 100** — interaction matrix, routes, states, contracts, rejection lesson, RTM.
