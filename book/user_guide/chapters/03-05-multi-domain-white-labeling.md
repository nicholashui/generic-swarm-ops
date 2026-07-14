# Chapter 3.5: Multi-Domain Deployment and White-Labeling

## Learning Objectives

By the end of this chapter, you will be able to:

1. Deploy and manage multiple Domain Packs simultaneously on a single host
2. Configure and verify domain isolation boundaries (tool namespaces, memory scopes)
3. Run coevolution experiments across domain packs
4. Use the lesson utility dashboard to track cross-agent learning effectiveness
5. Implement white-label configurations for different organizational units
6. Understand and enforce N3 inventory rules for the video reference pack
7. Apply the Wave 4 multi-pack proof pattern for production deployments

## Prerequisites

- Completed Chapters 3.1 through 3.4
- At least two registered Domain Packs (one can be `example_research`)
- Understanding of the Domain Pack architecture and registration process
- Familiarity with the Evolution Sandbox and self-improvement loop
- Admin access to the Generic Swarm Ops instance

---

## Architecture Overview

![Multi-Domain Isolation](../assets/03-05-multi-domain-isolation.svg)

Multi-domain deployment enables multiple business domains to share the same Generic Swarm Ops host runtime while maintaining strict isolation boundaries. Each domain pack operates within its own namespace, memory scope, and evaluation overlay, connected only through the shared infrastructure layer (FastAPI, Governance Officer, Evolution Engine, Postgres).

### The Multi-Pack Proof (Wave 4)

Wave 4 validates that the system can support multiple concurrent domain packs with full isolation:

| Pack | Role | Scale |
|------|------|-------|
| `video` | N3 full roster, reference implementation | 114 agents |
| `example_research` | Wave 1 second pack, minimal | 3-5 agents |
| `example_education` | Wave 4 third lite pack | 3-5 agents |

> **Note:** The video pack with its 114 agents serves as the reference implementation for a large-scale domain pack. It demonstrates that the architecture can handle complex, multi-agent domains without performance degradation or isolation violations.

---

## Step-by-Step: Multi-Domain Deployment

### Step 1: Register Multiple Domain Packs

Register each domain pack independently. They share the host runtime but maintain separate namespaces:

```bash
# Register the research pack
python scripts/business/register_domain.py \
  --manifest business/example_research/manifest.json

# Register the education pack
python scripts/business/register_domain.py \
  --manifest business/example_education/manifest.json

# Verify registration
curl http://127.0.0.1:8000/api/v1/agents?domain=example_research \
  -H "Authorization: Bearer admin-token"

curl http://127.0.0.1:8000/api/v1/agents?domain=example_education \
  -H "Authorization: Bearer admin-token"
```

### Step 2: Verify Domain Isolation

After registration, verify that isolation boundaries are correctly enforced:

```bash
# Check tool namespace isolation
curl http://127.0.0.1:8000/api/v1/agents/video.editor_agent \
  -H "Authorization: Bearer admin-token" | jq '.tool_permissions.allowed'
# Should only contain "video.*" and "shared.*" tools

curl http://127.0.0.1:8000/api/v1/agents/research.analyst_agent \
  -H "Authorization: Bearer admin-token" | jq '.tool_permissions.allowed'
# Should only contain "research.*" and "shared.*" tools
```

### Step 3: Verify Memory Scope Isolation

Memory scopes prevent cross-pack data leakage:

```bash
# Write memory to video agent scope
curl -X POST http://127.0.0.1:8000/api/v1/memory \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "video.editor_agent",
    "scope": "agent",
    "content": "Preferred export format: ProRes 4444",
    "category": "preference"
  }'

# Attempt to read from research agent (should return empty)
curl "http://127.0.0.1:8000/api/v1/memory?agent_id=research.analyst_agent&scope=agent" \
  -H "Authorization: Bearer admin-token"
# Response should NOT contain video agent memories
```

> **Warning:** Memory scope isolation is a critical security boundary. The rule is simple: no cross-pack bleed. An agent in the `video` pack cannot access memories written by agents in the `research` pack, and vice versa. This is enforced at the runtime level, not just the API level.

