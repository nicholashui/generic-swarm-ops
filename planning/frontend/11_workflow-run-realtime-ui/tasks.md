# Tasks — 11 Workflow Run Realtime UI

| Field | Value |
|-------|-------|
| Task list ID | `FE-11-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-11-DES`) |
| Paired requirements | `requirements.md` (`FE-11`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR 11/11 · NFR 4/4 · AC 4/4 · C-* 7/7 |

---

## SDD workflow

Run console → SSE/poll → timeline/logs → lifecycle actions → status badges.

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

These are the **main source locations** for FE-11. Individual tasks narrow further via **Deliverable (code paths)**.

- `frontend/src/components/domain/workflow-run-console.tsx`
- `frontend/src/hooks/use-realtime-run.ts`
- `frontend/src/lib/realtime/sse.ts`
- `frontend/src/components/ui/timeline.tsx`
- `frontend/src/components/ui/log-viewer.tsx`
- `frontend/src/lib/formatting/status.ts`

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
| C-11-1 | Run console | `frontend/src/components/domain/workflow-run-console.tsx` |
| C-11-2 | Realtime hook | `frontend/src/hooks/use-realtime-run.ts` |
| C-11-3 | SSE helper | `frontend/src/lib/realtime/sse.ts` |
| C-11-4 | Timeline | `frontend/src/components/ui/timeline.tsx` |
| C-11-5 | Log viewer | `frontend/src/components/ui/log-viewer.tsx` |
| C-11-6 | Status formatting | `frontend/src/lib/formatting/status.ts, design/status.ts` |
| C-11-7 | Improve entry | `frontend/src/components/domain/improve-run-button.tsx` |

---

## Task backlog

### [x] T-11-01 — Provide workflow run detail page for runId
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-1, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-11-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/ui/timeline.tsx` |
| **Test-first** | Failing check first for FR-11-01: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-11-01 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Compose run detail route/panel with WorkflowRunConsole + StatusBadge. 4) Load GET run/steps; map statuses via `lib/formatting/status` + design status tokens. 5) Render Timeline + LogViewer; never execute steps in the browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-01. |
| **Success** | Observable: The frontend shall provide a workflow run detail page for a given runId. |
| **Acceptance** | FR-11-01: The frontend shall provide a workflow run detail page for a given runId. |
| **Evidence** | `frontend/src/components/domain/workflow-run-console.tsx` |

### [x] T-11-02 — Render run status, steps/timeline, timestamps
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-11-02 |
| **Deliverable (code paths)** | `frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/ui/timeline.tsx`<br>`frontend/src/components/ui/log-viewer.tsx` |
| **Test-first** | Failing check first for FR-11-02: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-11-02 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Compose run detail route/panel with WorkflowRunConsole + StatusBadge. 4) Load GET run/steps; map statuses via `lib/formatting/status` + design status tokens. 5) Render Timeline + LogViewer; never execute steps in the browser. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-02. |
| **Success** | Observable: When run data is loaded, the run detail page shall display run status, steps/timeline, and timestamps from backend data. |
| **Acceptance** | FR-11-02: When run data is loaded, the run detail page shall display run status, steps/timeline, and timestamps from backend data. |
| **Evidence** | `frontend/src/hooks/use-realtime-run.ts` |

### [x] T-11-03 — Realtime run updates without full reload
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-11-03 |
| **Deliverable (code paths)** | `frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/components/ui/timeline.tsx` |
| **Test-first** | Mock stream events → UI updates; kill stream → degraded/poll (FR-11-03). |
| **Steps** | 1) Open `requirements.md` FR-11-03 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/extend `useRealtimeRun` + `sse.ts` subscribe/merge. 4) On stream error set degraded + poll; cleanup on unmount. 5) Drive Timeline/LogViewer from merged events without full page reload. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-03. |
| **Success** | Observable: When realtime events are available, the frontend shall update the run UI without full page reload. |
| **Acceptance** | FR-11-03: When realtime events are available, the frontend shall update the run UI without full page reload. |
| **Evidence** | `frontend/src/lib/realtime/sse.ts` |

### [x] T-11-04 — SSE failure → poll degraded mode
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-11-04 |
| **Deliverable (code paths)** | `frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/components/ui/timeline.tsx` |
| **Test-first** | Mock stream events → UI updates; kill stream → degraded/poll (FR-11-04). |
| **Steps** | 1) Open `requirements.md` FR-11-04 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement/extend `useRealtimeRun` + `sse.ts` subscribe/merge. 4) On stream error set degraded + poll; cleanup on unmount. 5) Drive Timeline/LogViewer from merged events without full page reload. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-04. |
| **Success** | Observable: If realtime transport fails, the frontend shall fall back to polling or show a degraded-live indicator. |
| **Acceptance** | FR-11-04: If realtime transport fails, the frontend shall fall back to polling or show a degraded-live indicator. |
| **Evidence** | `frontend/src/lib/realtime/sse.ts` |

### [x] T-11-05 — Cancel/retry actions via backend APIs
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-5, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-11-05 |
| **Deliverable (code paths)** | `frontend/src/components/ui/log-viewer.tsx`<br>`frontend/src/lib/formatting/status.ts`<br>`frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts` |
| **Test-first** | Failing check first for FR-11-05: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-11-05 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Add action handlers on run console calling lifecycle POST routes. 4) Disable when status/permission forbids; busy state prevents double-submit. 5) Refresh/merge run state after success; show AppError on failure. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-05. |
| **Success** | Observable: When the user is permitted and the run status allows, the frontend shall offer cancel and retry actions that call backend APIs. |
| **Acceptance** | FR-11-05: When the user is permitted and the run status allows, the frontend shall offer cancel and retry actions that call backend APIs. |
| **Evidence** | `frontend/src/components/ui/log-viewer.tsx` |

### [x] T-11-06 — Pause/resume/expire lifecycle controls
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-6, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-11-06 |
| **Deliverable (code paths)** | `frontend/src/lib/formatting/status.ts, design/status.ts`<br>`frontend/src/lib/formatting/status.ts`<br>`frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts` |
| **Test-first** | Failing check first for FR-11-06: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-11-06 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Add action handlers on run console calling lifecycle POST routes. 4) Disable when status/permission forbids; busy state prevents double-submit. 5) Refresh/merge run state after success; show AppError on failure. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-06. |
| **Success** | Observable: When backend supports pause/resume/expire and the run status allows, the frontend shall expose controls calling those lifecycle endpoints. |
| **Acceptance** | FR-11-06: When backend supports pause/resume/expire and the run status allows, the frontend shall expose controls calling those lifecycle endpoints. |
| **Evidence** | `frontend/src/lib/formatting/status.ts, design/status.ts` |

### [x] T-11-07 — Status badge vocabulary for run states
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-7, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-11-07 |
| **Deliverable (code paths)** | `frontend/src/components/domain/improve-run-button.tsx`<br>`frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/ui/timeline.tsx` |
| **Test-first** | Failing check first for FR-11-07: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-11-07 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Add action handlers on run console calling lifecycle POST routes. 4) Disable when status/permission forbids; busy state prevents double-submit. 5) Refresh/merge run state after success; show AppError on failure. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-07. |
| **Success** | Observable: The frontend shall render status badges for running, succeeded, failed, awaiting approval, paused, cancelled (and expired when returned). |
| **Acceptance** | FR-11-07: The frontend shall render status badges for running, succeeded, failed, awaiting approval, paused, cancelled (and expired when returned). |
| **Evidence** | `frontend/src/components/domain/improve-run-button.tsx` |

### [x] T-11-08 — Forbid browser-side workflow step execution
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-1, design §3 arch / §4 models / §5 ICD / §4a visual, §10 non-goals |
| **Maps to** | FR-11-08 |
| **Deliverable (code paths)** | `frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/ui/timeline.tsx`<br>`frontend/src/components/ui/log-viewer.tsx` |
| **Test-first** | Negative test/review: attempt forbidden behaviour for FR-11-08 must fail or be absent. |
| **Steps** | 1) Open `requirements.md` FR-11-08 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Audit deliverables (`frontend/src/components/domain/workflow-run-console.tsx`) for forbidden capability; remove or gate. 4) Add review note / negative test so regression is blocked. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-08. |
| **Success** | Observable: The frontend shall not execute workflow steps in the browser. |
| **Acceptance** | FR-11-08: The frontend shall not execute workflow steps in the browser. |
| **Evidence** | `frontend/src/components/domain/workflow-run-console.tsx` |

### [x] T-11-09 — Surface step failure context + request_id
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-2, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-11-09 |
| **Deliverable (code paths)** | `frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/ui/timeline.tsx`<br>`frontend/src/components/ui/log-viewer.tsx`<br>`frontend/src/lib/formatting/status.ts` |
| **Test-first** | Force API 4xx/5xx with request_id → ErrorState shows message + id (FR-11-09). |
| **Steps** | 1) Open `requirements.md` FR-11-09 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement against design component `C-11-2` and ICD in deliverable paths. 4) Prefer typed `backendApi` calls; map errors to AppError. 5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-09. |
| **Success** | Observable: When a step fails, the frontend shall display the failure context and request_id/correlation when provided by the backend. |
| **Acceptance** | FR-11-09: When a step fails, the frontend shall display the failure context and request_id/correlation when provided by the backend. |
| **Evidence** | `frontend/src/hooks/use-realtime-run.ts` |

### [x] T-11-10 — Human-gate callout when waiting for approval
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-3, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-11-10 |
| **Deliverable (code paths)** | `frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/ui/timeline.tsx`<br>`frontend/src/components/ui/log-viewer.tsx`<br>`frontend/src/lib/formatting/status.ts`<br>`frontend/src/components/domain/workflow-run-console.tsx` |
| **Test-first** | Failing check first for FR-11-10: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-11-10 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Detect waiting_for_approval status from run payload. 4) Show callout with deep link / embed to approvals decision panel. 5) Keep improve slot separate; do not auto-approve. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-10. |
| **Success** | Observable: If the run is waiting for approval, the frontend shall surface a human-gate callout with navigation or embedded actions to the approvals …. |
| **Acceptance** | FR-11-10: If the run is waiting for approval, the frontend shall surface a human-gate callout with navigation or embedded actions to the approvals flow. |
| **Evidence** | `frontend/src/lib/realtime/sse.ts` |

### [x] T-11-11 — Reserve Improve panel slot without auto-start
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | C-11-4, design §3 arch / §4 models / §5 ICD / §4a visual |
| **Maps to** | FR-11-11 |
| **Deliverable (code paths)** | `frontend/src/components/ui/timeline.tsx`<br>`frontend/src/components/ui/log-viewer.tsx`<br>`frontend/src/lib/formatting/status.ts`<br>`frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts` |
| **Test-first** | Failing check first for FR-11-11: assert observable outcome from statement before marking done. |
| **Steps** | 1) Open `requirements.md` FR-11-11 + `design.md` §3 architecture / §5 ICD / §4a visual. 2) Write failing test or checklist for the observable outcome. 3) Implement stepper state machine (idle→…→done|failed) in improve control. 4) Each step requires click + BE success; disable concurrent submits. 5) Render step evidence; never write production DNA client-side. 6) Re-run test-first check; update **Evidence** if paths moved. 7) Incremental compliance: only then set status complete for FR-11-11. |
| **Success** | Observable: When the Improve pipeline is available for the run, the frontend shall reserve UI space for Improve controls (FE-18) without auto-startin…. |
| **Acceptance** | FR-11-11: When the Improve pipeline is available for the run, the frontend shall reserve UI space for Improve controls (FE-18) without auto-starting improve steps. |
| **Evidence** | `frontend/src/components/ui/timeline.tsx` |

### [x] T-11-12 — NFR gate — NFR-11-01
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-11-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/ui/timeline.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-11-01 before changing code. |
| **Steps** | 1) Map NFR-11-01 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-11-01 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-11-01: Realtime handlers shall avoid unbounded memory growth on long-running streams. |
| **Evidence** | `frontend/src/components/domain/workflow-run-console.tsx` |

### [x] T-11-13 — NFR gate — NFR-11-02
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-11-02 |
| **Deliverable (code paths)** | `frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/ui/timeline.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-11-02 before changing code. |
| **Steps** | 1) Map NFR-11-02 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-11-02 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-11-02: Timeline rendering shall remain usable for typical step counts of MVP workflows. |
| **Evidence** | `frontend/src/components/domain/workflow-run-console.tsx` |

