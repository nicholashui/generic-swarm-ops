# -*- coding: utf-8 -*-
"""Sections 2–5 + appendices + masters for book/user_guide."""
from __future__ import annotations

from pathlib import Path

BOOK = Path(__file__).resolve().parents[2] / "book" / "user_guide"
CH = BOOK / "chapters"
CH.mkdir(parents=True, exist_ok=True)


def R() -> str:
    return (
        "> **Residual (honesty):** E1, recommend, viral-hook **stubs**, 17 skills catalog are in bar. "
        "Not claimed: live media vendors, full studio, fleet true-100. `EXECUTABLE_PRODUCT.md`.\n"
    )


def quiz(pairs):
    lines = ["## Knowledge check\n"]
    for i, (q, _) in enumerate(pairs, 1):
        lines.append(f"{i}. {q}")
    lines.append("\n<details>\n<summary>Answer key</summary>\n")
    for i, (_, a) in enumerate(pairs, 1):
        lines.append(f"{i}. {a}")
    lines.append("\n</details>\n")
    return "\n".join(lines)


def nav(prev, nxt):
    lines = ["## Navigation\n"]
    if prev:
        lines.append(f"- Previous: [`{prev}`](./{prev})")
    if nxt:
        lines.append(f"- Next: [`{nxt}`](./{nxt})")
    lines.append("- Guide home: [../user_guide.md](../user_guide.md)")
    return "\n".join(lines) + "\n"


def write(name, content):
    (CH / name).write_text(content.strip() + "\n", encoding="utf-8")
    print("OK", name)


# ---- Section 2 ----

write(
    "02-01-agents-and-tools.md",
    f"""
# 2.1 Agents and tools

| | |
|--|--|
| **Section** | 2 — Intermediate Workflows |
| **Level** | Intermediate |
| **Est. time** | 40–50 minutes |

## Learning objectives

- Inspect and create agents with tool allow-lists
- Explain why tools outside the allow-list fail
- Locate the tools catalog in the UI

## Prerequisites

- Section 1 complete; live login

## Illustration

![Agents DNA tools](../assets/02-01-agents-tools.svg)

*Figure 2.1 — Agent → DNA step → tool adapter*

{R()}

## Concepts

An **agent** is not a free LLM persona. It is a registry record with:

- Identity (`id`, name, status)
- **`allowed_tools[]`** enforced at runtime
- Optional learning/lesson attachments (later chapters)

A **tool** is an adapter under `backend/app/infrastructure/tools/` (examples: crm, billing, email, audit helpers, `video_*` stubs). Successful or attempted calls leave auditable **`tool_effects`**.

DNA **steps** bind `agent` + `tools` + action metadata. If the DNA asks for a tool not on the agent allow-list, execution should fail closed or skip per policy—not silently escalate privilege.

## UI surfaces

| UI | Route | Actions |
|----|-------|---------|
| Agents | `/app/agents` | List, open detail, create (live forms) |
| Tools | `/app/tools` | Browse available tools |

Create forms require **demoMode false**; otherwise you only preview UI.

## Hands-on steps

1. Open **Agents**. Note seeded or empty state.  
2. Create an agent (live mode) with a small allow-list, e.g. audit-related tools only.  
   - Use a clear id such as `lab_agent_02_01`.  
3. Open **Tools** and identify at least three tool names.  
4. Mentally pair: “which tools would onboarding need?” vs “which would video stubs need?”

**Expected:** Agent appears in list; you can articulate allow-list purpose.

## Technical notes

- Frontend create path: `backendApi.createAgent` → `POST /api/v1/agents`  
- Errors should surface actionable messages; copy `request_id` when shown.  
- Video media tools are **stubs** on the executable bar—they prove wiring, not vendor media.

## Real-world use cases

### Use case 1 — Least privilege for finance steps

Billing agent allow-list excludes web browse tools; research agent excludes billing tools.

### Use case 2 — Incident: unexpected tool call

Audit `tool_effects`; if tool not on allow-list, treat as bug or attack attempt.

### Use case 3 — Pack authoring

When adding a video agent, declare tools in agent JSON and DNA steps together.

## Best practices

- Prefer many narrow agents over one omnipotent agent.  
- Review allow-lists in PR diffs.  
- Never “temporarily” allow all tools in shared environments.

## Chapter summary

- Agents are allow-listed executors  
- Tools are audited adapters  
- DNA binds the two with gates later  

{quiz([
    ("What field limits agent tools?", "allowed_tools"),
    ("Where do operators browse tools?", "/app/tools"),
    ("Are video media tools live vendors by default?", "No—stubs on executable bar."),
])}

{nav("01-05-accounts-login-and-session.md", "02-02-first-workflow-run-e1.md")}
""",
)

write(
    "02-02-first-workflow-run-e1.md",
    f"""
# 2.2 First workflow run (E1 path)

| | |
|--|--|
| **Section** | 2 — Intermediate Workflows |
| **Level** | Intermediate |
| **Est. time** | 45–70 minutes |

## Learning objectives

- Complete the E1 operator path end-to-end
- Supply required `case_id` for flagship onboarding
- Approve a human gate and confirm completion
- Know where Improve starts

## Prerequisites

- Live backend + frontend; admin login
- Chapter 2.1 recommended

## Illustration

![E1 operator path](../assets/02-02-e1-path.svg)

*Figure 2.2 — Login → run → approve → complete → improve*

{R()}

## What E1 proves

E1 is the **product-bar** operator path. Automated proof:

`backend/app/tests/e2e/test_e1_operator_path.py`

| Item | Value |
|------|--------|
| Flagship workflow | `wf_customer_onboarding_v12` |
| Critical input | `case_id` (required) |
| Human gate | Billing-style irreversible step |
| Aftercare | Improve / reflect entry on run |

## Lab A — UI path

1. Confirm `NEXT_PUBLIC_DEMO_MODE=false` and backend ready.  
2. Login as `admin@example.com` / `admin-password`.  
3. Open **Workflows**.  
4. Select flagship onboarding `wf_customer_onboarding_v12` (or equivalent seeded name).  
5. Click **Run now**.  
6. Provide input payload including:

```json
{{
  "case_id": "case_lab_e1_001"
}}
```

(If the form uses nested `input_payload`, place `case_id` where the UI expects—mirror validation errors.)

7. When the run pauses, open **Approvals**.  
8. Approve with reason: `lab-e1-approve`.  
9. Return to the run; confirm terminal success.  
10. Locate **Improve** controls on the run detail (used in chapter 3.5).

**Expected:** Run completes after approval; events/audit show progress.

## Lab B — Automated proof

```powershell
cd backend
$env:PYTHONPATH = "."
python -m pytest app/tests/e2e/test_e1_operator_path.py -q --tb=short
```

**Expected:** exit code 0, test passed.

## Common failures

| Symptom | Fix |
|---------|-----|
| Validation error on run | Add `case_id` / required fields |
| Stuck pending | Complete Approvals decision |
| Buttons do nothing | demoMode on → turn off |
| 401 | Re-login; backend up |

## Real-world use cases

### Use case 1 — New environment acceptance

E1 green is the go/no-go for “control plane works.”

### Use case 2 — Training

Operators practice approval rationale quality, not only clicking Approve.

### Use case 3 — Regression

Run the e2e test in CI on every backend change that touches runtime.

## Best practices

- Always use unique `case_id` values per lab to avoid confusion in lists.  
- Write meaningful approval comments.  
- Prefer e2e test when UI is unavailable.

## Chapter summary

- E1 is the flagship live path  
- `case_id` + approval are load-bearing  
- Improve is the bridge to self-improvement  

{quiz([
    ("Flagship workflow id?", "wf_customer_onboarding_v12"),
    ("Required input field highlighted in this guide?", "case_id"),
    ("Which test proves E1?", "test_e1_operator_path.py"),
])}

{nav("02-01-agents-and-tools.md", "02-03-approvals-risk-and-audit.md")}
""",
)

