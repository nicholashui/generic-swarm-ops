# Chapter 3.1: Custom Domain Pack Development

## Learning Objectives

By the end of this chapter, you will be able to:

1. Understand the Domain Pack architecture and how packs plug into the host runtime
2. Create a new Domain Pack from the `example_research` skeleton
3. Define `manifest.json` and `agent_spec.json` with ALC (Autonomous Learning Capability) fields
4. Register a Domain Pack via both CLI and API
5. Configure Wave progression (0-4) and understand the activation gate
6. Validate pack schemas and run inventory checks
7. Set up evaluation corpus overlays for your domain

## Prerequisites

- Completed Section 1 (Core System Fundamentals) and Section 2 (Intermediate Workflows)
- Access to a running Generic Swarm Ops instance (backend + frontend)
- Familiarity with JSON Schema validation
- Understanding of agent-based workflow concepts
- Node.js and Python installed in your development environment

---

## Architecture Overview

![Domain Pack Architecture](../assets/03-01-domain-pack-architecture.svg)

A **Domain Pack** is a self-contained Multi-Model Agent (MMA) system that lives under `business/<domain_id>/` and plugs into the host runtime without forking the FastAPI backend, runtime services, governance, or evolution engine. This architecture enables multiple business domains to share the same infrastructure while maintaining strict isolation boundaries.

### Non-Negotiable Design Rules

The Domain Pack architecture enforces three non-negotiable rules:

| ID | Rule | Rationale |
|----|------|-----------|
| **N1** | Domain business logic stays in the pack path; agents gain ALC for autonomous learning | Separation of concerns; host remains universal |
| **N2** | Any domain onboards via manifest + artifacts; host remains universal | Prevents host fork fragmentation |
| **N3** | Video pack retains all 114 va agents + process index; inventory CI enforces | Reference implementation integrity |

> **Note:** These rules are enforced both at CI time (via inventory checks and schema validation) and at runtime (via the registration API).

---

## Step-by-Step: Creating a Custom Domain Pack

### Step 1: Understand the Directory Layout

Every Domain Pack follows a standardized directory structure:

```text
business/<domain_id>/
  manifest.json            # Pack identity, version, dependencies
  agents/
    <pack_id>/
      agent_spec.json      # Agent definition with ALC fields
      SPEC.md              # Human-readable agent specification
      ...
  workflows/               # Workflow DNA YAML files
  tools/                   # Domain-specific tool adapters
  evals/                   # Evaluation corpus (golden, regression, adversarial)
  knowledge/seeds/         # Initial knowledge base documents
  policies/                # Domain governance overrides
  ui/                      # Domain-specific frontend components
```

> **Tip:** Use the `example_research` skeleton as your starting point. It provides all required files in the correct structure with placeholder values you can customize.

### Step 2: Copy the Skeleton Pack

Begin by copying the example skeleton to create your new domain:

```bash
# Create your new domain pack from the skeleton
cp -r business/example_research/ business/my_domain/

# Verify the structure
tree business/my_domain/
```

Expected output:

```text
business/my_domain/
├── manifest.json
├── agents/
│   └── my_domain/
│       ├── agent_spec.json
│       └── SPEC.md
├── workflows/
├── tools/
├── evals/
├── knowledge/
│   └── seeds/
├── policies/
└── ui/
```

### Step 3: Define the Domain Manifest

The `manifest.json` is the entry point for domain registration. It declares pack identity, version, agent roster, and runtime requirements.

**Schema reference:** `business/schemas/domain-manifest.schema.json`

```json
{
  "$schema": "../schemas/domain-manifest.schema.json",
  "domain_id": "my_domain",
  "display_name": "My Custom Domain",
  "version": "1.0.0",
  "description": "A custom domain pack for [your use case]",
  "owner": "team@example.com",
  "wave": 1,
  "agents": {
    "roster_count": 5,
    "roster": [
      "intake_agent",
      "analysis_agent",
      "synthesis_agent",
      "review_agent",
      "orchestrator"
    ]
  },
  "workflows": [
    "wf_primary_process_v1"
  ],
  "tools": {
    "namespace": "my_domain",
    "adapters": [
      "my_domain.search",
      "my_domain.analyze",
      "my_domain.generate"
    ]
  },
  "knowledge": {
    "seed_documents": 3,
    "embedding_tier": 0
  },
  "evals": {
    "golden_tasks": 10,
    "regression_tests": 5
  },
  "dependencies": {
    "min_host_version": "1.0.0",
    "required_services": ["postgres", "knowledge_store"]
  }
}
```

