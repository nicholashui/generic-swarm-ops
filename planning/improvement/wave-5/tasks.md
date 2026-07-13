# Wave 5 Tasks — N3 Completion Checklist

**Wave:** 5  
**Implements:** `requirements.md` + `design.md`  
**Date:** 2026-07-12  
**Status:** All tasks completed  

Tag legend: **[Structure]** / **[Backend]** / **[Frontend]**.

---

## Structure

### T1 — Bulk agent_spec readiness
**Paths:** `business/video/agents/*/agent_spec.json` via `scripts/business/prepare_wave5_n3.py`  
**Acceptance:**
- [x] All 114 `status` ∈ {registered, active}
- [x] ALC fields + `allowed_tools` / tools present
- [x] `n3_maturity` L1_indexed or L2_runtime on spine set

### T2 — DNA families
**Paths:** `business/video/workflows/wf_video_{production_e2e,lqr_overview,delivery,arch_b..j}_*.dna.json`  
**Acceptance:**
- [x] 14 DNA files total (incl. prior spine + A)
- [x] Entry agent orchestrator or planner
- [x] Real `video.*` pack agent ids on steps

### T3 — Router + standby
**Paths:** `business/video/router_table.json`, `business/video/standby_pool.json`  
**Acceptance:**
- [x] Standby agents == 114 and set-equal ROSTER
- [x] Categories cover all pack_ids; entry `video.orchestrator`

### T4 — Process coverage + docs
**Paths:** `process_coverage.json`, `docs/process-maps.md`, `docs/deep-spec-modules.md`, `PROCESSES.md`  
**Acceptance:**
- [x] No `va-only` processes
- [x] Every path file exists (dna or pack_doc)

### T5 — Retention policy
**Path:** `business/video/policies/roster-retention.md`  
- [x] Forever-114 rules documented

### T6 — Manifest
**Path:** `business/video/manifest.json`  
- [x] version 1.0.0; workflows list length 14

### T7 — Inventory N3 extensions
**Path:** `scripts/business/inventory_check.py`  
- [x] Standby, DNA, coverage, retention, registered status gates

### T8 — CI workflow
**Path:** `.github/workflows/n3-inventory.yml`  
- [x] Runs `python scripts/business/inventory_check.py`

---

## Backend

### T9 — N3 status API
**Paths:** `runtime.video_n3_roster_status`, `GET /api/v1/domains/video/n3-status`  
- [x] Returns roster/standby/orphans/dna/process_coverage/`n3_complete`

### T10 — Unit tests
**Path:** `backend/app/tests/unit/test_wave5_n3_roster.py`  
- [x] 9 cases green; full unit suite green with inventory PASS

---

## Frontend

### T11 — VideoN3RosterPanel
**Paths:** `frontend/src/components/domain/video-n3-roster-panel.tsx`, domains page mount, API client  
- [x] Shows 114 / DNA / process / categories; demo mode

---

## Close

### T12 — Completion report + handoff
- [x] `planning/improvement/wave-5/completion-report.md`
- [x] `memory/handoff.md` updated

---

## Order executed

T1 → T2 → T3 → T4 → T5 → T6 → T7 → T8 → T9 → T10 → T11 → T12

## AC map

| AC | Tasks |
|----|-------|
| AC-1 114 registered + standby | T1, T3 |
| AC-2 No orphans | T3, T7, T10 |
| AC-3 DNA families | T2 |
| AC-4 process_coverage | T4 |
| AC-5 inventory N3 | T7 |
| AC-6 CI | T8 |
| AC-7 unit suite | T10 |
| AC-8 FE | T11 |
| AC-9 retention | T5 |
| AC-10 report | T12 |

## Out of scope (post–N3)

- Real media providers  
- Full deep L2 step logic per specialist  
- Advanced timeline FE  
- Temporal adapters  

*End Phase 3 — Tasks.*
