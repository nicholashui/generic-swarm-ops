# Wave 1 Requirements — Domain Pack SDK + Full ALC

**Wave:** 1  
**Source of truth:** `improvements.md` v1.0 § Wave 1  
**Cross-refs:** `adoption.md` v2.3, `repo_compare.md`, Wave 0 exit (`planning/improvement/wave-0/`)  
**Date:** 2026-07-11  
**Status:** Ready for design/implementation  

---

## 1. Goal of this wave

Make **generic-swarm-ops** a true extensible MMA host:

1. **Agent Learning Contract (ALC)** works platform-wide: lessons carry `agent_id`, reflect tags agents, pre-step retrieve injects agent lessons, activation to `active` hard-gates ALC fields.
2. **Domain Pack registration** is a real API (validate manifest → load draft agents into org catalog) plus CLI.
3. **Second pack** (`example_research`) proves isolation and independent learning (N2).
4. **Agent genome** evolution variant type is sandbox-only (no direct production mutation).
5. **Frontend** shows domain/pack filter + ALC status for agents without breaking ops console.
6. Protect **E1 / mark ~100** and Wave 0 inventory (114 video agents remain on disk).

**Out of scope (Wave 2+):** Full video spine DNA E2E, media adapters, full 114 activation, multi-generation coevolution experiments.

---

## 2. Non-negotiables (N1 / N2 / N3)

From `adoption.md` v2.3 §0:

| # | Requirement |
|---|-------------|
| **N1** | **va-agent-swarm** keeps **all** video agent-specific business logic; every agent must gain **mandatory autonomous learning** (individual knowledge growth). Video logic lives only under domain pack paths (`business/video/` …). Every registered agent must implement the **Agent Learning Contract** (ALC) or fail activation. |
| **N2** | **generic-swarm-ops** becomes a **universal foundation** for dozens of multi-agent (MMA) systems beyond video. Introduce **Domain Pack** interface, schemas, registration hooks, and isolation so any `business/<domain>/` onboard is config + artifacts, not a fork of the runtime. |
| **N3** | **Adopt ALL agents and ALL business processes from va-agent-swarm** into the generic project — from **orchestrator / planner / meta-agents down through every specialist and workflow-support agent**. **No agent may be dropped.** Inventory CI remains enforced for video pack presence. |

**Wave 1 enforcement:** ALC gate on activation (N1); domain register for any domain_id (N2); do not delete video catalog; inventory still passes (N3).

---

## 3. Functional requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-W1-01 | `Lesson` / improvement_lessons store optional `agent_id`; backward compatible with legacy lessons. | P0 |
| FR-W1-02 | `reflect_on_workflow_run` writes lessons tagged with step agent when steps have agents; multi-agent runs produce multi-agent lessons. | P0 |
| FR-W1-03 | Pre-step hook retrieves top-k lessons for the step’s agent and attaches `injected_lessons` (or equivalent) on the step record / context. | P0 |
| FR-W1-04 | `POST /api/v1/improvement/reflect/agent/{agent_id}` reflects scoped to that agent (filter lessons / re-run reflect filtered). | P0 |
| FR-W1-05 | `GET /api/v1/improvement/lessons?agent_id=` filters by agent. | P0 |
| FR-W1-06 | `GET /api/v1/improvement/metrics?agent_id=` returns knowledge_growth_count, lesson_reuse_rate (and related). | P0 |
| FR-W1-07 | Activation to `active` denied if `requires_alc` and missing agent memory scope / reflect hook / alc_version (error `alc_required`). | P0 |
| FR-W1-08 | DNA / production_ready validation: active step agents must pass ALC when workflow is production_ready (or deny activation of such DNA). | P1 |
| FR-W1-09 | `POST /api/v1/domains/register` validates domain-manifest schema; loads agents from pack dirs as `draft`/`registered` with ALC fields; fails closed on invalid manifest. | P0 |
| FR-W1-10 | CLI register remains working and can call same service logic. | P0 |
| FR-W1-11 | Evolution: `variant_type` / genome type `agent_genome` forced `sandbox_only`; direct production mutation blocked. | P0 |
| FR-W1-12 | example_research pack has ≥2 ALC agents + 1 workflow DNA + 1 golden; isolation unit tests (agent A cannot read B lessons/episodes). | P0 |
| FR-W1-13 | FE: domain pack roster view — filter by domain_id, show ALC readiness, list registered pack agents. | P0 |
| FR-W1-14 | Auto-reflect path uses agent-tagged lessons when available. | P0 |

## 4. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR-W1-01 | E1 operator path + existing unit suite remain green. |
| NFR-W1-02 | Wave 0 inventory still PASS (114 video agents). |
| NFR-W1-03 | No video business logic hard-coded in core beyond domain_id fields. |
| NFR-W1-04 | sandbox_only evolution never bypassed for agent genomes. |
| NFR-W1-05 | Memory isolation: agent-scoped lesson retrieve does not leak across agent_id. |

---

## 5. Success / acceptance criteria

| Gate | Pass condition |
|------|----------------|
| AC-1 | Unit: lesson with agent_id persisted and retrieved by filter |
| AC-2 | Unit: activate without ALC fields → ValidationError / PermissionDenied with alc_required |
| AC-3 | Unit: activate with ALC fields → success |
| AC-4 | Unit: pre-step inject populates injected_lessons for agent with prior lessons |
| AC-5 | Unit: agent A lessons not returned when querying agent B |
| AC-6 | API/register: valid video or example_research manifest → draft agents in store |
| AC-7 | Invalid manifest → 4xx / fail closed |
| AC-8 | agent_genome propose → sandbox_only true; direct mutation blocked |
| AC-9 | Domain pack unit tests + inventory still green |
| AC-10 | FE agents/domain view renders without typecheck/lint break |
| AC-11 | docs/domain-packs.md updated for register API + ALC |

---

## 6. Traceability

| Item | Source |
|------|--------|
| ALC runtime | improvements.md W1-T1; adoption.md §4 ALC |
| Activation gate | improvements.md W1-T2; adoption.md N1 |
| Domain register | improvements.md W1-T3; adoption.md §3.1 |
| Agent genome | improvements.md W1-T4 |
| Second pack + isolation | improvements.md W1-T5; N2 |
| FE shell | improvements.md W1-T6 |
| Wave 0 foundation | planning/improvement/wave-0/ |

---

## 7. Risks & constraints

| Risk | Mitigation |
|------|------------|
| Breaking legacy lessons without agent_id | Optional field; retrieve falls back |
| ALC gate blocks seed ops agents | Seed agents get ALC fields on create/seed or exempt if requires_alc false |
| Register loads 114 agents heavy | Allow register with manifest agent list; load specs from disk when present |
| FE large slug page | Additive component; no rewrite of entire shell |
| E1 regression | Run unit suite; avoid changing onboarding DNA |

---

## 8. Structure / Backend / Frontend requirements

### 8.1 Structure
- Enrich `example_research` with workflow DNA + golden eval.
- Keep video pack inventory intact.
- Update `docs/domain-packs.md` for API register + ALC.

### 8.2 Backend
- Primary owner of ALC, domains API, evolution genome, isolation tests.
- Extend lessons, reflection usage, runtime gates, routes.

### 8.3 Frontend
- Domain pack roster UI (filter domain_id, ALC badge).
- Client methods for domains register / list if needed; can use agents list filtered by domain_id when backend stamps domain_id.

---

## 9. Critic notes

- Wave 1 does **not** claim N3 complete.
- Draft register must not auto-activate agents without ALC.
- Pre-step inject must be best-effort and not fail runs if no lessons exist.

*End of Phase 1 requirements.*
