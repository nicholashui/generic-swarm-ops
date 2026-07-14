# Chapter 3.2: API Integration and Extension

## Learning Objectives

By the end of this chapter, you will be able to:

1. Navigate the full FastAPI API surface and understand route group organization
2. Implement authentication flows using password-based login and bearer tokens
3. Perform workflow CRUD operations, run execution, and approval queue management
4. Integrate with knowledge search, memory operations, and process intelligence APIs
5. Handle structured error envelopes with request IDs for debugging
6. Extend the API with custom integrations using proper middleware patterns
7. Implement rate limiting and security header best practices

## Prerequisites

- Completed Chapter 3.1 (Custom Domain Pack Development)
- Running Generic Swarm Ops backend (`uvicorn app.main:app --reload`)
- Familiarity with RESTful API concepts and HTTP methods
- `curl` or an API client (Postman, HTTPie) installed
- Understanding of JWT/bearer token authentication patterns

---

## Architecture Overview

![API Architecture](../assets/03-02-api-architecture.svg)

The Generic Swarm Ops API is built on FastAPI and organized into logical route groups. Every request passes through authentication, middleware (request-ID injection, CORS, security headers, rate limiting), and structured error handling before reaching backend services.

### API Base URL

```
http://127.0.0.1:8000/api/v1
```

### Health Check

```bash
# Verify the backend is running
curl http://127.0.0.1:8000/api/v1/health/ready
```

**Response:**

```json
{
  "status": "healthy",
  "database": "postgres",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Step-by-Step: Authentication

### Step 1: Password-Based Login

The primary authentication method uses PBKDF2 password hashing with session cookies:

```bash
# Login with email and password
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin-password"
  }' \
  -c cookies.txt
```

**Response:**

```json
{
  "user": {
    "id": "usr_001",
    "email": "admin@example.com",
    "role": "admin",
    "organization_id": "org_default"
  },
  "message": "Login successful"
}
```

The response sets a `gso_access_token` cookie and a session user cookie. Subsequent requests should include these cookies.

### Step 2: Bearer Token Authentication

For programmatic/CLI access, use bearer tokens:

```bash
# Using bearer token
curl http://127.0.0.1:8000/api/v1/workflows \
  -H "Authorization: Bearer admin-token"
```

> **Warning:** Static bearer tokens (`admin-token`) are intended for development and curl smoke testing only. In production, always use password-based login with session cookies or implement a proper OAuth2 flow.

### Step 3: Cookie-Based Session Flow

After login, use the session cookie for subsequent requests:

```bash
# Use cookie from login
curl http://127.0.0.1:8000/api/v1/auth/me \
  -b cookies.txt
```

**Response:**

```json
{
  "id": "usr_001",
  "email": "admin@example.com",
  "role": "admin",
  "organization_id": "org_default",
  "permissions": ["workflows:read", "workflows:write", "runs:execute", "approvals:manage"]
}
```

---

## Step-by-Step: Workflow Operations

### Step 4: List Workflows

```bash
curl http://127.0.0.1:8000/api/v1/workflows \
  -H "Authorization: Bearer admin-token"
```

**Response:**

```json
{
  "workflows": [
    {
      "id": "wf_customer_onboarding_v12",
      "display_name": "Customer Onboarding",
      "version": 12,
      "status": "active",
      "risk_tier": 3,
      "domain": "ops",
      "created_at": "2024-01-10T08:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20
}
```

### Step 5: Create a Workflow

```bash
curl -X POST http://127.0.0.1:8000/api/v1/workflows \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "wf_data_analysis_v1",
    "display_name": "Data Analysis Pipeline",
    "domain": "my_domain",
    "risk_tier": 2,
    "steps": [
      {
        "id": "intake",
        "agent": "my_domain.intake_agent",
        "action": "classify_input",
        "risk_tier": 0
      },
      {
        "id": "analyze",
        "agent": "my_domain.analysis_agent",
        "action": "deep_analysis",
        "risk_tier": 2
      },
      {
        "id": "report",
        "agent": "my_domain.synthesis_agent",
        "action": "generate_report",
        "risk_tier": 2,
        "requires_approval": true
      }
    ]
  }'
```

**Response:**

```json
{
  "id": "wf_data_analysis_v1",
  "status": "created",
  "version": 1,
  "created_at": "2024-01-15T11:00:00Z"
}
```

### Step 6: Execute a Workflow Run

```bash
# Start a new run
curl -X POST http://127.0.0.1:8000/api/v1/runs \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "wf_customer_onboarding_v12",
    "payload": {
      "case_id": "case_2024_001",
      "customer_name": "Acme Corp",
      "tier": "enterprise"
    }
  }'
