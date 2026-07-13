# Wave 2 Requirements — Video Catalog Complete + Spine E2E

**Wave:** 2  
**Source:** `improvements.md` v1.0 Wave 2 · `adoption.md` v2.3 §5.0–5.4  
**Prior:** Wave 0 catalog L0; Wave 1 ALC + domains register  
**Date:** 2026-07-12  

---

## 1. Goal

Deliver a **runnable video spine** on the L0 catalog:

1. Confirm **114-agent** catalog (inventory green) with spine agents ALC-ready and activatable.
2. Author **orchestrator-down** Workflow DNA: spine + viral-hook archetype A.
3. Add **video.* tool stubs** + permission register entries (CI-safe, no real media APIs).
4. Golden eval + **human gate** on package/publish step.
5. **E2E unit test**: register video pack → activate spine agents → run DNA → approve gate → reflect (agent_id lessons).
6. Standby pool / reachability index so every roster agent is orchestrator-reachable (document or table).
7. Initial knowledge seeds with provenance; FE domain view remains usable.

**Out of scope:** Real Sora/Veo calls; full A–J DNA depth; full 114 active activation; advanced timeline FE.

---

## 2. Non-negotiables (N1 / N2 / N3)

| # | From adoption.md |
|---|------------------|
| **N1** | Video business logic stays in pack; every agent gains mandatory autonomous learning (ALC). |
| **N2** | generic remains universal host; packs are config + artifacts. |
| **N3** | All 114 agents + process coverage retained; no agent dropped; inventory CI enforces. |

Wave 2: N3 **catalog + spine L2 proof**, not “all agents active.”

---

## 3. Functional requirements

| ID | Requirement | P |
|----|-------------|---|
| FR-W2-01 | Inventory remains 114; MAP complete. | P0 |
| FR-W2-02 | Spine agent_specs list video tools + ALC; standby_pool.json lists all pack_ids reachable via orchestrator. | P0 |
| FR-W2-03 | `wf_video_spine_v1.dna.json` + `wf_video_arch_a_viral_hook_v1.dna.json` under `business/video/workflows/`. Entry via orchestrator/planner. | P0 |
| FR-W2-04 | Adapters: `video_media_gen_stub`, `video_script_format`, `video_qc_stub` (+ package stub if needed). | P0 |
| FR-W2-05 | tool-permission-register includes video tools; load_tools exposes them. | P0 |
| FR-W2-06 | Golden eval fixture for spine/viral-hook. | P0 |
| FR-W2-07 | Human gate step on irreversible package/publish. | P0 |
| FR-W2-08 | Unit/e2e test: spine run completes after approval; ALC lessons with agent_id. | P0 |
| FR-W2-09 | Knowledge seed file(s) under `business/video/knowledge/seeds/` with provenance. | P1 |
| FR-W2-10 | PROCESSES.md notes spine DNA paths ready. | P0 |
| FR-W2-11 | E1 / full unit suite still green. | P0 |

## 4. Non-functional

| ID | Requirement |
|----|-------------|
| NFR-W2-01 | Media adapters are local stubs only (no network). |
| NFR-W2-02 | No second control plane. |
| NFR-W2-03 | Namespace `video.*` / tool ids do not replace ops tools. |
| NFR-W2-04 | production_ready DNA optional false for spine until validated. |

## 5. Acceptance criteria

| AC | Pass |
|----|------|
| AC-1 | inventory_check PASS 114 |
| AC-2 | DNA files exist; first step agent is video.orchestrator or video.planner |
| AC-3 | execute_tool(video_*_stub) returns status ok |
| AC-4 | Unit test spine path: queued→…→waiting_for_approval→completed |
| AC-5 | After reflect, lessons with agent_id for spine agents |
| AC-6 | standby_pool covers all 114 pack_ids |
| AC-7 | Backend unit suite green; E1 not broken |
| AC-8 | FE typecheck if FE touched |

## 6. Structure / Backend / Frontend

### Structure
DNA, golden, seeds, standby_pool, process index update, tool adapters.md.

### Backend
Video adapters, tool seed/register, e2e/unit test for spine, optional register helpers.

### Frontend
Minimal: ensure DomainPackPanel still works; optional link to video workflows (P2).

## 7. Risks

| Risk | Mitigation |
|------|------------|
| Human gate blocks CI forever | Test approves gate like E1 |
| Missing tools in store | Extend load_tools + register |
| Activating 114 agents slow | Only activate spine set in test |

*End Phase 1.*
