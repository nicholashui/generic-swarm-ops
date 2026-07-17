# Project Construction Action List

**Product:** `generic-swarm-ops` (universal governed multi-agent host + ops console)  
**Real host path:** `C:\Project\generic-swarm-ops`  
**Workspace note:** `C:\Project\genetic-swarm-ops` is often an empty/partial mirror; **do not** treat it as the implementation root.  
**Report date:** 2026-07-16  
**Scope:** How this app was **built** — prompts, human actions, agent workflows, SDD phases, verification, and residual productization — with file-level references.

---

## 0. How to read this report

| Column | Meaning |
|--------|---------|
| **ID** | Stable construction action id (`P0-A01`, `W2-A03`, …) |
| **Phase** | Chronological / strategic phase of construction |
| **Trigger (prompt or human action)** | Exact or reconstructed user/agent prompt, or UI/ops action that caused work |
| **Agent / actor action** | What was done (implement, write SDD, test, migrate, fix) |
| **Primary deliverables** | Concrete files, APIs, UI, scripts produced |
| **Verify / acceptance** | Commands or criteria used to close the action |
| **References** | Source-of-truth docs, commits, session segments, tests |

**Construction model used throughout**

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **SDD triad** | Requirements → Design → Tasks → Implement → Tests → Completion report | `improvement_prompt.txt`, `planning/*/*/requirements.md` |
| **Product bar** | Score dimensions to 100/100 (not “all folders full”) | `plan_to_mark_100.md`, `structure_scorecard_100.md`, `mark_100_verification.md` |
| **N1/N2/N3** | Isolation / universality / full video roster retention | `adoption.md`, `improvements.md` |
| **L0→L1→L2** | Catalog → indexed → runnable | `memory/handoff.md`, `adoption.md` |
| **Dual harness** | Trae (`.trae/`) + Grok (`.grok/`) via `npm run sync` | `starter.md`, `docs/sync.md`, `AGENTS.md` |
| **Sandbox evolution** | Propose → evaluate → canary → promote; never silent prod DNA mutation | `business/evolution/`, BE-20/21 |

---

## 1. Executive timeline (high level)

| Order | Approx date | Phase name | Outcome | Key refs |
|------:|-------------|------------|---------|----------|
| 1 | 2026-07-07 → 07-10 | **P0 Starter / dual harness** | Trae+Grok bootstrap, business OS layer, sources | `starter.md`, git `08a06ac`, `docs/changelog.md` 1.2.0 / 2.1.0 |
| 2 | 2026-07-08 → 07-10 | **P1 Structure SDD** | 17 structure sub-functions; 194 tasks `[x]`; gap 100/100 | `planning/structure/`, `planning/gap_analysis_for_structure.md` |
| 3 | 2026-07-08 → 07-10 | **P2 Backend SDD + runtime** | FastAPI control plane, RuntimeStore, 24 BE areas | `planning/backend/`, `backend/app/` |
| 4 | 2026-07-08 → 07-10 | **P3 Frontend SDD + ops console** | Next.js shell, live ops, auth, 20 FE areas | `planning/frontend/`, `frontend/` |
| 5 | 2026-07-09 | **P4 Mark 100 / E1** | Product bar 100; E1 login→run→approve→improve | `plan_to_mark_100.md`, `mark_100_verification.md`, `test_e1_operator_path.py` |
| 6 | 2026-07-09 → 07-10 | **P5 Grok migrate + investigate** | Wire Grok skills/MCP; structure compliance | Session segment 000; `migrate_to_grok_build.md`, `grok_investigate_now.md` |
| 7 | 2026-07-11 | **P6 Repo compare + adoption** | generic=host, va=video pack strategy | `repo_compare.md`, `adoption.md`, `adoption_plan.md` |
| 8 | 2026-07-11 → 07-12 | **P7 Improvements Waves 0–5** | Domain Pack + ALC + N3 complete | `improvements.md`, `improvement_prompt.txt`, `planning/improvement/` |
| 9 | 2026-07-13 | **P8 VA migration + special skills** | 325 corpus, 114 SPECs, 17 special skills | `MIGRATION_COMPLETE.md`, `planning/special/` |
| 10 | 2026-07-13 → 07-14 | **P9 Executable slice + Domains UI** | Recommend workflow, special-skills UI | `EXECUTABLE_PRODUCT.md`, git `e01409c` |
| 11 | 2026-07-14 | **P10 User guide / book / HK** | Deep EN+HK guides, book creator | `book_creator.md`, `book/user_guide/`, git docs commits |
| 12 | 2026-07-15 → 07-16 | **P11 Ops polish + auth/session** | start/stop scripts, help panel, cookies, dispatch fix | `start_all.ps1`, `help_spec.md`, session 011–012 |

**Git anchors (selected)**

| Commit | Date | Message | Phase link |
|--------|------|---------|------------|
| `08a06ac` | 2026-07-10 | Inital | P0 |
| `3243766` | 2026-07-11 | `repo_compare.md` | P6 |
| `c9a5336` | 2026-07-11 | `improvements.md` | P7 plan |
| `d2ba581` | 2026-07-12 | `improvement_prompt.txt` | P7 SDD prompt |
| `344abfe` | 2026-07-13 | video agent domain scaffolding | P7/P8 |
| `d4a062e` | 2026-07-14 | video migration scoring/docs | P8 |
| `e01409c` | 2026-07-14 | domain catalog + recommend tools | P9 |
| `872d915` … | 2026-07-14 | user guide comprehensive | P10 |
| `707d61b` | 2026-07-16 | full platform stack feat | umbrella snapshot |

---

## 2. Phase P0 — Starter / bootstrap / dual harness

### 2.1 Canonical prompts

