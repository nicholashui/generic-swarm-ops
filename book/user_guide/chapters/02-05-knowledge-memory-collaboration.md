# Chapter 2.5: Knowledge and Memory Collaboration

![Knowledge Retrieval Tiers and Memory Types](../assets/02-05-knowledge-memory-tiers.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Understand the tiered retrieval architecture (Tier 0, Tier 1, Tier 2)
2. Use the knowledge search APIs for both simple and relational queries
3. Work with all eight memory types and their scoping rules
4. Perform document indexing for knowledge base population
5. Use K1-lite graph operations for entity extraction and federation
6. Apply memory scope enforcement in workflow contexts

## Prerequisites

Before starting this chapter, ensure you have:

- Completed Chapters 2.1 through 2.4
- A running backend instance with Postgres connectivity
- Understanding of workflow execution and memory reads/writes
- Familiarity with RAG (Retrieval-Augmented Generation) concepts

---

## The Knowledge Layer Architecture

The knowledge layer in Generic Swarm Business OS separates two distinct concerns:

1. **Knowledge** - Rules, best practices, tacit expertise, policies, and documented procedures
2. **Memory** - Operational state: what happened, what was decided, what was learned

These work together but serve different purposes. Knowledge is relatively stable (policies change infrequently). Memory is dynamic (every workflow run generates new memories).

> **Note:** The design deliberately avoids GraphRAG-style community summarization. Its per-chunk extraction plus community-report generation makes both initial indexing and re-indexing on every new document prohibitively expensive for a system that ingests event logs and documents continuously. Instead, the system uses a cost-tiered retrieval stack.

---

## Tiered Retrieval Architecture

The retrieval system uses three tiers, each progressively more expensive and powerful. An escalation rule routes queries to the cheapest tier that can satisfy them.

### Tier 0 - Vector Search (Default)

**Behavior:** Keyword search with semantic similarity via embeddings. Every hit includes `source_refs` and `provenance.retrieval_tier`.

**When Used:** Always (default tier for all queries).

**Cost:** Lowest - no graph traversal, no extra LLM calls.

**Handles:** 80%+ of all queries ("find the relevant passage" type).

```bash
# Basic Tier 0 query
curl "http://127.0.0.1:8000/api/v1/knowledge?query=billing+gate" \
  -H "Cookie: gso_access_token=<your_token>"
```

Example response:

```json
{
  "results": [
    {
      "content": "Billing configuration requires human gate approval when the action is irreversible.",
      "source_refs": ["business/knowledge-base/rules/billing-policy.md"],
      "provenance": {
        "retrieval_tier": 0,
        "confidence": 0.89,
        "source_type": "policy_document"
      },
      "relevance_score": 0.92
    }
  ],
  "tier_used": 0,
  "query_time_ms": 45
}
```

### Tier 1 - LightRAG Graph Layer (Relational)

**Behavior:** Entity-link multi-hop expansion with dual-level retrieval (low-level entity-specific + high-level thematic).

**When Used:** Relational queries or when `multi_hop=true` is specified.

**Cost:** Medium - graph traversal but no expensive community generation.

**Key Advantage:** Incremental updates. New documents/events are added without rebuilding the entire graph.

```bash
# Tier 1 query with multi-hop
curl "http://127.0.0.1:8000/api/v1/knowledge?query=which+policy+is+related&multi_hop=true" \
  -H "Cookie: gso_access_token=<your_token>"
```

Example response:

```json
{
  "results": [
    {
      "content": "The billing gate policy (billing-policy.md) is connected to the enterprise contract review policy through the 'financial_controls' entity.",
      "source_refs": [
        "business/knowledge-base/rules/billing-policy.md",
        "business/knowledge-base/rules/enterprise-contracts.md"
      ],
      "provenance": {
        "retrieval_tier": 1,
        "confidence": 0.84,
        "hops": 2,
        "entities_traversed": ["billing_gate", "financial_controls", "enterprise_contract_review"]
      },
      "relevance_score": 0.87
    }
  ],
  "tier_used": 1,
  "query_time_ms": 230
}
```

Tier 1 answers relational questions such as:
- "Which obligations depend on this contract?"
- "Who touched this case and in what order?"
- "What policies relate to the billing gate?"

### Tier 2 - RAPTOR Hierarchical Summaries (On Demand)

**Behavior:** Recursive cluster-and-summarize tree built for corpus-wide synthesis.

**When Used:** Global synthesis questions only (deferred/optional tier).

**Cost:** Highest - requires building hierarchical summary trees.

**Key Constraint:** Built lazily, not for the whole knowledge base. Only corpora with frequent corpus-wide questions get Tier 2 treatment.

Tier 2 handles questions like:
- "What are the recurring root causes across all failed onboarding cases?"
- "Summarize all policy exceptions granted in Q3"
- "What common patterns exist across 100+ decision cards?"

> **Tip:** In the current implementation, Tier 2 is deferred. Tier 0 and Tier 1 handle the vast majority of operational queries. Tier 2 will be built on demand for specific corpora that receive frequent synthesis queries.

### Escalation Rule

```text
Query arrives
  -> Try Tier 0 (vector search)
  -> If query needs relationships/multi-hop -> Escalate to Tier 1
  -> If query needs global synthesis -> Escalate to Tier 2
```

This keeps 80%+ of traffic on the cheapest tier, controlling both latency and cost.

### Always-On: Provenance Layer

Regardless of which tier serves a result, **every answer cites its sources**:

- Source documents (file paths, versions)
- Expert sources (who provided the knowledge)
- Event logs (if knowledge came from operational data)
- Decision records (if knowledge came from past decisions)

```json
{
  "provenance": {
    "retrieval_tier": 0,
    "source_refs": ["business/knowledge-base/rules/billing-policy.md"],
    "source_type": "policy_document",
    "last_updated": "2026-06-15T10:00:00Z",
    "authored_by": "compliance_team",
    "confidence": 0.89
  }
}
```

---

## Knowledge Search APIs

### Basic Search (Tier 0)

```bash
# Simple keyword/semantic search
curl "http://127.0.0.1:8000/api/v1/knowledge?query=billing+gate" \
  -H "Cookie: gso_access_token=<your_token>"
```

### Multi-Hop Search (Tier 1)

```bash
# Relational query with graph traversal
curl "http://127.0.0.1:8000/api/v1/knowledge?query=which+policy+is+related&multi_hop=true" \
  -H "Cookie: gso_access_token=<your_token>"
```

### Advanced Search with POST

```bash
# Full search with options
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/search \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>" \
  -d '{
    "query": "What are the approval requirements for enterprise billing?",
    "multi_hop": true,
    "limit": 10
  }'
```

### Document Indexing

To add new documents to the knowledge base and build entity links for Tier 1:

```bash
# Index a document (builds entity_links for Tier-1 edges)
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/documents/doc_123/index \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>"
```

Indexing extracts:
- Entities (people, processes, policies, tools)
- Claims (statements of fact or rule)
- Relations (connections between entities)
- Evidence spans (text supporting each claim)

These extracted elements form the Tier 1 graph edges that enable multi-hop queries.

### Graph Federation

Export the knowledge graph for integration with external graph systems:

```bash
# Federation export (Cypher + GraphAnything-compatible JSON)
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/graph/federate \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>"
```

---

## The Eight Memory Types

The system uses eight differentiated memory types, each serving a specific purpose in the operational lifecycle:

### 1. Event Memory

**Stores:** Raw operational logs - the unprocessed record of what happened.

```json
{
  "type": "event",
  "content": "Agent sent invoice at 9:42 AM to customer_12345.",
  "timestamp": "2026-07-06T09:42:00Z",
  "actor": "business_orchestrator",
  "run_id": "run_abc123"
}
```

**Purpose:** The ground truth of system activity. Event memory is append-only and provides the raw data that feeds Process Intelligence.

### 2. Episodic Memory

**Stores:** Case narratives - higher-level stories about what happened during specific cases.

```json
{
  "type": "episodic",
  "content": "This renewal almost failed - legal was pulled in late because the non-standard clause was not detected until billing configuration.",
  "case_id": "renewal_789",
  "lessons": ["Detect non-standard clauses in verify_contract step"],
  "outcome": "completed_with_delay"
}
```

**Purpose:** Provides context for similar future cases. When a new case matches a previous episodic memory, the system can apply learned lessons proactively.

### 3. Semantic Memory

**Stores:** Facts and rules - stable knowledge about how things work.

```json
{
  "type": "semantic",
  "content": "Enterprise contracts over $250,000 require legal review before billing configuration.",
  "domain": "legal_operations",
  "confidence": 0.95,
  "source": "SOP v4 + expert Alice confirmation"
}
```

**Purpose:** The system's "general knowledge" - facts that apply across cases and do not change frequently.

### 4. Procedural Memory

**Stores:** Skills and workflows - how to do things.

```json
{
  "type": "procedural",
  "content": "How to onboard a new client: 1. Verify contract, 2. Create record, 3. Configure billing (gate), 4. Send welcome.",
  "workflow_id": "wf_customer_onboarding_v12",
  "version": "12.0"
}
```

**Purpose:** Encodes the "how" of operations. Updated when workflow DNA evolves through the Evolution Engine.

### 5. Decision Memory

**Stores:** Decisions and their reasons - why specific choices were made.

```json
{
  "type": "decision",
  "content": "Approved exception for customer X because: pre-approved fallback clause was accepted, enterprise customer, and liability cap within standard range.",
  "decision_id": "dec_456",
  "decision_point": "approve_non_standard_clause",
  "factors": ["customer_size", "liability_cap", "pre_approved_fallback"],
  "outcome": "approved"
}
```

**Purpose:** Enables consistent decision-making. When a similar decision point arises, the system can reference past decisions for guidance.

### 6. Exception Memory

**Stores:** Edge cases - situations that deviated from normal processing.

```json
{
  "type": "exception",
  "content": "If supplier is in region Z, use alternate billing process due to local tax regulations.",
  "trigger_condition": "supplier.region == 'Z'",
  "alternate_path": "use_regional_billing_adapter",
  "discovered_from": "case_exception_2026_03"
}
```

**Purpose:** Captures rare but important deviations. Prevents the system from being surprised by the same edge case twice.

### 7. Evaluation Memory

**Stores:** Test results - how well workflows and agents performed.

```json
{
  "type": "evaluation",
  "content": "Workflow v12 failed privacy test: customer PII was included in welcome packet subject line.",
  "eval_id": "eval_789",
  "target": "wf_customer_onboarding_v12",
  "test_type": "privacy_scan",
  "result": "fail",
  "severity": "medium"
}
```

**Purpose:** Prevents regression. The Evolution Engine checks evaluation memory before promoting variants.

### 8. Provenance Memory

**Stores:** Source attribution - where knowledge and rules came from.

```json
{
  "type": "provenance",
  "content": "The $250K legal review rule came from SOP v4 (section 3.2) and was confirmed by expert Alice during cognitive task analysis session on 2026-03-15.",
  "rule_id": "rule_enterprise_legal_review",
  "sources": [
    {"type": "document", "ref": "sop_v4_section_3.2"},
    {"type": "expert", "ref": "alice_cta_session_20260315"}
  ]
}
```

**Purpose:** Enables trust and verification. Any rule or fact can be traced to its origin, supporting governance reviews and dispute resolution.

---

## Memory Scope Enforcement

Workflow execution enforces `allowed_memory_scopes` on every read and write operation. This prevents agents from accessing memory outside their permitted scope.

### How Scoping Works

```yaml
# In Workflow DNA
memory_reads: ["contract_rules", "customer_exceptions", "past_failures"]
memory_writes: ["event_log", "decision_memory", "lessons_learned"]
```

At runtime, the system validates:

1. Is the requested memory item within the workflow's `allowed_memory_scopes`?
2. Does the agent have permission to read/write this memory type?
3. Is the scope appropriate for the current step?

### Scope Enforcement Example

```text
Agent: business_orchestrator
Step: create_customer_record
Allowed scopes: ["contract_rules", "customer_exceptions", "organization_memory"]

Attempt: Read "security_red_team_results"
Result: DENIED - not in allowed scopes

Attempt: Read "contract_rules"
Result: ALLOWED - within scope
```

### Memory Write Provenance

Every memory write includes automatic provenance:

```json
{
  "memory_write": {
    "type": "decision",
    "content": "Approved billing for standard plan",
    "provenance": {
      "workflow_id": "wf_customer_onboarding_v12",
      "run_id": "run_abc123",
      "step_id": "configure_billing",
      "agent": "tool_permission_broker",
      "timestamp": "2026-07-06T14:10:00Z"
    }
  }
}
```

> **Warning:** Memory writes without provenance are rejected by the system. This ensures every piece of stored information can be traced to its origin.

### Organization Memory and Lessons

Seed agents union `organization_memory` for flagship onboarding paths. Key behaviors:

- Lessons from auto-reflect are written to `organization_memory`
- Improvement lessons go to `improvement_lessons` namespace
- Both are accessible across workflow runs (not scoped to a single case)
- This enables continuous organizational learning

---

## K1-lite Graph Operations

K1-lite is the lightweight knowledge graph implementation that powers Tier 1 retrieval.

### Entity Extraction

When documents are indexed, K1-lite extracts:

| Element | Description | Example |
|---------|-------------|---------|
| Entities | Named concepts, people, processes, tools | "billing_gate", "governance_officer" |
| Claims | Statements of fact or rule | "Billing requires human approval" |
| Relations | Connections between entities | "billing_gate" --requires--> "human_approval" |
| Evidence Spans | Text supporting each claim | "...human gate approval for irreversible..." |

### Graph Operators

K1-lite provides three core operators:

**O1 - Seed Resolve:**
Starting from a query entity, resolve related entities through direct connections.

```bash
# Find all entities directly connected to "billing_gate"
# Returns: human_approval, irreversible_action, financial_controls
```

**O2 - Lineage:**
Trace the provenance chain for a specific fact or rule.

```bash
# Trace where the "$250K legal review" rule came from
# Returns: SOP v4 -> expert Alice -> CTA session -> semantic memory
```

**O5 - Gaps:**
Identify entities or relations that are referenced but not yet documented.

```bash
# Find knowledge gaps in the onboarding domain
# Returns: ["regional_tax_rules" (referenced but not documented),
#           "partner_integration" (entity with no relations)]
```

### Federation Export

Export the K1-lite graph for integration with external systems:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/graph/federate \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>"
```

Produces Cypher-compatible and GraphAnything-compatible JSON:

```json
{
  "format": "cypher_compatible",
  "nodes": [
    {"id": "billing_gate", "type": "process_control", "properties": {...}},
    {"id": "human_approval", "type": "requirement", "properties": {...}}
  ],
  "edges": [
    {"from": "billing_gate", "to": "human_approval", "type": "requires", "evidence": "..."}
  ],
  "export_timestamp": "2026-07-06T15:00:00Z"
}
```

---

## Step-by-Step: Knowledge Base Population

### Step 1: Prepare Documents

Place documents in the appropriate knowledge base folders:

```text
business/knowledge-base/
  rules/           <- Policy rules and constraints
  decision-patterns/ <- Common decision templates
  exceptions/      <- Edge case documentation
  best-practices/  <- Operational best practices
  tacit-knowledge/ <- Expert insights
  provenance/      <- Source attribution records
```

### Step 2: Index Documents

```bash
# Index a specific document
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/documents/billing-policy/index \
  -H "Cookie: gso_access_token=<your_token>"
```

### Step 3: Verify Indexing

```bash
# Search for content from the indexed document
curl "http://127.0.0.1:8000/api/v1/knowledge?query=billing+approval+requirements" \
  -H "Cookie: gso_access_token=<your_token>"
```

### Step 4: Test Multi-Hop Queries

```bash
# Verify Tier 1 graph edges were created
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/search \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>" \
  -d '{
    "query": "What policies are related to billing approval?",
    "multi_hop": true,
    "limit": 5
  }'
