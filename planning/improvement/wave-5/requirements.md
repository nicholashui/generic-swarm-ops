# Wave 5 Requirements — Full Roster Activation + Process Wiring (N3 Completion)

**Wave:** 5  
**Source of truth:** `improvements.md` v1.0 § Wave 5  
**Cross-refs:** `adoption.md` v2.3 §0 N3 / §5.1, Waves 0–4 exits, `business/video/PROCESSES.md`  
**Date:** 2026-07-12  
**Status:** Ready for design / implementation  

---

## 1. Goal of this wave

Complete **N3** for the video Domain Pack on the generic host:

1. **All 114 agents** are ALC-complete and **registered + orchestrator-reachable** (standby pool / router); activate category-by-category readiness (cats 1–10), with spine/meta runnable at L2 where DNA exists.
2. **All va business processes** (spine, 6-phase E2E, archetypes A–J, LQR family, delivery/QC fabric, maps, deep-spec modules) are represented as **Workflow DNA and/or linked pack docs** — **no process left va-only**.
3. **Standby pool + router tables** complete and machine-checkable (no orphan pack_ids).
4. **Full-roster inventory CI** in default pipeline (fail on missing agent / incomplete N3 gates).
5. **Retention policy** for roster forever-enforced in pack policies + inventory gate.
6. Protect **E1**, multipack isolation (Wave 4), coevolution (Wave 3), and inventory **114**.

**Out of scope (post–Wave 5):** Real Sora/Veo media providers, advanced timeline FE, Temporal adapters, deep per-agent SPEC prose expansion beyond L1 wiring.

**Depth note:** Wave 5 delivers **N3 completeness** (reachability + process representation + CI), not production-grade depth for every specialist step. Thin DNA stubs with real `agent` ids and orchestrator-down entry satisfy N3; deeper step logic may iterate after exit.

---

## 2. Non-negotiables (N1 / N2 / N3)

From `adoption.md` v2.3 §0 (quoted sense):

| # | Requirement |
|---|-------------|
| **N1** | **va-agent-swarm** keeps **all** video agent-specific business logic; every agent must gain **mandatory autonomous learning** (individual knowledge growth). Video logic lives only under domain pack paths (`business/video/` …). Every registered agent must implement the **Agent Learning Contract** (ALC) or fail activation. |
| **N2** | **generic-swarm-ops** becomes a **universal foundation** for dozens of multi-agent (MMA) systems beyond video. Introduce **Domain Pack** interface, schemas, registration hooks, and isolation so any `business/<domain>/` onboard is config + artifacts, not a fork of the runtime. |
| **N3** | **Adopt ALL agents and ALL business processes from va-agent-swarm** into the generic project — from **orchestrator / planner / meta-agents down through every specialist and workflow-support agent**. **No agent may be dropped.** Inventory CI remains enforced for video pack presence. |

**Wave 5 enforcement:** N3 acceptance is **mandatory** this wave. N1: all DNA/docs under `business/video/`. N2: host APIs remain domain-agnostic; no video-only fork of runtime core.

---

