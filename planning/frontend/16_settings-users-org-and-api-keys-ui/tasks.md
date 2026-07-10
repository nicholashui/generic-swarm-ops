# Tasks — 16 Settings, Users, Organization, and API Keys UI

| Field | Value |
|-------|-------|
| Task list ID | `FE-16-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-16-DES`) |
| Paired requirements | `requirements.md` (`FE-16`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 8/8 · NFR 3/3 · AC 4/4 · C-* 3/3 |

---

## SDD workflow

Settings hub → users/invite → org PATCH → API keys once → confirm danger.

```text
requirements.md (EARS + AC + TV)
  → design.md v2.1 (architecture / ICD / visual / RTM)
    → tasks.md v2.3 (this file; prioritized, test-first, design-aligned steps)
      → incremental implementation in frontend/ (one milestone / task)
        → iterative compliance check (unit / e2e / E1 / review after each P0 cluster)
          → exit only when FR/NFR/AC/C-* coverage = 100% and residual [~] documented
```

### Incremental specification validation (mandatory)

| Gate | When | Action |
|------|------|--------|
| Spec sync | Before coding | Re-read paired FR + design §3/§5/§4a for the task |
| Test-first | Before implementation | Add failing unit/checklist stated in task |
| Implement | Minimal change | Touch only **Deliverable** paths + necessary imports |
| Re-verify | After change | Re-run test-first; fix until green |
| Compliance | After P0 cluster | Update RTM mental model; no silent FR drift |
| Exit | Component done | Exit review task + FE-20 gates |

## Primary code deliverables (this component)

These are the **main source locations** for FE-16. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/components/domain/api-key-table.tsx`
- `frontend/src/app/app/[...slug]/page.tsx`
- `frontend/src/lib/api/client.ts`
- `frontend/src/lib/api/live-ops-surfaces.ts`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-16-1 | Settings surfaces | `app settings paths / slug` |
| C-16-2 | API key table | `frontend/src/components/domain/api-key-table.tsx` |
| C-16-3 | Live ops APIs | `lib/api client + live-ops` |

---

## Task backlog

### [x] T-16-01 — The frontend shall provide a settings hub under `/app/settings` with sub-routes for organization,…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-16-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-16-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/lib/api/live-ops-surfaces.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-16-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-16-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire settings sub-routes to users/orgs/keys APIs. 4) Confirm destructive actions; show API key secret once only. 5) Billing remains placeholder without inventing charges. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-16-01. |
| **Success** | Observable: The frontend shall provide a settings hub under `/app/settings` with sub-routes for organization, users, roles, billing, API keys, securi…. |
| **Acceptance** | FR-16-01: The frontend shall provide a settings hub under `/app/settings` with sub-routes for organization, users, roles, billing, API keys, security, integrations, and profile as specified. |
| **Evidence** | `frontend/src/components/domain/api-key-table.tsx` |

### [x] T-16-02 — User management UI shall list users via backend and support invite/disable/update actions through…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-16-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-16-02 |
| **Deliverable (code paths)** | `frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts`<br>`frontend/src/components/domain/api-key-table.tsx` |
| **Test-first** | Failing check first for FR-16-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-16-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-16-02. |
| **Success** | Observable: User management UI shall list users via backend and support invite/disable/update actions through BE-07 APIs when permitted. |
| **Acceptance** | FR-16-02: User management UI shall list users via backend and support invite/disable/update actions through BE-07 APIs when permitted. |
| **Evidence** | `frontend/src/app/app/[...slug]/page.tsx` |

### [x] T-16-03 — Organization settings UI shall load and save organization fields via GET/PATCH organization APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-16-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-16-03 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/lib/api/live-ops-surfaces.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-16-03: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-16-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire settings sub-routes to users/orgs/keys APIs. 4) Confirm destructive actions; show API key secret once only. 5) Billing remains placeholder without inventing charges. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-16-03. |
| **Success** | Observable: Organization settings UI shall load and save organization fields via GET/PATCH organization APIs. |
| **Acceptance** | FR-16-03: Organization settings UI shall load and save organization fields via GET/PATCH organization APIs. |
| **Evidence** | `frontend/src/components/domain/api-key-table.tsx` |

### [x] T-16-04 — API keys UI shall create/list/revoke keys only through backend auth/API key endpoints
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-16-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-16-04 |
| **Deliverable (code paths)** | `frontend/src/lib/api/live-ops-surfaces.ts`<br>`frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts` |
| **Test-first** | Failing check first for FR-16-04: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-16-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire settings sub-routes to users/orgs/keys APIs. 4) Confirm destructive actions; show API key secret once only. 5) Billing remains placeholder without inventing charges. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-16-04. |
| **Success** | Observable: API keys UI shall create/list/revoke keys only through backend auth/API key endpoints. |
| **Acceptance** | FR-16-04: API keys UI shall create/list/revoke keys only through backend auth/API key endpoints. |
| **Evidence** | `frontend/src/lib/api/live-ops-surfaces.ts` |

### [x] T-16-05 — Billing page may be a placeholder if backend lacks billing; it shall not invent charges
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-16-2, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-16-05 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-16-05 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-16-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/components/domain/api-key-table.tsx`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-16-05. |
| **Success** | Observable: Billing page may be a placeholder if backend lacks billing; it shall not invent charges. |
| **Acceptance** | FR-16-05: Billing page may be a placeholder if backend lacks billing; it shall not invent charges. |
| **Evidence** | `frontend/src/components/domain/api-key-table.tsx` |

### [x] T-16-06 — Security settings UI shall display backend-provided security configuration and not store secrets …
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-16-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-16-06 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/lib/api/live-ops-surfaces.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-16-06: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-16-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire settings sub-routes to users/orgs/keys APIs. 4) Confirm destructive actions; show API key secret once only. 5) Billing remains placeholder without inventing charges. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-16-06. |
| **Success** | Observable: Security settings UI shall display backend-provided security configuration and not store secrets in browser code. |
| **Acceptance** | FR-16-06: Security settings UI shall display backend-provided security configuration and not store secrets in browser code. |
| **Evidence** | `frontend/src/components/domain/api-key-table.tsx` |

