# Chapter 01-03: Initial Setup Wizard

![Setup Wizard Flow](../assets/01-03-setup-wizard-flow.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Execute the complete bootstrap process using `npm run bootstrap`
2. Initialize the business artifact layer with `npm run business:init`
3. Configure the PostgreSQL database connection in `backend/.env`
4. Start the FastAPI backend with uvicorn and verify database connectivity
5. Start the Next.js frontend console with the correct environment variables
6. Verify the full system is operational using health check endpoints
7. Understand the relationship between bootstrap, init, and runtime startup

## Prerequisites

- All dependencies from [Chapter 01-02](01-02-installation-prerequisites.md) installed and verified
- PostgreSQL 14+ running and accessible on `localhost:5432`
- A database named `generic_swarm_ops` created
- The repository cloned to your local machine
- Terminal/shell access in the repository root directory

---

## 1. Setup Process Overview

The initial setup follows a six-phase process:

| Phase | Command / Action | Purpose |
|-------|-----------------|---------|
| 1. Bootstrap | `npm run bootstrap` | Creates business directory tree, installs dependencies |
| 2. Business Init | `npm run business:init` | Scaffolds governance artifacts, creates eval golden tasks |
| 3. Environment | Edit `backend/.env` | Configure database URL and optional features |
| 4. Backend | `uvicorn app.main:app --reload` | Start FastAPI control plane |
| 5. Frontend | `pnpm dev` | Start Next.js ops console |
| 6. Verify | `GET /api/v1/health/ready` | Confirm full system connectivity |

> **Note:** These phases must be executed in order. The backend requires the database
> configuration from Phase 3, and the frontend requires the backend to be running (Phase 4)
> for live API connections.

---

## 2. Phase 1: Bootstrap

The bootstrap command is the entry point for initializing the entire system. It creates
the business directory structure, downloads required sources, and prepares the workspace.

### Step 1: Navigate to the Repository Root

```bash
cd generic-swarm-ops
```

### Step 2: Run Bootstrap

```bash
npm run bootstrap
```

**What this command does:**
1. Creates the `business/` directory tree with all required subdirectories
2. Initializes the starter harness configuration
3. Sets up the dual-harness structure (`.trae/` and `.grok/`)
4. Validates the repository structure

**Expected output:**
```text
> generic-swarm-ops@1.0.0 bootstrap
> node scripts/bootstrap.js

Creating business directory structure...
  business/process-intelligence/event-logs/
  business/process-intelligence/discovered-processes/
  business/process-intelligence/conformance-reports/
  business/process-intelligence/bottlenecks/
  business/process-intelligence/causal-hypotheses/
  business/knowledge-base/rules/
  business/knowledge-base/decision-patterns/
  business/knowledge-base/provenance/
  ...
Bootstrap complete.
```

### Step 3: Verify Bootstrap Results

```bash
# Check the business directory was created
ls business/

# Expected subdirectories:
# evals/  evolution/  governance/  knowledge-base/  materials/
# memory/  process-intelligence/  security/  experts/  distilled/
```

> **Tip:** If bootstrap fails, run `npm run doctor` to diagnose missing prerequisites.
> The doctor command checks all dependencies and reports which ones need attention.

---

## 3. Phase 2: Business Layer Initialization

After bootstrap creates the directory structure, `business:init` populates it with
required governance artifacts and evaluation fixtures.

### Step 1: Initialize the Business Layer

```bash
npm run business:init
```

**What this command does:**
1. Creates governance scaffold (AI inventory, risk tiers, approval policy)
2. Generates initial evaluation golden tasks (at least 20 required)
3. Sets up the evolution workflow DNA template
4. Creates security baseline artifacts

**Expected output:**
```text
> generic-swarm-ops@1.0.0 business:init
> node scripts/business/init.js

Initializing governance artifacts...
  business/governance/ai-inventory/
  business/governance/risk-assessments/
  business/governance/human-approval-policy/
Creating evaluation golden tasks...
  business/evals/golden-tasks/ (20 tasks created)
Setting up evolution templates...
  business/evolution/workflow-dna/
Business layer initialization complete.
```

### Step 2: Validate the Business Layer

```bash
# Run validation to ensure all artifacts are well-formed
npm run business:validate
```

**Expected output:**
```text
> generic-swarm-ops@1.0.0 business:validate
> node scripts/business/validate.js

Validating business artifacts...
  governance: PASS (inventory, risk-tiers, approval-policy)
  evals: PASS (20 golden tasks, schemas valid)
  evolution: PASS (workflow-dna templates present)
  security: PASS (threat-models, tool-permissions)
All validations passed.
```

### Step 3: Run Additional Governance Checks

```bash
# Check governance layer completeness
npm run business:governance

# Check security baseline
npm run business:security
```

> **Warning:** Do not skip the validation step. The runtime rejects workflows that
> reference missing governance artifacts. Running `business:validate` early catches
> these issues before they become runtime errors.

---

## 4. Phase 3: Environment Configuration

The system requires environment variables for database connectivity, API routing,
and optional feature flags.

### Step 1: Create the Backend Environment File

```bash
# Copy the example environment file
cp backend/.env.example backend/.env
```

### Step 2: Configure the Database URL

Edit `backend/.env` and set the `DATABASE_URL`:

```bash
# backend/.env
DATABASE_URL=postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops
```

Replace `gso_user` and `gso_password` with your actual PostgreSQL credentials.

### Step 3: Set the PYTHONPATH

The backend requires `PYTHONPATH=.` for proper module resolution:

```bash
# Set in your shell (Linux/macOS)
export PYTHONPATH=.

# Or on Windows
set PYTHONPATH=.
```

### Step 4: Configure Optional Features

Add optional settings to `backend/.env` as needed:

```bash
# backend/.env (complete example)
DATABASE_URL=postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops

# Auto-reflect on terminal runs (default: true)
GENERIC_SWARM_AUTO_REFLECT=true

# Optional LLM critic (default: false)
GENERIC_SWARM_LLM_CRITIC_ENABLED=false

# Optional embeddings (default: false)
GENERIC_SWARM_EMBEDDINGS_ENABLED=false

# Optional pgvector (default: false)
GENERIC_SWARM_PGVECTOR_ENABLED=false

# Optional Neo4j graph federation
# NEO4J_URI=bolt://localhost:7687
```

### Step 5: Configure Frontend Environment

Set the frontend environment variables in your terminal session:

```bash
# Linux/macOS
export NEXT_PUBLIC_DEMO_MODE=false
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1

# Windows
set NEXT_PUBLIC_DEMO_MODE=false
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

> **Note:** Setting `NEXT_PUBLIC_DEMO_MODE=false` is critical. When set to `true`,
> the frontend uses mock data instead of connecting to the live backend API. For
> production operation, this must always be `false`.

---

## 5. Phase 4: Backend Startup

The FastAPI backend is the control plane for the entire system. It handles authentication,
workflow execution, knowledge retrieval, and all API operations.

### Step 1: Navigate to the Backend Directory

```bash
cd backend
```

### Step 2: Install Python Dependencies

```bash
python -m pip install -e .
```

This installs the backend package in editable mode, including all required dependencies
(FastAPI, uvicorn, psycopg2, pydantic, and infrastructure packages).

### Step 3: Start the Backend Server

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=.  # Linux/macOS
# or: set PYTHONPATH=.  # Windows

# Start uvicorn with hot-reload
uvicorn app.main:app --reload
```

**Expected output:**
```text
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to stop)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Application startup complete.
```

### Step 4: Verify Backend Health

In a new terminal window:

```bash
# Check the health endpoint
curl http://127.0.0.1:8000/api/v1/health/ready
```

**Expected response:**
```json
{
  "database": "postgres",
  "status": "healthy"
}
```

> **Warning:** If the health check returns `"database": "json_file"` instead of
> `"database": "postgres"`, your `DATABASE_URL` is not configured correctly or
> PostgreSQL is not running. The system falls back to JSON file storage, which is
> only suitable for seeding and recovery, not production operation.

### Step 5: Verify API Documentation

The FastAPI backend automatically generates interactive API documentation:

```bash
# Open in browser
# Swagger UI: http://127.0.0.1:8000/docs
# ReDoc: http://127.0.0.1:8000/redoc
```

---

## 6. Phase 5: Frontend Startup

The Next.js frontend provides the ops console for managing agents, workflows, runs,
approvals, and the self-improvement pipeline.

### Step 1: Navigate to the Frontend Directory

```bash
cd frontend
```

### Step 2: Install Frontend Dependencies

```bash
pnpm install
```

**Expected output:**
```text
Packages: +XXX
Progress: resolved XXX, reused XXX, downloaded 0, added XXX, done
```

### Step 3: Start the Development Server

```bash
# Ensure environment variables are set
export NEXT_PUBLIC_DEMO_MODE=false
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1

# Start the Next.js dev server
pnpm dev
```

**Expected output:**
```text
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Ready in Xs
```

### Step 4: Verify Frontend Access

Open your browser and navigate to `http://localhost:3000`. You should see the
Generic Swarm Ops console login page.

> **Tip:** If the frontend shows "Demo Mode" or displays placeholder data, verify that
> `NEXT_PUBLIC_DEMO_MODE` is set to `false` and that the backend is running. The frontend
> requires a live backend connection for ops mode.

---

## 7. Phase 6: Full System Verification

After all services are running, perform a comprehensive verification.

### Step 1: Health Check

```bash
# Backend health
curl -s http://127.0.0.1:8000/api/v1/health/ready | python3 -m json.tool
```

Expected:
```json
{
  "database": "postgres",
  "status": "healthy"
}
```

### Step 2: List Available Workflows

```bash
curl -s http://127.0.0.1:8000/api/v1/workflows | python3 -m json.tool
```

This should return the list of registered workflow definitions, including the flagship
`wf_customer_onboarding_v12`.

### Step 3: List Available Agents

```bash
curl -s http://127.0.0.1:8000/api/v1/agents | python3 -m json.tool
```

This should return the agent roster with configured agents.

### Step 4: Test Authentication

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}'
```

Expected: A successful authentication response with a session token.

### Step 5: Frontend Connectivity Check

1. Open `http://localhost:3000` in your browser
2. Log in with `admin@example.com` / `admin-password`
3. Navigate to the Agents page -- should show live agent data
4. Navigate to the Workflows page -- should show registered workflows

