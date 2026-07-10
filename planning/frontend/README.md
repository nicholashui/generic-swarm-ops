# frontend.md — Sub-Functional Specifications

**Source:** `frontend.md` (Frontend Server / Ops Console Requirements, Design, and Implementation Plan)  
**Architecture SoT:** `structure.md` (§10–§12; implementation mapping)  
**Backend control plane:** `backend.md` + `planning/backend/` (FE never re-implements policy)  
**Path pattern:** `planning/frontend/nn_<sub-func-spec>/requirements.md`  
**Requirement style:** EARS (Easy Approach to Requirements Syntax)  
**Ordering:** `nn` is the sequential implementation priority (charter → scaffold → design system → shell/auth → API client → domain pages → evolution/improve → cross-cutting quality)

## Execution order

| nn | Component | frontend.md mapping |
|----|-----------|---------------------|
| 01 | Frontend Charter, Scope, and Design Principles | §1 Purpose, §2 Product Vision, §3 Core Design Principle, §4 Scope, §6 Runtime Responsibilities, §32 Final Frontend Rule, §33 Implementation Mapping |
| 02 | Next.js Scaffold, Stack, and Folder Structure | §5 Recommended Technology Stack, §7 Application Architecture, §18 Frontend Folder Structure, §19 Environment Variables, Phase 1 Project Setup |
| 03 | Design System, Tokens, and OpenDesign Workflow | §3 Core Design Principle, §8–11 OpenDesign MCP / Trae rules, §14 Core Layout Design, §15 Visual Design, §17 Reusable Components, Phase 2–3 |
| 04 | App Shell, Navigation, and Information Architecture | §7.3 Route Protection, §12 Information Architecture, §14 Core Layout Design, Phase 5 App Shell |
| 05 | Authentication and Session UI | §16.1–16.3a Public/Login/Register/Accept-invite, Phase 4 Authentication and Session UI, §20 API Integration auth |
| 06 | Permission-Aware Navigation and UI | §13 User Roles and Permissions, §6.3 Boundary Rule, permission-aware navigation in §4.1 |
| 07 | Typed API Client and OpenAPI Integration | §20 API Integration, §33.3a Backend API contracts, pnpm api:generate, DEMO_MODE ops profile |
| 08 | Dashboard Page | §16.4 Dashboard Page, Phase 6 Dashboard, §12.1 /app |
| 09 | Agents and Tools UI | §16.5–16.9 Agents/Tools pages, Phase 7 Agents and Tools |
| 10 | Workflows Definition UI | §16.10–16.12 Workflows list/create/detail, Phase 8 Workflows |
| 11 | Workflow Run Realtime UI | §16.13 Workflow Run Detail, §21 Real-Time Updates, Phase 9, run pause/resume/expire §33.3a |
| 12 | Approvals and Human Gates UI | §16.14–16.15 Approvals list/detail, Phase 10 Approvals, human gates §33 |
| 13 | Knowledge and Memory UI | §16.16–16.19 Knowledge/Memory pages, Phase 11 |
| 14 | Evaluations and Processes UI | §16.20–16.22 Evaluations/Processes pages, Phase 12 |
| 15 | Audit Logs UI | §16.23 Audit Logs Page, Phase 13 (audit portion) |
| 16 | Settings, Users, Organization, and API Keys UI | §16.24–16.28 Settings suite, Phase 13 Settings, §33.3a users/orgs/invitations |
| 17 | Evolution Sandbox Archive UI | §16.13a Evolution Archive Page, §4.1 Evolution section, §33.3 Evolution UI |
| 18 | Improve Pipeline UI (Reflect → Propose → Evaluate → Canary) | §1 Improve pipeline, §16.13 Improve actions, §33.3 Self-improvement UI, Phase D evolution |
| 19 | Accessibility, Loading, Empty, and Error States | §22 Loading/Empty/Error States, §23 Accessibility Requirements, §29 product ideas (UX quality) |
| 20 | Security, Performance, Testing, and Ops Profile | §24 Security, §25 Performance, §26 Observability, §27 Testing, §28 Phase 14, §30–31 Acceptance/DoD, §33 non-goals & ops profile |

## Dependency sketch

```text
01 charter
 └── 02 Next.js scaffold/stack
      └── 03 design system / OpenDesign
           ├── 07 typed API client / OpenAPI
           ├── 05 auth & session UI
           │     └── 06 permission-aware UI
           └── 04 app shell / IA / navigation
                ├── 08 dashboard
                ├── 09 agents & tools
                ├── 10 workflows ──► 11 run realtime
                │                      ├── 12 approvals / human gates
                │                      └── 18 improve pipeline
                ├── 13 knowledge & memory
                ├── 14 evaluations & processes
                ├── 15 audit logs
                ├── 16 settings / users / org / API keys
                ├── 17 evolution archive ──► 18 improve
                ├── 19 a11y + loading/empty/error (cross-cutting)
                └── 20 security / performance / testing / ops profile
```

## Document set (per component)

| File | Role |
|------|------|
| `requirements.md` | EARS requirements + scope, stakeholders, NFR, acceptance, dependencies, test protocols |
| `design.md` | SDD design v2.1: architecture, interactions, visual/UI, ICD, FR-level RTM, impl specs (**score 100**; see `DESIGN_QUALITY_SCORE.md`) |
| `tasks.md` | SDD implementation backlog v2.3: design-aligned steps, test-first milestones, residual honesty, full FR/NFR/AC/C-* RTM (**score 100**; see `TASKS_QUALITY_SCORE.md`) |
| `DESIGN_QUALITY_SCORE.md` | Portfolio design quality assessment report (**100/100**) |
| `TASKS_QUALITY_SCORE.md` | Portfolio tasks quality assessment report (**100/100**) |
| `TASK_TO_CODE_TRACEABILITY.md` | Task → `frontend/**` code path index |

## Document template (each `requirements.md`)

1. Document control  
2. Scope  
3. Stakeholder requirements  
4. Functional requirements (EARS)  
5. Non-functional requirements (performance & security)  
6. Acceptance criteria  
7. Integration dependencies  
8. Test validation protocols  
9. Traceability to `frontend.md` / `structure.md` / backend contracts  

## Recommended global build order

```text
01 charter → 02 scaffold → 03 design system
→ 07 API client → 05 auth UI → 06 permissions → 04 app shell
→ 08 dashboard → 09 agents/tools → 10 workflows → 11 run realtime
→ 12 approvals → 13 knowledge/memory → 14 evals/processes
→ 15 audit → 16 settings → 17 evolution → 18 improve
→ 19 a11y/states → 20 security/testing/ops proof
```

## EARS patterns used

| Pattern | Template |
|---------|----------|
| Ubiquitous | The frontend shall … |
| Event-driven | When <event>, the frontend shall … |
| State-driven | If <precondition>, the frontend shall … |
| Unwanted | If <unwanted>, the frontend shall not … / shall reject … |

## Related indexes

| Artifact | Path |
|----------|------|
| Parent plan | `frontend.md` |
| As-built code | `frontend/` |
| Backend SDD | `planning/backend/` |
| Structure SDD | `planning/structure/` |
| Backend API contracts (FE must honor) | `frontend.md` §33.3a, `planning/backend/TASK_TO_CODE_TRACEABILITY.md` |

## Generator

Regenerate requirements from this script:

```bash
python scripts/_gen_frontend_reqs.py
```
