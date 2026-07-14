# Chapter 01-02: Installation Prerequisites

![Installation Flow](../assets/01-02-installation-flow.svg)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Identify all required and optional dependencies for the Generic Swarm Business OS
2. Install Node.js 20+, Python 3.11+, PostgreSQL 14+, pnpm, and Git on your platform
3. Verify each prerequisite is correctly installed and accessible
4. Understand the role of optional dependencies (Neo4j, pgvector, LLM APIs)
5. Configure system environment variables for both development and production use
6. Troubleshoot common installation issues on Windows, macOS, and Linux

## Prerequisites

- A development machine running Windows 10+, macOS 12+, or a modern Linux distribution
- Administrator/sudo access for installing system packages
- At least 8 GB of RAM (16 GB recommended)
- At least 20 GB of free disk space
- A stable internet connection for downloading packages

---

## 1. Required Dependencies Overview

The Generic Swarm Business OS requires five core dependencies:

| Dependency | Minimum Version | Purpose |
|-----------|----------------|---------|
| **Node.js** | 20.0+ | Orchestration scripts, bootstrap, business commands |
| **npm** | 10.0+ | Package management (bundled with Node.js) |
| **Python** | 3.11+ | Backend runtime (FastAPI, agents, tools) |
| **PostgreSQL** | 14+ | Primary runtime store (JSONB documents) |
| **pnpm** | 8.0+ | Frontend package management |
| **Git** | 2.30+ | Version control, repository operations |

> **Note:** The system uses Node.js for orchestration scripts (`npm run bootstrap`,
> `npm run business:*`) and Python for the FastAPI backend. Both are required for a
> complete installation.

---

## 2. Installing Node.js 20+

Node.js provides the runtime for all orchestration scripts, including the bootstrap
process, business layer commands, and the dual-harness sync.

### 2.1 Windows Installation

```bash
# Option A: Download from official site
# Visit https://nodejs.org/ and download the LTS installer (v20+)

# Option B: Using winget (Windows Package Manager)
winget install OpenJS.NodeJS.LTS

# Option C: Using Chocolatey
choco install nodejs-lts
```

### 2.2 macOS Installation

```bash
# Option A: Using Homebrew (recommended)
brew install node@20

# Option B: Using nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20
nvm use 20
```

### 2.3 Linux Installation (Ubuntu/Debian)

```bash
# Using NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version   # Should show v20.x.x
npm --version    # Should show 10.x.x
```

### 2.4 Linux Installation (Fedora/RHEL)

```bash
# Using NodeSource repository
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo dnf install -y nodejs

# Verify
node --version
npm --version
```

### 2.5 Verification

```bash
# Verify Node.js version (must be 20+)
node --version
# Expected: v20.x.x or higher

# Verify npm version
npm --version
# Expected: 10.x.x or higher

# Quick functionality test
node -e "console.log('Node.js is working:', process.version)"
```

> **Warning:** Node.js versions below 20 are not supported. The orchestration scripts
> use features (such as native fetch and structured clone) that require Node.js 20+.

---

## 3. Installing Python 3.11+

Python powers the entire backend runtime, including the FastAPI application, agent
execution engine, tool adapters, and all infrastructure services.

### 3.1 Windows Installation

```bash
# Option A: Download from official site
# Visit https://www.python.org/downloads/ and download Python 3.11+

# Option B: Using winget
winget install Python.Python.3.11

# Option C: Using Chocolatey
choco install python --version=3.11
```

> **Tip:** During Windows installation, check "Add Python to PATH" and "Install pip"
> options in the installer wizard.

### 3.2 macOS Installation

```bash
# Using Homebrew (recommended)
brew install python@3.11

# Verify the correct version is active
python3 --version
# Expected: Python 3.11.x or higher

# If you have multiple versions, create an alias
alias python=python3.11
```