### Step 6: Run Business Layer Validation

```bash
# From the repository root
npm run business:validate
npm run business:governance
npm run business:security
```

All three commands should pass without errors.

---

## 8. Understanding the Startup Sequence

### 8.1 Why This Order Matters

The setup phases have strict dependencies:

```text
bootstrap ─┬─► business:init ──► environment config
            │                           │
            │                           ▼
            │                    backend startup
            │                           │
            │                           ▼
            │                    frontend startup
            │                           │
            │                           ▼
            └──────────────────► full verification
```

- **bootstrap** must run first because it creates the directory structure that
  `business:init` populates
- **business:init** must run before the backend because the runtime loads governance
  artifacts at startup
- The **backend** must start before the frontend because the frontend calls backend
  APIs for live data
- **Verification** confirms all layers are connected and operational

### 8.2 What Happens at Backend Startup

When uvicorn starts the FastAPI application (`app.main:app`), the following occurs:

1. Middleware is registered (request ID injection, CORS, security headers)
2. Database connection is established via `DATABASE_URL`
3. If the `runtime_state` table is empty, the seed data from `backend/data/runtime.json`
   is loaded
4. API routes are registered for all modules (auth, workflows, agents, runs, etc.)
5. The self-improvement module is initialized (if `GENERIC_SWARM_AUTO_REFLECT=true`)