write(
    "02-03-approvals-risk-and-audit.md",
    f"""
# 2.3 Approvals, risk, and audit

| | |
|--|--|
| **Section** | 2 — Intermediate Workflows |
| **Level** | Intermediate |
| **Est. time** | 35–50 minutes |

## Learning objectives

- Map risk tiers to operator behavior
- Approve/reject with rationale
- Find corresponding audit evidence

## Prerequisites

- Completed at least one gated run (2.2)

## Illustration

![Risk tiers and gates](../assets/02-03-governance-gates.svg)

*Figure 2.3 — R0–R4 and audit*

{R()}

## Risk tiers (operator view)

| Tier | Character | Operator stance |
|------|-----------|-----------------|
| R0–R1 | Read / draft | Usually automatic |
| R2 | Reversible write | Logged; soft checks |
| R3–R4 | Irreversible / high impact | **Human approval required** |

Sources: `business/governance/`, `docs/governance.md`, `rules/60-human-approval.md`.

## Approvals UI

1. Open `/app/approvals`.  
2. Select a pending item.  
3. Use the decision panel: **approve** or **reject** + comment.  
4. Live path calls `backendApi.decideApproval` (not a no-op label).

## Audit

- UI: `/app/audit-logs`  
- Runtime: `tool_effects` and decision records  
- Support: capture `request_id` from failed API calls

## Hands-on steps

1. Trigger or reuse an E1 billing gate.  
2. Approve once with comment `lab-2-3-approve`.  
3. Find evidence in Audit Logs (filter by time if needed).  
4. On a disposable run, **reject** once and observe terminal state.

**Expected:** You can narrate who approved what and why.

## Real-world use cases

### Use case 1 — Dual control

Even if product currently allows single approver, process policy may require two humans—document outside the app until enforced.

### Use case 2 — Dispute

Audit trail resolves “the system published without approval” claims.

### Use case 3 — Red team

Attempt to continue a run without approval; expect block.

## Best practices

- Never share “approve everything” accounts.  
- Reject with a fix hint when possible.  
- Review approval backlog daily in production.

## Chapter summary

- R3+ ⇒ human gates  
- Approvals UI + audit close the loop  
- Rationale text is part of the control  

{quiz([
    ("Which tiers need human approval in this model?", "R3–R4"),
    ("Where do operators decide gates?", "/app/approvals"),
    ("Why write a comment?", "Audit and future incident review"),
])}

{nav("02-02-first-workflow-run-e1.md", "02-04-domains-recommend-and-special-skills.md")}
""",
)

write(
    "02-04-domains-recommend-and-special-skills.md",
    f"""
# 2.4 Domain packs: recommend and special skills

| | |
|--|--|
| **Section** | 2 — Intermediate Workflows |
| **Level** | Intermediate |
| **Est. time** | 45–60 minutes |

## Learning objectives

- Submit a free-text brief and read ranked DNA recommendation
- List 17 special skills from live REGISTRY data
- Distinguish selection helpers from live media generation

## Prerequisites

- Live mode login; Domains visible in sidebar

## Illustration

![Brief to DNA recommendation](../assets/02-04-domain-recommend.svg)

*Figure 2.4 — Recommend path and skills catalog*

{R()}

## Domain pack idea

A **domain pack** lives under `business/<domain>/` (flagship: **video**) with agents, DNA, corpus, and integrations. Host rule **N1**: pack holds domain logic; host executes DNA/tools/gates.

Video pack scale (inventory checks): on the order of **114** agents and large corpus—use scripts for exact counts.

## Recommend workflow

| Layer | Entry |
|-------|--------|
| UI | `/app/domains` → Recommend workflow panel |
| API | `POST /api/v1/domains/video/recommend-workflow` |
| Client | `backendApi.recommendVideoWorkflow` |
| Engine | `backend/app/domain/workflows/archetype_selector.py` |
| CLI | `python scripts/business/recommend_video_workflow.py "..."` |

### Lab recommend

1. Open Domains.  
2. Brief: `15s viral TikTok hook about coffee`  
3. Duration: `15`  
4. Run recommend.  

**Expected (verified class of result):** top recommendation DNA id  
`wf_video_arch_a_viral_hook_v1` (code **A**), with confidence and alternatives.  
Respect **HiTL confirm** before any launch.

### Lab recommend (runtime)

```powershell
cd backend
$env:PYTHONPATH = "."
python -c "from pathlib import Path; from app.domain.workflows.archetype_selector import recommend_workflow; r=recommend_workflow('15s viral TikTok hook about coffee', duration_sec=15, top_k=3, repo_root=Path('..').resolve()); print(r['recommendation']['dna_id'])"
```

## Special skills catalog

| Layer | Entry |
|-------|--------|
| Disk | `business/video/special_skills/REGISTRY.json` |
| API | `GET /api/v1/domains/video/special-skills` |
| UI | Domains → Special skills table |
| Runtime | `runtime.list_video_special_skills` |

### Lab skills

1. UI: count rows = **17**; ids must not be `demo_skill_*`.  
2. Open one folder `business/video/special_skills/<skill_id>/`.  
3. Runtime:

```powershell
cd backend
$env:PYTHONPATH = "."
python -c "from app.runtime import runtime; u=runtime.authenticate(runtime.issue_token('admin@example.com','admin-password')['access_token']); d=runtime.list_video_special_skills(u); print(d['count'])"
```

**Expected:** prints `17`.

## Real-world use cases

### Use case 1 — Intake desk

Producer pastes a brief; system suggests DNA A/B/C; human picks and schedules.

### Use case 2 — Capability brochure

Special skills table shows MVP-integrated pack capabilities without opening every folder.

### Use case 3 — Stakeholder demo

Show recommend result, then explicitly state stubs—not finished ads.

## Best practices

- Always run recommend in live mode when claiming “real selector.”  
- Treat scores as MVP health, not marketing 100s.  
- Do not launch DNA without reading gates and scale (S1–S5).

## Chapter summary

- Recommend maps brief → DNA  
- Skills catalog is REGISTRY-backed (17)  
- Neither equals live media production  

{quiz([
    ("Example viral-hook dna_id?", "wf_video_arch_a_viral_hook_v1"),
    ("Special skills count?", "17"),
    ("Recommend API method/path?", "POST /api/v1/domains/video/recommend-workflow"),
])}

{nav("02-03-approvals-risk-and-audit.md", "02-05-knowledge-memory-and-processes.md")}
""",
)

