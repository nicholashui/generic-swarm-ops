# Chapter 4.2: Diagnostic Tools Walkthrough

![Diagnostic Tools Overview](../assets/04-02-diagnostic-tools-overview.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Execute all diagnostic commands and understand their purposes
2. Interpret output from each diagnostic tool correctly
3. Combine multiple diagnostic results for comprehensive system assessment
4. Build diagnostic workflows for routine maintenance
5. Automate diagnostic checks as part of CI/CD pipelines

## Prerequisites

Before working through this chapter, ensure you have:

- Completed installation (Node.js 20+, Python 3.11+, PostgreSQL 14+, Git, pnpm)
- Successfully run `npm run bootstrap` at least once
- Backend and frontend services available (for runtime diagnostics)
- Familiarity with the error categories from Chapter 4.1

---

## 1. Diagnostic Tools Architecture

Generic Swarm Ops provides diagnostic tools organized by system layer. Each tool checks specific aspects of system health and produces actionable output.

| Layer | Command | Purpose |
|-------|---------|---------|
| Starter | `npm run doctor` | Verify prerequisites |
| Starter | `npm run sources:download` | Fetch external sources |
| Starter | `npm run sources:audit` | Audit source integrity |
| Business | `npm run business:init` | Seed required files |
| Business | `npm run business:validate` | Schema/provenance/risk/gate checks |
| Business | `npm run business:governance` | Governance compliance |
| Business | `npm run business:security` | Security posture scan |
| Business | `npm run business:evolution:check` | Promotion evidence |
| Business | `npm run business:eval` | Golden task evaluation |
| Backend | Unit tests | Python test suite |
| Backend | E2E tests | Integration verification |
| Frontend | `pnpm lint` | ESLint code quality |
| Frontend | `pnpm typecheck` | TypeScript type safety |
| Frontend | `pnpm test` | Component/unit tests |

> **Tip:** Run these tools in order from top to bottom when performing a full system diagnostic. Issues at lower layers often cascade from unresolved higher-layer problems.

---

## 2. Starter Layer Diagnostics

### 2.1 npm run doctor

**Purpose:** Verifies that all system prerequisites are installed and at the correct versions.

**What It Checks:**
- Node.js version (requires 20+)
- Git installation and version
- Python version (requires 3.11+)
- PostgreSQL availability (requires 14+)
- pnpm installation

**How to Run:**

```bash
npm run doctor
```

**Interpreting Output:**

A successful run looks like:

```
[PASS] Node.js: v20.11.0 (>= 20.0.0)
[PASS] Git: 2.43.0
[PASS] Python: 3.11.7 (>= 3.11.0)
[PASS] PostgreSQL: 14.10 (>= 14.0)
[PASS] pnpm: 8.15.1

All prerequisites satisfied.
```

A failing run identifies the specific issue:

```
[PASS] Node.js: v20.11.0 (>= 20.0.0)
[PASS] Git: 2.43.0
[FAIL] Python: 3.9.7 (requires >= 3.11.0)
[PASS] PostgreSQL: 14.10 (>= 14.0)
[FAIL] pnpm: not found

2 prerequisites not met. See docs/installation.md.
```

**Action on Failure:**
- Install or upgrade the failing prerequisite
- Re-run `npm run doctor` to confirm the fix
- Refer to `docs/installation.md` for platform-specific installation instructions

> **Note:** Some prerequisites (like PostgreSQL) may be running in Docker. The doctor command checks for client tools, not necessarily the server. Ensure both client and server components are available.

### 2.2 npm run sources:download

**Purpose:** Downloads approved external source repositories into `external/sources/`.

**What It Checks/Does:**
- Clones configured external repositories
- Records commit hashes and status in `sources/source-lock.json`
- Skips already-downloaded sources at the same commit

**How to Run:**

```bash
npm run sources:download
```

**Interpreting Output:**

```
Downloading repository: example-lib (https://github.com/org/example-lib)
  [OK] Cloned at commit abc1234
Downloading repository: utils-pkg (https://github.com/org/utils-pkg)
  [OK] Already at commit def5678 (skipped)

2/2 sources ready.
```

**Post-Run Verification:**

```bash
# Check the lock file
cat sources/source-lock.json
```

Expected lock file structure:

```json
{
  "sources": [
    {
      "name": "example-lib",
      "url": "https://github.com/org/example-lib",
      "commit": "abc1234...",
      "status": "ok",
      "downloaded_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Action on Failure:**
- Check network connectivity to the repository URLs
- Verify Git credentials for private repositories
- Remove `external/sources/<repo>` and re-run if the clone is corrupted

### 2.3 npm run sources:audit

**Purpose:** Audits downloaded external sources for licensing, integrity, and policy compliance.

**What It Checks:**
- License compatibility
- Hash integrity of downloaded sources
- Policy compliance (organization-specific rules)
- Known vulnerability databases

**How to Run:**

```bash
npm run sources:audit
```

**Interpreting Output:**

The command writes its full report to `docs/source-audit.md`. Terminal output summarizes findings:

```
Auditing 2 sources...
  example-lib: [PASS] MIT license, integrity OK
  utils-pkg: [WARN] No license file found

1 warning(s). See docs/source-audit.md for details.
```

**Action on Warnings:**
- Review `docs/source-audit.md` for full details on each warning
- Contact source maintainers about missing license files
- Document exceptions for known-acceptable warnings
- Remove sources that violate organizational policy

---

## 3. Business Layer Diagnostics

### 3.1 npm run business:validate

**Purpose:** Validates all business operating-system artifacts against their expected schemas and rules.

**What It Checks:**
- **Schema compliance:** Business artifacts match their JSON/YAML schemas
- **Provenance:** Each artifact has proper source attribution and metadata
- **Risk-tier alignment:** Declared risk levels match artifact scope and impact
- **Workflow-gate integrity:** All prerequisite gates are properly configured and have approval records

**How to Run:**

```bash
npm run business:validate
```

**Interpreting Output:**

A clean run:

```
Validating business artifacts...
  [PASS] Schema validation: 24/24 artifacts valid
  [PASS] Provenance check: all artifacts have source attribution
  [PASS] Risk-tier alignment: all tiers consistent
  [PASS] Workflow-gate integrity: all gates configured

All validations passed.
```

A failing run with specific issues:

```
Validating business artifacts...
  [FAIL] Schema validation: 2 errors
    - business/evals/golden-tasks/task_05.json: missing "expected_output" field
    - business/governance/model-card.json: "risk_level" must be one of [low, medium, high, critical]
  [PASS] Provenance check: all artifacts have source attribution
  [FAIL] Risk-tier alignment: 1 mismatch
    - business/knowledge-base/policy.json: declared "low" but references "high" risk data
  [PASS] Workflow-gate integrity: all gates configured

2 validation categories failed. Fix issues and re-run.
```

**Action on Failure:**
1. Fix each reported issue in the specific file mentioned
2. For schema errors: add missing fields or correct data types
3. For provenance issues: add source attribution metadata
4. For risk-tier mismatches: align the declared tier with actual scope
5. For gate issues: ensure approval records exist
6. Re-run `npm run business:validate` after each fix

> **Tip:** Run this command before every commit that touches business artifacts. It catches configuration drift before it reaches shared branches.

### 3.2 npm run business:security

**Purpose:** Scans business artifacts and configuration for security issues.

**What It Checks:**
- **Secrets detection:** Hardcoded API keys, passwords, tokens in files
- **Permission auditing:** Overly permissive agent or workflow configurations
- **Prompt-injection coverage:** Adversarial test coverage for critical prompts

**How to Run:**

```bash
npm run business:security
```

**Interpreting Output:**

A clean scan:

```
Security scan...
  [PASS] Secrets: no hardcoded credentials detected
  [PASS] Permissions: all agents follow least-privilege
  [PASS] Prompt-injection: all critical prompts have adversarial coverage

No security findings.
```

A scan with findings:

```
Security scan...
  [FAIL] Secrets: 1 finding
    - business/knowledge-base/config.yaml:12 contains pattern matching API key
  [FAIL] Permissions: 2 findings
    - Agent "data_processor" has write access to all memory scopes (should be restricted)
    - Workflow "batch_import" skips human gate for high-risk operations
  [WARN] Prompt-injection: 1 gap
    - Prompt template "customer_greeting" has no adversarial test case

2 failures, 1 warning.
```

**Action on Findings:**
1. **Secrets:** Remove the credential, move to environment variable, add to `.gitignore`
2. **Permissions:** Restrict agent scopes to minimum required; add human gates for high-risk operations
3. **Prompt-injection:** Add adversarial test cases to `business/evals/golden-tasks/`

### 3.3 npm run business:governance

**Purpose:** Validates governance artifacts including the model card and assurance case.

**What It Checks:**
- Model card completeness and accuracy
- Assurance case structure and evidence links
- Governance policy compliance
- Risk registry currency

**How to Run:**

```bash
npm run business:governance
```

**Interpreting Output:**

```
Governance check...
  [PASS] Model card: complete (all required sections present)
  [PASS] Assurance case: 12/12 claims have evidence
  [PASS] Policy compliance: all active policies satisfied
  [PASS] Risk registry: all entries current (last updated within 30 days)

Governance status: compliant.
```

**Action on Failure:**
- Update the model card with missing sections (under `business/governance/`)
- Add evidence links for unsupported assurance claims
- Review and acknowledge expired risk registry entries

### 3.4 npm run business:evolution:check

**Purpose:** Verifies that sandbox variant promotion evidence is complete.

**What It Checks:**
- Evaluation scores for pending variants
- Canary deployment results
- Governance sign-off records
- Rollback plan documentation

**How to Run:**

```bash
npm run business:evolution:check
```

**Interpreting Output:**

```
Evolution check...
  Variants in sandbox: 3
  
  variant_improved_greeting_v2:
    [PASS] Evaluation: score 0.92 (threshold: 0.85)
    [PASS] Canary: 48h clean run, no regressions
    [PASS] Governance: signed off by reviewer
    Status: ELIGIBLE for promotion
  
  variant_faster_billing_v1:
    [PASS] Evaluation: score 0.88 (threshold: 0.85)
    [FAIL] Canary: not yet deployed
    [SKIP] Governance: pending canary results
    Status: NEEDS canary deployment
  
  variant_new_parser_v3:
    [FAIL] Evaluation: not run
    [SKIP] Canary: pending evaluation
    [SKIP] Governance: pending evaluation
    Status: NEEDS evaluation

2 variants need action. Run evaluations and canary deployments.
```

**Action on Incomplete Evidence:**
1. Run evaluations for untested variants: `npm run business:eval -- --variant <name>`
2. Deploy passing variants as canaries via the ops console or API
3. After successful canary, request governance review
4. Only then proceed with explicit promotion

### 3.5 npm run business:eval

**Purpose:** Runs the golden task evaluation corpus against the system or specific variants.

**What It Checks:**
- System performance on standardized golden tasks (20+ tasks)
- Regression detection against baseline scores
- Adversarial test resilience
- Historical replay accuracy

**How to Run:**

```bash
# Full evaluation
npm run business:eval

# Dry run (check what would be evaluated)
npm run business:eval -- --dry-run

# Evaluate specific variant
npm run business:eval -- --variant <variant_name>
```

**Interpreting Output:**

```
Evaluation run...
  Golden tasks: 24 executed
  Passed: 22/24 (91.7%)
  Regression: 0 (no score decreases vs. baseline)
  Adversarial: 5/5 passed
  Historical replay: 3/3 matched

Overall score: 0.917 (threshold: 0.850)
Status: PASSING
```

**Action on Failure:**
- Investigate individual task failures in `business/evals/golden-tasks/`
- Check for regressions by comparing to previous baseline scores
- Fix the underlying issue before promoting any variants

---

## 4. Backend Diagnostics

### 4.1 Backend Unit Tests

**Purpose:** Runs the Python unit test suite for the backend service.

**What It Checks:**
- API endpoint behavior
- Business logic correctness
- Data model integrity
- Authentication and authorization
- Tool adapter functionality

**How to Run:**

```bash
cd backend
set PYTHONPATH=.
python -m unittest discover -s app/tests/unit -p "test_*.py" -v
```

**Interpreting Output:**

A successful run:

```
test_health_ready (app.tests.unit.test_health.TestHealth) ... ok
test_login_password (app.tests.unit.test_auth.TestAuth) ... ok
test_workflow_create (app.tests.unit.test_workflows.TestWorkflows) ... ok
test_tool_effects_recorded (app.tests.unit.test_tools.TestTools) ... ok
...

----------------------------------------------------------------------
Ran 45 tests in 2.3s

OK
```

A failing run:

```
test_memory_scope_validation (app.tests.unit.test_memory.TestMemory) ... FAIL

======================================================================
FAIL: test_memory_scope_validation (app.tests.unit.test_memory.TestMemory)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "app/tests/unit/test_memory.py", line 42, in test_memory_scope_validation
    self.assertEqual(result.allowed_scopes, ["agent", "organization"])
AssertionError: Lists differ: ['agent'] != ['agent', 'organization']

----------------------------------------------------------------------
Ran 45 tests in 2.4s

FAILED (failures=1)
```

**Action on Failure:**
1. Read the test error message to understand the expected vs. actual behavior
2. Locate the source code being tested
3. Determine if the test or the implementation is wrong
4. Fix the issue and re-run the specific test:

```bash
python -m unittest app.tests.unit.test_memory.TestMemory.test_memory_scope_validation -v
```

### 4.2 Backend E2E Tests

**Purpose:** Runs end-to-end integration tests that exercise the full backend stack.

**What It Checks:**
- Full request/response cycles through the API
- Database integration
- Cross-service interactions
- Workflow execution paths

**How to Run:**

```bash
cd backend
set PYTHONPATH=.
python -m unittest discover -s app/tests/e2e -p "test_*.py" -v
```

**Prerequisites:**
- PostgreSQL must be running and accessible
- `DATABASE_URL` must be set in `backend/.env`
- The database should be in a clean state (or tests should handle setup/teardown)

**Interpreting Output:**

Similar to unit tests but with integration-level assertions:

```
test_full_workflow_execution (app.tests.e2e.test_workflow_run.TestWorkflowRun) ... ok
test_improvement_pipeline (app.tests.e2e.test_improvement.TestImprovement) ... ok
...

----------------------------------------------------------------------
Ran 12 tests in 8.7s

OK
```

**Action on Failure:**
- Ensure PostgreSQL is running and the database exists
- Check that `DATABASE_URL` is correct
- Verify PYTHONPATH is set
- Look for test isolation issues (tests depending on state from other tests)

---

## 5. Frontend Diagnostics

### 5.1 pnpm lint

**Purpose:** Runs ESLint to check code quality and style compliance.

**What It Checks:**
- JavaScript/TypeScript style violations
- Unused variables and imports
- React hooks rules compliance
- Accessibility issues (a11y)

**How to Run:**

```bash
cd frontend
pnpm lint
```

**Interpreting Output:**

A clean run produces no output (or a brief success message).

A failing run:

```
/frontend/src/components/WorkflowPanel.tsx
  12:5  error  'useState' is defined but never used  @typescript-eslint/no-unused-vars
  45:3  warning  Missing aria-label on interactive element  jsx-a11y/interactive-supports-focus

/frontend/src/pages/evolution.tsx
  8:1  error  Import 'React' is not needed in scope  react/react-in-jsx-scope

Found 2 errors and 1 warning.
```

**Action on Failure:**
- Fix reported errors in the specific files and line numbers shown
- Warnings may be acceptable but errors must be resolved
- Run `pnpm lint --fix` for auto-fixable issues

### 5.2 pnpm typecheck

**Purpose:** Runs the TypeScript compiler in check mode to verify type safety.

**What It Checks:**
- Type correctness across all TypeScript files
- Interface and type compatibility
- Missing or incorrect type assertions
- API response shape alignment (if types are generated)

**How to Run:**

```bash
cd frontend
pnpm typecheck
```

**Interpreting Output:**

Clean:

```
Done in 4.2s.
```

Failing:

```
src/hooks/useWorkflow.ts:23:5 - error TS2322: Type 'string | undefined' is not assignable to type 'string'.

src/components/AgentCard.tsx:45:9 - error TS2339: Property 'status' does not exist on type 'Agent'.

Found 2 errors in 2 files.
```

**Action on Failure:**
- If errors reference API types, regenerate with `pnpm api:generate`
- For code errors, fix the type annotations or add proper null checks
- Never use `@ts-ignore` as a permanent fix

### 5.3 pnpm test

**Purpose:** Runs the component and unit test suite (Vitest/Jest).

**What It Checks:**
- Component rendering correctness
- Hook behavior
- Utility function logic
- State management

**How to Run:**

```bash
cd frontend
pnpm test
```

**Interpreting Output:**

```
 PASS  src/components/__tests__/AgentCard.test.tsx
 PASS  src/hooks/__tests__/useWorkflow.test.ts
 FAIL  src/components/__tests__/EvolutionPanel.test.tsx
  - renders sandbox variants correctly

Tests: 1 failed, 24 passed, 25 total
Time:  3.2s
```

**Action on Failure:**
- Read the failing test to understand the expected behavior
- Check if the component implementation matches the test expectations
- Update either the test or the implementation as appropriate
- Run the specific test in watch mode for rapid iteration:

```bash
pnpm test -- --filter EvolutionPanel
```

---

## 6. Combined Diagnostic Workflow

### 6.1 Full System Diagnostic Script

For a comprehensive system check, run all diagnostics in sequence:

```bash
#!/bin/bash
echo "=== Generic Swarm Ops Full Diagnostic ==="
echo ""

echo "--- Starter Layer ---"
npm run doctor
echo ""

echo "--- Business Layer ---"
npm run business:validate
npm run business:security
npm run business:governance
npm run business:evolution:check
echo ""

echo "--- Backend ---"
cd backend
set PYTHONPATH=.
python -m unittest discover -s app/tests/unit -p "test_*.py" 2>&1 | tail -5
cd ..
echo ""

echo "--- Frontend ---"
cd frontend
pnpm lint 2>&1 | tail -5
pnpm typecheck 2>&1 | tail -5
pnpm test 2>&1 | tail -5
cd ..
echo ""

echo "=== Diagnostic Complete ==="
```

### 6.2 Quick Health Check (Daily)

For a quick daily health check, focus on the critical path:

```bash
# 1. Prerequisites still OK?
npm run doctor

# 2. Business layer valid?
npm run business:validate

# 3. Backend healthy?
curl -s http://127.0.0.1:8000/api/v1/health/ready | python -m json.tool

# 4. Frontend builds?
cd frontend && pnpm typecheck
```

### 6.3 Pre-Commit Diagnostic

Before committing changes:

```bash
# Validate business artifacts if changed
npm run business:validate
npm run business:security

# Run tests for changed layer
cd backend && set PYTHONPATH=. && python -m unittest discover -s app/tests/unit -p "test_*.py"
cd frontend && pnpm lint && pnpm typecheck && pnpm test
```

---

## 7. Real-World Use Case Examples

### Use Case 1: CI/CD Pipeline Integration

**Scenario:** Your team wants to add diagnostic checks to the CI pipeline.

**Implementation:**

```yaml
# Example CI configuration
diagnostic-checks:
  steps:
    - run: npm run doctor
    - run: npm run business:validate
    - run: npm run business:security
    - run: npm run business:governance
    - run: |
        cd backend
        export PYTHONPATH=.
        python -m unittest discover -s app/tests/unit -p "test_*.py"
    - run: |
        cd frontend
        pnpm lint
        pnpm typecheck
        pnpm test
```

**Key Consideration:** The CI environment needs all prerequisites installed. Use a Docker image that includes Node.js 20+, Python 3.11+, and pnpm, or install them in a setup step.

### Use Case 2: Post-Deployment Verification

**Scenario:** After deploying a new version, verify the system is healthy.

**Implementation:**

```bash
# 1. Health endpoint responds correctly
response=$(curl -s http://production-url/api/v1/health/ready)
echo "$response" | grep -q '"database": "postgres"' && echo "DB OK" || echo "DB FAIL"

# 2. Authentication works
token=$(curl -s -X POST http://production-url/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin-password"}' \
  | python -c "import sys,json; print(json.load(sys.stdin).get('token','FAIL'))")
echo "Auth: $token"

# 3. Core API responds
curl -s -b "gso_access_token=$token" http://production-url/api/v1/workflows | python -m json.tool | head -5
```

### Use Case 3: Investigating Intermittent Failures

**Scenario:** A workflow sometimes fails at the tool execution step.

**Investigation:**

```bash
# 1. Check audit logs for tool execution patterns
curl -s -b "gso_access_token=$token" \
  "http://127.0.0.1:8000/api/v1/audit?event_type=tool.executed&limit=50" \
  | python -c "
import sys, json
data = json.load(sys.stdin)
for entry in data:
    if entry.get('status') == 'failed':
        print(f\"FAILED: {entry['tool_name']} at {entry['timestamp']}\")
        print(f\"  Reason: {entry.get('error', 'unknown')}\")
"

# 2. Check if it correlates with specific inputs
# 3. Review tool_effects for the failing executions
# 4. Look for resource contention or timeout patterns
```

---

## 8. Best Practices

### Diagnostic Scheduling

| Frequency | Checks |
|-----------|--------|
| Every commit | `business:validate`, `business:security`, relevant test suite |
| Daily | `npm run doctor`, health endpoint, quick backend test run |
| Weekly | Full diagnostic suite including `business:eval` |
| After deployment | Health endpoint, auth, core API smoke test |
| After system updates | Full `npm run doctor` + all test suites |

### Interpreting Results

1. **Read errors from top to bottom.** Earlier errors often cause later ones.
2. **Check the exit code.** `0` means success, non-zero means failure.
3. **Look for patterns.** Multiple failures in the same category suggest a shared root cause.
4. **Compare against baseline.** If you saved a previous successful run, diff the outputs.
5. **Do not ignore warnings.** Today's warning becomes tomorrow's error.

### Automation Tips

- Store diagnostic results in a log file with timestamps for trend analysis
- Set up alerts for diagnostic failures in shared environments
- Use `--dry-run` flags (where available) for safe exploration
- Cache `npm run doctor` results and only re-run after system changes
- Run `npm test` (root level) as a quick starter layer sanity check

---

## 9. Chapter Summary

This chapter provided a comprehensive walkthrough of all diagnostic tools available in Generic Swarm Ops:

- **Starter Layer:** `npm run doctor` (prerequisites), `sources:download` (external repos), `sources:audit` (integrity)
- **Business Layer:** `business:validate` (schemas), `business:security` (scan), `business:governance` (compliance), `business:evolution:check` (promotion), `business:eval` (golden tasks)
- **Backend:** Unit tests and E2E tests via Python unittest
- **Frontend:** `pnpm lint` (quality), `pnpm typecheck` (types), `pnpm test` (components)

The key takeaway is that these tools are designed to be used together in a systematic workflow, from basic prerequisites through to comprehensive system validation.

---

## 10. Knowledge Check Quiz

Test your understanding of the diagnostic tools:

**Question 1:** What is the correct order to run diagnostics when troubleshooting a system that was working yesterday but fails today?

<details>
<summary>Answer</summary>

1. `npm run doctor` (check prerequisites have not changed)
2. `npm run business:validate` (check business artifact integrity)
3. Health endpoint check (verify backend connectivity)
4. Test suites for the specific layer showing errors

Start from the lowest layer (prerequisites) and work up to isolate where the break occurred.

</details>

**Question 2:** What four things does `npm run business:validate` check?

<details>
<summary>Answer</summary>

1. Schema compliance (artifacts match their JSON/YAML schemas)
2. Provenance (source attribution and metadata)
3. Risk-tier alignment (declared risk matches actual scope)
4. Workflow-gate integrity (prerequisite gates configured with approvals)

</details>

**Question 3:** What three categories does `npm run business:security` scan for?

<details>
<summary>Answer</summary>

1. Secrets (hardcoded API keys, passwords, tokens)
2. Unsafe permissions (overly permissive agent/workflow configurations)
3. Prompt-injection coverage gaps (missing adversarial test cases)

</details>

**Question 4:** Why must you set `PYTHONPATH=.` before running backend tests?

<details>
<summary>Answer</summary>

Python needs to resolve imports relative to the `backend/` directory. Without `PYTHONPATH=.`, the `app` package cannot be found, resulting in `ModuleNotFoundError` or `ImportError`. Setting it to `.` (current directory) tells Python to look in the backend folder for the app package.

</details>

**Question 5:** What should you do before running `pnpm api:generate` in the frontend?

<details>
<summary>Answer</summary>

Ensure the backend is running so that the OpenAPI schema is available at `http://127.0.0.1:8000/openapi.json`. The generation tool fetches the live schema from the running backend to produce TypeScript types.

</details>

**Question 6:** What is the difference between `npm run business:eval` and `npm run business:eval -- --dry-run`?

<details>
<summary>Answer</summary>

`npm run business:eval` actually executes the golden task evaluation corpus and produces scores. The `--dry-run` flag shows what would be evaluated without actually running the tasks, which is useful for verifying the evaluation configuration without consuming resources.

</details>

**Question 7:** When running `npm run business:evolution:check`, what three pieces of evidence are required for a variant to be eligible for promotion?

<details>
<summary>Answer</summary>

1. Evaluation scores above the threshold (tested against golden task corpus)
2. Canary deployment results (successful side-by-side run with no regressions)
3. Governance sign-off (human reviewer approval)

All three must be complete before a variant can be explicitly promoted from sandbox to production.

</details>