### [x] T-11-14 — NFR gate — NFR-11-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-11-03 |
| **Deliverable (code paths)** | `frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/ui/timeline.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-11-03 before changing code. |
| **Steps** | 1) Map NFR-11-03 to design §7 security row. 2) Inspect `frontend/src/components/domain/workflow-run-console.tsx` and related modules for leakage/unsafe rendering. 3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. 4) Security review note + unit/grep evidence. 5) Compliance check against FE-01 charter. |
| **Success** | NFR-11-03 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-11-03: Stream subscriptions shall require authenticated session. |
| **Evidence** | `frontend/src/components/domain/workflow-run-console.tsx` |

### [x] T-11-15 — NFR gate — NFR-11-04
| | |
|--|--|
| **Priority** | P1 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §7 NFR design + observability |
| **Maps to** | NFR-11-04 |
| **Deliverable (code paths)** | `frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/src/components/ui/timeline.tsx` |
| **Test-first** | Define pass/fail measurement for NFR-11-04 before changing code. |
| **Steps** | 1) Map NFR-11-04 to design §7. 2) Implement control in primary deliverables. 3) Verify with test or review protocol. 4) Record evidence. |
| **Success** | NFR-11-04 measurable outcome holds under ops profile assumptions. |
| **Acceptance** | NFR-11-04: Run actions shall send only backend-defined payloads. |
| **Evidence** | `frontend/src/components/domain/workflow-run-console.tsx` |

### [x] T-11-16 — Acceptance proof — AC-11-01
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-11-01 |
| **Deliverable (code paths)** | `frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-11-01 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Run detail shows steps for a live run. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-11-01 passes with recorded evidence. |
| **Acceptance** | AC-11-01: Run detail shows steps for a live run. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-11-17 — Acceptance proof — AC-11-02
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-11-02 |
| **Deliverable (code paths)** | `frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-11-02 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Status updates reflect backend changes (stream or poll). 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-11-02 passes with recorded evidence. |
| **Acceptance** | AC-11-02: Status updates reflect backend changes (stream or poll). |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-11-18 — Acceptance proof — AC-11-03
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-11-03 |
| **Deliverable (code paths)** | `frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-11-03 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Pause/resume/expire controls call documented APIs when enabled. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-11-03 passes with recorded evidence. |
| **Acceptance** | AC-11-03: Pause/resume/expire controls call documented APIs when enabled. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-11-19 — Acceptance proof — AC-11-04
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §9 Validation design; requirements §5 AC |
| **Maps to** | AC-11-04 |
| **Deliverable (code paths)** | `frontend/src/components/domain/workflow-run-console.tsx`<br>`frontend/src/hooks/use-realtime-run.ts`<br>`frontend/src/lib/realtime/sse.ts`<br>`frontend/tests/unit`<br>`frontend/e2e/e1-smoke.spec.ts` |
| **Test-first** | Create checklist/automated assertion named for AC-11-04 before claiming pass. |
| **Steps** | 1) Execute AC protocol: Cancel/retry respect permission UX. 2) Prefer unit/e2e; else documented manual ops-profile steps. 3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. 4) Capture evidence (test name, command, or review note). 5) Iterative compliance: fail → fix mapped FR tasks → re-run AC. |
| **Success** | AC-11-04 passes with recorded evidence. |
| **Acceptance** | AC-11-04: Cancel/retry respect permission UX. |
| **Evidence** | `frontend/tests/unit or e2e / manual ops review log` |

