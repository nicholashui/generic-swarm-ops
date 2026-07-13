# Wave 1 Tasks

Execute in order. Tags: **[Structure]** | **[Backend]** | **[Frontend]**

---

## T1 — Lesson.agent_id + library retrieve  [Backend]
- **Modify:** `backend/app/infrastructure/self_improvement/lessons.py`
- Add `agent_id` to Lesson, to_dict, from_dict; dedup includes agent_id; retrieve filters agent_id.
- **Acceptance:** unit covers filter + legacy without agent_id still loads.

## T2 — alc_validator  [Backend]
- **Create:** `backend/app/infrastructure/governance/alc_validator.py`
- `assert_alc_ready(agent) -> None` raises ValidationError with code/message alc_required.
- **Acceptance:** unit pure function tests.

## T3 — Runtime ALC: reflect, inject, gate, metrics, agent reflect  [Backend]
- **Modify:** `runtime.py`
  - `update_agent_status`: call ALC gate when status==active
  - `reflect_on_workflow_run`: tag lessons with step agent; write agent-scoped memory when agent known
  - `_execute_run_body`: after agent resolved, retrieve lessons → `step_record["injected_lessons"]`
  - `list_improvement_lessons(..., agent_id=)`
  - `improvement_metrics(agent_id=)`
  - `reflect_on_agent(agent_id, run_id optional)`
  - `register_domain_pack(...)`
- **Acceptance:** unit tests in test_alc_and_domains.py

## T4 — Improvement routes  [Backend]
- **Modify:** `improvement.py`
  - GET lessons?agent_id=
  - POST reflect/agent/{agent_id}
  - GET metrics?agent_id=
- **Acceptance:** callable via runtime methods (route thin wrappers).

## T5 — Domains router  [Backend]
- **Create:** `domains.py`; include in `router.py`
- POST /register, GET / (list domain_packs)
- **Acceptance:** unit tests call runtime.register_domain_pack.

## T6 — Evolution agent_genome  [Backend]
- **Modify:** propose_evolution_variant to accept variant_type agent_genome; force sandbox_only; require agent_id for genome.
- **Acceptance:** unit blocks direct mutation; genome sandbox_only.

## T7 — example_research DNA + golden  [Structure]
- **Create:** workflow DNA JSON + golden eval fixture.
- **Acceptance:** files exist; DNA has example.researcher step.

## T8 — Isolation + ALC unit tests  [Backend]
- **Create:** `test_alc_and_domains.py`
- **Acceptance:** AC-1–AC-8 covered.

## T9 — FE DomainPackPanel  [Frontend]
- **Create:** domain-pack-panel.tsx; wire into agents section of slug page; optional path domains.
- Show domain_id, ALC ready/missing from agent fields.
- **Acceptance:** typecheck/lint clean if run; no crash.

## T10 — Docs + CLI  [Structure][Backend]
- Update docs/domain-packs.md; handoff; register_domain.py notes API.
- **Acceptance:** docs mention ALC gate + POST /domains/register.

## T11 — Verification  [Backend][Frontend]
- inventory_check PASS
- pytest unit domain + alc + existing smoke
- completion-report.md

---

## By part

| Part | Tasks |
|------|-------|
| Structure | T7, T10 |
| Backend | T1–T6, T8, T11 |
| Frontend | T9, T11 |

*End of Phase 3 tasks.*
