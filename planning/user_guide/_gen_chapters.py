"""Generate chapter scaffold markdown files for the user_guide plan."""
from __future__ import annotations

from pathlib import Path
from textwrap import dedent

# Canonical publish home for user guide chapters
ROOT = Path(__file__).resolve().parents[2] / "book" / "user_guide"
CH = ROOT / "chapters"
CH.mkdir(parents=True, exist_ok=True)

# Each chapter: id, title, level, part, svg, objectives, outline sections, labs, sources
CHAPTERS = [
    {
        "id": "00",
        "file": "00-how-to-use-this-guide.md",
        "title": "How to use this guide",
        "level": "Beginner",
        "part": "Front matter",
        "svg": "01-learning-path.svg",
        "time": "15 min",
        "objectives": [
            "Choose a learning track (operator / builder / SRE) by goal",
            "Understand doc map: this guide vs design_phase book vs structure.md",
            "Know honesty boundaries (what is executable vs residual)",
        ],
        "outline": [
            "Who this guide is for (operator, pack author, platform engineer)",
            "How the multi-file guide is organized (parts I–V)",
            "Symbols: Lab · API · UI · Caution · Residual claim",
            "Prerequisites checklist (Node, Python, optional Postgres, ports)",
            "Relationship to book/design_phase (architecture deep dives) and docs/*",
            "Honesty box: live media, full studio, inflated scores — out of scope",
        ],
        "labs": [
            "Skim TOC and mark your track (operator path: ch01–ch09 first)",
            "Open EXECUTABLE_PRODUCT.md and note proven vs not-claimed table",
        ],
        "sources": [
            "EXECUTABLE_PRODUCT.md",
            "README.md",
            "book/design_phase/book.md (design context only)",
        ],
    },
    {
        "id": "01",
        "file": "01-what-is-this-system.md",
        "title": "What is generic-swarm-ops?",
        "level": "Beginner",
        "part": "Part I — Foundations",
        "svg": "02-system-overview.svg",
        "time": "30 min",
        "objectives": [
            "Explain the system in one paragraph without jargon",
            "Name the four planes: console, control plane, business OS, domain packs",
            "State N1 rule: domain logic in pack; host executes DNA/tools/gates",
        ],
        "outline": [
            "Problem: multi-agent work without audit, gates, or improvement loops",
            "Product name and dual-harness (Trae + Grok) at a high level",
            "Four planes diagram walkthrough",
            "Core nouns: agent, tool, DNA workflow, run, approval, lesson, domain pack",
            "What you can run today (E1 + viral-hook) vs design aspirational docs",
            "Glossary starter (link to appendix A when written)",
        ],
        "labs": [
            "Draw your own 4-box diagram from memory",
            "List 5 nouns you will use in every run",
        ],
        "sources": [
            "docs/architecture.md",
            "structure.md",
            "EXECUTABLE_PRODUCT.md",
        ],
    },
    {
        "id": "02",
        "file": "02-mental-model-and-layers.md",
        "title": "Mental model and layered architecture",
        "level": "Beginner",
        "part": "Part I — Foundations",
        "svg": "02-system-overview.svg",
        "time": "40 min",
        "objectives": [
            "Map repo folders to runtime layers",
            "Explain harness sync (.trae/.grok) vs runtime backend",
            "Trace a request: UI → API → runtime → tool → audit",
        ],
        "outline": [
            "Layer table: starter, business, backend, frontend, generated",
            "Repo map walk: backend/, frontend/, business/, rules/, scripts/",
            "Request lifecycle sequence (operator click → JSON → DNA step)",
            "Persistence: Postgres primary, JSON snapshot backup",
            "Why evolution never mutates production DNA in place",
            "Common misconception: 'second LangGraph control plane' — not here",
        ],
        "labs": [
            "From repo root, list top-level dirs and assign each to a layer",
            "Read docs/architecture.md end-to-end once",
        ],
        "sources": [
            "docs/architecture.md",
            "structure.md",
            "docs/sync.md",
        ],
    },
    {
        "id": "03",
        "file": "03-install-and-first-boot.md",
        "title": "Install and first boot",
        "level": "Beginner",
        "part": "Part I — Foundations",
        "svg": "03-install-boot.svg",
        "time": "45–90 min",
        "objectives": [
            "Bootstrap the repo and pass doctor checks",
            "Start backend and hit health/ready",
            "Start frontend with live APIs (demoMode off)",
        ],
        "outline": [
            "Prerequisites (OS, Node, Python, pnpm, optional Docker Postgres)",
            "npm run bootstrap / doctor / sync",
            "Backend: pip install -e ., uvicorn, .env and DATABASE_URL options",
            "JSON-file mode vs Postgres (when degraded is OK for learning)",
            "Frontend: NEXT_PUBLIC_DEMO_MODE must not be true for real product path",
            "Seed login admin@example.com / admin-password",
            "Troubleshooting first boot (ports, CORS, PYTHONPATH)",
        ],
        "labs": [
            "Lab A: backend health/live/ready curl or browser",
            "Lab B: frontend login and land on Dashboard",
            "Lab C: intentionally set demoMode true, see mock behavior, then restore false",
        ],
        "sources": [
            "docs/installation.md",
            "docs/usage.md",
            "backend/docs/postgres-runbook.md",
            "frontend/README.md",
            "frontend/.env.example",
        ],
    },
    {
        "id": "04",
        "file": "04-ops-console-tour.md",
        "title": "Ops console tour",
        "level": "Beginner",
        "part": "Part I — Foundations",
        "svg": "04-console-map.svg",
        "time": "30 min",
        "objectives": [
            "Navigate every sidebar group without dead ends",
            "Open Domains and recognize recommend + special skills panels",
            "Know where audit logs and API keys live",
        ],
        "outline": [
            "Sidebar groups: Main, Data, Quality, Security, Admin",
            "Route table: appPaths (dashboard, agents, domains, workflows, …)",
            "Domains page panels deep-link",
            "Permission-gated items (role-based visibility)",
            "Command palette / mobile nav notes",
            "Demo vs live visual cues in the UI",
        ],
        "labs": [
            "Click every Main nav item; screenshot or note empty states",
            "Open /app/domains and identify recommend-workflow-panel test id",
        ],
        "sources": [
            "frontend/src/types/navigation.ts",
            "frontend/src/lib/routes/paths.ts",
            "frontend/src/app/app/[...slug]/page.tsx",
        ],
    },
    {
        "id": "05",
        "file": "05-first-workflow-run-e1.md",
        "title": "Your first workflow run (E1 path)",
        "level": "Beginner → Intermediate",
        "part": "Part II — Operator core",
        "svg": "05-e1-operator-path.svg",
        "time": "60 min",
        "objectives": [
            "Complete the full E1 path end-to-end",
            "Supply required payload (case_id) for flagship workflow",
            "Observe run states and terminal completion",
        ],
        "outline": [
            "What E1 proves (product bar)",
            "Flagship workflow wf_customer_onboarding_v12",
            "Step-by-step UI path: list → run → approve → complete → improve",
            "API equivalent curl sequence",
            "Reading run events / console",
            "Common failures: missing case_id, wrong role, demoMode mocks",
            "Automated proof: test_e1_operator_path.py",
        ],
        "labs": [
            "Lab E1-UI: complete path in browser",
            "Lab E1-API: login + run via API with token",
            "Lab E1-Test: run e2e test and read assertion names",
        ],
        "sources": [
            "docs/usage.md",
            "reviews/e1_operator_checklist.md",
            "backend/app/tests/e2e/test_e1_operator_path.py",
            "EXECUTABLE_PRODUCT.md",
        ],
    },
    {
        "id": "06",
        "file": "06-approvals-risk-audit.md",
        "title": "Approvals, risk tiers, and audit",
        "level": "Intermediate",
        "part": "Part II — Operator core",
        "svg": "06-governance-gates.svg",
        "time": "45 min",
        "objectives": [
            "Decide when a step needs human approval",
            "Approve/reject with rationale and find audit trail",
            "Connect risk tiers R0–R4 to operator behavior",
        ],
        "outline": [
            "Risk tier model and irreversible actions",
            "Approvals queue UX and decision panel",
            "Audit logs: what is recorded (who, when, decision, tool_effects)",
            "request_id for support / debugging",
            "Governance artifacts under business/governance/",
            "Rules: 60-human-approval, 90-governance-risk",
        ],
        "labs": [
            "Force a billing gate and approve as reviewer",
            "Find the matching audit log entry",
            "Reject once and observe run outcome",
        ],
        "sources": [
            "docs/governance.md",
            "docs/security.md",
            "business/governance/",
            "rules/60-human-approval.md",
        ],
    },
    {
        "id": "07",
        "file": "07-agents-tools-rbac.md",
        "title": "Agents, tools, and RBAC",
        "level": "Intermediate",
        "part": "Part II — Operator core",
        "svg": "07-agents-tools.svg",
        "time": "45 min",
        "objectives": [
            "Create or inspect an agent with allowed_tools",
            "Explain why tools outside allow-list fail",
            "Map roles to permissions on key screens",
        ],
        "outline": [
            "Agent record fields and statuses",
            "Tool adapters catalog (ops tools + video stubs)",
            "Allow-list enforcement at runtime",
            "RBAC permissions types",
            "API keys vs user sessions",
            "ALC / lessons attachment to agents (preview of ch14)",
        ],
        "labs": [
            "Create an agent via UI form (live mode)",
            "Attempt a tool not on allow-list (expect controlled failure)",
            "Compare admin vs operator visible nav items",
        ],
        "sources": [
            "docs/agents.md",
            "frontend/src/types/permissions.ts",
            "backend/app/infrastructure/tools/",
        ],
    },
    {
        "id": "08",
        "file": "08-domain-packs-and-recommend.md",
        "title": "Domain packs and recommend workflow",
        "level": "Intermediate",
        "part": "Part III — Domains & video pack",
        "svg": "08-domain-recommend.svg",
        "time": "60 min",
        "objectives": [
            "Explain what a domain pack is and where video pack lives",
            "Submit a free-text brief and read ranked DNA recommendation",
            "Distinguish selection helper from live media generation",
        ],
        "outline": [
            "Domain pack anatomy: manifest, agents, workflows DNA, corpus",
            "Video pack inventory (114 agents, A–J archetypes)",
            "Recommend API + UI panel walkthrough",
            "Scale S1–S5 and confidence interpretation",
            "Hitl_confirm_required before launch",
            "Run viral-hook DNA after recommend (optional advanced lab)",
            "Residuals: production_ready flags, live Sora/Veo not claimed",
        ],
        "labs": [
            "UI: Domains → brief '15s viral TikTok hook' → assert dna_id A",
            "CLI: scripts/business/recommend_video_workflow.py same brief",
            "API: POST recommend-workflow with auth",
        ],
        "sources": [
            "docs/domain-packs.md",
            "docs/add-domain-pack-runbook.md",
            "business/video/",
            "backend/app/domain/workflows/archetype_selector.py",
            "EXECUTABLE_PRODUCT.md",
        ],
    },
    {
        "id": "09",
        "file": "09-special-skills-catalog.md",
        "title": "Special skills catalog",
        "level": "Intermediate",
        "part": "Part III — Domains & video pack",
        "svg": "09-special-skills.svg",
        "time": "40 min",
        "objectives": [
            "List 17 special skills from real REGISTRY, not demo rows",
            "Read skill status/score fields from API/UI",
            "Locate integration.json + SKILL.md on disk",
        ],
        "outline": [
            "Why special skills exist (host MVP bind of pack capabilities)",
            "REGISTRY.json schema and skill_count=17",
            "API GET /domains/video/special-skills",
            "UI SpecialSkillsPanel behavior (demo off)",
            "Scorecard honesty (harsh scores vs inflated 100s)",
            "What 'mvp_integrated' means vs production canary",
        ],
        "labs": [
            "Open Domains special skills table; count rows = 17",
            "Pick one skill_id; open business/video/special_skills/<id>/",
            "Call GET special-skills with token; compare ids",
        ],
        "sources": [
            "business/video/special_skills/REGISTRY.json",
            "special_skill_impl_score.md",
            "backend/app/runtime.py list_video_special_skills",
        ],
    },
    {
        "id": "10",
        "file": "10-workflow-dna-deep-dive.md",
        "title": "Workflow DNA deep dive",
        "level": "Intermediate → Advanced",
        "part": "Part III — Domains & video pack",
        "svg": "10-workflow-dna.svg",
        "time": "60 min",
        "objectives": [
            "Read a .dna.json file and explain each major field",
            "Describe sandbox → evaluate → canary → promote",
            "Locate viral-hook DNA and customer onboarding DNA",
        ],
        "outline": [
            "DNA as executable process graph (not free-form chat)",
            "Step structure: agent, tools, action_type, memory, verification",
            "Human gates and risk metadata",
            "Versioning and promote rules",
            "Validation commands business:validate / evolution checks",
            "Authoring checklist before production",
        ],
        "labs": [
            "Diff two DNA files (onboarding vs viral-hook)",
            "Run DNA schema/validation tests if available",
            "Sketch a 3-step DNA for a toy process on paper",
        ],
        "sources": [
            "docs/workflow-dna.md",
            "rules/100-evolution-sandbox.md",
            "business/video/workflows/",
            "skills workflow-dna",
        ],
    },
    {
        "id": "11",
        "file": "11-knowledge-and-memory.md",
        "title": "Knowledge and memory",
        "level": "Advanced",
        "part": "Part IV — Intelligence & improvement",
        "svg": "11-knowledge-memory.svg",
        "time": "50 min",
        "objectives": [
            "Choose Tier 0 vs Tier 1 retrieval for a query",
            "Browse knowledge and memory surfaces in UI",
            "Explain provenance and retention concerns",
        ],
        "outline": [
            "Tiered retrieval policy",
            "K1-lite graph operators and federation export",
            "Memory scopes: episodic, semantic, procedural, evaluation",
            "UI /app/knowledge and /app/memory",
            "APIs knowledge search / graph / federate",
            "Provenance and retention policy links",
        ],
        "labs": [
            "Run a knowledge search from UI or API",
            "Inspect business/knowledge-base structure",
            "Read retrieval-tier-policy.md",
        ],
        "sources": [
            "docs/knowledge-memory.md",
            "business/knowledge-base/",
            "docs/self-improvement-and-orchestration.md",
        ],
    },
    {
        "id": "12",
        "file": "12-process-intelligence.md",
        "title": "Process intelligence",
        "level": "Advanced",
        "part": "Part IV — Intelligence & improvement",
        "svg": "12-pi-evolution.svg",
        "time": "45 min",
        "objectives": [
            "Ingest or view process intelligence artifacts",
            "Read discovered process, conformance, bottlenecks",
            "Connect PI findings to improvement hypotheses",
        ],
        "outline": [
            "Why PI exists (mine reality, not assumed process)",
            "Artifact locations under business/process-intelligence/",
            "UI Processes surface",
            "APIs under /processes",
            "From bottleneck to sandbox variant proposal",
        ],
        "labs": [
            "Open Processes page; note available summaries",
            "Inspect a PI JSON artifact on disk",
            "Write one causal hypothesis from a bottleneck",
        ],
        "sources": [
            "docs/process-intelligence.md",
            "business/process-intelligence/",
            "rules/80-process-intelligence.md",
        ],
    },
    {
        "id": "13",
        "file": "13-evaluation-and-evolution.md",
        "title": "Evaluation and evolution sandbox",
        "level": "Advanced",
        "part": "Part IV — Intelligence & improvement",
        "svg": "12-pi-evolution.svg",
        "time": "60 min",
        "objectives": [
            "Run or interpret golden/regression/adversarial evals",
            "Use Evolution archive UI",
            "State promote rules and rollback expectation",
        ],
        "outline": [
            "Eval corpus layout business/evals/",
            "Fitness and archive concepts",
            "UI /app/evolution",
            "Canary promotion and versioned DNA",
            "npm run business:eval and evolution:check",
            "What not to do: mutate production DNA in place",
        ],
        "labs": [
            "Open Evolution archive page",
            "List golden tasks count (≥20 product bar)",
            "Trace one successful variant JSON if present",
        ],
        "sources": [
            "docs/evaluation.md",
            "docs/evolution-sandbox.md",
            "business/evals/",
            "business/evolution/",
        ],
    },
    {
        "id": "14",
        "file": "14-self-improvement-loops.md",
        "title": "Self-improvement and loops",
        "level": "Advanced",
        "part": "Part IV — Intelligence & improvement",
        "svg": "13-self-improve.svg",
        "time": "50 min",
        "objectives": [
            "Run Improve pipeline steps on a completed run",
            "Locate lessons-learned artifacts",
            "Explain stop/continue criteria for loop DNA",
        ],
        "outline": [
            "Closed loop: observe → verify → iterate",
            "UI Improve: Reflect → Propose → Evaluate → Canary",
            "APIs improvement/* and loops/*",
            "Lesson library quality controls",
            "Auto-propose sandbox variants",
            "Link to self-evolving agent literature (docs mapping)",
        ],
        "labs": [
            "On a completed E1 run, execute Reflect",
            "GET improvement/lessons",
            "Read one lesson file under business/evolution/lessons-learned/",
        ],
        "sources": [
            "docs/self-improvement-and-orchestration.md",
            "docs/usage.md (API table)",
            "backend/app/infrastructure/self_improvement/",
        ],
    },
    {
        "id": "15",
        "file": "15-backend-runtime-and-apis.md",
        "title": "Backend runtime and APIs",
        "level": "Expert",
        "part": "Part V — Expert & production",
        "svg": "02-system-overview.svg",
        "time": "75 min",
        "objectives": [
            "Locate runtime entry points and route modules",
            "Authenticate and call core APIs with request_id awareness",
            "Explain store backends (Postgres vs JSON)",
        ],
        "outline": [
            "app.main and middleware",
            "RuntimeServices responsibilities",
            "Route map: auth, workflows, runs, approvals, domains, improvement…",
            "OpenAPI export",
            "Workers and long jobs (if any)",
            "Testing pyramid: unit vs e2e",
            "Reading tool_effects and runtime.json snapshot",
        ],
        "labs": [
            "Export or open OpenAPI; find recommend-workflow",
            "Trace recommend_video_workflow in runtime.py",
            "Run targeted pytest for special skills + archetype",
        ],
        "sources": [
            "backend/README.md",
            "backend.md / book/design_phase/book.backend_hk.md",
            "backend/app/api/v1/routes/",
            "backend/app/runtime.py",
        ],
    },
    {
        "id": "16",
        "file": "16-frontend-deep-dive.md",
        "title": "Frontend deep dive",
        "level": "Expert",
        "part": "Part V — Expert & production",
        "svg": "04-console-map.svg",
        "time": "60 min",
        "objectives": [
            "Explain client auth cookie and live-data facade",
            "Wire a new panel to backendApi safely",
            "Keep demoMode opt-in only",
        ],
        "outline": [
            "App shell, sidebar, slug router",
            "backendApi client patterns",
            "product-data demo vs live",
            "Forms: Zod + RHF + formatMutationError",
            "Improve pipeline and evolution panels",
            "Vitest + Playwright smoke",
            "Adding Domains-style features without forking architecture",
        ],
        "labs": [
            "Read client.ts recommend + special skills methods",
            "Run frontend unit product-slice tests",
            "Trace env.demoMode default in env.ts",
        ],
        "sources": [
            "frontend/README.md",
            "frontend/src/lib/api/client.ts",
            "frontend/src/lib/config/env.ts",
            "frontend/docs/api/frontend-api-contract.md",
        ],
    },
    {
        "id": "17",
        "file": "17-extend-dna-agents-packs.md",
        "title": "Extend DNA, agents, and packs",
        "level": "Expert",
        "part": "Part V — Expert & production",
        "svg": "14-extend-pack.svg",
        "time": "90 min",
        "objectives": [
            "Scaffold a minimal domain pack or DNA extension",
            "Register tools and allow-list agents correctly",
            "Prove with golden task + inventory check",
        ],
        "outline": [
            "When to extend pack vs host",
            "Manifest and versioning matrix",
            "Agent JSON + DNA authoring steps",
            "Tool adapter stub pattern",
            "inventory_check and corpus standalone checks",
            "Anti-patterns: second control plane, rubber-stamp scores",
        ],
        "labs": [
            "Study example_education or example_research pack",
            "Draft a one-page design for your pack",
            "Run inventory_check on video pack for reference",
        ],
        "sources": [
            "docs/add-domain-pack-runbook.md",
            "docs/domain-pack-versioning-matrix.md",
            "business/example_education/",
            "scripts/business/",
        ],
    },
    {
        "id": "18",
        "file": "18-security-ops-troubleshooting.md",
        "title": "Security, ops, and troubleshooting",
        "level": "Expert",
        "part": "Part V — Expert & production",
        "svg": "15-security-production.svg",
        "time": "60 min",
        "objectives": [
            "Apply a production readiness checklist",
            "Diagnose common boot and run failures",
            "Apply agentic security basics (tool abuse, prompt injection awareness)",
        ],
        "outline": [
            "Auth hardening beyond seed passwords",
            "Secrets, CORS, security headers",
            "Postgres runbook essentials",
            "Doctor / security scripts",
            "Troubleshooting matrix (symptom → check)",
            "Incident: approval bypass attempts",
        ],
        "labs": [
            "Run npm run doctor and record output",
            "Break health with wrong DATABASE_URL; restore",
            "Walk rules/110-agentic-security.md highlights",
        ],
        "sources": [
            "docs/security.md",
            "docs/troubleshooting.md",
            "backend/docs/postgres-runbook.md",
            "rules/30-security.md",
            "rules/110-agentic-security.md",
        ],
    },
    {
        "id": "19",
        "file": "19-expert-playbooks-and-checklists.md",
        "title": "Expert playbooks and checklists",
        "level": "Expert",
        "part": "Part V — Expert & production",
        "svg": "01-learning-path.svg",
        "time": "40 min + ongoing",
        "objectives": [
            "Use role-based daily/weekly checklists",
            "Know where design-phase books fit as deep reference",
            "Define personal mastery criteria",
        ],
        "outline": [
            "Operator daily checklist",
            "Pack author release checklist",
            "Platform SRE weekly checklist",
            "Mastery rubric (can teach E1, recommend, promote rules)",
            "Where to go next: structure.md, design_phase books, gap analyses",
            "Appendix pointers (glossary, API cheat sheet, command cheat sheet)",
        ],
        "labs": [
            "Complete mastery self-score (1–5) per rubric row",
            "Write one playbook for your org's top workflow",
        ],
        "sources": [
            "reviews/e1_operator_checklist.md",
            "mark_100_verification.md",
            "book/design_phase/",
            "planning/user_guide/TOC.md",
        ],
    },
    {
        "id": "A",
        "file": "A-glossary.md",
        "title": "Appendix A — Glossary",
        "level": "Reference",
        "part": "Appendices",
        "svg": None,
        "time": "ref",
        "objectives": ["Look up any term used in the guide"],
        "outline": [
            "Agent, ALC, approval, archetype, audit, bootstrap",
            "Canary, conformance, DNA, domain pack, demoMode",
            "E1, evolution, federation, fitness, gate",
            "Harness, inventory, K1-lite, lesson, loop DNA",
            "Memory scopes, N1, PI, provenance, RBAC",
            "Runtime, special skill, tool_effects, viral-hook",
        ],
        "labs": [],
        "sources": ["This guide + docs/*"],
    },
    {
        "id": "B",
        "file": "B-command-and-api-cheatsheet.md",
        "title": "Appendix B — Commands and API cheat sheet",
        "level": "Reference",
        "part": "Appendices",
        "svg": None,
        "time": "ref",
        "objectives": ["Copy-paste bootstrap, run, eval, and key API calls"],
        "outline": [
            "npm scripts table",
            "Backend uvicorn and pytest",
            "Frontend pnpm",
            "Auth login curl",
            "Recommend + special-skills curl",
            "Improvement APIs",
        ],
        "labs": [],
        "sources": ["docs/usage.md", "package.json", "frontend/.env.example"],
    },
    {
        "id": "C",
        "file": "C-troubleshooting-matrix.md",
        "title": "Appendix C — Troubleshooting matrix",
        "level": "Reference",
        "part": "Appendices",
        "svg": None,
        "time": "ref",
        "objectives": ["Jump from symptom to fix"],
        "outline": [
            "Backend won't start",
            "ready degraded",
            "Login fails",
            "UI shows demo mocks",
            "Domains missing from sidebar",
            "Recommend empty / mock",
            "Approval stuck",
            "Inventory check fail",
        ],
        "labs": [],
        "sources": ["docs/troubleshooting.md", "ch03, ch05, ch08"],
    },
]


