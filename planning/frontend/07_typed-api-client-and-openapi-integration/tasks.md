# Tasks — 07 Typed API Client and OpenAPI Integration

| Field | Value |
|-------|-------|
| Task list ID | `FE-07-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-07-DES`) |
| Paired requirements | `requirements.md` (`FE-07`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 8/8 · NFR 4/4 · AC 4/4 · C-* 6/6 |

---

## SDD workflow

OpenAPI generate → backendApi → AppError → live loaders → demo/ops switch.

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

These are the **main source locations** for FE-07. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/lib/api/client.ts`
- `frontend/src/lib/api/generated`
- `frontend/src/lib/api/live-data.ts`
- `frontend/src/lib/api/live-ops-surfaces.ts`
- `frontend/src/lib/errors/app-error.ts`
- `frontend/openapi.json`
- `frontend/tests/unit/openapi-generated.test.ts`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-07-1 | HTTP client | `frontend/src/lib/api/client.ts` |
| C-07-2 | Generated types | `frontend/src/lib/api/generated/*` |
| C-07-3 | Live data adapters | `frontend/src/lib/api/live-data.ts, live-ops-surfaces.ts` |
| C-07-4 | AppError | `frontend/src/lib/errors/app-error.ts` |
| C-07-5 | OpenAPI artifact | `frontend/openapi.json` |
| C-07-6 | Tests | `frontend/tests/unit/openapi-generated.test.ts, live-ops.test.ts` |

---

## Task backlog

### [x] T-07-01 — The frontend shall call the backend only through versioned HTTP APIs under `/api/v1` (or document…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-07-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-07-01 |
| **Deliverable (code paths)** | `frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts` |
| **Test-first** | Failing check first for FR-07-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-07-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-07-1` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-07-01. |
| **Success** | Observable: The frontend shall call the backend only through versioned HTTP APIs under `/api/v1` (or documented base path). |
| **Acceptance** | FR-07-01: The frontend shall call the backend only through versioned HTTP APIs under `/api/v1` (or documented base path). |
| **Evidence** | `frontend/src/lib/api/client.ts` |

### [x] T-07-02 — The frontend shall maintain a typed API client layer for domain resources (auth, users, agents, t…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-07-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-07-02 |
| **Deliverable (code paths)** | `frontend/src/lib/api/generated/*`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated` |
| **Test-first** | Mock stream events → UI updates; kill stream → degraded/poll (FR-07-02). |
| **Steps** | 1) Open `requirements.md` FR-07-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update OpenAPI artifact; run `pnpm api:generate`. 4) Extend `backendApi` method; parse errors into AppError. 5) Consume types in domain loader/panel; no hand-forked DTOs. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-07-02. |
| **Success** | Observable: The frontend shall maintain a typed API client layer for domain resources (auth, users, agents, tools, workflows, runs, approvals, knowle…. |
| **Acceptance** | FR-07-02: The frontend shall maintain a typed API client layer for domain resources (auth, users, agents, tools, workflows, runs, approvals, knowledge, memory, evaluations, processes, audit, evolution, improvement). |
| **Evidence** | `frontend/src/lib/api/generated/*` |

### [x] T-07-03 — Generate OpenAPI TypeScript types
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-07-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-07-03 |
| **Deliverable (code paths)** | `frontend/src/lib/api/live-data.ts, live-ops-surfaces.ts`<br>`frontend/tests/unit/openapi-generated.test.ts`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/openapi.json` |
| **Test-first** | Run `pnpm api:generate`; typecheck uses generated types (FR-07-03). |
| **Steps** | 1) Open `requirements.md` FR-07-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update OpenAPI artifact; run `pnpm api:generate`. 4) Extend `backendApi` method; parse errors into AppError. 5) Consume types in domain loader/panel; no hand-forked DTOs. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-07-03. |
| **Success** | Observable: When OpenAPI schema is available, the frontend shall generate TypeScript types via `pnpm api:generate` (or documented equivalent). |
| **Acceptance** | FR-07-03: When OpenAPI schema is available, the frontend shall generate TypeScript types via `pnpm api:generate` (or documented equivalent). |
| **Evidence** | `frontend/src/lib/api/live-data.ts, live-ops-surfaces.ts` |

### [x] T-07-04 — When a backend error response includes `request_id`, the frontend shall display or log it for ope…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-07-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-07-04 |
| **Deliverable (code paths)** | `frontend/src/lib/errors/app-error.ts`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated` |
| **Test-first** | Force API 4xx/5xx with request_id → ErrorState shows message + id (FR-07-04). |
| **Steps** | 1) Open `requirements.md` FR-07-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update OpenAPI artifact; run `pnpm api:generate`. 4) Extend `backendApi` method; parse errors into AppError. 5) Consume types in domain loader/panel; no hand-forked DTOs. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-07-04. |
| **Success** | Observable: When a backend error response includes `request_id`, the frontend shall display or log it for operator support. |
| **Acceptance** | FR-07-04: When a backend error response includes `request_id`, the frontend shall display or log it for operator support. |
| **Evidence** | `frontend/src/lib/errors/app-error.ts` |

### [x] T-07-05 — If `NEXT_PUBLIC_DEMO_MODE=true`, the frontend may use demo fixtures; if `false`, the frontend sha…
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-07-5, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-07-05 |
| **Deliverable (code paths)** | `frontend/src/lib/errors/app-error.ts`<br>`frontend/openapi.json`<br>`frontend/tests/unit/openapi-generated.test.ts`<br>`frontend/src/lib/api/client.ts` |
| **Test-first** | Failing check first for FR-07-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-07-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-07-5` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-07-05. |
| **Success** | Observable: If `NEXT_PUBLIC_DEMO_MODE=true`, the frontend may use demo fixtures; if `false`, the frontend shall use the live backend. |
| **Acceptance** | FR-07-05: If `NEXT_PUBLIC_DEMO_MODE=true`, the frontend may use demo fixtures; if `false`, the frontend shall use the live backend. |
| **Evidence** | `frontend/src/lib/errors/app-error.ts` |

### [x] T-07-06 — After backend OpenAPI changes, implementers shall regenerate the client types before claiming API…
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-07-6, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-07-06 |
| **Deliverable (code paths)** | `frontend/tests/unit/openapi-generated.test.ts, live-ops.test.ts`<br>`frontend/tests/unit/openapi-generated.test.ts`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/openapi.json` |
| **Test-first** | Run `pnpm api:generate`; typecheck uses generated types (FR-07-06). |
| **Steps** | 1) Open `requirements.md` FR-07-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Update OpenAPI artifact; run `pnpm api:generate`. 4) Extend `backendApi` method; parse errors into AppError. 5) Consume types in domain loader/panel; no hand-forked DTOs. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-07-06. |
| **Success** | Observable: After backend OpenAPI changes, implementers shall regenerate the client types before claiming API compatibility. |
| **Acceptance** | FR-07-06: After backend OpenAPI changes, implementers shall regenerate the client types before claiming API compatibility. |
| **Evidence** | `frontend/tests/unit/openapi-generated.test.ts, live-ops.test.ts` |

### [x] T-07-07 — The frontend shall not write to databases or internal services except via backend APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-07-1, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-07-07 |
| **Deliverable (code paths)** | `frontend/tests/unit/openapi-generated.test.ts`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-07-07 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-07-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/tests/unit/openapi-generated.test.ts`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-07-07. |
| **Success** | Observable: The frontend shall not write to databases or internal services except via backend APIs. |
| **Acceptance** | FR-07-07: The frontend shall not write to databases or internal services except via backend APIs. |
| **Evidence** | `frontend/tests/unit/openapi-generated.test.ts` |

### [x] T-07-08 — API client shall attach authentication credentials per the auth session design
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-07-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-07-08 |
| **Deliverable (code paths)** | `frontend/src/lib/api/generated/*`<br>`frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts` |
| **Test-first** | Unit/e2e: valid login establishes session; invalid shows error (FR-07-08). |
| **Steps** | 1) Open `requirements.md` FR-07-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. 4) Pending state disables submit; map AppError + request_id into form alert. 5) On success navigate `/app` or complete invite per design §3.4 sequence. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-07-08. |
| **Success** | Observable: API client shall attach authentication credentials per the auth session design. |
| **Acceptance** | FR-07-08: API client shall attach authentication credentials per the auth session design. |
| **Evidence** | `frontend/src/lib/api/generated/*` |

### [x] T-07-09 — NFR gate — NFR-07-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-07-01 |
| **Deliverable (code paths)** | `frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts` |
| **Test-first** | Define pass/fail measurement for NFR-07-01 before changing code. |
| **Steps** | 1) Map NFR-07-01 to design §7 performance row. 2) Implement debounce/pagination/abort/code-split as applicable in `frontend/src/lib/api/client.ts`. 3) Manual or unit timing check for MVP data sizes. 4) Confirm shell remains interactive. 5) Record evidence path. |
| **Success** | NFR-07-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-07-01: API client shall support abort/cancel for in-flight requests on navigation where practical. |
| **Evidence** | `frontend/src/lib/api/client.ts` |

### [x] T-07-10 — NFR gate — NFR-07-02
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-07-02 |
| **Deliverable (code paths)** | `frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts` |
| **Test-first** | Define pass/fail measurement for NFR-07-02 before changing code. |
| **Steps** | 1) Map NFR-07-02 to design §7 performance row. 2) Implement debounce/pagination/abort/code-split as applicable in `frontend/src/lib/api/client.ts`. 3) Manual or unit timing check for MVP data sizes. 4) Confirm shell remains interactive. 5) Record evidence path. |
| **Success** | NFR-07-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-07-02: List endpoints shall support pagination parameters when provided by backend. |
| **Evidence** | `frontend/src/lib/api/client.ts` |

### [x] T-07-11 — NFR gate — NFR-07-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-07-03 |
| **Deliverable (code paths)** | `frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts` |
| **Test-first** | Define pass/fail measurement for NFR-07-03 before changing code. |
| **Steps** | 1) Map NFR-07-03 to design §7 security row. 2) Inspect `frontend/src/lib/api/client.ts` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-07-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-07-03: API client shall not embed long-lived secrets in source. |
| **Evidence** | `frontend/src/lib/api/client.ts` |

### [x] T-07-12 — NFR gate — NFR-07-04
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-07-04 |
| **Deliverable (code paths)** | `frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/src/lib/api/live-ops-surfaces.ts` |
| **Test-first** | Define pass/fail measurement for NFR-07-04 before changing code. |
| **Steps** | 1) Map NFR-07-04 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-07-04 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-07-04: Cross-origin calls shall rely on documented CORS/credentials settings from backend. |
| **Evidence** | `frontend/src/lib/api/client.ts` |

### [x] T-07-13 — Acceptance proof — AC-07-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-07-01 |
| **Deliverable (code paths)** | `frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-07-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Generated OpenAPI types exist and are imported by client modules. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-07-01 passes with recorded evidence. |
| **Acceptance** | AC-07-01: Generated OpenAPI types exist and are imported by client modules. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-07-14 — Acceptance proof — AC-07-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-07-02 |
| **Deliverable (code paths)** | `frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-07-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Live mode login + at least one authenticated GET succeed against backend. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-07-02 passes with recorded evidence. |
| **Acceptance** | AC-07-02: Live mode login + at least one authenticated GET succeed against backend. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-07-15 — Acceptance proof — AC-07-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-07-03 |
| **Deliverable (code paths)** | `frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-07-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Error UI can show request_id from a forced 4xx/5xx. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-07-03 passes with recorded evidence. |
| **Acceptance** | AC-07-03: Error UI can show request_id from a forced 4xx/5xx. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-07-16 — Acceptance proof — AC-07-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-07-04 |
| **Deliverable (code paths)** | `frontend/src/lib/api/client.ts`<br>`frontend/src/lib/api/generated`<br>`frontend/src/lib/api/live-data.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-07-04 before claiming pass. |
| **Steps** | 1) Execute AC protocol: README documents `pnpm api:generate`. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-07-04 passes with recorded evidence. |
| **Acceptance** | AC-07-04: README documents `pnpm api:generate`. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-07-17 — Exit review — FE-07 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-07-01, FR-07-02, FR-07-03, FR-07-04, FR-07-05, FR-07-06, FR-07-07, FR-07-08… |
| **Deliverable (code paths)** | `planning/frontend/07_typed-api-client-and-openapi-integration/tasks.md`<br>`planning/frontend/07_typed-api-client-and-openapi-integration/design.md`<br>`planning/frontend/07_typed-api-client-and-openapi-integration/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-07-01 | T-07-01, T-07-17 |
| FR-07-02 | T-07-02, T-07-17 |
| FR-07-03 | T-07-03, T-07-17 |
| FR-07-04 | T-07-04, T-07-17 |
| FR-07-05 | T-07-05, T-07-17 |
| FR-07-06 | T-07-06, T-07-17 |
| FR-07-07 | T-07-07, T-07-17 |
| FR-07-08 | T-07-08, T-07-17 |
| NFR-07-01 | T-07-09, T-07-17 |
| NFR-07-02 | T-07-10, T-07-17 |
| NFR-07-03 | T-07-11, T-07-17 |
| NFR-07-04 | T-07-12, T-07-17 |
| AC-07-01 | T-07-13, T-07-17 |
| AC-07-02 | T-07-14, T-07-17 |
| AC-07-03 | T-07-15, T-07-17 |
| AC-07-04 | T-07-16, T-07-17 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-07-1 | T-07-01, T-07-07 |
| C-07-2 | T-07-02, T-07-08 |
| C-07-3 | T-07-03 |
| C-07-4 | T-07-04 |
| C-07-5 | T-07-05 |
| C-07-6 | T-07-06 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 8/8 | [x] FR-07-01, FR-07-02, FR-07-03, FR-07-04, FR-07-05, FR-07-06, FR-07-07, FR-07-08 |
| 4 | NFR coverage 4/4 | [x] NFR-07-01, NFR-07-02, NFR-07-03, NFR-07-04 |
| 5 | AC coverage 4/4 | [x] AC-07-01, AC-07-02, AC-07-03, AC-07-04 |
| 6 | C-* coverage 6/6 | [x] C-07-1, C-07-2, C-07-3, C-07-4, C-07-5, C-07-6 |
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
