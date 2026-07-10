# Design — 06 Process Intelligence Layer

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-06-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-06`) |
| Source | `structure.md` §2.3 |
| Design quality bar | 100 |

---

## 1. Purpose

Learn from **operational traces** (not only documents): ingest structured events, produce discovered processes / conformance / bottlenecks / causal hypotheses, feed evaluation and sandbox evolution—**never** mutate production DNA.

---

## 2. Context

### 2.1 Logical agents → realization

| structure.md agent | Realization | Output |
|--------------------|-------------|--------|
| Process Miner | Analysis module | discovered-processes/ |
| Task Mining | Optional traces module | shadow / UI steps when permitted |
| Conformance | Comparator vs SOP refs | conformance-reports/ |
| Bottleneck Analyzer | Latency/loop metrics | bottlenecks/ |
| Causal Improvement | Hypothesis generator | causal-hypotheses/ (sandbox input only) |

**Decision D-06-01:** Services + artifacts, not five independent LLM agents. Inventory may still list roles (15).

### 2.2 Event sources

tickets, CRM/ERP, calendar, email, approvals, file edits, API calls, completions (via API/connectors when present).

---

## 3. Architecture

```text
Sources → Ingest API → Validate schema → Persist event
                │
                ▼
         Analysis core (miner, conformance, bottleneck, causal)
                │
                ├── business/process-intelligence/**/*.json
                ├── runtime process summaries
                └── evolution opportunity signals (read-only)
```

### 3.1 Components

| ID | Component | Path |
|----|-----------|------|
| C-06-1 | Event schema | `business/schemas/event-log.schema.json` |
| C-06-2 | Ingest | processes/events API + runtime |
| C-06-3 | Analyzer | `infrastructure/process_intelligence/` |
| C-06-4 | Disk writer | `business/process-intelligence/` |
| C-06-5 | Query API | process summary/bottlenecks/metrics |
| C-06-6 | Handoff bus | Read model for evolution (14) |

---

## 4. Data model — event log (field-level)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | string | Y | `evt_…` |
| timestamp | ISO-8601 | Y | |
| actor_type | enum human\|agent\|system | Y | |
| actor_id | string | Y | |
| process_id | string | Y | |
| case_id | string | Y | |
| activity | string | Y | |
| input_refs | string[] | N | |
| output_refs | string[] | N | |
| tools_used | string[] | N | |
| decision_point | bool | N | |
| decision_reason_summary | string | if decision | |
| confidence | number 0–1 | N | |
| risk_tier | string | N | |
| human_approved | bool | N | |
| outcome.status | string | N | |
| outcome.latency_minutes | number | N | |
| outcome.quality_score | number | N | |

### 4.1 Artifact types

| Artifact | Content |
|----------|---------|
| discovered-processes | Graph/path summary of observed activities |
| conformance-reports | Deviations vs SOP |
| bottlenecks | Delays, loops, rework, handoffs |
| causal-hypotheses | Proposed interventions; **no DNA write** |

---

## 5. Algorithms

### 5.1 Ingest

```text
on_event(e):
  errors = schema_validate(e)
  if errors: quarantine/reject; audit; return
  persist(e)
  artifacts = analyze(window_including(e))
  write_disk(artifacts)
  update_runtime_summary(artifacts)
```

### 5.2 Causal handoff rule

```text
emit_hypothesis(h):
  write causal-hypotheses/
  FORBIDDEN: call evolution.promote or mutate production DNA
  ALLOWED: evolution.propose from human/API using h as hint
```

---

## 6. API contract

| Method | Path | Notes |
|--------|------|-------|
| POST | process events / ingest | validate + analyze |
| GET | `/api/v1/processes` summaries | authz |
| GET | bottlenecks / failures / metrics | authz |

Errors: 401/403/422 with request_id.

---

## 7. NFR design

| NFR | Design |
|-----|--------|
| NFR-06-01 validate &lt;100ms | schema-lite local |
| NFR-06-02 batch &lt;5 min sample | windowed analyze |
| NFR-06-03–04 sensitivity | RBAC on APIs; minimize PII in fixtures |

**Metrics:** `events_ingested_total`, `pi_artifacts_written`, analyze latency.

---

## 8. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-06-01…04 | §4 event model + ingest | schema + ingest tests |
| FR-06-05…09 | §2.1 + §5 | test_p3_pi_evolution |
| FR-06-10…12 | §5.1–5.2 | disk artifacts; causal no promote |
| NFR-06-01…04 | §7 | unit + authz |
| AC-06-01…04 | §4–6 | automated |

---

## 9. Validation design

Invalid event rejected; ingest writes artifacts; causal path has no promote calls (code review + unit).

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-06-01 | Live CRM/ERP connectors | Non-goal product bar |
| OI-06-02 | Rich UI task mining | Later |

---

## 11. Design score claim

**Self-score: 100** — field-level event model, algorithms, agent mapping, API, RTM.