| ID | Trigger (prompt or human action) | Agent / actor action | Primary deliverables | Verify / acceptance | References |
|----|----------------------------------|----------------------|----------------------|---------------------|------------|
| P0-A01 | *“Implement starter.md in the current repository… Create all required files… Then run: `npm run bootstrap`”* (template in starter) | Self-bootstrap Trae/Grok harness + scripts + docs | `package.json`, `scripts/*.mjs`, `rules/`, `docs/`, `.trae/`, `.grok/` | `npm run bootstrap`, `npm run doctor` | `starter.md` L66–78; `docs/installation.md` |
| P0-A02 | *“Create a new project named … based on starter.md”* | Create-new-project mode (alt path; not always used) | New project tree from contract | Bootstrap validation | `starter.md` L16–57 |
| P0-A03 | *“Migrate Trae project to Grok Build (dual harness)”* | Plan + execute dual harness wire | `npm run sync`, `npm run grok:wire`, asset registry | Trae still works; Grok discovers skills | Session segment 000; `migrate_to_grok_build.md`; `AGENTS.md` |
| P0-A04 | *“Wire skills/plugins/memory/MCP; status report”* | Wire ECC/library assets carefully; report usable set | `.grok/asset-registry.json`, MCP configs | User asks “use all?” → selective wire | Segment 000 user messages; `mcp-configs/` |
| P0-A05 | *“execute grok_investigate_now”* | Investigate structure.md compliance vs implementation | `grok_investigation_report.md`, scorecard gaps | Evidence for mark-100 plan | `grok_investigate_now.md`, `grok_investigation_report.md` |
| P0-A06 | Human / agent: `npm run sources:download` + audit | Download upstream refs into `external/sources/` | `sources/source-lock.json`, `docs/source-audit.md` | `npm run sources:audit` | `sources/README.md`, `docs/source-audit.md` |
| P0-A07 | Business layer expansion (changelog 2.1.0) | Add OS schemas, governance, evals, evolution scaffolding | `business/**`, `npm run business:*` | `npm run business:validate` | `docs/changelog.md` §2.1.0 |

### 2.2 Key bootstrap commands (still used)

| Action | Command | Reference |
|--------|---------|-----------|
| Full bootstrap | `npm run bootstrap` | `docs/installation.md` |
| Dual harness regenerate | `npm run sync` | `AGENTS.md`, `docs/sync.md` |
| Grok asset wire | `npm run grok:wire` | `AGENTS.md` |
| Root tests | `npm test` | `status.md` |
| Business gates | `npm run business:validate` / `governance` / `security` / `evolution:check` / `eval` | `docs/installation.md`, `mark_100_verification.md` |

---

## 3. Phase P1 — Structure SDD (business OS model)

**Meta-prompt pattern:** For each of **17** structure folders under `planning/structure/0x_*/`: write `requirements.md` → `design.md` → `tasks.md` → implement → mark tasks `[x]`.

| ID | Structure component | Trigger / intent | Implementation anchors | Status ref |
|----|---------------------|------------------|------------------------|------------|
| P1-A01 | 01 System charter & design priorities | Safety→…→Autonomy lattice; invariants | `structure.md`, rules, charter checklist | `planning/structure/IMPLEMENTATION_STATUS.md` |
| P1-A02 | 02 Business artifact repository | `business/` tree + validate/security scripts | `business/schemas/`, `scripts/business/` | same |
| P1-A03 | 03 Intake & risk router | Auth run start, `risk_tier` | runtime start path | same |
| P1-A04 | 04 Governance risk tiers & cards | Tier 0–5, policies, model cards | `business/governance/` | same |
| P1-A05 | 05 Security controls & tool broker | Allow-list, fail-closed adapters | `backend/app/infrastructure/tools/` | same |
| P1-A06 | 06 Process intelligence layer | Ingest → discovered/conformance/bottlenecks | `business/process-intelligence/`, PI artifacts | same |
| P1-A07 | 07 Knowledge elicitation & DRC | Templates, Decision Requirement Cards | `business/examples/`, validators | same |
| P1-A08 | 08 Hybrid memory system | Scopes, lessons, rejection→lesson | memory APIs + runtime | same |
| P1-A09 | 09 Tiered hybrid retrieval | Tier-0 provenance + Tier-1 multi-hop lite | knowledge/retrieval | same + `test_retrieval` |
| P1-A10 | 10 Workflow DNA definition | Schema + production DNA validators | `business/schemas/*dna*`, `structure_validators.py` | same |
| P1-A11 | 11 Bounded workflow execution | Runtime graph, gates, E1 path | `backend/app/runtime.py` | same |
| P1-A12 | 12 Human gates & audit logging | Approve/reject + audit | approvals + audit routes | same |
| P1-A13 | 13 Evaluation harness & corpus | ≥20 golden; no auto-promote | `business/evals/` | same |
| P1-A14 | 14 Evolution sandbox engine | Propose→eval→canary→rollback | `business/evolution/`, evolution APIs | same |
| P1-A15 | 15 Agent roster & control roles | Seed agents + role map | runtime seed agents | same |
| P1-A16 | 16 Human–AI interaction rules | FE Improve / archive surfaces | FE improve panels | same |
| P1-A17 | 17 Phased rollout & operator path | E1 checklist + verification pack | `reviews/e1_operator_checklist.md` | same |

| Close-out action | Result | References |
|------------------|--------|------------|
| Gap analysis | **100/100** structure tasks implemented | `planning/gap_analysis_for_structure.md` |
| Task count | **194** tasks, all `[x]` | `planning/structure/IMPLEMENTATION_STATUS.md` |
| Production DNA safety | `_assert_production_dna_safe` on activate | `structure_validators.py`, `test_structure_sdd_validators` |

---

## 4. Phase P2 — Backend SDD (24 components)

