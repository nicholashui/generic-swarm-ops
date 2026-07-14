# Chapter 4.1: Common Error Resolution

![Error Resolution Flowchart](../assets/04-01-error-resolution-flowchart.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Identify and categorize errors by their source layer (bootstrap, backend, frontend, evolution)
2. Apply systematic resolution procedures for each error category
3. Use diagnostic commands to pinpoint root causes quickly
4. Resolve the most common operational issues without external support
5. Understand fail-closed behavior and how it protects system integrity

## Prerequisites

Before working through this chapter, ensure you have:

- Completed the installation steps from Section 1 (Node.js 20+, Python 3.11+, PostgreSQL 14+, Git, pnpm)
- Access to a terminal with the Generic Swarm Ops repository cloned
- Basic familiarity with environment variables and command-line operations
- Read Chapter 1.1 (System Architecture) for context on the layered structure

---

## 1. Error Categorization Framework

Generic Swarm Ops errors fall into four distinct categories, each corresponding to a system layer:

| Category | Layer | Common Triggers |
|----------|-------|-----------------|
| Bootstrap/Starter | Infrastructure setup | Missing prerequisites, failed source downloads |
| Backend/Postgres | Runtime services | Database connectivity, auth, memory scopes |
| Frontend | User interface | Environment config, API drift, test setup |
| Evolution | Self-improvement | Incomplete evidence, blocked promotions |

> **Tip:** Always start diagnosis by identifying which layer the error originates from. Running `npm run doctor` first eliminates the most basic issues before you investigate deeper problems.

---

## 2. Bootstrap and Starter Layer Errors

### 2.1 Source Lock Failures

**Symptom:** `npm run bootstrap` fails with errors referencing `sources/source-lock.json`.

**Root Cause:** External source repositories could not be cloned or the lock file is corrupted.

**Resolution Steps:**

1. Inspect the lock file for clone failures:

```bash
cat sources/source-lock.json
```

2. Look for entries with `"status": "failed"` or missing `"commit"` hashes.

3. Verify network connectivity to the source repositories listed in the lock file.

4. Re-run the source download:

```bash
npm run sources:download
```

5. Verify the lock file is now complete:

```bash
cat sources/source-lock.json | python -m json.tool
```

**Expected Outcome:** All entries in `source-lock.json` show successful status with valid commit hashes.

> **Warning:** Never manually edit `source-lock.json`. Always use `npm run sources:download` to regenerate it.

### 2.2 Source Audit Warnings

**Symptom:** `npm run bootstrap` reports audit warnings or `docs/source-audit.md` contains unresolved findings.

**Root Cause:** Downloaded external sources have unverified licensing, integrity issues, or policy violations.

**Resolution Steps:**

1. Review the audit report:

```bash
cat docs/source-audit.md
```

2. Run the audit command independently to see current status:

```bash
npm run sources:audit
```

3. For each warning, determine if the source:
   - Has an acceptable license for your use case
   - Passes integrity checks (hash matches)
   - Meets your organization's security policy

4. Address individual findings by either:
   - Updating the source configuration to accept the license
   - Removing problematic sources from the configuration
   - Filing an exception with your governance process

**Expected Outcome:** `docs/source-audit.md` shows all sources passing or with documented exceptions.

### 2.3 Missing Business Seed Files

**Symptom:** `npm run business:validate` reports missing required files, or bootstrap complains about absent business artifacts.

**Root Cause:** The business operating-system layer has not been initialized, or files were accidentally deleted.

**Resolution Steps:**

1. Initialize the business layer:

```bash
npm run business:init
```

2. Verify the generated structure:

```bash
ls business/
ls business/process-intelligence/
ls business/evolution/
ls business/governance/
ls business/evals/golden-tasks/
ls business/knowledge-base/
```

3. Run validation to confirm all required files exist:

```bash
npm run business:validate
```

**Expected Outcome:** All business directories contain their required seed files, and validation passes.

### 2.4 Schema and Validation Failures

**Symptom:** `npm run business:validate` reports schema violations, provenance failures, risk-tier mismatches, or workflow-gate errors.

**Root Cause:** Business artifacts do not conform to the expected schemas or have incomplete metadata.

**Resolution Steps:**

1. Run validation with verbose output:

```bash
npm run business:validate
```

2. For each failure type:

   **Schema violations:**
   ```bash
   # Check the artifact against its expected schema
   # Look at the specific field reported as invalid
   # Correct the data format or add missing required fields
   ```

   **Provenance failures:**
   ```bash
   # Ensure each artifact has proper provenance metadata
   # Check that source references are valid
   # Verify creation timestamps and authorship
   ```

   **Risk-tier mismatches:**
   ```bash
   # Verify the declared risk tier matches the artifact's actual scope
   # Higher-risk artifacts need more governance evidence
   ```

   **Workflow-gate errors:**
   ```bash
   # Ensure all prerequisite gates have been passed
   # Check that approval records exist for gated transitions
   ```

3. After fixing, re-run validation:

```bash
npm run business:validate
```

**Expected Outcome:** All validation checks pass with no errors.

### 2.5 Security Scan Failures

**Symptom:** `npm run business:security` reports secrets in files, unsafe permissions, or prompt-injection coverage gaps.

**Root Cause:** Business artifacts contain sensitive data, have overly permissive configurations, or lack adversarial test coverage.

**Resolution Steps:**

1. Run the security scan:

```bash
npm run business:security
```

2. Address findings by category:

   **Secrets detected:**
   - Remove any hardcoded credentials, API keys, or tokens
   - Move sensitive values to environment variables
   - Add patterns to `.gitignore` if needed

   **Unsafe permissions:**
   - Review agent permission boundaries
   - Ensure least-privilege principle is followed
   - Tighten any overly broad scope declarations

   **Prompt-injection coverage gaps:**
   - Add adversarial test cases to the evaluation corpus
   - Ensure critical prompts have injection resistance testing
   - Document mitigations in the governance model card

3. Re-run to verify fixes:

```bash
npm run business:security
```

**Expected Outcome:** Security scan completes with no findings.

---

## 3. Backend and Postgres Errors

### 3.1 Health Endpoint Shows No Postgres

**Symptom:** `GET /api/v1/health/ready` does not return `"database": "postgres"`, or the health check fails entirely.

**Root Cause:** The `DATABASE_URL` environment variable is missing or incorrect, or PostgreSQL is not running.

**Resolution Steps:**

1. Check your backend environment file:

```bash
cat backend/.env
```

2. Verify `DATABASE_URL` is present and correctly formatted:

```
DATABASE_URL=postgresql://user:pass@localhost:5432/generic_swarm_ops
```

3. Verify PostgreSQL is running:

```bash
# On Linux/Mac
pg_isready

# On Windows
pg_isready -h localhost -p 5432
```

4. If PostgreSQL is not running, start it:

```bash
# Linux systemd
sudo systemctl start postgresql

# macOS Homebrew
brew services start postgresql

# Docker
docker run -d --name gso-postgres -p 5432:5432 -e POSTGRES_PASSWORD=pass postgres:14
```

5. Verify the database exists:

```bash
psql -U user -h localhost -l | grep generic_swarm_ops
```

6. If missing, create it:

```bash
createdb -U user -h localhost generic_swarm_ops
```

7. Restart the backend and check health:

```bash
cd backend
set PYTHONPATH=.
uvicorn app.main:app --reload
# In another terminal:
curl http://127.0.0.1:8000/api/v1/health/ready
```

**Expected Outcome:** Health endpoint returns JSON with `"database": "postgres"`.

> **Note:** The primary data store is Postgres JSONB. JSON file storage is backup only. If the database appears empty after a restart, ensure you are connecting to the same PostgreSQL instance and database.

### 3.2 Empty Database After Restart

**Symptom:** Data appears to be missing after restarting the backend service.

**Root Cause:** The primary store is Postgres JSONB, and JSON file is backup only. You may be connecting to a different database instance.

**Resolution Steps:**

1. Verify your `DATABASE_URL` points to the correct instance:

```bash
cat backend/.env | grep DATABASE_URL
```

2. Check that the database has data:

```bash
psql "$DATABASE_URL" -c "SELECT count(*) FROM runtime_state;"
```

3. If using Docker, ensure the container is the same one (not recreated without a volume):

```bash
docker ps -a | grep postgres
docker volume ls
```

4. For persistent Docker storage, always use a named volume:

```bash
docker run -d --name gso-postgres \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=pass \
  -v gso_pgdata:/var/lib/postgresql/data \
  postgres:14
```

**Expected Outcome:** Data persists across backend restarts.

### 3.3 Authentication Failures

**Symptom:** API calls return 401 Unauthorized or 403 Forbidden errors.

**Root Cause:** Incorrect authentication method or expired credentials.

**Resolution Steps:**

1. Use password-based login (preferred method):

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}'
```

2. The response sets a cookie `gso_access_token`. Use it for subsequent requests:

```bash
curl -b "gso_access_token=<token_value>" \
  http://127.0.0.1:8000/api/v1/workflows
