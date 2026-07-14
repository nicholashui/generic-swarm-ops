# Chapter 5.1: Performance Tuning Strategies

![Performance Architecture](../assets/05-01-performance-architecture.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Identify performance-critical paths in the Generic Swarm architecture
2. Optimize PostgreSQL for JSONB workloads with GIN indexing and connection pooling
3. Tune the FastAPI backend for production concurrency using uvicorn workers
4. Configure knowledge retrieval tier escalation thresholds for cost efficiency
5. Implement frontend caching strategies with Next.js ISR and API response caching
6. Apply batch processing techniques for process intelligence workloads
7. Establish benchmarking procedures to measure and track performance improvements

## Prerequisites

Before working through this chapter, ensure you have:

- Completed Section 1 (Core System Fundamentals) for architecture understanding
- A running Generic Swarm Ops instance with PostgreSQL connected
- Access to `backend/.env` for configuration changes
- Familiarity with SQL query plans and EXPLAIN ANALYZE
- Basic understanding of async Python (asyncio, uvicorn)
- Reviewed Chapter 2.4 (Knowledge & Memory Management) for retrieval tier context

---

## 1. Understanding the Performance-Critical Path

Every request in Generic Swarm Ops flows through a deterministic path with measurable latency at each stage. Understanding this path is essential for targeted optimization.

### 1.1 Request Lifecycle

The full request lifecycle from client to response involves these stages:

```text
Client Request
  -> Load Balancer / Reverse Proxy (if deployed)
  -> FastAPI (uvicorn worker)
    -> Authentication + Rate Limiting
    -> Intake + Risk Router (classification)
    -> Business Orchestrator (state-graph dispatch)
      -> Knowledge Retrieval (Tier 0/1/2)
      -> Tool Adapter Execution
      -> PostgreSQL (runtime_state read/write)
    -> Response Assembly
  -> Client Response
```

Each stage contributes latency. The most impactful optimization targets are:

| Stage | Typical Latency | Optimization Impact |
|-------|----------------|---------------------|
| Auth + Rate Limiting | 2-5ms | Low (already fast) |
| Risk Classification | 10-30ms | Medium |
| Knowledge Retrieval (Tier 0) | 20-50ms | High |
| Knowledge Retrieval (Tier 1) | 100-500ms | High |
| PostgreSQL JSONB Query | 5-200ms | Very High |
| Tool Adapter Call | 50-2000ms | Medium (external dependency) |
| Response Assembly | 2-10ms | Low |

### 1.2 Identifying Bottlenecks

Use the built-in request tracing to identify which stage dominates latency:

```bash
# Enable detailed timing in backend logs
export GENERIC_SWARM_LOG_LEVEL=DEBUG
export GENERIC_SWARM_TRACE_TIMING=true

# Restart backend with profiling
cd backend
uvicorn app.main:app --reload --log-level debug
```

Check request timing in structured logs:

```json
{
  "request_id": "req_abc123",
  "total_ms": 342,
  "stages": {
    "auth": 3,
    "classification": 18,
    "orchestration": 45,
    "retrieval": 180,
    "db_queries": 62,
    "tool_calls": 28,
    "response": 6
  }
}
```

> **Tip:** In most deployments, knowledge retrieval and database queries together account for 60-80% of total request latency. Focus optimization efforts there first.

---

## 2. PostgreSQL Optimization

PostgreSQL is the primary runtime store for Generic Swarm Ops. The `runtime_state` table uses JSONB columns extensively, which requires specific indexing strategies.

### 2.1 JSONB Indexing with GIN

The default `runtime_state` table stores workflow state, agent configurations, and memory entries as JSONB. Without proper indexing, containment queries scan the entire table.

**Step 1:** Identify slow queries using pg_stat_statements:

```sql
-- Enable pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find the slowest queries
SELECT
  query,
  calls,
  mean_exec_time AS avg_ms,
  total_exec_time AS total_ms
FROM pg_stat_statements
WHERE mean_exec_time > 50
ORDER BY mean_exec_time DESC
LIMIT 20;
```

**Step 2:** Create GIN indexes on frequently queried JSONB paths:

```sql
-- Index for workflow state lookups by status
CREATE INDEX idx_runtime_state_status
  ON runtime_state USING GIN ((data -> 'status'));

-- Index for agent lookups by domain
CREATE INDEX idx_runtime_state_domain
  ON runtime_state USING GIN ((data -> 'domain'));

-- Index for memory entries by type and scope
CREATE INDEX idx_runtime_state_memory_type
  ON runtime_state USING GIN ((data -> 'memory_type'));

-- Composite GIN index for common filter patterns
CREATE INDEX idx_runtime_state_workflow_active
  ON runtime_state USING GIN (data jsonb_path_ops);
```

**Step 3:** Verify index usage with EXPLAIN ANALYZE:

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT id, data
FROM runtime_state
WHERE data @> '{"status": "active", "domain": "operations"}';
```

Expected output should show `Bitmap Index Scan on idx_runtime_state_workflow_active` rather than `Seq Scan`.

> **Warning:** GIN indexes increase write latency and storage. Only index paths that are actually queried in production. Monitor `pg_stat_user_indexes` to identify unused indexes.

### 2.2 Connection Pooling

Each uvicorn worker maintains its own database connections. Without pooling, connection overhead becomes significant under load.

**Step 1:** Configure connection pooling in `backend/.env`:

```bash
# Connection pool settings
DATABASE_URL=postgresql://user:pass@localhost:5432/generic_swarm_ops
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_POOL_TIMEOUT=30
DATABASE_POOL_RECYCLE=3600
```

**Step 2:** For production deployments, use PgBouncer as an external pooler:

```ini
# pgbouncer.ini
[databases]
generic_swarm_ops = host=localhost port=5432 dbname=generic_swarm_ops

[pgbouncer]
listen_port = 6432
listen_addr = 127.0.0.1
auth_type = md5
pool_mode = transaction
default_pool_size = 20
max_client_conn = 200
reserve_pool_size = 5
reserve_pool_timeout = 3
```

**Step 3:** Update the backend to connect through PgBouncer:

```bash
DATABASE_URL=postgresql://user:pass@localhost:6432/generic_swarm_ops
```

### 2.3 Query Optimization Patterns

Common query patterns in Generic Swarm Ops and their optimizations:

**Pattern 1: Workflow state lookup (frequent)**

```sql
-- Before: Full JSONB scan
SELECT * FROM runtime_state
WHERE data->>'type' = 'workflow_run'
  AND data->>'status' = 'active';

-- After: Use containment operator with GIN index
SELECT * FROM runtime_state
WHERE data @> '{"type": "workflow_run", "status": "active"}';
```

**Pattern 2: Memory retrieval with pagination**

```sql
-- Before: Offset-based pagination (slow for large offsets)
SELECT * FROM runtime_state
WHERE data @> '{"type": "memory"}'
ORDER BY created_at DESC
OFFSET 1000 LIMIT 50;

-- After: Cursor-based pagination (consistent performance)
SELECT * FROM runtime_state
WHERE data @> '{"type": "memory"}'
  AND created_at < $1  -- cursor from last page
ORDER BY created_at DESC
LIMIT 50;
```

**Pattern 3: Aggregation for metrics**

```sql
-- Create a materialized view for frequently-accessed metrics
CREATE MATERIALIZED VIEW workflow_metrics AS
SELECT
  data->>'domain' AS domain,
  data->>'status' AS status,
  COUNT(*) AS count,
  AVG((data->>'cycle_time_ms')::numeric) AS avg_cycle_time
FROM runtime_state
WHERE data @> '{"type": "workflow_run"}'
GROUP BY data->>'domain', data->>'status';

-- Refresh on schedule (not per-request)
REFRESH MATERIALIZED VIEW CONCURRENTLY workflow_metrics;
```

### 2.4 Vacuum and Maintenance

JSONB updates create dead tuples faster than simple column updates. Configure autovacuum aggressively:

```sql
-- Per-table autovacuum settings for high-churn tables
ALTER TABLE runtime_state SET (
  autovacuum_vacuum_scale_factor = 0.05,
  autovacuum_analyze_scale_factor = 0.02,
  autovacuum_vacuum_cost_delay = 10
);
```

Monitor table bloat:

```sql
SELECT
  schemaname || '.' || tablename AS table,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
  n_dead_tup,
  n_live_tup,
  ROUND(n_dead_tup::numeric / GREATEST(n_live_tup, 1) * 100, 1) AS dead_pct
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;
```

---

## 3. Backend Tuning (FastAPI + Uvicorn)

### 3.1 Worker Configuration

The number of uvicorn workers determines how many requests can be processed concurrently. The optimal count depends on whether your workload is I/O-bound (typical) or CPU-bound.

**Step 1:** Calculate optimal worker count:

```bash
# For I/O-bound workloads (most Generic Swarm operations):
# workers = 2 * CPU_cores + 1

# For a 4-core machine:
uvicorn app.main:app --workers 9 --host 0.0.0.0 --port 8000

# For CPU-bound workloads (heavy computation):
# workers = CPU_cores + 1
uvicorn app.main:app --workers 5 --host 0.0.0.0 --port 8000
```

**Step 2:** Configure in a production process manager (systemd example):

```ini
[Unit]
Description=Generic Swarm Ops Backend
After=network.target postgresql.service

[Service]
Type=notify
User=swarm
WorkingDirectory=/opt/generic-swarm-ops/backend
Environment="DATABASE_URL=postgresql://swarm:secret@localhost:5432/generic_swarm_ops"
Environment="PYTHONPATH=."
ExecStart=/opt/generic-swarm-ops/backend/.venv/bin/uvicorn \
  app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 9 \
  --timeout-keep-alive 65 \
  --limit-concurrency 100
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 3.2 Async Patterns

Generic Swarm Ops uses async Python throughout. Ensure all I/O operations are truly async:

```python
# GOOD: Async database call
async def get_workflow_state(workflow_id: str):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT data FROM runtime_state WHERE id = $1",
            workflow_id
        )
        return row["data"] if row else None

# BAD: Blocking call in async context (blocks the entire event loop)
def get_workflow_state_sync(workflow_id: str):
    # This blocks the worker!
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT data FROM runtime_state WHERE id = %s", (workflow_id,))
    return cur.fetchone()
```

> **Warning:** A single blocking call in an async handler can stall all concurrent requests on that worker. Use `asyncio.to_thread()` as a last resort for unavoidable sync code.

### 3.3 Rate Limiting Configuration

Rate limiting protects against unbounded consumption (OWASP LLM10). Configure per-route limits:

```python
# backend/app/infrastructure/rate_limiting.py
RATE_LIMITS = {
    # High-frequency, low-cost endpoints
    "/api/v1/health/ready": "100/minute",
    "/api/v1/workflows": "60/minute",

    # Medium-cost endpoints
    "/api/v1/knowledge/search": "30/minute",
    "/api/v1/evolution/archive": "20/minute",

    # High-cost endpoints (trigger LLM calls)
    "/api/v1/improvement/reflect": "5/minute",
    "/api/v1/improvement/auto-propose": "3/minute",
    "/api/v1/loops/run": "2/minute",

    # Admin endpoints
    "/api/v1/evolution/variants/*/promote": "1/minute",
}
```

### 3.4 Request Timeout Budgets

Set timeout budgets that cascade through the request lifecycle:

```python
# Total request timeout
REQUEST_TIMEOUT_SECONDS = 120

# Internal budget allocation
TIMEOUT_BUDGETS = {
    "classification": 5,       # Risk router has 5s
    "retrieval_tier_0": 10,    # Vector search has 10s
    "retrieval_tier_1": 30,    # Graph query has 30s
    "retrieval_tier_2": 60,    # RAPTOR summary has 60s
    "tool_adapter": 30,        # Each tool call has 30s
    "llm_call": 45,            # LLM generation has 45s
    "db_query": 10,            # Database query has 10s
}
```

---

## 4. Knowledge Retrieval Tuning

The tiered retrieval system is designed for cost efficiency. Tuning the escalation thresholds determines how much traffic stays on the cheaper tiers.

### 4.1 Tier Escalation Thresholds

The retrieval system starts at Tier 0 (vector search) and only escalates when the query cannot be adequately answered at the current tier:

```python
# Retrieval configuration
RETRIEVAL_CONFIG = {
    "tier_0": {
        "type": "vector_search",
        "embedding_dimensions": 384,  # MiniLM default
        "top_k": 10,
        "similarity_threshold": 0.72,
        "escalation_trigger": "similarity_below_threshold"
    },
    "tier_1": {
        "type": "lightrag_graph",
        "mode": "dual_level",  # low-level + high-level
        "max_hops": 3,
        "escalation_trigger": "relational_query_detected"
    },
    "tier_2": {
        "type": "raptor_summary",
        "build_on_demand": True,
        "cluster_threshold": 0.85,
        "escalation_trigger": "corpus_wide_synthesis_needed"
    }
}
```

**Step 1:** Analyze current tier distribution:

```sql
-- Check what percentage of queries use each tier
SELECT
  data->>'retrieval_tier' AS tier,
  COUNT(*) AS query_count,
  ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER() * 100, 1) AS pct
FROM runtime_state
WHERE data @> '{"type": "retrieval_log"}'
  AND created_at > NOW() - INTERVAL '7 days'
GROUP BY data->>'retrieval_tier';
```

Target distribution: 80%+ at Tier 0, 15% at Tier 1, less than 5% at Tier 2.

**Step 2:** Adjust the similarity threshold:

```bash
# Higher threshold = more escalations (better quality, higher cost)
# Lower threshold = fewer escalations (lower cost, may miss relevant results)
# Default: 0.72. Production range: 0.65-0.80
export GENERIC_SWARM_RETRIEVAL_SIMILARITY_THRESHOLD=0.72
```

**Step 3:** Enable optional pgvector for production-grade vector search:

```bash
# Enable pgvector embeddings
export GENERIC_SWARM_EMBEDDINGS_ENABLED=true
export GENERIC_SWARM_PGVECTOR_ENABLED=true
```

```sql
-- Create pgvector extension and index
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE embeddings (
  id TEXT PRIMARY KEY,
  document_id TEXT NOT NULL,
  chunk_text TEXT NOT NULL,
  embedding vector(384),
  metadata JSONB DEFAULT '{}'
);

-- IVFFlat index for approximate nearest neighbor
CREATE INDEX idx_embeddings_vector
  ON embeddings USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);  -- sqrt(row_count) is a good starting point
```

### 4.2 Embedding Dimensions and Model Selection

The embedding model determines both quality and performance:

| Model | Dimensions | Speed | Quality | Use Case |
|-------|-----------|-------|---------|----------|
| all-MiniLM-L6-v2 | 384 | Fast | Good | Default, cost-sensitive |
| all-mpnet-base-v2 | 768 | Medium | Better | Production with budget |
| text-embedding-3-small | 1536 | API call | Best | High-accuracy requirement |

> **Note:** Higher dimensions mean larger index sizes and slower similarity searches. For most business workloads, 384 dimensions provides an excellent quality-to-cost ratio.

### 4.3 Graph Query Optimization (Tier 1)

When queries escalate to the LightRAG graph layer, optimize entity resolution:

```python
# Graph query configuration
GRAPH_CONFIG = {
    "max_entities_per_query": 20,
    "max_hops": 3,
    "neighborhood_limit": 50,
    "entity_resolution_cache_ttl": 300,  # 5 minutes
    "batch_entity_extraction": True
}
```

Monitor graph query performance:

```bash
# Check average graph query latency
curl -s http://localhost:8000/api/v1/knowledge/graph/query?seed=test \
  -H "Authorization: Bearer $TOKEN" \
  -w "\n%{time_total}s\n"
```

---

## 5. Frontend Optimization

### 5.1 Next.js Build Optimization

The ops console frontend uses Next.js. Optimize the production build:

```bash
cd frontend

# Analyze bundle size
pnpm build
pnpm analyze  # if configured

# Key environment variables for production
export NEXT_PUBLIC_DEMO_MODE=false
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

**Step 1:** Enable Incremental Static Regeneration (ISR) for semi-static pages:

```typescript
// pages/evolution/archive.tsx
export async function getStaticProps() {
  const archive = await fetch(`${API_BASE}/evolution/archive`);
  return {
    props: { archive: await archive.json() },
    revalidate: 60,  // Regenerate every 60 seconds
  };
}
```

**Step 2:** Configure API response caching:

```typescript
// lib/api-client.ts
import useSWR from 'swr';

export function useWorkflowRuns() {
  return useSWR('/api/v1/workflows/runs', fetcher, {
    refreshInterval: 5000,     // Poll every 5s for active monitoring
    dedupingInterval: 2000,    // Deduplicate requests within 2s
    revalidateOnFocus: false,  // Don't refetch on tab focus
  });
}
```

### 5.2 API Caching Strategy

Implement a caching layer between frontend and backend:

```typescript
// middleware.ts - Edge caching for read-heavy endpoints
const CACHE_RULES = {
  '/api/v1/health/ready': { maxAge: 5, staleWhileRevalidate: 10 },
  '/api/v1/evolution/archive': { maxAge: 30, staleWhileRevalidate: 60 },
  '/api/v1/knowledge/graph/query': { maxAge: 300, staleWhileRevalidate: 600 },
  '/api/v1/improvement/lessons': { maxAge: 60, staleWhileRevalidate: 120 },
};
```

---

## 6. Process Intelligence Batch Processing

Process mining operations (event log analysis, conformance checking, bottleneck detection) are computationally expensive. Run them as background batch jobs rather than in the request path.

### 6.1 Batch Job Configuration

```python
# Process intelligence batch settings
PI_BATCH_CONFIG = {
    "discovery": {
        "schedule": "0 2 * * *",         # Daily at 2 AM
        "max_events_per_batch": 10000,
        "timeout_minutes": 30
    },
    "conformance": {
        "schedule": "0 */6 * * *",       # Every 6 hours
        "max_cases_per_batch": 500,
        "timeout_minutes": 15
    },
    "bottleneck_analysis": {
        "schedule": "0 3 * * 1",         # Weekly on Monday at 3 AM
        "lookback_days": 30,
        "timeout_minutes": 45
    }
}
```

### 6.2 Event Log Partitioning

For large event log volumes, partition the storage by time:

```sql
-- Partition event logs by month
CREATE TABLE event_logs (
  id TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  data JSONB NOT NULL
) PARTITION BY RANGE (timestamp);

-- Create monthly partitions
CREATE TABLE event_logs_2026_07
  PARTITION OF event_logs
  FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

CREATE TABLE event_logs_2026_08
  PARTITION OF event_logs
  FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');

-- Index each partition separately
CREATE INDEX idx_event_logs_2026_07_process
  ON event_logs_2026_07 USING GIN ((data -> 'process_id'));
```

---

## 7. Benchmarking and Measurement

### 7.1 Establishing Baselines

Before making any optimization, establish a measurable baseline:

```bash
# Run the built-in benchmark suite
cd backend
python -m pytest tests/ -k "benchmark" --benchmark-only --benchmark-json=baseline.json

# Or use the evaluation harness for end-to-end benchmarks
npm run business:eval -- --benchmark --output results/baseline.json
```

### 7.2 Key Performance Metrics

Track these metrics continuously:

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| P50 request latency | < 200ms | > 500ms |
| P95 request latency | < 1000ms | > 3000ms |
| P99 request latency | < 3000ms | > 10000ms |
| Database query P95 | < 50ms | > 200ms |
| Retrieval Tier 0 P95 | < 100ms | > 300ms |
| Cost per case (USD) | < $0.42 | > $1.00 |
| Worker utilization | 60-80% | > 95% |
| Connection pool usage | < 70% | > 90% |

### 7.3 Load Testing

Use the evaluation corpus as a load test baseline:

```bash
# Run concurrent workflow executions
python scripts/load_test.py \
  --concurrency 20 \
  --duration 300 \
  --target http://localhost:8000/api/v1 \
  --scenario golden_tasks
```

---

## 8. Real-World Use Cases

### Use Case 1: E-commerce Order Processing at Scale

A mid-size e-commerce company processes 5,000 orders per day through Generic Swarm Ops. Key optimizations:

- **Database:** GIN indexes on order status and customer_id JSONB paths reduced query latency from 180ms to 8ms
- **Retrieval:** Similarity threshold set to 0.68 (lower than default) kept 92% of queries at Tier 0
- **Workers:** 17 uvicorn workers on an 8-core machine achieved 200 req/s throughput
- **Result:** Average order processing time dropped from 4.2s to 1.1s

### Use Case 2: Legal Document Review Pipeline

A legal firm uses Generic Swarm Ops for contract review. The knowledge base contains 50,000 contracts and regulatory documents:

- **Database:** Materialized views for common clause patterns reduced report generation from 45s to 3s
- **Retrieval:** pgvector with 768-dimension embeddings improved clause matching accuracy by 18%
- **Batch processing:** Nightly conformance checks across all active contracts complete in 25 minutes
- **Result:** Cost per contract review dropped from $2.80 to $0.65

### Use Case 3: Multi-Domain Support Operations

An enterprise deploys three domain packs (video, research, education) on a single instance:

- **Database:** Separate connection pools per domain prevented one domain's load spike from affecting others
- **Retrieval:** Domain-scoped vector indexes eliminated cross-domain result contamination
- **Workers:** Dedicated worker allocation (video=12, research=5, education=4) matched load profiles
- **Result:** All domains maintained sub-500ms P95 latency even during peak hours

---

## 9. Best Practices

### Performance Optimization Principles

1. **Measure before optimizing.** Always establish a baseline with real production data before making changes.

2. **Optimize the critical path first.** Focus on the stages that contribute the most latency (typically retrieval and database).

3. **Keep 80%+ of retrieval at Tier 0.** The tiered system is designed so that most queries never need expensive graph or summary operations.

4. **Use async throughout.** A single blocking call in the request path can negate all other optimizations.

5. **Index selectively.** Every GIN index speeds reads but slows writes. Only index JSONB paths that appear in WHERE clauses.

6. **Partition by time.** Event logs and memory entries grow without bound. Partitioning enables efficient pruning and targeted queries.

7. **Set timeout budgets.** Every external call (LLM, tool adapter, database) should have a timeout. Unbounded waits cascade into system-wide stalls.

8. **Cache read-heavy, write-rarely data.** Evolution archive, lesson library, and knowledge graph results are excellent cache candidates.

9. **Batch process intelligence.** PI operations (mining, conformance, bottleneck analysis) should never run in the request path.

10. **Monitor continuously.** Performance degrades gradually. Track metrics weekly and alert on threshold crossings.

### Common Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Indexing every JSONB path | Write amplification, bloated storage | Index only queried paths |
| Offset pagination | O(N) scan for deep pages | Use cursor-based pagination |
| Sync DB driver in async code | Event loop blocking | Use asyncpg or async SQLAlchemy |
| No connection pooling | Connection overhead per request | PgBouncer or built-in pool |
| Unbounded LLM calls | Timeout cascades | Budget caps + fallback logic |

---

## 10. Chapter Summary

This chapter covered the complete performance tuning methodology for Generic Swarm Ops:

- **Request lifecycle analysis** to identify the performance-critical path
- **PostgreSQL optimization** including GIN indexing, connection pooling, query patterns, and maintenance
- **Backend tuning** with worker configuration, async patterns, rate limiting, and timeout budgets
- **Knowledge retrieval tuning** through tier escalation thresholds, embedding selection, and graph optimization
- **Frontend optimization** with Next.js ISR, SWR caching, and API response caching
- **Process intelligence batch processing** for compute-heavy operations
- **Benchmarking methodology** to establish baselines and track improvements

The key insight is that Generic Swarm Ops is designed as a tiered system where most work stays cheap. Performance tuning is about keeping traffic on the efficient paths and identifying when expensive operations are truly necessary.

---

## Knowledge Check

1. **What is the recommended formula for calculating uvicorn worker count for I/O-bound workloads?**
   - A) CPU cores - 1
   - B) 2 * CPU cores + 1
   - C) CPU cores * 4
   - D) Fixed at 4 workers

2. **Which PostgreSQL index type is most appropriate for JSONB containment queries?**
   - A) B-tree
   - B) Hash
   - C) GIN
   - D) BRIN

3. **What is the target percentage of retrieval queries that should remain at Tier 0 (vector search)?**
   - A) 50%+
   - B) 60%+
   - C) 80%+
   - D) 95%+

4. **Why is offset-based pagination problematic for large datasets?**
   - A) It requires more memory
   - B) It performs O(N) scans for deep pages
   - C) It cannot be indexed
   - D) It breaks JSONB queries

5. **What is the primary risk of using a synchronous database driver in an async FastAPI handler?**
   - A) It causes memory leaks
   - B) It blocks the event loop, stalling all concurrent requests on that worker
   - C) It prevents connection pooling
   - D) It corrupts JSONB data

6. **Which of the following is NOT a recommended optimization for process intelligence workloads?**
   - A) Running them as background batch jobs
   - B) Partitioning event logs by time
   - C) Running them in the request path for real-time results
   - D) Setting timeout limits on batch operations

7. **What is the recommended connection pool mode when using PgBouncer with Generic Swarm Ops?**
   - A) Session mode
   - B) Transaction mode
   - C) Statement mode
   - D) Direct mode

**Answers:** 1-B, 2-C, 3-C, 4-B, 5-B, 6-C, 7-B
