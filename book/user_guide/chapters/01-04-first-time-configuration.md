# Chapter 01-04: First-Time Configuration

![Configuration Overview](../assets/01-04-configuration-overview.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Log in with the seed credentials and understand authentication modes
2. Configure password-based authentication for production use
3. Set up initial agent definitions and assign roles
4. Create your first Workflow DNA definition
5. Run business layer validation commands to verify configuration integrity
6. Understand the relationship between configuration layers (environment, backend, frontend, business artifacts)

## Prerequisites

- Completed [Chapter 01-03](01-03-initial-setup-wizard.md) with all services running
- Backend accessible at `http://127.0.0.1:8000`
- Frontend accessible at `http://localhost:3000`
- PostgreSQL database connected (health endpoint shows `"database": "postgres"`)
- Business artifacts initialized (`npm run business:init` completed)

---

## 1. Seed Login and Authentication

The system ships with seed credentials for initial access. Understanding the authentication
model is critical for secure operation.

### 1.1 Seed Credentials

The default administrator account is pre-configured:

| Field | Value |
|-------|-------|
| Email | `admin@example.com` |
| Password | `admin-password` |
| Role | `admin` (full access) |

> **Warning:** These are development-only credentials. In a production environment,
> change the admin password immediately after first login and disable static tokens.

### 1.2 Authentication Methods

The system supports two authentication methods:

| Method | Use Case | Security Level |
|--------|----------|---------------|
| **Password login** | Production operation, browser access | High (recommended) |
| **Static bearer tokens** | Curl smoke testing only | Low (development only) |

**Password login** produces a session with:
- `gso_access_token` cookie (HTTP-only, secure)
- Session user cookie for frontend state
- Automatic session expiration and renewal

**Static tokens** (like `admin-token`) exist only for quick curl testing during
development and should never be used in production.

### 1.3 Step-by-Step: First Login

#### Via the Frontend Console

1. Open `http://localhost:3000` in your browser
2. Enter email: `admin@example.com`
3. Enter password: `admin-password`
4. Click "Sign In"
5. You should be redirected to the main dashboard

#### Via the API

```bash
# Login via API
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}' \
  -c cookies.txt

# Use the session cookie for subsequent requests
curl -b cookies.txt http://127.0.0.1:8000/api/v1/workflows
```

**Expected response from login:**
```json
{
  "status": "authenticated",
  "user": {
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

### 1.4 Understanding Roles

The RBAC system defines three roles:

| Role | Permissions | Intended User |
|------|------------|---------------|
| `admin` | Full access: create, run, approve, configure, evolve | System administrators |
| `operator` | Create agents/workflows, run workflows, view results | Day-to-day operators |
| `reviewer` | Approve human-gated steps, view audit logs | Compliance reviewers |

> **Note:** Role assignments are stored in the `runtime_state` database. The seed
> installation creates only the `admin` role. Additional users and roles can be
> created via the API or ops console.

---

## 2. Password Authentication Setup

For production environments, configure proper password authentication.

### 2.1 Understanding the Auth Flow

```text
User submits email + password
    |
    v
POST /api/v1/auth/login
    |
    v
Backend verifies credentials against stored hash
    |
    v
On success: Set gso_access_token cookie + session user cookie
    |
    v
Frontend stores session, enables navigation
```

### 2.2 Creating Additional Users

To add users beyond the seed admin:

```bash
# Create a new operator user via API
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_session_token>" \
  -d '{
    "email": "operator@company.com",
    "password": "secure-password-here",
    "role": "operator"
  }'
```

### 2.3 Creating a Reviewer Account

```bash
# Create a reviewer for human-gate approvals
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_session_token>" \
  -d '{
    "email": "reviewer@company.com",
    "password": "secure-password-here",
    "role": "reviewer"
  }'
```

### 2.4 Session Management

Sessions are managed through cookies:

| Cookie | Purpose | Attributes |
|--------|---------|------------|
| `gso_access_token` | Authentication token | HTTP-only, Secure, SameSite |
| Session user | Frontend display state | Readable by JavaScript |

```bash
# Check current session
curl -b cookies.txt http://127.0.0.1:8000/api/v1/auth/me

