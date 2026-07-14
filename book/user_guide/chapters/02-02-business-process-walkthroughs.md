# Chapter 2.2: Business Process Walkthroughs

![Customer Onboarding Process Flow](../assets/02-02-onboarding-process-flow.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Execute the flagship customer onboarding workflow end-to-end
2. Understand the E1 operator path from login through improvement
3. Handle human gate approvals as a reviewer
4. Inspect audit logs, memory writes, and tool effects after a run
5. Trigger the self-improvement pipeline (Reflect, Propose, Evaluate, Canary)
6. Navigate the run detail view and evolution population archive

## Prerequisites

Before starting this chapter, ensure you have:

- Completed Chapter 2.1 (Workflow DNA Implementation)
- A running backend instance at `http://127.0.0.1:8000`
- A running frontend instance at `http://localhost:3000`
- Login credentials configured (default: `admin@example.com` / `admin-password`)
- The flagship workflow `wf_customer_onboarding_v12` loaded (via `npm run business:init`)

---

## The E1 Operator Path

The E1 (End-to-End Operator) path is the reference walkthrough that proves the entire system works from login through self-improvement. It exercises:

- Authentication and session management
- Workflow listing and selection
- Run execution with real payloads
- Human gate approval workflows
- Audit log inspection
- Memory and evaluation review
- Self-improvement pipeline activation

> **Note:** The E1 path is covered by the automated test `test_e1_operator_path`. Everything you do in this walkthrough mirrors what that test verifies programmatically.

---

## Step-by-Step: Complete Onboarding Walkthrough

### Step 1: Log In to the System

Access the ops console and authenticate:

```bash
# Via the frontend (recommended)
# Navigate to http://localhost:3000
# Enter credentials:
#   Email: admin@example.com
#   Password: admin-password
```

Alternatively, authenticate via the API:

```bash
# Password login returns cookie gso_access_token + session user cookie
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin-password"
  }'
```

The response sets:

- `gso_access_token` cookie for session authentication
- Session user cookie with role information

> **Tip:** For curl-based testing, static bearer tokens (`admin-token`) remain available for smoke testing only. Always prefer password login for realistic testing.

### Step 2: List Available Workflows

After login, view the available workflows:

**Frontend:**
1. Navigate to the **Workflows** page from the sidebar
2. You should see `wf_customer_onboarding_v12` listed with its metadata

**API:**
```bash
curl http://127.0.0.1:8000/api/v1/workflows \
  -H "Cookie: gso_access_token=<your_token>"
```

Expected response includes:

```json
{
  "workflows": [
    {
      "id": "wf_customer_onboarding_v12",
      "name": "Customer Onboarding",
      "domain": "operations",
      "version": "12.0",
      "status": "active"
    }
  ]
}
```

### Step 3: List Available Agents

View the agents that participate in workflows:

**Frontend:**
1. Navigate to the **Agents** page
2. Review agent capabilities and assigned roles

**API:**
```bash
curl http://127.0.0.1:8000/api/v1/agents \
  -H "Cookie: gso_access_token=<your_token>"
```

Key agents for the onboarding workflow:

| Agent | Role in Onboarding |
|-------|-------------------|
| `governance_officer` | Verifies contracts against policies |
| `business_orchestrator` | Creates records, sends welcome packets |
| `tool_permission_broker` | Manages billing configuration with gate |

### Step 4: Start a Run (Run Now)

Execute the flagship workflow with a valid payload:

**Frontend:**
1. On the Workflows page, click on `wf_customer_onboarding_v12`
2. Click the **Run Now** button
3. Enter the payload: `{"case_id": "customer_12345"}`
4. Confirm execution

**API:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/workflows/wf_customer_onboarding_v12/runs \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>" \
  -d '{
    "case_id": "customer_12345"
  }'
