# User Guide — Complete Table of Contents

**Product:** generic-swarm-ops  
**Published:** `book/user_guide/`  
**Naming:** `NN-MM-slug.md` + `assets/NN-MM-….svg`

---

## Reading path

| If you are… | Start at | Through |
|-------------|----------|---------|
| New operator | §1 | §2 |
| Building packs / DNA | §1–2 | §3 |
| Platform / SRE | §1 + §4–5 | all |
| Expert mastery | Full guide | quizzes + labs |

---

## Section 1 — Core System Fundamentals (Beginner)

| ID | Chapter | File | Learning objectives |
|----|---------|------|---------------------|
| 1.1 | System overview | `01-01-system-overview.md` | Explain four planes; name core nouns; state N1 and honesty bar |
| 1.2 | Prerequisites & environment | `01-02-prerequisites-and-environment.md` | Install toolchain; verify versions |
| 1.3 | Install, bootstrap & first boot | `01-03-install-bootstrap-first-boot.md` | Bootstrap; run backend health; run frontend live |
| 1.4 | Ops console navigation | `01-04-ops-console-navigation.md` | Use sidebar groups; open Domains; know route map |
| 1.5 | Accounts, login & session | `01-05-accounts-login-and-session.md` | Login with seed user; understand session/token; demoMode effect |

**Exit §1:** Logged into live ops console with backend ready.

---

## Section 2 — Intermediate Workflows (Skill-Building)

| ID | Chapter | File | Learning objectives |
|----|---------|------|---------------------|
| 2.1 | Agents & tools | `02-01-agents-and-tools.md` | Create/inspect agents; explain allow-lists; list tools |
| 2.2 | First workflow run (E1) | `02-02-first-workflow-run-e1.md` | Complete E1 path with case_id and approval |
| 2.3 | Approvals, risk & audit | `02-03-approvals-risk-and-audit.md` | Decide gates; find audit evidence; map R3+ |
| 2.4 | Domain packs: recommend & special skills | `02-04-domains-recommend-and-special-skills.md` | Recommend DNA from brief; list 17 skills from REGISTRY |
| 2.5 | Knowledge, memory & process basics | `02-05-knowledge-memory-and-processes.md` | Use Knowledge/Memory/Processes surfaces; tiered retrieval idea |

**Exit §2:** Can run ops day path: run → approve → recommend → inspect catalog.

---

## Section 3 — Advanced Customization (Expert)

| ID | Chapter | File | Learning objectives |
|----|---------|------|---------------------|
| 3.1 | Workflow DNA deep dive | `03-01-workflow-dna-deep-dive.md` | Read/author DNA fields; place human gates |
| 3.2 | Backend API integration | `03-02-backend-api-integration.md` | Auth + call core APIs with request_id awareness |
| 3.3 | RBAC & permission-aware UI | `03-03-rbac-and-permissions.md` | Map roles to permissions; secure surfaces |
| 3.4 | Extending with domain packs | `03-04-extending-domain-packs.md` | Scaffold pack; inventory; avoid second control plane |
| 3.5 | Improve pipeline, loops & evolution | `03-05-improve-loops-and-evolution.md` | Reflect→propose→evaluate→canary; sandbox rules |

**Exit §3:** Can extend safely and improve without mutating production DNA in place.

---

## Section 4 — Troubleshooting & Support

| ID | Chapter | File | Learning objectives |
|----|---------|------|---------------------|
| 4.1 | Common errors & fixes | `04-01-common-errors-and-fixes.md` | Resolve top failure modes with a matrix |
| 4.2 | Health, doctor & diagnostics | `04-02-health-doctor-and-diagnostics.md` | Use health endpoints and npm doctor |
| 4.3 | Support paths & evidence packs | `04-03-support-paths-and-evidence.md` | Collect logs, request_id, versions for support |

**Exit §4:** Self-serve recovery for boot, auth, demoMode, and run failures.

---

## Section 5 — Optimization & Scaling (Advanced Expert)

| ID | Chapter | File | Learning objectives |
|----|---------|------|---------------------|
| 5.1 | Performance & Postgres ops | `05-01-performance-and-postgres.md` | Prefer Postgres primary; tune local ops |
| 5.2 | Security hardening | `05-02-security-hardening.md` | Hardening checklist beyond seed demos |
| 5.3 | Deployment, scale & maintenance | `05-03-deployment-scale-and-maintenance.md` | Long-term ops playbook; promote discipline |

**Exit §5:** Production-minded checklist complete.

---

## Appendices (compiled into master)

| ID | Topic | File |
|----|-------|------|
| A | Glossary | `99-01-glossary.md` |
| B | Command & API cheat sheet | `99-02-command-api-cheatsheet.md` |

---

## Chapter count

- Section chapters: **21** (5+5+5+3+3)  
- Appendices: **2**  
- Total MD content files: **23** + README + user_guide.md + TOC  
- SVGs: **one primary illustration per section chapter** (21) + optional overview  