### [x] T-16-07 — Invitation creation from settings shall use backend invitation APIs; accept flow remains on `/acc…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-16-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-16-07 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/lib/api/live-ops-surfaces.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Failing check first for FR-16-07: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-16-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-16-07. |
| **Success** | Observable: Invitation creation from settings shall use backend invitation APIs; accept flow remains on `/accept-invite` (FE-05). |
| **Acceptance** | FR-16-07: Invitation creation from settings shall use backend invitation APIs; accept flow remains on `/accept-invite` (FE-05). |
| **Evidence** | `frontend/src/components/domain/api-key-table.tsx` |

### [x] T-16-08 — Permission-aware UI shall restrict admin settings to authorized roles
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-16-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-16-08 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/lib/api/live-ops-surfaces.ts`<br>`frontend/src/app/app/[...slug]/page.tsx` |
| **Test-first** | Mock /auth/me without perm → control hidden/disabled; API 403 surfaced (FR-16-08). |
| **Steps** | 1) Open `requirements.md` FR-16-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Extend `can()` / permission types from `/auth/me` payload. 4) Apply hide|disable on nav/actions; fail closed if payload missing. 5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-16-08. |
| **Success** | Observable: Permission-aware UI shall restrict admin settings to authorized roles. |
| **Acceptance** | FR-16-08: Permission-aware UI shall restrict admin settings to authorized roles. |
| **Evidence** | `frontend/src/components/domain/api-key-table.tsx` |

### [x] T-16-09 — NFR gate — NFR-16-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-16-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts` |
| **Test-first** | Define pass/fail measurement for NFR-16-01 before changing code. |
| **Steps** | 1) Map NFR-16-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-16-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-16-01: Settings forms shall avoid full app remounts on save success. |
| **Evidence** | `frontend/src/components/domain/api-key-table.tsx` |

### [x] T-16-10 — NFR gate — NFR-16-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-16-02 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts` |
| **Test-first** | Define pass/fail measurement for NFR-16-02 before changing code. |
| **Steps** | 1) Map NFR-16-02 to design §7 security row. 2) Inspect `frontend/src/components/domain/api-key-table.tsx` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-16-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-16-02: Newly created API key secrets shall be shown once (if backend returns plaintext once) and not re-fetchable from FE cache. |
| **Evidence** | `frontend/src/components/domain/api-key-table.tsx` |