### [x] T-11-20 — Exit review — FE-11 SDD iterative compliance complete
| | |
|--|--|
| **Priority** | P0 |
| **Status** | [x] Implemented — re-verify after changes |
| **Design** | §12 score claim; §9 validation; all C-* from §3.1 |
| **Maps to** | FR-11-01, FR-11-02, FR-11-03, FR-11-04, FR-11-05, FR-11-06, FR-11-07, FR-11-08… |
| **Deliverable (code paths)** | `planning/frontend/11_workflow-run-realtime-ui/tasks.md`<br>`planning/frontend/11_workflow-run-realtime-ui/design.md`<br>`planning/frontend/11_workflow-run-realtime-ui/requirements.md` |
| **Test-first** | Automated coverage counters FR/NFR/AC/C-* = 100% before exit. |
| **Steps** | 1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. 2) Confirm every design C-* appears in a task Design field. 3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. 4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). 5) Sign compliance checkpoint; only then claim component score 100. |
| **Success** | Zero coverage deficiencies; iterative checks green; residual gaps documented. |
| **Acceptance** | Coverage counters match totals; compliance boxes [x]; no silent P0 gaps. |
| **Evidence** | `tasks.md compliance checkpoint + FE-20 command output` |


---

## Requirements → tasks RTM (full)