### Step 4: Understand Isolation Rules

The system enforces these isolation rules:

| Boundary | Rule | Enforcement |
|----------|------|-------------|
| **Tool namespaces** | `video.*` agents can only call `video.*` tools | Runtime tool broker |
| **Memory scopes** | Agent-scoped memories isolated per pack | Query filter on `domain_id` |
| **Orchestrators** | `business_orchestrator` is distinct from `video.orchestrator` | Separate agent IDs |
| **Eval overlays** | Corpus loads `business/<domain>/evals/*` when DNA `domain` matches | Eval harness filter |
| **Lessons** | Agent-scoped lessons/episodes per domain | Lesson library filter |
| **Tool allow-list** | Enforced outside the model (red-team validated) | No allow-list expansion from injection |

### Step 5: Configure Evaluation Overlays Per Domain

Each domain pack has its own evaluation corpus that loads automatically when the domain matches:

```yaml
# Evaluation overlay configuration
# When workflow DNA has domain: "video", only video evals load
# When workflow DNA has domain: "research", only research evals load

# Video pack evaluation (LQR golden tasks)
business/video/evals/
  golden-tasks/
    lqr_quality_task_001.json
    lqr_quality_task_002.json
    ...
  regression/
    codec_compatibility_001.json
  adversarial/
    injection_via_subtitle_001.json

# Research pack evaluation
business/example_research/evals/
  golden-tasks/
    research_quality_001.json
  regression/
    citation_accuracy_001.json
```

---

## Step-by-Step: Coevolution Experiments

### Step 6: Run a Coevolution Experiment

Coevolution experiments allow multiple agents within a domain to evolve together in a sandboxed multi-generation learning environment:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/evolution/coevolution/run \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "generations": 5,
    "domain_id": "my_domain",
    "agent_ids": [
      "my_domain.analysis_agent",
      "my_domain.synthesis_agent",
      "my_domain.review_agent"
    ],
    "base_workflow_id": "wf_primary_process_v1",
    "config": {
      "population_size": 3,
      "selection_pressure": "moderate",
      "mutation_rate": 0.2,
      "crossover_enabled": true
    }
  }'
```

**Response:**

```json
{
  "experiment_id": "coevo_001",
  "status": "running",
  "domain_id": "my_domain",
  "generations_total": 5,
  "current_generation": 1,
  "agents_evolving": 3,
  "sandbox_only": true,
  "auto_promote": false
}
```

> **Warning:** Coevolution experiments operate strictly in the sandbox. They never mutate production DNA and never auto-promote. This is the same safety invariant as the standard evolution pipeline.

### Step 7: Monitor Coevolution Progress

```bash
# Check experiment status
curl http://127.0.0.1:8000/api/v1/evolution/coevolution/coevo_001 \
  -H "Authorization: Bearer admin-token"
```

**Response:**

```json
{
  "experiment_id": "coevo_001",
  "status": "completed",
  "generations_completed": 5,
  "results": {
    "generation_fitness": [0.72, 0.78, 0.81, 0.84, 0.86],
    "best_variant_per_agent": {
      "my_domain.analysis_agent": {"variant_id": "coevo_001_g5_a1", "fitness": 0.89},
      "my_domain.synthesis_agent": {"variant_id": "coevo_001_g5_a2", "fitness": 0.84},
      "my_domain.review_agent": {"variant_id": "coevo_001_g5_a3", "fitness": 0.87}
    },
    "combined_workflow_fitness": 0.86,
    "lessons_generated": 12
  }
}
```

### Step 8: Promote Coevolution Results

If coevolution produces promising variants, promote them through the standard pipeline:

```bash
# Evaluate best variant against full corpus
curl -X POST http://127.0.0.1:8000/api/v1/evolution/variants/coevo_001_g5_a1/evaluate \
  -H "Authorization: Bearer admin-token"