```

### Step 5: Review Entity Extraction

After indexing, verify that entities, claims, and relations were properly extracted by checking the graph state.

### Step 6: Check Provenance

```bash
# Verify provenance is attached to all results
curl "http://127.0.0.1:8000/api/v1/knowledge?query=enterprise+contract+review" \
  -H "Cookie: gso_access_token=<your_token>"

# Every result should include provenance with source_refs and retrieval_tier
```

---

## Evaluation and Testing

The knowledge and memory system has its own evaluation framework:

### Unit Tests

- `test_retrieval.py` - Tests provenance attachment and multi-hop retrieval
- Validates that every result includes `source_refs` and `provenance.retrieval_tier`

### Evaluation Fixtures

| Fixture | Purpose |
|---------|---------|
| `business/evals/retrieval/tier0-provenance.json` | Validates Tier 0 returns provenance |
| `business/evals/retrieval/tier1-multi-hop-entity.json` | Validates Tier 1 entity expansion |

### Retrieval Quality Metrics

Score retrieval separately on three dimensions:

1. **Context Relevance** - Are the retrieved passages relevant to the query?
2. **Answer Relevance** - Does the answer address what was asked?
3. **Faithfulness** - Is the answer grounded in the retrieved sources?

> **Warning:** A weak retriever silently poisons every agent. If retrieval returns irrelevant context, agents will generate plausible but incorrect answers. Always evaluate retrieval quality independently.

---

## Retrieval Tier Policy

The system maintains a formal retrieval tier policy at:

```
business/knowledge-base/provenance/retrieval-tier-policy.md
```

This policy defines:

- When to use each tier
- Cost budgets per tier
- Escalation rules
- Quality thresholds for each tier
- Monitoring and alerting for tier usage

---

## Real-World Use Cases

### Use Case 1: Cross-Domain Knowledge Discovery

A legal operations team needs to understand how billing policies affect contract renewals.

**Query:** "What billing constraints apply to enterprise contract renewals?"

**Tier 0 result:** Finds the billing policy document but cannot connect it to contract renewal rules.

**Tier 1 result (multi_hop=true):** Traverses from "billing_constraints" through "enterprise_contracts" to "contract_renewal_process", revealing that:
- Contracts over $250K require legal review before billing changes
- Renewal billing must match original contract terms unless amendment is signed
- Regional tax rules may override standard billing configuration

**Value:** Without multi-hop, the legal team would need to manually search across multiple policy documents.

### Use Case 2: Exception Pattern Learning

An operations manager notices recurring exceptions in the onboarding process.

**Query to Exception Memory:** "What exceptions have occurred in customer onboarding in Q3?"

**Results:**
- 4 cases with non-standard liability clauses (all escalated to legal)
- 2 cases with regional tax exceptions (required alternate billing)
- 1 case with enterprise customer insisting on custom data residency

**Action:** The team creates a new exception rule: "Customers in region Z with liability clauses exceeding $1M require pre-approval from senior counsel."

**Memory Update:** The new rule is written to semantic memory with provenance linking to the 4 original cases.

### Use Case 3: Decision Consistency Verification

A governance reviewer wants to verify that similar cases received similar treatment.

**Query to Decision Memory:** "How have we handled non-standard liability clauses in the past year?"

**Results:** 12 decision records showing:
- 8 approved with standard conditions
- 3 escalated to legal
- 1 rejected (uncapped liability, no fallback)

**Insight:** The pattern reveals that "enterprise customer AND pre-approved fallback accepted" consistently leads to approval. This validates the exception path in the Decision Requirement Card.

---

## Best Practices

### 1. Start with Tier 0 and Escalate

Do not default to multi-hop queries. Most operational questions are answerable with Tier 0:

```bash
# Start here (fast, cheap)
curl "http://127.0.0.1:8000/api/v1/knowledge?query=billing+approval"