```

**Response:**

```json
{
  "run_id": "run_abc123",
  "workflow_id": "wf_customer_onboarding_v12",
  "status": "running",
  "started_at": "2024-01-15T11:05:00Z",
  "current_step": "intake"
}
```

> **Note:** The `case_id` field is required for the flagship `wf_customer_onboarding_v12` workflow. Other workflows may have different required payload fields defined in their DNA.

### Step 7: Check Run Status

```bash
# Get run status and detail
curl http://127.0.0.1:8000/api/v1/runs/run_abc123 \
  -H "Authorization: Bearer admin-token"
```

**Response:**

```json
{
  "run_id": "run_abc123",
  "workflow_id": "wf_customer_onboarding_v12",
  "status": "awaiting_approval",
  "started_at": "2024-01-15T11:05:00Z",
  "current_step": "billing_setup",
  "steps_completed": 3,
  "steps_total": 5,
  "pending_approval": {
    "step_id": "billing_setup",
    "approval_type": "human_gate",
    "reason": "Tier 4 irreversible action requires human approval"
  }
}
```

---

## Step-by-Step: Approval Queue

### Step 8: List Pending Approvals

```bash
curl http://127.0.0.1:8000/api/v1/approvals \
  -H "Authorization: Bearer admin-token"
```

**Response:**

```json
{
  "approvals": [
    {
      "id": "appr_xyz789",
      "run_id": "run_abc123",
      "step_id": "billing_setup",
      "workflow_id": "wf_customer_onboarding_v12",
      "risk_tier": 4,
      "requested_at": "2024-01-15T11:06:00Z",
      "sla_deadline": "2024-01-15T12:06:00Z",
      "context": {
        "action": "create_billing_account",
        "customer": "Acme Corp",
        "amount": "enterprise_tier"
      }
    }
  ],
  "total_pending": 1
}
```

### Step 9: Approve or Reject

```bash
# Approve
curl -X POST http://127.0.0.1:8000/api/v1/approvals/appr_xyz789/approve \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "approved",
    "reviewer_notes": "Customer verified, billing details confirmed"
  }'

# Reject
curl -X POST http://127.0.0.1:8000/api/v1/approvals/appr_xyz789/reject \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "rejected",
    "reviewer_notes": "Customer credit check failed",
    "escalation": false
  }'
```

---

## Step-by-Step: Knowledge and Memory

### Step 10: Search Knowledge Base

```bash
# Keyword + semantic search
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/search \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "customer onboarding best practices",
    "limit": 10,
    "tier": 0
  }'
```

**Response:**

```json
{
  "results": [
    {
      "document_id": "doc_001",
      "title": "Enterprise Onboarding SOP",
      "snippet": "Step 1: Verify customer identity...",
      "score": 0.92,
      "source": "knowledge/seeds/onboarding_sop.md"
    }
  ],
  "total": 5,
  "search_tier": 0
}
```

### Step 11: Query Knowledge Graph

```bash
# Seed + neighborhood graph query
curl "http://127.0.0.1:8000/api/v1/knowledge/graph/query?seed=customer_onboarding&depth=2" \
  -H "Authorization: Bearer admin-token"
```

**Response:**

```json
{
  "nodes": [
    {"id": "n_001", "type": "process", "label": "Customer Onboarding"},
    {"id": "n_002", "type": "entity", "label": "KYC Verification"},
    {"id": "n_003", "type": "entity", "label": "Account Setup"}
  ],
  "edges": [
    {"source": "n_001", "target": "n_002", "relation": "REQUIRES"},
    {"source": "n_001", "target": "n_003", "relation": "INCLUDES"}
  ]
}
```

### Step 12: Detect Knowledge Gaps

```bash
curl http://127.0.0.1:8000/api/v1/knowledge/graph/gaps \
  -H "Authorization: Bearer admin-token"
```

**Response:**

```json
{
  "gaps": [
    {
      "type": "missing_relation",
      "entity": "Compliance Check",
      "expected_connections": ["KYC Verification", "Risk Assessment"],
      "actual_connections": ["KYC Verification"],
      "recommendation": "Add BUILD_ON relation to Risk Assessment"
    }
  ],
  "total_gaps": 3
}
```

### Step 13: Memory Operations

```bash
# Store a memory (agent-scoped)
curl -X POST http://127.0.0.1:8000/api/v1/memory \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "my_domain.analysis_agent",
    "scope": "agent",
    "content": "Customer Acme Corp prefers PDF reports over HTML",
    "category": "preference",
    "provenance": {
      "source_run": "run_abc123",
      "confidence": 0.95
    }
  }'