# If passes, promote via canary (standard pipeline)
curl -X POST http://127.0.0.1:8000/api/v1/evolution/variants/coevo_001_g5_a1/promote \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{"mode": "canary", "rollback_plan": {"trigger": "fitness below 0.80"}}'
```

---

## Step-by-Step: Lesson Utility Dashboard

### Step 9: Query Lesson Utility

The lesson utility dashboard shows how effectively agents reuse lessons from the library:

```bash
# Get lesson utility for a specific agent
curl "http://127.0.0.1:8000/api/v1/improvement/lesson-utility?agent_id=my_domain.analysis_agent&limit=20" \
  -H "Authorization: Bearer admin-token"
```

**Response:**

```json
{
  "agent_id": "my_domain.analysis_agent",
  "lessons": [
    {
      "lesson_id": "lesson_001",
      "content": "Parallel verification reduces step time by 70%",
      "utility_score": 0.92,
      "times_applied": 15,
      "last_applied": "2024-01-15T10:00:00Z",
      "success_rate_when_applied": 0.93,
      "trend": "stable"
    },
    {
      "lesson_id": "lesson_002",
      "content": "External API timeout at 5KB payload",
      "utility_score": 0.78,
      "times_applied": 8,
      "last_applied": "2024-01-14T16:00:00Z",
      "success_rate_when_applied": 0.88,
      "trend": "improving"
    }
  ],
  "summary": {
    "total_lessons": 15,
    "high_utility_count": 5,
    "low_utility_count": 3,
    "avg_utility_score": 0.72
  }
}
```

### Step 10: Analyze Cross-Agent Learning Patterns

Compare lesson utility across agents in a domain:

```bash
# Get metrics for all agents in a domain
for AGENT in analysis_agent synthesis_agent review_agent; do
  echo "=== my_domain.$AGENT ==="
  curl -s "http://127.0.0.1:8000/api/v1/improvement/metrics?agent_id=my_domain.$AGENT" \
    -H "Authorization: Bearer admin-token" | jq '{lesson_reuse_rate, improvement_trend}'
done
```

> **Tip:** The frontend Evolution page shows the Lesson Utility panel beside the population archive. This gives a visual overview of which agents are learning effectively and which may need additional training data or evaluation corpus expansion.

---

## Step-by-Step: N3 Inventory Enforcement

### Step 11: Understand N3 Rules

The N3 rule ensures that the video reference pack maintains its complete roster of 114 agents. This is enforced through CI and runtime checks:

```bash
# Run inventory check
python scripts/business/inventory_check.py
```

The inventory check fails if:
- Agent directories do not equal 114
- ROSTER, MAP, or `agent_spec.json` files are incomplete
- Standby, router, or process coverage agents are missing
- Required DNA files are absent
- Agents are not in `registered` or `active` status

### Step 12: Check N3 Status via API

```bash
curl http://127.0.0.1:8000/api/v1/domains/video/n3-status \
  -H "Authorization: Bearer admin-token"
```

**Response:**

```json
{
  "domain_id": "video",
  "n3_complete": true,
  "roster_count": 114,
  "dna_count": 12,
  "orphan_agents": 0,
  "status_breakdown": {
    "active": 108,
    "registered": 6,
    "draft": 0,
    "inactive": 0
  },
  "last_inventory_check": "2024-01-15T06:00:00Z",
  "ci_workflow": ".github/workflows/n3-inventory.yml"
}
```

### Step 13: CI Enforcement

The N3 inventory is enforced in CI via GitHub Actions:

```yaml
# .github/workflows/n3-inventory.yml
name: N3 Inventory Check
on: [push, pull_request]
jobs:
  inventory:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python scripts/business/inventory_check.py
        # Fails the build if video pack != 114 agents