## 3. Functional requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-W5-01 | Every roster agent (114) has ALC-complete `agent_spec` (`requires_alc`, scopes include `agent`, `alc_version`, reflect hook) and pack status ≥ `registered`. | P0 |
| FR-W5-02 | Every pack_id appears in `standby_pool.json` with route + category; entry remains `video.orchestrator`. | P0 |
| FR-W5-03 | Router table maps process families / categories → agent pack_ids (machine-readable). | P0 |
| FR-W5-04 | DNA families authored (thin OK): 6-phase E2E, archetypes B–J, LQR overview, delivery fabric; A + spine already exist. Entry via orchestrator and/or planner. | P0 |
| FR-W5-05 | `PROCESSES.md` + `process_coverage.json`: every process_id has `status` of DNA path or pack-linked doc path — **zero va-only**. | P0 |
| FR-W5-06 | Coverage matrix: every agent appears in ≥1 DNA step **or** standby_pool (standby already covers all; DNA should cover category representatives + prior spine). | P0 |
| FR-W5-07 | Inventory check extended for N3: standby 114, required DNA files present, process_coverage complete, retention doc present. | P0 |
| FR-W5-08 | Default CI pipeline runs inventory N3 gate (GitHub Actions or equivalent). | P0 |
| FR-W5-09 | Runtime: N3 roster status API/method (counts registered/reachable, DNA list, orphans empty). | P0 |
| FR-W5-10 | Unit tests prove 114 reachable, no orphans, DNA files load, process coverage, sample category activation ALC. | P0 |
| FR-W5-11 | FE: N3 roster readiness summary (114, by category, DNA count). | P1 |
| FR-W5-12 | Video pack retention policy documents forever roster retention. | P0 |

---

## 4. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR-W5-01 | No agent deletion; inventory count remains 114. |
| NFR-W5-02 | DNA remain `production_ready: false` unless already validated; human gates on irreversible package steps. |
| NFR-W5-03 | No second control plane; no Temporal/LangGraph host. |
| NFR-W5-04 | Full unit suite + inventory PASS; E1 protected. |
| NFR-W5-05 | Generation scripts may write pack artifacts; runtime stays domain-agnostic. |

---

## 5. Success / acceptance criteria (N3 mandatory)

| Gate | Pass condition |
|------|----------------|
| AC-1 | All 114 agents ALC-complete; status registered (disk); standby_pool len=114 |
| AC-2 | No orphan: every ROSTER pack_id in standby + agent dir; every standby pack_id in ROSTER |
| AC-3 | DNA files exist for spine, A–J, e2e 6-phase, LQR overview, delivery |
| AC-4 | process_coverage: 0 processes with status `va-only` or missing representation |
| AC-5 | inventory_check PASS with extended N3 checks |
| AC-6 | CI workflow file runs inventory_check |
| AC-7 | Unit test module wave-5 green; full unit suite green |
| AC-8 | FE N3 summary renders (if FE touched) |
| AC-9 | Retention policy file present under video pack |
| AC-10 | Completion report under `planning/improvement/wave-5/` |

---

## 6. Traceability

| Item | Source |
|------|--------|
| Full roster activation | improvements.md Wave 5; adoption.md §5.1 |
| Process A–J, LQR, delivery | PROCESSES.md; va study/workflows |
| Standby + router | improvements.md Wave 5; Wave 2 standby |
| Inventory CI pipeline | improvements.md Wave 0/5; inventory_check.py |
| Retention forever | adoption.md N3 |
| ALC activation | Wave 1; N1 |

---

## 7. Structure / Backend / Frontend

### Structure
Agent status/tools bulk readiness; DNA B–J + e2e + LQR + delivery; router_table; process_coverage; PROCESSES update; retention policy; CI workflow.

### Backend
N3 roster status method + optional route; extended inventory used by tests; wave-5 unit tests.

### Frontend
N3 roster readiness panel or DomainPackPanel video N3 strip.

---

## 8. Risks & constraints

| Risk | Mitigation |
|------|------------|
| DNA theater without agent ids | Every DNA step uses real pack_id agents; entry orchestrator/planner |
| Claiming full L2 depth for 114 | Explicit thin-stub policy; L1 reachability + representation = N3 exit |
| CI absent | Create `.github/workflows/n3-inventory.yml` |
| Breaking E1 | Full unit suite gate |

---

## 9. Internal critic

| Question | Answer |
|----------|--------|
| Is N3 complete without 114 deep L2? | Yes per adoption L0/L1/L2 model: N3 ≈ all ≥L1, spine L2, processes indexed as DNA/docs. |
| va-only residual? | Forbidden — every process DNA or pack doc. |
| N2 host purity? | Video artifacts under pack only. |

*End Phase 1 — Requirements.*
