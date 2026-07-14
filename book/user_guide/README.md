# Generic Swarm Business Operating System - User Guide

> A comprehensive, hands-on guide to deploying, operating, and optimizing the Generic Swarm
> multi-agent business operating system.

**Version:** 2.1 (Research-Integrated Edition)
**Last updated:** July 2026

---

## About This Guide

This user guide is organized into five progressive sections. Each section builds on the
knowledge from the previous one, taking you from initial installation through advanced
customization and production-scale optimization.

**Design priorities** of the system (in strict order):

1. Safety
2. Auditability
3. Correctness
4. Efficiency
5. Autonomy

> **Tip:** If you are new to Generic Swarm Ops, start with Section 1 and work through each
> chapter sequentially. Experienced operators can jump directly to the section most relevant
> to their needs.

---

## Table of Contents

### Section 1: Core System Fundamentals

Beginner-level content covering the system architecture, installation, first-time setup,
configuration, and basic navigation.

| Chapter | Title | Description |
|---------|-------|-------------|
| [01-01](chapters/01-01-system-overview.md) | System Overview | Six-layer architecture, design priorities, core concepts |
| [01-02](chapters/01-02-installation-prerequisites.md) | Installation Prerequisites | Node.js, Python, PostgreSQL, pnpm, Git setup |
| [01-03](chapters/01-03-initial-setup-wizard.md) | Initial Setup Wizard | Bootstrap, business:init, database, backend/frontend startup |
| [01-04](chapters/01-04-first-time-configuration.md) | First-Time Configuration | Seed login, agent setup, first Workflow DNA, validation |
| [01-05](chapters/01-05-basic-navigation-account-management.md) | Basic Navigation & Account Management | Ops console walkthrough, RBAC, session management |

**Learning objectives for Section 1:**
- Understand the six-layer architecture and design priorities
- Install all prerequisites on your platform
- Complete the initial bootstrap and database setup
- Configure the system for first use
- Navigate the ops console and manage user accounts

---

### Section 2: Intermediate Workflows

Intermediate content covering workflow creation, agent configuration, human-in-the-loop
patterns, knowledge management, and process intelligence.

| Chapter | Title | Description |
|---------|-------|-------------|
| [02-01](chapters/02-01-workflow-dna-authoring.md) | Workflow DNA Authoring | Creating bounded state-graph workflows from scratch |
| [02-02](chapters/02-02-agent-configuration.md) | Agent Configuration & Roles | Agent roster, role assignment, tool permissions |
| [02-03](chapters/02-03-human-gates-approvals.md) | Human Gates & Approvals | Risk tiers, approval policies, gate configuration |
| [02-04](chapters/02-04-knowledge-memory-management.md) | Knowledge & Memory Management | Tiered retrieval, memory types, provenance |
| [02-05](chapters/02-05-process-intelligence.md) | Process Intelligence | Event logs, process mining, conformance, bottlenecks |

**Learning objectives for Section 2:**
- Author production-ready Workflow DNA definitions
- Configure agents with appropriate roles and tool permissions
- Implement human-in-the-loop approval gates
- Manage the tiered knowledge retrieval system
- Use process intelligence to discover real operational workflows

---

### Section 3: Advanced Customization

Advanced content covering the evolution sandbox, evaluation harness, domain packs,
custom tool adapters, and self-improvement loops.

| Chapter | Title | Description |
|---------|-------|-------------|
| [03-01](chapters/03-01-evolution-sandbox.md) | Evolution Sandbox | Variant generation, fitness functions, canary deployment |
| [03-02](chapters/03-02-evaluation-harness.md) | Evaluation Harness & Corpus | Golden tasks, regression, adversarial, replay testing |
| [03-03](chapters/03-03-domain-packs.md) | Domain Packs | Multi-domain extension, manifest schemas, inventory gates |
| [03-04](chapters/03-04-custom-tool-adapters.md) | Custom Tool Adapters | Building adapters, tool_effects, permission broker |
| [03-05](chapters/03-05-self-improvement-loops.md) | Self-Improvement Loops | Reflect, propose, evaluate, canary pipeline |

**Learning objectives for Section 3:**
- Operate the evolution sandbox safely with production guardrails
- Build and maintain comprehensive evaluation test suites
- Create and register domain packs for new business areas
- Develop custom tool adapters with proper effect tracking
- Configure and monitor self-improvement feedback loops

---

### Section 4: Troubleshooting & Support

Troubleshooting content covering common issues, diagnostic tools, incident response,
and recovery procedures.

| Chapter | Title | Description |
|---------|-------|-------------|
| [04-01](chapters/04-01-diagnostic-commands.md) | Diagnostic Commands | npm run doctor, health endpoints, log analysis |
| [04-02](chapters/04-02-common-issues.md) | Common Issues & Solutions | Database connectivity, auth failures, sync errors |
| [04-03](chapters/04-03-incident-response.md) | Incident Response | Runbooks, rollback procedures, postmortem templates |
| [04-04](chapters/04-04-recovery-procedures.md) | Recovery Procedures | Data recovery, state reset, backup restoration |

**Learning objectives for Section 4:**
- Use diagnostic commands to identify system issues
- Resolve common operational problems quickly
- Follow incident response runbooks during failures
- Execute recovery procedures to restore system state

---

### Section 5: Optimization & Scaling

Production optimization content covering performance tuning, monitoring, scaling
strategies, and governance compliance.

| Chapter | Title | Description |
|---------|-------|-------------|
| [05-01](chapters/05-01-performance-tuning.md) | Performance Tuning | Database optimization, caching, retrieval efficiency |
| [05-02](chapters/05-02-monitoring-observability.md) | Monitoring & Observability | Audit trails, metrics, alerting, dashboards |
| [05-03](chapters/05-03-scaling-strategies.md) | Scaling Strategies | Horizontal scaling, multi-tenant, high availability |
| [05-04](chapters/05-04-governance-compliance.md) | Governance & Compliance | NIST AI RMF, ISO 42001, EU AI Act, audit readiness |

**Learning objectives for Section 5:**
- Tune system performance for production workloads
- Implement comprehensive monitoring and observability
- Scale the system for enterprise deployments
- Maintain governance compliance with regulatory frameworks

---

## Prerequisites

Before starting this guide, ensure you have:

- Basic familiarity with command-line interfaces
- Understanding of REST APIs and JSON
- Access to a development machine (Windows, macOS, or Linux)
- At least 8 GB of RAM and 20 GB free disk space

## Conventions Used

Throughout this guide, the following conventions are used:

| Convention | Meaning |
|------------|---------|
| `monospace` | Commands, file paths, code, or configuration values |
| **Bold** | Important terms or UI elements |
| > **Tip:** | Helpful suggestions and shortcuts |
| > **Warning:** | Actions that could cause problems if not followed carefully |
| > **Note:** | Additional context or clarification |

## Quick Reference

| Resource | Location |
|----------|----------|
| System architecture | `structure.md` (repo root) |
| Installation docs | `docs/installation.md` |
| Usage reference | `docs/usage.md` |
| Backend API | `http://127.0.0.1:8000/api/v1/` |
| Frontend console | `http://localhost:3000/` |
| Health check | `GET /api/v1/health/ready` |
| Business artifacts | `business/` directory |

---

*This guide is part of the Generic Swarm Business Operating System documentation suite.*
*For architecture details, see `structure.md`. For design rationale, see `book/design_phase/`.*