```

---

## Step-by-Step: White-Label Configuration

### Step 14: Configure Domain-Specific Branding

White-labeling allows different organizational units to present Generic Swarm Ops with their own branding while sharing the same infrastructure:

```json
{
  "domain_id": "enterprise_client_a",
  "white_label": {
    "display_name": "Client A Operations Platform",
    "logo_url": "/static/branding/client_a/logo.svg",
    "primary_color": "#1a365d",
    "accent_color": "#2b6cb0",
    "favicon": "/static/branding/client_a/favicon.ico",
    "support_email": "support@client-a.example.com",
    "documentation_url": "https://docs.client-a.example.com",
    "footer_text": "Powered by Generic Swarm Ops"
  }
}
```

### Step 15: Configure Domain-Specific UI Components

Domain packs can include custom UI components in their `ui/` directory:

```text
business/enterprise_client_a/
  ui/
    dashboard/
      DomainDashboard.tsx    # Custom domain landing page
      MetricsPanel.tsx       # Domain-specific KPIs
    workflows/
      CustomWorkflowForm.tsx # Domain-specific workflow creation form
    branding/
      theme.json            # Color scheme and typography overrides
      logo.svg              # Domain logo
```

### Step 16: Configure Per-Domain Access Controls

Each white-label instance can have its own user roles and permissions:

```json
{
  "domain_id": "enterprise_client_a",
  "access_control": {
    "roles": [
      {
        "role": "domain_admin",
        "permissions": [
          "workflows:*",
          "runs:*",
          "agents:read",
          "agents:activate",
          "approvals:*",
          "evolution:read",
          "evolution:propose"
        ]
      },
      {
        "role": "domain_operator",
        "permissions": [
          "workflows:read",
          "runs:execute",
          "runs:read",
          "approvals:approve"
        ]
      },
      {
        "role": "domain_viewer",
        "permissions": [
          "workflows:read",
          "runs:read",
          "knowledge:search"
        ]
      }
    ],
    "default_role": "domain_viewer",
    "admin_users": ["admin@client-a.example.com"]
  }
}
```

---

## Step-by-Step: Security and Red-Team Validation

### Step 17: Run Red-Team Validation

Multi-domain deployments require additional security validation to ensure isolation holds:

```bash
# Run security scan across all domains
npm run business:security

# Check for cross-domain tool access attempts
curl "http://127.0.0.1:8000/api/v1/audit-logs?event_type=tool_denied&since=24h" \
  -H "Authorization: Bearer admin-token"
```

Red-team validation confirms:
- No allow-list expansion from prompt injection
- Tool namespace boundaries hold under adversarial input
- Memory scope isolation prevents information leakage
- Cross-pack agent invocation is blocked

### Step 18: Review Security Evidence

The system maintains security evidence for each wave:

```bash
# Wave 4 security evidence
cat business/security/red-team-results/wave-4-tool-misuse.json
```

```json
{
  "test_suite": "wave-4-multi-pack-isolation",
  "date": "2024-01-10",
  "results": {
    "tool_namespace_breach_attempts": 15,
    "tool_namespace_breaches": 0,
    "memory_scope_breach_attempts": 12,
    "memory_scope_breaches": 0,
    "injection_via_cross_domain": 8,
    "injection_successes": 0,
    "allow_list_expansion_attempts": 5,
    "allow_list_expansions": 0
  },
  "conclusion": "All isolation boundaries held under adversarial testing",
  "next_review": "2024-04-10"
}
```

---

## Multi-Domain Deployment Checklist

Before deploying multiple domain packs to production:

```markdown
## Pre-Deployment Checklist

- [ ] All packs registered and schema-validated
- [ ] Tool namespaces unique and non-overlapping
- [ ] Memory scope isolation verified (Wave 1 tests pass)
- [ ] Evaluation overlays configured per domain
- [ ] N3 inventory check passes (if video pack included)
- [ ] Security red-team evidence documented
- [ ] Per-domain access controls configured
- [ ] Audit logging covers all domains
- [ ] Governance review queue accessible to domain admins
- [ ] Coevolution experiments validated in sandbox
- [ ] Rollback plans documented for each domain
- [ ] CI workflows include isolation validation
```

---

## Troubleshooting

### Common Multi-Domain Issues

| Issue | Symptoms | Resolution |
|-------|----------|------------|
| Cross-pack tool access | `tool_denied` events in audit log | Verify tool namespace configuration; check for typos in allow-lists |
| Memory bleed between domains | Agent sees memories from another pack | Check memory scope filter; verify `domain_id` is set on all memory writes |
| Eval overlay loading wrong corpus | Fitness scores inconsistent | Verify `domain` field in workflow DNA matches the pack's `domain_id` |
| N3 inventory failure | CI build fails | Check agent directory count; verify all ROSTER entries have specs |
| Coevolution timeout | Experiment stuck at generation N | Reduce population size or generation count; check compute resources |
| Registration conflict | `duplicate_domain_id` error | Use a unique domain_id or increment the version |

### Debugging Isolation Violations

```bash
# 1. Check for cross-domain tool access attempts
curl "http://127.0.0.1:8000/api/v1/audit-logs?event_type=tool_denied&since=24h" \
  -H "Authorization: Bearer admin-token" | jq '.events[] | {agent_id, tool_requested, reason}'

