# Generic Swarm Ops — User Guide

**Beginner → expert.** How to understand and operate this system step by step.

| | |
|--|--|
| **Location** | `book/user_guide/` (canonical) |
| **Chapters** | [`chapters/`](./chapters/) |
| **Illustrations** | [`assets/`](./assets/) |
| **Full TOC** | [`TOC.md`](./TOC.md) |
| **Writing plan** | [`../../planning/user_guide/00_PLAN.md`](../../planning/user_guide/00_PLAN.md) |
| **Traditional Chinese** | [`user_guide_hk.md`](./user_guide_hk.md) · [`TOC_hk.md`](./TOC_hk.md) |
| **Design monographs** | [`../design_phase/`](../design_phase/) |

> **Scope honesty:** Proven paths include the E1 operator run and video pack recommend / viral-hook DNA with stubs. Live media vendors and full studio are **not** claimed here — see `EXECUTABLE_PRODUCT.md`.

---

## Learning path

![Beginner to expert learning path](./assets/01-learning-path.svg)

| Track | Start here |
|-------|------------|
| **Operator** | [00](./chapters/00-how-to-use-this-guide.md) → Part I–III (through special skills) |
| **Builder** | Operator path + [10 DNA](./chapters/10-workflow-dna-deep-dive.md) + [17 Extend](./chapters/17-extend-dna-agents-packs.md) |
| **Platform / SRE** | Part I–II + [15 Backend](./chapters/15-backend-runtime-and-apis.md)–[18 Security](./chapters/18-security-ops-troubleshooting.md) |
| **Expert** | All chapters + appendices |

---

> 繁體中文版：[user_guide_hk.md](./user_guide_hk.md)

## Front matter

- [00 — How to use this guide](./chapters/00-how-to-use-this-guide.md)

## Part I — Foundations (Beginner)

- [01 — What is generic-swarm-ops?](./chapters/01-what-is-this-system.md)
- [02 — Mental model and layered architecture](./chapters/02-mental-model-and-layers.md)
- [03 — Install and first boot](./chapters/03-install-and-first-boot.md)
- [04 — Ops console tour](./chapters/04-ops-console-tour.md)

## Part II — Operator core

- [05 — Your first workflow run (E1 path)](./chapters/05-first-workflow-run-e1.md)
- [06 — Approvals, risk tiers, and audit](./chapters/06-approvals-risk-audit.md)
- [07 — Agents, tools, and RBAC](./chapters/07-agents-tools-rbac.md)

## Part III — Domains & video pack

- [08 — Domain packs and recommend workflow](./chapters/08-domain-packs-and-recommend.md)
- [09 — Special skills catalog](./chapters/09-special-skills-catalog.md)
- [10 — Workflow DNA deep dive](./chapters/10-workflow-dna-deep-dive.md)

## Part IV — Intelligence & improvement

- [11 — Knowledge and memory](./chapters/11-knowledge-and-memory.md)
- [12 — Process intelligence](./chapters/12-process-intelligence.md)
- [13 — Evaluation and evolution sandbox](./chapters/13-evaluation-and-evolution.md)
- [14 — Self-improvement and loops](./chapters/14-self-improvement-loops.md)

## Part V — Expert & production

- [15 — Backend runtime and APIs](./chapters/15-backend-runtime-and-apis.md)
- [16 — Frontend deep dive](./chapters/16-frontend-deep-dive.md)
- [17 — Extend DNA, agents, and packs](./chapters/17-extend-dna-agents-packs.md)
- [18 — Security, ops, and troubleshooting](./chapters/18-security-ops-troubleshooting.md)
- [19 — Expert playbooks and checklists](./chapters/19-expert-playbooks-and-checklists.md)

## Appendices

- [A — Glossary](./chapters/A-glossary.md)
- [B — Commands and API cheat sheet](./chapters/B-command-and-api-cheatsheet.md)
- [C — Troubleshooting matrix](./chapters/C-troubleshooting-matrix.md)

---

## System at a glance

![System overview](./assets/02-system-overview.svg)

---

## How content is maintained

1. **Canonical user guide** = this folder: `book/user_guide/`.
2. Planning / task tracking may still live under `planning/user_guide/` — do **not** treat that as the published guide.
3. When expanding scaffolds to full prose, edit files **here** under `book/user_guide/chapters/`.
4. Keep SVGs in `book/user_guide/assets/` and embed with relative paths (`../assets/...` from chapters, `./assets/...` from this master).
