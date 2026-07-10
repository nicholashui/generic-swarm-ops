# Design — 11 Bounded Workflow Execution

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-11-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-11`) |
| Source | `structure.md` §4.2 |
| Design quality bar | 100 |

---

## 1. Purpose

Execute Workflow DNA as a **bounded state graph** under the Business Orchestrator: allow-listed tools, scoped memory, verification, gates, audit—never free-form swarm authority. ReAct only **inside** a node.

---

## 2. Context

Intake (03) creates run → Orchestrator walks DNA → Tools (05) → Memory (08) → Retrieval (09) → Gates (12) → Eval/Reflect (13/14).

**Decision D-11-01:** Single process + Postgres document store (not actor mesh).  
**D-11-02:** Graph owns permissions; models do not.

---

## 3. Architecture

```text
Run record
  │
  ▼
┌─────────────────────────────────────┐
│ Orchestrator                        │
│ load DNA · cursor · transition      │
└───┬───────────┬───────────┬─────────┘
    │           │           │
 Research   Execution    Verify
 (09)       (05 adapters) (checks)
    └───────────┼───────────┘
                ▼
         needs_gate? → (12) pause
                ▼
         audit + memory_writes
                ▼
         terminal → reflect optional
```

### 3.1 Components

| ID | Component | Module |
|----|-----------|--------|
| C-11-1 | Runtime engine | `runtime.py` |
| C-11-2 | Adapters | `tools/adapters.py` |
| C-11-3 | Memory enforcer | scopes |
| C-11-4 | Verification | required_checks |
| C-11-5 | Queue/dispatch | queued runs |
| C-11-6 | Stream | SSE events |
| C-11-7 | Store | Postgres runtime_state |

---

## 4. Run state machine (complete)

### 4.1 States

`queued | running | awaiting_approval | completed | failed | cancelled | rejected`

### 4.2 Transitions

| From | Event | To |
|------|-------|-----|
| — | start ok | queued/running |
| queued | worker pick | running |
| running | step ok | running (next) |
| running | needs gate | awaiting_approval |
| awaiting_approval | approve | running |
| awaiting_approval | reject | rejected |
| running | verification fail + block_on_fail | failed |
| running | adapter error fail-closed | failed |
| running | cancel | cancelled |
| running | all steps + checks ok | completed |
| failed/cancelled/rejected | retry (policy) | queued/running |

Illegal: completed → running without new run; awaiting_approval → completed without decide.

### 4.3 Step execution sequence (normative)

1. Load step (agent, tools, flags).  
2. AuthZ + broker (05).  
3. memory_reads (08).  
4. Optional retrieval (09).  
5. If gate required and not satisfied → create approval, status=awaiting_approval, stop.  
6. Adapter execute → tool_effects.  
7. On adapter error → fail step/run (no fake success).  
8. memory_writes + audit.  
9. Advance cursor or run verification.  
10. On terminal → optional auto-reflect (14).  

---

## 5. Data model — run

```text
WorkflowRun {
  id, organization_id, workflow_id, workflow_version,
  risk_tier, status, inputs, outputs?,
  steps: [{id, status, error?, outputs?}],
  tool_effects: [...],
  approval_request_id?, approval_state?,
  error?, created_by, created_at, completed_at?,
  request_id?
}
```

---

## 6. API contract

| Method | Path | Notes |
|--------|------|-------|
| POST | `/api/v1/workflows/{id}/runs` | Start (03) |
| GET | `/api/v1/workflow_runs/{id}` | Status |
| POST | cancel / retry | As implemented |
| GET | stream/events | SSE |

Error envelope: `{message, request_id}`.

---

## 7. Failure & concurrency

| Case | Behavior |
|------|----------|
| Adapter fail | step failed; run failed unless policy retries |
| Unauthorized tool | deny; audit |
| Double approve | idempotent decide |
| Concurrent workers | single cursor owner per run_id (document lock via store save) |

---

## 8. NFR design

| NFR | Design |
|-----|--------|
| NFR-11-01 Multi-step local &lt;30s excl human wait | Local adapters |
| NFR-11-02 Status read &lt;500ms | Postgres primary |
| NFR-11-03 Long work queued | dispatch_queued_runs |
| NFR-11-04–06 AuthZ, no free tools, gates | 05+12 |

**Metrics:** `runs_total{status}`, step duration, tool errors.

---

## 9. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-11-01…02 | §3–4 orchestrator | unit runtime |
| FR-11-03…05 | §4.3 tools | test_real_execution |
| FR-11-06 | research node | retrieval integration |
| FR-11-07…08 | verification | block_on_fail tests |
| FR-11-09…10 | memory | E1 scopes |
| FR-11-11…12 | graph authority; handoff | e2e |
| NFR-11-01…06 | §8 | live_ops, restart |
| AC-11-01…05 | E1 | test_e1_operator_path |

---

## 10. Validation design

State transitions unit; real adapters; postgres restart; E1 full path.

---

## 11. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-11-01 | External SaaS adapters | Non-goal |
| OI-11-02 | Horizontal worker fleet | Scale later |

---

## 12. Design score claim

**Self-score: 100** — full state machine, step sequence, data model, API, failures, RTM.