# Only escalate if relationships needed
curl "http://127.0.0.1:8000/api/v1/knowledge?query=related+policies&multi_hop=true"
```

### 2. Maintain Provenance at All Times

Never write knowledge or memory without attribution:

```json
// Good: full provenance
{
  "content": "Enterprise contracts need legal review",
  "provenance": {"source": "SOP v4", "expert": "Alice", "date": "2026-03-15"}
}

// Bad: no provenance (will be rejected)
{
  "content": "Enterprise contracts need legal review"
}
```

### 3. Use Appropriate Memory Types

Do not dump everything into one memory type:

| Situation | Correct Memory Type |
|-----------|-------------------|
| Raw log of what happened | Event |
| Story of a case | Episodic |
| A rule that always applies | Semantic |
| How to do something | Procedural |
| Why we chose X | Decision |
| When the normal rule breaks | Exception |
| Test results | Evaluation |
| Where info came from | Provenance |

### 4. Index Documents Incrementally

Index new documents as they arrive rather than batch-rebuilding:

```bash
# Index immediately when a new policy is added
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/documents/new_policy_v1/index
```

K1-lite supports incremental updates - no need to rebuild the entire graph.

### 5. Respect Memory Scope Boundaries

When designing workflows, choose the minimal memory scopes needed:

```yaml
# Good: minimal scopes
memory_reads: ["contract_rules", "customer_exceptions"]

