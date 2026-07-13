# Wave 4 Tasks — Implementation Checklist

**Wave:** 4  
**Implements:** `requirements.md` + `design.md`  
**Date:** 2026-07-12  

Tag legend: **[Structure]** / **[Backend]** / **[Frontend]**.

---

## Structure

### T1 — Third lite pack `example_education`
**Create:**
- `business/example_education/manifest.json`
- `business/example_education/README.md`
- `business/example_education/agents/example.edu_planner/agent_spec.json`
- `business/example_education/agents/example.edu_reviewer/agent_spec.json`
- `business/example_education/workflows/wf_example_education_v1.dna.json`
- `business/example_education/evals/golden/example-education-brief.json`

**Pattern:** Copy shape from `business/example_research/`.

**Acceptance:**
- [x] Manifest validates required fields
- [x] ≥2 ALC agents + 1 DNA + 1 golden
- [x] Outside `business/video/` (N3 inventory unaffected)

### T2 — Adversarial / red-team fixtures
**Create:**
- `business/video/evals/adversarial/video-tool-misuse-injection.json`
- `business/security/red-team-results/wave-4-tool-misuse.json` (evidence stub)

**Acceptance:**
- [x] Threats + pass_criteria + forbidden tools documented
- [x] Provenance → improvements Wave 4

### T3 — Runbook + versioning matrix
**Create/Update:**
- `docs/add-domain-pack-runbook.md`
- `docs/domain-pack-versioning-matrix.md`
- `docs/domain-packs.md` (links)

**Acceptance:**
- [x] Step-by-step add pack
- [x] Versioning matrix table
- [x] Links from domain-packs.md

### T10 — Completion report
- `planning/improvement/wave-4/completion-report.md`

---

## Backend

### T4 — Domain isolation helpers
**Create:** `backend/app/infrastructure/security/domain_isolation.py`  
**Optional:** `backend/app/infrastructure/security/__init__.py` if missing

**Acceptance:**
- [x] domain prefix helper + allowlist equality helper
- [x] Unit-tested via T7

### T5 — Expanded isolation + third pack register tests
Part of `test_wave4_multipack.py`

**Acceptance:**
- [x] Cross-agent lesson isolation
- [x] Corpus domain overlay isolation (education golden not under video domain load)
- [x] register example_education

### T6 — Load harness (≥20 mixed-domain runs)
Part of `test_wave4_multipack.py`

**Reuse:** `create_agent`, `create_workflow`, `start_workflow_run`, `dispatch_queued_runs`

**Acceptance:**
- [x] ≥20 runs started
- [x] All in completed | waiting_for_approval | failed
- [x] Completes offline < 2 min

### T7 — Red-team security tests
Part of `test_wave4_multipack.py`

**Acceptance:**
- [x] Video-like agent + billing tool → failed / not allowed
- [x] Injection input does not change allowed_tools
- [x] Optional: fixture file readable / referenced

### T9 — Full suite + inventory
```bash
python scripts/business/inventory_check.py   # PASS 114
pytest app/tests/unit -q
```

---

## Frontend

### T8 — Multi-pack summary on DomainPackPanel
**Modify:** `frontend/src/components/domain/domain-pack-panel.tsx`

**Acceptance:**
- [x] Shows domain pack count (excluding “all”)
- [x] Isolation/N2 operator hint
- [x] Existing filter still works

---

## Recommended order

1. T1 third pack  
2. T2 adversarial fixtures  
3. T4 isolation helpers  
4. T5–T7 tests  
5. T3 docs  
6. T8 FE  
7. T9 verify  
8. T10 completion report  

---

## Acceptance matrix

| AC | Tasks |
|----|-------|
| AC-1 Load ≥20 | T6, T9 |
| AC-2 Isolation | T4, T5, T9 |
| AC-3 Tool misuse | T2, T7 |
| AC-4 Allow-list immutable | T7 |
| AC-5 Runbook + matrix | T3 |
| AC-6 Third pack | T1, T5 |
| AC-7 Inventory + suite | T9 |
| AC-8 FE | T8 |
| AC-9 Report | T10 |

## Out of scope

- Wave 5 full roster activation  
- Real media APIs  
- True multi-process load cluster  
- Auto-promote  

*End Phase 3 — Tasks.*


**Status:** All tasks completed (Wave 4 exit).