# Expected response:
# {"email": "admin@example.com", "role": "admin"}
```

> **Tip:** Prefer password login over static tokens. Static tokens (`admin-token`)
> bypass proper session management and should only be used for quick curl smoke
> testing during development.

---

## 3. Initial Agent Configuration

Agents are the execution units of the system. Each agent has a defined role, tool
access permissions, and behavioral constraints.

### 3.1 Understanding the Agent Roster

The system defines two categories of agents:

**Control/Meta Agents:**

| Agent | Purpose |
|-------|---------|
| Business Orchestrator | Routes work, manages state, owns the global objective |
| Evolution Manager | Proposes and tests variants (sandbox only) |
| Evaluation Harness | Runs golden/regression/adversarial/replay suites |
| Governance Officer | Applies risk tiers, approval rules, audit requirements |
| Security Red-Team | Tests injection, tool misuse, leakage, unsafe autonomy |
| Memory Steward | Maintains memory quality, provenance, expiration |
| Tool Permission Broker | Grants scoped, temporary tool access |
| Incident Commander | Handles failures, rollbacks, postmortems |

**Learning Agents:**

| Agent | Purpose |
|-------|---------|
| Expert Shadow | Observes experts (with permission) |
| Cognitive Task Analyst | Turns interviews into decision cards + heuristics |
| Process Miner | Discovers workflows from logs |
| Task Mining Agent | Observes permitted UI/human task traces |
| Conformance Agent | Compares SOPs with observed behavior |
| Bottleneck Analyzer | Finds delays, loops, and handoff failures |
| Causal Improvement Agent | Proposes sandbox experiments from evidence |
| Knowledge Distiller | Converts raw material into rules/skills/playbooks |
| Knowledge Curator | Validates, deduplicates, organizes |

### 3.2 Creating Your First Agent

Use the ops console or API to create an agent:

#### Via the Ops Console

1. Navigate to **Agents** in the sidebar
2. Click **Create Agent**
3. Fill in the form:
   - **Name:** `customer_support_agent`
   - **Role:** `execution`
   - **Description:** `Handles customer support ticket routing and initial response`
   - **Tools:** `["email", "crm", "knowledge_retriever"]`
   - **Risk Tier:** `3` (Execute reversible)
4. Click **Save**

#### Via the API

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "customer_support_agent",
    "role": "execution",
    "description": "Handles customer support ticket routing and initial response",
    "tools": ["email", "crm", "knowledge_retriever"],
    "risk_tier": 3,
    "constraints": {
      "max_actions_per_run": 10,
      "require_human_gate_for": ["irreversible_actions"],
      "memory_scope": ["episodic", "semantic"]
    }
  }'
```

**Expected response:**
```json
{
  "id": "agent_customer_support_001",
  "name": "customer_support_agent",
  "role": "execution",
  "status": "active",
  "created_at": "2026-07-06T14:00:00Z"
}
```

### 3.3 Agent Configuration Best Practices

1. **Principle of least privilege** -- only grant tools the agent actually needs
2. **Set explicit risk tiers** -- higher tiers require more oversight
3. **Define memory scope** -- limit what memory types the agent can read/write
4. **Set action limits** -- prevent runaway execution with `max_actions_per_run`
5. **Document the purpose** -- clear descriptions help governance reviews

---

## 4. First Workflow DNA Creation

Workflow DNA is the central abstraction for defining business processes. Your first
workflow should be simple enough to verify the system works end-to-end.

### 4.1 Understanding Workflow DNA Structure

Every Workflow DNA must declare:

```yaml
workflow_dna:
  id: "unique_workflow_identifier"
  name: "Human-readable name"
  domain: "business_domain"
  objective: "What this workflow achieves"
  owner: "business_orchestrator"
  version: "1.0"
  inputs: ["required_input_data"]
  preconditions: ["conditions_that_must_be_true"]
  steps: [...]            # Bounded execution steps
  guardrails: {...}       # Human-approval conditions
  verification: {...}     # Required post-execution checks
  rollback: {...}         # Reversibility plan
  fitness_metrics: [...]  # How success is measured
```

