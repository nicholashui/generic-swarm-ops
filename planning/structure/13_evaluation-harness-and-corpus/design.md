# Design — 13 Evaluation Harness and Corpus

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-13-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-13`) |
| Source | `structure.md` §8 |
| Design quality bar | 100 |

---

## 1. Purpose

Make quality **empirical**: every material agent/skill/workflow/prompt owns evaluation assets; harness produces evaluation cards; **promotion stays manual** (pass ≠ auto production promote).

---

## 2. Context

Eight ownership classes (structure.md): golden, regression, adversarial, human-review, historical-replay, cost/latency benchmark, business-outcome metric, safety/compliance score.

---

## 3. Architecture

```text
business/evals/**
        │
        ▼
┌──────────────────┐     ┌─────────────────┐
│ Eval Harness CLI │────▶│ Evaluation cards│
│ business:eval    │     │ + exit code     │
└────────┬─────────┘     └────────┬────────┘
         │                        │
         │                        ▼
         │               Evolution promote gate (14)
         ▼               (never auto production)
 Runtime verification (DNA required_checks)
```

### 3.1 Components

| ID | Component | Path |
|----|-----------|------|
| C-13-1 | Golden corpus | `evals/golden-tasks/` (≥20) |
| C-13-2 | Regression | `evals/regression-tests/` |
| C-13-3 | Adversarial | `evals/adversarial-tests/` |
| C-13-4 | Historical replay | `evals/historical-replay/` |
| C-13-5 | Human-review sets | `evals/human-review-sets/` |
| C-13-6 | Retrieval fixtures | `evals/retrieval/` |
| C-13-7 | Benchmark results | `evals/benchmark-results/` |
| C-13-8 | Harness runner | `scripts/business/eval-harness.mjs` |
| C-13-9 | Card schema | `schemas/evaluation-card.schema.json` |
| C-13-10 | Runtime checks | DNA verification / block_on_fail |

### 3.2 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-13-01 | Disk corpus SoT for offline eval | Reproducible CI |
| D-13-02 | promotion_decision never unattended production | Charter INV |
| D-13-03 | Multi-step tool-using cases preferred for workflows | structure.md |

---

## 4. Evaluation card model

```text
evaluation {
  target, eval_type, test_set,
  metrics {
    quality_score, compliance_pass_rate,
    average_cycle_time_minutes, escalation_rate,
    hallucination_rate, unauthorized_tool_attempts,
    cost_per_case_usd
  },
  result: pass|fail,
  promotion_decision: none|canary_only|manual_review|...,
  reviewer?
}
```

**Forbidden:** `promotion_decision = auto_production` without human.

---

## 5. Harness algorithm

```text
for suite in [golden, regression, adversarial, historical, ...]:
  for case in suite:
    execute checks (schema/policy/sim)
    record metrics
emit summary
if hard_fail: exit != 0
assert not auto_promote_production
```

Runtime path: after steps, evaluate `required_checks`; if fail and `block_on_fail` → run failed.

---

## 6. Interfaces

| Interface | Contract |
|-----------|----------|
| CLI | `npm run business:eval` |
| Evolution | Offline corpus eval module |
| FE | `/app/evaluations` lists cards |
| API | evaluations list/run as implemented |

---

## 7. NFR design

| NFR | Design |
|-----|--------|
| NFR-13-01 Baseline golden ≤10 min local | Disk fixtures, no live LLM required for core |
| NFR-13-02 Durable cards under business/evals | File write |
| NFR-13-03 Adversarial without disabling auth | Separate fixtures |
| NFR-13-04 No secrets in fixtures | security scan |

---

## 8. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-13-01…08 | §2–3 corpus | file count + harness |
| FR-13-09…11 | §4–5 cards + multi-step | schema + golden |
| FR-13-12…13 | D-13-02 | unit invariant |
| NFR-13-01…04 | §7 | timed eval, scan |
| AC-13-01…05 | §3 | business:eval green |

---

## 9. Validation design

≥20 golden; all suites in harness; auto-promote blocked; card fields present.

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-13-01 | Exhaustive per-agent 8-class packs | Content growth |
| OI-13-02 | Large-scale latency labs | Later |

---

## 11. Design score claim

**Self-score: 100** — eight classes mapped, card model, harness algorithm, promote ban, RTM.