> **Warning:** The `domain_id` must be a valid Python/JavaScript identifier (lowercase, underscores, no hyphens). It becomes the namespace prefix for all tools, memory scopes, and agent identifiers within the pack.

### Step 4: Create Agent Specifications with ALC Fields

Each agent within your pack requires an `agent_spec.json` that defines its capabilities, role, and Autonomous Learning Capability (ALC) configuration.

**Schema reference:** `business/schemas/agent-spec.schema.json`

```json
{
  "$schema": "../../schemas/agent-spec.schema.json",
  "agent_id": "my_domain.analysis_agent",
  "pack_id": "my_domain",
  "display_name": "Analysis Agent",
  "role": "analyzer",
  "description": "Performs deep analysis on incoming data and generates structured insights",
  "status": "draft",
  "requires_alc": true,
  "alc_version": "1.0.0",
  "alc_config": {
    "allowed_memory_scopes": ["agent", "organization"],
    "learning_rate": "conservative",
    "max_lessons_per_run": 3,
    "lesson_retention_days": 90
  },
  "hooks": {
    "reflect": true,
    "pre_execute": false,
    "post_execute": true
  },
  "tools": [
    "my_domain.search",
    "my_domain.analyze",
    "knowledge.search"
  ],
  "risk_tier": 2,
  "capabilities": [
    "data_analysis",
    "pattern_recognition",
    "report_generation"
  ],
  "constraints": {
    "max_tokens_per_turn": 4096,
    "max_tool_calls_per_step": 5,
    "timeout_seconds": 120
  }
}
```

#### ALC Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `requires_alc` | boolean | Yes | Whether the agent needs autonomous learning |
| `alc_version` | string | If ALC | Semantic version of the ALC configuration |
| `alc_config.allowed_memory_scopes` | array | If ALC | Must include `"agent"` at minimum |
| `alc_config.learning_rate` | string | No | `"conservative"`, `"moderate"`, or `"aggressive"` |
| `alc_config.max_lessons_per_run` | integer | No | Cap on lessons extracted per workflow run |
| `hooks.reflect` | boolean | If ALC | Must be `true` for ALC activation |

> **Note:** The ALC activation gate will deny `PATCH /api/v1/agents/{id}` to `active` status unless: (1) `requires_alc` is false, OR (2) `alc_version` is set, `allowed_memory_scopes` includes `"agent"`, and `hooks.reflect` is `true`.

### Step 5: Define Workflow DNA

Create workflow definitions in the `workflows/` directory. Workflow DNA files define the execution graph, agent assignments, and governance controls:

```yaml
# business/my_domain/workflows/wf_primary_process_v1.yaml
workflow_id: wf_primary_process_v1
domain: my_domain
version: 1
display_name: "Primary Analysis Process"
description: "End-to-end analysis workflow for incoming data"
risk_tier: 2

steps:
  - id: intake
    agent: my_domain.intake_agent
    action: receive_and_classify
    risk_tier: 0
    outputs: [classification, priority]

  - id: analyze
    agent: my_domain.analysis_agent
    action: deep_analysis
    risk_tier: 2
    inputs: [classification]
    outputs: [analysis_report]
    requires_approval: false

  - id: synthesize
    agent: my_domain.synthesis_agent
    action: generate_summary
    risk_tier: 2
    inputs: [analysis_report]
    outputs: [summary, recommendations]

  - id: review
    agent: my_domain.review_agent
    action: quality_check
    risk_tier: 3
    inputs: [summary, recommendations]
    outputs: [final_report]
    requires_approval: true
    approval_role: reviewer

orchestrator: my_domain.orchestrator
evaluation:
  golden_task_set: "evals/golden-tasks/"
  regression_set: "evals/regression/"
```

### Step 6: Create Evaluation Corpus

The evaluation corpus is critical for the Evolution Sandbox to validate changes. Create at least golden tasks:

```json
// business/my_domain/evals/golden-tasks/task_001.json
{
  "task_id": "golden_001",
  "description": "Standard analysis of quarterly report data",
  "input": {
    "case_id": "test_quarterly_q2",
    "data_type": "financial_report",
    "priority": "normal"
  },
  "expected_output": {
    "classification": "financial_analysis",
    "analysis_complete": true,
    "recommendations_count_min": 3
  },
  "evaluation_criteria": {
    "quality_score_min": 0.85,
    "compliance_pass": true,
    "max_steps": 10,
    "max_duration_seconds": 300
  }
}
```

> **Tip:** Aim for at least 10 golden tasks covering the primary success paths, 5 regression tests for known edge cases, and 3 adversarial tests for error handling.

### Step 7: Register the Domain Pack via CLI

The CLI registration tool validates your pack against all schemas and optionally produces a receipt:

```bash
# Dry run - validates without registering
python scripts/business/register_domain.py \
  --manifest business/my_domain/manifest.json \
  --dry-run

# Full registration
python scripts/business/register_domain.py \
  --manifest business/my_domain/manifest.json
```

Expected output for a successful dry run:

```text
[VALIDATE] Loading manifest: business/my_domain/manifest.json
[VALIDATE] Schema check: PASS
[VALIDATE] Agent specs (5): ALL VALID
[VALIDATE] ALC fields: 3 agents require ALC, all properly configured
[VALIDATE] Workflow DNA: 1 workflow validated
[VALIDATE] Eval corpus: 10 golden, 5 regression
[DRY-RUN] Registration would succeed. Agents loaded as draft/registered.
```

### Step 8: Register via API (Wave 1+)

For programmatic registration, use the REST API:

```bash
# Register by manifest path
curl -X POST http://127.0.0.1:8000/api/v1/domains/register \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "manifest_path": "business/my_domain/manifest.json"
  }'

# Or register with inline manifest
curl -X POST http://127.0.0.1:8000/api/v1/domains/register \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "manifest": {
      "domain_id": "my_domain",
      "display_name": "My Custom Domain",
      "version": "1.0.0",
      "agents": { "roster_count": 5, "roster": ["..."] }
    }
  }'
```

**Response:**

```json
{
  "status": "registered",
  "domain_id": "my_domain",
  "agents_loaded": 5,
  "agents_status": "draft",
  "message": "Domain registered. Agents in draft state. Use PATCH /agents/{id} to activate."
}
```

> **Warning:** Registration loads agents as `draft/registered` status. It does NOT auto-activate agents. You must explicitly activate each agent after verifying ALC configuration.

### Step 9: Activate Agents (ALC Gate)

After registration, activate agents one by one:

```bash
# Activate an agent (will pass ALC gate check)
curl -X PATCH http://127.0.0.1:8000/api/v1/agents/my_domain.analysis_agent \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

The ALC activation gate validates:

1. If `requires_alc` is `false`: activation proceeds immediately
2. If `requires_alc` is `true`: checks that `alc_version` is set, `allowed_memory_scopes` includes `"agent"`, and `hooks.reflect` is `true`

If validation fails:

```json
{
  "error": "alc_activation_denied",
  "detail": "Agent requires ALC but hooks.reflect is not enabled",
  "request_id": "req_abc123"
}
```

### Step 10: Verify with Inventory Check

Run the inventory check to confirm your pack is properly registered:

```bash
# Check domain inventory
python scripts/business/inventory_check.py

# For the video pack specifically (N3 enforcement)
# Fails if agent directories != 114
```

---

## Wave Progression

Domain Packs progress through waves, each unlocking additional capabilities:

| Wave | Capabilities | Requirements |
|------|-------------|--------------|
| **Wave 0** | Schema validation, structure setup | manifest.json + skeleton |
| **Wave 1** | ALC activation, API registration, memory scopes | Valid agent_spec with ALC, evals |
| **Wave 2** | Evolution proposals, corpus evaluation | Golden + regression eval sets |
| **Wave 3** | Coevolution, lesson utility, governance review | Full eval corpus, policies |
| **Wave 4** | Multi-pack proof, cross-domain experiments | Multiple packs isolated |

### Wave 3 Features

Wave 3 unlocks advanced pack capabilities:

```bash
# Run coevolution experiment
curl -X POST http://127.0.0.1:8000/api/v1/evolution/coevolution/run \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "generations": 5,
    "domain_id": "my_domain",
    "agent_ids": ["my_domain.analysis_agent", "my_domain.synthesis_agent"],
    "base_workflow_id": "wf_primary_process_v1"
  }'

