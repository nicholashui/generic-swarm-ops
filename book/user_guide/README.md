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

Intermediate content covering workflow implementation, business process walkthroughs,
tool integration, process intelligence, and knowledge collaboration.

| Chapter | Title | Description |
|---------|-------|-------------|
| [02-01](chapters/02-01-workflow-dna-implementation.md) | Workflow DNA Implementation | Creating bounded state-graph workflows from scratch |
| [02-02](chapters/02-02-business-process-walkthroughs.md) | Business Process Walkthroughs | End-to-end workflow examples and patterns |
| [02-03](chapters/02-03-tool-adapter-integration.md) | Tool Adapter Integration | Building and configuring tool adapters |
| [02-04](chapters/02-04-process-intelligence-usage.md) | Process Intelligence Usage | Event logs, process mining, conformance, bottlenecks |
| [02-05](chapters/02-05-knowledge-memory-collaboration.md) | Knowledge & Memory Collaboration | Tiered retrieval, memory types, provenance |

**Learning objectives for Section 2:**
- Implement production-ready Workflow DNA definitions
- Walk through complete business process examples
- Integrate tool adapters with proper effect tracking
- Use process intelligence to discover real operational workflows
- Manage the tiered knowledge retrieval and collaboration system

---

### Section 3: Advanced Customization

Advanced content covering domain pack development, API integration, advanced workflow
automation, RBAC governance, and multi-domain deployment.

| Chapter | Title | Description |
|---------|-------|-------------|
| [03-01](chapters/03-01-custom-domain-pack-development.md) | Custom Domain Pack Development | Multi-domain extension, manifest schemas, inventory gates |
| [03-02](chapters/03-02-api-integration-extension.md) | API Integration & Extension | Building integrations with the REST API |
| [03-03](chapters/03-03-advanced-workflow-automation.md) | Advanced Workflow Automation | Evolution sandbox, variant generation, canary deployment |
| [03-04](chapters/03-04-rbac-governance-configuration.md) | RBAC & Governance Configuration | Risk tiers, approval policies, compliance frameworks |
| [03-05](chapters/03-05-multi-domain-white-labeling.md) | Multi-Domain & White Labeling | Domain isolation, white-label deployment, federation |

**Learning objectives for Section 3:**
- Develop and register custom domain packs for new business areas
- Integrate external systems through the REST API
- Configure advanced workflow automation with evolution sandbox
- Set up RBAC and governance policies for enterprise compliance
- Deploy multi-domain configurations with proper isolation

---

### Section 4: Troubleshooting & Support

Troubleshooting content covering common error resolution, diagnostic tools,
system health monitoring, and support resources.

| Chapter | Title | Description |
|---------|-------|-------------|
| [04-01](chapters/04-01-common-error-resolution.md) | Common Error Resolution | Bootstrap, backend, frontend, evolution error fixes |
| [04-02](chapters/04-02-diagnostic-tools-walkthrough.md) | Diagnostic Tools Walkthrough | npm run doctor, health endpoints, log analysis |
| [04-03](chapters/04-03-system-health-monitoring.md) | System Health Monitoring | Metrics, alerting, dashboards, uptime tracking |
| [04-04](chapters/04-04-support-community-resources.md) | Support & Community Resources | Documentation, community, escalation paths |

**Learning objectives for Section 4:**
- Resolve common operational errors across all system layers
- Use diagnostic tools to identify system issues quickly
- Monitor system health with appropriate metrics and alerts
- Access support resources and community channels

---

### Section 5: Optimization & Scaling

Production optimization content covering performance tuning, resource allocation,
large-scale deployment, and security hardening with maintenance.

| Chapter | Title | Description |
|---------|-------|-------------|
| [05-01](chapters/05-01-performance-tuning-strategies.md) | Performance Tuning Strategies | Database optimization, backend tuning, retrieval efficiency |
| [05-02](chapters/05-02-resource-allocation-optimization.md) | Resource Allocation & Optimization | Eval corpus budgets, memory retention, Loop Engineering |
| [05-03](chapters/05-03-large-scale-deployment.md) | Large-Scale Deployment | Horizontal scaling, domain isolation, CI/CD, Docker |
| [05-04](chapters/05-04-security-hardening-maintenance.md) | Security Hardening & Maintenance | OWASP controls, agentic security, long-term maintenance |

**Learning objectives for Section 5:**
- Tune system performance for production workloads
- Manage resource allocation and budgets across all components
- Deploy at enterprise scale with horizontal scaling and domain isolation
- Implement comprehensive security hardening with OWASP LLM Top 10 controls
- Maintain long-term system health through archival, versioning, and auditing

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