### 4.2 Creating a Simple Workflow

Let's create a basic "document review" workflow as your first Workflow DNA:

#### Via the Ops Console

1. Navigate to **Workflows** in the sidebar
2. Click **Create Workflow**
3. Fill in the form:

```yaml
# Workflow DNA for document review
id: "wf_document_review_v1"
name: "Document Review"
domain: "operations"
objective: "Review and approve submitted documents with compliance checks."
owner: "business_orchestrator"
version: "1.0"
inputs: ["document_id", "submitter_id", "document_type"]
preconditions:
  - "document_status == submitted"
  - "submitter_id is valid"
steps:
  - id: "classify_document"
    agent: "knowledge_distiller"
    tools: ["document_classifier"]
    description: "Determine document type and applicable rules"
  - id: "compliance_check"
    agent: "governance_officer"
    tools: ["policy_retriever", "compliance_checker"]
    description: "Verify document meets compliance requirements"
  - id: "human_review"
    agent: "business_orchestrator"
    tools: []
    description: "Human reviewer approves or rejects"
    human_gate: true
  - id: "finalize"
    agent: "business_orchestrator"
    tools: ["document_store", "notification"]
    description: "Store approved document and notify submitter"
guardrails:
  human_approval_required_if:
    - "compliance_check.risk_score > 0.7"
    - "document_type == confidential"
verification:
  required_checks:
    - "document_classified"
    - "compliance_verified"
    - "human_approved"
    - "audit_log_complete"
rollback:
  reversible: true
  rollback_steps: ["revert_document_status", "notify_submitter_of_rejection"]
fitness_metrics:
  - "review_cycle_time"
  - "compliance_pass_rate"
  - "rejection_rate"
```

#### Via the API

```bash
curl -X POST http://127.0.0.1:8000/api/v1/workflows \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "id": "wf_document_review_v1",
    "name": "Document Review",
    "domain": "operations",
    "objective": "Review and approve submitted documents with compliance checks.",
    "version": "1.0",
    "inputs": ["document_id", "submitter_id", "document_type"],
    "steps": [
      {"id": "classify_document", "agent": "knowledge_distiller", "tools": ["document_classifier"]},
      {"id": "compliance_check", "agent": "governance_officer", "tools": ["policy_retriever"]},
      {"id": "human_review", "agent": "business_orchestrator", "human_gate": true},
      {"id": "finalize", "agent": "business_orchestrator", "tools": ["document_store"]}
    ],
    "guardrails": {
      "human_approval_required_if": ["compliance_check.risk_score > 0.7"]
    },
    "verification": {
      "required_checks": ["document_classified", "compliance_verified", "audit_log_complete"]
    },
    "rollback": {
      "reversible": true,
      "rollback_steps": ["revert_document_status"]
    },
    "fitness_metrics": ["review_cycle_time", "compliance_pass_rate"]
  }'
```

### 4.3 Understanding the Flagship Workflow

The system ships with a flagship workflow: `wf_customer_onboarding_v12`. Study its
structure to understand production-grade Workflow DNA:

```bash
# View the flagship workflow
curl -b cookies.txt http://127.0.0.1:8000/api/v1/workflows/wf_customer_onboarding_v12 \
  | python3 -m json.tool
```

Key features of the flagship workflow:
- **4 bounded steps** with explicit agent and tool assignments
- **Memory reads** from `contract_rules`, `customer_exceptions`, `past_failures`
- **Memory writes** to `event_log`, `decision_memory`, `lessons_learned`
- **Human gate** for high risk, contract exceptions, and irreversible actions
- **Verification** of CRM record, billing config, welcome packet, and audit log
- **Rollback plan** with specific reversal steps
- **6 fitness metrics** for evolution tracking

---

## 5. Business Layer Validation

After configuring agents and workflows, validate the entire business layer to ensure
consistency and completeness.

### 5.1 Running Validation

```bash
# From the repository root
npm run business:validate
```

**What it checks:**
- All governance artifacts exist and conform to schemas
- Evaluation golden tasks are well-formed (minimum 20 required)
- Workflow DNA definitions have required fields
- Cross-references between artifacts resolve correctly
- Security baselines are in place