def chapter_md(c: dict) -> str:
    svg_block = ""
    if c["svg"]:
        title = c["title"]
        svg = c["svg"]
        svg_block = (
            f"\n## Illustration\n\n"
            f"![{title}](../assets/{svg})\n\n"
            f"*Figure: {title} — source `assets/{svg}`*\n"
        )
    objectives = "\n".join(f"- {o}" for o in c["objectives"])
    outline = "\n".join(f"{i}. {s}" for i, s in enumerate(c["outline"], 1))
    labs = (
        "\n".join(f"- [ ] {lab}" for lab in c["labs"])
        if c["labs"]
        else "_No lab (reference appendix)._"
    )
    sources = "\n".join(f"- `{s}`" for s in c["sources"])

    return f"""# Chapter {c['id']}: {c['title']}

> **Status:** SCAFFOLD in `book/user_guide/` — expand to full prose in place  
> **Level:** {c['level']}  
> **Part:** {c['part']}  
> **Est. time:** {c['time']}  
> **Path:** `book/user_guide/chapters/{c['file']}`

{svg_block}

## Learning objectives

{objectives}

## Narrative outline (to expand into full prose)

{outline}

## Hands-on labs

{labs}

## Primary sources (do not invent beyond these without verifying)

{sources}

## Writing checklist (for full draft)

- [ ] Open with 1-paragraph “why this matters”
- [ ] Step-by-step commands that work on Windows PowerShell and bash where possible
- [ ] At least one “Expected result” block per major lab
- [ ] Explicit residual / non-claim callouts where relevant
- [ ] Cross-links to previous/next chapter
- [ ] Keep SVG embed pointing at `../assets/` (this folder is the publish home)

## Navigation

- TOC: [../TOC.md](../TOC.md)
- Master: [../user_guide.md](../user_guide.md)
- Plan: [../../../planning/user_guide/00_PLAN.md](../../../planning/user_guide/00_PLAN.md)
"""


def main() -> None:
    for c in CHAPTERS:
        path = CH / c["file"]
        path.write_text(chapter_md(c), encoding="utf-8")
    print(f"wrote {len(CHAPTERS)} chapters -> {CH}")


if __name__ == "__main__":
    main()
