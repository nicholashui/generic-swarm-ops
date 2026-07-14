# Chapter 4.4: Support and Community Resources

![Support Resources Map](../assets/04-04-support-resources-map.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Navigate the complete documentation ecosystem efficiently
2. Use session continuity files (memory/handoff) for agent context
3. Access design phase resources for deep architectural understanding
4. Follow the contribution workflow for bug fixes and features
5. Report issues effectively with proper context
6. Leverage both agent harnesses (Trae IDE and Grok Build) for development support

## Prerequisites

Before working through this chapter, ensure you have:

- The Generic Swarm Ops repository cloned locally
- Familiarity with basic Git operations
- Understanding of the system architecture from Chapter 1.1
- Access to the project's issue tracker

---

## 1. Documentation Ecosystem Overview

Generic Swarm Ops maintains a comprehensive documentation ecosystem organized across multiple directories. Understanding this structure helps you find answers quickly.

### 1.1 Documentation Map

| Directory | Purpose | When to Use |
|-----------|---------|-------------|
| `docs/` | Operational reference | Day-to-day development and troubleshooting |
| `book/` | In-depth learning | Understanding concepts and architecture |
| `memory/` | Session continuity | Starting a new development session |
| `business/` | Living system artifacts | Business OS configuration and state |
| `planning/` | Project plans | Understanding roadmap and priorities |
| `backend/docs/` | Backend-specific guides | Database operations and backend setup |
| `reviews/` | Evaluation checklists | Verifying product completeness |

### 1.2 Documentation Freshness

The documentation is maintained alongside the code. When in doubt about currency:

1. Check the file's `git log` for recent updates:

```bash
git log --oneline -5 docs/troubleshooting.md
```

2. Cross-reference with the actual system behavior:

```bash
# Does the documented command still work?
npm run doctor
```

3. If documentation is stale, file an issue or update it as part of your contribution.

---

## 2. Operational Reference Documents (docs/)

### 2.1 Core Reference Files

The `docs/` directory contains the primary operational references:

**docs/architecture.md**
- Full layered architecture description
- Component relationships and data flows
- System design principles and constraints
- When to read: Understanding how components interact

**docs/installation.md**
- Prerequisites (Node.js 20+, Python 3.11+, PostgreSQL 14+, Git, pnpm)
- Full setup procedure (bootstrap, backend, frontend)
- Environment variable reference
- When to read: Setting up a new development environment

**docs/usage.md**
- All available commands with descriptions
- Backend and frontend startup procedures
- Self-improvement API reference
- Runtime flow documentation
- Business artifact locations
- When to read: Looking up how to run specific operations

**docs/troubleshooting.md**
- Error categories and resolution steps
- Common symptoms and their diagnoses
- Verification commands
- When to read: Something is not working as expected

**docs/self-improvement-and-orchestration.md**
- Self-evolving pipeline details
- Loop runner configuration
- K1-lite knowledge graph
- When to read: Understanding the evolution and self-improvement systems

### 2.2 Harness-Specific Documentation

**docs/trae.md**
- Trae IDE configuration and usage
- Generated `.trae/` directory structure
- Agent configuration for Trae
- When to read: Working within the Trae IDE harness

**docs/grok.md**
- Grok Build configuration and usage
- Generated `.grok/` directory structure
- Migration from other harnesses
- When to read: Working within the Grok Build harness

**docs/sync.md**
- Harness synchronization process
- How `npm run sync` regenerates managed files
- Shared source of truth locations
- When to read: Understanding how harness files are generated

### 2.3 Additional Reference Files

**docs/source-audit.md** (generated)
- Audit results for external sources
- License compliance status
- Integrity verification results
- When to read: After running `npm run sources:audit`

**migrate_to_grok_build.md**
- Step-by-step migration guide
- Configuration differences between harnesses
- When to read: Moving from Trae to Grok Build

---

## 3. In-Depth Learning Resources (book/)

### 3.1 User Guide (book/user_guide/)

The comprehensive user guide (this document) is organized into sections:

```
book/user_guide/
  user_guide.md          # Master document and table of contents
  chapters/              # Individual chapters organized by section
    01-*.md              # Section 1: Core System Fundamentals
    02-*.md              # Section 2: Intermediate Workflows
    03-*.md              # Section 3: Advanced Customization
    04-*.md              # Section 4: Troubleshooting & Support (this section)
  assets/                # SVG diagrams and illustrations
    01-*.svg             # Section 1 diagrams
    02-*.svg             # Section 2 diagrams
    03-*.svg             # Section 3 diagrams
    04-*.svg             # Section 4 diagrams
```

**How to Navigate:**
1. Start with `user_guide.md` for the table of contents
2. Read chapters in order within each section for a learning path
3. Jump to specific chapters when you need targeted help
4. Reference asset SVGs for visual understanding of concepts

### 3.2 Design Phase Resources (book/design_phase/)

The design phase directory contains deep architectural analysis:

```
book/design_phase/
  # Architecture design documents
  # System pattern analysis
  # Design decision records
  # Component interaction models
```

**When to Use:**
- Understanding why the system is designed a certain way
- Reviewing design decisions before proposing changes
- Learning about system patterns used throughout the codebase
- Preparing for architectural discussions

> **Tip:** Design phase documents are more theoretical than operational. Read them when you want to understand the "why" behind the system, not the "how" of day-to-day operation.

---

## 4. Session Continuity (memory/)

### 4.1 Handoff Protocol

The `memory/` directory supports session continuity for both human developers and AI agents:

**memory/handoff.md**
- Current session state and context
- Active work items and their status
- Decisions made in previous sessions
- Outstanding questions or blockers

**memory/project.md**
- Overall project state
- Key milestones and their status
- Important configuration decisions
- Team conventions and agreements

### 4.2 Using Handoff Files

**At Session Start:**

```bash
# Always read these files when starting a new session
cat memory/handoff.md
cat memory/project.md
```

This applies whether you are:
- A developer starting work for the day
- An AI agent beginning a new session in Trae IDE
- An AI agent beginning a new session in Grok Build

**At Session End:**

Update `memory/handoff.md` with:
- What you accomplished
- What is still in progress
- Any blockers or decisions needed
- Context the next session will need

```bash
# Example handoff update
cat >> memory/handoff.md << 'EOF'

## Session 2024-01-15

### Completed
- Fixed memory scope issue in flagship workflow
- Updated business:validate to check new schema fields

### In Progress
- Evolution check refinement (evaluation threshold adjustment)

### Context for Next Session
- Need to run full business:eval after threshold change
- Frontend types need regeneration (backend schema changed)
EOF
```

> **Note:** Both Trae IDE and Grok Build agent harnesses read `memory/handoff.md` and `memory/project.md` at session start. Keeping these files current ensures AI agents have full context regardless of which harness is used.

---

## 5. Project Planning Artifacts

### 5.1 Planning Directory Structure

```
planning/
  # Project roadmaps
  # Sprint/iteration plans
  # Priority matrices
  # Resource allocation
```

### 5.2 Key Planning Documents

**plan_to_mark_100.md**
- The product-bar plan from P0 to P5 (all done)
- Feature completeness criteria
- When to read: Understanding what "done" means for the product

**structure.md**
- Architecture source of truth
- Component boundaries and interfaces
- When to read: Before making structural changes

**structure_scorecard_100.md**
- Scoring rubric for product completeness
- Evidence requirements per category
- When to read: Verifying product-bar compliance

### 5.3 Review Artifacts

**reviews/e1_operator_checklist.md**
- E1 operator path verification
- End-to-end test scenarios
- When to read: Validating the operator experience works correctly

---

## 6. Agent Harness Support

### 6.1 Trae IDE Harness

The Trae IDE harness generates configuration under `.trae/`:

```
.trae/
  settings/        # IDE-specific settings
  agents/          # Agent configurations
  commands/        # Custom commands
  rules/           # Behavioral rules
```

**Key Trae Resources:**
- `docs/trae.md` - Full Trae configuration guide
- `.trae/` directory - Generated files (do not manually edit)
- `rules/` - Shared rules (source of truth)
- `skills/` - Shared skills (source of truth)

**Using Trae for Development:**

1. Open the project in Trae IDE
2. Agents automatically load from `.trae/agents/`
3. Custom commands available from `.trae/commands/`
4. Rules enforced from `.trae/rules/` and shared `rules/`

### 6.2 Grok Build Harness

The Grok Build harness generates configuration under `.grok/`:

```
.grok/
  rules/          # Behavioral rules
  agents/         # Agent configurations
  skills/         # Agent skills
  commands/       # Custom commands
```

**Key Grok Resources:**
- `docs/grok.md` - Full Grok configuration guide
- `migrate_to_grok_build.md` - Migration from other harnesses
- `.grok/` directory - Generated files (do not manually edit)
- `rules/` - Shared rules (source of truth)
- `skills/` - Shared skills (source of truth)

**Using Grok for Development:**

1. Start a Grok Build session
2. Agents load from `.grok/agents/`
3. Skills available from `.grok/skills/`
4. Rules enforced from `.grok/rules/` and shared `rules/`

### 6.3 Harness Synchronization

Both harnesses are generated from shared source-of-truth files:

```bash
# Regenerate both harness configurations
npm run sync

# Verify managed files exist
npm run sync:check
```

**Shared Sources:**
| Source | Purpose |
|--------|---------|
| `rules/` | Behavioral rules for both harnesses |
| `skills/` | Agent skills shared across harnesses |
| `hooks/` | Event hooks |
| `mcp-configs/` | MCP server configurations |
| `scripts/adapters/shared.mjs` | Shared adapter logic |

> **Warning:** Never manually edit files in `.trae/` or `.grok/`. These are generated by `npm run sync` from the shared sources. Any manual changes will be overwritten on the next sync.

---

## 7. Contribution Workflow

### 7.1 Before Contributing

1. Read `memory/handoff.md` for current project state
2. Check open issues for existing discussions
3. Review `plan_to_mark_100.md` for project priorities
4. Understand the affected area's architecture via `docs/architecture.md`

### 7.2 Contribution Process

**Step 1:** Create a feature branch:

```bash
git checkout -b feature/your-improvement-name
```

**Step 2:** Make your changes, following existing patterns:

```bash
# After making changes, validate
npm run business:validate
npm run business:security
```

**Step 3:** Run relevant tests:

```bash
# Backend changes
cd backend && set PYTHONPATH=. && python -m unittest discover -s app/tests/unit -p "test_*.py" -v

# Frontend changes
cd frontend && pnpm lint && pnpm typecheck && pnpm test

# Business artifact changes
npm run business:validate && npm run business:security && npm run business:governance
```

**Step 4:** Sync harnesses if you changed shared sources:

```bash
npm run sync
npm run sync:check
```

**Step 5:** Update handoff:

```bash
# Update memory/handoff.md with your changes
```

**Step 6:** Commit and push:

```bash
git add -A
git commit -m "feat: description of your change"
git push origin feature/your-improvement-name
```

**Step 7:** Create a pull request with:
- Description of the change
- Testing performed
- Impact on other components
- Any new environment variables or dependencies

### 7.3 Contribution Guidelines

| Guideline | Detail |
|-----------|--------|
| Branch naming | `feature/`, `fix/`, `docs/`, `refactor/` prefixes |
| Commit messages | Conventional commits (feat:, fix:, docs:, etc.) |
| Testing | All tests must pass before merge |
| Validation | `business:validate` and `business:security` clean |
| Documentation | Update docs if behavior changes |
| Harness sync | Run `npm run sync` after changing shared sources |

---

## 8. Issue Reporting

### 8.1 Effective Issue Reports

When reporting issues, include the following information:

**Issue Template:**

```markdown
## Issue: [Brief title]

### Environment
- OS: [Windows/macOS/Linux]
- Node.js version: [output of `node --version`]
- Python version: [output of `python --version`]
- PostgreSQL version: [output of `psql --version`]

### Steps to Reproduce
1. [First step]
2. [Second step]
3. [Step where error occurs]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Error Output
```
[Paste full error output here]
```

### Diagnostic Results
```
[Output of npm run doctor]
[Output of npm run business:validate if relevant]
[Output of health endpoint if relevant]
```

### Additional Context
- [ ] Occurs consistently / intermittently
- [ ] First time / regression (previously worked)
- [ ] Blocking work / inconvenience
```

### 8.2 Information Gathering Before Reporting

Run these commands and include the output:

```bash
# System prerequisites
npm run doctor

# Business layer status (if relevant)
npm run business:validate 2>&1 | tail -20

# Backend health (if relevant)
curl -s http://127.0.0.1:8000/api/v1/health/ready

# Git state
git log --oneline -3
git status --short
```

### 8.3 Common Issue Categories

| Category | Label | Response Time |
|----------|-------|---------------|
| Security vulnerability | `security` | Immediate |
| Data loss risk | `critical` | Same day |
| Workflow failure | `bug` | 1-3 days |
| Performance issue | `performance` | 1 week |
| Documentation error | `docs` | 1-2 weeks |
| Feature request | `enhancement` | As prioritized |

---

## 9. Community Engagement

### 9.1 Discussion Topics

Common community discussion areas:

- **Architecture decisions:** Why is the system designed this way?
- **Evolution strategies:** Best practices for variant proposals
- **Governance customization:** Adapting risk tiers to your organization
- **Integration patterns:** Connecting external tools and services
- **Performance optimization:** Scaling for larger workloads
- **Agent design:** Creating effective agent configurations

### 9.2 Knowledge Sharing

Contribute back to the community:

1. **Document solutions:** When you solve a novel problem, add it to troubleshooting
2. **Share golden tasks:** Add evaluation tasks that cover edge cases
3. **Propose improvements:** Use the evolution sandbox for experimental changes
4. **Update handoff:** Keep session continuity files current for other contributors

### 9.3 Staying Current

Keep up with project development:

```bash
# Pull latest changes
git pull origin main

# Check what changed
git log --oneline -10

# Validate your environment still works
npm run doctor
npm run business:validate

# Sync harnesses with latest
npm run sync
```

---

## 10. Quick Reference Guide

### Essential Commands Cheat Sheet

```bash
# Setup and validation
npm run bootstrap           # Full system setup
npm run doctor              # Check prerequisites
npm run sync                # Regenerate harness files
npm run sync:check          # Verify managed files

# Business layer
npm run business:init       # Seed business files
npm run business:validate   # Validate artifacts
npm run business:governance # Check governance
npm run business:security   # Security scan
npm run business:evolution:check  # Evolution status
npm run business:eval       # Run evaluations

# Backend
cd backend
set PYTHONPATH=.
uvicorn app.main:app --reload
python -m unittest discover -s app/tests/unit -p "test_*.py" -v
python -m unittest discover -s app/tests/e2e -p "test_*.py" -v

# Frontend
cd frontend
pnpm install
pnpm dev
pnpm lint && pnpm typecheck && pnpm test
pnpm api:generate           # Regenerate API types

# Sources
npm run sources:download    # Download external sources
npm run sources:audit       # Audit source integrity
```

### Key File Locations

| File | Purpose |
|------|---------|
| `backend/.env` | Backend environment configuration |
| `sources/source-lock.json` | External source status |
| `docs/source-audit.md` | Audit results |
| `memory/handoff.md` | Session continuity |
| `memory/project.md` | Project state |
| `business/governance/` | Governance artifacts |
| `business/evals/golden-tasks/` | Evaluation corpus |
| `business/distilled/skills/_sandbox/` | Evolution sandbox |

### API Endpoints Reference

| Endpoint | Purpose |
|----------|---------|
| `GET /api/v1/health/ready` | Health check |
| `POST /api/v1/auth/login` | Password authentication |
| `GET /api/v1/workflows` | List workflows |
| `POST /api/v1/workflows/{id}/run` | Execute workflow |
| `GET /api/v1/audit` | Query audit logs |
| `POST /api/v1/improvement/reflect/{run_id}` | Reflect on run |
| `GET /api/v1/improvement/lessons` | View lessons |
| `POST /api/v1/improvement/auto-propose` | Generate proposals |
| `POST /api/v1/loops/run` | Run improvement loop |
| `GET /api/v1/evolution/archive` | Evolution status |
| `POST /api/v1/knowledge/graph/federate` | Knowledge federation |

---

## 11. Real-World Use Case Examples

### Use Case 1: Onboarding a New Team Member

**Scenario:** A new developer joins and needs to become productive quickly.

**Recommended Path:**

1. Start with `docs/installation.md` for environment setup
2. Run `npm run bootstrap` and `npm run doctor` to verify
3. Read `memory/handoff.md` for current project context
4. Read this user guide Section 1 for fundamentals
5. Read `docs/usage.md` for command reference
6. Set up both backend and frontend following the documented procedures
7. Run the health endpoint to confirm everything works
8. Read `docs/architecture.md` for system understanding
9. Start with small contributions (documentation fixes, test additions)
10. Progress to feature work after understanding the codebase patterns

**Time to Productivity:** Most developers are contributing within 2-3 days following this path.

### Use Case 2: Finding Help for a Specific Problem

**Scenario:** You encounter an error you have not seen before.

**Resolution Path:**

1. Check `docs/troubleshooting.md` for known issues
2. Read Chapter 4.1 (Common Error Resolution) for systematic diagnosis
3. Run `npm run doctor` and `npm run business:validate` for context
4. Check `git log` for recent changes that might have introduced the issue
5. Search the issue tracker for similar reports
6. If unresolved, file a detailed issue report (Section 8)

### Use Case 3: Contributing an Improvement

**Scenario:** You have an idea for a better workflow configuration.

**Contribution Path:**

1. Read `plan_to_mark_100.md` to understand project priorities
2. Check the evolution sandbox for similar proposals:
   ```bash
   ls business/distilled/skills/_sandbox/
   ```
3. Create your improvement in the sandbox first (not production)
4. Run evaluation: `npm run business:eval`
5. If scores are good, follow the promotion pipeline
6. Document your change in `memory/handoff.md`
7. Submit via the standard contribution workflow (Section 7)

---

## 12. Best Practices

### Documentation Hygiene

1. **Update as you go.** When you discover something undocumented, add it immediately.
2. **Cross-reference.** Link between related documents rather than duplicating content.
3. **Date your updates.** Include timestamps in handoff files and change notes.
4. **Verify commands.** Run documented commands before adding them to guides.
5. **Use examples.** Show actual output, not theoretical descriptions.

### Self-Sufficiency Principles

1. **Exhaust documentation before asking.** Most questions are answered in the docs.
2. **Run diagnostics first.** `npm run doctor` and `npm run business:validate` answer 80% of questions.
3. **Check the audit trail.** For runtime issues, the audit logs contain the answer.
4. **Read the error message.** Generic Swarm Ops error messages are designed to be actionable.
5. **Follow the flowchart.** Chapter 4.1's resolution flowchart handles most common errors.

### Community Principles

1. **Give back what you receive.** Document solutions you discover.
2. **Be specific in issues.** Include reproduction steps and diagnostic output.
3. **Respect the pipeline.** Use sandbox for experiments, not production shortcuts.
4. **Keep context fresh.** Update handoff files for others who follow.
5. **Trust the safety systems.** Fail-closed, sandbox-only, and human gates exist for good reasons.

---

## 13. Chapter Summary

This chapter covered the complete support and community resource ecosystem:

- **Documentation Structure:** The `docs/`, `book/`, `memory/`, `business/`, and `planning/` directories and their purposes
- **Session Continuity:** Using `memory/handoff.md` and `memory/project.md` for context persistence across sessions
- **Agent Harnesses:** Trae IDE and Grok Build configuration, synchronization, and shared source of truth
- **Contribution Workflow:** From branch creation through validation to pull request
- **Issue Reporting:** Effective templates, diagnostic gathering, and categorization
- **Community Engagement:** Knowledge sharing, discussion topics, and staying current
- **Quick Reference:** Essential commands, key file locations, and API endpoints

The key principle is self-sufficiency: the documentation ecosystem is designed to answer most questions without external help, and the community thrives when everyone contributes solutions back.

---

## 14. Knowledge Check Quiz

Test your understanding of support and community resources:

**Question 1:** What two files should you always read at the start of a new development session?

<details>
<summary>Answer</summary>

1. `memory/handoff.md` (current session state and context)
2. `memory/project.md` (overall project state)

Both files are read by AI agents in Trae IDE and Grok Build harnesses, and they provide critical context for continuing work from previous sessions.

</details>

**Question 2:** You want to understand why the system uses fail-closed behavior for tool adapters. Which documentation should you read?

<details>
<summary>Answer</summary>

Read `book/design_phase/` documents for architectural design decisions and rationale. For operational details, read `docs/architecture.md`. The design phase documents explain the "why" while the operational docs explain the "how."

</details>

**Question 3:** After changing files in the `rules/` directory, what command must you run?

<details>
<summary>Answer</summary>

Run `npm run sync` to regenerate both `.trae/` and `.grok/` directories from the shared source of truth. Then run `npm run sync:check` to verify all managed files were created correctly. Never manually edit files in `.trae/` or `.grok/` directly.

</details>

**Question 4:** What information should you include in an issue report to help resolve it quickly?

<details>
<summary>Answer</summary>

Include: environment details (OS, Node.js, Python, PostgreSQL versions), steps to reproduce, expected vs. actual behavior, full error output, and diagnostic results (`npm run doctor`, `npm run business:validate`, health endpoint response). Also note whether the issue is consistent or intermittent, and whether it is new or a regression.

</details>

**Question 5:** What is the shared source of truth for both Trae and Grok harness configurations?

<details>
<summary>Answer</summary>

The shared sources are: `rules/` (behavioral rules), `skills/` (agent skills), `hooks/` (event hooks), `mcp-configs/` (MCP server configurations), and `scripts/adapters/shared.mjs` (shared adapter logic). Both `.trae/` and `.grok/` are generated from these sources via `npm run sync`.

</details>

**Question 6:** Where do evolution sandbox proposals live, and why should you never manually move them to production?

<details>
<summary>Answer</summary>

Sandbox proposals live in `business/distilled/skills/_sandbox/`. You should never manually move them because the governance system requires a complete evidence trail (evaluation scores, canary results, human sign-off) before promotion. Bypassing this breaks the safety guarantee that only verified improvements reach production.

</details>

**Question 7:** What is the recommended path for a new developer to become productive in this project?

<details>
<summary>Answer</summary>

1. Follow `docs/installation.md` for setup
2. Run `npm run bootstrap` and `npm run doctor`
3. Read `memory/handoff.md` for project context
4. Read the user guide Section 1 for fundamentals
5. Read `docs/usage.md` for commands
6. Set up backend and frontend
7. Verify with health endpoint
8. Read `docs/architecture.md`
9. Start with small contributions
10. Progress to feature work

This typically takes 2-3 days.

</details>