### 3.3 Linux Installation (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python 3.11 and development tools
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Set as default (if needed)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Verify
python3 --version
# Expected: Python 3.11.x or higher
```

### 3.4 Linux Installation (Fedora/RHEL)

```bash
# Fedora (usually has Python 3.11+ by default)
sudo dnf install -y python3.11 python3-pip python3-devel

# Verify
python3 --version
```

### 3.5 Virtual Environment (Recommended)

While not strictly required (the backend uses `pip install -e .`), using a virtual
environment keeps your system Python clean:

```bash
# Create a virtual environment
python3 -m venv ~/.venvs/generic-swarm-ops

# Activate it
# Linux/macOS:
source ~/.venvs/generic-swarm-ops/bin/activate
# Windows:
~\.venvs\generic-swarm-ops\Scripts\activate

# Verify
which python  # Should point to the venv
python --version
```

### 3.6 Verification

```bash
# Check version
python3 --version
# Expected: Python 3.11.x or higher

# Check pip
pip3 --version
# Expected: pip 23.x or higher

# Quick functionality test
python3 -c "import sys; print(f'Python {sys.version} is working')"
```

---

## 4. Installing PostgreSQL 14+

PostgreSQL is the primary runtime store for the Business Orchestrator. All workflow state,
agent state, run history, and audit logs are persisted in a `runtime_state` table using
JSONB documents.

### 4.1 Windows Installation

```bash
# Option A: Download installer from https://www.postgresql.org/download/windows/

# Option B: Using Chocolatey
choco install postgresql14

# Option C: Using Docker (recommended for development)
docker run --name gso-postgres -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_DB=generic_swarm_ops -p 5432:5432 -d postgres:14
```

### 4.2 macOS Installation

```bash
# Using Homebrew (recommended)
brew install postgresql@14

# Start the service
brew services start postgresql@14

# Create the database
createdb generic_swarm_ops

# Verify connection
psql generic_swarm_ops -c "SELECT version();"
```

### 4.3 Linux Installation (Ubuntu/Debian)

```bash
# Install PostgreSQL 14
sudo apt update
sudo apt install -y postgresql-14 postgresql-client-14

# Start the service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create user and database
sudo -u postgres createuser --interactive
# Enter name of role to add: your_username
# Shall the new role be a superuser? y

sudo -u postgres createdb generic_swarm_ops

# Verify
psql generic_swarm_ops -c "SELECT version();"
```

### 4.4 Linux Installation (Fedora/RHEL)

```bash
# Install PostgreSQL
sudo dnf install -y postgresql-server postgresql

# Initialize database
sudo postgresql-setup --initdb

# Start and enable
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database
sudo -u postgres createdb generic_swarm_ops
```

### 4.5 Docker Installation (All Platforms)

For development, Docker provides the simplest setup:

```bash
# Pull and run PostgreSQL 14
docker run --name gso-postgres \
  -e POSTGRES_USER=gso_user \
  -e POSTGRES_PASSWORD=gso_password \
  -e POSTGRES_DB=generic_swarm_ops \
  -p 5432:5432 \
  -d postgres:14

# Verify it's running
docker ps | grep gso-postgres

# Test connection
psql postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops \
  -c "SELECT 1;"
```

### 4.6 Database Configuration

After installation, configure the connection in `backend/.env`:

```bash
# backend/.env
DATABASE_URL=postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops
```

> **Tip:** See `backend/docs/postgres-runbook.md` for detailed operational guidance
> on Postgres management, backups, and troubleshooting.

### 4.7 Verification

```bash
# Check PostgreSQL version
psql --version
# Expected: psql (PostgreSQL) 14.x or higher

# Test database connectivity
psql postgresql://localhost:5432/generic_swarm_ops -c "SELECT current_database();"
# Expected: generic_swarm_ops
```

---

## 5. Installing pnpm

pnpm is the package manager for the Next.js frontend console. It is faster and more
disk-efficient than npm for frontend projects.

### 5.1 Using Corepack (Recommended)

Corepack is bundled with Node.js 16+ and is the recommended way to manage pnpm:

```bash
# Enable corepack (may require sudo on Linux)
corepack enable

