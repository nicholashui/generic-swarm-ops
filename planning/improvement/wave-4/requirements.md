# Wave 4 Requirements — Multi-Pack Proof, Load & Security Hardening

**Wave:** 4  
**Source of truth:** `improvements.md` v1.0 § Wave 4  
**Cross-refs:** `adoption.md` v2.3 (N1/N2/N3), `repo_compare.md`, Wave 0–3 exits under `planning/improvement/wave-{0,1,2,3}/`  
**Date:** 2026-07-12  
**Status:** Ready for design / implementation  

---

## 1. Goal of this wave

Prove **N2 at scale**: the host runs **multiple domain packs** cleanly under isolation, load, and security pressure—without forking the runtime or shrinking the video roster.

1. **Load:** ≥20 concurrent (or batched concurrent-start) **mixed-domain** workflow runs complete or reach a safe terminal/wait state without host crash or cross-domain corruption.
2. **Security:** Red-team **video tool misuse** + **prompt injection** scenarios; unauthorized tools stay blocked; **allow-list must not expand** from adversarial input.
3. **Cross-pack isolation expanded:** lessons, episodes, eval corpus overlays, and tool namespaces do not bleed across `video` / `example_research` / third lite pack.
4. **Docs kit:** “Add a Domain Pack” runbook + **versioning matrix** (manifest, DNA, ALC, tools, evals).
5. **Optional third pack:** lite `example_education` (or equivalent) proving a third domain registers and runs a stub DNA.
6. Protect **E1**, inventory **114**, Wave 1–3 ALC / spine / coevolution paths.

**Out of scope (Wave 5+):** Full 114 activation, full A–J DNA depth, real media providers, advanced timeline FE, Temporal adapters.

---

## 2. Non-negotiables (N1 / N2 / N3)

From `adoption.md` v2.3 §0 (quoted sense):

| # | Requirement |
|---|-------------|
| **N1** | **va-agent-swarm** keeps **all** video agent-specific business logic; every agent must gain **mandatory autonomous learning** (individual knowledge growth). Video logic lives only under domain pack paths (`business/video/` …). Every registered agent must implement the **Agent Learning Contract** (ALC) or fail activation. |
| **N2** | **generic-swarm-ops** becomes a **universal foundation** for dozens of multi-agent (MMA) systems beyond video. Introduce **Domain Pack** interface, schemas, registration hooks, and isolation so any `business/<domain>/` onboard is config + artifacts, not a fork of the runtime. |
| **N3** | **Adopt ALL agents and ALL business processes from va-agent-swarm** into the generic project — from **orchestrator / planner / meta-agents down through every specialist and workflow-support agent**. **No agent may be dropped.** Inventory CI remains enforced for video pack presence. |

**Wave 4 enforcement:**

- **N1:** Video tools remain namespaced; red-team must not grant video agents ops/billing tools; video fixtures stay under `business/video/`.
- **N2:** Third pack + mixed-domain load + runbook prove multi-pack host without core forks.
- **N3:** Inventory still PASS 114; no agent deletion for “load” convenience.

**Additional:** Evolution/skill promote remain explicit; no auto-promote; sandbox discipline for adversarial evals.

---

## 3. Functional requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-W4-01 | Unit/load harness starts **≥20** workflow runs mixing ≥2 domains (e.g. ops flagship, example_research, video stub DNA, and/or third pack). | P0 |
| FR-W4-02 | Under load, runs reach `completed`, `waiting_for_approval`, or controlled `failed` (tool denial)—not silent hang or store corruption of other domains’ lessons. | P0 |
| FR-W4-03 | **Red-team:** video-scoped agent cannot successfully execute non-video / ops tools (e.g. `billing_system`) even if DNA or input requests them. | P0 |
| FR-W4-04 | **Prompt injection:** adversarial input text must **not** expand `agent.allowed_tools` or bypass allow-list; unauthorized attempts fail and are auditable. | P0 |
| FR-W4-05 | **Cross-pack isolation:** agent A’s lessons/episodes not returned for agent B across domains; corpus overlay for domain X does not inject domain Y-only goldens. | P0 |
| FR-W4-06 | Structure adversarial fixtures for video tool misuse / injection under pack or `business/security` / `business/evals`. | P0 |
| FR-W4-07 | Docs: `docs/add-domain-pack-runbook.md` (or equivalent) + versioning matrix. | P0 |
| FR-W4-08 | Optional third pack `example_education` (lite): manifest, ≥2 ALC agents, 1 DNA, 1 golden; registerable. | P1 (in-wave preferred) |
| FR-W4-09 | FE: multi-pack summary (domain count / isolation hint) on DomainPackPanel without breaking typecheck. | P1 |
| FR-W4-10 | Inventory 114 + full unit suite green; E1 not broken. | P0 |

