---
name: book-creator
description: >
  Create professional, deep technical books and progressive user guides (English +
  Traditional Chinese) with per-chapter Markdown, hand-crafted SVG diagrams, and
  grounded repo evidence. Use when the user runs /book-creator, mentions create_user_guide,
  book/user_guide, design-phase monographs, "write the user guide", "create technical book",
  or needs book-quality documentation that is not thin scaffold. Quality bar: design_phase
  monographs and Opus-grade user_guide chapters (~500–800 lines each), never outline stubs.
---

# Book Creator Skill

Turn a brief (e.g. `create_user_guide.md`) plus **repository source of truth** into a
**self-contained book** under a target folder. This skill exists because thin, template-only
guides fail the project quality bar. Successful output matches the depth of
`book/design_phase/` monographs and the Opus-produced `book/user_guide/` set.

---

## 0. Why thin guides fail (study this before writing)

### Failure mode (rejected quality)

| Symptom | What went wrong |
|--------|------------------|
| Chapters ~80–200 lines | Outline + filler, not teachable content |
| Generic “install Node.js” text | Not grounded in *this* repo’s commands, paths, DNA IDs |
| SVG as decorative boxes | No labels of real layers, agents, APIs, or flows |
| “Best practices” as 3 bullet platitudes | No good/bad code, no validation commands |
| Use cases as one-line scenarios | No step mapping to layers/workflows/outcomes |
| HK files as partial gloss | Not full parallel chapters |
| Invented APIs / fake paths | Reader cannot execute; trust collapses |

### Success mode (accepted quality — measured from Opus `book/user_guide`)

| Metric | Target |
|--------|--------|
| EN chapters | 3–5 per section × 5 sections ≈ 15–25 chapters |
| Lines per EN chapter | **≥ 480** (typical 550–780) |
| Chars per EN chapter | **≥ 22,000** |
| SVG per chapter | **≥ 1** substantive diagram (≈4–10 KB), not a 200-byte placeholder |
| Use cases | **3** per chapter with Scenario → How the system handles it → Result |
| Quiz | **5–8** questions with `<details>` answers |
| HK chapters | **1:1** with EN, Traditional Chinese (Hong Kong technical register) |
| Grounding | Real paths, npm scripts, API routes, workflow IDs, folder trees from repo |

**Hard rule:** If a chapter is under ~450 lines or lacks runnable commands + three use cases +
quiz, it is **not done**. Expand from source; do not ship the stub.

---

## 1. Inputs and authority order

### 1.1 Brief (required)

Read the user’s creation brief first (examples in this repo):

- `create_user_guide.md` — progressive user guide, 5 sections, chapters + SVG + QA
- `book/design_phase/create_book.txt` — architecture monograph + HK + script variants

Obey the brief’s phases, folder layout, naming, and bilingual requirements **without
downgrading depth**.

### 1.2 Source corpus (read before drafting any chapter)

Read **in this order**; prefer primary sources over secondary summaries:

1. **Architecture spine:** `structure.md`, `docs/architecture.md`, `docs/business-architecture.md`
2. **Product honesty:** `EXECUTABLE_PRODUCT.md`, `README.md`, `status.md` / `tasks.md` if present
3. **Layer docs:** `docs/workflow-dna.md`, `docs/governance.md`, `docs/security.md`,
   `docs/process-intelligence.md`, `docs/knowledge-memory.md`, `docs/evolution-sandbox.md`,
   `docs/evaluation.md`, `docs/installation.md`, `docs/usage.md`, `docs/troubleshooting.md`
4. **Code truth:** `backend/app/main.py`, runtime/routes under `backend/app/api/`,
   `frontend/src/app/` routes, `package.json` scripts, `business/` tree layouts
5. **Reference monographs (quality few-shots):** `book/design_phase/book.md` and siblings
6. **Prior good user guide (style few-shot):** `book/user_guide/chapters/*.md` when regenerating
   or extending — **copy structure and density, not stale facts**

**Never invent** endpoints, CLI flags, DNA IDs, or folder names. If unknown, open the file
or run a read-only listing; if still unknown, write “verify in repo” and cite the nearest
real artifact.

### 1.3 Design priorities (always restate where relevant)

