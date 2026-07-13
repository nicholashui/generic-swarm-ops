# Wave 0 Requirements — Foundations (Inventory, Skeletons, Schemas, CI Gates)

**Wave:** 0  
**Source of truth:** `improvements.md` v1.0 §4 Wave 0  
**Cross-refs:** `adoption.md` v2.3, `repo_compare.md`, `improvement_prompt.txt`  
**Date:** 2026-07-11  
**Status:** Approved for implementation after design + tasks  

---

## 1. Goal of this wave

Complete the **catalog foundation** for the video Domain Pack and the **Domain Pack schema surface** so that:

1. All **114** va agents are present in-repo under `business/video/agents/<pack_id>/` as L0 Catalog assets (dirs + minimal `agent_spec.json` + stub `SPEC.md`).
2. Full process **index** exists (`PROCESSES.md`) without requiring deep runnable DNA yet.
3. Platform schemas for domain packs / agent specs / learning logs exist and validate.
4. **Inventory CI** fails closed if the video roster is incomplete.
5. A **draft domain register stub** accepts valid manifests for `video` and `example_research` (or `example_domain`) without activating runtime ALC (Wave 1).
6. Existing product bar remains green: **no E1 regression**, no host self-rewrite, no video logic in core runtime.

**Out of scope for Wave 0:** runtime ALC wiring, deep SPEC for all agents, media adapters, spine E2E DNA, FE full domain UI, agent genomes.

---

## 2. Non-negotiables (quote N1 / N2 / N3)

From `adoption.md` v2.3 §0:

| # | Requirement (verbatim sense from adoption.md) |
|---|-----------------------------------------------|
| **N1** | **va-agent-swarm** keeps **all** video agent-specific business logic; every agent must gain **mandatory autonomous learning** (individual knowledge growth). Video logic lives only under domain pack paths (`business/video/` …). Every registered agent must implement the **Agent Learning Contract** (ALC) or fail activation. |
| **N2** | **generic-swarm-ops** becomes a **universal foundation** for dozens of multi-agent (MMA) systems beyond video. Introduce **Domain Pack** interface, schemas, registration hooks, and isolation so any `business/<domain>/` onboard is config + artifacts, not a fork of the runtime. |
| **N3** | **Adopt ALL agents and ALL business processes from va-agent-swarm** into the generic project — from **orchestrator / planner / meta-agents down through every specialist and workflow-support agent**. **No agent may be dropped, archived-out, or left only in the external va repo as the long-term home.** Complete roster import of **114** agents; complete process import/index; retention in-project forever; pack CI fails if MAP count &lt; roster or any agent lacks a pack directory. |

**Wave 0 enforcement of non-negotiables:**

- **N1:** All video assets under `business/video/` only; `agent_spec` carries ALC fields (`requires_alc`, scopes) even if hard-gate is Wave 1.
- **N2:** Schemas + register stub + optional `business/example_research/` skeleton prove multi-pack shape without video-only host changes.
- **N3:** Exactly **114** agent dirs + ROSTER + MAP 1:1; no “P0-only” omissions; inventory check fails if incomplete.

---

## 3. Functional requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-W0-01 | Parse / materialize full roster from `adoption.md` Appendix A (aligned with va `study/agents.md`) into `business/video/ROSTER.json` (114 entries: id, name, category, pack_id). | P0 |
| FR-W0-02 | Produce `business/video/MAP.md` with one row per agent: va_id, name, pack_id, category, va_source, genetic→**generic** path, runtime_status=draft. | P0 |
| FR-W0-03 | Produce `business/video/PROCESSES.md` indexing orchestration spine, 6-phase E2E, archetypes A–J, LQR family, human→AI maps, UI process docs, deep-spec modules (adoption §5.0). | P0 |
| FR-W0-04 | Create `business/video/` tree: agents, workflows, tools, evals/{golden,regression,adversarial}, knowledge/seeds, policies, ui; plus `README.md` with N3 retention policy. | P0 |
| FR-W0-05 | For every pack_id: directory + `agent_spec.json` (draft, ALC fields) + stub `SPEC.md` (link to va source). | P0 |
| FR-W0-06 | Add JSON Schemas: `domain-manifest.schema.json`, `agent-spec.schema.json`, `learning-log.schema.json` under `business/schemas/`. | P0 |
| FR-W0-07 | Positive/negative fixtures for schemas; validation via existing schema-lite or unit tests. | P0 |
| FR-W0-08 | Inventory gate: fail if agent dir count ≠ 114, MAP incomplete, or any roster pack_id missing dir/spec. | P0 |
| FR-W0-09 | Domain register **stub** (CLI and/or minimal API): validate manifest against schema; return draft status for `video` and example pack; no production activation. | P0 |
| FR-W0-10 | Optional but recommended: `business/example_research/` minimal skeleton (manifest + 1–2 toy agents + README for N2). | P1 |
| FR-W0-11 | Docs: `docs/domain-packs.md`; short Domain Pack sections in structure/backend/frontend docs; handoff/status notes. | P0 |
| FR-W0-12 | Do **not** implement deep runtime ALC, media adapters, or spine DNA execution in Wave 0. | P0 |

