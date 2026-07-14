# Chapter 2.3: Tool Adapter Integration

![Tool Adapter Architecture](../assets/02-03-tool-adapter-architecture.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Understand the architecture of tool adapters and their role in workflow execution
2. Configure each of the six shipped tool adapters (CRM, billing, email, audit, contract_parser, policy_retriever)
3. Implement permission scoping using the Tool Permission Broker
4. Track and inspect tool_effects for audit and compliance
5. Handle adapter failures using fail-closed behavior patterns
6. Set up basic integrations between adapters and external systems

## Prerequisites

Before starting this chapter, ensure you have:

- Completed Chapters 2.1 and 2.2
- A running backend instance with database connectivity
- Understanding of Workflow DNA step definitions (agents and tools)
- Familiarity with REST API patterns and JSON payloads

---

## What Are Tool Adapters?

Tool adapters are the interface between workflow agents and external systems. They provide a controlled, auditable, permission-scoped mechanism for agents to interact with business tools like CRM systems, billing platforms, email services, and compliance databases.

Every tool adapter in the system follows a strict execution pattern:

```text
Request -> Permission Check -> Adapter Execution -> tool_effects Capture -> Audit Log -> Response
```

This pattern ensures:

1. **No unauthorized access** - The Permission Broker validates every request
2. **Full auditability** - Every interaction is logged with provenance
3. **Durable effects** - All outcomes are captured as tool_effects
4. **Fail-closed safety** - Errors block execution rather than allowing silent failures

> **Warning:** Tool adapters are currently implemented as **local adapters** with durable `tool_effects`. Live connections to external CRM/email/billing SaaS platforms are a future enhancement. The adapter interface is identical whether executing locally or against live systems.

---

## The Permission Model

### Tool Permission Broker

The Tool Permission Broker is the gatekeeper for all tool access. Before any adapter can execute, the broker validates:

1. **DNA Allow-List** - Is this tool listed in the current step's `tools[]` array?
2. **RBAC Check** - Does the executing agent have the required role?
3. **Gate Check** - Does this action require human approval first?
4. **Scope Validation** - Is the action within the agent's permitted scope?

```text
Agent Request
    |
    v
[DNA Allow-List] -- tool not in step.tools[] --> BLOCKED
    |
    v (tool allowed)
[RBAC Check] -- agent lacks permission --> BLOCKED
    |
    v (role valid)
[Gate Check] -- irreversible/high-risk --> HUMAN GATE
    |
    v (approved or not gated)
[Scope Validation] -- out of scope --> BLOCKED
    |
    v (in scope)
[Adapter Execution]
```

### Permission Scoping Rules

Each adapter has a permission scope that defines what operations are allowed:

| Adapter | Read Operations | Write Operations | Requires Gate |
|---------|----------------|------------------|---------------|
| `crm` | query records, search | create, update, disable | create/disable: no gate (reversible) |
| `billing` | view plans, invoices | configure, void | configure: GATE (irreversible) |
| `email` | view templates | send | send to external: GATE |
| `audit` | query logs | write entries | No gate (append-only) |
| `contract_parser` | parse, extract | None | No gate (read-only) |
| `policy_retriever` | query policies | None | No gate (read-only) |

> **Note:** The intersection of DNA tools, RBAC roles, and gate conditions determines what an agent can actually do. An agent must satisfy ALL three to execute a tool action.

---

## Shipped Tool Adapters

### 1. CRM Adapter

The CRM adapter manages customer records throughout the workflow lifecycle.

**Capabilities:**

```yaml
adapter: crm
operations:
  - create: Create new customer records
  - read: Query existing records by ID or criteria
  - update: Modify record fields
  - disable: Soft-delete (reversible deactivation)
  - search: Full-text search across records
```

**API Examples:**

```bash
# Create a customer record (via workflow step)
# This happens automatically when the step executes
# The tool_effects record shows:
{
  "tool": "crm",
  "action": "create",
  "input": {
    "name": "Acme Corporation",
    "type": "enterprise",
    "contract_id": "contract_001",
    "region": "us-east"
  },
  "output": {
    "record_id": "cust_456",
    "status": "active",
    "created_at": "2026-07-06T14:05:22Z"
  },
  "reversible": true,
  "rollback_action": "disable_customer_record"
}
```

**Configuration:**

```yaml
# Tool adapter configuration
crm:
  adapter_type: "local"
  storage: "postgres"
  operations_allowed: ["create", "read", "update", "disable", "search"]
  requires_gate_for: []
  reversible_operations: ["create", "update", "disable"]
  rollback_mapping:
    create: "disable"
    update: "restore_previous"
    disable: "enable"
```

### 2. Billing Adapter

The billing adapter manages financial operations including plan configuration and invoicing.

**Capabilities:**

```yaml
adapter: billing
operations:
  - configure: Set up billing plans and schedules
  - view_plan: Read current plan details
  - view_invoices: List invoice history
  - void: Cancel a pending invoice (limited window)
```

**API Examples:**

```bash
# Configure billing (requires human gate approval first)
{
  "tool": "billing",
  "action": "configure",
  "input": {
    "customer_id": "cust_456",
    "plan": "enterprise_standard",
    "billing_cycle": "monthly",
    "start_date": "2026-08-01"
  },
  "output": {
    "billing_id": "bill_789",
    "status": "active",
    "first_invoice_date": "2026-08-01",
    "amount": 2500.00
  },
  "reversible": false,
  "gate_required": true,
  "approved_by": "admin@example.com"
}
```

> **Warning:** Billing configuration is marked as **irreversible** because once an invoice cycle begins, reversing it requires manual intervention with the payment processor. This is why it always triggers a human gate.

**Configuration:**

```yaml
billing:
  adapter_type: "local"
  storage: "postgres"
  operations_allowed: ["configure", "view_plan", "view_invoices", "void"]
  requires_gate_for: ["configure"]
  reversible_operations: ["void"]
  irreversible_operations: ["configure"]
  rollback_mapping:
    void: "reinstate_invoice"
```

### 3. Email Adapter

The email adapter handles all outbound communications.

**Capabilities:**

```yaml
adapter: email
operations:
  - send: Send templated emails
  - view_templates: List available templates
  - preview: Generate email preview without sending
```

**API Examples:**

```bash
# Send welcome packet email
{
  "tool": "email",
  "action": "send",
  "input": {
    "recipient": "contact@acme.com",
    "template": "welcome_packet_v3",
    "variables": {
      "customer_name": "Acme Corporation",
      "account_manager": "Jane Smith",
      "portal_url": "https://portal.example.com/acme"
    }
  },
  "output": {
    "message_id": "msg_012",
    "status": "delivered",
    "sent_at": "2026-07-06T14:15:00Z"
  },
  "reversible": false
}
```

**Configuration:**

```yaml
email:
  adapter_type: "local"
  storage: "postgres"
  operations_allowed: ["send", "view_templates", "preview"]
  requires_gate_for: []
  reversible_operations: []
  templates_path: "business/materials/email-templates/"
```

### 4. Audit Adapter

The audit adapter provides append-only logging for compliance and governance.

**Capabilities:**

```yaml
adapter: audit
operations:
  - write: Append an audit entry
  - query: Search audit history
  - export: Generate audit reports
```

**API Examples:**

```bash
# Write audit entry (happens automatically for every step)
{
  "tool": "audit",
  "action": "write",
  "input": {
    "event_type": "workflow_step_completed",
    "workflow_id": "wf_customer_onboarding_v12",
    "step_id": "verify_contract",
    "actor": "governance_officer",
    "outcome": "success",
    "evidence": ["contract_valid", "policy_compliant"]
  },
  "output": {
    "audit_id": "aud_345",
    "timestamp": "2026-07-06T14:03:00Z",
    "immutable": true
  },
  "reversible": false
}
```

> **Note:** The audit adapter is append-only by design. Once an entry is written, it cannot be modified or deleted. This ensures the integrity of the audit trail for governance reviews.

**Configuration:**

```yaml
audit:
  adapter_type: "local"
  storage: "postgres"
  operations_allowed: ["write", "query", "export"]
  requires_gate_for: []
  reversible_operations: []
  retention_days: 2555  # 7 years for compliance
  immutable: true
```

### 5. Contract Parser Adapter

The contract parser extracts structured information from contract documents.

**Capabilities:**

```yaml
adapter: contract_parser
operations:
  - parse: Extract clauses and terms from a contract document
  - validate: Check contract against standard templates
  - extract_clauses: Return specific clause types
  - identify_exceptions: Flag non-standard terms
```

**API Examples:**

```bash
# Parse a contract document
{
  "tool": "contract_parser",
  "action": "parse",
  "input": {
    "document_id": "doc_contract_v3",
    "extract_types": ["liability", "data_protection", "termination", "pricing"]
  },
  "output": {
    "clauses_found": 12,
    "exceptions": [],
    "standard_compliance": true,
    "risk_flags": [],
    "parsed_at": "2026-07-06T14:02:00Z"
  },
  "reversible": true
}
```

**Configuration:**

```yaml
contract_parser:
  adapter_type: "local"
  storage: "memory"
  operations_allowed: ["parse", "validate", "extract_clauses", "identify_exceptions"]
  requires_gate_for: []
  reversible_operations: ["parse", "validate", "extract_clauses", "identify_exceptions"]
  read_only: true
```

### 6. Policy Retriever Adapter

The policy retriever queries the compliance policy database for relevant rules and SOPs.

**Capabilities:**

```yaml
adapter: policy_retriever
operations:
  - query: Search policies by topic or keyword
  - check_compliance: Validate an action against applicable policies
  - list_applicable: Return all policies for a given domain/action
```

**API Examples:**

```bash
# Check compliance for a billing action
{
  "tool": "policy_retriever",
  "action": "check_compliance",
  "input": {
    "domain": "billing",
    "action": "configure_enterprise_plan",
    "context": {
      "customer_type": "enterprise",
      "contract_value": 250000,
      "region": "eu"
    }
  },
  "output": {
    "compliant": true,
    "policies_checked": [
      "enterprise_billing_policy_v2",
      "eu_data_protection_billing",
      "financial_controls_sop"
    ],
    "requirements_met": ["legal_review_complete", "risk_score_acceptable"],
    "warnings": []
  },
  "reversible": true
}
```

**Configuration:**

```yaml
policy_retriever:
  adapter_type: "local"
  storage: "memory"
  operations_allowed: ["query", "check_compliance", "list_applicable"]
  requires_gate_for: []
  reversible_operations: ["query", "check_compliance", "list_applicable"]
  read_only: true
  policy_sources:
    - "business/knowledge-base/rules/"
    - "business/materials/regulations/"
    - "business/materials/sops/"
```

---

## Effect Tracking System

### How tool_effects Are Captured

Every adapter call produces a `tool_effects` record that is persisted to the Postgres control plane:

```json
{
  "effect_id": "eff_unique_id",
  "run_id": "run_abc123",
  "step_id": "create_customer_record",
  "workflow_id": "wf_customer_onboarding_v12",
  "tool": "crm",
  "action": "create",
  "input": { },
  "output": { },
  "timestamp": "2026-07-06T14:05:22Z",
  "duration_ms": 450,
  "agent": "business_orchestrator",
  "reversible": true,
  "rollback_action": "disable_customer_record",
  "status": "success"
}
```

### Querying tool_effects

```bash
# Get all effects for a run
curl http://127.0.0.1:8000/api/v1/workflows/wf_customer_onboarding_v12/runs/run_abc123/effects \
  -H "Cookie: gso_access_token=<your_token>"

# Get effects for a specific tool
curl "http://127.0.0.1:8000/api/v1/tool-effects?tool=crm&run_id=run_abc123" \
  -H "Cookie: gso_access_token=<your_token>"
```

### Effect Lifecycle

```text
1. Agent requests tool action
2. Permission Broker validates
3. Adapter executes action
4. Effect record created (status: success/failure)
5. Effect persisted to Postgres
6. Audit log entry appended
7. If step fails later: rollback uses effect records to determine undo actions
```

---

## Fail-Closed Behavior

A critical design principle of the tool adapter system is **fail-closed behavior**: when something goes wrong, the system blocks further execution rather than allowing potentially unsafe operations to proceed.

### What Fail-Closed Means

| Scenario | Behavior |
|----------|----------|
| Permission denied | Step is BLOCKED, run pauses |
| Adapter execution error | Step FAILS, rollback triggered |
| Timeout exceeded | Step FAILS, incident logged |
| Invalid input | Step BLOCKED before execution |
| External system unreachable | Step FAILS, retry with backoff |

### Fail-Closed vs Fail-Open

```text
Fail-Closed (this system):
  Error -> Block execution -> Log incident -> Await human resolution
  Result: No unintended actions ever occur

Fail-Open (NEVER used):
  Error -> Continue with default/empty result -> Risk unintended consequences
  Result: Potentially dangerous state changes
```

> **Warning:** The system NEVER fails open. If a tool adapter cannot complete its action successfully and safely, the step fails and the workflow either retries (with backoff) or pauses for human intervention.

### Error Handling Patterns

```python
# Conceptual adapter execution pattern
def execute_tool_action(step, action, input_data):
    # 1. Permission check (fail-closed)
    if not permission_broker.validate(step, action):
        raise PermissionDenied(f"Tool {action.tool} not permitted for step {step.id}")

    # 2. Gate check (pause if required)
    if requires_human_gate(step, action):
        pause_for_approval(step, action)
        return  # Execution resumes after approval

    # 3. Execute adapter (fail-closed on error)
    try:
        result = adapter.execute(action, input_data)
    except AdapterError as e:
        log_incident(step, action, e)
        trigger_rollback(step)
        raise StepFailed(f"Adapter error: {e}")

    # 4. Record effect (always, even on failure)
    record_tool_effect(step, action, input_data, result)

    # 5. Audit log (always)
    write_audit_entry(step, action, result)

    return result
```

### Incident Response for Adapter Failures

When an adapter fails:

1. The step is marked as `failed`
2. An incident record is created with full context
3. Rollback steps for previously completed steps are evaluated
4. The Incident Commander agent is notified
5. Human operators can review the incident and decide on resolution

---

## Setting Up Basic Integrations

### Step 1: Register a New Tool Adapter

To add a new tool adapter to the system:

```yaml
# business/schemas/tool-adapters/my_new_tool.yaml
adapter:
  id: "my_new_tool"
  name: "My New Tool"
  type: "local"
  description: "Integrates with XYZ system"
  operations:
    - id: "action_one"
      description: "Performs action one"
      reversible: true
      rollback: "undo_action_one"
    - id: "action_two"
      description: "Performs action two"
      reversible: false
      requires_gate: true
  permissions:
    roles_required: ["operator", "admin"]
    scopes: ["read", "write"]
```

### Step 2: Define Permission Rules

```yaml
# Permission configuration for the new tool
permissions:
  tool_id: "my_new_tool"
  allowed_agents: ["business_orchestrator", "governance_officer"]
  gate_conditions:
    - "action == 'action_two'"
    - "risk_tier >= 4"
  scope_limits:
    max_records_per_call: 100
    allowed_domains: ["operations"]
```

### Step 3: Reference in Workflow DNA

```yaml
steps:
  - id: "use_new_tool"
    agent: "business_orchestrator"
    tools: ["my_new_tool"]
```

### Step 4: Validate Integration

```bash
# Validate that the tool is properly registered
npm run business:validate

# Run security checks on tool permissions
npm run business:security
```

---

## Real-World Use Cases

### Use Case 1: Multi-Tool Workflow Step

A contract review step that uses multiple tools in sequence:

```yaml
- id: "comprehensive_contract_review"
  agent: "governance_officer"
  tools: ["contract_parser", "policy_retriever", "crm"]
```

The agent:
1. Uses `contract_parser` to extract clauses
2. Uses `policy_retriever` to check each clause against policies
3. Uses `crm` to verify customer history and risk profile
4. Each tool call produces its own tool_effects record

**Result:** Three tool_effects records provide a complete audit trail of the review process.

### Use Case 2: Conditional Tool Usage

An agent that uses different tools based on contract findings:

```yaml
- id: "handle_contract_exceptions"
  agent: "governance_officer"
  tools: ["contract_parser", "policy_retriever", "email", "audit"]
```

If the contract parser finds exceptions:
- `policy_retriever` checks if exceptions are pre-approved
- If not pre-approved: trigger human gate
- `email` notifies legal team of pending review
- `audit` logs the exception detection

**Result:** The bounded tool list ensures the agent cannot access unauthorized tools even when handling exceptions.

### Use Case 3: Rollback After Partial Failure

A workflow where step 3 fails after steps 1 and 2 succeeded:

```text
Step 1: create_customer_record (CRM) - SUCCESS
Step 2: configure_notifications (email) - SUCCESS
Step 3: configure_billing (billing) - FAILED (external system down)
```

Rollback process:
1. System reads tool_effects for steps 1 and 2
2. Executes rollback for step 2: cancel notification preferences
3. Executes rollback for step 1: disable customer record
4. Logs all rollback actions as new tool_effects
5. Incident recorded for human review

**Result:** The system returns to a clean state with full audit trail of both the original actions and their rollbacks.

---

## Best Practices

### 1. Use Read-Only Adapters Where Possible

Prefer `contract_parser` and `policy_retriever` (read-only) over write-capable tools. Read-only tools are inherently safe and never require gates.

### 2. Define Granular Rollback Actions

Every write operation should have a specific, tested rollback:

```yaml
rollback_mapping:
  create: "disable"          # Not "delete" - preserve audit trail
  update: "restore_previous" # Keep history
  configure: "void"          # Explicit cancellation
```

### 3. Set Conservative Gate Thresholds

Start with gates on all write operations, then relax based on evidence:

```yaml
# Start conservative
requires_gate_for: ["create", "update", "configure", "send"]

# After evidence shows safety (e.g., 100+ successful executions)
requires_gate_for: ["configure"]  # Only irreversible actions
```

### 4. Monitor Adapter Latency

Track `duration_ms` in tool_effects to identify performance degradation:

- CRM operations: expect < 500ms
- Billing operations: expect < 2000ms
- Email operations: expect < 1000ms
- Parser operations: expect < 3000ms (document-dependent)

### 5. Test Adapter Failures Explicitly

Include failure scenarios in your evaluation tests:

```yaml
# Golden task: adapter timeout
test_case:
  scenario: "crm_adapter_timeout"
  expected_behavior: "step_fails_and_triggers_rollback"
  expected_tool_effects: ["timeout_recorded", "rollback_initiated"]
```

### 6. Never Bypass the Permission Broker

All tool access must go through the Permission Broker, even for debugging:

```bash
# Wrong: direct adapter call bypasses permissions
# adapter.execute("crm", "create", {...})

# Correct: go through the workflow execution engine
# which enforces permission broker validation
```

---

## Chapter Summary

In this chapter, you learned:

- **Tool adapters** are the controlled interface between agents and external systems
- The **Permission Broker** validates every tool request against DNA allow-lists, RBAC, gates, and scopes
- Six adapters are shipped: **CRM, billing, email, audit, contract_parser, policy_retriever**
- **tool_effects** capture every adapter interaction as a durable, auditable record
- The system uses **fail-closed behavior** - errors block execution, never fail silently
- **Rollback plans** use tool_effects to reverse previous actions when failures occur
- Adapters currently run as **local adapters** with live SaaS integration as a future enhancement

---

## Knowledge Check Quiz

Test your understanding of tool adapter integration:

**Question 1:** What four checks does the Permission Broker perform before allowing a tool action?

<details>
<summary>Show Answer</summary>
(1) DNA Allow-List - is the tool listed in the step's tools[] array, (2) RBAC Check - does the agent have the required role, (3) Gate Check - does the action require human approval, (4) Scope Validation - is the action within the agent's permitted scope. All four must pass for the action to proceed.
</details>

**Question 2:** Which tool adapters are read-only and why does that matter?

<details>
<summary>Show Answer</summary>
`contract_parser` and `policy_retriever` are read-only. This matters because read-only tools are inherently safe (they cannot modify state), never require human gates, are always reversible (nothing to undo), and have minimal risk. They can be used freely without governance overhead.
</details>

**Question 3:** What does "fail-closed" mean in the context of tool adapters?

<details>
<summary>Show Answer</summary>
Fail-closed means that when any error occurs (permission denied, adapter failure, timeout, invalid input), the system blocks further execution rather than continuing with a default or empty result. The step fails, rollback may be triggered, and the incident is logged for human review. The system never fails open (continues despite errors).
</details>

**Question 4:** Why is billing configuration marked as irreversible?

<details>
<summary>Show Answer</summary>
Billing configuration is irreversible because once a billing plan is activated and an invoice cycle begins, reversing it requires manual intervention with payment processors, potential refunds, and accounting adjustments. These cannot be automated safely, so the action triggers a mandatory human gate before execution.
</details>

**Question 5:** How does the system handle rollback when a later step fails?

<details>
<summary>Show Answer</summary>
The system reads tool_effects records for all previously completed steps, then executes the rollback_action defined for each effect in reverse order. Each rollback action is itself recorded as a new tool_effect, creating a complete audit trail of both the original actions and their reversals. The Incident Commander is notified for human review.
</details>

**Question 6:** What is the relationship between tool_effects and the Evolution Engine?

<details>
<summary>Show Answer</summary>
The Evolution Engine uses tool_effects data to calculate fitness metrics for workflow variants. Effect records provide data on latency, success rates, cost, and outcomes that feed into the fitness function. This enables evidence-based comparison of variants rather than subjective evaluation.
</details>

---

## Next Steps

In the next chapter, you will learn how to use the Process Intelligence layer to analyze event logs, discover processes, check conformance, and identify bottlenecks in your business operations.