write(
    "02-05-knowledge-memory-and-processes.md",
    f"""
# 2.5 Knowledge, memory, and process basics

| | |
|--|--|
| **Section** | 2 — Intermediate Workflows |
| **Level** | Intermediate |
| **Est. time** | 35–45 minutes |

## Learning objectives

- Use Knowledge and Memory UI surfaces
- Explain Tier 0 vs Tier 1 retrieval at a high level
- Open process intelligence artifacts concept

## Prerequisites

- Section 1; optional E1 completed

## Illustration

![Knowledge and memory tiers](../assets/02-05-knowledge-memory.svg)

*Figure 2.5 — Retrieval tiers and memory scopes*

{R()}

## Knowledge retrieval

| Tier | Behavior |
|------|----------|
| **0** | Keyword + embeddings — broad, fast |
| **1** | Entity multi-hop / K1-lite graph operators |

Policy reference: `business/knowledge-base/provenance/retrieval-tier-policy.md`  
Docs: `docs/knowledge-memory.md`

## Memory scopes

Episodic · semantic · procedural · evaluation — stewarded with retention/provenance thinking. UI: `/app/memory`.

## Process intelligence (intro)

UI: `/app/processes`  
Disk: `business/process-intelligence/`  
PI mines event reality (discovery, conformance, bottlenecks) so improvements are evidence-based (deep dive in advanced evolution chapter).

## Hands-on steps

1. Open **Knowledge**; run a simple search if data exists (empty state is OK).  
2. Open **Memory**; note scopes/labels present.  
3. Open **Processes**; open any summary cards.  
4. Browse `business/knowledge-base/` on disk for structure.

**Expected:** You know where operators look for “what do we know?” vs “what did the process do?”

## Real-world use cases

### Use case 1 — Agent grounding

Before a research-heavy DNA step, Tier 0 search gathers candidates; Tier 1 expands entities.

### Use case 2 — Retention request

Legal asks what is stored in memory scopes—you point to policy + UI.

### Use case 3 — Bottleneck review

Weekly PI review feeds evolution proposals—not gut feel alone.

## Best practices

- Never store secrets in free-text memory.  
- Prefer provenance-bearing sources.  
- Empty indexes are a data problem, not always a product bug.

## Chapter summary

- Tiered retrieval + scoped memory  
- Processes UI surfaces PI  
- Sets up advanced improve/evolution work  

{quiz([
    ("Which tier is broader/faster?", "Tier 0"),
    ("Memory UI route?", "/app/memory"),
    ("Where do PI disk artifacts live?", "business/process-intelligence/"),
])}

{nav("02-04-domains-recommend-and-special-skills.md", "03-01-workflow-dna-deep-dive.md")}
""",
)

print("section2 done")

# ---- Section 3 ----
write(
    "03-01-workflow-dna-deep-dive.md",
    f"""
# 3.1 Workflow DNA deep dive

| | |
|--|--|
| **Section** | 3 — Advanced Customization |
| **Level** | Expert |
| **Est. time** | 50–70 minutes |

## Learning objectives

- Read a `.dna.json` and explain major fields
- Place human gates and verification points
- Describe sandbox → evaluate → canary → promote

## Prerequisites

- Chapters 2.2–2.4

## Illustration

![DNA lifecycle](../assets/03-01-workflow-dna.svg)

*Figure 3.1 — DNA lifecycle*

{R()}

## DNA as executable contract

DNA is **not** a chat prompt. It is a versioned process graph:

- Identity / version metadata  
- `steps[]` with agent, tools, action types  
- Memory read/write declarations  
- Verification hooks  
- Risk / human gate metadata  

Examples:

- `business/video/workflows/wf_video_arch_a_viral_hook_v1.dna.json`  
- Flagship onboarding DNA used by E1  

## Lifecycle (safe change)

1. **Author** DNA offline  
2. **Validate** (`npm run business:validate` / schema tests)  
3. **Sandbox run**  
4. **Evaluate** against corpus  
5. **Canary / versioned promote**  
6. Keep **rollback** DNA id  

> **Warning:** Never mutate production DNA in place.

## Hands-on steps

1. Open viral-hook DNA in an editor.  
2. List each step’s agent and tools in a table.  
3. Mark where a human package/publish gate belongs.  
4. Diff complexity mentally vs onboarding DNA.  
5. Run:

```powershell
npm run business:validate
```

**Expected:** You can explain every step’s purpose in one sentence each.

## Real-world use cases

### Use case 1 — Change control

Marketing wants a new step; you add DNA version `v2`, evaluate, canary—not edit live v1.

### Use case 2 — Incident rollback

Pin traffic back to last known good DNA id.

### Use case 3 — Training authors

Paper exercise: design a 3-step DNA before writing JSON.

## Best practices

- Small steps, explicit tools.  
- Gates on irreversible side effects.  
- Name DNA ids stably and meaningfully.

## Chapter summary

- DNA is the process contract  
- Lifecycle protects production  
- Viral-hook and onboarding are two DNA styles  

{quiz([
    ("Should you edit production DNA in place?", "No"),
    ("Name a viral-hook DNA file purpose.", "Short-form video archetype A workflow"),
    ("What comes before promote?", "Evaluate (and usually canary)"),
])}

{nav("02-05-knowledge-memory-and-processes.md", "03-02-backend-api-integration.md")}
""",
)