# Verify pnpm is available
pnpm --version
# Expected: 8.x.x or higher
```

### 5.2 Standalone Installation

If corepack is not available or you prefer a standalone install:

```bash
# Using npm
npm install -g pnpm

# Using curl (Linux/macOS)
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Using PowerShell (Windows)
iwr https://get.pnpm.io/install.ps1 -useb | iex
```

### 5.3 Verification

```bash
# Check version
pnpm --version
# Expected: 8.x.x or higher

# Test functionality
pnpm --help
```

> **Note:** The frontend uses pnpm exclusively. Do not use npm or yarn for frontend
> dependency management, as the lockfile format is pnpm-specific.

---

## 6. Installing Git

Git is required for version control, the dual-harness sync, and repository operations.

### 6.1 Windows Installation

```bash
# Option A: Download from https://git-scm.com/download/win

# Option B: Using winget
winget install Git.Git

# Option C: Using Chocolatey
choco install git
```

### 6.2 macOS Installation

```bash
# macOS includes Git via Xcode Command Line Tools
xcode-select --install

# Or using Homebrew
brew install git
```

### 6.3 Linux Installation

```bash
# Ubuntu/Debian
sudo apt install -y git

# Fedora/RHEL
sudo dnf install -y git
```

### 6.4 Verification

```bash
# Check version
git --version
# Expected: git version 2.30+ or higher

# Verify configuration
git config --global user.name
git config --global user.email
```

---

## 7. Optional Dependencies

These dependencies enable advanced features but are not required for basic operation.

### 7.1 Neo4j (Graph Federation)

Neo4j enables the knowledge graph federation feature, allowing multi-hop entity queries
and relationship visualization.

```bash
# Docker installation (recommended)
docker run --name gso-neo4j \
  -e NEO4J_AUTH=neo4j/your_password \
  -p 7474:7474 -p 7687:7687 \
  -d neo4j:5

# Configure in backend/.env
# NEO4J_URI=bolt://localhost:7687
```

**When to install:** Only needed if you plan to use Tier 1 knowledge retrieval with
full graph federation (the `POST /api/v1/knowledge/graph/federate` endpoint).

### 7.2 pgvector (Embedding Search)

pgvector adds vector similarity search to PostgreSQL, enabling semantic retrieval
in the Tier 0 knowledge layer.

```bash
# If using Docker PostgreSQL, use the pgvector image instead:
docker run --name gso-postgres \
  -e POSTGRES_USER=gso_user \
  -e POSTGRES_PASSWORD=gso_password \
  -e POSTGRES_DB=generic_swarm_ops \
  -p 5432:5432 \
  -d pgvector/pgvector:pg14

# Enable the extension
psql generic_swarm_ops -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

**Environment variable:**
```bash
GENERIC_SWARM_PGVECTOR_ENABLED=true
GENERIC_SWARM_EMBEDDINGS_ENABLED=true
```

### 7.3 LLM API Access (Optional Critic)

The optional LLM critic provides AI-powered evaluation of workflow outputs:

```bash
# Enable the critic in environment
GENERIC_SWARM_LLM_CRITIC_ENABLED=true

# Configure your LLM API key (provider-specific)
# LLM_API_KEY=your_api_key_here
```

**When to install:** Only needed if you want AI-powered evaluation feedback during
the self-improvement pipeline.

---

## 8. Environment Variables Reference

The complete set of environment variables used by the system:

### 8.1 Required Variables