---

## 4. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR-W4-01 | Load tests run offline without external LLM/network. |
| NFR-W4-02 | Load suite finishes in CI-reasonable time (< ~2 min for the new tests). |
| NFR-W4-03 | No second control plane; no pack-specific forks of runtime. |
| NFR-W4-04 | Security tests fail closed (deny > allow). |
| NFR-W4-05 | Third pack does not alter video inventory count. |
| NFR-W4-06 | Sandbox/evolution paths remain non-auto-promoting under adversarial DNA. |

---

## 5. Success / acceptance criteria

| Gate | Pass condition |
|------|----------------|
| AC-1 | Load test: ≥20 mixed-domain runs started; majority terminal/wait; no exception storm |
| AC-2 | Isolation: cross-domain lesson/episode retrieve empty for foreign agent_id |
| AC-3 | Security: unauthorized video tool misuse → failed run / denied; allow-list size unchanged |
| AC-4 | Injection payload does not add tools to `allowed_tools` |
| AC-5 | Runbook + versioning matrix published under `docs/` |
| AC-6 | Third pack present and register path works (if FR-W4-08 in scope) |
| AC-7 | Inventory PASS 114; full unit suite green |
| AC-8 | FE multi-pack summary renders (if FE touched) |
| AC-9 | Completion report under `planning/improvement/wave-4/` |

---

## 6. Traceability

| Item | Source |
|------|--------|
| Multi-pack load | improvements.md Wave 4; adoption N2 |
| Red-team tool misuse / injection | improvements.md Wave 4; structure security; existing adversarial fixture |
| Cross-pack isolation | improvements.md Wave 4; Wave 1 isolation baseline |
| Runbook + versioning | improvements.md Wave 4; domain-packs.md |
| Third lite pack | improvements.md Wave 4 optional |
| Protect E1 / inventory | improvements.md §5.1; N3 |

---

## 7. Structure / Backend / Frontend requirements

### 7.1 Structure

| ID | Requirement |
|----|-------------|
| ST-W4-01 | Adversarial / red-team fixtures for video tool misuse + injection. |
| ST-W4-02 | Runbook + versioning matrix docs. |
| ST-W4-03 | Optional `business/example_education/` lite pack. |
| ST-W4-04 | SDD + completion under `planning/improvement/wave-4/`. |
| ST-W4-05 | Do not remove video roster agents. |

### 7.2 Backend

| ID | Requirement |
|----|-------------|
| BE-W4-01 | Load harness / unit test for ≥20 mixed-domain runs. |
| BE-W4-02 | Expanded isolation tests (lessons, episodes, corpus domain). |
| BE-W4-03 | Red-team security unit tests (tool misuse + injection allow-list immutable). |
| BE-W4-04 | Optional small isolation/security helper module if reuse warrants. |
| BE-W4-05 | Third pack registration covered by tests when pack exists. |

### 7.3 Frontend

| ID | Requirement |
|----|-------------|
| FE-W4-01 | DomainPackPanel shows multi-pack count / domains listed. |
| FE-W4-02 | Isolation/N2 hint text for operators. |
| FE-W4-03 | No lint/typecheck regression on touched files. |

---

## 8. Risks & constraints

| Risk | Mitigation |
|------|------------|
| Runtime store not thread-safe | Prefer concurrent-**start** batch + serial dispatch; document true multi-thread as future hardening |
| Load flakiness | Deterministic stub tools only; no sleep-based assertions beyond timeouts |
| Security false pass | Assert allow-list identity before/after + failed status |
| Third pack scope creep | Lite only: 2 agents, 1 DNA, 1 golden |
| Breaking E1 | Full unit suite gate |

---

## 9. Internal critic (Phase 1)

| Question | Answer |
|----------|--------|
| Proves N2? | Yes — 3 packs + load + isolation + runbook. |
| N1 video safe? | Red-team blocks tool escape; inventory untouched. |
| N3? | 114 inventory remains. |
| Wave 5 bleed? | No full roster activation. |

*End Phase 1 — Requirements.*