write(
    "03-02-backend-api-integration.md",
    f"""
# 3.2 Backend API integration

| | |
|--|--|
| **Section** | 3 — Advanced Customization |
| **Level** | Expert |
| **Est. time** | 50–70 minutes |

## Learning objectives

- Authenticate and call core APIs with a bearer token
- Locate runtime and route modules
- Use health and domains endpoints programmatically

## Prerequisites

- Backend running; Python available

## Illustration

![API surface map](../assets/03-02-api-map.svg)

*Figure 3.2 — Major API groups*

{R()}

## Map

| Piece | Path |
|-------|------|
| App | `backend/app/main.py` |
| Engine | `backend/app/runtime.py` |
| Routes | `backend/app/api/v1/routes/` |
| Base URL | `http://127.0.0.1:8000/api/v1` |

## Essential endpoints

| Area | Examples |
|------|----------|
| Health | `/health`, `/health/live`, `/health/ready` |
| Auth | `POST /auth/login` |
| Workflows/runs | list, create, run, retry, cancel |
| Approvals | decision |
| Domains | `POST /domains/video/recommend-workflow`, `GET /domains/video/special-skills` |
| Improvement | `/improvement/reflect/{{run_id}}`, `/improvement/lessons` |
| Evolution | `/evolution/archive` |
| Loops | `POST /loops/run` |

## Hands-on steps

1. Login and store token (chapter 1.5 pattern).  
2. `GET /workflows` with `Authorization: Bearer …`.  
3. `POST /domains/video/recommend-workflow` with brief JSON.  
4. `GET /domains/video/special-skills` and confirm count 17.  
5. Run unit tests:

```powershell
cd backend
$env:PYTHONPATH = "."
python -m pytest app/tests/unit/test_video_archetype_selector.py app/tests/unit/test_video_special_skills_api.py -q
```

**Expected:** tests pass; API returns non-demo data.

## Real-world use cases

### Use case 1 — External portal

A thin internal portal calls recommend only; ops console remains for approvals.

### Use case 2 — Automation bot

Service account runs inventory checks via scripts, not UI.

### Use case 3 — Debugging

Reproduce UI failure with curl to isolate frontend vs backend.

## Best practices

- Always send auth on non-public routes.  
- Log `request_id` from errors.  
- Prefer OpenAPI export for client generation when available.

## Chapter summary

- Runtime + routes own behavior  
- Domains APIs power pack UX  
- Tests are first-class clients  

{quiz([
    ("Runtime singleton module?", "backend/app/runtime.py"),
    ("Special skills HTTP method?", "GET"),
    ("Base API prefix?", "/api/v1"),
])}

{nav("03-01-workflow-dna-deep-dive.md", "03-03-rbac-and-permissions.md")}
""",
)

write(
    "03-03-rbac-and-permissions.md",
    f"""
# 3.3 RBAC and permission-aware UI

| | |
|--|--|
| **Section** | 3 — Advanced Customization |
| **Level** | Expert |
| **Est. time** | 35–50 minutes |

## Learning objectives

- Map roles → permissions → visible nav items
- Explain why UI hide is not sufficient security
- Plan least-privilege operator roles

## Prerequisites

- Chapters 1.4–1.5

## Illustration

![RBAC to UI](../assets/03-03-rbac.svg)

*Figure 3.3 — Role → permissions → UI*

{R()}

## Model

1. User has a **role**.  
2. Role grants **permissions** (e.g. `workflows:read`, `approvals:read`).  
3. `NAVIGATION_GROUPS` items declare required permissions.  
4. Sidebar filters with `hasPermission`.  
5. **API still enforces** authorization—UI is convenience, not the boundary.

Code: `frontend/src/types/permissions.ts`, `navigation.ts`, `lib/auth/permissions`.

## Hands-on steps

1. As admin, note visible nav count.  
2. Read permission strings on Domains / Approvals items in `navigation.ts`.  
3. Sketch a role `operator_readonly` with only `*:read` style permissions.  
4. Confirm Settings/Users would hide for that role.

**Expected:** You can predict hidden items from a permission list.

## Real-world use cases

### Use case 1 — External reviewer

Approvals + audit only; no agent create.

### Use case 2 — Producer

Domains + workflows run; no user admin.

### Use case 3 — Break-glass

Time-limited admin elevation with audit.

## Best practices

- Least privilege by default.  
- Review permission diffs in PRs.  
- Pair API tests with UI permission assumptions.

## Chapter summary

- RBAC drives nav and actions  
- Server enforcement is mandatory  
- Design roles around jobs-to-be-done  

{quiz([
    ("Does hiding a nav item secure the API?", "No—API must enforce too."),
    ("Where are nav permissions declared?", "NAVIGATION_GROUPS in navigation.ts"),
    ("Example permission?", "workflows:read (or similar)"),
])}

{nav("03-02-backend-api-integration.md", "03-04-extending-domain-packs.md")}
""",
)

write(
    "03-04-extending-domain-packs.md",
    f"""
# 3.4 Extending with domain packs

| | |
|--|--|
| **Section** | 3 — Advanced Customization |
| **Level** | Expert |
| **Est. time** | 60–90 minutes |

## Learning objectives

- Scaffold a minimal domain pack structure
- Wire agents, DNA, and tool allow-lists consistently
- Prove with inventory/golden checks—not second control planes

## Prerequisites

- Chapters 3.1–3.2
- Comfort editing JSON

## Illustration

![Extend pack steps](../assets/03-04-extend-pack.svg)

*Figure 3.4 — Manifest → register → tools → prove*

{R()}

## Extension algorithm

1. **Manifest** under `business/<domain>/` with agents + workflows  
2. **Register / inventory** so the host can load and count  
3. **Tools** — adapters + agent allow-lists + DNA step tools align  
4. **Prove** — golden task, unit/e2e as appropriate  

Runbook: `docs/add-domain-pack-runbook.md`  
Examples: `business/example_education/`, `business/example_research/`  
Video reference quality: `python scripts/business/inventory_check.py`

## Anti-patterns

- Forking a second LangGraph “host” for domain logic  
- Rubber-stamp score 100s without research  
- Editing production DNA without evaluate/canary  

## Hands-on steps

1. Read `business/example_education/manifest.json` and its DNA.  
2. Draft a one-page design for a tiny pack (name, 1 agent, 1 DNA, 1 golden).  
3. Run video inventory check as a quality bar reference.  
4. List which host APIs (if any) you would need beyond pack files.

**Expected:** A written pack design that obeys N1.

## Real-world use cases

### Use case 1 — New vertical

Education pack first; reuse host gates and audit.

### Use case 2 — Vendor swap

Replace a stub tool adapter without rewriting DNA ids.

### Use case 3 — Acquisition integration

Import partner agents as a pack with quarantine evals.

## Best practices

- Version packs explicitly.  
- Document residuals in pack README.  
- Keep host changes minimal and generic.

## Chapter summary

- Packs extend capability under N1  
- Prove before promote  
- No second control plane  

{quiz([
    ("What is N1?", "Domain logic stays in pack."),
    ("Example pack folder?", "business/example_education/"),
    ("Name an anti-pattern.", "Second control plane / in-place prod DNA edit / fake 100 scores"),
])}

{nav("03-03-rbac-and-permissions.md", "03-05-improve-loops-and-evolution.md")}
""",
)

