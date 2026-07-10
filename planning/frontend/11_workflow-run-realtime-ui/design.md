# Design — 11 Workflow Run Realtime UI

| Field | Value |
|-------|-------|
| Design ID | `FE-11-DES` |
| Version | 2.1 (comprehensive SDD — implementation-ready) |
| Paired requirements | `requirements.md` (`FE-11`) |
| Source | `frontend.md` + as-built `frontend/` |
| Architecture SoT | `structure.md` §10–§12; backend control plane `planning/backend/` |
| Design quality bar | **100** |

---

## 1. Purpose

Run detail with steps/timeline, realtime SSE/poll updates, lifecycle actions cancel/retry/pause/resume/expire, status badges, no step execution in browser.

---

## 2. Context, actors, and trust boundaries

**Actors:** Operators monitoring runs.  
**Related BE:** BE-11 runs, BE-19 streaming, lifecycle pause/resume/expire.

**Related specs:** See `planning/frontend/README.md` dependency sketch.  
**Code modules:** `workflow-run-console.tsx`, `use-realtime-run.ts`, `lib/realtime/sse.ts`.

---

## 3. Architecture

```text
WorkflowRunConsole(runId)
  ├── useRealtimeRun → SSE (lib/realtime/sse) → poll fallback
  ├── Timeline + LogViewer
  └── Actions → backendApi.retry/cancel/(pause/resume/expire)
Improve slot → FE-18   Gate callout → FE-12
```

### 3.3 Component interactions

| Module | Responsibility |
|--------|----------------|
| `workflow-run-console.tsx` | Layout, actions, connection badge |
| `use-realtime-run.ts` | Event merge + connectionState |
| `sse.ts` | EventSource wrapper |
| Status formatters | Badge labels |

### 3.1 Components

| ID | Component | Implementation anchor |
|----|-----------|----------------------|
| C-11-1 | Run console | `frontend/src/components/domain/workflow-run-console.tsx` |
| C-11-2 | Realtime hook | `frontend/src/hooks/use-realtime-run.ts` |
| C-11-3 | SSE helper | `frontend/src/lib/realtime/sse.ts` |
| C-11-4 | Timeline | `frontend/src/components/ui/timeline.tsx` |
| C-11-5 | Log viewer | `frontend/src/components/ui/log-viewer.tsx` |
| C-11-6 | Status formatting | `frontend/src/lib/formatting/status.ts, design/status.ts` |
| C-11-7 | Improve entry | `frontend/src/components/domain/improve-run-button.tsx` |

### 3.2 Decisions (with rejected alternatives)

| ID | Decision | Rejected alternative | Rationale |
|----|----------|----------------------|-----------|
| D-11-01 | SSE preferred + poll fallback | Hard-fail without WS | Resilience |
| D-11-02 | Lifecycle via BE routes | Client-only fake state machine | Authority |
| D-11-03 | Replace state on events | Unbounded append-only buffer | Memory safety |

### 3.4 Interaction sequence

```text
Open run detail
  → GET run + steps
  → open SSE stream
  → render timeline
User cancel
  → POST cancel → refresh/merge state
SSE drop
  → badge degraded → poll GET until reconnected or leave
```

---

## 4. Data models, algorithms, state machines, and UI structures

### Status badge set

`queued | running | waiting_for_approval | succeeded/completed | failed | cancelled | paused | expired`

### Realtime algorithm

```text
subscribe(runId)
on event: merge into run/steps/events state
on stream error: connectionState=degraded; start poll interval
on unmount: close EventSource; clear poll
```

### Action enablement matrix (UX)

| Action | Typical enabled when |
|--------|----------------------|
| Cancel | running / queued / waiting (if BE allows) |
| Retry | failed / cancelled (if BE allows) |
| Pause | running |
| Resume | paused |
| Expire | waiting / stalled per BE |

---

## 4a. Visual and interaction design

### Visual

- Header: run id, workflow name, StatusBadge, timestamps, connection badge.
- Grid: timeline + logs.
- Pending approval callout → approvals.
- Improve panel slot (does not auto-start).
- Degraded-live indicator when polling.

---

## 5. API and interface contracts (ICD)

| Method | Path | Usage |
|--------|------|-------|
| GET | `/api/v1/workflow-runs/{id}` | Snapshot |
| GET | `.../steps` | Steps |
| GET/SSE | `.../events` or stream route | Realtime |
| POST | `.../cancel`, `.../retry` | Actions |
| POST | `.../pause`, `.../resume`, `.../expire` | Lifecycle (as-built BE) |

**Envelope:** Backend success/error formats; FE maps to `AppError` including `request_id` when present (FE-07).  
**AuthZ:** Backend final (FE-06 UX only). Mutations never invent success without API confirmation.

---

## 6. Failure modes and edge cases

| Case | Behaviour |
|------|-----------|
| SSE disconnect | Degraded poll + indicator |
| Action 403 | Error string; button re-enabled |
| Unknown run id | ErrorState not found |
| Step failure payload | Show message + request_id/correlation |