```
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned; evolution never mutates production directly.

---

## 2. Execution phases (do not skip)

### Phase A — TOC & learning map

1. Design 5 progressive sections (or the brief’s section set).
2. Each section: **3–5** chapters with sequential dependence.
3. For every chapter, draft **before writing body**:
   - Title + slug `SS-CC-kebab-title`
   - 5–7 learning objectives
   - Prerequisites (prior chapters + env)
   - Primary sources to open (file paths)
   - Diagram type needed (architecture / flowchart / sequence / matrix)
4. Write `book/<target>/README.md` with full TOC tables and section objectives.
5. Stop and sanity-check: beginner → intermediate → advanced → troubleshoot → scale.

### Phase B — Deep chapter drafting (one chapter at a time)

For each chapter file `book/<target>/chapters/SS-CC-slug.md`:

1. Open listed sources; extract real IDs, commands, trees, schemas.
2. Write the **full** chapter using §3 skeleton (no placeholders like “TBD” or “add steps later”).
3. Embed diagram: `![Alt](../assets/SS-CC-descriptive-name.svg)` near the top.
4. Self-score against §6 rubric; expand until pass.
5. Only then start the next chapter.

### Phase C — SVG per chapter

1. Create one primary SVG matching the chapter’s central mental model.
2. Use §4 SVG few-shot style (fixed viewBox, semantic colors, real labels).
3. File name aligns with chapter: `assets/SS-CC-descriptive-name.svg`.

### Phase D — Traditional Chinese (`_hk.md`)

1. Full parallel file per EN chapter + `README_hk.md`.
2. Rules in §5. Not machine gloss of first 20 lines.

### Phase E — Compilation QA

1. Broken-link check for all `](../` and `](chapters/` references.
2. Every EN chapter has SVG + HK twin.
3. Spot-check 3 random technical claims against source files.
4. Confirm depth metrics (line counts) meet §0 success mode.
5. README is the only required entry point for readers.

**Output layout (user guide default):**

```text
book/user_guide/
├── README.md
├── README_hk.md
├── chapters/
│   ├── 01-01-system-overview.md
│   ├── 01-01-system-overview_hk.md
│   └── ...
└── assets/
    ├── 01-01-system-architecture.svg
    └── ...
```

---

## 3. Mandatory chapter skeleton

Every chapter **must** contain these sections in order (titles may vary slightly by genre,
but content obligations do not).

```markdown
# Chapter SS-CC: <Title>

![<Descriptive alt>](../assets/SS-CC-<diagram-slug>.svg)

## Learning Objectives
## Prerequisites
## <Concept / architecture body — majority of chapter>
## <Step-by-step hands-on — numbered, with commands + expected outcomes>
## Real-World Use Cases   # exactly 3
## Best Practices         # actionable; prefer good vs bad examples
## Chapter Summary
## Knowledge Check Quiz   # 5–8 items, answers in <details>
```

### 3.1 Section obligations

| Section | Obligation |
|---------|------------|
| Learning objectives | 5–7 numbered, verb-led (“Create…”, “Explain…”, “Validate…”) |
| Prerequisites | Prior chapters + concrete env (running backend, `business/` access, etc.) |
| Concept body | Tables, field glossaries, layer maps, **artifact locations** (`business/...`) |
| Steps | Numbered; `bash`/`yaml`/`json` blocks; **expected output** or failure modes |
| Use cases | Scenario + multi-step system mapping + business Result/Value |
| Best practices | ≥ 6 items; include anti-patterns where relevant |
| Summary | Bullets restating only what the chapter taught |
| Quiz | Multiple choice; correct answer + 1–3 sentence rationale in `<details>` |

### 3.2 Callout conventions

```markdown
> **Tip:** Shortcut or proven practice.
> **Warning:** Safety / irreversibility / production mutation risk.
> **Note:** Extra context that is not a hard constraint.
```

Use **Warning** for: production mutation, irreversible tools, demoMode traps, missing gates.

### 3.3 Formatting conventions

| Convention | Use |
|------------|-----|
| `monospace` | Paths, commands, IDs, JSON keys, env vars |
| **Bold** | UI labels, critical terms on first use |
| Tables | Comparisons, tiers, field glossaries, component maps |
| ` ```yaml ` / ` ```bash ` / ` ```json ` / ` ```text ` | Schemas, CLIs, payloads, trees |
| Relative SVG path | Always `../assets/...` from `chapters/` |

---

## 4. Few-shot patterns (copy density and structure)

These excerpts are **style exemplars** distilled from accepted Opus output. When writing a
new chapter, match this density of specificity — not the exact domain text if the topic differs.

### 4.1 FEW-SHOT: Opening + objectives + grounded definition

```markdown
# Chapter 01-01: System Overview

![System Architecture](../assets/01-01-system-architecture.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Describe the six-layer architecture of the Generic Swarm Business Operating System
2. Explain the design priority hierarchy (Safety > Auditability > Correctness > Efficiency > Autonomy)
3. Identify the core concepts: Workflow DNA, bounded autonomy, sandbox evolution, and provenance
4. Understand how the Intake Router and Business Orchestrator coordinate work
5. Map each architectural layer to its corresponding role in the system
6. Articulate why autonomy is earned through evidence rather than granted by default

## Prerequisites

- Basic understanding of software architecture concepts (layers, services, APIs)
- Familiarity with multi-agent systems (helpful but not required)
- Access to a cloned copy of the `generic-swarm-ops` repository

---

## 1. What Is the Generic Swarm Business Operating System?

The Generic Swarm Business Operating System is a governed, self-improving multi-agent system
designed to:

1. **Learn** how a business actually operates -- from documents, experts, AND real event logs
2. **Distill** that knowledge into reusable rules, skills, workflows, and playbooks
3. **Execute** work through bounded, auditable agent workflows
4. **Evolve** those workflows in a sandbox -- never directly in production

> **Note:** This is not a chatbot or a simple automation tool. It is a complete operating
> system for business processes, with built-in governance, security, and self-improvement
> capabilities.
```

**Why this works:** Objectives are testable; definition is product-specific; callout kills
wrong mental model immediately.

### 4.2 FEW-SHOT: Concept table + artifact location (not abstract prose only)

```markdown
### 3.5 Governance Layer

**Purpose:** Apply risk tiers, approval rules, and audit requirements to all operations.

**Autonomy Risk Tiers:**

| Tier | Autonomy Level | Allowed Behavior |
|---|---|---|
| 0 | Observe | Log and summarize only |
| 1 | Recommend | Suggest; human acts |
| 2 | Draft | Prepare artifacts; human approves before send/execute |
| 3 | Execute (reversible) | Act if rollback exists and risk is low |
| 4 | Execute + gate | Act, but human approves the critical step |
| 5 | Restricted | No autonomous action until an assurance case exists |

**Artifact location:** `business/governance/`
```

**Why this works:** Reader can act (open the folder) and reason (tier table) without leaving the page.

### 4.3 FEW-SHOT: Schema teaching with running example + field glossary

```markdown
## The Workflow DNA Schema

Every production Workflow DNA must declare the following components. Walk through each one
using the flagship `wf_customer_onboarding_v12` as the running example.

### 1. Identity and Metadata

```yaml
workflow_dna:
  id: "wf_customer_onboarding_v12"
  name: "Customer Onboarding"
  domain: "operations"
  objective: "Onboard customer with minimal delay and compliance risk."
  owner: "business_orchestrator"
  version: "12.0"
```

| Field | Purpose | Example |
|-------|---------|---------|
| `id` | Unique identifier with version suffix | `wf_customer_onboarding_v12` |
| `name` | Human-readable name | `Customer Onboarding` |
| `domain` | Business domain classification | `operations`, `legal`, `finance` |
| `objective` | What the workflow achieves | Natural language goal |
| `owner` | Orchestrating agent | `business_orchestrator` |
| `version` | Change tracking | `12.0` |

> **Tip:** Encode version in the ID so audit logs and evolution history stay unambiguous.
```

**Why this works:** One real DNA ID anchors the whole chapter; tables turn YAML into operable knowledge.

### 4.4 FEW-SHOT: Step-by-step with validation commands (not “configure as needed”)

```markdown
### Step 10: Validate the Workflow

```bash
npm run business:validate
```

The validator checks for:

- All high-risk actions have human gates
- All irreversible actions have rollback plans
- Provenance is declared for all memory writes
- Audit log write is required
- All referenced tools exist in the tool registry
- All referenced agents exist in the agent roster

```bash
npm run business:evolution:check
```

This second command verifies Evolution Engine sandbox compatibility.
```

**Why this works:** Commands are real project scripts; checklist matches enforcement narrative.

### 4.5 FEW-SHOT: Runtime walkthrough with intermediate state

```markdown
### 2. Runtime Walks the Graph

```text
Step 1: verify_contract
  Agent: governance_officer
  Tools: contract_parser, policy_retriever
  Result: contract verified, no exceptions
  tool_effects: [parse_result, policy_check_result]

Step 3: configure_billing
  Agent: tool_permission_broker
  Tools: billing_system
  ** HUMAN GATE TRIGGERED ** (irreversible action)
  Waiting for reviewer approval...
```

### 5. Tool Effects Tracking

```json
{
  "step_id": "create_customer_record",
  "tool": "crm",
  "action": "create",
  "input": {"name": "Acme Corp", "type": "enterprise"},
  "output": {"id": "cust_456", "status": "active"},
  "timestamp": "2026-07-06T14:05:22Z",
  "reversible": true,
  "rollback_action": "disable_customer_record"
}
```
```

**Why this works:** Shows pause points and audit artifacts the operator will actually see.

### 4.6 FEW-SHOT: Use case block (repeat ×3)

```markdown
### Use Case 1: Automated Customer Onboarding

**Scenario:** A B2B SaaS company needs to onboard enterprise customers with compliance
checks, contract verification, billing setup, and welcome communications.

**How the system handles it:**

1. **Process Intelligence** mines historical onboarding event logs
2. **Knowledge** stores contract rules, exceptions, and past failures
3. **Workflow DNA** `wf_customer_onboarding_v12` bounds the steps and tools
4. **Governance** enforces a human gate when `risk_tier` is high or exceptions appear
5. **Evolution** improves cycle time only via sandbox → canary → promote

**Result:** Onboarding drops from days to hours with full compliance auditability.
Human experts intervene only for genuinely complex cases.
```

**Why this works:** Maps a business story onto *named layers and IDs*, not generic “AI helps”.

### 4.7 FEW-SHOT: Best practice with anti-pattern

```markdown
### 3. Use Specific Tool Lists

Never give an agent tools it does not need for its step:

```yaml
# Bad: too many tools
- id: "send_email"
  agent: "business_orchestrator"
  tools: ["email", "crm", "billing", "audit"]

# Good: least privilege
- id: "send_email"
  agent: "business_orchestrator"
  tools: ["email"]
```
```

### 4.8 FEW-SHOT: Knowledge check with collapsible answer

```markdown
**Question 1:** What is the correct ordering of design priorities?

a) Autonomy > Efficiency > Correctness > Auditability > Safety
b) Safety > Auditability > Correctness > Efficiency > Autonomy
c) Correctness > Safety > Efficiency > Auditability > Autonomy
d) Safety > Correctness > Auditability > Autonomy > Efficiency