**Meta-prompt pattern:** Decompose backend into ordered charter → scaffold → … → testing. Each folder: requirements → design → tasks with **Deliverable (code paths)**. Traceability: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`.

| ID | BE area | Typical agent actions | Primary code | Key tests / docs |
|----|---------|----------------------|--------------|------------------|
| P2-A01 | BE-01 Platform charter | Encode invariants, API-first boundary | `main.py`, `runtime.py`, `router.py` | `backend.md`, `structure.md` |
| P2-A02 | BE-02 Stack scaffold | FastAPI layers, config, CORS | `core/config.py`, `api/` | `backend/README.md` |
| P2-A03 | BE-03 Persistence | Postgres `runtime_state` JSONB + JSON fallback | `infrastructure/database/*`, RuntimeStore | `test_postgres_restart.py`, `docs/postgres-runbook.md` |
| P2-A04 | BE-04 API envelope | Errors, pagination, logging | `api/errors.py`, `core/errors.py` | OpenAPI |
| P2-A05 | BE-05 AuthN | Login, tokens, password hash PBKDF2 | `routes/auth.py`, `runtime.issue_token` | seed users in `runtime.py` |
| P2-A06 | BE-06 AuthZ / RBAC | Permission matrix | `core/permissions.py`, dependencies | `test_scorecard_controls.py` |
| P2-A07 | BE-07 Users / orgs / tenancy | Multi-user seed, invitations | `routes/users.py`, `organizations.py` | seed emails `*@example.com` |
| P2-A08 | BE-08 Agent registry | CRUD agents, scopes, tools | `routes/agents.py` | E1 create agent |
| P2-A09 | BE-09 Tools / adapters | Local adapters + `tool_effects` | `infrastructure/tools/adapters.py` | `test_real_execution.py` |
| P2-A10 | BE-10 Workflow definition | DNA-ish workflow versions | `routes/workflows.py` | flagship `wf_customer_onboarding_v12` |
| P2-A11 | BE-11 Run engine | queue → **dispatch** → execute → gates | `workflow_runs.py`, `_execute_run` | E1 + dispatch API |
| P2-A12 | BE-12 Governance | Risk tier policy engine | `domain/governance/` | business governance scripts |
| P2-A13 | BE-13 Approvals | decide/approve/reject/reassign | `routes/approvals.py` | FE `ApprovalDecisionPanel` |
| P2-A14 | BE-14 Audit | Append-only style logs | `routes/audit_logs.py` | E1 audit asserts |
| P2-A15 | BE-15 Knowledge | Chunk + retrieve | knowledge routes + retrieval | Tier-0/1 tests |
| P2-A16 | BE-16 Memory | Scoped memory items | memory routes | E1 memory asserts |
| P2-A17 | BE-17 Evaluations | Eval runs, block_on_fail | evaluations routes | `business:eval` |
| P2-A18 | BE-18 Process intelligence | Summary + artifacts | processes routes | `test_p3_pi_evolution` |
| P2-A19 | BE-19 Health / streaming | `/health`, `/health/ready`, SSE | `routes/health.py`, stream | ready = postgres |
| P2-A20 | BE-20 Evolution APIs | Sandbox, canary, archive | `routes/evolution.py` | canary status tests |
| P2-A21 | BE-21 Self-improvement | Reflect, lessons, loops, skill sandbox | `routes/improvement.py`, `loops.py` | Improve pipeline |
| P2-A22 | BE-22 Production DNA safety | Validators on activate | `structure_validators.py` | negative fixtures |
| P2-A23 | BE-23 Security hardening | Rate limit, secure defaults | `rate_limit.py`, security | hardening tests |
| P2-A24 | BE-24 Testing / operator path | Unit + e2e E1 | `app/tests/**` | `test_e1_operator_path.py` |

### 4.1 Flagship workflow construction (ops seed)

| ID | Trigger | Action | Deliverable | Verify |
|----|---------|--------|-------------|--------|
| P2-F01 | Product bar E1 / W1 real execution | Seed Customer Onboarding DNA-like steps with tools | Workflow id **`wf_customer_onboarding_v12`**, steps: `verify_contract` → `create_customer_record` → `activate_billing` → `send_welcome_packet` → `audit_and_close` | `GET /workflows/wf_customer_onboarding_v12` |
| P2-F02 | Human gate policy | Stop on approval-required steps; `waiting_for_approval` | Approval records + `approval_request_id` on run | E1 loop with `decide_approval` |
| P2-F03 | Real adapters goal | Wire local adapters not fake success-only | `crm`, `billing_system`, `email`, `audit_log_writer`, `contract_parser`, `policy_retriever` | `test_real_execution.py` |
| P2-F04 | Queue model | `start` → status `queued`; **must** `POST /workflow-runs/dispatch` | `dispatch_queued_runs` | Live 2026-07-16 API probe: dispatch then 2× approve → `completed` |

**Seed credentials (local only)**

| Email | Password | Role | Ref |
|-------|----------|------|-----|
| `admin@example.com` | `admin-password` | admin | `runtime.py` seed |
| `reviewer@example.com` | `reviewer-password` | reviewer | same |
| `operator@example.com` | `operator-password` | operator | same |
| `owner@example.com` | `owner-password` | owner | same |

---

## 5. Phase P3 — Frontend SDD (20 components)

**Meta-prompt pattern:** FE charter → Next scaffold → design tokens → shell → auth → … → security/ops. Traceability: `planning/frontend/TASK_TO_CODE_TRACEABILITY.md`.

| ID | FE area | Trigger / intent | Primary deliverables | Refs |
|----|---------|------------------|----------------------|------|
| P3-A01 | FE-01 Charter | Ops console principles | `frontend.md`, FE README | planning/frontend/01_* |
| P3-A02 | FE-02 Next scaffold | App Router, pnpm, vitest, playwright | `frontend/package.json`, `src/app` | 02_* |
| P3-A03 | FE-03 Design system | Tokens, status badges, UI kit | `src/design/*`, `components/ui` | 03_* |
| P3-A04 | FE-04 App shell / IA | Sidebar, header, routes | `app-shell`, `paths.ts` | 04_* |
| P3-A05 | FE-05 Auth UI | Login, accept-invite, session | `login/page.tsx`, BFF cookies | 05_* |
| P3-A06 | FE-06 Permission-aware UI | Role-gated nav | `lib/auth/permissions.ts` | 06_* |
| P3-A07 | FE-07 OpenAPI client | Typed client + live data | `lib/api/client.ts`, `openapi.d.ts` | 07_* |
| P3-A08 | FE-08 Dashboard | Metrics + shortcuts | `/app` | 08_* |
| P3-A09 | FE-09 Agents & tools UI | Lists + create forms | `/app/agents`, tools | 09_* |
| P3-A10 | FE-10 Workflows UI | Detail + **Run now** | `RunWorkflowButton` | 10_* |
| P3-A11 | FE-11 Run realtime UI | Console + events | `WorkflowRunConsole` | 11_* |
| P3-A12 | FE-12 Approvals UI | Queue + decision panel | `ApprovalDecisionPanel` | 12_* |
| P3-A13 | FE-13 Knowledge/memory UI | Browse surfaces | routes | 13_* |
| P3-A14 | FE-14 Evals/processes UI | Lists | routes | 14_* |
| P3-A15 | FE-15 Audit UI | Audit log list | `/app/audit-logs` | 15_* |
| P3-A16 | FE-16 Settings/users | Org settings | `/app/settings` | 16_* |
| P3-A17 | FE-17 Evolution archive UI | Archive panel | `EvolutionArchivePanel` | 17_* |
| P3-A18 | FE-18 Improve pipeline UI | Reflect→Propose→Evaluate→Canary | `ImproveRunButton` | 18_* |
| P3-A19 | FE-19 A11y / empty / error | Loading/empty states | shared components | 19_* |
| P3-A20 | FE-20 Ops profile | `DEMO_MODE=false`, security | `env.ts`, middleware | 20_* |

### 5.1 Frontend runtime construction actions (product slice)

| ID | Trigger | Action | Deliverable | Verify |
|----|---------|--------|-------------|--------|
| P3-F01 | E7 product forms | Real create forms + backend error formatting | Zod/RHF forms, `formatMutationError` | FE unit tests historically 24/24 |
| P3-F02 | Run now UX | Build payload with auto `case_id` | `workflow-run-payload.ts` | Run now on onboarding |
| P3-F03 | Auth BFF | `POST /api/auth/login` sets **httpOnly** cookies | `gso_access_token` + `frontend_session` | middleware requires both for `/app` |
| P3-F04 | Demo mode | `NEXT_PUBLIC_DEMO_MODE` | demo vs live ops | env at **build** time for `next start` |

---

## 6. Phase P4 — Mark 100 / E1 operator path / self-improvement

### 6.1 Planning prompt

| ID | Trigger | Action | Deliverables | Refs |
|----|---------|--------|--------------|------|
| P4-A01 | *“Execute plan_to_mark_100”* / close product bar | Drive workstreams W1–W8 against E1–E8 exit criteria | `plan_to_mark_100.md` updates, score 100 | plan file + `mark_100_verification.md` |
| P4-A02 | User: *“do all sequential next steps”* | E1 → Playwright → Improve UI → commit/PR | SI backlog closed | Session segment 001 |
| P4-A03 | Goal: *“fix all errors”* | Lint zero; test green; memory scope fix | Flagship agents get `organization_memory` | segment 001 errors/fixes |

### 6.2 Exit criteria map (what “100” meant)

| Criterion | Meaning | Proof action | Reference |
|-----------|---------|--------------|-----------|
| **E1** | login → lists → create → **run** → gate → approve → complete → improve | Run `test_e1_operator_path` + checklist | `reviews/e1_operator_checklist.md` |
| **E2** | Controls survive restart (Postgres) | `test_postgres_restart` | mark_100_verification |
| **E3** | Real tool adapters / side effects | `test_real_execution` | adapters.py |
| **E4** | PI disk artifacts | `test_p3_pi_evolution` | business/process-intelligence |
| **E5** | Evolution loop non-mutating | corpus eval + canary tests | evolution routes |
| **E6** | ≥20 golden + suites; no auto-promote | `npm run business:eval` | 20 golden JSON |
| **E7** | FE real forms + request id errors | FE tests | forms + live-data |
| **E8** | Postgres primary | health ready `database: postgres` | RuntimeStore |

### 6.3 E1 construction sequence (how the golden path was built)

| Step | Prompt / action | Technical action | API / UI | Ref |
|------|-----------------|------------------|----------|-----|
| 1 | Ensure ready | Health check | `GET /api/v1/health/ready` | e2e test L26–30 |
| 2 | Login | Password login | `POST /api/v1/auth/login` | e2e L32–39 |
| 3 | List control plane | Live lists | `GET workflows/agents/approvals` | e2e L41–44 |
| 4 | Create agent | POST agent with tool + memory scopes | `POST /api/v1/agents` | e2e L46–60 |
| 5 | Run flagship | Start with `case_id` | `POST /workflows/wf_customer_onboarding_v12/run` | e2e L62–68 |
| 6 | Dispatch worker | **Critical:** pick up queue | `runtime.dispatch_queued_runs` / `POST /workflow-runs/dispatch` | e2e L70–71; routes |
| 7 | Human gates | Approve until not waiting | `decide_approval` / FE Approvals | e2e L74–79 |
| 8 | Assert complete | `activate_billing` completed | run status `completed` | e2e L81–83 |
| 9 | Improve | Reflect → propose → evaluate → canary | improvement + evolution APIs | e2e L85–95 |

**UI equivalent (operator):**

1. Open `http://127.0.0.1:3000/login` (same host always).  
2. Workflows → `wf_customer_onboarding_v12` → **Run now**.  
3. If build predates auto-dispatch fix: call dispatch API or rebuild FE (see P11).  
4. Approvals → Approve (typically **2** gates).  
5. Workflow run detail → Improve pipeline.

---

## 7. Phase P5 — Grok / Trae harness hardening

| ID | User message (from session history) | Action | Deliverables | Refs |
|----|-------------------------------------|--------|--------------|------|
| P5-A01 | Trae→Grok reuse; migrate plan then execute | Dual harness plan + wire | `.grok/`, `.trae/`, sync scripts | segment 000 |
| P5-A02 | skills list; ECC installed? | Inventory skills; answer what is usable | skill list report | segment 000 |
| P5-A03 | wire assets + status report | Selective wire (not blind “use all”) | asset registry | segment 000 |
| P5-A04 | execute `grok_investigate_now` | Structure compliance investigation | investigation report | `grok_investigation_report.md` |
| P5-A05 | Continuous `npm run sync` discipline | Keep harness generated files regenerated | AGENTS.md rule | `AGENTS.md` |

---

## 8. Phase P6 — Strategy: compare, adopt, improve plan

### 8.1 User intent (explicit concern)

> *After applying improvements, will generic-swarm-ops benefit other projects (not only va-agent-swarm)? Or will video-specific logic pollute the core?*

Answer embedded in plan: **host benefits many domains; video stays under `business/video/` only (N1).**  
Reference: `improvements.md` §2.4; `repo_compare.md`; `adoption.md`.

### 8.2 Construction actions

| ID | Trigger | Action | Deliverables | Verify |
|----|---------|--------|--------------|--------|
| P6-A01 | Compare generic vs va | Deep repo compare write-up | `repo_compare.md` (+ HK + YouTube script) | git `3243766`, `2ad246b` |
| P6-A02 | Study adoption strategy | Formalize N1/N2/N3, L0–L2 | `adoption.md` v2.3→v2.4, `adoption_plan.md` v3.2 | handoff.md |
| P6-A03 | Write execution plan | Wave 0–5 roadmap with file-level tasks | **`improvements.md` v1.0** | git `c9a5336` |
| P6-A04 | Write agent SDD prompt | Mandatory Requirements→Design→Tasks protocol | **`improvement_prompt.txt`** | git `d2ba581` |
| P6-A05 | Chain runner prompt | Auto-advance waves 0→5 with gates | **`run_all_improvement.md`** | chain-run-report |
| P6-A06 | HK localization of strategy | Full Traditional Chinese + scripts | `*_hk.md`, `*.script.txt` | various docs commits |

### 8.3 Canonical agent prompt (Wave execution)

**Source:** `improvement_prompt.txt` + `run_all_improvement.md`

```text
Execute Wave <N> of improvements.md using the full SDD flow.
Output all documents to planning/improvement/wave-N/.
Begin with Phase 1 (Requirements).

Then: Design → Tasks → Implement → Verify (inventory + pytest) → completion-report.md
Gate: only advance if verify PASSES. Protect E1. Enforce N1/N2/N3.
```

**Cross-refs required in every wave:** `improvements.md`, `adoption.md` (N1/N2/N3), `repo_compare.md`.

---

## 9. Phase P7 — Improvements Waves 0–5 (Domain Pack + ALC + N3)

**Index:** `planning/improvement/README.md`  
**Chain result:** ALL WAVES PASS — `planning/improvement/chain-run-report.md`  
**Inventory end-state:** `INVENTORY PASS count=114 n3=complete`

### 9.1 Wave table (prompt → action → proof)

| ID | Wave | User / agent trigger | Core implementation actions | Structure deliverables | Backend deliverables | Frontend deliverables | Verify (historical) | SDD folder |
|----|------|----------------------|-----------------------------|------------------------|----------------------|-----------------------|---------------------|------------|
| W0-A01 | **0 Foundations** | *Execute Wave 0…* / start chain | L0 catalog 114 dirs; schemas; inventory script; register dry-run | `business/video/` skeleton, ROSTER/MAP | domain pack schema tests | minimal | inventory 114; 8 domain-pack tests | `planning/improvement/wave-0/` |
| W1-A01 | **1 ALC + Domain SDK** | *Execute Wave 1…* | ALC `agent_id` on lessons; register API; isolation; genome sandbox | pack contracts | `POST /domains/register`, ALC gates | DomainPackPanel | 12 ALC tests | `wave-1/` |
| W2-A01 | **2 Spine E2E** | *Execute Wave 2…* | Spine + viral-hook DNA; video_* stub tools; standby pool | DNA files under `business/video/workflows/` | spine runner + stubs | domains shell | `test_video_spine_e2e` 3 passed | `wave-2/` |
| W3-A01 | **3 Coevolution** | *Finish Wave 3…* (segment 006) | multi-gen coevolution; lesson utility; LQR goldens | video goldens | coevolution routes | LessonUtilityPanel | 7 coevolution tests | `wave-3/` |
| W4-A01 | **4 Multi-pack** | *Execute Wave 4…* | third pack `example_education`; load; red-team isolation | multipack fixtures | isolation helpers | multi-pack summary UI | 8 multipack tests | `wave-4/` |
| W5-A01 | **5 N3 complete** | *Execute Wave 5…* / `run_all_improvement` | full roster wiring; process_coverage va_only=0; CI inventory | retention policy | `GET /domains/video/n3-status` | VideoN3RosterPanel | 9 N3 tests; n3=complete; unit ~104 | `wave-5/` |
| WX-A01 | **Chain re-verify** | *Execute `run_all_improvement.md`* | Prefer re-verify; no code if green | — | — | — | all waves PASS | `chain-run-report.md` |

### 9.2 Wave 0 detail (example of SDD → code)

| Step | Action | Output | Ref |
|------|--------|--------|-----|
| 1 | Write requirements (Structure/Backend/Frontend) | `wave-0/requirements.md` | improvement_prompt |
| 2 | Write design | `wave-0/design.md` | same |
| 3 | Write tasks with paths | `wave-0/tasks.md` | same |
| 4 | Create 114 agent dirs + roster | `business/video/agents/*` | inventory |
| 5 | Schemas for domain packs | business schemas + backend validators | domain pack tests |
| 6 | Inventory script | `scripts/business/inventory_check.py` | CI later `n3-inventory.yml` |
| 7 | Completion report with command evidence | `wave-0/completion-report.md` | wave folder |

### 9.3 Non-negotiables enforced in every wave

| ID | Rule | Enforcement actions | Ref |
|----|------|---------------------|-----|
| N1 | Video logic only in pack; ALC mandatory | namespace `video.*`; pack paths; ALC tests | `adoption.md` |
| N2 | Universal host for many MMA packs | second/third example packs; isolation tests | wave-1/4 |
| N3 | All 114 agents retained forever | inventory CI fails if missing | wave-5, inventory_check |

---

## 10. Phase P8 — VA migration, agent SPECs, special skills

### 10.1 Migration construction

| ID | Trigger | Action | Deliverables | Verify | Refs |
|----|---------|--------|--------------|--------|------|
| P8-A01 | *execute planning/migration/tasks.md* | Migrate va knowledge into pack | `business/video/corpus/` **325** files | `check_video_corpus_standalone.py` | `MIGRATION_COMPLETE.md` |
| P8-A02 | Standalone knowledge goal | Expand all 114 SPEC.md self-contained | `agents/*/SPEC.md` (≥8KB framing; later enriched 10–195KB) | standalone tests | handoff.md |
| P8-A03 | Honest scoring (user skepticism: *too good to be true?*) | Revert false fleet-100; honest marks | `planning/migration/agent_impl_v1_mark.md` (mean ~93.8; true 100 count=0) | score file | handoff, segment 007/009 |
| P8-A04 | *agent implement order* | Spine-first order list for L2 activation | `planning/migration/agent_implement_order_list.md` | order 1=orchestrator… | same file |
| P8-A05 | Process index integrity | Map processes; zero va-only rows | `PROCESSES.md`, `process_coverage.json` | va_only_count=0 | MIGRATION_COMPLETE |
| P8-A06 | DNA set | Import/create 14 DNA workflows | `business/video/workflows/*.dna.json` | inventory/DNA tests | README improvement |

### 10.2 Special skills construction

| ID | Trigger | Action | Deliverables | Refs |
|----|---------|--------|--------------|------|
| P8-B01 | `generate_special_skills.md` | Generate 17 SDD plans from va study | `planning/special/*.md` | `planning/special/README.md` |
| P8-B02 | Implement + score script | Host MVP integrations | `business/video/special_skills/<id>/{integration.json,SKILL.md}` | `implement_and_score_special_skills.py` |
| P8-B03 | Score reporting | Mean ~92.9; not all full 100 | `special_skill_impl_score.md` | planning/special + root pointer |
| P8-B04 | API exposure | List special skills | `GET /api/v1/domains/video/special-skills` | tests + FE panel |

### 10.3 Archetype recommend construction

| ID | Trigger | Action | Deliverables | Refs |
|----|---------|--------|--------------|------|
| P8-C01 | Product need: brief → DNA | Deterministic keyword/scale selector | `archetype_registry.json`, `archetype_selector.py` | handoff 2026-07-13 |
| P8-C02 | API + CLI | Recommend endpoint + script | `POST .../recommend-workflow`, `recommend_video_workflow.py` | EXECUTABLE_PRODUCT |
| P8-C03 | Policy | HiTL confirm default; no auto_start | response fields `hitl_confirm_required`, `auto_start_allowed` | live API 2026-07-16 |

---

## 11. Phase P9 — Executable product slice (operator-facing)

| ID | Trigger | Action | Deliverables | Verify | Refs |
|----|---------|--------|--------------|--------|------|
| P9-A01 | *executable product* / write status | Document what is truly runnable vs residual | `EXECUTABLE_PRODUCT.md` | health + E1 + viral-hook tests | file itself |
| P9-A02 | One-command product check | Aggregate gate script | `scripts/business/check_executable_product.py` | script exit 0 | EXECUTABLE_PRODUCT |
| P9-A03 | Domains UI product slice | FE panels for recommend + special skills | `RecommendWorkflowPanel`, `SpecialSkillsPanel` | FE unit product-slice tests | git `e01409c`, handoff |
| P9-A04 | Proven path 1 | E1 customer onboarding | e2e test + checklist | PASS | reviews/e1_* |
| P9-A05 | Proven path 2 | Video viral-hook spine with stubs + gate | `test_video_spine_e2e` | PASS | EXECUTABLE_PRODUCT |

**Explicit non-claims (built as docs, not product lies)**

| Residual | Why listed | Ref |
|----------|------------|-----|
| Live Sora/Veo/Runway | Stubs only by design | EXECUTABLE_PRODUCT, MIGRATION_COMPLETE |
| All A–J `production_ready` deep DNA | Many thin_stub_n3 | recommend depths |
| Full Discover gallery FE | Not built | residuals list |
| Fleet true-100 agent scores | Honest marks <100 | agent_impl_v1_mark |

---

## 12. Phase P10 — Documentation / book / user guide

| ID | Trigger | Action | Deliverables | Refs |
|----|---------|--------|--------------|------|
| P10-A01 | book-creator skill / create_user_guide | Deep EN chapters (Opus-grade bar ≥480 lines) | `book/user_guide/chapters/*` | `book_creator.md` |
| P10-A02 | HK localization | Parallel Traditional Chinese materials | `*_hk.md`, user guide HK | git docs commits 2026-07-14 |
| P10-A03 | Design-phase monographs | Structure/backend/frontend books + SVG | `book/design_phase/` | book_creator |
| P10-A04 | FEAT-001…005 tracking | Mark user guide sections complete | task chore commits | git log 2026-07-14 |
| P10-A05 | YouTube / spoken scripts | Continuous narrative scripts from markdown | `*.script.txt` | repo_compare_hk, adoption scripts |

---

## 13. Phase P11 — Recent product ops sessions (run / auth / help / polish)

**Session source:** Grok compaction segments **011–012** (+ current chat).  
**Host:** always `C:\Project\generic-swarm-ops`.

| ID | User prompt / action (approx.) | Agent action | Deliverables / fix | Why it mattered | Refs |
|----|--------------------------------|--------------|--------------------|-----------------|------|
| P11-A01 | *start app* / *start again* | Run backend uvicorn + FE next | Processes on :8000 / :3000 | Local demo | segment 011 |
| P11-A02 | *start/stop scripts* | Write production-friendly scripts | `start_all.ps1`, `stop_all.ps1`, `.run/servers.json`, logs | Avoid manual two terminals; prebuild kills “Rendering…” | scripts at repo root |
| P11-A03 | *sources download / security* | Run/diagnose source download + security scripts | source lock / security reports | Harness hygiene | segment 011 |
| P11-A04 | FE login failures / *stupid GET* | Fix login to **POST** BFF + credentials | `api/auth/login` route, AuthForm | GET cannot set session correctly | segment 011 |
| P11-A05 | CORS * + credentials bug | Align CORS with credentialed browser calls | backend CORS config | Login/proxy failures | segment 011 |
| P11-A06 | *help_spec* / route docs | Independent resizable help document panel | help panel + `public/docs` route mapping | In-app docs | `help_spec.md` |
| P11-A07 | SPEC click / orchestrator / right panel | Agent SPEC view + resizable right panel | FE domain panels | Operator readability | segment 011 |
| P11-A08 | *why login every time? session cookies?* | Diagnose dual cookies; Secure on HTTP bug | `resolveCookieSecure`, login/logout/accept-invite | Session persistence | segment 011–012; cookies helpers |
| P11-A09 | Cookie host mismatch | Document use **only** `127.0.0.1` or only `localhost` | operator guidance | Cookies are host-bound | session notes |
| P11-A10 | *how to start this app* | Document `.\start_all.ps1` + seed login | user guidance | onboarding | current chat |
| P11-A11 | *lots of things but does not work* | Honest working-slice vs inventory analysis | product honesty answer | Expectation reset | current chat |
| P11-A12 | *how to run wf_customer_onboarding_v12 with gates?* | Document UI + API; **discover missing auto-dispatch** | guide + **code fix** `dispatchWorkflowRuns` after Run now | Run stayed `queued` forever in UI | current chat + `run-workflow-button.tsx` |
| P11-A13 | *write complete construction report…* | This document | `project_construction_action_list.md` | Audit trail | this file |

### 13.1 start_all construction semantics

| Mode | Command | Behavior | Ref |
|------|---------|----------|-----|
| Production (default) | `.\start_all.ps1` | `pnpm build` then `next start` + uvicorn | `start_all.ps1` |
| Skip rebuild | `.\start_all.ps1 -SkipBuild` | Reuse `.next` | same |
| Dev HMR | `.\start_all.ps1 -Dev` | `next dev` + uvicorn `--reload` | same |
| Demo | `.\start_all.ps1 -DemoMode` | `NEXT_PUBLIC_DEMO_MODE=true` at build | same |
| Stop | `.\stop_all.ps1` | Kill PID tree + free 3000/8000 | `stop_all.ps1` |

### 13.2 Auth cookie construction

| Cookie | Purpose | Flags | Consumer |
|--------|---------|-------|----------|
| `gso_access_token` | Bearer equivalent httpOnly | maxAge 12h; Secure only if HTTPS (or override) | BFF proxy + middleware |
| `frontend_session` | Non-secret session display JSON | SameSite=Lax | middleware + shell |

**Failure modes fixed/documented:** Secure cookie on plain HTTP; `localhost` vs `127.0.0.1`; middleware requiring both cookies.

### 13.3 Dispatch gap (important construction lesson)

| Observation | Cause | Fix | Status |
|-------------|-------|-----|--------|
| UI Run now left runs `queued` | `startWorkflowRun` only queues; worker is **manual dispatch** | FE calls `POST /workflow-runs/dispatch` after start | Fixed in `frontend/src/lib/api/client.ts` + `run-workflow-button.tsx` (rebuild FE to load) |
| E1 test always worked | Test explicitly calls `dispatch_queued_runs` | — | `test_e1_operator_path.py` L71 |
| Approvals | Need `decision` field on `/decision` | FE already sends `{decision, reason}` | `client.ts` `decideApproval` |

---

## 14. Cross-cutting “how we build” recipes (reusable prompts)

| Recipe ID | Paste-ready prompt | Expected outputs |
|-----------|--------------------|------------------|
| R-SDD-WAVE | See §8.3 Wave prompt | `planning/improvement/wave-N/{requirements,design,tasks,completion-report}.md` + code + tests |
| R-SDD-STRUCTURE | *For structure component NN: write requirements, design, tasks to 100 quality; implement; update gap analysis* | `planning/structure/NN_*/` + code wiring |
| R-SDD-BACKEND | *Execute BE-NN tasks.md with deliverable paths; tests green* | BE routes/services/tests |
| R-SDD-FRONTEND | *Execute FE-NN; live ops; DEMO_MODE false* | FE pages/components/tests |
| R-MARK100 | *Close plan_to_mark_100 E1–E8 with evidence logs* | `mark_100_verification.md`, `reviews/mark100-logs/` |
| R-E1 | *Run E1 operator path and fix until PASS* | e2e green + checklist |
| R-INVENTORY | *Keep N3: inventory_check must PASS 114 n3=complete* | CI + local script |
| R-MIGRATION | *Execute migration_plan; standalone corpus; no va primary dependency* | `MIGRATION_COMPLETE.md` |
| R-HONESTY | *If scores look too perfect, re-score honestly* | agent_impl_v1_mark reopen |
| R-PRODUCT-SLICE | *Add one operator-visible path only (recommend / special skills / run)* | FE+API+tests; update EXECUTABLE_PRODUCT |
| R-OPS | *Make it startable: scripts, login, cookies, dispatch* | start_all, session fix, Run now fix |

---

## 15. Architecture construction map (what the “app” is)

```text
Operator (browser) / API client / unittest
        │
        ▼