## 4. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR-W0-01 | E1 operator path and backend unit suite remain green (protect mark ~100). |
| NFR-W0-02 | No second control plane; no LangGraph/Temporal host. |
| NFR-W0-03 | No hard-coded video business logic in `backend/app/runtime.py` core flows (register stub may be thin and domain-agnostic). |
| NFR-W0-04 | Provenance: roster/MAP/SPEC stubs cite `va-agent-swarm` paths + `adoption.md` §5.0 / Appendix A. |
| NFR-W0-05 | Inventory check runnable offline (pytest/script) without live media APIs. |
| NFR-W0-06 | Idempotent generation: re-running skeleton scripts must not drop agents. |

---

## 5. Success / acceptance criteria (measurable)

| Gate | Pass condition |
|------|----------------|
| AC-1 | `len(business/video/agents/*)` == **114** |
| AC-2 | `ROSTER.json` length == 114; unique pack_ids; ids 1–114 |
| AC-3 | `MAP.md` data rows == 114 |
| AC-4 | Every agent dir has `agent_spec.json` with `requires_alc: true`, `domain_id: "video"`, `status: "draft"`, `allowed_memory_scopes` includes `"agent"` |
| AC-5 | `PROCESSES.md` mentions Orchestrator/Planner, phases 1–6, A–J, LQR |
| AC-6 | Three new schemas validate fixtures (positive pass, negative fail) |
| AC-7 | Inventory test/script **fails** if one agent dir removed; **passes** on complete tree |
| AC-8 | Register stub accepts example manifests for video + example pack (draft) |
| AC-9 | Backend unit suite still passes (no intentional E1 break); no FE regression required beyond “no FE breakage if untouched” |
| AC-10 | `docs/domain-packs.md` exists and references N1/N2/N3 |

---

## 6. Traceability

| This wave | Source |
|-----------|--------|
| Catalog / ROSTER / MAP / 114 dirs | `improvements.md` Wave 0 tasks 1–2; `adoption.md` §5.0, Appendix A, N3 |
| PROCESSES index | `improvements.md` W0-T1; `adoption.md` §5.0 process table |
| Schemas domain/agent/learning | `improvements.md` W0-T3; `adoption.md` §3.1 Domain Pack |
| Inventory CI | `improvements.md` W0-T4; `adoption.md` inventory CI contract |
| Register stub | `improvements.md` W0-T4; N2 |
| Docs | `improvements.md` W0-T5; `repo_compare.md` multi-domain gap |
| Isolation of video pack | `repo_compare.md` final recommendation; N1 |

---

## 7. Risks & constraints

| Risk | Mitigation |
|------|------------|
| Scope explosion into deep SPECs for 114 agents | Wave 0 = L0 only; deep SPEC on activation (adoption rethink) |
| Dropping agents accidentally | Inventory CI; no delete policy in README |
| Dual orchestrator confusion | Document ops `business_orchestrator` vs `video.orchestrator` |
| Register stub becomes full runtime | Keep draft-only; full ALC in Wave 1 |
| E1 regression | Do not rewrite runtime engine; run unit suite after |
| Path pollution (genetic typo) | Use **generic-swarm-ops** only |

---

## 8. Structure / Backend / Frontend requirements

### 8.1 Structure (business/, docs/, planning/)

- Own ROSTER, MAP, PROCESSES, agent dirs, manifests, schemas, fixtures, domain-packs.md, example_research skeleton.
- Structure is the **primary** deliverable of Wave 0.

### 8.2 Backend

- Inventory test under `backend/app/tests/unit/` (or scripts invoked by tests).
- Optional thin domain-register stub (script preferred; API route only if non-invasive).
- **No** ALC hard-gate implementation; **no** lesson.agent_id runtime work (Wave 1).
- Protect existing routes and E1 tests.

### 8.3 Frontend

- **No required UI features** for Wave 0.
- Constraint: do not break existing ops console; no mandatory new routes.
- Docs may note future `/app/domains/video` (Wave 1–2).

---

## 9. Critic / rethink notes (Phase 1)

- Wave 0 is **catalog + contracts**, not “demo day video swarm.”
- Claiming N3 complete after Wave 0 is **forbidden** — only L0 catalog readiness.
- Register stub must not imply production activation without ALC (Wave 1).

*End of Phase 1 requirements.*
