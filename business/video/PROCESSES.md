# Video Domain Pack — Process Index (N3)

**Status:** Wave 5 N3 complete — DNA or pack-linked (no va-only)  
**Entry rule:** Executable DNA enters via **video.orchestrator** and/or **video.planner**.  
**Generated/updated:** 2026-07-12

---

## 1. Orchestration spine

| process_id | target_dna_id | status |
|------------|---------------|--------|
| video.spine.orchestrate | wf_video_spine_v1 | **DNA ready** |
| video.spine.plan | wf_video_spine_v1 | **DNA ready** |

## 2. Six-phase E2E

| process_id | target_dna_id | status |
|------------|---------------|--------|
| video.phase.1–6.* | wf_video_production_e2e_v1 | **DNA ready (thin)** |

## 3. Archetypes A–J

| process_id | target_dna_id | status |
|------------|---------------|--------|
| video.arch.a.viral_hook | wf_video_arch_a_viral_hook_v1 | **DNA ready** |
| video.arch.b.ugc_ad | wf_video_arch_b_ugc_ad_v1 | **DNA ready (thin)** |
| video.arch.c.animated_explainer | wf_video_arch_c_animated_explainer_v1 | **DNA ready (thin)** |
| video.arch.d.personalized_birthday | wf_video_arch_d_personalized_birthday_v1 | **DNA ready (thin)** |
| video.arch.e.ai_short_film | wf_video_arch_e_ai_short_film_v1 | **DNA ready (thin)** |
| video.arch.f.corporate_training | wf_video_arch_f_corporate_training_v1 | **DNA ready (thin)** |
| video.arch.g.music_video | wf_video_arch_g_music_video_v1 | **DNA ready (thin)** |
| video.arch.h.ai_avatar | wf_video_arch_h_ai_avatar_v1 | **DNA ready (thin)** |
| video.arch.i.documentary | wf_video_arch_i_documentary_v1 | **DNA ready (thin)** |
| video.arch.j.feature_film | wf_video_arch_j_feature_film_v1 | **DNA ready (thin)** |

## 4. LQR family

All map to `wf_video_lqr_overview_v1` (thin family entry) — **DNA ready**.

## 5. Maps / UI / deep-spec

Pack-linked under `business/video/docs/process-maps.md` and `deep-spec-modules.md` — **not va-only**.

## 6. Delivery / QC

| process_id | DNA | status |
|------------|-----|--------|
| video.delivery.package | wf_video_delivery_v1 | **DNA ready** |
| video.qc.* | wf_video_lqr_overview_v1 | **DNA ready** |

## 7. Machine index

See `process_coverage.json`, `router_table.json`, `standby_pool.json` (114 agents).

*End PROCESSES.md (Wave 5 N3)*