```

3. If using static bearer tokens (smoke testing only):

```bash
curl -H "Authorization: Bearer admin-token" \
  http://127.0.0.1:8000/api/v1/health/ready
```

> **Warning:** Static bearer tokens (`admin-token`) are for curl smoke tests only. Always prefer password-based login for actual operation.

4. Verify RBAC permissions for the target endpoint if you receive 403 errors.

**Expected Outcome:** Authentication succeeds and API calls return expected data.

### 3.4 Tool Step Fails Closed

**Symptom:** A workflow step involving a tool adapter fails with an error about missing inputs or rejected execution.

**Root Cause:** Tool adapters use fail-closed behavior - they reject execution if required inputs are missing or invalid.

**Resolution Steps:**

1. Inspect the `tool_effects` for the failed step:

```bash
# Check the audit log for the specific tool execution
curl -b "gso_access_token=<token>" \
  http://127.0.0.1:8000/api/v1/audit?event_type=tool.executed
```

2. Look for the specific adapter that failed (crm, billing, email, audit, contract_parser, policy_retriever).

3. Verify all required inputs are provided in the workflow step configuration.

4. Check that the tool adapter's prerequisites are met:
   - Required fields are non-null
   - Data types match expectations
   - Referenced entities exist in the system

5. Correct the workflow step inputs and retry:

```bash
# Re-run the workflow with corrected payload
curl -X POST http://127.0.0.1:8000/api/v1/workflows/<workflow_id>/run \
  -b "gso_access_token=<token>" \
  -H "Content-Type: application/json" \
  -d '{"case_id": "valid_case_id", ...}'