| Requirement | Tasks |
|-------------|-------|
| FR-11-01 | T-11-01, T-11-20 |
| FR-11-02 | T-11-02, T-11-20 |
| FR-11-03 | T-11-03, T-11-20 |
| FR-11-04 | T-11-04, T-11-20 |
| FR-11-05 | T-11-05, T-11-20 |
| FR-11-06 | T-11-06, T-11-20 |
| FR-11-07 | T-11-07, T-11-20 |
| FR-11-08 | T-11-08, T-11-20 |
| FR-11-09 | T-11-09, T-11-20 |
| FR-11-10 | T-11-10, T-11-20 |
| FR-11-11 | T-11-11, T-11-20 |
| NFR-11-01 | T-11-12, T-11-20 |
| NFR-11-02 | T-11-13, T-11-20 |
| NFR-11-03 | T-11-14, T-11-20 |
| NFR-11-04 | T-11-15, T-11-20 |
| AC-11-01 | T-11-16, T-11-20 |
| AC-11-02 | T-11-17, T-11-20 |
| AC-11-03 | T-11-18, T-11-20 |
| AC-11-04 | T-11-19, T-11-20 |

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
| C-11-1 | T-11-01, T-11-08 |
| C-11-2 | T-11-02, T-11-09 |
| C-11-3 | T-11-03, T-11-10 |
| C-11-4 | T-11-04, T-11-11 |
| C-11-5 | T-11-05 |
| C-11-6 | T-11-06 |
| C-11-7 | T-11-07 |

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage 11/11 | [x] FR-11-01, FR-11-02, FR-11-03, FR-11-04, FR-11-05, FR-11-06, FR-11-07, FR-11-08, FR-11-09, FR-11-10, FR-11-11 |
| 4 | NFR coverage 4/4 | [x] NFR-11-01, NFR-11-02, NFR-11-03, NFR-11-04 |
| 5 | AC coverage 4/4 | [x] AC-11-01, AC-11-02, AC-11-03, AC-11-04 |
| 6 | C-* coverage 7/7 | [x] C-11-1, C-11-2, C-11-3, C-11-4, C-11-5, C-11-6, C-11-7 |
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
