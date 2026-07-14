# Chapter 5.3: Large-Scale Deployment

![Deployment Architecture](../assets/05-03-deployment-architecture.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Design multi-domain deployment architectures with horizontal scaling
2. Deploy multiple backend instances behind a load balancer with session affinity
3. Configure PostgreSQL replication for read-heavy workloads
4. Implement domain pack isolation at enterprise scale
5. Set up federated knowledge graph export via Neo4j/GraphAnything
6. Integrate Generic Swarm Ops into CI/CD pipelines with inventory gates
7. Containerize the system with Docker for reproducible deployments
8. Manage environment variables securely in production environments

## Prerequisites

Before working through this chapter, ensure you have:

- Completed Chapter 5.1 (Performance Tuning) and 5.2 (Resource Allocation)
- Understanding of domain packs from Chapter 3.3 (Domain Packs)
- Familiarity with Docker and container orchestration concepts
- Access to a multi-node deployment environment (or ability to simulate locally)
- Knowledge of reverse proxies (nginx, Caddy, or HAProxy)
- Read `docs/domain-packs.md` and `docs/installation.md` for reference

---

## 1. Multi-Domain Deployment Architecture

Enterprise deployments typically run multiple domain packs on shared infrastructure. The architecture must provide isolation between domains while sharing common services.

### 1.1 Architecture Overview

The large-scale deployment model consists of:

```text
                    Load Balancer
                         |
            +------------+------------+
            |            |            |
      Backend-1    Backend-2    Backend-N
      (uvicorn)    (uvicorn)    (uvicorn)
            |            |            |
            +------------+------------+
                         |
              +----------+----------+
              |                     |
       PostgreSQL              Knowledge
       (Primary +              Federation
        Replicas)              (Neo4j opt.)
              |                     |
              +----------+----------+
                         |
            +------------+------------+
            |            |            |
       Domain: video  Domain: research  Domain: education
       (114 agents)   (Wave 1)          (Wave 4)
```

### 1.2 Deployment Sizing Guide

| Scale | Users | Domains | Backend Instances | DB Config | Monthly Cost |
|-------|-------|---------|-------------------|-----------|-------------|
| Small | 1-10 | 1 | 1 (4 workers) | Single node | $100-300 |
| Medium | 10-50 | 2-3 | 2-3 (9 workers each) | Primary + 1 replica | $500-1500 |
| Large | 50-200 | 3-5 | 4-8 (9 workers each) | Primary + 2 replicas | $2000-5000 |
| Enterprise | 200+ | 5+ | 8+ (17 workers each) | Cluster + PgBouncer | $5000+ |

---

## 2. Horizontal Scaling

### 2.1 Multiple Backend Instances

Generic Swarm Ops backends are stateless (state lives in PostgreSQL). This means you can run multiple instances behind a load balancer.

**Step 1:** Configure a reverse proxy (nginx example):

```nginx
# /etc/nginx/conf.d/generic-swarm-ops.conf
upstream swarm_backend {
    least_conn;
    server backend-1:8000;
    server backend-2:8000;
    server backend-3:8000;
    
    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name swarm.example.com;

    ssl_certificate /etc/ssl/certs/swarm.crt;
    ssl_certificate_key /etc/ssl/private/swarm.key;

    location /api/ {
        proxy_pass http://swarm_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Request-ID $request_id;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Timeout configuration
        proxy_connect_timeout 5s;
        proxy_read_timeout 120s;
        proxy_send_timeout 30s;
    }

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Step 2:** Health check configuration for the load balancer:

```nginx
upstream swarm_backend {
    least_conn;
    server backend-1:8000 max_fails=3 fail_timeout=30s;
    server backend-2:8000 max_fails=3 fail_timeout=30s;
    server backend-3:8000 max_fails=3 fail_timeout=30s;
}

# Active health checking (nginx plus or alternatives)
# Check /api/v1/health/ready endpoint
```

**Step 3:** Verify all instances are healthy:

```bash
# Check each instance individually
for i in 1 2 3; do
  echo "Backend-$i:"
  curl -s http://backend-$i:8000/api/v1/health/ready | python -m json.tool
  echo
done
```

### 2.2 Stateless Design Requirements

For horizontal scaling to work, ensure:

1. **No in-memory state between requests.** All workflow state is in PostgreSQL.
2. **No file-system state.** Business artifacts are shared via a mounted volume or object storage.
3. **No sticky sessions required.** Any instance can handle any request.
4. **Shared database.** All instances connect to the same PostgreSQL cluster.

```bash
# All instances share the same DATABASE_URL
DATABASE_URL=postgresql://swarm:secret@pgbouncer:6432/generic_swarm_ops

# All instances share the same business artifacts
BUSINESS_ARTIFACTS_PATH=/shared/business/
```

> **Warning:** If you use in-memory caching (e.g., for retrieval results), ensure cache invalidation works across instances. A shared Redis instance or PostgreSQL NOTIFY/LISTEN can coordinate cache invalidation.

---

## 3. Database Replication

### 3.1 PostgreSQL Streaming Replication

For read-heavy workloads, deploy read replicas to offload SELECT queries:

**Step 1:** Configure the primary for replication:

```sql
-- postgresql.conf on primary
wal_level = replica
max_wal_senders = 5
wal_keep_size = 1GB
hot_standby = on
```

**Step 2:** Set up streaming replication on replicas:

```bash
# On replica server
pg_basebackup -h primary-host -D /var/lib/postgresql/data -U replicator -Fp -Xs -P

# recovery.conf (or standby.signal for PG12+)
# primary_conninfo = 'host=primary-host port=5432 user=replicator'
```

**Step 3:** Configure the application for read/write splitting:

```bash
# Primary for writes
DATABASE_URL=postgresql://swarm:secret@primary:5432/generic_swarm_ops

# Replicas for reads (round-robin via PgBouncer)
DATABASE_READ_URL=postgresql://swarm:secret@pgbouncer-read:6432/generic_swarm_ops
```

### 3.2 Read/Write Routing

Configure the backend to route queries appropriately:

```python
# Read-heavy operations use replicas
READ_OPERATIONS = [
    "GET /api/v1/workflows",
    "GET /api/v1/knowledge/search",
    "GET /api/v1/evolution/archive",
    "GET /api/v1/improvement/lessons",
    "GET /api/v1/domains/*/n3-status",
]

# Write operations always use primary
WRITE_OPERATIONS = [
    "POST /api/v1/workflows/*/run",
    "POST /api/v1/evolution/variants",
    "POST /api/v1/improvement/reflect/*",
    "POST /api/v1/loops/run",
    "PATCH /api/v1/agents/*",
]
```

> **Note:** Streaming replication has a small lag (typically milliseconds). Read-after-write operations that require immediate consistency must use the primary.

---

## 4. Domain Pack Isolation at Scale

### 4.1 Isolation Boundaries

Each domain pack operates within strict isolation boundaries:

| Boundary | Mechanism | Enforcement |
|----------|-----------|-------------|
| Tool namespaces | Prefix-based (`video.*` vs `ops.*`) | Tool Permission Broker |
| Memory scopes | Agent-scoped, no cross-pack bleed | Memory Steward + RBAC |
| Knowledge | Domain-filtered retrieval | Query-time domain filter |
| Evaluation | Domain-specific corpus overlays | `domain` field in DNA |
| Governance | Pack-specific risk policies | Governance Officer |

**Step 1:** Register domain packs with proper isolation:

```bash
# Register the video pack (114 agents, N3 enforced)
python scripts/business/register_domain.py \
  --manifest business/video/manifest.json \
  --validate-n3

# Register additional packs
python scripts/business/register_domain.py \
  --manifest business/example_research/manifest.json

python scripts/business/register_domain.py \
  --manifest business/example_education/manifest.json
```

**Step 2:** Verify isolation with the N3 status endpoint:

```bash
# Check video pack N3 compliance
curl -s http://localhost:8000/api/v1/domains/video/n3-status \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool

# Expected:
# {
#   "domain_id": "video",
#   "roster_count": 114,
#   "dna_count": 12,
#   "orphan_agents": 0,
#   "n3_complete": true
# }
```

### 4.2 Cross-Domain Communication (Controlled)

Domains should not communicate directly, but they can share knowledge through the federation layer:

```bash
# Export knowledge graph for federation
curl -X POST http://localhost:8000/api/v1/knowledge/graph/federate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "source_domain": "video",
    "target": "neo4j",
    "filter": {
      "entity_types": ["process", "skill", "decision"],
      "min_confidence": 0.8
    }
  }'
