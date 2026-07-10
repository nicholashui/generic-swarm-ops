# Design — 14 Evolution Sandbox Engine

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-14-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-14`) |
| Source | `structure.md` §5 |
| Design quality bar | 100 |

---

## 1. Purpose

Improve workflows **only through sandbox proposals**: offline fitness, security/compliance checks, optional human review, canary, rollback, lessons—**never** mutate production DNA directly. Host code self-rewrite is out of scope.

---

## 2. Context

Non-negotiable: Evolution Manager proposes; does not rewrite production in place. Reflective NL optimization allowed only inside sandbox gates.

---

## 3. Architecture

```text
Observe (runs/PI/lessons)
  → Propose (sandbox_only variant)
  → Offline eval (golden/regression/adversarial/replay)
  → Security + compliance checks
  → Human review if risk requires
  → Canary (limited scope)
  → Monitor metrics
  → Promote versioned OR Rollback
  → Store lessons + archive
```

### 3.1 Components

| ID | Component | Path/API |
|----|-----------|----------|
| C-14-1 | Variant store | evolution_variants |
| C-14-2 | Corpus eval | infrastructure/evolution |
| C-14-3 | Fitness scorer | multi-metric F |
| C-14-4 | Lifecycle API | propose/eval/canary/promote/rollback |
| C-14-5 | Archive | GET /evolution/archive |
| C-14-6 | Reflect/lessons | self_improvement |
| C-14-7 | Auto-propose | POST /improvement/auto-propose |
| C-14-8 | Skill sandbox | /improvement/skills/* → _sandbox/ |
| C-14-9 | Loop runner | /loops/run |
| C-14-10 | FE Improve | run detail pipeline |
| C-14-11 | Guards | reject auto_promote / direct mutate |

### 3.2 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-14-01 | Variants = DNA data clones | Not git host rewrites |
| D-14-02 | No DGM host rewrite | Explicit non-goal |
| D-14-03 | Reflect only pre-canary for DNA changes | Safety |
| D-14-04 | Weights default equal until configured | Transparent fitness |

---

## 4. Variant state machine

### 4.1 States

`sandbox | evaluated | approved_for_canary | canary | promoted | rolled_back | rejected`

### 4.2 Transitions

| From | Event | To | Guards |
|------|-------|-----|--------|
| — | propose | sandbox | always sandbox_only |
| sandbox | evaluate | evaluated | corpus ran |
| evaluated | fail metrics/safety | rejected | |
| evaluated | pass + human if needed | approved_for_canary | checklist |
| approved_for_canary | canary deploy | canary | limited scope |
| canary | metrics ok + promote | promoted | version bump; checklist |
| canary | metrics fail | rolled_back | restore prior |
| * | direct production write | **forbidden** | |

### 4.3 Variant model

```text
EvolutionVariant {
  id, baseline_workflow_id, baseline_version,
  proposed_dna | patch,
  status, sandbox_only: true,
  fitness: { Q,S,C,E,H,R,L,K, F? },
  eval_report_id, canary_scope?,
  created_at, updated_at
}
```

---

## 5. Fitness function

\[
F = w_q Q + w_s S + w_c C + w_e E + w_h H - w_r R - w_l L - w_k K
\]

Default \(w_* = 1\) unless configured. Store component scores for multi-metric comparison (Pareto UI optional).

**Promotion forbids:** lower safety/compliance than baseline; failed regression/adversarial; missing rollback; incomplete audit; missing human sign-off when required; no metric improvement.

---

## 6. Pipeline step mapping (structure §5.3)

| # | Step | Design element |
|---|------|----------------|
| 1–2 | Observe/detect | runs, PI, reflect |
| 3 | Generate | propose/auto-propose |
| 4–7 | Offline/security/compliance/replay | corpus eval module |
| 8 | Human review | approvals / evolution review |
| 9–10 | Canary/monitor | canary status + metrics |
| 11 | Promote/rollback | versioned APIs |
| 12 | Lessons | improvement_lessons + disk |

---

## 7. API contract

| Method | Path |
|--------|------|
| POST | evolution propose / evaluate / canary / promote / rollback |
| GET | `/api/v1/evolution/archive` |
| POST | `/api/v1/improvement/reflect/{run_id}` |
| GET | `/api/v1/improvement/lessons` |
| POST | `/api/v1/improvement/auto-propose` |
| POST | `/api/v1/loops/run` |
| * | `/api/v1/improvement/skills/*` |

Config: `GENERIC_SWARM_AUTO_REFLECT`, `GENERIC_SWARM_LLM_CRITIC_ENABLED`.

---

## 8. NFR design

| NFR | Design |
|-----|--------|
| NFR-14-01 Offline eval ≤15 min reference | Disk corpus |
| NFR-14-02 Archive list ≤2s baseline | Indexed variants |
| NFR-14-03 No prod creds in sandbox beyond fixtures | env isolation |
| NFR-14-04 Auditable artifacts | business/evolution + store |
| NFR-14-05 Skills sandbox | _sandbox path |

---

## 9. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-14-01…03 | §4 forbidden + guards | unit auto_promote |
| FR-14-04…05 | §5 fitness | fitness fields |
| FR-14-06…14 | §3 pipeline + §4 SM | p3 + e2e improve |
| FR-14-15…20 | §5 promote checklist | promote guards |
| FR-14-21…22 | reflect sandbox | SI tests |
| NFR-14-01…05 | §8 | evolution:check |
| AC-14-01…06 | §7 FE/API | E1 tail |

---

## 10. Validation design

Direct mutate blocked; propose→eval→canary→rollback; lessons; archive; skill sandbox.

---

## 11. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-14-01 | Full generic population search UI | Archive ranking first |
| OI-14-02 | DGM host rewrite | Forbidden non-goal |

---

## 12. Design score claim

**Self-score: 100** — full state machine, fitness, pipeline, API, guards, RTM.