```

**Expected Outcome:** Tool adapter executes successfully with proper `tool_effects` recorded.

> **Tip:** Fail-closed behavior is a safety feature. It prevents agents from executing actions with incomplete information. Always provide all required inputs rather than trying to bypass the check.

### 3.5 Flagship Run Fails on Memory Scope

**Symptom:** A run of the flagship workflow (`wf_customer_onboarding_v12`) fails mid-run with memory scope errors.

**Root Cause:** Agents in the workflow need correct `allowed_memory_scopes`. The seed/normalize union must include organization-level scopes.

**Resolution Steps:**

1. Check the current memory scope configuration for the failing agent:

```bash
curl -b "gso_access_token=<token>" \
  http://127.0.0.1:8000/api/v1/agents/<agent_id>
```

2. Verify that `allowed_memory_scopes` includes all necessary scopes:
   - Agent-level scopes (personal context)
   - Organization-level scopes (shared data)
   - Workflow-level scopes (execution context)

3. Update the agent's memory scope configuration to include the union of seed and normalize scopes:

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/agents/<agent_id> \
  -b "gso_access_token=<token>" \
  -H "Content-Type: application/json" \
  -d '{"allowed_memory_scopes": ["agent", "organization", "workflow"]}'
```

4. Retry the flagship run:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/workflows/wf_customer_onboarding_v12/run \
  -b "gso_access_token=<token>" \
  -H "Content-Type: application/json" \
  -d '{"case_id": "test_case_001"}'
```

**Expected Outcome:** Flagship workflow completes all steps without memory scope errors.

### 3.6 Import and PYTHONPATH Errors

**Symptom:** Python import errors when running tests or starting uvicorn from the backend directory.

**Root Cause:** The `PYTHONPATH` environment variable is not set to the backend directory.

**Resolution Steps:**

1. Navigate to the backend directory:

```bash
cd backend
```

2. Set the PYTHONPATH:

```bash
# Windows
set PYTHONPATH=.