# 2. Verify namespace enforcement
curl http://127.0.0.1:8000/api/v1/agents/video.editor_agent \
  -H "Authorization: Bearer admin-token" | jq '.tool_permissions'
# Should only show "video.*" and "shared.*" namespaces

# 3. Check memory scope boundaries
curl "http://127.0.0.1:8000/api/v1/memory?agent_id=video.editor_agent&include_foreign=true" \
  -H "Authorization: Bearer admin-token"
# "include_foreign" should return empty (no cross-domain memories visible)

# 4. Verify domain registration state
curl http://127.0.0.1:8000/api/v1/domains/video/n3-status \
  -H "Authorization: Bearer admin-token" | jq '{n3_complete, roster_count, orphan_agents}'
```

### Performance Monitoring for Multi-Pack Deployments

```bash
# Check per-domain resource utilization
for DOMAIN in video example_research example_education; do
  echo "=== $DOMAIN ==="
  curl -s "http://127.0.0.1:8000/api/v1/agents?domain=$DOMAIN" \
    -H "Authorization: Bearer admin-token" | jq '{
      total_agents: .total,
      active_agents: (.agents | map(select(.status == "active")) | length),
      total_runs_24h: .total_runs_24h
    }'
done

# Monitor database connection usage
curl http://127.0.0.1:8000/api/v1/health/ready \
  -H "Authorization: Bearer admin-token" | jq '.database'
```

---

## Advanced: Domain Lifecycle Management

### Adding a New Domain to an Existing Deployment

Follow this sequence to safely add a domain pack to a running multi-domain deployment:

```bash
# 1. Validate the new pack in isolation
python scripts/business/register_domain.py \
  --manifest business/new_domain/manifest.json --dry-run

# 2. Run schema validation
npm run business:validate

# 3. Register the pack (creates agents in draft state)
python scripts/business/register_domain.py \
  --manifest business/new_domain/manifest.json

# 4. Verify isolation against all existing packs
python scripts/business/isolation_verify.py \
  --domains video,example_research,new_domain

# 5. Activate agents one by one
for AGENT in $(jq -r '.agents.roster[]' business/new_domain/manifest.json); do
  curl -X PATCH "http://127.0.0.1:8000/api/v1/agents/new_domain.$AGENT" \
    -H "Authorization: Bearer admin-token" \
    -H "Content-Type: application/json" \
    -d '{"status": "active"}'
  echo ""
done

# 6. Run initial evaluation corpus
npm run business:eval

# 7. Monitor for 24 hours before enabling evolution
echo "Monitor for anomalies before proceeding to Wave 2"
```

### Decommissioning a Domain Pack

```bash
# 1. Set all agents to inactive
for AGENT in $(jq -r '.agents.roster[]' business/old_domain/manifest.json); do
  curl -X PATCH "http://127.0.0.1:8000/api/v1/agents/old_domain.$AGENT" \
    -H "Authorization: Bearer admin-token" \
    -H "Content-Type: application/json" \
    -d '{"status": "inactive"}'
done

# 2. Archive lessons and evolution data
curl "http://127.0.0.1:8000/api/v1/improvement/lessons?domain=old_domain" \
  -H "Authorization: Bearer admin-token" > archive/old_domain_lessons.json

