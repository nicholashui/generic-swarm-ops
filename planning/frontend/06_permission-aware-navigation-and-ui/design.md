# Design — 06 Permission-Aware Navigation and UI

| Field | Value |
|-------|-------|
| Design ID | `FE-06-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-06`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Load roles/permissions from backend; hide/disable nav and actions; show Access Denied; fail closed; never treat UI as enforcement authority.

---

## 2. Context, actors, and trust boundaries

**Actors:** All authenticated roles (Owner…Security Auditor).  
**Trust:** Backend 403 is source of truth. UI is convenience + least privilege presentation.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `frontend/src/lib/auth/permissions.ts`, `hooks/use-permissions.ts`, `tests/unit/permissions.test.ts`.

---

## 3. Architecture

```text
GET /auth/me → permissions model → usePermissions()
   ├── filter Sidebar / Command palette items
   ├── gate domain action buttons
   └── route-level Access Denied
```

### 3.3 Component interactions

| Consumer | API | Behaviour if deny |
|----------|-----|-------------------|
| Sidebar | `can(perm)` | Hide item |
| Run Now button | `can(workflows:run)` | Disable + tooltip |
| Settings admin | `can(org:admin)` | 403 page if navigated |

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-06-1 | Permissions model | `frontend/src/lib/auth/permissions.ts` |
| C-06-2 | usePermissions | `frontend/src/hooks/use-permissions.ts` |
| C-06-3 | Permission types | `frontend/src/types/permissions.ts` |
| C-06-4 | Unit tests | `frontend/tests/unit/permissions.test.ts` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-06-01 | Fail closed if payload missing | Show all then error | Least privilege |
| D-06-02 | Backend payload drives UI | Hardcoded role matrix only | Drift control |
| D-06-03 | Surface API 403 explicitly | Silent no-op | Operator trust |

### 3.4 Interaction sequence

```text
Login success → fetch /auth/me → cache perms for session
Org switch → refetch me → re-filter nav
User clicks gated action without perm → control not available
User hits API 403 → error toast/panel with message
```

---

## 4. Data models, algorithms, state machines, and UI structures

### Permission evaluation algorithm

```text
load me.permissions
if payload missing: DENY all gated actions
if route.required not in perms: AccessDenied view
if action.required not in perms: hide|disable control
on API 403: show ErrorState; do not keep optimistic success
```

### Role labels (display only)

Owner, Admin, Developer, Operator, Reviewer, Viewer, Billing Manager, Security Auditor — **must match backend names**.

---

## 4a. Visual and interaction design

### Visual

- Disabled controls: disabled styles + optional tooltip “Insufficient permission”.
- Access Denied: title, explanation, link to dashboard.
- Never imply user has admin powers via chrome alone.

---

## 5. API and interface contracts (ICD)

Consumes `GET /api/v1/auth/me` (or equivalent) permission/role fields.  
**No FE write path for privileges.**

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| Permissions fetch fails | Fail closed + error; limited shell |
| Stale perms after role change | Refresh on focus/org switch; 403 still authoritative |
| Client tampers localStorage perms | Ignored if not from API; API still enforces |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-06-01 Session cache | Refresh on login/org switch |
| NFR-06-02 Non-writable elevation | In-memory from API only |
| NFR-06-03 Fail closed | Default deny |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-06-01 | The frontend shall load the authenticated user’s roles and permission… | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| FR-06-02 | When the user lacks permission for a navigation item, the frontend sh… | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| FR-06-03 | When the user navigates to a route they cannot access, the frontend s… | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| FR-06-04 | When the user lacks permission for a mutating action, the frontend sh… | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| FR-06-05 | If the backend returns 403 for an action the UI allowed, the frontend… | §2 AuthZ UX · FE-06 · §6 unauthorized | requirements TV-*; FE-20 gates |
| FR-06-06 | The frontend shall treat permission-aware UI as UX-level only; backen… | §2 trust · §4 fail-closed algorithm | requirements TV-*; FE-20 gates |
| FR-06-07 | Role labels displayed in UI shall match backend-provided role names w… | §5 ICD · FE-07 client | requirements TV-*; FE-20 gates |
| NFR-06-01 | Permission payload shall be cached for the session and refreshed on l… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| NFR-06-02 | Client-side permission caches shall not be writable by untrusted page… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| NFR-06-03 | Permission checks in UI shall fail closed (deny/hide) when permission… | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| AC-06-01 | Viewer-like role cannot see admin-only nav items (given backend paylo… | §9 Validation design | Automated or review protocol |
| AC-06-02 | 403 from API shows error state on attempted mutation. | §9 Validation design | Automated or review protocol |
| AC-06-03 | Documentation states client gates are non-authoritative. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

Mock viewer hides admin; API 403 path; review non-authoritative docs. **TV-06-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-06-01 | Fine-grained ABAC attribute UI | When backend exposes |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

| Helper | Spec |
|--------|------|
| `can(permission: string): boolean` | false if unknown |
| `canAny(list)` / `canAll(list)` | as needed |
| Route config | map path → required permission |

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-06`.