### 8.3 What Happens at Frontend Startup

When Next.js starts (`pnpm dev`), it:

1. Reads environment variables (`NEXT_PUBLIC_DEMO_MODE`, `NEXT_PUBLIC_API_BASE_URL`)
2. If `DEMO_MODE=false`, configures API client to connect to the backend
3. Sets up app router with pages for each system function
4. Initializes Zod validation schemas for forms
5. Registers React Hook Form handlers for agent/workflow creation

---

## 9. Post-Setup Commands Reference

After initial setup, these commands are available for ongoing operation:

### 9.1 Orchestration Commands

```bash
# Re-run bootstrap (safe to repeat)
npm run bootstrap

# System health check
npm run doctor

# Download external sources
npm run sources:download

# Audit downloaded sources
npm run sources:audit

# Regenerate dual-harness files
npm run sync

# Check sync status
npm run sync:check
```

### 9.2 Business Layer Commands

```bash
# Initialize business artifacts
npm run business:init

# Validate all artifacts
npm run business:validate

# Check governance completeness
npm run business:governance

# Run security baseline
npm run business:security

# Check evolution readiness
npm run business:evolution:check

# Run evaluations (dry run)
npm run business:eval -- --dry-run
```

### 9.3 Backend Commands

```bash
cd backend

# Install/update dependencies
python -m pip install -e .

# Start with hot-reload
uvicorn app.main:app --reload

# Run unit tests
python -m unittest discover -s app/tests/unit -p "test_*.py"

# Run end-to-end tests
python -m unittest discover -s app/tests/e2e -p "test_*.py"
```