| Variable | Location | Value |
|----------|----------|-------|
| `DATABASE_URL` | `backend/.env` | `postgresql://user:pass@localhost:5432/generic_swarm_ops` |
| `PYTHONPATH` | Backend shell | `.` (current directory) |
| `NEXT_PUBLIC_DEMO_MODE` | Frontend shell | `false` (for live ops) |
| `NEXT_PUBLIC_API_BASE_URL` | Frontend shell | `http://127.0.0.1:8000/api/v1` |

### 8.2 Optional Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `GENERIC_SWARM_AUTO_REFLECT` | `true` | Auto-reflect on terminal runs |
| `GENERIC_SWARM_LLM_CRITIC_ENABLED` | `false` | Optional LLM critic for evaluation |
| `GENERIC_SWARM_EMBEDDINGS_ENABLED` | `false` | Enable embedding-based retrieval |
| `GENERIC_SWARM_PGVECTOR_ENABLED` | `false` | Enable pgvector extension |
| `NEO4J_URI` | (unset) | Optional graph federation endpoint |

> **Tip:** The `backend/.env.example` file contains a template with all available
> environment variables and their documentation.

---

## 9. System Requirements Validation

### Step 1: Run the Full Prerequisite Check

After installing all dependencies, verify them in sequence:

```bash
# 1. Node.js
node --version          # Must be >= 20.0.0
npm --version           # Must be >= 10.0.0

# 2. Python
python3 --version       # Must be >= 3.11.0
pip3 --version          # Must be available

# 3. PostgreSQL
psql --version          # Must be >= 14.0

# 4. pnpm
pnpm --version          # Must be >= 8.0.0

# 5. Git
git --version           # Must be >= 2.30
```

### Step 2: Verify Database Connectivity

```bash
# Test PostgreSQL connection
psql postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops \
  -c "SELECT current_database(), version();"
```

### Step 3: Clone the Repository (If Not Already Done)

```bash
# Clone the repository
git clone https://github.com/your-org/generic-swarm-ops.git
cd generic-swarm-ops

# Verify the structure
ls structure.md docs/ business/ backend/ frontend/
```

### Step 4: Run the Doctor Command

After installation, the built-in doctor command checks your environment:

```bash
# Run the system doctor
npm run doctor
```

This command validates that all required dependencies are present and correctly
configured.

---

## 10. Platform-Specific Notes

### 10.1 Windows Notes