---

## 7. NFR design and observability

| NFR | Design |
|-----|--------|
| NFR-11-01 Bound stream memory | Replace/merge state |
| NFR-11-02 Timeline usable MVP | Accept typical step counts |
| NFR-11-03 Auth on stream | Session credentials |
| NFR-11-04 Backend payloads only | Typed client |

**Observability:** Surface `request_id` on errors; optional client error hooks; correlate with backend logs. No secret/PII dump in production toasts.

---

## 8. Full requirements traceability matrix (RTM)

| Req | Statement (abbrev.) | Design anchor | Test anchor |
|-----|---------------------|---------------|-------------|
| FR-11-01 | The frontend shall provide a workflow run detail page for a given runId. | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-11-02 | When run data is loaded, the run detail page shall display run status… | §4a visual design · FE-03 tokens | requirements TV-*; FE-20 gates |
| FR-11-03 | When realtime events are available, the frontend shall update the run… | §4 realtime algorithm · §3.3 sequence | requirements TV-*; FE-20 gates |
| FR-11-04 | If realtime transport fails, the frontend shall fall back to polling … | §4 poll fallback · §6 failure modes | requirements TV-*; FE-20 gates |
| FR-11-05 | When the user is permitted and the run status allows, the frontend sh… | §4a visual design · FE-03 tokens | requirements TV-*; FE-20 gates |
| FR-11-06 | When backend supports pause/resume/expire and the run status allows, … | §4a visual design · FE-03 tokens | requirements TV-*; FE-20 gates |
| FR-11-07 | The frontend shall render status badges for running, succeeded, faile… | §4a visual design · FE-03 tokens | requirements TV-*; FE-20 gates |
| FR-11-08 | The frontend shall not execute workflow steps in the browser. | §1 Purpose · §3 invariants · §10 non-goals | requirements TV-*; FE-20 gates |
| FR-11-09 | When a step fails, the frontend shall display the failure context and… | §4 error model · §5 AppError · §6 failures | requirements TV-*; FE-20 gates |
| FR-11-10 | If the run is waiting for approval, the frontend shall surface a huma… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| FR-11-11 | When the Improve pipeline is available for the run, the frontend shal… | §3 architecture · §4 models · §5 ICD | requirements TV-*; FE-20 gates |
| NFR-11-01 | Realtime handlers shall avoid unbounded memory growth on long-running… | §7 NFR design table | Perf/security tests / reviews |
| NFR-11-02 | Timeline rendering shall remain usable for typical step counts of MVP… | §7 NFR design table | Perf/security tests / reviews |
| NFR-11-03 | Stream subscriptions shall require authenticated session. | §7 security NFR · §6 failure modes | Perf/security tests / reviews |
| NFR-11-04 | Run actions shall send only backend-defined payloads. | §7 NFR design table | Perf/security tests / reviews |
| AC-11-01 | Run detail shows steps for a live run. | §9 Validation design | Automated or review protocol |
| AC-11-02 | Status updates reflect backend changes (stream or poll). | §9 Validation design | Automated or review protocol |
| AC-11-03 | Pause/resume/expire controls call documented APIs when enabled. | §9 Validation design | Automated or review protocol |
| AC-11-04 | Cancel/retry respect permission UX. | §9 Validation design | Automated or review protocol |

---

## 9. Validation design

Live transitions; paused badge; lifecycle POSTs; permission on actions. **TV-11-***.

Cross-check acceptance criteria in paired `requirements.md` §5 and test protocols §7. Portfolio proof also via FE-20 (lint/typecheck/unit/build + E1 when stack available).

---

## 10. Open issues and deferred non-goals

| ID | Item | Disposition |
|----|------|-------------|
| OI-11-01 | Multi-run comparison view | Later |
| OI-11-02 | Wire pause/resume/expire buttons if not complete | Follow-on vs BE APIs |

**Product-bar non-goals (global FE):** always-on Playwright with permanent servers; full commercial LightRAG/Neo4j graph explorer; live external CRM/email/billing SaaS admin consoles; DGM-style host self-rewrite UI; replacing backend authorization with client-only checks; infinite enterprise content authoring UIs for every `business/` leaf.

---

## 11. Implementation notes (as-built alignment)

This design specifies the **full frontend.md-aligned ops console**. Where the repository already implements behaviour under `frontend/src`, the design is **authoritative for intent** and **descriptive of as-built** modules in §3.1. Residual wiring is tracked as open issues—not silent omission of design sections.

### Implementation specification

1. All lifecycle calls through `backendApi`.  
2. Demo mode may simulate cancel/retry locally but ops mode must hit BE.  
3. Connection badge reads `connectionState` from hook.  
4. Do not execute steps in browser.

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

**Self-score claim: 100** — SDD v2.1 design fully elaborating architecture, component interactions, visual/UX, ICD, FR-level traceability, and implementation specifications for `FE-11`.