```

### 4.3 N3 Inventory Enforcement in CI

The N3 rule (video pack retains all 114 agents) must be enforced in CI:

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
          python-version: '3.11'
      - name: Run inventory check
        run: python scripts/business/inventory_check.py
      - name: Validate business layer
        run: npm run business:validate
```

---

## 5. Federated Knowledge Graph

### 5.1 Neo4j/GraphAnything Export

For deployments that need advanced graph queries beyond K1-lite, export to an external graph database:

```bash
# Set up Neo4j connection
export NEO4J_URI=bolt://neo4j-host:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=secret
```

**Step 1:** Configure federation in the backend:

```python
# Federation configuration
FEDERATION_CONFIG = {
    "neo4j": {
        "uri": os.getenv("NEO4J_URI"),
        "auth": (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD")),
        "database": "swarm_knowledge",
        "batch_size": 500,
        "export_schedule": "0 */4 * * *"  # Every 4 hours
    }
}
```

**Step 2:** Trigger a federation export:

```bash
# Export current knowledge graph to Neo4j
curl -X POST http://localhost:8000/api/v1/knowledge/graph/federate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "target": "neo4j",
    "mode": "incremental",
    "since": "2026-07-01T00:00:00Z"
  }'

# Response:
# {
#   "status": "completed",
#   "entities_exported": 1247,
#   "relations_exported": 3891,
#   "duration_seconds": 45
# }
```