# Retrieve agent memories
curl "http://127.0.0.1:8000/api/v1/memory?agent_id=my_domain.analysis_agent&scope=agent&limit=20" \
  -H "Authorization: Bearer admin-token"
```

> **Note:** Memory writes to high-impact scopes require provenance metadata for poisoning defense. The `provenance` field records where the information originated and its confidence level.

---

## Step-by-Step: Process Intelligence

### Step 14: Query Process Mining Data

```bash
# Get process summaries
curl http://127.0.0.1:8000/api/v1/processes \
  -H "Authorization: Bearer admin-token"
```

**Response:**

```json
{
  "processes": [
    {
      "process_id": "proc_onboarding",
      "display_name": "Customer Onboarding",
      "total_runs": 142,
      "avg_cycle_time_minutes": 45,
      "completion_rate": 0.94,
      "bottleneck_step": "billing_setup",
      "last_run": "2024-01-15T10:00:00Z"
    }
  ]
}
```

---

## Middleware and Error Handling

### Request ID Tracking

Every API response includes a unique `X-Request-ID` header for tracing:

```bash
curl -v http://127.0.0.1:8000/api/v1/workflows \
  -H "Authorization: Bearer admin-token" 2>&1 | grep -i x-request-id
```

```
< X-Request-ID: req_f47ac10b-58cc-4372-a567-0e02b2c3d479
```

### Structured Error Envelopes

All errors follow a consistent structure:

```json
{
  "error": "validation_error",
  "detail": "Field 'case_id' is required for workflow wf_customer_onboarding_v12",
  "request_id": "req_f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "timestamp": "2024-01-15T11:10:00Z",
  "path": "/api/v1/runs"
}
```

Common error codes:

| HTTP Status | Error Type | Description |
|-------------|-----------|-------------|
| 400 | `validation_error` | Invalid request payload |
| 401 | `authentication_required` | Missing or invalid credentials |
| 403 | `permission_denied` | Insufficient role/permissions |
| 404 | `not_found` | Resource does not exist |
| 409 | `conflict` | State conflict (e.g., already approved) |
| 422 | `unprocessable_entity` | Semantic validation failure |
| 429 | `rate_limited` | Too many requests on sensitive route |
| 500 | `internal_error` | Unexpected server error |

### Rate Limiting

Sensitive routes enforce rate limits:

```
POST /api/v1/auth/login         - 5 requests per minute per IP
POST /api/v1/runs               - 30 requests per minute per user
POST /api/v1/evolution/variants - 10 requests per minute per user
POST /api/v1/improvement/*      - 20 requests per minute per user
```

When rate limited:

```json
{
  "error": "rate_limited",
  "detail": "Rate limit exceeded. Retry after 32 seconds.",
  "retry_after": 32,
  "request_id": "req_123"
}
```

> **Tip:** When integrating with the API programmatically, always implement exponential backoff with jitter for rate-limited responses. Extract the `retry_after` value from the response and add random jitter (0-5 seconds) to avoid thundering herd problems when multiple clients retry simultaneously.

### Security Headers

The API sets these security headers on all responses:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

### CORS Configuration

CORS is configured for the frontend origin:

```python
# Backend CORS settings
origins = [
    "http://localhost:3000",      # Next.js dev server
    "http://127.0.0.1:3000",
    os.getenv("FRONTEND_URL", "")
]
```

---

## Complete API Reference

### Auth Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/auth/login` | Password login, sets session cookie |
| POST | `/api/v1/auth/register` | Register new user |
| GET | `/api/v1/auth/me` | Current user profile |
| POST | `/api/v1/auth/logout` | Invalidate session |

### Workflow Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/workflows` | List all workflows |
| POST | `/api/v1/workflows` | Create workflow |
| GET | `/api/v1/workflows/{id}` | Get workflow detail |
| PUT | `/api/v1/workflows/{id}` | Update workflow |
| DELETE | `/api/v1/workflows/{id}` | Delete workflow |

### Run Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/runs` | Execute a workflow run |
| GET | `/api/v1/runs/{id}` | Get run status/detail |
| GET | `/api/v1/runs` | List runs (filterable) |

### Approval Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/approvals` | List pending approvals |
| POST | `/api/v1/approvals/{id}/approve` | Approve a gate |
| POST | `/api/v1/approvals/{id}/reject` | Reject a gate |

### Knowledge Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/knowledge/search` | Keyword + semantic search |
| POST | `/api/v1/knowledge/graph/extract/{document_id}` | Build graph from doc |
| GET | `/api/v1/knowledge/graph/query` | Seed + neighborhood query |
| GET | `/api/v1/knowledge/graph/gaps` | Gap detection |
| POST | `/api/v1/knowledge/graph/federate` | Export to Neo4j/JSON |

### Memory Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/memory` | Store memory entry |
| GET | `/api/v1/memory` | Retrieve memories (filtered) |

### Process Intelligence Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/processes` | List process summaries |

### Evolution Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/evolution/variants` | Propose evolution variant |
| POST | `/api/v1/evolution/variants/{id}/evaluate` | Corpus evaluation |
| POST | `/api/v1/evolution/variants/{id}/promote` | Canary or promote |
| POST | `/api/v1/evolution/variants/{id}/rollback` | Rollback variant |
| GET | `/api/v1/evolution/archive` | Population ranked by fitness |
| POST | `/api/v1/evolution/coevolution/run` | Multi-domain coevolution |
| GET | `/api/v1/evolution/governance/review` | Governance review queue |

### Improvement Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/improvement/reflect/{run_id}` | Extract lessons from run |
| GET | `/api/v1/improvement/lessons` | List lesson library |
| POST | `/api/v1/improvement/auto-propose` | Auto-propose variant from failures |
| GET | `/api/v1/improvement/lesson-utility` | Lesson utility dashboard |
| GET | `/api/v1/improvement/metrics` | Agent improvement metrics |
| POST | `/api/v1/improvement/skills/propose` | Propose skill sandbox change |

### Loop Engineering Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/loops/run` | Start governed improvement loop |
| GET | `/api/v1/loops/{id}` | Loop run status |

### Domain Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/domains/register` | Register domain pack |
| GET | `/api/v1/domains/video/n3-status` | N3 inventory status |

### Agent Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/agents` | List agents |
| GET | `/api/v1/agents/{id}` | Get agent detail |
| PATCH | `/api/v1/agents/{id}` | Update agent (activate) |

### Settings and Health Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/settings` | Get system settings |
| PUT | `/api/v1/settings` | Update settings |
| GET | `/api/v1/health/ready` | Readiness check |

---

## Real-World Use Cases

### Use Case 1: Building a Custom Dashboard Integration

A team builds an external dashboard that aggregates run metrics:

```python
import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"
HEADERS = {"Authorization": "Bearer admin-token"}

def get_dashboard_metrics():
    """Aggregate metrics for external dashboard."""
    # Get all runs from the last 24 hours
    runs = requests.get(
        f"{BASE_URL}/runs?since=24h&status=completed",
        headers=HEADERS
    ).json()

    # Get process intelligence summaries
    processes = requests.get(
        f"{BASE_URL}/processes",
        headers=HEADERS
    ).json()

    # Get pending approvals count
    approvals = requests.get(
        f"{BASE_URL}/approvals",
        headers=HEADERS
    ).json()

    # Get evolution archive fitness
    archive = requests.get(
        f"{BASE_URL}/evolution/archive",
        headers=HEADERS
    ).json()

    return {
        "runs_completed_24h": len(runs.get("runs", [])),
        "avg_cycle_time": processes["processes"][0]["avg_cycle_time_minutes"],
        "pending_approvals": approvals["total_pending"],
        "top_variant_fitness": archive[0]["fitness"] if archive else None
    }
```

### Use Case 2: Automated CI/CD Integration

A CI pipeline triggers evaluation after workflow changes:

```bash
#!/bin/bash
# ci-evaluate.sh - Run after workflow DNA changes

WORKFLOW_ID="wf_customer_onboarding_v12"
BASE_URL="http://127.0.0.1:8000/api/v1"
AUTH="Authorization: Bearer admin-token"

# 1. Propose evolution variant
VARIANT=$(curl -s -X POST "$BASE_URL/evolution/variants" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d "{\"workflow_id\": \"$WORKFLOW_ID\", \"source\": \"ci_pipeline\"}" \
  | jq -r '.variant_id')

echo "Proposed variant: $VARIANT"

# 2. Evaluate against corpus
EVAL=$(curl -s -X POST "$BASE_URL/evolution/variants/$VARIANT/evaluate" \
  -H "$AUTH" \
  | jq -r '.fitness')

echo "Fitness score: $EVAL"

# 3. Check fitness threshold
if (( $(echo "$EVAL > 0.85" | bc -l) )); then
  echo "PASS: Fitness $EVAL exceeds threshold 0.85"
  exit 0
else
  echo "FAIL: Fitness $EVAL below threshold 0.85"
  exit 1
fi
```

### Use Case 3: Webhook-Driven Run Automation

An external system triggers workflow runs via webhook:

```python
from fastapi import FastAPI, Request
import httpx

webhook_app = FastAPI()

GSO_BASE = "http://127.0.0.1:8000/api/v1"
GSO_TOKEN = "admin-token"

@webhook_app.post("/webhooks/new-customer")
async def handle_new_customer(request: Request):
    """Webhook handler that triggers GSO workflow on new customer signup."""
    payload = await request.json()

    async with httpx.AsyncClient() as client:
        # Trigger onboarding workflow
        response = await client.post(
            f"{GSO_BASE}/runs",
            headers={
                "Authorization": f"Bearer {GSO_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "workflow_id": "wf_customer_onboarding_v12",
                "payload": {
                    "case_id": f"case_{payload['customer_id']}",
                    "customer_name": payload["name"],
                    "tier": payload.get("tier", "standard")
                }
            }
        )

        result = response.json()
        return {
            "status": "triggered",
            "run_id": result["run_id"],
            "message": f"Onboarding initiated for {payload['name']}"
        }
```

---

## Best Practices

### Authentication

1. **Use cookie-based sessions for browser clients.** The `gso_access_token` cookie provides secure, httpOnly session management.

2. **Use bearer tokens only for development/testing.** Static tokens should never appear in production code or be shared across environments.

3. **Implement token rotation.** For long-lived integrations, implement a refresh flow rather than using permanent tokens.

### Error Handling

4. **Always capture the `request_id`.** Include it in support tickets and debugging logs. It correlates to backend trace entries.

5. **Implement exponential backoff for 429 responses.** Respect the `retry_after` field and implement jitter to avoid thundering herd issues.

6. **Handle 409 conflicts gracefully.** State conflicts (e.g., approving an already-approved gate) should trigger a state refresh, not a retry.

### Integration Patterns

7. **Poll run status with backoff.** For async runs, start with 2-second intervals and increase to 10-second intervals after 30 seconds.

8. **Batch knowledge queries.** If you need multiple graph queries, use the federate endpoint to export a subgraph rather than making many individual queries.

9. **Use request-ID correlation.** Pass your own `X-Request-ID` header to correlate your client logs with GSO backend logs.

10. **Validate payloads client-side.** Check required fields before sending to reduce 400 error rates and improve user experience.

### Security

11. **Never log bearer tokens or passwords.** Mask sensitive fields in your application logs.

12. **Validate CORS origins in production.** Configure `FRONTEND_URL` environment variable to restrict cross-origin access.

13. **Use HTTPS in production.** The security headers assume TLS termination; running without HTTPS negates HSTS protection.

---

## Chapter Summary

In this chapter, you learned how to:

- Authenticate using password-based login (cookie sessions) and bearer tokens
- Navigate the complete API surface across 12+ route groups
- Execute workflow runs with proper payloads and monitor their status
- Manage the human approval queue for gated workflow steps
- Query the knowledge base (search, graph, gap detection) and manage agent memory
- Handle structured error envelopes with request-ID tracking
- Implement rate limiting awareness and security header best practices
- Build integrations including dashboards, CI/CD pipelines, and webhook handlers

The API is designed for composability: each route group handles one concern cleanly, and the middleware layer provides consistent security, tracing, and error handling across all endpoints.

---

## Knowledge Check

1. **What are the two authentication methods supported by the API? Which one is recommended for production browser clients?**

2. **Write a curl command to start a workflow run for `wf_customer_onboarding_v12`. What field is required in the payload?**

3. **Describe the structured error envelope format. What fields are always present in an error response?**

4. **What rate limits apply to the `/api/v1/auth/login` endpoint? What happens when the limit is exceeded?**

5. **How does the approval queue work? What information is available to a reviewer before making a decision?**

6. **Explain the difference between `/api/v1/knowledge/search` and `/api/v1/knowledge/graph/query`. When would you use each?**

7. **What security headers does the API set on all responses? Why is each one important?**

8. **How do you correlate a client request with backend logs? What header enables this?**

9. **What is the correct sequence to register a domain pack, activate an agent, and verify it can receive lessons?**

10. **Describe how to build a CI pipeline that proposes an evolution variant, evaluates it against the corpus, and gates on fitness score.**