Next.js ops console (frontend/)  ── BFF cookies ──► FastAPI (backend/app/main.py)
        │                                              │
        │                                              ▼
        │                                         Runtime (runtime.py)
        │                                         - auth/RBAC
        │                                         - workflows / runs / dispatch
        │                                         - tools adapters
        │                                         - approvals / audit / memory
        │                                         - evolution / improvement
        │                                              │
        │                         ┌────────────────────┼────────────────────┐
        │                         ▼                    ▼                    ▼
        │                  ops seed DNA          Domain Packs          Postgres
        │              (onboarding etc.)      business/<domain>/     runtime_state
        │                                         video/ (114 agents,
        │                                         14 DNA, special_skills,
        │                                         corpus 325)
        ▼
public/docs + help panel (route-mapped markdown)
```

| Layer | Built by phases | Primary refs |
|-------|-----------------|--------------|
| Harness | P0, P5 | starter, sync, .grok/.trae |
| Structure OS model | P1 | planning/structure, business/* |
| Control plane API | P2, P4 | backend/app |
| Ops console | P3, P4, P9, P11 | frontend/src |
| Video pack | P6–P8 | business/video |
| Docs / books | P10 | book/, docs/ |
| Local ops | P11 | start_all, cookies, help |

---

## 16. Verification command matrix (construction gates)

| Gate | Command | Expected | Used in |
|------|---------|----------|---------|
| Root unit | `npm test` | pass | mark 100 |
| Business validate | `npm run business:validate` | failures: none | mark 100 |
| Business eval | `npm run business:eval` | ≥20 golden + suites | E6 |
| Inventory N3 | `python scripts/business/inventory_check.py` | `count=114 n3=complete` | Waves 0–5 |
| Corpus standalone | `python scripts/business/check_video_corpus_standalone.py` | STANDALONE PASS | migration |
| Backend unit | `cd backend && python -m pytest app/tests/unit -q` | green (count grew over time) | waves |
| E1 e2e | `python -m unittest app.tests.e2e.test_e1_operator_path -v` | PASS | product bar |
| Video spine | `pytest app/tests/unit/test_video_spine_e2e.py -q` | PASS | Wave 2 |
| FE typecheck | `cd frontend && pnpm typecheck` | pass | FE close |
| FE unit | `cd frontend && pnpm test` | pass | FE close |
| Health | `GET http://127.0.0.1:8000/api/v1/health/ready` | database postgres or json-file | ops |
| Executable aggregate | `python scripts/business/check_executable_product.py` | pass | P9 |