- Use PowerShell or Windows Terminal (not cmd.exe) for all commands
- Environment variables are set with `set VARIABLE=value` (no `export`)
- Path separators use backslash (`\`), but most commands accept forward slash
- Docker Desktop is recommended for PostgreSQL and Neo4j

```bash
# Windows environment variable syntax
set PYTHONPATH=.
set NEXT_PUBLIC_DEMO_MODE=false
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

### 10.2 macOS Notes

- Install Xcode Command Line Tools first: `xcode-select --install`
- Homebrew (`brew`) is the recommended package manager
- PostgreSQL via Homebrew uses `brew services` for lifecycle management
- Add `export PATH="/usr/local/opt/python@3.11/bin:$PATH"` if needed

### 10.3 Linux Notes

- Use your distribution's package manager for system packages
- Consider using Docker for database services to avoid version conflicts
- Ensure `python3` points to Python 3.11+ (use `update-alternatives` if needed)
- `sudo` may be required for service management (`systemctl`)

---

## 11. Real-World Use Cases

### Use Case 1: Enterprise Development Team Setup

**Scenario:** A team of 10 developers needs to set up the system on standardized
development machines (Ubuntu 22.04 workstations).

**Approach:**
1. Create a setup script that installs all prerequisites via apt and Docker
2. Use Docker Compose for PostgreSQL and Neo4j services
3. Pin specific versions in the script for reproducibility
4. Store environment variables in a shared `.env.example` template

```bash
#!/bin/bash
# team-setup.sh - Enterprise team prerequisite installation
set -e

echo "Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

echo "Installing Python 3.11..."
sudo apt install -y python3.11 python3.11-venv python3-pip

echo "Installing Git..."
sudo apt install -y git

echo "Enabling pnpm via corepack..."
corepack enable

echo "Starting PostgreSQL via Docker..."
docker run --name gso-postgres \
  -e POSTGRES_USER=gso_user \
  -e POSTGRES_PASSWORD=gso_password \
  -e POSTGRES_DB=generic_swarm_ops \
  -p 5432:5432 -d postgres:14

echo "All prerequisites installed. Run 'npm run doctor' to verify."
```

### Use Case 2: CI/CD Pipeline Setup

**Scenario:** Setting up prerequisites in a CI/CD pipeline (GitHub Actions) for
automated testing.

**Approach:**
```yaml
# .github/workflows/test.yml excerpt
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_USER: gso_user
          POSTGRES_PASSWORD: gso_password
          POSTGRES_DB: generic_swarm_ops
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: corepack enable
      - run: npm run bootstrap
```

### Use Case 3: Local Development with Docker Compose

**Scenario:** A developer wants to run all services locally with minimal manual setup.

**Approach:**
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg14
    environment:
      POSTGRES_USER: gso_user
      POSTGRES_PASSWORD: gso_password
      POSTGRES_DB: generic_swarm_ops
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  neo4j:
    image: neo4j:5
    environment:
      NEO4J_AUTH: neo4j/gso_password
    ports:
      - "7474:7474"
      - "7687:7687"

volumes:
  pgdata:
```

```bash
# Start all services
docker compose -f docker-compose.dev.yml up -d

# Configure backend/.env
echo "DATABASE_URL=postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops" > backend/.env
```

---

## 12. Troubleshooting Installation Issues

### Common Issue: Node.js Version Too Old

**Symptom:** `npm run bootstrap` fails with syntax errors or "unexpected token" messages.

**Fix:**
```bash
# Check version
node --version
# If below v20, upgrade:
nvm install 20 && nvm use 20
# Or reinstall from NodeSource
```

### Common Issue: Python Not Found

**Symptom:** `python` command not found, or points to Python 2.x.

**Fix:**
```bash
# Check what's available
which python3
python3 --version

# Create alias if needed
alias python=python3

# Or use update-alternatives (Linux)
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
```

### Common Issue: PostgreSQL Connection Refused

**Symptom:** Backend fails to start with "connection refused" to port 5432.

**Fix:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql
# Or for Docker:
docker ps | grep postgres

# Start if needed
sudo systemctl start postgresql
# Or:
docker start gso-postgres

# Verify connectivity
psql postgresql://localhost:5432/generic_swarm_ops -c "SELECT 1;"
```

### Common Issue: pnpm Not Recognized

**Symptom:** `pnpm: command not found` after installation.

**Fix:**
```bash
# Re-enable corepack
corepack enable

# Or install globally
npm install -g pnpm

# Verify
pnpm --version
```

### Common Issue: Permission Denied

**Symptom:** Installation commands fail with "EACCES" or "Permission denied".

**Fix:**
```bash
# Never use sudo with npm install -g (configure npm prefix instead)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# Add to shell profile
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
```

---

## 13. Best Practices

1. **Use exact versions** -- Pin Node.js and Python to specific major versions to avoid
   compatibility issues across team members.

2. **Docker for databases** -- Use Docker for PostgreSQL (and optionally Neo4j) in
   development. It avoids version conflicts and makes cleanup simple.

3. **Virtual environments for Python** -- Even though the backend uses `pip install -e .`,
   a virtual environment prevents polluting your system Python.

4. **Check `.env.example`** -- The `backend/.env.example` file documents all available
   environment variables. Copy it to `backend/.env` and customize.

5. **Run `npm run doctor`** -- After any installation change, run the doctor command
   to verify your environment is correctly configured.

6. **Keep Git updated** -- Some dual-harness features require Git 2.30+ for sparse
   checkout and other modern features.

7. **Allocate sufficient resources** -- The system requires at least 8 GB RAM. If
   running Docker containers locally alongside the app, 16 GB is recommended.

---

## 14. Chapter Summary

In this chapter, you learned:

- The system requires Node.js 20+, Python 3.11+, PostgreSQL 14+, pnpm 8+, and Git 2.30+
- Each dependency can be installed on Windows, macOS, and Linux using platform-specific
  package managers
- PostgreSQL is the primary runtime store, and Docker is the recommended approach for
  development environments
- Optional dependencies (Neo4j, pgvector, LLM APIs) enable advanced features but are not
  required for basic operation
- Environment variables control system behavior, with `DATABASE_URL` and
  `NEXT_PUBLIC_DEMO_MODE` being the most critical
- The `npm run doctor` command validates your complete installation
- Common issues (wrong versions, connection failures, permission errors) have straightforward
  solutions documented above

---

## 15. Knowledge Check Quiz

Test your understanding of the installation prerequisites:

**Question 1:** What is the minimum required version of Node.js for the system?

a) Node.js 16
b) Node.js 18
c) Node.js 20
d) Node.js 22