write(
    "03-05-improve-loops-and-evolution.md",
    f"""
# 3.5 Improve pipeline, loops, and evolution

| | |
|--|--|
| **Section** | 3 — Advanced Customization |
| **Level** | Expert |
| **Est. time** | 45–65 minutes |

## Learning objectives

- Run Improve steps on a completed run
- Explain sandbox evaluate → canary rules
- Call improvement/evolution APIs

## Prerequisites

- Completed E1 run (2.2)

## Illustration

![Improve and evolution loop](../assets/03-05-improve-evolution.svg)

*Figure 3.5 — Reflect → lessons → propose → eval → canary*

{R()}

## Improve pipeline (UI)

On a completed run detail:

**Reflect → Propose → Evaluate → Canary** (or full pipeline control)

## APIs

| Method | Path |
|--------|------|
| POST | `/api/v1/improvement/reflect/{{run_id}}` |
| GET | `/api/v1/improvement/lessons` |
| POST | `/api/v1/improvement/auto-propose` |
| POST | `/api/v1/loops/run` |
| GET | `/api/v1/evolution/archive` |

Docs: `docs/self-improvement-and-orchestration.md`, `docs/evolution-sandbox.md`  
Artifacts: `business/evolution/`, `business/evals/`

## Rules

- Loops need **stop criteria** (max iterations / fitness / human abort).  
- Evolution variants stay sandbox until evaluated.  
- Promote is explicit; rollback DNA retained.

## Hands-on steps

1. Open a completed E1 run.  
2. Trigger **Reflect** if available.  
3. Open `/app/evolution` archive.  
4. List golden tasks under `business/evals/golden-tasks/` (product bar aims ≥20).  
5. Optional: `GET /improvement/lessons` with bearer token.

**Expected:** Lesson artifacts or clear empty state; archive UI loads.

## Real-world use cases

### Use case 1 — Weekly improvement council

Review lessons, accept 1–2 sandbox proposals max.

### Use case 2 — Fitness regression

Canary detects drop; auto-rollback to previous DNA.

### Use case 3 — Loop DNA for flaky research steps

Bounded retries with verifier—not infinite agent chatter.

## Best practices

- Human review of proposals that touch money/PII.  
- Never auto-promote to 100% traffic.  
- Keep eval corpus healthy.

## Chapter summary

- Improve closes the learning loop  
- Evolution is sandboxed  
- APIs mirror UI pipeline  

{quiz([
    ("Name first Improve step.", "Reflect"),
    ("Where is evolution UI?", "/app/evolution"),
    ("Promote without evaluate?", "No"),
])}

{nav("03-04-extending-domain-packs.md", "04-01-common-errors-and-fixes.md")}
""",
)

print("section3 done")

# ---- Section 4 ----
write(
    "04-01-common-errors-and-fixes.md",
    f"""
# 4.1 Common errors and fixes

| | |
|--|--|
| **Section** | 4 — Troubleshooting & Support |
| **Level** | All levels |
| **Est. time** | 30–45 minutes |

## Learning objectives

- Diagnose failures by layer (boot, auth, UI, run, pack)
- Apply the troubleshooting matrix
- Capture enough context to avoid blind retries

## Prerequisites

- Sections 1–2 experience preferred

## Illustration

![Troubleshooting decision tree](../assets/04-01-error-matrix.svg)

*Figure 4.1 — Symptom → layer → fix*

{R()}

## Matrix

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Backend won't start | deps / cwd / PYTHONPATH | `pip install -e .`, set `PYTHONPATH=.` |
| Port 8000 busy | other process | free port or change bind |
| ready degraded | no Postgres | set `DATABASE_URL` or accept json-file |
| Login fails | backend down / bad password | start uvicorn; seed creds |
| UI mocks / demo skills | `NEXT_PUBLIC_DEMO_MODE=true` | set `false`; restart Next |
| Domains missing | nav not wired / permissions | `NAVIGATION_GROUPS` + role |
| Recommend empty/mock | demoMode or 401 | live mode + login |
| E1 validation error | missing `case_id` | add to payload |
| Approval stuck | role / API error | admin role; check request_id |
| Inventory fail | pack incomplete | fix agents/DNA; re-run scripts |

## Hands-on drills

1. Toggle demoMode true → observe mock skills → restore false.  
2. Stop backend → note UI errors → restart.  
3. Run without `case_id` → read validation → fix.

## Real-world use cases

### Use case 1 — War room

Paste matrix into incident channel; assign layer owners.

### Use case 2 — Onboarding FAQ

Link this chapter from internal wiki.

### Use case 3 — Support L1

L1 uses matrix; L2 gets evidence pack (4.3).

## Best practices

- Change one variable at a time.  
- Write down last good state.  
- Prefer reproduction over speculation.

## Chapter summary

- Layered diagnosis beats random restarts  
- demoMode and case_id are top footguns  
- Matrix is living documentation  

{quiz([
    ("Top cause of UI mocks?", "NEXT_PUBLIC_DEMO_MODE true"),
    ("Flagship required field?", "case_id"),
    ("Domains missing first checks?", "navigation + permissions"),
])}

{nav("03-05-improve-loops-and-evolution.md", "04-02-health-doctor-and-diagnostics.md")}
""",
)

