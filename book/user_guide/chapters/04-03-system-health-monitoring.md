# Chapter 4.3: System Health Monitoring

![Health Monitoring Dashboard](../assets/04-03-health-monitoring-dashboard.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Configure and query the health endpoint for real-time system status
2. Monitor database connectivity and runtime state
3. Inspect audit logs for operational intelligence
4. Track process intelligence artifact integrity
5. Monitor evolution sandbox status and tool adapter health
6. Design monitoring dashboards for production deployments

## Prerequisites

Before working through this chapter, ensure you have:

- Backend service running with PostgreSQL connected
- Successful authentication (admin credentials available)
- Familiarity with the API endpoints from Chapter 2
- Understanding of the six-layer architecture from Chapter 1.1

---

## 1. Health Endpoint Fundamentals

The primary health check endpoint is the foundation of all system monitoring:

```
GET /api/v1/health/ready
```

### 1.1 Querying the Health Endpoint

**Step 1:** Make a basic health check request:

```bash
curl -s http://127.0.0.1:8000/api/v1/health/ready
```

**Step 2:** Interpret the response:

```json
{
  "status": "healthy",
  "database": "postgres",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Key Fields:**
| Field | Healthy Value | Unhealthy Value |
|-------|--------------|-----------------|
| `status` | `"healthy"` | `"degraded"` or `"unavailable"` |
| `database` | `"postgres"` | `"unavailable"` or missing |
| `timestamp` | Current time | Stale or missing |

**Step 3:** Verify with formatted output:

```bash
curl -s http://127.0.0.1:8000/api/v1/health/ready | python -m json.tool
```

> **Tip:** If the `database` field does not show `"postgres"`, the system cannot persist data reliably. Resolve this before any other monitoring work.

### 1.2 Automated Health Polling

For continuous monitoring, set up periodic health checks:

```bash
#!/bin/bash
# health-monitor.sh - Simple health polling script
ENDPOINT="http://127.0.0.1:8000/api/v1/health/ready"
INTERVAL=30  # seconds

while true; do
  response=$(curl -s -w "\n%{http_code}" "$ENDPOINT")
  http_code=$(echo "$response" | tail -1)
  body=$(echo "$response" | head -1)
  
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  
  if [ "$http_code" = "200" ]; then
    db_status=$(echo "$body" | python -c "import sys,json; print(json.load(sys.stdin).get('database','unknown'))" 2>/dev/null)
    echo "[$timestamp] OK - database: $db_status"
  else
    echo "[$timestamp] FAIL - HTTP $http_code"
  fi
  
  sleep $INTERVAL
done
```

### 1.3 Health Check Response Codes

| HTTP Status | Meaning | Action Required |
|-------------|---------|-----------------|
| 200 | System healthy | None |
| 503 | Service unavailable | Check Postgres, restart backend |
| Connection refused | Backend not running | Start uvicorn |
| Timeout | Backend overloaded | Check resource usage |

---

## 2. Database Connectivity Monitoring

### 2.1 PostgreSQL Connection Verification

The database is the primary persistence layer. Monitor its health independently:

**Step 1:** Check PostgreSQL is accepting connections:

```bash
pg_isready -h localhost -p 5432
```

Expected output:
```
localhost:5432 - accepting connections
```

**Step 2:** Verify the specific database exists and is accessible:

```bash
psql "$DATABASE_URL" -c "SELECT 1 AS connectivity_check;"
```

Expected output:
```
 connectivity_check 
--------------------
                  1
(1 row)
```

**Step 3:** Check database size and table count:

```bash
psql "$DATABASE_URL" -c "
  SELECT 
    pg_size_pretty(pg_database_size(current_database())) as db_size,
    (SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public') as table_count;
"
```

### 2.2 Runtime State Inspection

The backend uses Postgres JSONB for runtime state. Monitor the state table:

```bash
psql "$DATABASE_URL" -c "
  SELECT 
    count(*) as total_entries,
    max(updated_at) as last_update,
    pg_size_pretty(pg_total_relation_size('runtime_state')) as table_size
  FROM runtime_state;
"
```

**Expected Behavior:**
- `total_entries` grows as workflows execute
- `last_update` should be recent (within minutes during active use)
- `table_size` growth should be linear, not exponential

> **Warning:** If `last_update` is stale but the backend is running, this may indicate the backend lost its database connection. Restart the backend service.

### 2.3 Connection Pool Monitoring

For production deployments, monitor connection pool health:

```bash
psql "$DATABASE_URL" -c "
  SELECT 
    state,
    count(*) as connections
  FROM pg_stat_activity 
  WHERE datname = current_database()
  GROUP BY state;
"
```

**Healthy Pattern:**
```
   state   | connections 
-----------+-------------
 idle      |           3
 active    |           1
```

**Unhealthy Pattern:**
```
   state   | connections 
-----------+-------------
 idle      |          45
 active    |          20
 waiting   |           5
```

> **Note:** If connections are high or many are in "waiting" state, the connection pool may be exhausted. Consider increasing `max_connections` in PostgreSQL or reducing pool size in the backend configuration.

---

## 3. Audit Log Monitoring

### 3.1 Querying Audit Logs

The audit system records all significant operations. Use it for operational monitoring:

**Step 1:** Authenticate:

```bash
# Login and capture the cookie
curl -s -c cookies.txt -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}'
```

**Step 2:** Query recent audit events:

```bash
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/audit?limit=20" \
  | python -m json.tool
```

**Step 3:** Filter by event type:

```bash
# Tool execution events
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/audit?event_type=tool.executed"

# Workflow state transitions
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/audit?event_type=workflow.transition"

# Authentication events
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/audit?event_type=auth.login"
```

### 3.2 Key Audit Event Types

| Event Type | Description | Monitor For |
|------------|-------------|-------------|
| `tool.executed` | Tool adapter ran | Failed executions, unexpected tools |
| `workflow.transition` | Workflow state changed | Stuck states, unexpected transitions |
| `auth.login` | User authenticated | Failed attempts, unusual patterns |
| `memory.write` | Memory scope written | Scope violations, excessive writes |
| `improvement.reflect` | Self-improvement reflection | Reflection quality, lesson generation |
| `evolution.propose` | Variant proposed | Proposal frequency, quality |

### 3.3 Monitoring for Anomalies

Set up anomaly detection on audit logs:

```bash
#!/bin/bash
# audit-monitor.sh - Check for concerning audit patterns

TOKEN_COOKIE="cookies.txt"
API="http://127.0.0.1:8000/api/v1"

# Check for failed tool executions in last hour
echo "=== Failed Tool Executions ==="
curl -s -b "$TOKEN_COOKIE" \
  "$API/audit?event_type=tool.executed&status=failed&since=1h" \
  | python -c "
import sys, json
data = json.load(sys.stdin)
if len(data) > 0:
    print(f'WARNING: {len(data)} failed tool executions')
    for entry in data[:5]:
        print(f'  - {entry.get(\"tool_name\", \"unknown\")} at {entry.get(\"timestamp\", \"?\")}')
else:
    print('OK: No failed tool executions')
"

# Check for authentication failures
echo ""
echo "=== Auth Failures ==="
curl -s -b "$TOKEN_COOKIE" \
  "$API/audit?event_type=auth.login&status=failed&since=1h" \
  | python -c "
import sys, json
data = json.load(sys.stdin)
if len(data) > 3:
    print(f'ALERT: {len(data)} auth failures in last hour (possible brute force)')
else:
    print(f'OK: {len(data)} auth failure(s)')
"
```

> **Tip:** In production, feed audit events into a log aggregation system (ELK, Datadog, etc.) for real-time alerting and historical analysis.

---

## 4. Process Intelligence Artifact Monitoring

### 4.1 Event Ingestion Status

Process intelligence relies on continuous event ingestion. Monitor the pipeline:

```bash
# Check for recent process intelligence artifacts
ls -la business/process-intelligence/

# Expected contents:
# - event logs
# - discovered processes
# - conformance results
# - bottleneck analysis
```

**Verification Steps:**

1. Check that event logs are being written:

```bash
find business/process-intelligence/ -name "*.json" -mmin -60
```

2. Verify artifact freshness (should have recent modification times):

```bash
stat business/process-intelligence/discovered-processes.json
```

3. Check conformance analysis is current:

```bash
cat business/process-intelligence/conformance-report.json | python -m json.tool | head -20
```

### 4.2 Process Mining Health

Process mining generates artifacts from event data. Monitor for:

| Artifact | Expected Freshness | Alert If |
|----------|-------------------|----------|
| Event logs | Updated per workflow run | No updates in 24h during active use |
| Discovered processes | Updated per analysis cycle | Missing or empty |
| Conformance results | Updated after discovery | Stale (older than last discovery) |
| Bottleneck analysis | Updated weekly minimum | Missing or empty |

### 4.3 Knowledge Base Integrity

The knowledge base supports retrieval and federation. Monitor:

```bash
# Check retrieval tier policy
cat business/knowledge-base/provenance/retrieval-tier-policy.md

# Verify knowledge artifacts exist
ls business/knowledge-base/

# Check federation status (if Neo4j is configured)
if [ -n "$NEO4J_URI" ]; then
  curl -s -b cookies.txt \
    "http://127.0.0.1:8000/api/v1/knowledge/graph/federate" \
    | python -m json.tool
fi
```

---

## 5. Evolution Sandbox Monitoring

### 5.1 Sandbox Status Overview

The evolution sandbox contains proposed variants awaiting promotion:

```bash
# Check sandbox contents
ls business/distilled/skills/_sandbox/

# Use the evolution archive API
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/evolution/archive" \
  | python -m json.tool
```

### 5.2 Evolution Pipeline Health

Monitor the self-improvement pipeline stages:

```bash
# Check recent reflections
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/improvement/lessons" \
  | python -c "
import sys, json
data = json.load(sys.stdin)
print(f'Total lessons: {len(data)}')
if data:
    latest = data[0]
    print(f'Latest: {latest.get(\"title\", \"untitled\")} ({latest.get(\"created_at\", \"unknown\")})')
"
```

**Pipeline Stages to Monitor:**

1. **Reflect:** Are reflections being generated after runs?
2. **Propose:** Are proposals being created from reflections?
3. **Evaluate:** Are proposals being tested against golden tasks?
4. **Canary:** Are passing proposals deployed for comparison?
5. **Promote/Rollback:** Are decisions being made on canary results?

### 5.3 Lesson Library Growth

Track the growth and quality of the lesson library:

```bash
# Count lessons by category
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/improvement/lessons" \
  | python -c "
import sys, json
from collections import Counter
data = json.load(sys.stdin)
categories = Counter(l.get('category', 'uncategorized') for l in data)
print('Lessons by category:')
for cat, count in categories.most_common():
    print(f'  {cat}: {count}')
print(f'  Total: {len(data)}')
"
```

---

## 6. Tool Adapter Health

### 6.1 Fail-Closed Behavior Monitoring

Tool adapters (crm, billing, email, audit, contract_parser, policy_retriever) use fail-closed behavior. Monitor for rejected executions:

```bash
# Query tool execution audit trail
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/audit?event_type=tool.executed" \
  | python -c "
import sys, json
data = json.load(sys.stdin)
total = len(data)
failed = sum(1 for d in data if d.get('status') == 'failed')
print(f'Tool executions: {total} total, {failed} failed ({100*failed/max(total,1):.1f}%)')
if failed > 0:
    print('Failed tools:')
    for d in data:
        if d.get('status') == 'failed':
            print(f'  - {d.get(\"tool_name\")} at {d.get(\"timestamp\")}: {d.get(\"error\", \"unknown\")}')
"
```

### 6.2 tool_effects Inspection

Each tool execution records its effects. Inspect them for correctness:

```bash
# Get tool effects for a specific run
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/workflows/<workflow_id>/runs/<run_id>" \
  | python -c "
import sys, json
data = json.load(sys.stdin)
for step in data.get('steps', []):
    if 'tool_effects' in step:
        print(f'Step: {step[\"name\"]}')
        for effect in step['tool_effects']:
            print(f'  Tool: {effect[\"tool\"]}')
            print(f'  Status: {effect[\"status\"]}')
            print(f'  Effects: {json.dumps(effect.get(\"effects\", {}), indent=4)}')
            print()
"
```

### 6.3 Adapter-Specific Checks

| Adapter | Health Indicator | Check |
|---------|-----------------|-------|
| CRM | Record creation success | Verify CRM entries are being created |
| Billing | Payment processing | Check billing step approvals complete |
| Email | Delivery status | Confirm email sends are recorded |
| Audit | Log writes | Verify audit entries are persisting |
| Contract Parser | Parse success rate | Check for parsing failures |
| Policy Retriever | Retrieval accuracy | Verify correct policies are returned |

---

## 7. Production Monitoring Setup

### 7.1 Monitoring Architecture

For production deployments, implement a layered monitoring approach:

```
Layer 1: Infrastructure (Postgres, containers, network)
Layer 2: Application (health endpoint, API latency)
Layer 3: Business (workflow success, tool execution, evolution)
Layer 4: Intelligence (audit patterns, anomaly detection)
```

### 7.2 Key Metrics to Track

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| Health endpoint response time | HTTP probe | > 2 seconds |
| Database connection count | pg_stat_activity | > 80% of max |
| Failed tool executions | Audit logs | > 5% failure rate |
| Workflow completion rate | Runtime state | < 95% completion |
| Auth failure rate | Audit logs | > 10 failures/hour |
| Evolution sandbox size | File system | > 20 pending variants |
| Lesson generation rate | Improvement API | 0 new lessons in 7 days |
| API error rate | Backend logs | > 1% of requests |

### 7.3 Alert Configuration Template

```yaml
# Example monitoring configuration
alerts:
  - name: health-endpoint-down
    check: GET /api/v1/health/ready
    interval: 30s
    alert_after: 3 consecutive failures
    notify: ops-team
    
  - name: database-disconnected
    check: health response missing "database": "postgres"
    interval: 30s
    alert_after: 1 failure
    notify: ops-team, dba-team
    severity: critical
    
  - name: high-tool-failure-rate
    check: tool.executed failure rate > 5% over 15min
    interval: 5m
    alert_after: 2 consecutive checks
    notify: ops-team
    
  - name: auth-brute-force
    check: auth.login failures > 10 in 5min
    interval: 1m
    alert_after: 1 occurrence
    notify: security-team
    severity: high
    
  - name: stale-evolution-sandbox
    check: sandbox variants unchanged for 14 days
    interval: 24h
    alert_after: 1 check
    notify: dev-team
    severity: low
```

### 7.4 Dashboard Panels

Design your monitoring dashboard with these panels:

1. **System Overview:** Health endpoint status, uptime percentage, last restart
2. **Database Health:** Connection count, query latency, storage used
3. **API Performance:** Request rate, error rate, p95 latency
4. **Workflow Status:** Active runs, completed today, failed today
5. **Tool Adapters:** Per-adapter success rate, average latency
6. **Evolution Status:** Sandbox count, last promotion, lesson count
7. **Security:** Auth failures, unusual access patterns, scope violations

---

## 8. Real-World Use Case Examples

### Use Case 1: Detecting Silent Failures

**Scenario:** Workflows appear to complete but customers report missing emails.

**Investigation:**

```bash
# 1. Check email tool adapter success rate
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/audit?event_type=tool.executed&tool_name=email" \
  | python -c "
import sys, json
data = json.load(sys.stdin)
for d in data[-10:]:
    status = d.get('status', 'unknown')
    effects = d.get('tool_effects', {})
    print(f'{d[\"timestamp\"]}: {status} - effects: {json.dumps(effects)}')
"
```

**Discovery:** The email adapter is returning "success" but `tool_effects` shows `delivery_status: "queued"` rather than `"sent"`. The external email service queue is backing up.

**Resolution:** Address the email service queue, then verify effects show `"sent"` status.

### Use Case 2: Performance Degradation Detection

**Scenario:** Users report the ops console is slow.

**Investigation:**

```bash
# 1. Check health endpoint latency
time curl -s http://127.0.0.1:8000/api/v1/health/ready > /dev/null

# 2. Check database connection count
psql "$DATABASE_URL" -c "SELECT count(*) FROM pg_stat_activity;"

# 3. Check for long-running queries
psql "$DATABASE_URL" -c "
  SELECT pid, now() - query_start as duration, query 
  FROM pg_stat_activity 
  WHERE state = 'active' AND query_start < now() - interval '5 seconds'
  ORDER BY duration DESC;
"
```

**Discovery:** A process intelligence analysis query is running for 45 seconds, blocking other connections.

**Resolution:** Optimize the query or schedule heavy analysis during off-peak hours.

### Use Case 3: Evolution Pipeline Stall

**Scenario:** No new variants have been promoted in 30 days despite active system use.

**Investigation:**

```bash
# 1. Check evolution archive
curl -s -b cookies.txt "http://127.0.0.1:8000/api/v1/evolution/archive" \
  | python -c "
import sys, json
data = json.load(sys.stdin)
print(f'Total variants: {len(data)}')
for v in data:
    print(f'  {v[\"name\"]}: {v[\"status\"]} (last updated: {v.get(\"updated_at\", \"unknown\")})')
"

# 2. Check for pending evaluations
npm run business:evolution:check

# 3. Check lesson generation
curl -s -b cookies.txt "http://127.0.0.1:8000/api/v1/improvement/lessons" \
  | python -c "import sys,json; d=json.load(sys.stdin); print(f'Lessons: {len(d)}')"
```

**Discovery:** Reflections are being generated but `auto-propose` is not being called. Proposed variants exist but no one has initiated evaluation.

**Resolution:** Set up a scheduled job to run evaluations weekly, or enable `GENERIC_SWARM_AUTO_REFLECT` with a proposal review workflow.

---

## 9. Best Practices

### Monitoring Principles

1. **Monitor from the outside in.** Start with the health endpoint, then drill into components.

2. **Set meaningful thresholds.** Base alerts on actual usage patterns, not arbitrary numbers.

3. **Correlate across layers.** A tool failure often correlates with a database issue or network problem.

4. **Retain historical data.** Keep at least 30 days of monitoring data for trend analysis.

5. **Test your monitoring.** Periodically simulate failures to verify alerts fire correctly.

### Operational Hygiene

- Review audit logs weekly for unexpected patterns
- Check evolution sandbox monthly for stale variants
- Verify backup integrity quarterly (JSON backup vs. Postgres primary)
- Update monitoring thresholds after system changes
- Document all monitoring runbooks and escalation procedures

### Environment Variables for Monitoring

| Variable | Purpose | Default |
|----------|---------|---------|
| `GENERIC_SWARM_AUTO_REFLECT` | Auto-reflect on terminal runs | `true` |
| `GENERIC_SWARM_LLM_CRITIC_ENABLED` | Enable LLM-based quality critic | `false` |
| `GENERIC_SWARM_EMBEDDINGS_ENABLED` | Enable embedding-based retrieval | `false` |
| `GENERIC_SWARM_PGVECTOR_ENABLED` | Enable pgvector similarity search | `false` |
| `NEO4J_URI` | Graph federation endpoint | unset |

> **Note:** Enable these features progressively. Each adds monitoring surface area. Start with base monitoring, then add feature-specific checks as you enable capabilities.

---

## 10. Chapter Summary

This chapter covered comprehensive system health monitoring for Generic Swarm Ops:

- **Health Endpoint:** The primary `GET /api/v1/health/ready` endpoint and its interpretation
- **Database Monitoring:** PostgreSQL connectivity, runtime state, and connection pool health
- **Audit Logs:** Querying, filtering, and anomaly detection on operational events
- **Process Intelligence:** Artifact freshness and pipeline integrity
- **Evolution Sandbox:** Variant status, pipeline health, and lesson library growth
- **Tool Adapters:** Fail-closed behavior monitoring and tool_effects inspection
- **Production Setup:** Metrics, alerts, dashboards, and monitoring architecture

The key principle is layered monitoring: verify infrastructure first, then application health, then business metrics, and finally intelligence-level patterns.

---

## 11. Knowledge Check Quiz

Test your understanding of system health monitoring:

**Question 1:** What response from the health endpoint confirms the database is properly connected?

<details>
<summary>Answer</summary>

The response must include `"database": "postgres"`. This confirms the backend has an active connection to the PostgreSQL primary store. If this field is missing or shows a different value, database connectivity has been lost.

</details>

**Question 2:** How do you check for failed tool adapter executions via the audit API?

<details>
<summary>Answer</summary>

Query `GET /api/v1/audit?event_type=tool.executed` and filter for entries where `status` is `"failed"`. The response includes `tool_name`, `timestamp`, and `error` fields that identify what failed and why.

</details>

**Question 3:** What is the difference between the Postgres primary store and the JSON backup?

<details>
<summary>Answer</summary>

PostgreSQL with JSONB columns is the primary runtime store. JSON files serve as backup only. If data appears missing after a restart, verify you are connecting to the same PostgreSQL instance. Never rely on JSON files as the source of truth during normal operation.

</details>

**Question 4:** What audit event types should you monitor for security purposes?

<details>
<summary>Answer</summary>

Monitor `auth.login` (for brute force attempts), `memory.write` (for scope violations), and `tool.executed` (for unauthorized tool usage). Set alerts for unusual patterns: high failure rates, unexpected tools being called, or writes to restricted memory scopes.

</details>

**Question 5:** Why should you monitor the evolution sandbox size?

<details>
<summary>Answer</summary>

A growing sandbox with no promotions indicates a stalled evolution pipeline. Variants are being proposed but not evaluated, tested as canaries, or promoted. This means the self-improvement system is not delivering value. Monitor for stale variants (unchanged for 14+ days) and ensure the evaluation pipeline is running regularly.

</details>

**Question 6:** What does fail-closed behavior mean for tool adapters, and how do you verify it is working?

<details>
<summary>Answer</summary>

Fail-closed means tool adapters reject execution when required inputs are missing or invalid, rather than proceeding with partial data. Verify by checking `tool_effects` in the audit log - failed executions should show a clear rejection reason. This protects system integrity by preventing agents from taking actions based on incomplete information.

</details>

**Question 7:** What four layers should a production monitoring dashboard cover?

<details>
<summary>Answer</summary>

1. Infrastructure (Postgres, containers, network connectivity)
2. Application (health endpoint, API latency, error rates)
3. Business (workflow completion, tool execution success, evolution progress)
4. Intelligence (audit patterns, anomaly detection, trend analysis)

</details>

---

## 12. Advanced Monitoring Patterns

### 12.1 Correlation Analysis

When investigating issues, correlate events across multiple monitoring sources:

```bash
#!/bin/bash
# correlate-events.sh - Find related events within a time window
TIMESTAMP="2024-01-15T10:30:00Z"
WINDOW="5m"

echo "=== Events near $TIMESTAMP (window: $WINDOW) ==="

# Audit events
echo ""
echo "--- Audit Events ---"
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/audit?since=$TIMESTAMP&window=$WINDOW" \
  | python -c "
import sys, json
data = json.load(sys.stdin)
for event in data:
    print(f'  {event[\"timestamp\"]} [{event[\"event_type\"]}] {event.get(\"detail\", \"\")}')
"

# Database activity
echo ""
echo "--- Database Activity ---"
psql "$DATABASE_URL" -c "
  SELECT query_start, state, left(query, 80) as query_preview
  FROM pg_stat_activity
  WHERE datname = current_database()
  ORDER BY query_start DESC
  LIMIT 10;
"
```

### 12.2 Trend Detection

Track metrics over time to detect degradation before it becomes critical:

```bash
#!/bin/bash
# trend-check.sh - Compare current metrics to historical baseline

API="http://127.0.0.1:8000/api/v1"
COOKIE="cookies.txt"

# Workflow completion rate (last 24h vs previous 24h)
echo "=== Workflow Completion Trend ==="
curl -s -b "$COOKIE" "$API/audit?event_type=workflow.transition&since=24h" \
  | python -c "
import sys, json
data = json.load(sys.stdin)
completed = sum(1 for d in data if d.get('to_state') == 'completed')
failed = sum(1 for d in data if d.get('to_state') == 'failed')
total = completed + failed
if total > 0:
    rate = completed / total * 100
    print(f'  Completion rate: {rate:.1f}% ({completed}/{total})')
    if rate < 95:
        print('  WARNING: Below 95% threshold')
else:
    print('  No workflow transitions in period')
"

# Tool adapter reliability
echo ""
echo "=== Tool Adapter Reliability ==="
curl -s -b "$COOKIE" "$API/audit?event_type=tool.executed&since=24h" \
  | python -c "
import sys, json
from collections import Counter
data = json.load(sys.stdin)
by_tool = {}
for d in data:
    tool = d.get('tool_name', 'unknown')
    if tool not in by_tool:
        by_tool[tool] = {'total': 0, 'failed': 0}
    by_tool[tool]['total'] += 1
    if d.get('status') == 'failed':
        by_tool[tool]['failed'] += 1

for tool, stats in sorted(by_tool.items()):
    rate = (1 - stats['failed'] / max(stats['total'], 1)) * 100
    status = 'OK' if rate >= 95 else 'WARN'
    print(f'  [{status}] {tool}: {rate:.1f}% success ({stats[\"total\"]} calls)')
"
```

### 12.3 Capacity Planning Metrics

Monitor resource usage trends for capacity planning:

```bash
# Database growth rate
psql "$DATABASE_URL" -c "
  SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) as total_size,
    n_live_tup as row_count
  FROM pg_stat_user_tables
  ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC
  LIMIT 10;
"

# Audit log growth (entries per day)
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/audit?since=7d" \
  | python -c "
import sys, json
from collections import Counter
data = json.load(sys.stdin)
by_day = Counter(d.get('timestamp', '')[:10] for d in data)
print('Audit entries per day (last 7 days):')
for day, count in sorted(by_day.items()):
    print(f'  {day}: {count}')
print(f'  Average: {sum(by_day.values()) / max(len(by_day), 1):.0f}/day')
"
```

> **Tip:** If the database is growing faster than expected, check for excessive audit logging or memory writes. Consider implementing log rotation for older audit entries that have been analyzed.