# Bad: overly broad scopes
memory_reads: ["all_rules", "all_exceptions", "all_decisions", "all_evaluations"]
```

### 6. Monitor Retrieval Quality

Regularly evaluate retrieval quality using the built-in fixtures:

- Run `test_retrieval.py` after any knowledge base changes
- Check that provenance is attached to all results
- Verify multi-hop queries return relevant entity chains

### 7. Use Federation for External Integration

If your organization uses Neo4j or other graph databases, use the federation endpoint to export K1-lite data:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/graph/federate
```

This enables integration with enterprise knowledge management systems.

---

## Chapter Summary

In this chapter, you learned:

- The **tiered retrieval architecture** uses three tiers (Tier 0 vector, Tier 1 graph, Tier 2 RAPTOR) with cost-based escalation
- **Tier 0** handles 80%+ of queries cheaply via keyword/embedding search
- **Tier 1 (LightRAG-lite)** enables relational multi-hop queries with incremental updates
- **Tier 2** provides hierarchical summaries for corpus-wide synthesis (built lazily, on demand)
- **Eight memory types** (Event, Episodic, Semantic, Procedural, Decision, Exception, Evaluation, Provenance) serve distinct operational purposes
- **Memory scope enforcement** prevents unauthorized memory access during workflow execution
- **K1-lite graph operations** (seed resolve, lineage, gaps) power entity-based reasoning
- **Provenance** is always-on: every answer traces back to its source regardless of retrieval tier
- **Federation export** enables integration with external graph systems (Cypher/GraphAnything JSON)