```

> **Warning:** The `case_id` field is required for the flagship workflow. Omitting it will result in a validation error. Each case_id should be unique to avoid conflicts with existing records.

Expected response:

```json
{
  "run_id": "run_abc123",
  "workflow_id": "wf_customer_onboarding_v12",
  "status": "running",
  "case_id": "customer_12345",
  "started_at": "2026-07-06T14:00:00Z"
}
```

### Step 5: Observe Step Execution

The runtime walks through each step of the bounded state graph. You can observe progress in real-time:

**Frontend:**
1. The run detail view shows each step's status
2. Watch steps transition from `pending` to `running` to `completed`

**API (poll for status):**
```bash
curl http://127.0.0.1:8000/api/v1/workflows/wf_customer_onboarding_v12/runs/run_abc123 \
  -H "Cookie: gso_access_token=<your_token>"
```

#### Step Execution Details

**Step 1: verify_contract**

```json
{
  "step_id": "verify_contract",
  "agent": "governance_officer",
  "tools_used": ["contract_parser", "policy_retriever"],
  "status": "completed",
  "tool_effects": [
    {
      "tool": "contract_parser",
      "action": "parse",
      "result": "contract_valid",
      "clauses_extracted": 12,
      "exceptions_found": 0
    },
    {
      "tool": "policy_retriever",
      "action": "check_compliance",
      "result": "compliant",
      "policies_checked": ["standard_liability", "data_protection"]
    }
  ],
  "duration_ms": 2340
}
```

**Step 2: create_customer_record**

```json
{
  "step_id": "create_customer_record",
  "agent": "business_orchestrator",
  "tools_used": ["crm"],
  "status": "completed",
  "tool_effects": [
    {
      "tool": "crm",
      "action": "create",
      "result": "record_created",
      "record_id": "cust_456",
      "reversible": true,
      "rollback_action": "disable_customer_record"
    }
  ],
  "duration_ms": 1890
}
```

**Step 3: configure_billing** (PAUSED - Human Gate)

```json
{
  "step_id": "configure_billing",
  "agent": "tool_permission_broker",
  "tools_used": [],
  "status": "awaiting_approval",
  "gate_reason": "tool_action_is_irreversible",
  "gate_context": {
    "action": "configure billing for customer_12345",
    "amount": "standard_plan",
    "irreversible": true,
    "requires_reviewer_role": true
  }
}
```

### Step 6: Approve the Human Gate

When the billing step triggers its human gate, a reviewer must approve:

**Frontend:**
1. Navigate to the **Approvals** page (or check notifications)
2. Review the pending approval for `configure_billing`
3. Examine the context: what action is proposed, why it requires approval
4. Click **Approve** to allow the step to proceed

**API:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/approvals/gate_billing_123/approve \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>" \
  -d '{
    "reviewer_notes": "Verified billing configuration matches contract terms.",
    "approved": true
  }'
```

> **Tip:** The reviewer should verify that the proposed billing configuration matches the signed contract terms. The gate context provides all necessary information for this decision.

After approval, the billing step executes:

```json
{
  "step_id": "configure_billing",
  "status": "completed",
  "tool_effects": [
    {
      "tool": "billing_system",
      "action": "configure",
      "result": "billing_active",
      "plan": "standard",
      "first_invoice_date": "2026-08-01",
      "reversible": false
    }
  ],
  "approved_by": "admin@example.com",
  "approved_at": "2026-07-06T14:12:00Z"
}
```

**Step 4: send_welcome_packet**

After billing is configured, the final step sends the welcome packet:

```json
{
  "step_id": "send_welcome_packet",
  "agent": "business_orchestrator",
  "tools_used": ["email"],
  "status": "completed",
  "tool_effects": [
    {
      "tool": "email",
      "action": "send",
      "result": "delivered",
      "recipient": "customer_12345@example.com",
      "template": "welcome_packet_v3"
    }
  ],
  "duration_ms": 1200
}
```

### Step 7: Inspect Audit Logs

After the run completes, review the full audit trail:

**Frontend:**
1. On the run detail page, click the **Audit Log** tab
2. Review each logged event with timestamps, actors, and outcomes

**API:**
```bash
curl http://127.0.0.1:8000/api/v1/audit/runs/run_abc123 \
  -H "Cookie: gso_access_token=<your_token>"
```

The audit log contains entries for:

- Run initiation (who started it, when, with what payload)
- Each step execution (agent, tools used, duration, outcome)
- Human gate creation and resolution (who approved, when, with what notes)
- Tool effects (every external system interaction)
- Memory reads and writes
- Verification check results
- Final run status

### Step 8: Review Memory and Evaluations

The completed run has written several memory items:

**Memory Writes:**

```bash
# View memory items for this run
curl http://127.0.0.1:8000/api/v1/memory?run_id=run_abc123 \
  -H "Cookie: gso_access_token=<your_token>"
```

Expected memory entries:

| Memory Type | Content |
|-------------|---------|
| `event_log` | Raw operational log of all steps |
| `decision_memory` | Why billing was approved (reviewer's rationale) |
| `lessons_learned` | Auto-reflect output (if enabled) |

**Evaluations:**

```bash
# View evaluation metrics
curl http://127.0.0.1:8000/api/v1/evaluations?run_id=run_abc123 \
  -H "Cookie: gso_access_token=<your_token>"
```

Evaluation metrics captured:

```json
{
  "run_id": "run_abc123",
  "workflow_id": "wf_customer_onboarding_v12",
  "metrics": {
    "quality_score": 0.94,
    "compliance_pass_rate": 1.0,
    "average_cycle_time_minutes": 12,
    "escalation_rate": 0.25,
    "unauthorized_tool_attempts": 0,
    "cost_per_case_usd": 0.38
  }
}
```

### Step 9: Review Process Summaries

View how this run contributes to process intelligence:

```bash
curl http://127.0.0.1:8000/api/v1/processes/summary \
  -H "Cookie: gso_access_token=<your_token>"
```

The process summary shows:

- How many times this workflow has been executed
- Average cycle time across all runs
- Conformance rate (actual vs expected path)
- Bottleneck identification (which step takes longest)
- Common exception patterns

### Step 10: Trigger Self-Improvement Pipeline

From the run detail page, you can initiate the improvement cycle:

**Frontend:**
1. On the run detail page, click **Improve**
2. Choose from: **Reflect**, **Run full pipeline**, or individual steps

**API - Step by Step:**

```bash
# Step 1: Reflect on the completed run
curl -X POST http://127.0.0.1:8000/api/v1/improvement/reflect/run_abc123 \
  -H "Cookie: gso_access_token=<your_token>"
```

The reflect step analyzes the run and produces lessons:

```json
{
  "run_id": "run_abc123",
  "lessons": [
    {
      "observation": "Billing gate added 8 minutes to cycle time",
      "suggestion": "Pre-validate billing config in verify_contract step",
      "confidence": 0.72,
      "risk_level": "low"
    }
  ]
}
```

```bash
# Step 2: View accumulated lessons
curl http://127.0.0.1:8000/api/v1/improvement/lessons \
  -H "Cookie: gso_access_token=<your_token>"
```

```bash
# Step 3: Auto-propose a variant based on lessons
curl -X POST http://127.0.0.1:8000/api/v1/improvement/auto-propose \
  -H "Cookie: gso_access_token=<your_token>"
```

The auto-propose creates a **sandbox-only** variant:

```json
{
  "variant_id": "wf_customer_onboarding_v12_variant_a",
  "status": "sandbox_only",
  "changes": [
    "Added pre-validation of billing configuration in verify_contract step",
    "Reduced expected gate wait time by 40%"
  ],
  "requires_evaluation": true
}
```

```bash
# Step 4: Run the evaluation loop
curl -X POST http://127.0.0.1:8000/api/v1/loops/run \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>" \
  -d '{
    "variant_id": "wf_customer_onboarding_v12_variant_a",
    "test_set": "golden_onboarding_cases"
  }'
```

```bash
# Step 5: View the evolution archive
curl http://127.0.0.1:8000/api/v1/evolution/archive \
  -H "Cookie: gso_access_token=<your_token>"
```

### Step 11: Explore the Evolution Population Archive

Navigate to the Evolution page:

**Frontend:**
1. Navigate to `/app/evolution` from the sidebar
2. View the population archive showing all variants
3. Compare variant fitness scores against the production baseline
4. Identify variants eligible for canary deployment

The evolution archive tracks:

- All proposed variants with their lineage
- Fitness scores per variant
- Which variants passed evaluation
- Which variants were canary-deployed
- Which variants were promoted or retired

---

## Understanding tool_effects in Detail

Every tool interaction during workflow execution produces a `tool_effects` record. This is one of the most important concepts for auditing and governance.

### tool_effects Schema

```json
{
  "effect_id": "eff_789",
  "run_id": "run_abc123",
  "step_id": "create_customer_record",
  "tool": "crm",
  "action": "create",
  "input": {
    "name": "Acme Corp",
    "type": "enterprise",
    "contract_id": "contract_001"
  },
  "output": {
    "record_id": "cust_456",
    "status": "active",
    "created_at": "2026-07-06T14:05:22Z"
  },
  "timestamp": "2026-07-06T14:05:22Z",
  "reversible": true,
  "rollback_action": "disable_customer_record",
  "latency_ms": 450,
  "agent": "business_orchestrator"
}
```

### Why tool_effects Matter

1. **Audit compliance** - Every external system change is recorded
2. **Rollback capability** - If a later step fails, previous effects can be reversed
3. **Process Intelligence** - Mining tool_effects reveals actual system behavior
4. **Evolution data** - The fitness function uses effect data to score variants
5. **Incident investigation** - When something goes wrong, tool_effects show exactly what happened

> **Note:** Tool effects are stored durably in the Postgres control plane. They persist even if the workflow run is deleted, ensuring audit completeness.

---

## Real-World Use Cases

### Use Case 1: Multi-Region Customer Onboarding

A global company uses the onboarding workflow across regions with different compliance requirements:

- **US Region:** Standard flow, billing gate at $10,000+
- **EU Region:** Additional GDPR data processing agreement step, human gate for all data storage
- **APAC Region:** Modified verification step for local contract formats

Each region uses a variant of the base DNA, with the Evolution Engine tracking which regional modifications perform best.

**Key Insight:** The bounded state graph allows regional customization within the same framework while maintaining governance standards across all regions.

### Use Case 2: High-Volume SaaS Onboarding

A SaaS company processes 200+ customer onboardings per day:

- Most are low-risk (standard plan, verified identity) and flow through without human gates
- Only 12% trigger the billing gate (enterprise plans or custom pricing)
- Auto-reflect identifies that 85% of gate approvals are immediate, suggesting the threshold could be adjusted
- Evolution Engine proposes a variant that only gates billing above $50,000 (reducing gate frequency by 60%)

**Key Insight:** The fitness metrics (cycle_time, escalation_rate) quantify the cost of gates, enabling evidence-based decisions about when gates are necessary.

### Use Case 3: Compliance-Heavy Financial Onboarding

A financial services firm requires extensive KYC/AML checks:

- **Additional Steps:** identity_verification, sanctions_check, risk_scoring, compliance_review
- **Multiple Gates:** Identity verification (manual), sanctions match (escalation), large transactions
- **Extended Memory:** Regulatory decisions stored for 7-year retention
- **Strict Fitness:** Compliance pass rate weighted 3x higher than efficiency

**Key Insight:** The DNA schema accommodates heavily regulated workflows by adding steps and gates without changing the underlying execution engine.

---

## Best Practices

### 1. Use Meaningful case_id Values

The `case_id` is your primary key for tracking a business process instance across the system:

```json
// Good: descriptive and traceable
{"case_id": "onb_acme_corp_2026_q3"}

// Bad: opaque
{"case_id": "12345"}
```

### 2. Review Gates Promptly

Human gates block workflow progress. Establish SLAs for gate review:

- **Low-risk gates:** Review within 1 hour
- **Medium-risk gates:** Review within 4 hours
- **High-risk gates:** Review within 1 business day

### 3. Inspect tool_effects After Every Run

Make it a habit to review tool_effects, especially for:

- First-time workflow executions
- Runs with unexpected outcomes
- Runs that triggered gates

### 4. Run the Improvement Pipeline Regularly

Do not wait for problems to trigger improvement. After every 10-20 successful runs:

1. Reflect on recent runs
2. Review accumulated lessons
3. Consider whether auto-propose suggestions merit evaluation

### 5. Monitor the Evolution Archive

Check the evolution archive weekly to:

- Identify promising variants
- Review canary deployment results
- Retire variants that did not improve metrics

### 6. Track Process Intelligence Trends

The PI layer reveals patterns invisible in individual runs:

- Increasing bottleneck times may indicate process degradation
- Conformance drops may signal workflow drift
- New exception patterns may require DNA updates

### 7. Document Gate Decisions

When approving or rejecting a human gate, always provide meaningful reviewer notes:

```json
{
  "approved": true,
  "reviewer_notes": "Verified billing matches contract section 4.2. Standard enterprise plan."
}
```

These notes feed into decision memory and help the Evolution Engine understand approval patterns.

---

## Chapter Summary

In this chapter, you walked through:

- The **E1 operator path** end-to-end: login, list workflows, run with payload, approve gates, inspect results, improve
- How the flagship **customer onboarding workflow** executes step by step
- How **human gates** pause execution for irreversible actions and require reviewer approval
- How **tool_effects** create a durable audit trail of all system interactions
- How **auto-reflect** generates lessons from completed runs
- How the **self-improvement pipeline** (Reflect, Propose, Evaluate, Canary) evolves workflows
- How the **Evolution population archive** tracks all variants and their fitness

The E1 path proves that the system works as an integrated whole: from authentication through execution through governance through self-improvement.

---

## Knowledge Check Quiz

Test your understanding of business process execution:

**Question 1:** What is the required payload field for the flagship customer onboarding workflow?

<details>
<summary>Show Answer</summary>
The `case_id` field is required. Example: `{"case_id": "customer_12345"}`. The workflow will not start without a valid case_id.
</details>

**Question 2:** At which step does the human gate trigger in the onboarding workflow, and why?

<details>
<summary>Show Answer</summary>
The human gate triggers at the `configure_billing` step because billing configuration is an irreversible action (the guardrail condition `tool_action_is_irreversible == true` is met). A reviewer must approve before the billing system is configured.
</details>

**Question 3:** What are the four steps of the self-improvement pipeline?

<details>
<summary>Show Answer</summary>
Reflect (analyze the run and extract lessons), Propose (auto-generate a sandbox-only variant), Evaluate (test the variant against golden tasks and regression suites), and Canary (deploy to a small scope with auto-rollback on failure). Optionally followed by Promote if all criteria pass.
</details>

**Question 4:** What does `tool_action_is_irreversible == true` mean in the context of guardrails?

<details>
<summary>Show Answer</summary>
It means the tool call being attempted cannot be undone after execution. For billing configuration, once a billing plan is set up and an invoice cycle begins, it cannot be simply reverted. This triggers the human gate to ensure a human reviews and approves the action before it executes.
</details>

**Question 5:** What information does a reviewer see when a human gate is triggered?

<details>
<summary>Show Answer</summary>
The reviewer sees the gate context including: what action is proposed, why it requires approval (gate_reason), the specific details of the proposed change (amount, plan, customer), whether the action is irreversible, and all preceding step results. This enables an informed approval decision.
</details>

**Question 6:** What happens after auto-propose creates a variant?

<details>
<summary>Show Answer</summary>
The variant is created with `status: sandbox_only`. It must pass evaluation (testing against golden tasks, regression tests, adversarial tests), potentially canary deployment, and human sign-off (if the risk tier requires it) before it can be promoted to production. The variant never mutates production directly.
</details>

**Question 7:** How does the system prevent a proposed variant from accidentally reaching production?

<details>
<summary>Show Answer</summary>
Multiple safeguards: (1) Variants are created with `sandbox_only` status by default, (2) the Evolution Manager is architecturally prohibited from mutating production directly, (3) promotion requires passing all regression and adversarial tests, (4) high-risk variants require human sign-off, (5) canary deployment with auto-rollback on metric regression, (6) `business:validate` and `activate_workflow_version` enforce production DNA safety checks.
</details>

---

## Next Steps

In the next chapter, you will learn how to configure and use the tool adapters that power workflow execution, including their permission models, effect tracking, and fail-closed behavior.