---

## 17. Session history index (chat construction evidence)

| Segment | Keywords / themes | Construction impact |
|---------|-------------------|---------------------|
| 000 | Trae→Grok, investigate, mark plan | Dual harness + investigation |
| 001 | E1, Playwright, Improve UI, PR, docs refresh | SI close + docs |
| 002–005 | structure_hk, YouTube scripts, adoption_hk | Localization / narrative |
| 006 | genetic→generic rename, Waves 0–5 execute | Domain pack platform |
| 007–010 | migration tasks, honest scores, subagents | VA pack quality |
| 011–012 | start app, auth cookies, help panel, session | Operator usability |
| Current | start guide, honesty, onboarding run guide, **this report** | Product clarity |

Compaction index path (local session):  
`C:\Users\NH24831\.grok\sessions\C%3A%5CProject%5Cgenetic-swarm-ops\019f44a7-ca1d-78e3-b15b-88e5ba69bdec\compaction\INDEX.md`

---

## 18. Master action checklist (chronological, condensed)

| # | Action | Prompt / driver | Result |
|--:|--------|-----------------|--------|
| 1 | Bootstrap starter dual harness | starter.md implement | Trae+Grok repo |
| 2 | Business OS scaffolding | business layer plan | schemas/evals/gov |
| 3 | Structure SDD 01–17 | SDD prompts | 194 tasks done |
| 4 | Backend SDD 01–24 | SDD prompts | FastAPI runtime |
| 5 | Frontend SDD 01–20 | SDD prompts | Next ops console |
| 6 | Postgres RuntimeStore | plan_to_mark_100 W2 | durable state |
| 7 | Real tool adapters | plan_to_mark_100 W1 | E3 pass |
| 8 | E1 path + SI | sequential next / e2e | mark 100 |
| 9 | Grok wire + investigate | migrate/investigate prompts | harness ready |
| 10 | repo_compare + adoption | compare/study prompts | merge model |
| 11 | improvements.md + prompts | write plan | Waves SoT |
| 12 | Wave 0–5 implement | improvement_prompt / run_all | N3 complete |
| 13 | Migrate va corpus+SPECs | migration tasks | standalone pack |
| 14 | Special skills 17 | generate_special_skills | plans + MVP integrations |
| 15 | Recommend workflow | product slice | API+FE+CLI |
| 16 | User guide / books | book_creator | EN+HK deep docs |
| 17 | start_all / stop_all | ops UX | one-command run |
| 18 | Auth cookie Secure fix | re-login complaint | session stickiness |
| 19 | Help panel | help_spec | in-app docs drawer |
| 20 | Auto-dispatch after Run now | onboarding how-to | UI path can complete |
| 21 | Construction report | this user request | this file |