# Linux/macOS
export PYTHONPATH=.
```

3. Verify imports work:

```bash
python -c "from app.main import app; print('Import OK')"
```

4. Now run your command:

```bash
# For uvicorn
uvicorn app.main:app --reload

# For tests
python -m unittest discover -s app/tests/unit -p "test_*.py" -v
```

**Expected Outcome:** No `ModuleNotFoundError` or `ImportError` messages.

> **Note:** Always set `PYTHONPATH=.` before running any backend commands. This ensures Python can resolve the `app` package correctly relative to the `backend/` directory.

---

## 4. Frontend Errors

### 4.1 Demo Data Only (Stuck in Demo Mode)

**Symptom:** The frontend displays only demo/mock data instead of live data from the backend.

**Root Cause:** The `NEXT_PUBLIC_DEMO_MODE` environment variable is set to `true` (or not set to `false`), or the API base URL is not configured.

**Resolution Steps:**

1. Stop the frontend development server if running.

2. Set the required environment variables:

```bash
cd frontend

# Windows
set NEXT_PUBLIC_DEMO_MODE=false
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1

# Linux/macOS
export NEXT_PUBLIC_DEMO_MODE=false
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

3. Alternatively, create or update `frontend/.env.local`:

```env
NEXT_PUBLIC_DEMO_MODE=false
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

4. Verify the backend is running:

```bash
curl http://127.0.0.1:8000/api/v1/health/ready
```

5. Restart the frontend:

```bash
pnpm dev
```

**Expected Outcome:** Frontend displays live data from the backend API.

### 4.2 Mutations Show No Detail

**Symptom:** API mutation errors in the frontend show generic error messages without helpful detail.

**Root Cause:** The backend error envelope includes `message` and `request_id` fields, but you need to inspect the network tab to see them.

**Resolution Steps:**

1. Open browser developer tools (F12 or Cmd+Option+I).

2. Navigate to the Network tab.

3. Reproduce the failing mutation (form submission, action click, etc.).

4. Find the failed request (usually shown in red).

5. Inspect the response body for:

```json
{
  "message": "Detailed error description",
  "request_id": "uuid-for-tracing"
}
```

6. Use the `request_id` to trace the error in backend logs:

```bash
# Search backend logs for the request ID
grep "request_id" backend/logs/ -r
```

7. Address the underlying issue based on the error message.

**Expected Outcome:** You can identify the specific error cause and resolve it.

> **Tip:** The `request_id` is your most valuable debugging tool when frontend errors lack detail. It connects the frontend error to the exact backend log entry.

### 4.3 Playwright Smoke Tests Skipped

**Symptom:** End-to-end tests are skipped or fail because services are not available.

**Root Cause:** Playwright E2E tests require both the backend and frontend to be running.

**Resolution Steps:**

1. Start the backend (in one terminal):

```bash
cd backend
set PYTHONPATH=.
uvicorn app.main:app --reload
```

2. Start the frontend (in another terminal):

```bash
cd frontend
set NEXT_PUBLIC_DEMO_MODE=false
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
pnpm dev
```

3. Run the E2E tests (in a third terminal):

```bash
cd frontend
pnpm test:e2e
```

4. Alternatively, use the auto-start flag:

```bash
cd frontend
E2E_START=1 pnpm test:e2e
```

**Expected Outcome:** Playwright tests execute against the live services and report pass/fail results.

### 4.4 OpenAPI Types Drift

**Symptom:** TypeScript type errors in the frontend that reference API response shapes, or runtime type mismatches between frontend expectations and backend responses.

**Root Cause:** The generated OpenAPI client types are out of sync with the current backend API schema.

**Resolution Steps:**

1. Ensure the backend is running and exporting its OpenAPI schema:

```bash
cd backend
set PYTHONPATH=.
uvicorn app.main:app --reload
# Verify schema is available:
curl http://127.0.0.1:8000/openapi.json > /dev/null && echo "Schema available"
```

2. Regenerate the frontend API types:

```bash
cd frontend
pnpm api:generate
```

3. Run type checking to confirm the drift is resolved:

```bash
pnpm typecheck
```

4. If new type errors appear, update the frontend components to match the new API shape.

**Expected Outcome:** `pnpm typecheck` passes with no errors after regenerating API types.

---

## 5. Evolution and Self-Improvement Errors

### 5.1 Variants Stuck in Sandbox

**Symptom:** Evolved variants never appear in production, remaining in the sandbox directory.

**Root Cause:** This is intentional behavior. Variants stay sandbox-only until they complete the full evaluation and canary process. `auto_promote` is always blocked.

**Resolution Steps:**

1. Check the variant's current status:

```bash
ls business/distilled/skills/_sandbox/
```

2. Verify that evaluation has been completed:

```bash
npm run business:evolution:check
```

3. Follow the promotion pipeline:
   - **Evaluate:** Run the variant through the golden task corpus
   - **Canary:** Deploy as a canary alongside the current production version
   - **Promote:** Explicitly promote after canary success

4. Use the self-improvement APIs:

```bash
# Reflect on a run
curl -X POST http://127.0.0.1:8000/api/v1/improvement/reflect/<run_id> \
  -b "gso_access_token=<token>"

