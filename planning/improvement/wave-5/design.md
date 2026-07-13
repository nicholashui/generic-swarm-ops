# Wave 5 Design — N3 Roster + Process Wiring

**Wave:** 5  
**Implements:** `requirements.md`  
**Date:** 2026-07-12  

---

## 1. Architecture

```text
business/video/
  ROSTER.json (114) ──► agents/*/agent_spec.json (ALC + registered)
  standby_pool.json ──► every pack_id route=orchestrator_standby
  router_table.json ──► category + process_id → agents
  process_coverage.json ──► process_id → dna|doc
  workflows/*.dna.json ──► spine, e2e, A–J, LQR, delivery
  policies/roster-retention.md
        │
        ▼
inventory_check.py (N3 gates) ◄── .github/workflows/n3-inventory.yml
        │
        ▼
runtime.video_n3_roster_status() / GET /domains/video/n3-status
        │
        ▼
FE VideoN3RosterPanel
```

---

## 2. Key artifacts

### 2.1 Agent readiness (disk)

```json
{
  "status": "registered",
  "requires_alc": true,
  "allowed_memory_scopes": ["agent", "organization"],
  "alc_version": "1.0",
  "hooks": { "reflect": true },
  "tools": ["audit_log_writer"],
  "allowed_tools": ["audit_log_writer"],
  "n3_maturity": "L1_indexed",
  "activation_category": "3-Edit"
}
```

Spine/meta used on DNA: `n3_maturity: L2_runtime` where already on spine/A.

### 2.2 process_coverage.json

```json
{
  "schema_version": "1.0",
  "processes": [
    {
      "process_id": "video.arch.b.ugc_ad",
      "representation": "dna",
      "path": "business/video/workflows/wf_video_arch_b_ugc_ad_v1.dna.json",
      "status": "dna_ready"
    },
    {
      "process_id": "video.map.human_production",
      "representation": "pack_doc",
      "path": "business/video/docs/process-maps.md",
      "status": "pack_linked"
    }
  ]
}
```

No `va-only` status allowed.

### 2.3 router_table.json

```json
{
  "entry": "video.orchestrator",
  "categories": {
    "1-ATL": ["video.director", "..."],
    ...
  },
  "processes": {
    "video.spine.orchestrate": {
      "entry": "video.orchestrator",
      "agents": ["video.orchestrator", "video.planner", "..."]
    }
  }
}
```

### 2.4 DNA family template (thin)

Orchestrator → planner → domain specialists → QC → gated package (when irreversible).

### 2.5 Runtime status payload

```json
{
  "roster_count": 114,
  "standby_count": 114,
  "orphans": [],
  "dna_workflows": ["wf_video_spine_v1", "..."],
  "process_coverage": { "total": N, "dna": X, "pack_linked": Y, "va_only": 0 },
  "n3_complete": true
}
```

---

## 3. DNA inventory (to create/update)

| DNA id | Purpose |
|--------|---------|
| wf_video_spine_v1 | exists |
| wf_video_arch_a_viral_hook_v1 | exists |
| wf_video_arch_b_ugc_ad_v1 | new |
| wf_video_arch_c_animated_explainer_v1 | new |
| wf_video_arch_d_personalized_birthday_v1 | new |
| wf_video_arch_e_ai_short_film_v1 | new |
| wf_video_arch_f_corporate_training_v1 | new |
| wf_video_arch_g_music_video_v1 | new |
| wf_video_arch_h_ai_avatar_v1 | new |
| wf_video_arch_i_documentary_v1 | new |
| wf_video_arch_j_feature_film_v1 | new |
| wf_video_production_e2e_v1 | 6-phase |
| wf_video_lqr_overview_v1 | LQR family entry |
| wf_video_delivery_v1 | delivery fabric |

---

## 4. N1 / N2 / N3

| N | Design |
|---|--------|
| N1 | All artifacts under `business/video/`; ALC on every agent |
| N2 | Status API generic-shaped (`domain_id=video`); other packs unchanged |
| N3 | 114 retained; inventory+CI; processes represented in-pack |

---

## 5. Reuse

- Wave 2 DNA style, standby_pool, inventory_check  
- Wave 1 ALC fields, register_domain_pack (manifest already 114 agents)  
- DomainPackPanel patterns for FE  

---

## 6. Files

```text
planning/improvement/wave-5/*
business/video/workflows/wf_video_arch_{b..j}_*.dna.json
business/video/workflows/wf_video_production_e2e_v1.dna.json
business/video/workflows/wf_video_lqr_overview_v1.dna.json
business/video/workflows/wf_video_delivery_v1.dna.json
business/video/router_table.json
business/video/process_coverage.json
business/video/docs/process-maps.md
business/video/docs/deep-spec-modules.md
business/video/policies/roster-retention.md
business/video/PROCESSES.md  # update
business/video/agents/*/agent_spec.json  # bulk registered
business/video/manifest.json  # version bump + workflows list
business/video/standby_pool.json  # enrich category
scripts/business/inventory_check.py  # N3 gates
scripts/business/prepare_wave5_n3.py  # generator (optional)
.github/workflows/n3-inventory.yml
backend/app/runtime.py  # video_n3_roster_status
backend/app/api/v1/routes/domains.py  # route if exists
backend/app/tests/unit/test_wave5_n3_roster.py
frontend/src/components/domain/video-n3-roster-panel.tsx
```

---

## 7. Inventory N3 extensions

```text
check_inventory():
  existing 114 gates
  + standby_pool agents == 114 and set equality with ROSTER
  + required DNA files exist
  + process_coverage.json: no va_only; every process has path file
  + roster-retention.md exists
```

---

## 8. FE

`VideoN3RosterPanel`: show 114, category breakdown (static from API or demo), DNA count, n3_complete badge. Mount near DomainPackPanel when video agents present.

---

## 9. Critic

| Risk | Mitigation |
|------|------------|
| Huge DNA hand-authoring | Generator script from ROSTER + templates |
| Manifest workflows empty | Populate workflow ids |
| Activate all 114 live in prod store | Disk `registered` + runtime status from disk/standby; activate sample in tests |

*End Phase 2 — Design.*