# Check lesson utility
curl http://127.0.0.1:8000/api/v1/improvement/lesson-utility?agent_id=my_domain.analysis_agent&limit=20 \
  -H "Authorization: Bearer admin-token"

# View governance review queue
curl http://127.0.0.1:8000/api/v1/evolution/governance/review \
  -H "Authorization: Bearer admin-token"
```

### Fitness Composite Formula

Evolution evaluation uses a deterministic fitness formula:

```
fitness = 0.6 * suite_pass_rate + 0.2 * knowledge_growth_norm + 0.2 * lesson_reuse_norm
```

Where:
- `suite_pass_rate`: Proportion of evaluation corpus tasks that pass
- `knowledge_growth_norm`: Normalized measure of knowledge base expansion
- `lesson_reuse_norm`: Normalized frequency of lesson library utilization

---

## Real-World Use Cases

### Use Case 1: Legal Compliance Domain Pack

A legal firm creates a domain pack for contract review automation:

```json
{
  "domain_id": "legal_compliance",
  "display_name": "Legal Compliance Pack",
  "version": "1.0.0",
  "agents": {
    "roster_count": 8,
    "roster": [
      "contract_intake",
      "clause_analyzer",
      "risk_assessor",
      "compliance_checker",
      "redline_drafter",
      "approval_router",
      "audit_logger",
      "legal_orchestrator"
    ]
  },
  "tools": {
    "namespace": "legal",
    "adapters": [
      "legal.clause_search",
      "legal.precedent_lookup",
      "legal.risk_score",
      "legal.redline_generate"
    ]
  }
}
```

Key decisions:
- `risk_tier: 4` for the `redline_drafter` (irreversible external action)
- All agents require ALC for continuous learning from reviewed contracts
- Golden tasks include sample contracts with known compliance issues
- Human gate on final approval before any client-facing output

### Use Case 2: Healthcare Operations Domain Pack

A hospital system automates patient intake and scheduling:

```json
{
  "domain_id": "healthcare_ops",
  "display_name": "Healthcare Operations",
  "version": "1.0.0",
  "agents": {
    "roster_count": 12,
    "roster": [
      "patient_intake",
      "triage_classifier",
      "schedule_optimizer",
      "insurance_verifier",
      "referral_coordinator",
      "discharge_planner",
      "follow_up_scheduler",
      "quality_monitor",
      "compliance_auditor",
      "patient_communicator",
      "staff_notifier",
      "ops_orchestrator"
    ]
  }
}
```

Key decisions:
- `risk_tier: 5` (restricted) for any clinical decision agents until assurance case approved
- HIPAA compliance policies in `policies/hipaa_controls.json`
- Adversarial eval tests include PHI leakage scenarios
- Tool namespace `healthcare.*` with strict memory scope isolation

### Use Case 3: E-commerce Fulfillment Domain Pack

An online retailer automates order processing and customer support:

```json
{
  "domain_id": "ecommerce_fulfillment",
  "display_name": "E-commerce Fulfillment",
  "version": "2.0.0",
  "wave": 2,
  "agents": {
    "roster_count": 6,
    "roster": [
      "order_processor",
      "inventory_checker",
      "shipping_coordinator",
      "customer_support",
      "return_handler",
      "fulfillment_orchestrator"
    ]
  }
}
```

Key decisions:
- `risk_tier: 3` for `shipping_coordinator` (reversible: can cancel shipment)
- `risk_tier: 2` for `customer_support` (drafts responses, human reviews)
- ALC enabled on support agent to learn from resolved tickets
- Eval corpus includes seasonal demand spike scenarios

---

## Best Practices

### Pack Design

1. **Start small, grow incrementally.** Begin with 3-5 agents and one primary workflow. Add complexity only after Wave 1 validation passes.

2. **Namespace everything.** Every tool, memory scope, and agent ID should carry the domain prefix (e.g., `legal.clause_search`, not just `clause_search`).

3. **Design for isolation.** Your pack should never reference tools or memory from another domain. The host enforces this, but design for it from the start.

4. **Invest in evaluation corpus.** The Evolution Sandbox cannot improve what it cannot measure. Aim for 20+ golden tasks before attempting Wave 2.

### ALC Configuration

5. **Start with conservative learning rate.** Set `learning_rate: "conservative"` initially. Upgrade to `"moderate"` only after reviewing lesson quality over 50+ runs.

6. **Scope memory appropriately.** Use `"agent"` scope for agent-specific learnings. Use `"organization"` only for cross-agent knowledge that all agents should access.

7. **Set lesson retention limits.** Configure `lesson_retention_days` to prevent unbounded memory growth. 90 days is a sensible default.

### Registration and Deployment

8. **Always dry-run first.** Use `--dry-run` before any registration to catch schema issues early.

9. **Activate agents incrementally.** Do not activate all agents simultaneously. Start with the orchestrator, then add downstream agents one at a time.

10. **Monitor ALC metrics.** After activation, track lesson generation rate via `GET /api/v1/improvement/lessons?agent_id=...` and lesson utility via the dashboard.

---

## Validation Commands

Use these commands to validate your Domain Pack at any stage:

```bash
# Validate business artifacts (schemas, manifests)
npm run business:validate