---

## 19. What was *not* built (explicit, to avoid false construction claims)

| Item | Status | References |
|------|--------|------------|
| Live media generation vendors | Not built (stubs) | EXECUTABLE_PRODUCT residuals |
| All 114 agents deep L2 production polish | Catalog/index mostly; spine runnable | adoption L0–L2 model |
| Second control plane (LangGraph/Temporal host) | Forbidden by design | improvements.md merge model |
| Pixel-perfect Discover studio UI from va | Not claimed | residuals |
| Auto-promote production DNA | Blocked by design | E6, evolution rules |
| Treating `genetic-swarm-ops` workspace as SoT | Anti-pattern; real code in generic | handoff, sessions |

---

## 20. Primary reference catalog (complete reading order)

| Order | Document | Why |
|------:|----------|-----|
| 1 | `starter.md` | Original bootstrap contract + example prompts |
| 2 | `structure.md` | Product architecture / bar definition |
| 3 | `plan_to_mark_100.md` | How 100 was defined and closed |
| 4 | `mark_100_verification.md` | Evidence matrix |
| 5 | `status.md` | Living status |
| 6 | `repo_compare.md` | Why merge host+pack |
| 7 | `adoption.md` / `adoption_plan.md` | N1/N2/N3 strategy |
| 8 | `improvements.md` | Wave execution SoT |
| 9 | `improvement_prompt.txt` | SDD agent prompt |
| 10 | `run_all_improvement.md` | Chain prompt |
| 11 | `planning/improvement/**` | Wave SDD + completion |
| 12 | `planning/backend|frontend|structure/**` | Full SDD libraries |
| 13 | `MIGRATION_COMPLETE.md` / `migration_plan.md` | VA import |
| 14 | `EXECUTABLE_PRODUCT.md` | Runnable slice honesty |
| 15 | `memory/handoff.md` | Session continuity map |
| 16 | `docs/changelog.md` | Version narrative |
| 17 | `reviews/e1_operator_checklist.md` | Operator path |
| 18 | `backend/app/tests/e2e/test_e1_operator_path.py` | Automated construction proof |
| 19 | `start_all.ps1` / `stop_all.ps1` | Local product run |
| 20 | This file | Construction action inventory |