<details>
<summary>Answer</summary>
<b>b)</b> Safety > Auditability > Correctness > Efficiency > Autonomy.
Autonomy is always the lowest priority and must be earned through evidence.
</details>
```

**Why this works:** Quiz tests chapter-specific claims; rationale teaches, not only scores.

### 4.9 FEW-SHOT: Troubleshooting chapter pattern

For Section 4 chapters, prefer **error category → symptoms → diagnosis commands → fix →
prevention**:

```markdown
### 3.1 Health Endpoint Shows No Postgres

**Symptoms:** `GET /api/v1/health/ready` omits `"database": "postgres"` or returns degraded status.

**Diagnose:**

```bash
curl http://127.0.0.1:8000/api/v1/health/ready
# Inspect DATABASE_URL / Postgres container / migrate status
```

**Fix:** Ensure Postgres is reachable, migrations applied, and runtime can open `runtime_state`.

**Prevent:** Health-check before any flagship run; treat JSON-file-only mode as recovery, not prod.
```

### 4.10 ANTI-FEW-SHOT: Reject this shape

```markdown
# Chapter 1.1 System Overview

## Learning Objectives
- Understand the system

## Overview
Generic Swarm is a multi-agent platform that helps businesses automate work.

## Steps
1. Install dependencies
2. Configure the system
3. Start using features