write(
    "04-02-health-doctor-and-diagnostics.md",
    f"""
# 4.2 Health, doctor, and diagnostics

| | |
|--|--|
| **Section** | 4 — Troubleshooting & Support |
| **Level** | Intermediate–Expert |
| **Est. time** | 25–40 minutes |

## Learning objectives

- Interpret `/health`, `/live`, `/ready`
- Run `npm run doctor` and product check scripts
- Know when degraded is acceptable

## Prerequisites

- Backend install from section 1

## Illustration

![Health endpoints](../assets/04-02-health-doctor.svg)

*Figure 4.2 — Health triad and doctor*

{R()}

## Health triad

| Endpoint | Question it answers |
|----------|---------------------|
| `/api/v1/health` | Process up? |
| `/api/v1/health/live` | Liveness? |
| `/api/v1/health/ready` | Dependencies ready? (`database` field) |

## Commands

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health/ready
cd C:\\Project\\generic-swarm-ops
npm run doctor
python scripts/business/check_executable_product.py
```

## Hands-on steps

1. Capture ready JSON while healthy.  
2. Optionally mis-set `DATABASE_URL`, restart, compare ready.  
3. Restore config.  
4. Run doctor; file any red items.

**Expected:** You can explain degraded vs hard down.

## Real-world use cases

### Use case 1 — Load balancer probes

live for liveness; ready for traffic admission.

### Use case 2 — Release gate

doctor + executable check before demo.

### Use case 3 — On-call

ready database field distinguishes DB outage from app bug.

## Best practices

- Alert on ready failures in shared envs.  
- Keep executable check in CI if feasible.  
- Document intentional degraded modes.

## Chapter summary

- Health endpoints split process vs deps  
- doctor covers tree integrity  
- executable script guards product bar  

{quiz([
    ("Which endpoint reports database?", "/health/ready"),
    ("doctor command?", "npm run doctor"),
    ("Is degraded always an outage?", "No—json-file learning may be degraded yet usable."),
])}

{nav("04-01-common-errors-and-fixes.md", "04-03-support-paths-and-evidence.md")}
""",
)

write(
    "04-03-support-paths-and-evidence.md",
    f"""
# 4.3 Support paths and evidence packs

| | |
|--|--|
| **Section** | 4 — Troubleshooting & Support |
| **Level** | All levels |
| **Est. time** | 20–30 minutes |

## Learning objectives

- Build a minimal evidence pack for support
- Avoid leaking secrets
- Know where deeper docs live

## Prerequisites

- Ability to reproduce a simple failure

## Illustration

![Support evidence pack](../assets/04-03-support-evidence.svg)

*Figure 4.3 — What to collect*

{R()}

## Evidence pack checklist

- [ ] UTC timestamp of issue  
- [ ] Node/Python versions  
- [ ] `health/ready` JSON  
- [ ] `NEXT_PUBLIC_DEMO_MODE` value  
- [ ] `NEXT_PUBLIC_API_BASE_URL`  
- [ ] Workflow id / run id if any  
- [ ] `request_id` from errors  
- [ ] Minimal repro steps (5 lines)  
- [ ] Screenshots **without** secrets  

## Support paths (typical)

1. Self-serve: chapters 4.1–4.2  
2. Internal platform channel with evidence pack  
3. Design depth: `book/design_phase/` (engineering, not L1)  
4. Product claims disputes: `EXECUTABLE_PRODUCT.md`

There is no external SaaS ticket UI in the open repo—use your organization’s process.

## Hands-on steps

1. Intentionally cause a login failure (wrong password).  
2. Write a 5-line repro.  
3. Attach ready JSON + demoMode value.  
4. Redact password from any notes.

**Expected:** Another engineer could retry your steps cold.

## Real-world use cases

### Use case 1 — Vendor escalation

Evidence pack prevents “works on my machine” loops.

### Use case 2 — Security review

Prove gates fired with audit excerpts (no PII dumps).

### Use case 3 — Handoff

Night shift leaves evidence pack in ticket.

## Best practices

- Prefer text over huge videos first.  
- Never paste production secrets.  
- One issue per ticket.

## Chapter summary

- Evidence packs speed support  
- Redact ruthlessly  
- Point to honesty docs for scope fights  

{quiz([
    ("Name three evidence fields.", "ready JSON, demoMode, request_id (examples)"),
    ("Should you paste admin passwords into tickets?", "No"),
    ("Where are design monographs?", "book/design_phase/"),
])}

{nav("04-02-health-doctor-and-diagnostics.md", "05-01-performance-and-postgres.md")}
""",
)

# ---- Section 5 ----
write(
    "05-01-performance-and-postgres.md",
    f"""
# 5.1 Performance and Postgres ops

| | |
|--|--|
| **Section** | 5 — Optimization & Scaling |
| **Level** | Advanced Expert |
| **Est. time** | 40–55 minutes |

## Learning objectives

- Prefer Postgres as primary store for durable ops
- Apply basic performance hygiene
- Use the Postgres runbook

## Prerequisites

- Section 1 install knowledge

## Illustration

![Postgres performance path](../assets/05-01-postgres-perf.svg)

*Figure 5.1 — Postgres primary with JSON snapshot backup*

{R()}

## Persistence model

| Store | Role |
|-------|------|
| Postgres `runtime_state` JSONB | Primary when `DATABASE_URL` set |
| `backend/data/runtime.json` | Snapshot backup / seed |

Runbook: `backend/docs/postgres-runbook.md`

## Hands-on steps

1. Configure `DATABASE_URL` in `backend/.env`.  
2. Restart uvicorn; check ready `database: postgres`.  
3. Run E1 once; confirm state survives restart.  
4. Note backup/snapshot path exists.

**Expected:** Restarts keep workflow/run history when using Postgres.

## Performance hygiene

- Avoid unbounded debug logging in hot paths  
- Keep eval corpora trimmed for local machines  
- Monitor disk for `business/` artifact growth  
- Use connection pooling settings per runbook when scaling  

## Real-world use cases

### Use case 1 — Demo laptop vs server

Laptop JSON-file; server Postgres.

### Use case 2 — Burst workshops

Postgres sized for concurrent learners; ready probes on LB.

### Use case 3 — Backup drill

Restore from snapshot procedure quarterly.

## Best practices

- Never rely on a single laptop disk for production state.  
- Test backup restore, not only backup creation.  
- Document RPO/RTO targets for your org.

## Chapter summary

- Postgres is the durability path  
- JSON is learning/backup  
- Hygiene beats premature micro-optimizations  

{quiz([
    ("Primary production store?", "Postgres"),
    ("Env var for DB?", "DATABASE_URL"),
    ("JSON file role?", "Snapshot/backup/learning"),
])}

{nav("04-03-support-paths-and-evidence.md", "05-02-security-hardening.md")}
""",
)