**Expected output (success):**
```text
Validating business artifacts...
  governance: PASS
  evals: PASS (20+ golden tasks)
  evolution: PASS
  security: PASS
  knowledge-base: PASS
All validations passed.
```

### 5.2 Governance Validation

```bash
npm run business:governance
```

**What it checks:**
- AI inventory is populated
- Risk tier assignments exist for active workflows
- Human-approval policy covers all tier-4+ operations
- Audit log retention policy is defined
- Model cards exist for AI components
- Assurance cases are documented

### 5.3 Security Validation

```bash
npm run business:security
```

**What it checks:**
- Threat models exist for exposed interfaces
- Tool permissions are defined (allow-lists)
- Prompt injection test fixtures are present
- Red-team results are documented
- Incident response plan exists

### 5.4 Evolution Readiness Check

```bash
npm run business:evolution:check
```

**What it checks:**
- Workflow DNA definitions have fitness metrics
- Golden task coverage is sufficient for evolution evaluation
- Baseline measurements exist for comparison
- Sandbox configuration is valid

### 5.5 Evaluation Dry Run

```bash
npm run business:eval -- --dry-run
```

**What it does:**
- Loads all golden tasks from `business/evals/golden-tasks/`
- Validates each task definition
- Reports which workflows have evaluation coverage
- Does not actually execute evaluations (dry run mode)

---

## 6. Configuration Layers Explained

The system uses a layered configuration model where each layer serves a different purpose:

### 6.1 Layer 1: System Environment Variables

These control infrastructure behavior at the OS level:

```bash
GENERIC_SWARM_AUTO_REFLECT=true      # Auto-reflect on terminal runs
GENERIC_SWARM_LLM_CRITIC_ENABLED=false  # Optional AI critic
GENERIC_SWARM_EMBEDDINGS_ENABLED=false  # Embedding retrieval
GENERIC_SWARM_PGVECTOR_ENABLED=false    # pgvector extension
```

### 6.2 Layer 2: Backend .env

Database connectivity and backend-specific settings:

```bash
# backend/.env
DATABASE_URL=postgresql://user:pass@localhost:5432/generic_swarm_ops
NEO4J_URI=bolt://localhost:7687  # Optional
```

### 6.3 Layer 3: Frontend Environment

Frontend routing and mode configuration:

```bash
NEXT_PUBLIC_DEMO_MODE=false
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

### 6.4 Layer 4: Business Artifacts

Declarative configuration stored in the `business/` directory:

```text
business/governance/         - Risk tiers, approval policy, inventory
business/evals/              - Golden tasks, regression tests
business/evolution/          - Workflow DNA, variants, lessons
business/security/           - Threat models, permissions
business/knowledge-base/     - Rules, provenance, retrieval policy
```

> **Note:** The configuration layers are applied in order. Environment variables override
> defaults. Backend .env provides database connection. Frontend env controls UI mode.
> Business artifacts define the declarative governance and evaluation configuration.

---

## 7. Verifying Your Configuration

### Step 1: Full Health Check

```bash
curl -s http://127.0.0.1:8000/api/v1/health/ready | python3 -m json.tool
```

Confirm: `"database": "postgres"`

### Step 2: Authentication Test

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}' \
  -c cookies.txt

# Verify session
curl -b cookies.txt http://127.0.0.1:8000/api/v1/auth/me
```

### Step 3: Agent Listing

```bash
curl -b cookies.txt http://127.0.0.1:8000/api/v1/agents | python3 -m json.tool
```

### Step 4: Workflow Listing

```bash
curl -b cookies.txt http://127.0.0.1:8000/api/v1/workflows | python3 -m json.tool
```

### Step 5: Business Validation Suite

```bash
npm run business:validate
npm run business:governance
npm run business:security
npm run business:evolution:check
```

All commands should pass without errors.

---

## 8. Real-World Use Cases

### Use Case 1: Onboarding a New Team Member

**Scenario:** A new operator joins the team and needs access to run workflows but not
approve sensitive actions.