## Summary
You learned about the system.
```

**Reject reasons:** No depth, no repo evidence, no use cases, no quiz, no diagram, no commands,
no failure modes. This is the quality that users discard.

---

## 5. SVG creation standard

### 5.1 Technical requirements

- Root: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H" font-family="Segoe UI, Arial, sans-serif">`
- Typical size: **960×620** to **960×700**
- White background rect; high-contrast text (`#0f172a` on white)
- Semantic fills (examples): indigo execution/orchestrator, green process intelligence,
  blue knowledge, violet evolution, fuchsia governance, red security/guardrails, slate neutrals
- Rounded rects `rx="8"`, readable 11–15px labels, subtitle under title
- Real system nouns: layer names, agent roles, step IDs, pipeline stages — **not** “Box A / Box B”
- Arrow group with marker for flow direction
- No external images, no scripts, no tiny illegible text walls

### 5.2 FEW-SHOT SVG fragment (architecture)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 700" font-family="Segoe UI, Arial, sans-serif">
  <rect width="960" height="700" fill="#ffffff"/>
  <text x="480" y="34" text-anchor="middle" font-size="22" font-weight="700" fill="#0f172a">Generic Swarm Business OS - Six-Layer Architecture</text>
  <text x="480" y="58" text-anchor="middle" font-size="12" fill="#64748b">Safety &#8594; Auditability &#8594; Correctness &#8594; Efficiency &#8594; Autonomy</text>
  <!-- Intake / Orchestrator / six layer cards / audit bar / evolution bar / infra bar + arrows -->