write(
    "05-02-security-hardening.md",
    f"""
# 5.2 Security hardening

| | |
|--|--|
| **Section** | 5 — Optimization & Scaling |
| **Level** | Advanced Expert |
| **Est. time** | 40–60 minutes |

## Learning objectives

- Apply a hardening checklist beyond seed demos
- Combine RBAC, allow-lists, and gates
- Reference agentic security rules

## Prerequisites

- Chapters 2.3, 3.3

## Illustration

![Security hardening pillars](../assets/05-02-security-hardening.svg)

*Figure 5.2 — Identity, runtime, operate*

{R()}

## Hardening checklist

- [ ] Replace seed admin password; disable shared lab accounts  
- [ ] `NEXT_PUBLIC_DEMO_MODE` not true in shared envs  
- [ ] Registration locked down if unused  
- [ ] Tool allow-lists least privilege  
- [ ] R3+ always gated; no bypass flags in prod  
- [ ] API keys scoped + rotated  
- [ ] Secrets only in env/secret manager  
- [ ] Audit log retention defined  
- [ ] Dependencies scanned per org policy  

References: `docs/security.md`, `rules/30-security.md`, `rules/110-agentic-security.md`

## Agentic specifics

- Treat tool outputs as untrusted in later prompts.  
- Constrain browsing/code tools.  
- Prefer human gates for external side effects.

## Hands-on steps

1. Walk the checklist against your local lab (expect many “N/A lab only”).  
2. Read `rules/110-agentic-security.md` highlights.  
3. Confirm demoMode false on any shared compose file.

## Real-world use cases

### Use case 1 — Pre-production gate

Security signs checklist before customer data.

### Use case 2 — Key leak

Rotate API keys; review audit for misuse window.

### Use case 3 — Prompt injection drill

Use agentic-red-team skill scenarios in a sandbox.

## Best practices

- Defense in depth: UI + API + tools + gates.  
- Log access to admin surfaces.  
- Separate duties: author DNA ≠ sole approver when possible.

## Chapter summary

- Seed demos are not secure defaults  
- Allow-lists + gates + RBAC stack  
- Agentic threats need explicit design  

{quiz([
    ("Keep demoMode on in prod?", "No"),
    ("Name one agentic control.", "Tool allow-list / human gate / treat tool output untrusted"),
    ("Seed password OK in production?", "No"),
])}

{nav("05-01-performance-and-postgres.md", "05-03-deployment-scale-and-maintenance.md")}
""",
)

write(
    "05-03-deployment-scale-and-maintenance.md",
    f"""
# 5.3 Deployment, scale, and maintenance

| | |
|--|--|
| **Section** | 5 — Optimization & Scaling |
| **Level** | Advanced Expert |
| **Est. time** | 40–60 minutes |

## Learning objectives

- Describe a sane deploy loop for this architecture
- Separate scale levers (app vs DB vs packs)
- Run a weekly maintenance cadence

## Prerequisites

- Sections 1–4

## Illustration

![Deploy and maintain](../assets/05-03-deploy-maintain.svg)

*Figure 5.3 — Build → test → canary → observe*

{R()}

## Deploy loop

1. **Build** backend/frontend artifacts  
2. **Test** E1 + unit suites + doctor  
3. **Canary** DNA and app release  
4. **Observe** ready, errors, approval backlog  
5. **Rollback** app or DNA independently when needed  

## Scale levers

| Lever | Notes |
|-------|-------|
| Horizontal API instances | Stateless app + shared Postgres |
| DB sizing | Primary bottleneck for shared state |
| Artifact growth | `business/` evals/evolution disk |
| LLM/tool cost | Not free—budget loops/stop criteria |
| Pack complexity | More agents ≠ more value without evals |

## Weekly maintenance

- [ ] `npm run doctor`  
- [ ] Security/script checks your org requires  
- [ ] Approval backlog zero or escalated  
- [ ] Evolution archive skim  
- [ ] Backup verify note  
- [ ] Dependency update batch  

## Hands-on steps

1. Write your environment’s deploy checklist (10 lines).  
2. Identify rollback owner for DNA vs app.  
3. Schedule a calendar reminder for weekly maintenance.

**Expected:** A concrete ops cadence, not only “we’ll monitor.”

## Real-world use cases

### Use case 1 — Startup production

Single region, Postgres, two API replicas, manual canary.

### Use case 2 — Enterprise

Change windows, dual control on promote, SIEM audit export.

### Use case 3 — Multi-pack org

Pack teams ship independently; host versioning matrix enforced.

## Best practices

- Canary DNA separately from app binaries.  
- Keep executable product scripts in CI.  
- Document residuals in release notes.

## Chapter summary

- Deploy is a loop with rollback  
- Scale the bottleneck you measure  
- Maintenance is scheduled work  

{quiz([
    ("Name two independent rollback targets.", "App release and DNA version"),
    ("Why stop criteria on loops?", "Cost and runaway automation"),
    ("Weekly item example?", "doctor / approvals / backups"),
])}

{nav("05-02-security-hardening.md", "99-01-glossary.md")}
""",
)

# ---- Appendices ----
write(
    "99-01-glossary.md",
    f"""
# Appendix A — Glossary

{R()}

| Term | Definition |
|------|------------|
| Agent | Runtime actor with allow-listed tools |
| Approval | Human decision on a gated step |
| Archetype | Video workflow class (A–J) |
| Bootstrap | `npm run bootstrap` setup |
| Canary | Limited rollout of a change |
| DNA | Workflow definition JSON |
| Domain pack | Versioned domain bundle under `business/` |
| demoMode | Frontend fixture mode; must be opt-in only |
| E1 | Flagship operator acceptance path |
| Evolution | Sandbox variant search + archive |
| Gate / HiTL | Human-in-the-loop hold |
| Harness | `.trae` / `.grok` coding-agent config |
| Inventory | Pack integrity check |
| K1-lite | Lightweight knowledge graph operators |
| Lesson | Post-run reflection artifact |
| N1 | Domain logic stays in pack |
| PI | Process intelligence |
| RBAC | Role-based access control |
| Runtime | `RuntimeServices` engine |
| Special skill | Catalogued pack integration |
| tool_effects | Audited tool side effects |
| viral-hook | `wf_video_arch_a_viral_hook_v1` |

{nav("05-03-deployment-scale-and-maintenance.md", "99-02-command-api-cheatsheet.md")}
""",
)