**Configuration steps:**

```bash
# 1. Create operator account
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "email": "newoperator@company.com",
    "password": "secure-password",
    "role": "operator"
  }'

# 2. The operator can now:
#    - Create and run workflows
#    - View agent activity and run results
#    - Cannot approve human-gated steps (requires reviewer role)
#    - Cannot modify system configuration (requires admin role)
```

**Governance implication:** The `operator` role automatically inherits the constraints
defined in `business/governance/human-approval-policy/`. They can execute tier-3
(reversible) actions but cannot approve tier-4 (gated) actions.

### Use Case 2: Setting Up a Compliance Workflow

**Scenario:** A legal team needs a workflow that routes contract reviews through
multiple approval gates with full audit trail.

**Configuration steps:**

```yaml
# Workflow DNA for contract compliance
workflow_dna:
  id: "wf_contract_compliance_v1"
  name: "Contract Compliance Review"
  domain: "legal_operations"
  objective: "Ensure all contracts meet regulatory and internal compliance requirements."
  owner: "business_orchestrator"
  version: "1.0"
  inputs: ["contract_id", "customer_id", "contract_value"]
  preconditions:
    - "contract_status == pending_review"
  steps:
    - id: "initial_screening"
      agent: "governance_officer"
      tools: ["contract_parser", "policy_retriever"]
    - id: "risk_assessment"
      agent: "governance_officer"
      tools: ["risk_scorer"]
    - id: "legal_review"
      agent: "business_orchestrator"
      human_gate: true
      description: "Senior counsel reviews high-value or high-risk contracts"
    - id: "final_approval"
      agent: "business_orchestrator"
      human_gate: true
      description: "Contract manager signs off"
    - id: "archive"
      agent: "business_orchestrator"
      tools: ["document_store", "audit_writer"]
  guardrails:
    human_approval_required_if:
      - "contract_value > 250000"
      - "risk_assessment.score > 0.8"
      - "jurisdiction not in approved_list"
  verification:
    required_checks:
      - "screening_complete"
      - "risk_assessed"
      - "legal_reviewed"
      - "approval_documented"
      - "audit_log_complete"
  rollback:
    reversible: true
    rollback_steps: ["revert_contract_status", "notify_stakeholders"]
  fitness_metrics:
    - "review_cycle_time"
    - "compliance_pass_rate"
    - "escalation_rate"
    - "cost_per_review"
```

### Use Case 3: Configuring Auto-Reflection

**Scenario:** A team wants the system to automatically learn from every completed
workflow run and store improvement suggestions.

**Configuration:**

```bash
# Enable auto-reflect in environment
export GENERIC_SWARM_AUTO_REFLECT=true

# Restart backend to pick up the change
# (or it's already true by default)
```

**What happens:** After every workflow run reaches a terminal state (completed, failed,
or timed out), the system automatically:

1. Calls `POST /api/v1/improvement/reflect/{run_id}`
2. Analyzes what worked and what failed
3. Stores lessons in `business/evolution/lessons-learned/`
4. Optionally proposes workflow improvements (if conditions are met)

```bash
# View accumulated lessons
curl -b cookies.txt http://127.0.0.1:8000/api/v1/improvement/lessons \
  | python3 -m json.tool
```

---

## 9. Best Practices

1. **Change seed credentials immediately** -- the `admin@example.com` / `admin-password`
   combination is public knowledge. Set a strong password for production.

2. **Use role-based access from the start** -- even in development, create separate
   operator and reviewer accounts to test RBAC behavior.

3. **Start with simple workflows** -- your first Workflow DNA should be small (2-3 steps)
   to verify the system works. Add complexity incrementally.

4. **Always include a rollback plan** -- the runtime rejects DNA without a rollback
   specification. Make this a habit from day one.

5. **Run validation after every change** -- `npm run business:validate` catches errors
   early. Integrate it into your development workflow.

6. **Document agent purpose clearly** -- governance reviews require understanding what
   each agent does and why it has its assigned tools.

7. **Monitor the auto-reflect output** -- lessons learned from auto-reflection provide
   valuable insight into workflow performance and failure patterns.