---

## 21. Appendix A — Backend BE folder list (construction units)

| # | Folder |
|--:|--------|
| 01 | `planning/backend/01_platform-charter-boundaries-and-principles/` |
| 02 | `planning/backend/02_runtime-stack-and-project-scaffold/` |
| 03 | `planning/backend/03_persistence-control-plane/` |
| 04 | `planning/backend/04_api-contract-envelope-and-errors/` |
| 05 | `planning/backend/05_authentication-and-identity/` |
| 06 | `planning/backend/06_authorization-and-rbac/` |
| 07 | `planning/backend/07_users-organizations-and-tenancy/` |
| 08 | `planning/backend/08_agent-registry/` |
| 09 | `planning/backend/09_tool-registry-adapters-and-broker/` |
| 10 | `planning/backend/10_workflow-definition-and-versioning/` |
| 11 | `planning/backend/11_workflow-run-execution-engine/` |
| 12 | `planning/backend/12_governance-policies-and-risk/` |
| 13 | `planning/backend/13_human-approval-gates/` |
| 14 | `planning/backend/14_audit-logging/` |
| 15 | `planning/backend/15_knowledge-base-and-retrieval/` |
| 16 | `planning/backend/16_memory-system/` |
| 17 | `planning/backend/17_evaluation-system/` |
| 18 | `planning/backend/18_process-intelligence/` |
| 19 | `planning/backend/19_streaming-health-and-observability/` |
| 20 | `planning/backend/20_evolution-sandbox-apis/` |
| 21 | `planning/backend/21_self-improvement-and-loops/` |
| 22 | `planning/backend/22_production-dna-safety/` |
| 23 | `planning/backend/23_security-hardening-and-nfr/` |
| 24 | `planning/backend/24_testing-strategy-and-operator-path/` |