curl "http://127.0.0.1:8000/api/v1/evolution/archive?domain=old_domain" \
  -H "Authorization: Bearer admin-token" > archive/old_domain_variants.json

# 3. Verify no active runs reference this domain
curl "http://127.0.0.1:8000/api/v1/runs?domain=old_domain&status=running" \
  -H "Authorization: Bearer admin-token"

# 4. Remove from CI validation (update .github/workflows)
# 5. Archive the domain pack directory
mv business/old_domain/ archive/domains/old_domain_$(date +%Y%m%d)/
```

### Version Upgrades for Domain Packs

```bash
# Upgrade a domain pack from v1.0.0 to v2.0.0
# 1. Update manifest version
jq '.version = "2.0.0"' business/my_domain/manifest.json > tmp.json \
  && mv tmp.json business/my_domain/manifest.json

# 2. Run validation
npm run business:validate

# 3. Re-register (updates version in registry)
python scripts/business/register_domain.py \
  --manifest business/my_domain/manifest.json

# 4. Run full evaluation suite
npm run business:eval

# 5. If new agents added, activate them
curl -X PATCH http://127.0.0.1:8000/api/v1/agents/my_domain.new_agent \
  -H "Authorization: Bearer admin-token" \
  -d '{"status": "active"}'
```

---

## Real-World Use Cases

### Use Case 1: Enterprise Multi-Division Deployment

A corporation deploys separate domain packs for each business division:

```text
business/
  sales_ops/          # Sales automation (8 agents)
  hr_operations/      # HR workflow automation (12 agents)
  finance_ops/        # Financial processing (6 agents)
  customer_success/   # Customer lifecycle management (10 agents)
```

Isolation ensures:
- HR agents cannot access financial data
- Sales agents cannot view HR records
- Customer success lessons are separate from internal operations
- Each division has its own evaluation corpus and governance policies

Configuration:

```bash
# Register all divisions
for DOMAIN in sales_ops hr_operations finance_ops customer_success; do
  python scripts/business/register_domain.py \
    --manifest "business/$DOMAIN/manifest.json"
done

# Verify isolation between all pairs
python scripts/business/isolation_verify.py --domains sales_ops,hr_operations,finance_ops,customer_success
```

### Use Case 2: SaaS Platform with Tenant Isolation

A SaaS platform uses domain packs to isolate customer tenants:

```json
{
  "deployment_model": "multi_tenant_saas",
  "tenants": [
    {
      "domain_id": "tenant_acme",
      "display_name": "Acme Corp Instance",
      "white_label": true,
      "max_agents": 20,
      "max_workflows": 10,
      "data_residency": "us-east-1"
    },
    {
      "domain_id": "tenant_globex",
      "display_name": "Globex Corp Instance",
      "white_label": true,
      "max_agents": 50,
      "max_workflows": 25,
      "data_residency": "eu-west-1"
    }
  ],
  "shared_infrastructure": {
    "host_runtime": "single",
    "database": "postgres_with_row_level_security",
    "isolation": "domain_pack_boundaries"
  }
}
```

Key architecture decisions:
- Row-level security in Postgres enforces tenant data isolation at the database level
- Domain pack boundaries provide application-level isolation
- White-label branding per tenant for customer-facing UI
- Separate evaluation corpus per tenant (no shared golden tasks)
- Data residency enforced through per-tenant storage configuration

### Use Case 3: Research Lab with Experimental Domains

A research lab uses multi-domain deployment for concurrent experiments:

```bash
# Create experimental domains
for EXP in exp_nlp_v1 exp_vision_v2 exp_multimodal_v1; do
  cp -r business/example_research/ "business/$EXP/"
  # Customize manifest for each experiment
  python scripts/business/register_domain.py \
    --manifest "business/$EXP/manifest.json" --dry-run
done

# Run coevolution across experimental domains
curl -X POST http://127.0.0.1:8000/api/v1/evolution/coevolution/run \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "generations": 10,
    "domain_id": "exp_nlp_v1",
    "agent_ids": ["exp_nlp_v1.researcher", "exp_nlp_v1.evaluator"],
    "base_workflow_id": "wf_nlp_experiment_v1"
  }'

