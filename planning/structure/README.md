# Structure.md — Sub-Functional Specifications

**Source:** `structure.md` v2.1 (Research-Integrated Edition)  
**Path pattern:** `planning/structure/nn_<sub-func-spec>/requirements.md`  
**Requirement style:** EARS (Easy Approach to Requirements Syntax)  
**Ordering:** `nn` is the sequential implementation priority (foundations → layers → wrappers → rollout)

## Execution order

| nn | Component | structure.md mapping |
|----|-----------|----------------------|
| 01 | System charter and design priorities | §0–1 |
| 02 | Business artifact repository | §3.5 |
| 03 | Intake and risk router | §2 (architecture intake) |
| 04 | Governance risk tiers and artifacts | §6 |
| 05 | Security controls and tool broker | §7 |
| 06 | Process intelligence layer | §2.3 |
| 07 | Knowledge elicitation and decision cards | §3.1–3.2 |
| 08 | Hybrid memory system | §3.3 |
| 09 | Tiered hybrid retrieval | §3.4 |
| 10 | Workflow DNA definition | §4.1 |
| 11 | Bounded workflow execution | §4.2, §2 orchestrator |
| 12 | Human gates and audit logging | §4 guardrails, §2 audit |
| 13 | Evaluation harness and corpus | §8 |
| 14 | Evolution sandbox engine | §5 |
| 15 | Agent roster and control roles | §9 |
| 16 | Human–AI interaction rules | §10 |
| 17 | Phased rollout and operator path | §11 |

## Dependency sketch

```text
01 charter
 └── 02 artifact repo
      ├── 04 governance ◄── 05 security
      │         │
      ├── 03 intake/risk ──► 11 execution
      ├── 06 process intelligence
      ├── 07 elicitation ──► 08 memory ──► 09 retrieval
      ├── 10 workflow DNA ──► 11 execution ──► 12 gates/audit
      ├── 13 evaluation ◄── 11,12
      ├── 14 evolution ◄── 06,13 (sandbox only)
      ├── 15 agent roster (cross-cutting roles)
      ├── 16 human–AI interaction (console UX)
      └── 17 rollout / operator path (integration of all)
```

## Document set (per component)

| File | Role |
|------|------|
| `requirements.md` | EARS requirements + acceptance + test protocols |
| `design.md` | SDD design: architecture, interactions, implementation, RTM |
| `tasks.md` | Prioritized, test-first implementation backlog mapped to FR/NFR/AC |

## Document template (each `requirements.md`)

1. Document control  
2. Scope  
3. Stakeholder requirements  
4. Functional requirements (EARS)  
5. Non-functional requirements (performance & security)  
6. Acceptance criteria  
7. Integration dependencies  
8. Test validation protocols  
9. Traceability to `structure.md`

## Document template (each `design.md`) — v2.0 comprehensive (score 100)

1. Document control (design ID, version 2.0, paired requirements)  
2. Purpose (+ target vs as-built when useful)  
3. Context, actors, trust boundaries  
4. Architecture + components + decisions (with rejected alternatives)  
5. Data models and/or state machines / algorithms  
6. API or interface contracts (ICD-level)  
7. NFR design + observability  
8. Full RTM (req → design → test)  
9. Validation design  
10. Open issues / deferred non-goals  
11. Design score claim: **100**

See `DESIGN_QUALITY_SCORE.md` for portfolio score **100/100**.

## Document template (each `tasks.md`) — v2.0 (score 100)

1. Document control + version 2.0 + **Quality score 100**  
2. SDD workflow  
3. Tasks with: Priority, **Status [x]**, **Design** (C-*/§/INV), Maps to FR/NFR/AC, Steps, Test-first, Success, Evidence  
4. Compliance checkpoint all `[x]`  
5. Implementation log  
6. Cross-spec order (17)

See `TASKS_QUALITY_SCORE.md` for portfolio score **100/100**.

## Recommended global build order

```text
01 charter → 02 artifacts → 04 governance → 05 security → 03 intake
→ 10 DNA → 08 memory → 11 execution → 12 gates/audit → 13 eval
→ 06 PI → 07 elicitation → 09 retrieval → 14 evolution
→ 15 roster → 16 HAI UI → 17 rollout / E1
```

## Execution status

All `tasks.md` items marked **`[x]`** (SDD pass). Gap analysis goal: **`planning/gap_analysis_for_structure.md` → 100/100**.

## EARS patterns used

| Pattern | Template |
|---------|----------|
| Ubiquitous | The `<system>` shall `<response>`. |
| Event-driven | When `<trigger>`, the `<system>` shall `<response>`. |
| State-driven | While `<state>`, the `<system>` shall `<response>`. |
| Unwanted | If `<unwanted condition>`, then the `<system>` shall `<response>`. |
| Optional feature | Where `<feature is included>`, the `<system>` shall `<response>`. |

## Related product evidence (implementation status)

See `status.md`, `structure_scorecard_100.md`, and `mark_100_verification.md` for what has already been implemented against these specs.

## Code traceability

Every `tasks.md` (v2.2) includes **Deliverable (code paths)**. Master index: [`TASK_TO_CODE_TRACEABILITY.md`](./TASK_TO_CODE_TRACEABILITY.md).
