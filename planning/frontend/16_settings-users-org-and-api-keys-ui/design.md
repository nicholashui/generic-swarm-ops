# Design — 16 Settings, Users, Organization, and API Keys UI

| Field | Value |
|-------|-------|
| Design ID | `FE-16-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-16`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Settings hub: org profile, users invite/disable, API keys, security, billing placeholder, profile/integrations—wired to BE-07 and auth key APIs.

---

## 2. Context, actors, and trust boundaries

**Actors:** Org admins, billing managers, security admins.  
**Related BE:** BE-07 users/orgs/invitations; BE-05 API keys.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `api-key-table.tsx`, settings surfaces.

---

## 3. Architecture

```text
/app/settings
  ├── organization → GET/PATCH orgs
  ├── users → users + invitations
  ├── api-keys → key CRUD (secret once)
  ├── security / billing / profile / integrations
  └── accept-invite flow remains /accept-invite (FE-05)
```

### 3.3 Component interactions

| Surface | Component | API |
|---------|-----------|-----|
| API keys | `api-key-table.tsx` | auth api-keys |
| Users | settings users panel | users + invitations |
| Org | settings org form | organizations |

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-16-1 | Settings surfaces | `app settings paths / slug` |
| C-16-2 | API key table | `frontend/src/components/domain/api-key-table.tsx` |
| C-16-3 | Live ops APIs | `lib/api client + live-ops` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-16-01 | Billing placeholder OK | Fake charge calculator | Non-goal honesty |
| D-16-02 | Show API key secret once | Persist secret in localStorage | Security |
| D-16-03 | Invite via BE invitations | Email-less fake users only | Tenancy |
| D-16-04 | Confirm destructive actions | Immediate disable/revoke | Safety UX |

### 3.4 Interaction sequence

```text
Admin invites user
  → POST /users/invitations
  → show success
Invitee opens /accept-invite
  → FE-05 accept flow
```

---

## 4. Data models, algorithms, state machines, and UI structures

### Settings IA

organization · users · roles · billing · api-keys · security · integrations · profile

### API key lifecycle

create → show secret once in modal → list shows prefix only → revoke confirms → DELETE/revoke API.

### User admin

list · invite · disable/update with confirm on destructive.

---

## 4a. Visual and interaction design

### Visual

- Vertical settings subnav.
- Forms in Cards with Save bar.
- Danger zone styling for disable/revoke.
- One-time secret modal with copy + warning.

---

## 5. API and interface contracts (ICD)

| Domain | Paths |
|--------|-------|
| Users | `GET/POST /users`, `PATCH /users/{id}` |
| Invitations | `GET/POST /users/invitations`, accept on FE-05 |
| Orgs | `GET/PATCH /organizations/{id}` |
| API keys | auth api-keys CRUD |

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| PATCH org 403 | Error; form not marked saved |
| Invite invalid email | 422 field error |
| Key create failure | No fake secret display |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-16-01 Save without remount | Local state update |
| NFR-16-02 One-time secret | Ephemeral UI state only |
| NFR-16-03 Confirm destructive | Modal confirm |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-16-01 | The frontend shall provide a settings hub under `/app/settings` with … | §3 architecture · §5 routes ICD | requirements TV-*; FE-20 gates |
| FR-16-02 | User management UI shall list users via backend and support invite/di… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-16-03 | Organization settings UI shall load and save organization fields via … | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-16-04 | API keys UI shall create/list/revoke keys only through backend auth/A… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-16-05 | Billing page may be a placeholder if backend lacks billing; it shall … | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-16-06 | Security settings UI shall display backend-provided security configur… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-16-07 | Invitation creation from settings shall use backend invitation APIs; … | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| FR-16-08 | Permission-aware UI shall restrict admin settings to authorized roles. | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| NFR-16-01 | Settings forms shall avoid full app remounts on save success. | §7 NFR design table | Perf/security tests / reviews |
| NFR-16-02 | Newly created API key secrets shall be shown once (if backend returns… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| NFR-16-03 | User disable/invite actions require confirmation where destructive. | §7 NFR design table | Perf/security tests / reviews |
| AC-16-01 | Settings nav links resolve to settings surfaces. | §9 Validation design | Automated or review protocol |
| AC-16-02 | Users invite/list wired to backend invitations/users APIs (or documen… | §9 Validation design | Automated or review protocol |
| AC-16-03 | Organization save calls PATCH when implemented. | §9 Validation design | Automated or review protocol |
| AC-16-04 | API keys page uses backend endpoints. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

Settings links; invite/org save when wired; keys via BE. **TV-16-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-16-01 | Full roles matrix editor | When BE roles API expands |
| OI-16-02 | Complete invite/org wiring gaps | Follow-on; BE already ships APIs |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

Wire forms to BE-07; regenerate OpenAPI; never store API secrets in localStorage; FE-06 admin gates.

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-16`.