**Step 3:** Query the federated graph:

```bash
# Use the graph query endpoint for local K1-lite queries
curl -s "http://localhost:8000/api/v1/knowledge/graph/query?seed=contract+review" \
  -H "Authorization: Bearer $TOKEN"

# For complex multi-hop queries, use Neo4j directly
# Cypher query example:
# MATCH (a:Entity)-[r:RELATES_TO*1..3]->(b:Entity)
# WHERE a.name = 'contract_review'
# RETURN a, r, b
```

### 5.2 Gap Detection

Identify knowledge gaps that need filling:

```bash
# Run gap detection
curl -s http://localhost:8000/api/v1/knowledge/graph/gaps \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool

# Response includes entities with few connections, isolated clusters,
# and topics mentioned in queries but not in the knowledge base
```

---

## 6. CI/CD Integration

### 6.1 Pipeline Design

A production CI/CD pipeline for Generic Swarm Ops includes validation gates at every stage:

```yaml
# .github/workflows/deploy.yml
name: Deploy Generic Swarm Ops
on:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Business validation
        run: npm run business:validate
      - name: Security scan
        run: npm run business:security
      - name: Governance check
        run: npm run business:governance
      - name: Inventory check (N3)
        run: python scripts/business/inventory_check.py

  test:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Backend tests
        run: |
          cd backend
          pip install -e .
          pytest tests/ --tb=short
      - name: Evaluation dry run
        run: npm run business:eval -- --dry-run

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build backend image
        run: docker build -t swarm-backend:${{ github.sha }} -f backend/Dockerfile .
      - name: Build frontend image
        run: docker build -t swarm-frontend:${{ github.sha }} -f frontend/Dockerfile .

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: |
          # Rolling deployment - one instance at a time
          kubectl set image deployment/swarm-backend \
            backend=swarm-backend:${{ github.sha }}
          kubectl rollout status deployment/swarm-backend
```

### 6.2 Inventory Checks in Pipelines

The `business:validate` command ensures all required artifacts exist and are well-formed:

```bash
# What business:validate checks:
# 1. All workflow DNA files parse correctly
# 2. All agent specs conform to schema
# 3. Domain manifests are valid
# 4. Required governance artifacts exist
# 5. N3 inventory is complete (for video domain)
npm run business:validate

# Additional evolution check
npm run business:evolution:check
```

> **Tip:** Run `business:validate` as the first step in every CI pipeline. It catches schema errors and missing files before expensive tests run.

---

## 7. Docker Containerization

### 7.1 Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/pyproject.toml backend/setup.cfg ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY backend/ .
COPY business/ /app/business/

# Non-root user
RUN useradd -m swarm && chown -R swarm:swarm /app
USER swarm

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/ready || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 7.2 Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

COPY frontend/ .
RUN pnpm build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