# Check proposals
curl http://127.0.0.1:8000/api/v1/improvement/lessons \
  -b "gso_access_token=<token>"

# Propose improvements
curl -X POST http://127.0.0.1:8000/api/v1/improvement/auto-propose \
  -b "gso_access_token=<token>"
```

**Expected Outcome:** Variants are promoted only after completing the full evidence trail.

> **Warning:** Never attempt to bypass the sandbox by manually moving files to production directories. The governance system requires a complete evidence trail for all promotions.

### 5.2 Incomplete Promotion Evidence

**Symptom:** `npm run business:evolution:check` reports missing evidence for a variant promotion.

**Root Cause:** The promotion pipeline requires evaluation scores, canary results, and governance sign-off before a variant can be promoted.

**Resolution Steps:**

1. Run the evolution check to see what is missing:

```bash
npm run business:evolution:check
```

2. For each missing piece of evidence:

   **Missing evaluation:**
   ```bash
   npm run business:eval -- --variant <variant_name>
   ```

   **Missing canary results:**
   - Deploy the variant as a canary through the ops console
   - Or use the API: `POST /api/v1/loops/run`

   **Missing governance sign-off:**
   - Ensure the model card is updated
   - Verify the assurance case covers the variant
   - Get human reviewer approval

3. Re-run the check:

```bash
npm run business:evolution:check
```

**Expected Outcome:** All evidence requirements are satisfied and the variant is eligible for promotion.

---

## 6. Real-World Use Case Examples

### Use Case 1: New Developer Onboarding

**Scenario:** A new developer joins the team and cannot get the system running after cloning the repository.

**Diagnosis Path:**

1. Run `npm run doctor` - discovers Node.js is version 18 (needs 20+)
2. Update Node.js to version 20+
3. Run `npm run bootstrap` - source download fails (corporate proxy)
4. Configure Git proxy settings
5. Re-run `npm run bootstrap` - succeeds
6. Run `cd backend && pip install -e .` - Python 3.9 detected (needs 3.11+)
7. Install Python 3.11+
8. Set PYTHONPATH and start backend
9. Run health check - `"database": "postgres"` confirmed

**Outcome:** Full stack running in under 30 minutes with systematic error resolution.

### Use Case 2: Production Workflow Failure

**Scenario:** The flagship customer onboarding workflow fails at the billing step during a live demonstration.

**Diagnosis Path:**

1. Check audit logs for `tool.executed` events on the billing adapter
2. Find `tool_effects` showing missing `case_id` in the input payload
3. Verify the workflow was started with a valid `case_id`
4. Discover the test payload was missing the required field
5. Re-run with corrected payload: `{"case_id": "demo_001"}`
6. Workflow completes successfully through all steps including human-gated billing approval

**Outcome:** Root cause identified in 5 minutes via audit trail inspection.

### Use Case 3: Evolution Pipeline Blocked

**Scenario:** A promising variant has been proposed but will not promote to production.

**Diagnosis Path:**

1. Run `npm run business:evolution:check` - reports missing canary evidence
2. Check the evolution archive: `GET /api/v1/evolution/archive`
3. Find the variant in sandbox state
4. Run evaluation: variant scores above threshold on golden tasks
5. Deploy as canary: variant handles traffic alongside production
6. After successful canary period, explicitly promote
7. Variant now serves production traffic

**Outcome:** Systematic promotion through the safety pipeline takes 2-3 days but ensures no regressions.

---

## 7. Best Practices

### Systematic Diagnosis Approach

1. **Layer identification first:** Always determine which layer (bootstrap, backend, frontend, evolution) the error originates from before attempting fixes.

2. **Run diagnostics before manual investigation:** Use `npm run doctor`, `npm run business:validate`, and `npm run business:security` before diving into logs.

3. **Check the obvious first:** Environment variables, service availability, and database connectivity account for 80% of issues.

4. **Use the audit trail:** The `tool_effects` and audit log provide a complete record of what happened and why.

5. **Verify after fixing:** Always re-run the diagnostic command that revealed the issue to confirm your fix resolved it.

### Prevention Strategies

- Run `npm run doctor` after any system update
- Run `npm run business:validate` before committing business artifacts
- Run `npm run business:security` as part of your pre-commit workflow
- Keep `PYTHONPATH` in your shell profile for backend work
- Use `.env.local` files to persist environment configuration
- Document exceptions and known issues in your team's runbook

### Error Documentation Template

When documenting new errors for your team:

```markdown
## Error: [Brief description]