<details>
<summary>Answer</summary>
<b>c)</b> Node.js 20+. The orchestration scripts use features that require this version.
</details>

---

**Question 2:** What is the recommended way to install pnpm?

a) npm install -g pnpm
b) corepack enable
c) brew install pnpm
d) apt install pnpm

<details>
<summary>Answer</summary>
<b>b)</b> corepack enable. Corepack is bundled with Node.js 16+ and provides managed
access to pnpm without global installs.
</details>

---

**Question 3:** Which database table does the Business Orchestrator use for state storage?

a) `workflow_state`
b) `runtime_state`
c) `agent_registry`
d) `orchestrator_state`

<details>
<summary>Answer</summary>
<b>b)</b> The <code>runtime_state</code> table uses JSONB documents to store all
orchestrator state, with a JSON file backup at <code>backend/data/runtime.json</code>.
</details>

---

**Question 4:** What environment variable controls whether the frontend connects to a
live backend API?

a) `API_MODE`
b) `NEXT_PUBLIC_DEMO_MODE`
c) `FRONTEND_LIVE`
d) `GSO_LIVE_API`

<details>
<summary>Answer</summary>
<b>b)</b> <code>NEXT_PUBLIC_DEMO_MODE=false</code> puts the frontend in ops mode,
connecting to the live backend API specified by <code>NEXT_PUBLIC_API_BASE_URL</code>.
</details>

---

**Question 5:** When is Neo4j required?

a) Always -- it is a core dependency
b) Only for Tier 1 knowledge retrieval with full graph federation
c) Only for the frontend console
d) Only for running evaluations

<details>
<summary>Answer</summary>
<b>b)</b> Neo4j is optional and only needed for Tier 1 knowledge retrieval with full
graph federation (the <code>POST /api/v1/knowledge/graph/federate</code> endpoint).
The system functions without it using the K1-lite graph operators.
</details>

---

**Question 6:** What command verifies that all prerequisites are correctly installed?

a) `npm run verify`
b) `npm run check`
c) `npm run doctor`
d) `npm run test`

<details>
<summary>Answer</summary>
<b>c)</b> <code>npm run doctor</code> validates that all required dependencies are
present and correctly configured.
</details>

---

**Question 7:** What is the recommended approach for PostgreSQL in development?

a) Install natively via package manager
b) Use a managed cloud service
c) Use Docker
d) Use SQLite instead

<details>
<summary>Answer</summary>
<b>c)</b> Docker is recommended for development because it avoids version conflicts,
makes cleanup simple, and allows easy use of extensions like pgvector.
</details>

---

## Next Chapter

Continue to [Chapter 01-03: Initial Setup Wizard](01-03-initial-setup-wizard.md) to
walk through the complete bootstrap and startup process.