ENV NODE_ENV=production
EXPOSE 3000
CMD ["node", "server.js"]
```

### 7.3 Docker Compose for Development

```yaml
# docker-compose.yml
version: '3.9'

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: generic_swarm_ops
      POSTGRES_USER: swarm
      POSTGRES_PASSWORD: development
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U swarm"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    environment:
      DATABASE_URL: postgresql://swarm:development@postgres:5432/generic_swarm_ops
      GENERIC_SWARM_AUTO_REFLECT: "true"
      PYTHONPATH: "."
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./business:/app/business

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    environment:
      NEXT_PUBLIC_API_BASE_URL: http://backend:8000/api/v1
      NEXT_PUBLIC_DEMO_MODE: "false"
    ports:
      - "3000:3000"
    depends_on:
      - backend

  neo4j:
    image: neo4j:5
    environment:
      NEO4J_AUTH: neo4j/development
    ports:
      - "7474:7474"
      - "7687:7687"
    profiles:
      - graph  # Only start with --profile graph

volumes:
  pgdata:
```

---

## 8. Environment Variable Management

### 8.1 Production Environment Variables

All configuration is managed through environment variables. Never hardcode secrets:

| Variable | Purpose | Required |
|----------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `DATABASE_READ_URL` | Read replica connection (optional) | No |
| `GENERIC_SWARM_AUTO_REFLECT` | Auto-reflect on terminal runs | No (default: true) |
| `GENERIC_SWARM_LLM_CRITIC_ENABLED` | Optional LLM critic for reflection | No |
| `GENERIC_SWARM_EMBEDDINGS_ENABLED` | Enable vector embeddings | No |
| `GENERIC_SWARM_PGVECTOR_ENABLED` | Enable pgvector extension | No |
| `NEO4J_URI` | Neo4j connection for graph federation | No |
| `NEXT_PUBLIC_DEMO_MODE` | Frontend demo mode (false for production) | Yes |
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL for frontend | Yes |

### 8.2 Secrets Management

```bash
# Never store secrets in code or docker-compose files
# Use environment-specific secret managers:

# AWS Secrets Manager
aws secretsmanager get-secret-value --secret-id swarm/production/database

# Kubernetes Secrets
kubectl create secret generic swarm-secrets \
  --from-literal=DATABASE_URL='postgresql://...' \
  --from-literal=NEO4J_PASSWORD='...'

# Docker Swarm Secrets
echo "postgresql://..." | docker secret create database_url -
```

### 8.3 Configuration Validation

Validate all required environment variables on startup:

```python
# backend/app/config.py
import os
import sys

REQUIRED_VARS = ["DATABASE_URL"]
OPTIONAL_VARS = {
    "GENERIC_SWARM_AUTO_REFLECT": "true",
    "GENERIC_SWARM_LLM_CRITIC_ENABLED": "false",
    "GENERIC_SWARM_EMBEDDINGS_ENABLED": "false",
    "GENERIC_SWARM_PGVECTOR_ENABLED": "false",
}

def validate_config():
    """Validate all required environment variables are set."""
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        print(f"FATAL: Missing required environment variables: {missing}")
        sys.exit(1)
    
    # Apply defaults for optional vars
    for var, default in OPTIONAL_VARS.items():
        if not os.getenv(var):
            os.environ[var] = default