**Symptom:** What the user observes
**Diagnostic Command:** The command that reveals the issue
**Root Cause:** Why this happens
**Resolution:** Step-by-step fix
**Prevention:** How to avoid recurrence
**Related:** Links to other relevant errors
```

---

## 8. Chapter Summary

This chapter covered the systematic resolution of common errors across all four layers of Generic Swarm Ops:

- **Bootstrap/Starter Layer:** Source lock failures, audit warnings, missing business seeds, validation failures, and security scan issues
- **Backend/Postgres:** Database connectivity, authentication, tool adapter fail-closed behavior, memory scope configuration, and PYTHONPATH issues
- **Frontend:** Demo mode configuration, mutation error inspection, E2E test setup, and OpenAPI type drift
- **Evolution:** Sandbox-only variant behavior, promotion evidence requirements, and the full promotion pipeline

The key principle is systematic diagnosis: identify the layer, run the appropriate diagnostic command, follow the resolution steps, and verify the fix.

---

## 9. Knowledge Check Quiz

Test your understanding of common error resolution:

**Question 1:** Your backend health endpoint returns JSON but does not show `"database": "postgres"`. What are the three things to check?

<details>
<summary>Answer</summary>

1. Verify `DATABASE_URL` is correctly set in `backend/.env`
2. Confirm PostgreSQL is running (use `pg_isready`)
3. Ensure the database name in the URL matches an existing database

</details>

**Question 2:** After a fresh clone, `npm run business:validate` reports missing files. What command should you run first?

<details>
<summary>Answer</summary>

Run `npm run business:init` to seed the required business layer files, then re-run `npm run business:validate` to confirm.

</details>

**Question 3:** The frontend only shows demo data. What two environment variables must be set?

<details>
<summary>Answer</summary>

1. `NEXT_PUBLIC_DEMO_MODE=false` (disable demo mode)
2. `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1` (point to live backend)

</details>

**Question 4:** A tool adapter rejects execution with a fail-closed error. Where do you look to understand what went wrong?

<details>
<summary>Answer</summary>

Inspect `tool_effects` in the audit log. Query the audit API for `event_type=tool.executed` to see exactly what inputs were provided and why the adapter rejected the execution.

</details>

**Question 5:** Why can't a sandbox variant be auto-promoted to production?

<details>
<summary>Answer</summary>

`auto_promote` is always blocked by design. Variants must complete the full pipeline: evaluate (golden task corpus), canary (side-by-side deployment), and explicit human-approved promotion. This ensures safety and prevents regressions.

</details>

**Question 6:** What is the correct command to regenerate frontend API types when they drift from the backend schema?

<details>
<summary>Answer</summary>

From the `frontend/` directory, run `pnpm api:generate` while the backend is running (so the OpenAPI schema is available at `/openapi.json`). Then run `pnpm typecheck` to confirm the drift is resolved.

</details>

**Question 7:** The flagship workflow `wf_customer_onboarding_v12` fails mid-run with a memory scope error. What is the likely cause and fix?

<details>
<summary>Answer</summary>

The agents in the workflow need correct `allowed_memory_scopes`. The seed/normalize union must include organization-level scopes. Update the agent configuration to include `["agent", "organization", "workflow"]` scopes.

</details>