</svg>
```

### 5.3 Markdown embed

```markdown
![System Architecture](../assets/01-01-system-architecture.svg)
```

Alt text must describe the diagram’s teaching point (screen-reader + WCAG intent).

---

## 6. Bilingual (Traditional Chinese) standard

### 6.1 Rules

- Filename: same stem + `_hk.md` (e.g. `01-01-system-overview_hk.md`)
- Translate **all** narrative; keep code, paths, CLI, IDs, JSON keys, DNA IDs in original
- Prefer HK/TW technical register (系統、工作流程、審批、沙箱、可審計性)
- Preserve heading hierarchy, tables, callouts (`> **提示：**` / `> **警告：**` / `> **注意：**`)
- Keep SVG embeds identical (shared assets)
- Quiz: translate stems and options; keep `<details>` structure
- Do not leave EN paragraphs mixed in mid-chapter except unavoidable proper nouns

### 6.2 FEW-SHOT HK opening

```markdown
# 第 01-01 章：系統概覽

![System Architecture](../assets/01-01-system-architecture.svg)

## 學習目標

在完成本章後，你將能夠：

1. 描述 Generic Swarm 商業作業系統的六層架構
2. 解釋設計優先層級（安全性 > 可審計性 > 正確性 > 效率 > 自主性）
...
```

### 6.3 Optional script variant

If the brief asks for `*_hk.script.txt` (design_phase style): spoken-words-only Cantonese,
no stage directions, natural listening rhythm — only after HK markdown is complete.

---

## 7. Quality rubric (gate before “done”)

Score each chapter 0–2 on every row. **Ship only if total ≥ 16/20 and no zero rows.**

| # | Criterion | 0 | 1 | 2 |
|---|-----------|---|---|---|
| 1 | Depth | <300 lines | 300–479 | ≥480 |
| 2 | Grounding | Invented paths | Partial real refs | Commands, paths, IDs verified |
| 3 | Steps | Missing / vague | Steps without expected results | Full steps + outcomes + failures |
| 4 | Use cases | 0–1 thin | 2 partial | 3 full Scenario/How/Result |
| 5 | Best practices | Platitudes | Useful list | Anti-patterns + examples |
| 6 | Quiz | None | Few without answers | 5–8 with `<details>` rationales |
| 7 | Diagram | Missing / placeholder | Simple boxes | Labeled semantic SVG |
| 8 | Callouts | None | Sparse | Tip/Warning/Note at real risks |
| 9 | Progressive fit | Orphan advanced jargon | Some bridging | Explicit prerequisites + level fit |
| 10 | HK twin | Missing | Partial | Full parallel chapter |

**Global guide gates:**

- [ ] README TOC links resolve
- [ ] Every chapter SVG path resolves
- [ ] Section order matches brief
- [ ] Design priority hierarchy stated consistently
- [ ] No production-mutation advice that contradicts Evolution rules
- [ ] Demo/opt-in behaviors documented where product honesty requires it (`EXECUTABLE_PRODUCT.md`)

---

## 8. Workflow for the agent (checklist)

```text
[ ] 1. Read brief (create_user_guide.md or equivalent)
[ ] 2. Read structure.md + layer docs + EXECUTABLE_PRODUCT.md
[ ] 3. Sample code: main.py routes, package.json scripts, business/ tree
[ ] 4. Open 1–2 design_phase monographs + 1 accepted user_guide chapter as few-shots
[ ] 5. Write README TOC + learning map
[ ] 6. For each chapter:
[ ]      a. Extract sources for THIS chapter only
[ ]      b. Write full EN chapter (≥480 lines, rubric pass)
[ ]      c. Write matching SVG
[ ]      d. Write full HK twin
[ ] 7. Link/path QA + spot fact-check
[ ] 8. Report: chapter counts, line-count range, any residual risks
```

**Parallelism:** You may draft multiple chapters in parallel **only if** each worker has the
few-shot standards and source list. Never parallelize by generating empty stubs first.

**Token strategy:** Prefer fewer, complete chapters per turn over many incomplete files.
Never mark Phase B complete when files are scaffolds.

---

## 9. Adapting the skill to other book types

| Brief type | Output folder | Spine sources | Extra deliverable |
|------------|---------------|---------------|-------------------|
| User guide (`create_user_guide.md`) | `book/user_guide/` | structure + docs + product + code | Progressive 5 sections |
| Architecture book (`create_book.txt`) | `book/design_phase/` or `book/` | starter/tasks/status/structure/backend/frontend | Optional HK script |
| Backend/frontend monographs | per create_*.txt | matching .md + code tree | Focused SVG set |

Always keep: depth floors, few-shot density, grounding, SVG quality, bilingual rules when asked.

---

## 10. Root-cause summary (Opus vs thin agents)

| Factor | Thin agent behavior | Opus-grade behavior encoded here |
|--------|---------------------|----------------------------------|
| Interpreting the brief | Treats phases as file checklists | Treats phases as **quality gates** with depth floors |
| Source use | Paraphrases high-level README | Mines `structure.md`, DNA, APIs, npm scripts |
| Chapter unit | Outline + filler | Textbook unit: teach → do → apply → check |
| Examples | Hypothetical soft claims | Flagship IDs, curl, YAML, tool_effects JSON |
| Diagrams | Decorative | Cognitive model of the chapter |
| Translation | Afterthought stub | Full pedagogical twin |
| Stop condition | “Files exist” | Rubric ≥ 16/20 + metrics in §0 |

**Instruction to the model:** When unsure whether content is “good enough,” open
`book/user_guide/chapters/01-01-system-overview.md` and compare length, table count, command
count, and quiz depth. Match or exceed that standard for every chapter you emit.

---

## 11. Invocation examples

**User:** “Execute `create_user_guide.md` and write `book/user_guide`.”

**Agent:** Load this skill → Phase A–E → produce full EN+HK+SVG set at Opus depth.

**User:** “Add a new chapter on special skills recommend flow.”

**Agent:** Read FE recommend routes + API + EXECUTABLE_PRODUCT honesty → full chapter skeleton
with steps, three use cases, SVG, quiz, HK twin → update README TOC.

**User:** “Regenerate only Section 4 troubleshooting.”

**Agent:** Re-read troubleshooting docs + real error modes from ops → rewrite 04-xx chapters
to §4.9 pattern without thinning other sections.

---

*Skill distilled from: `create_user_guide.md` (input brief), repository sources
(`structure.md`, `docs/*`, product/code trees), and accepted few-shot corpus
`book/user_guide/**` (Opus-grade) plus density reference `book/design_phase/book.md`.*