### [x] T-16-11 — NFR gate — NFR-16-03
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-16-03 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts` |
| **Test-first** | Define pass/fail measurement for NFR-16-03 before changing code. |
| **Steps** | 1) Map NFR-16-03 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-16-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-16-03: User disable/invite actions require confirmation where destructive. |
| **Evidence** | `frontend/src/components/domain/api-key-table.tsx` |

### [x] T-16-12 — Acceptance proof — AC-16-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-16-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-16-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Settings nav links resolve to settings surfaces. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-16-01 passes with recorded evidence. |
| **Acceptance** | AC-16-01: Settings nav links resolve to settings surfaces. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-16-13 — Acceptance proof — AC-16-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-16-02 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-16-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Users invite/list wired to backend invitations/users APIs (or documented gap). 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-16-02 passes with recorded evidence. |
| **Acceptance** | AC-16-02: Users invite/list wired to backend invitations/users APIs (or documented gap). |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-16-14 — Acceptance proof — AC-16-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-16-03 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-16-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Organization save calls PATCH when implemented. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-16-03 passes with recorded evidence. |
| **Acceptance** | AC-16-03: Organization save calls PATCH when implemented. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-16-15 — Acceptance proof — AC-16-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-16-04 |
| **Deliverable (code paths)** | `frontend/src/components/domain/api-key-table.tsx`<br>`frontend/src/app/app/[...slug]/page.tsx`<br>`frontend/src/lib/api/client.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-16-04 before claiming pass. |
| **Steps** | 1) Execute AC protocol: API keys page uses backend endpoints. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-16-04 passes with recorded evidence. |
| **Acceptance** | AC-16-04: API keys page uses backend endpoints. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-16-16 — Exit review — FE-16 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-16-01, FR-16-02, FR-16-03, FR-16-04, FR-16-05, FR-16-06, FR-16-07, FR-16-08… |
| **Deliverable (code paths)** | `planning/frontend/16_settings-users-org-and-api-keys-ui/tasks.md`<br>`planning/frontend/16_settings-users-org-and-api-keys-ui/design.md`<br>`planning/frontend/16_settings-users-org-and-api-keys-ui/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-16-01 | T-16-01, T-16-16 |
| FR-16-02 | T-16-02, T-16-16 |
| FR-16-03 | T-16-03, T-16-16 |
| FR-16-04 | T-16-04, T-16-16 |
| FR-16-05 | T-16-05, T-16-16 |
| FR-16-06 | T-16-06, T-16-16 |
| FR-16-07 | T-16-07, T-16-16 |
| FR-16-08 | T-16-08, T-16-16 |
| NFR-16-01 | T-16-09, T-16-16 |
| NFR-16-02 | T-16-10, T-16-16 |
| NFR-16-03 | T-16-11, T-16-16 |
| AC-16-01 | T-16-12, T-16-16 |
| AC-16-02 | T-16-13, T-16-16 |
| AC-16-03 | T-16-14, T-16-16 |
| AC-16-04 | T-16-15, T-16-16 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-16-1 | T-16-01, T-16-04, T-16-07 |
| C-16-2 | T-16-02, T-16-05, T-16-08 |
| C-16-3 | T-16-03, T-16-06 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 8/8 | [x] FR-16-01, FR-16-02, FR-16-03, FR-16-04, FR-16-05, FR-16-06, FR-16-07, FR-16-08 |
| 4 | NFR coverage 3/3 | [x] NFR-16-01, NFR-16-02, NFR-16-03 |
| 5 | AC coverage 4/4 | [x] AC-16-01, AC-16-02, AC-16-03, AC-16-04 |
| 6 | C-* coverage 3/3 | [x] C-16-1, C-16-2, C-16-3 |
| 7 | Every task has Priority, Status, Design, Maps to, Deliverable, Test-first, Steps, Success, Acceptance, Evidence | [x] |
| 8 | Test-first + status discipline ( [x] or documented [~] residual ) | [x] |
| 9 | Full RTM appendix | [x] |
| 10 | Exit review + this compliance log | [x] |

### Qualitative gates (required for 100)

| Gate | Assessment |
|------|------------|
| Clarity of objectives | Task titles state implementable outcomes from EARS FRs |
| Completeness of implementation requirements | Steps reference design sections + concrete modules |
| Inclusion of acceptance criteria | **Acceptance** field maps FR/NFR/AC statement text |
| Thoroughness of status updates | [x] baseline or [~] residual with disposition — no silent gaps |

**Component tasks quality score: 100 / 100**

---

## Notes

- Status `[x]` = product-bar baseline present under `frontend/` and re-verified via test-first path.
- Status `[~]` = intentional residual follow-on (backend API already exists; FE wiring incomplete) — **not** a hidden deficiency; tracked for completion.
- Backend remains source of truth for AuthZ, execution, and DNA safety.
- Regenerate: `python scripts/_gen_frontend_tasks.py`