### 9.4 Frontend Commands

```bash
cd frontend

# Install dependencies
pnpm install

# Start dev server
pnpm dev

# Run linter
pnpm lint

# Run type checking
pnpm typecheck

# Run tests
pnpm test
```

---

## 10. Self-Improvement API Endpoints

The backend exposes these self-improvement APIs for the evolution pipeline:

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/improvement/reflect/{run_id}` | Reflect on a completed run |
| GET | `/api/v1/improvement/lessons` | Retrieve stored lessons learned |
| POST | `/api/v1/improvement/auto-propose` | Generate workflow improvement proposals |
| POST | `/api/v1/loops/run` | Execute a self-improvement loop |
| GET | `/api/v1/evolution/archive` | View the evolution population archive |
| POST | `/api/v1/knowledge/graph/federate` | Push to knowledge graph (requires Neo4j) |

---

## 11. Real-World Use Cases

### Use Case 1: Multi-Service Development Environment

**Scenario:** A developer needs to work on both backend and frontend simultaneously,
with hot-reload on both sides.

**Approach:**

Open three terminal windows:

```bash
# Terminal 1: Backend
cd backend
export PYTHONPATH=.
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
export NEXT_PUBLIC_DEMO_MODE=false
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
pnpm dev

# Terminal 3: Business validation (run periodically)
npm run business:validate
```

Changes to Python files trigger backend reload. Changes to TypeScript/React files
trigger frontend reload. Business artifact changes are validated on demand.

### Use Case 2: Headless API-Only Setup

**Scenario:** A team wants to run the system without the frontend, using only API
calls for integration testing or headless automation.

**Approach:**

```bash
# Only start the backend
cd backend
export PYTHONPATH=.
export DATABASE_URL=postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops
uvicorn app.main:app --reload

# Test with curl
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}'

# List workflows
curl http://127.0.0.1:8000/api/v1/workflows

# Trigger a workflow run
curl -X POST http://127.0.0.1:8000/api/v1/runs \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "wf_customer_onboarding_v12", "payload": {"case_id": "test_001"}}'
```

### Use Case 3: Database Reset and Re-Seeding

**Scenario:** After extensive testing, a developer wants to reset the system to its
initial state.

**Approach:**

```bash
# Stop the backend (Ctrl+C in the backend terminal)

# Drop and recreate the database
psql postgresql://localhost:5432/postgres -c "DROP DATABASE generic_swarm_ops;"
psql postgresql://localhost:5432/postgres -c "CREATE DATABASE generic_swarm_ops;"

# Re-initialize business artifacts
npm run business:init
npm run business:validate

# Restart backend (it will seed from runtime.json)
cd backend
uvicorn app.main:app --reload