```

---

## 9. Real-World Use Cases

### Use Case 1: SaaS Platform with Domain Isolation

A SaaS provider offers Generic Swarm Ops as a managed service with per-tenant domain packs:

- **Architecture:** Shared backend cluster (8 instances), per-tenant PostgreSQL schemas
- **Isolation:** Tool namespaces enforced at schema level, memory scopes per tenant
- **Scaling:** Auto-scale backend instances based on request rate (HPA in Kubernetes)
- **CI/CD:** Canary deployments per tenant, independent rollback capability
- **Result:** 50+ tenants on shared infrastructure with strong isolation guarantees

### Use Case 2: Regulated Financial Services

A bank deploys Generic Swarm Ops for internal operations with strict compliance:

- **Architecture:** Dedicated cluster in private cloud, no shared infrastructure
- **Database:** 3-node PostgreSQL with synchronous replication (zero data loss)
- **Federation:** Neo4j for compliance relationship mapping across all 7-year audit records
- **CI/CD:** Mandatory security scan + governance check + manual approval gates
- **N3 enforcement:** Audit-grade inventory tracking with daily reconciliation
- **Result:** Full regulatory compliance with sub-second query performance on 10M+ records

### Use Case 3: Global Multi-Region Deployment

An international enterprise with operations in EU, US, and APAC:

- **Architecture:** Regional clusters with cross-region replication for knowledge base
- **Database:** Per-region primary with async replication for analytics
- **Compliance:** EU data stays in EU (GDPR), US data in US, federated queries only on metadata
- **Domain packs:** Regional customization (EU=GDPR-aware, US=SOX-aware, APAC=local regulations)
- **CI/CD:** Region-specific deployment pipelines with timezone-aware canary windows
- **Result:** Global coverage with data sovereignty compliance and 99.9% uptime

---

## 10. Best Practices

### Deployment Principles

1. **Stateless backends, stateful database.** Never store application state in the backend process. All state goes to PostgreSQL.

2. **Health checks on every service.** Use `/api/v1/health/ready` for backend, `pg_isready` for database, TCP checks for proxies.

3. **Rolling deployments only.** Never deploy all instances simultaneously. Roll one at a time with health check validation.

4. **Enforce N3 in CI.** The inventory check must pass before any deployment. A broken inventory is a broken system.

5. **Federation is optional, isolation is not.** Neo4j export adds capability but domain isolation must work without it.

6. **Separate read and write paths.** Use replicas for read-heavy operations. Direct all writes to the primary.

7. **Container everything.** Docker images ensure reproducible deployments across all environments.

8. **Validate environment on startup.** Fail fast if required configuration is missing rather than failing on the first request.

9. **Version your DNS/database schemas.** Track schema migrations alongside code deployments.

10. **Monitor replication lag.** In scaled deployments, replication lag can cause stale reads. Alert when lag exceeds acceptable thresholds.

### Deployment Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Shared file system for state | Race conditions, data loss | Use PostgreSQL for all state |
| Manual deployments | Inconsistency, human error | Automate via CI/CD |
| Single database instance | Single point of failure | Primary + replicas |
| No health checks | Failed instances receive traffic | Configure active health checks |
| Secrets in code/compose | Security breach | Use secret managers |

---

## 11. Chapter Summary

This chapter covered large-scale deployment architecture for Generic Swarm Ops:

- **Multi-domain architecture** with horizontal scaling and shared infrastructure
- **Backend scaling** with multiple uvicorn instances behind a load balancer
- **Database replication** with PostgreSQL streaming replication and read/write splitting
- **Domain pack isolation** with namespace enforcement, memory scoping, and N3 compliance
- **Federated knowledge** via Neo4j export using `POST /api/v1/knowledge/graph/federate`
- **CI/CD integration** with `business:validate`, `business:security`, and inventory checks
- **Docker containerization** for reproducible builds and deployments
- **Environment management** with proper secrets handling and startup validation

The key architectural decision is that Generic Swarm Ops backends are stateless. This enables horizontal scaling while PostgreSQL provides the consistency guarantees that a governed AI system requires.

---

## Knowledge Check

1. **Why can Generic Swarm Ops backend instances scale horizontally?**
   - A) They use shared memory
   - B) They are stateless - all state lives in PostgreSQL
   - C) They share a file system
   - D) They use sticky sessions

2. **What does N3 inventory enforcement guarantee for the video domain pack?**
   - A) At least 50 agents are registered
   - B) All 114 video agents remain registered with complete specs
   - C) Agents are automatically created
   - D) Domain packs are isolated from each other

3. **Which API endpoint is used for federated knowledge graph export?**
   - A) `GET /api/v1/knowledge/graph/query`
   - B) `POST /api/v1/knowledge/graph/federate`
   - C) `PUT /api/v1/knowledge/export`
   - D) `POST /api/v1/domains/export`

4. **What is the recommended pool_mode for PgBouncer in production?**
   - A) Session
   - B) Statement
   - C) Transaction
   - D) Direct

5. **Which CI pipeline step should run FIRST before any other checks?**
   - A) Docker build
   - B) Unit tests
   - C) `npm run business:validate`
   - D) Security scan

6. **What is the primary risk of deploying all backend instances simultaneously?**
   - A) Higher cost
   - B) If the new version has a bug, all instances fail at once (no graceful rollback)
   - C) Database overload
   - D) Certificate renewal

7. **Why must environment variables be validated on startup rather than on first request?**
   - A) Startup is faster
   - B) To fail fast and prevent a partially-configured service from handling traffic
   - C) Environment variables cannot be read after startup
   - D) It reduces memory usage

**Answers:** 1-B, 2-B, 3-B, 4-C, 5-C, 6-B, 7-B
