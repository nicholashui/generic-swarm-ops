# User Guide — Complete Table of Contents

**Product:** generic-swarm-ops  
**Guide target:** `book/user_guide/user_guide.md` (assembled)  
**Scaffolds:** `planning/user_guide/chapters/`  
**Illustrations:** `planning/user_guide/assets/`

---

## Reading map

![Beginner to expert learning path](./assets/01-learning-path.svg)

| Track | Recommended path |
|-------|------------------|
| Operator | Front → Part I → Part II → Part III (08–09) → skim 06, 18 troubleshooting |
| Builder | Operator path + Part III (10) + Part IV + Part V (17) |
| Platform / SRE | Part I + II + Part V (15–18) + Appendices B–C |
| Expert | All chapters + design_phase books as advanced reference |

---

## Front matter

| Ch | Title | File | Level | SVG | Est. |
|----|-------|------|-------|-----|------|
| 00 | How to use this guide | [chapters/00-how-to-use-this-guide.md](./chapters/00-how-to-use-this-guide.md) | Beginner | 01-learning-path | 15m |

---

## Part I — Foundations (Beginner)

*Goal: mental model + running system + knowing where to click.*

| Ch | Title | File | SVG | Est. |
|----|-------|------|-----|------|
| 01 | What is generic-swarm-ops? | [chapters/01-what-is-this-system.md](./chapters/01-what-is-this-system.md) | 02-system-overview | 30m |
| 02 | Mental model and layered architecture | [chapters/02-mental-model-and-layers.md](./chapters/02-mental-model-and-layers.md) | 02-system-overview | 40m |
| 03 | Install and first boot | [chapters/03-install-and-first-boot.md](./chapters/03-install-and-first-boot.md) | 03-install-boot | 45–90m |
| 04 | Ops console tour | [chapters/04-ops-console-tour.md](./chapters/04-ops-console-tour.md) | 04-console-map | 30m |

**Part I exit criteria:** Backend ready, frontend live (demo off), logged in, Domains visible in sidebar.

---

## Part II — Operator core (Beginner → Intermediate)

*Goal: run real work with gates and audit.*

| Ch | Title | File | SVG | Est. |
|----|-------|------|-----|------|
| 05 | Your first workflow run (E1 path) | [chapters/05-first-workflow-run-e1.md](./chapters/05-first-workflow-run-e1.md) | 05-e1-operator-path | 60m |
| 06 | Approvals, risk tiers, and audit | [chapters/06-approvals-risk-audit.md](./chapters/06-approvals-risk-audit.md) | 06-governance-gates | 45m |
| 07 | Agents, tools, and RBAC | [chapters/07-agents-tools-rbac.md](./chapters/07-agents-tools-rbac.md) | 07-agents-tools | 45m |

**Part II exit criteria:** Completed onboarding run with approval; can find audit entry; understand allow-lists.

---

## Part III — Domains & video pack (Intermediate)

*Goal: use domain packs without confusing selection helpers with live media studio.*

| Ch | Title | File | SVG | Est. |
|----|-------|------|-----|------|
| 08 | Domain packs and recommend workflow | [chapters/08-domain-packs-and-recommend.md](./chapters/08-domain-packs-and-recommend.md) | 08-domain-recommend | 60m |
| 09 | Special skills catalog | [chapters/09-special-skills-catalog.md](./chapters/09-special-skills-catalog.md) | 09-special-skills | 40m |
| 10 | Workflow DNA deep dive | [chapters/10-workflow-dna-deep-dive.md](./chapters/10-workflow-dna-deep-dive.md) | 10-workflow-dna | 60m |

**Part III exit criteria:** Recommend returns `wf_video_arch_a_viral_hook_v1` class result for viral brief; 17 skills listed from live data; can read a `.dna.json`.

---

## Part IV — Intelligence & improvement (Advanced)

*Goal: knowledge, process mining, evals, evolution, closed-loop improve.*

| Ch | Title | File | SVG | Est. |
|----|-------|------|-----|------|
| 11 | Knowledge and memory | [chapters/11-knowledge-and-memory.md](./chapters/11-knowledge-and-memory.md) | 11-knowledge-memory | 50m |
| 12 | Process intelligence | [chapters/12-process-intelligence.md](./chapters/12-process-intelligence.md) | 12-pi-evolution | 45m |
| 13 | Evaluation and evolution sandbox | [chapters/13-evaluation-and-evolution.md](./chapters/13-evaluation-and-evolution.md) | 12-pi-evolution | 60m |
| 14 | Self-improvement and loops | [chapters/14-self-improvement-loops.md](./chapters/14-self-improvement-loops.md) | 13-self-improve | 50m |

**Part IV exit criteria:** Can explain Tier 0/1; open Evolution archive; run Reflect on a completed run; never promote without evaluate.

---

## Part V — Expert & production

*Goal: extend the system and run it safely.*

| Ch | Title | File | SVG | Est. |
|----|-------|------|-----|------|
| 15 | Backend runtime and APIs | [chapters/15-backend-runtime-and-apis.md](./chapters/15-backend-runtime-and-apis.md) | 02-system-overview | 75m |
| 16 | Frontend deep dive | [chapters/16-frontend-deep-dive.md](./chapters/16-frontend-deep-dive.md) | 04-console-map | 60m |
| 17 | Extend DNA, agents, and packs | [chapters/17-extend-dna-agents-packs.md](./chapters/17-extend-dna-agents-packs.md) | 14-extend-pack | 90m |
| 18 | Security, ops, and troubleshooting | [chapters/18-security-ops-troubleshooting.md](./chapters/18-security-ops-troubleshooting.md) | 15-security-production | 60m |
| 19 | Expert playbooks and checklists | [chapters/19-expert-playbooks-and-checklists.md](./chapters/19-expert-playbooks-and-checklists.md) | 01-learning-path | 40m+ |

**Part V exit criteria:** Can scaffold/extend a pack safely; production checklist complete; teach E1 + recommend to another person.

---

## Appendices

| ID | Title | File |
|----|-------|------|
| A | Glossary | [chapters/A-glossary.md](./chapters/A-glossary.md) |
| B | Commands and API cheat sheet | [chapters/B-command-and-api-cheatsheet.md](./chapters/B-command-and-api-cheatsheet.md) |
| C | Troubleshooting matrix | [chapters/C-troubleshooting-matrix.md](./chapters/C-troubleshooting-matrix.md) |

---

## Suggested lab sequence (operator intensive day)

1. Ch03 Lab A–B — boot  
2. Ch04 — console map  
3. Ch05 Lab E1-UI — flagship run  
4. Ch06 — approve + audit  
5. Ch08 Lab UI recommend  
6. Ch09 Lab special skills ×17  
7. Ch14 Lab Reflect  

---

## Cross-links to design-phase books

Use **after** Part III, not before first boot:

| Design book | When |
|-------------|------|
| `book/design_phase/book.md` | Architecture monograph |
| `book/design_phase/book.structure_hk.md` | Six-layer structure (ZH) |
| `book/design_phase/book.backend_hk.md` | Backend deep dive (ZH) |
| `book/design_phase/book.frontend_hk.md` | Frontend deep dive (ZH) |

---

## Chapter count

- Narrative chapters: **20** (00–19)  
- Appendices: **3** (A–C)  
- SVG assets: **15**  
- Total scaffold MD files: **23**