8. **Keep fitness metrics measurable** -- abstract metrics like "quality" need concrete
   definitions. Use specific measurements like "cycle_time_minutes" or "error_count".

---

## 10. Chapter Summary

In this chapter, you configured the system for first use:

- **Authentication:** Logged in with seed credentials (`admin@example.com` /
  `admin-password`), understood password vs. token auth, and learned about RBAC roles
  (admin, operator, reviewer)
- **Agents:** Created your first agent with defined role, tools, risk tier, and constraints
- **Workflows:** Created your first Workflow DNA with steps, guardrails, verification
  checks, rollback plan, and fitness metrics
- **Validation:** Ran `business:validate`, `business:governance`, `business:security`,
  and `business:evolution:check` to verify configuration integrity
- **Configuration layers:** Understood how environment variables, backend .env, frontend
  env, and business artifacts work together

The system is now fully configured and ready for daily operation.

---

## 11. Knowledge Check Quiz

**Question 1:** What are the seed login credentials?

a) `root@system.local` / `password`
b) `admin@example.com` / `admin-password`
c) `system@generic-swarm.io` / `admin123`
d) `admin@admin.com` / `changeme`

<details>
<summary>Answer</summary>
<b>b)</b> The seed credentials are <code>admin@example.com</code> /
<code>admin-password</code>. These should be changed immediately in production.
</details>

---

**Question 2:** Which role can approve human-gated workflow steps?

a) `operator`
b) `admin` and `reviewer`
c) Only `admin`
d) Any authenticated user

<details>
<summary>Answer</summary>
<b>b)</b> Both <code>admin</code> (full access) and <code>reviewer</code> (approve only)
can approve human-gated steps. The <code>operator</code> role can run workflows but
cannot approve gated steps.
</details>

---

**Question 3:** What cookie stores the authentication token after password login?

a) `session_id`
b) `auth_token`
c) `gso_access_token`
d) `jwt_token`

<details>
<summary>Answer</summary>
<b>c)</b> The <code>gso_access_token</code> cookie stores the authentication token.
It is HTTP-only and secure, preventing JavaScript access from potential XSS attacks.
</details>

---

**Question 4:** What happens if you submit a Workflow DNA without a rollback plan?

a) It is accepted with a warning
b) It is rejected by the runtime
c) It runs in restricted mode
d) A default rollback is generated

<details>
<summary>Answer</summary>
<b>b)</b> The runtime rejects Workflow DNA that has no rollback plan. This is enforced
deterministically to maintain the Safety priority.
</details>

---

**Question 5:** What does `npm run business:governance` check?

a) Code formatting
b) Database schema
c) AI inventory, risk tiers, approval policy, model cards, assurance cases
d) Frontend routing

<details>
<summary>Answer</summary>
<b>c)</b> <code>npm run business:governance</code> validates governance artifacts including
AI inventory, risk tier assignments, human-approval policy, audit log retention, model
cards, and assurance cases.
</details>

---

**Question 6:** What is the recommended authentication method for production use?

a) Static bearer tokens
b) Password login with session cookies
c) API keys in headers
d) OAuth2 with external provider

<details>
<summary>Answer</summary>
<b>b)</b> Password login producing session cookies (<code>gso_access_token</code>) is
the recommended method. Static tokens exist only for curl smoke testing during
development and should never be used in production.
</details>

---

**Question 7:** What environment variable controls automatic post-run reflection?

a) `GENERIC_SWARM_LLM_CRITIC_ENABLED`
b) `GENERIC_SWARM_AUTO_REFLECT`
c) `GENERIC_SWARM_EVOLUTION_ENABLED`
d) `AUTO_IMPROVE_MODE`

<details>
<summary>Answer</summary>
<b>b)</b> <code>GENERIC_SWARM_AUTO_REFLECT</code> (default: true) controls whether the
system automatically reflects on completed runs and stores lessons learned.
</details>

---

## Next Chapter

Continue to [Chapter 01-05: Basic Navigation & Account Management](01-05-basic-navigation-account-management.md)
to learn how to navigate the ops console and manage user accounts effectively.