# Verify health
curl http://127.0.0.1:8000/api/v1/health/ready
# Should show: {"database": "postgres"}
```

---

## 12. Best Practices

1. **Always verify health after startup** -- the `GET /api/v1/health/ready` endpoint
   should always return `"database": "postgres"`. If it returns `"json_file"`, fix your
   database configuration immediately.

2. **Use hot-reload during development** -- the `--reload` flag on uvicorn and the
   `pnpm dev` command both support hot-reload, eliminating the need for manual restarts.

3. **Run `business:validate` after any artifact change** -- this catches schema violations
   and missing references before they become runtime errors.

4. **Keep environment variables consistent** -- use the same `DATABASE_URL` for backend
   startup and direct database operations. Inconsistency causes subtle bugs.

5. **Start services in order** -- database first, then backend, then frontend. The
   reverse order causes connection errors that may be confusing.

6. **Use the seed credentials for initial testing** -- `admin@example.com` /
   `admin-password` is pre-configured. Change these in production.

7. **Check `backend/docs/postgres-runbook.md`** -- for database-specific operations
   like backup, restore, and schema migrations.

---

## 13. Chapter Summary

In this chapter, you completed the full initial setup process:

- **Phase 1 (Bootstrap):** Created the business directory structure with `npm run bootstrap`
- **Phase 2 (Business Init):** Populated governance and evaluation artifacts with
  `npm run business:init`
- **Phase 3 (Environment):** Configured `backend/.env` with `DATABASE_URL` and set
  frontend environment variables (`NEXT_PUBLIC_DEMO_MODE=false`, `NEXT_PUBLIC_API_BASE_URL`)
- **Phase 4 (Backend):** Started the FastAPI server with `uvicorn app.main:app --reload`
- **Phase 5 (Frontend):** Started the Next.js console with `pnpm dev`
- **Phase 6 (Verify):** Confirmed full system health via API endpoints and browser access

The system is now operational and ready for first-time configuration (next chapter).

---

## 14. Knowledge Check Quiz

**Question 1:** What is the correct command to bootstrap the system?

a) `npm start`
b) `npm run bootstrap`
c) `npm run init`
d) `npm run setup`

<details>
<summary>Answer</summary>
<b>b)</b> <code>npm run bootstrap</code> creates the business directory structure and
initializes the workspace. It is the first command to run in a fresh clone.
</details>

---

**Question 2:** What does `NEXT_PUBLIC_DEMO_MODE=false` do?

a) Disables the frontend entirely
b) Enables dark mode in the UI
c) Connects the frontend to the live backend API instead of mock data
d) Disables authentication

<details>
<summary>Answer</summary>
<b>c)</b> Setting <code>NEXT_PUBLIC_DEMO_MODE=false</code> puts the frontend in ops mode,
where it connects to the live backend API specified by <code>NEXT_PUBLIC_API_BASE_URL</code>.
When set to <code>true</code>, the frontend uses mock/demo data.
</details>

---

**Question 3:** What does the health endpoint return when the database is properly connected?

a) `{"status": "ok"}`
b) `{"database": "postgres", "status": "healthy"}`
c) `{"connected": true}`
d) `{"health": "green"}`

<details>
<summary>Answer</summary>
<b>b)</b> <code>GET /api/v1/health/ready</code> returns
<code>{"database": "postgres"}</code> when properly connected to PostgreSQL.
If it returns <code>"json_file"</code>, the database configuration is incorrect.
</details>

---

**Question 4:** In what order must the services be started?

a) Frontend, Backend, Database
b) Database, Frontend, Backend
c) Database, Backend, Frontend
d) Backend, Database, Frontend

<details>
<summary>Answer</summary>
<b>c)</b> Database (PostgreSQL) must be running first, then the Backend (which connects
to the database), then the Frontend (which connects to the backend API).
</details>

---

**Question 5:** What command validates all business artifacts are well-formed?

a) `npm run doctor`
b) `npm run business:validate`
c) `npm run business:check`
d) `npm test`

<details>
<summary>Answer</summary>
<b>b)</b> <code>npm run business:validate</code> checks all business artifacts against
their schemas and validates cross-references. <code>npm run doctor</code> checks system
prerequisites, not artifact validity.
</details>

---

**Question 6:** What happens if the backend starts without a valid `DATABASE_URL`?

a) It crashes immediately
b) It falls back to JSON file storage (not suitable for production)
c) It creates a SQLite database
d) It waits for the database to become available

<details>
<summary>Answer</summary>
<b>b)</b> The backend falls back to using <code>backend/data/runtime.json</code> as a
file-based store. This is suitable only for seeding and recovery, not production.
The health endpoint will report <code>"database": "json_file"</code> in this state.
</details>

---

**Question 7:** Which file should you copy to create your backend environment configuration?

a) `backend/config.example`
b) `backend/.env.example`
c) `backend/settings.yml`
d) `backend/environment.json`

<details>
<summary>Answer</summary>
<b>b)</b> Copy <code>backend/.env.example</code> to <code>backend/.env</code> and
customize the values for your environment. This file documents all available variables.
</details>

---

## Next Chapter

Continue to [Chapter 01-04: First-Time Configuration](01-04-first-time-configuration.md)
to configure authentication, agents, and your first workflow.