---

## Knowledge Check Quiz

Test your understanding of knowledge and memory collaboration:

**Question 1:** What are the three retrieval tiers and when is each used?

<details>
<summary>Show Answer</summary>
Tier 0 (Vector Search): Used by default for all queries - keyword/embedding similarity, cheapest, handles 80%+ of traffic. Tier 1 (LightRAG Graph): Used for relational queries or when multi_hop=true - entity-link multi-hop expansion with incremental updates. Tier 2 (RAPTOR Summaries): Used for global synthesis questions only - hierarchical cluster-and-summarize, built lazily on demand.
</details>

**Question 2:** Why was GraphRAG-style community summarization deliberately avoided?

<details>
<summary>Show Answer</summary>
GraphRAG's per-chunk extraction plus community-report generation makes both initial indexing and re-indexing on every new document prohibitively expensive for a system that ingests event logs and documents continuously. LightRAG was chosen instead because it supports incremental updates without rebuilding the graph.
</details>

**Question 3:** Name all eight memory types and give a one-sentence description of each.

<details>
<summary>Show Answer</summary>
(1) Event - raw operational logs, (2) Episodic - case narratives, (3) Semantic - facts and rules, (4) Procedural - skills and workflows, (5) Decision - decisions and their reasons, (6) Exception - edge cases and deviations, (7) Evaluation - test results and performance data, (8) Provenance - source attribution for all knowledge.
</details>