write(
    "99-02-command-api-cheatsheet.md",
    f"""
# Appendix B — Command and API cheat sheet

{R()}

## npm (repo root)

```text
npm run bootstrap
npm run doctor
npm run sync
npm run business:validate
npm run business:governance
npm run business:security
npm run business:evolution:check
npm run business:eval
```

## Backend

```powershell
cd backend
python -m pip install -e .
$env:PYTHONPATH = "."
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
python -m pytest app/tests/e2e/test_e1_operator_path.py -q
```

## Frontend

```powershell
cd frontend
$env:NEXT_PUBLIC_DEMO_MODE = "false"
$env:NEXT_PUBLIC_API_BASE_URL = "http://127.0.0.1:8000/api/v1"
pnpm install
pnpm dev
```

## Auth

`POST /api/v1/auth/login` with `admin@example.com` / `admin-password`

## Domains

- `POST /api/v1/domains/video/recommend-workflow`
- `GET /api/v1/domains/video/special-skills`
- `GET /api/v1/domains/video/archetypes`

## Improvement / evolution

- `POST /api/v1/improvement/reflect/{{run_id}}`
- `GET /api/v1/improvement/lessons`
- `POST /api/v1/loops/run`
- `GET /api/v1/evolution/archive`

## Health

- `GET /api/v1/health`
- `GET /api/v1/health/live`
- `GET /api/v1/health/ready`

{nav("99-01-glossary.md", None)}
""",
)


def write_masters():
    chapters = [
        ("1 — Fundamentals", [
            ("01-01-system-overview.md", "1.1 System overview"),
            ("01-02-prerequisites-and-environment.md", "1.2 Prerequisites and environment"),
            ("01-03-install-bootstrap-first-boot.md", "1.3 Install, bootstrap, and first boot"),
            ("01-04-ops-console-navigation.md", "1.4 Ops console navigation"),
            ("01-05-accounts-login-and-session.md", "1.5 Accounts, login, and session"),
        ]),
        ("2 — Intermediate workflows", [
            ("02-01-agents-and-tools.md", "2.1 Agents and tools"),
            ("02-02-first-workflow-run-e1.md", "2.2 First workflow run (E1)"),
            ("02-03-approvals-risk-and-audit.md", "2.3 Approvals, risk, and audit"),
            ("02-04-domains-recommend-and-special-skills.md", "2.4 Domains: recommend and special skills"),
            ("02-05-knowledge-memory-and-processes.md", "2.5 Knowledge, memory, and processes"),
        ]),
        ("3 — Advanced customization", [
            ("03-01-workflow-dna-deep-dive.md", "3.1 Workflow DNA deep dive"),
            ("03-02-backend-api-integration.md", "3.2 Backend API integration"),
            ("03-03-rbac-and-permissions.md", "3.3 RBAC and permissions"),
            ("03-04-extending-domain-packs.md", "3.4 Extending domain packs"),
            ("03-05-improve-loops-and-evolution.md", "3.5 Improve, loops, and evolution"),
        ]),
        ("4 — Troubleshooting", [
            ("04-01-common-errors-and-fixes.md", "4.1 Common errors and fixes"),
            ("04-02-health-doctor-and-diagnostics.md", "4.2 Health, doctor, and diagnostics"),
            ("04-03-support-paths-and-evidence.md", "4.3 Support paths and evidence"),
        ]),
        ("5 — Optimization and scaling", [
            ("05-01-performance-and-postgres.md", "5.1 Performance and Postgres"),
            ("05-02-security-hardening.md", "5.2 Security hardening"),
            ("05-03-deployment-scale-and-maintenance.md", "5.3 Deployment, scale, and maintenance"),
        ]),
        ("Appendices", [
            ("99-01-glossary.md", "A — Glossary"),
            ("99-02-command-api-cheatsheet.md", "B — Command and API cheat sheet"),
        ]),
    ]

    lines = [
        "# Generic Swarm Ops — User Guide",
        "",
        "**Beginner → expert.** Complete operator and platform guide for **generic-swarm-ops**.",
        "",
        "| | |",
        "|--|--|",
        "| **Location** | `book/user_guide/` |",
        "| **Chapters** | [`chapters/`](./chapters/) |",
        "| **Illustrations** | [`assets/`](./assets/) |",
        "| **Plan / TOC** | [`../../planning/user_guide/`](../../planning/user_guide/) |",
        "| **Instruction** | [`../../create_user_guide.md`](../../create_user_guide.md) |",
        "| **Design monographs** | [`../design_phase/`](../design_phase/) |",
        "",
        R(),
        "",
        "## How to use this guide",
        "",
        "1. Work **in order** through Section 1, then 2.",
        "2. Complete every **Hands-on** block on a live stack when possible.",
        "3. Use Section 4 when blocked; Section 5 before production.",
        "4. End each chapter with the knowledge check.",
        "",
        "![System architecture](./assets/01-01-system-architecture.svg)",
        "",
        "## Table of contents",
        "",
    ]
    for sec, items in chapters:
        lines.append(f"### {sec}")
        lines.append("")
        for fn, title in items:
            lines.append(f"- [{title}](./chapters/{fn})")
        lines.append("")

    lines += [
        "## Suggested first day",
        "",
        "1. 1.2–1.3 Boot stack  ",
        "2. 1.4–1.5 Navigate + login  ",
        "3. 2.2 E1 path  ",
        "4. 2.4 Recommend + 17 skills  ",
        "",
        "## Quality notes",
        "",
        "- Steps use real product ids (`wf_customer_onboarding_v12`, `wf_video_arch_a_viral_hook_v1`).",
        "- SVGs embed with relative paths under `assets/`.",
        "- Honesty residuals repeated to prevent over-claiming media studio.",
        "",
    ]
    (BOOK / "user_guide.md").write_text("\n".join(lines), encoding="utf-8")

    readme = """# User guide

Canonical beginner→expert guide for **generic-swarm-ops**.

| Start here | |
|------------|--|
| **[user_guide.md](./user_guide.md)** | Master TOC + entry |
| [chapters/](./chapters/) | Individual chapters (`NN-MM-*.md`) |
| [assets/](./assets/) | SVG illustrations |
| Plan | [../../planning/user_guide/](../../planning/user_guide/) |

Built per repository instruction [`create_user_guide.md`](../../create_user_guide.md).
"""
    (BOOK / "README.md").write_text(readme, encoding="utf-8")
    print("masters written")


if __name__ == "__main__":
    write_masters()
    print("all rest done", "chapters=", len(list(CH.glob("*.md"))), "svgs=", len(list((BOOK / "assets").glob("*.svg"))))