Each contains: `requirements.md`, `design.md`, `tasks.md`.

## 22. Appendix B — Frontend FE folder list

| # | Folder |
|--:|--------|
| 01–20 | `planning/frontend/01_frontend-charter-scope-and-principles/` … `20_security-performance-testing-and-ops-profile/` |

(Full names listed in §5 table.)

## 23. Appendix C — Flagship operator reproduction (post-construction)

| Step | Action | Expected |
|------|--------|----------|
| 1 | `cd C:\Project\generic-swarm-ops` ; `.\start_all.ps1` | BE :8000, FE :3000 |
| 2 | Open `http://127.0.0.1:3000/login` | Login page |
| 3 | `admin@example.com` / `admin-password` | Cookies set; `/app` |
| 4 | Open workflow `wf_customer_onboarding_v12` → Run now | Run created + dispatched (after FE rebuild with fix) |
| 5 | Approvals → Approve (repeat if needed) | Run `completed` |
| 6 | Domains → recommend “15s viral TikTok hook” | DNA `wf_video_arch_a_viral_hook_v1` |
| 7 | Optional API dispatch if queued | `POST /api/v1/workflow-runs/dispatch` |

---

## 24. Document control

| Field | Value |
|-------|-------|
| Title | Project Construction Action List |
| Path | `C:\Project\generic-swarm-ops\project_construction_action_list.md` |
| Audience | Humans reconstructing how the system was built; agents continuing work |
| Completeness | Best-effort synthesis of **repo artifacts + git history + session compaction summaries + live ops probes (2026-07-16)** |
| Not a claim of | Line-by-line reconstruction of every agent tool call across all months |
| Related handoff | `memory/handoff.md` |

---

*End of report.*