**Question 4:** What does the provenance layer guarantee?

<details>
<summary>Show Answer</summary>
The provenance layer guarantees that every answer cites its source documents, experts, event logs, or decisions, regardless of which retrieval tier served the result. This enables trust, verification, governance reviews, and dispute resolution by making all knowledge traceable to its origin.
</details>

**Question 5:** What are the three K1-lite graph operators and what does each do?

<details>
<summary>Show Answer</summary>
O1 (Seed Resolve): Starting from a query entity, resolves related entities through direct connections. O2 (Lineage): Traces the provenance chain for a specific fact or rule back to its origins. O5 (Gaps): Identifies entities or relations that are referenced but not yet documented, revealing knowledge gaps.
</details>

**Question 6:** How does memory scope enforcement work during workflow execution?

<details>
<summary>Show Answer</summary>
The workflow DNA declares allowed_memory_scopes. At runtime, every memory read and write is validated against these scopes. If an agent attempts to access memory outside its permitted scopes, the request is denied. This prevents agents from accessing information outside their need-to-know boundary. Seed agents union organization_memory for flagship paths.
</details>

**Question 7:** What is the escalation rule for retrieval tier selection?

<details>
<summary>Show Answer</summary>
Start at Tier 0 (vector search). If the query needs relationships or multi-hop reasoning, escalate to Tier 1 (graph layer). If the query needs global synthesis across the entire corpus, escalate to Tier 2 (RAPTOR summaries). This keeps 80%+ of traffic on the cheapest tier, controlling both latency and cost.
</details>

---

## Next Steps

Congratulations on completing Section 2! You now have intermediate-level knowledge of the Generic Swarm Business OS core workflows. In Section 3, you will advance to creating custom workflows, building domain packs, and implementing advanced evolution strategies.