# Compare lesson utility across experiments
for EXP in exp_nlp_v1 exp_vision_v2 exp_multimodal_v1; do
  echo "=== $EXP ==="
  curl -s "http://127.0.0.1:8000/api/v1/improvement/lesson-utility?domain=$EXP&limit=5" \
    -H "Authorization: Bearer admin-token" | jq '.summary'
done
```

---

## Best Practices

### Domain Isolation

1. **Never share tool namespaces between domains.** Even if two domains need similar functionality, create separate tool adapters under their own namespace. Shared utilities go in `shared.*`.

2. **Validate isolation after every deployment.** Run the isolation verification script as part of your CI pipeline, not just once during setup.

3. **Monitor for isolation violations.** Set up alerts on `tool_denied` audit events. Any spike in denials may indicate misconfiguration or attempted lateral movement.

4. **Use agent-scoped lessons exclusively for domain learning.** Organization-scoped memories should only contain truly universal knowledge, not domain-specific insights.

### Multi-Pack Operations

5. **Stagger domain pack registrations.** Do not register all packs simultaneously. Register one, verify isolation, then add the next. This makes debugging isolation issues easier.

6. **Run coevolution experiments in off-peak hours.** Multi-generation experiments are compute-intensive. Schedule them when the system has spare capacity.

7. **Set generation limits conservatively.** Start with 3-5 generations for coevolution. More generations increase the chance of overfitting to evaluation corpus.

### White-Labeling

8. **Keep branding assets in the domain pack.** Store logos, themes, and custom components in `business/<domain>/ui/` so they deploy with the pack.

9. **Test branding in isolation.** Verify that white-label themes do not bleed into other domains or the system admin interface.

10. **Document per-domain access controls clearly.** Each domain should have a clear RBAC specification that maps roles to specific permissions.

### Scale Planning

11. **Monitor per-domain resource usage.** Track agent execution time, memory usage, and lesson library size per domain to identify resource-heavy packs.

12. **Plan for N+1 domains.** Before adding a new domain pack, verify that the host has sufficient database connections, compute capacity, and memory for the additional agents.

13. **Use the video pack as a scale benchmark.** If your deployment can run the video pack (114 agents) alongside other domains without degradation, you have sufficient headroom.

---

## Chapter Summary

In this chapter, you learned how to:

- Deploy multiple Domain Packs on a single host with full isolation
- Verify and enforce isolation boundaries (tool namespaces, memory scopes, eval overlays)
- Run coevolution experiments across agents within a domain
- Monitor learning effectiveness through the lesson utility dashboard
- Enforce N3 inventory rules via CLI, API, and CI
- Configure white-label branding for different organizational units
- Set up per-domain access controls and RBAC
- Validate security through red-team testing
- Apply production deployment checklists for multi-domain environments

Multi-domain deployment is the culmination of the Domain Pack architecture. It demonstrates that Generic Swarm Ops can serve as a universal business operating system, supporting diverse domains with complete isolation while sharing the same governance, evolution, and security infrastructure.

---

## Knowledge Check

1. **What are the five isolation boundaries enforced between domain packs? How is each enforced at runtime?**

2. **Explain the N3 rule. What specifically does `python scripts/business/inventory_check.py` validate?**

3. **Write the API call to start a coevolution experiment. What fields are required? What safety guarantees does the system provide?**

4. **How does the evaluation overlay system work? If a workflow has `domain: "video"`, what corpus files are loaded?**

5. **Describe the lesson utility dashboard response. What metrics does it provide for each lesson?**

6. **What is the Wave 4 multi-pack proof? Name the three packs involved and their respective roles.**

7. **How would you configure white-label branding for a new organizational unit? What files and configurations are needed?**

8. **What does the red-team security evidence validate? What zero-tolerance metrics are checked?**

9. **In a SaaS multi-tenant deployment, how do domain pack boundaries combine with database-level row-level security for defense in depth?**

10. **Why should coevolution generation limits be set conservatively (3-5)? What risk increases with higher generation counts?**
