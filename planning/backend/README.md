# backend.md — Sub-Functional Specifications

**Source:** `backend.md` (Backend API Server Requirements, Design, and Implementation Plan)  
**Architecture SoT:** `structure.md` (§12 implementation mapping)  
**Path pattern:** `planning/backend/nn_<sub-func-spec>/requirements.md`  
**Requirement style:** EARS (Easy Approach to Requirements Syntax)  
**Ordering:** `nn` is the sequential implementation priority (platform foundations → domain APIs → safety wrappers → proof)

## Execution order

| nn | Component | backend.md mapping |
|----|-----------|--------------------|
| 01 | Platform Charter, Boundaries, and Design Principles | §1 Purpose, §2 Primary Objective, §4 System Boundary, §5 High-Level Architecture, §6 Core Design Principles |
| 02 | Runtime Stack and Project Scaffold | §3 Recommended Technology Stack, §9 Recommended Backend Folder Structure, §8.5 Maintainability |
| 03 | Persistence Control Plane | §10 Data Model (infra), §18 env DATABASE_URL, §24.3 Postgres runtime_state |
| 04 | API Contract, Envelope, and Errors | §6.1 API First, §11.1–11.3 Versioning / Response Format / Error Codes |
| 05 | Authentication and Identity | §7.1 Authentication, §11.4 Authentication Endpoints, §16 security auth |
| 06 | Authorization and RBAC | §7.2 Authorization, permission groups, future ABAC notes |
| 07 | Users, Organizations, and Tenancy | §7.3 User and Organization Management, §10.2–10.3, org settings APIs |
| 08 | Agent Registry | §7.4 Agent Registry, §10.4, §11.5, §15 Agent Runtime Design |
| 09 | Tool Registry, Adapters, and Broker | §7.5 Tool Registry, tool_effects as-built, tool permission broker |
| 10 | Workflow Definition and Versioning | §7.6 Workflow Management, §10.5–10.6, §11.6 |
| 11 | Workflow Run Execution Engine | §7.7–7.8 Runs/Steps, §11.7, §12 Workflow Execution Design, idempotency |
| 12 | Governance Policies and Risk | §7.9 (policy engine), §11.11, §13 Governance Design |
| 13 | Human Approval Gates | §6.4 HITL, §7.9 approvals, §11.8 Approval Endpoints |
| 14 | Audit Logging | §6.5 Audit Everything, §7.13, §10.14, §11.13 |
| 15 | Knowledge Base and Retrieval | §7.10, §11.9, §14.1–14.2, tiered retrieval as-built |
| 16 | Memory System | §7.11, §11.10, §14.3 Memory Rules |
| 17 | Evaluation System | §7.12, §11.12, evaluation design links |
| 18 | Process Intelligence | §7.14, §11.14, PI disk artifacts |
| 19 | Streaming, Health, and Observability | §7.18 Streaming, §8.4 Observability, §17 Health/Metrics/Logs |
| 20 | Evolution Sandbox APIs | §7.15, §11.15, §24.3 evolution as-built |
| 21 | Self-Improvement and Loops | §7.16, §11.16 Improvement / Loop Endpoints |
| 22 | Production DNA Safety | §7.17 Production DNA Safety, structure_validators, business:validate |
| 23 | Security Hardening and Cross-Cutting NFRs | §8 Non-Functional Requirements, §16 Security Design, rate limits, injection |
| 24 | Testing Strategy and Operator Path | §19 Testing Strategy, §21 MVP, §22 Definition of Done, §24 E1/non-goals |

## Dependency sketch

```text
01 charter
 └── 02 stack/scaffold
      └── 03 persistence control plane
           └── 04 API envelope
                ├── 05 authentication ──► 06 RBAC ──► 07 users/orgs
                │                              │
                ├── 08 agents ──► 09 tools/adapters/broker
                ├── 10 workflow definition ──► 11 run engine
                │         ▲                      │
                │         │                      ├─► 12 governance ◄── tiers
                │         │                      ├─► 13 human approvals
                │         │                      ├─► 14 audit
                │         │                      ├─► 15 knowledge/retrieval
                │         │                      ├─► 16 memory
                │         │                      ├─► 17 evaluation
                │         │                      ├─► 18 process intelligence
                │         │                      └─► 19 streaming/health/observability
                ├── 22 production DNA safety ──► 10/11/20
                ├── 20 evolution sandbox ◄── 17,22
                ├── 21 self-improvement ◄── 11,20,17
                ├── 23 security hardening & NFRs (cross-cutting)
                └── 24 testing strategy & operator path (E1 / DoD)
```

## Document set (per component)

| File | Role |
|------|------|
| `requirements.md` | EARS requirements + acceptance + test protocols (this decomposition) |
| `design.md` | SDD design v2.0: architecture, ICD, RTM (**score 100**; see `DESIGN_QUALITY_SCORE.md`) |
| `tasks.md` | SDD implementation backlog **v2.1** (**score 100**; see `TASKS_QUALITY_SCORE.md`) |
| `DESIGN_QUALITY_SCORE.md` | Portfolio design quality assessment report (**100/100**) |

## Document template (each `requirements.md`)

1. Document control  
2. Scope  
3. Stakeholder requirements  
4. Functional requirements (EARS)  
5. Non-functional requirements (performance & security)  
6. Acceptance criteria  
7. Integration dependencies  
8. Test validation protocols  
9. Traceability to `backend.md` / `structure.md`

## Recommended global build order

```text
01 charter → 02 scaffold → 03 persistence → 04 envelope
→ 05 auth → 06 RBAC → 07 users/orgs
→ 08 agents → 09 tools → 10 workflows → 12 governance → 13 approvals
→ 11 run engine → 14 audit → 19 health/stream
→ 15 knowledge → 16 memory → 17 evaluation → 18 PI
→ 22 DNA safety → 20 evolution → 21 self-improvement
→ 23 security/NFR hardening → 24 tests & E1 proof
```

## EARS patterns used

| Pattern | Template |
|---------|----------|
| Ubiquitous | The `<system>` shall `<response>`. |
| Event-driven | When `<trigger>`, the `<system>` shall `<response>`. |
| State-driven | While `<state>`, the `<system>` shall `<response>`. |
| Unwanted | If `<unwanted condition>`, then the `<system>` shall `<response>`. |
| Optional feature | Where `<feature is included>`, the `<system>` shall `<response>`. |

## Related product evidence

See `status.md`, `backend/README.md`, `structure_scorecard_100.md`, `mark_100_verification.md`, and `planning/gap_analysis_for_structure.md` for as-built status against the parent architecture. This backend decomposition is the **requirements** layer for `backend.md`; it does not replace `structure.md`.