# Run governance checks
npm run business:governance

# Run security scan on business artifacts
npm run business:security

# Check evolution readiness
npm run business:evolution:check

# Run evaluation corpus
npm run business:eval

# Full domain initialization
npm run business:init
```

---

## Advanced: Schema Deep Dive

### Domain Manifest Schema Fields

The complete `domain-manifest.schema.json` supports these fields:

```json
{
  "type": "object",
  "required": ["domain_id", "display_name", "version", "agents"],
  "properties": {
    "domain_id": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_]*$",
      "description": "Unique identifier, valid Python/JS identifier"
    },
    "display_name": {
      "type": "string",
      "maxLength": 100
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version"
    },
    "description": {"type": "string"},
    "owner": {"type": "string", "format": "email"},
    "wave": {"type": "integer", "minimum": 0, "maximum": 4},
    "agents": {
      "type": "object",
      "required": ["roster_count", "roster"],
      "properties": {
        "roster_count": {"type": "integer", "minimum": 1},
        "roster": {
          "type": "array",
          "items": {"type": "string"},
          "uniqueItems": true
        }
      }
    },
    "workflows": {
      "type": "array",
      "items": {"type": "string"}
    },
    "tools": {
      "type": "object",
      "properties": {
        "namespace": {"type": "string"},
        "adapters": {"type": "array", "items": {"type": "string"}}
      }
    },
    "knowledge": {
      "type": "object",
      "properties": {
        "seed_documents": {"type": "integer"},
        "embedding_tier": {"type": "integer", "minimum": 0, "maximum": 3}
      }
    },
    "evals": {
      "type": "object",
      "properties": {
        "golden_tasks": {"type": "integer"},
        "regression_tests": {"type": "integer"},
        "adversarial_tests": {"type": "integer"}
      }
    },
    "dependencies": {
      "type": "object",
      "properties": {
        "min_host_version": {"type": "string"},
        "required_services": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

### Agent Spec Schema - ALC Section Detail

The ALC (Autonomous Learning Capability) section has specific validation requirements:

```json
{
  "alc_config": {
    "type": "object",
    "required": ["allowed_memory_scopes"],
    "properties": {
      "allowed_memory_scopes": {
        "type": "array",
        "items": {"enum": ["agent", "organization"]},
        "minItems": 1,
        "description": "Must include 'agent' for ALC activation"
      },
      "learning_rate": {
        "enum": ["conservative", "moderate", "aggressive"],
        "default": "conservative"
      },
      "max_lessons_per_run": {
        "type": "integer",
        "minimum": 1,
        "maximum": 10,
        "default": 3
      },
      "lesson_retention_days": {
        "type": "integer",
        "minimum": 7,
        "maximum": 365,
        "default": 90
      },
      "reflection_depth": {
        "enum": ["shallow", "standard", "deep"],
        "default": "standard",
        "description": "How deeply the agent reflects on run outcomes"
      },
      "cross_agent_learning": {
        "type": "boolean",
        "default": false,
        "description": "Whether lessons can be shared with other agents in the same domain"
      }
    }
  }
}
```

> **Tip:** The `cross_agent_learning` field is a Wave 3+ feature. When enabled, high-utility lessons from one agent can be recommended to other agents within the same domain pack (never across packs).

### Learning Log Schema

The `learning-log.schema.json` defines how lessons are stored:

```json
{
  "type": "object",
  "required": ["lesson_id", "agent_id", "content", "source_run"],
  "properties": {
    "lesson_id": {"type": "string"},
    "agent_id": {"type": "string"},
    "domain_id": {"type": "string"},
    "content": {"type": "string", "maxLength": 2000},
    "type": {"enum": ["optimization", "error_pattern", "compliance", "preference", "capability"]},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "utility_score": {"type": "number", "minimum": 0, "maximum": 1},
    "source_run": {"type": "string"},
    "applicable_steps": {"type": "array", "items": {"type": "string"}},
    "times_reused": {"type": "integer", "default": 0},
    "created_at": {"type": "string", "format": "date-time"},
    "expires_at": {"type": "string", "format": "date-time"}
  }
}
```

---

## Troubleshooting

### Common Registration Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `schema_validation_failed` | Manifest does not match schema | Run `npm run business:validate` and fix reported issues |
| `duplicate_domain_id` | Domain ID already registered | Choose a different `domain_id` or use versioning |
| `roster_count_mismatch` | `roster_count` does not match `roster` array length | Ensure the count equals the array length exactly |
| `invalid_agent_spec` | Agent spec fails schema validation | Check required fields: `agent_id`, `pack_id`, `role` |
| `alc_validation_failed` | ALC fields incomplete for `requires_alc: true` | Ensure `alc_version`, `allowed_memory_scopes` (includes "agent"), and `hooks.reflect: true` |
| `namespace_conflict` | Tool namespace conflicts with existing pack | Use a unique namespace prefix matching your `domain_id` |

### Activation Failures

```bash
# Diagnose ALC activation failure
curl -X PATCH http://127.0.0.1:8000/api/v1/agents/my_domain.agent_name \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

If you receive `alc_activation_denied`, check these fields in `agent_spec.json`:

```bash
# Verify ALC readiness
jq '{requires_alc, alc_version, "memory_scopes": .alc_config.allowed_memory_scopes, "reflect": .hooks.reflect}' \
  business/my_domain/agents/my_domain/agent_spec.json
```

Expected output for a valid ALC configuration:

```json
{
  "requires_alc": true,
  "alc_version": "1.0.0",
  "memory_scopes": ["agent", "organization"],
  "reflect": true
}
```

### Inventory Check Failures

If `python scripts/business/inventory_check.py` fails:

1. **Missing agent directories:** Verify all agents listed in `manifest.json` roster have corresponding directories under `agents/`
2. **Incomplete specs:** Every agent directory must contain `agent_spec.json` and `SPEC.md`
3. **Status issues:** Agents must be in `registered` or `active` status (not `draft` or `inactive`)
4. **DNA missing:** At least one workflow DNA file must exist in `workflows/`

```bash
# Quick diagnostic for inventory issues
echo "=== Roster vs. Directories ==="
ROSTER=$(jq -r '.agents.roster[]' business/my_domain/manifest.json)
for AGENT in $ROSTER; do
  if [ -d "business/my_domain/agents/my_domain/$AGENT" ]; then
    echo "OK: $AGENT"
  else
    echo "MISSING: $AGENT"
  fi
done
```

### Evolution Corpus Issues

If `npm run business:eval` reports issues:

```bash
# Verify eval corpus structure
find business/my_domain/evals/ -name "*.json" | head -20

# Validate a golden task file
jq '.' business/my_domain/evals/golden-tasks/task_001.json

# Check required fields in each task
jq 'keys' business/my_domain/evals/golden-tasks/task_001.json
# Must include: task_id, description, input, expected_output, evaluation_criteria
```

---

## Reference: Wave Progression Detail

### Wave 0: Foundation

**Unlocks:** Schema validation, directory structure verification

**Requirements:**
- `manifest.json` with valid schema
- At least one agent directory with `agent_spec.json`
- Directory structure follows the standard layout

**Validation:**
```bash
npm run business:validate
```

### Wave 1: Activation

**Unlocks:** ALC activation, API registration, memory scopes, basic lessons

**Requirements (beyond Wave 0):**
- All agents have valid ALC fields (if `requires_alc: true`)
- At least 5 golden evaluation tasks
- Tool namespace defined and non-conflicting
- `hooks.reflect: true` on ALC agents

**Validation:**
```bash
python scripts/business/register_domain.py --manifest business/my_domain/manifest.json
curl -X PATCH http://127.0.0.1:8000/api/v1/agents/my_domain.agent_name \
  -H "Authorization: Bearer admin-token" -d '{"status": "active"}'
```

### Wave 2: Evolution

**Unlocks:** Evolution proposals, corpus evaluation, fitness scoring

**Requirements (beyond Wave 1):**
- At least 10 golden tasks + 5 regression tests
- At least one adversarial test
- Workflow DNA with domain field set correctly
- Evaluation criteria defined in each task

**Validation:**
```bash
npm run business:eval
npm run business:evolution:check
```

### Wave 3: Advanced Learning

**Unlocks:** Coevolution, lesson utility dashboard, governance review, skill sandbox

**Requirements (beyond Wave 2):**
- Full evaluation corpus (golden + regression + adversarial + historical)
- Policies directory with governance rules
- Multiple agents with ALC enabled (for coevolution)
- At least 50 completed runs for statistical significance

**Validation:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/evolution/coevolution/run \
  -H "Authorization: Bearer admin-token" \
  -d '{"generations": 3, "domain_id": "my_domain", "base_workflow_id": "..."}'
```

### Wave 4: Multi-Pack Proof

**Unlocks:** Multi-domain deployment, cross-domain isolation verification, full production readiness

**Requirements (beyond Wave 3):**
- At least two domain packs registered
- Isolation verification passes between all pack pairs
- Red-team security evidence documented
- N3 inventory check passes (if video pack included)
- Performance benchmarks under multi-pack load

**Validation:**
```bash
python scripts/business/inventory_check.py
npm run business:security
# Multi-pack isolation test
python scripts/business/isolation_verify.py --domains my_domain,example_research
```

---

## Chapter Summary

In this chapter, you learned how to:

- Structure a Domain Pack following the standardized `business/<domain_id>/` layout
- Create `manifest.json` with all required fields including agent roster and tool namespaces
- Define `agent_spec.json` files with ALC (Autonomous Learning Capability) configuration
- Write workflow DNA that assigns agents to steps with appropriate risk tiers
- Build an evaluation corpus for the Evolution Sandbox
- Register packs via CLI (`register_domain.py --dry-run`) and API (`POST /api/v1/domains/register`)
- Activate agents through the ALC gate with proper validation
- Progress through Waves 0-4 unlocking capabilities at each stage
- Apply isolation rules that prevent cross-pack contamination

Domain Packs are the fundamental unit of business customization in Generic Swarm Ops. By following the standardized structure and registration process, you ensure that your domain logic integrates cleanly with the shared host runtime while maintaining strict isolation from other packs.

---

## Knowledge Check

1. **What are the three non-negotiable rules (N1, N2, N3) for Domain Pack architecture?**

2. **What conditions must be met for the ALC activation gate to allow an agent to transition from `draft` to `active` status?**

3. **Write the API call to register a domain pack by manifest path. What status will the agents have after registration?**

4. **What is the fitness composite formula used by the Evolution Sandbox? Name all three components.**

5. **Explain the difference between Wave 1 and Wave 3 capabilities. What additional features does Wave 3 unlock?**

6. **Why must the `domain_id` be a valid Python/JavaScript identifier? What systems use it as a namespace prefix?**

7. **Describe the directory structure of a Domain Pack. What is the minimum set of files needed for Wave 0 validation?**

8. **What command validates that the video pack retains all 114 agents? What does it check specifically?**

9. **How does memory scope isolation work between domain packs? What scopes are allowed, and what prevents cross-pack bleed?**

10. **When configuring a healthcare domain pack, why would you set `risk_tier: 5` for clinical decision agents? What additional artifact is required?**
