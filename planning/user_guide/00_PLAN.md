# Plan: Complete User Guide (beginner → expert)

**Goal:** Produce a **detailed, complete** `user_guide.md` (assembled from chapter files) so a reader can **deeply understand** generic-swarm-ops and **use it step by step** from first boot to expert extension and production ops.

**Host product:** `C:\Project\generic-swarm-ops`  
**Design-phase books (already moved):** `book/design_phase/`  
**Canonical user guide (published here):** `book/user_guide/` — master `user_guide.md`, `chapters/`, `assets/`  
**This folder:** planning / tasks / generators only — **not** the reader-facing guide.

---

## Outcome definition

| Deliverable | Location | Done when |
|-------------|----------|-----------|
| Full TOC (stable numbering) | `book/user_guide/TOC.md` | Parts, chapters, labs, SVGs listed |
| Per-chapter files | `book/user_guide/chapters/*.md` | Objectives, outline, labs, sources, SVG embed |
| Illustrations | `book/user_guide/assets/*.svg` | Embedded in chapter MDs |
| Master entry (EN) | `book/user_guide/user_guide.md` | Links all EN chapters |
| Master entry (ZH-HK) | `book/user_guide/user_guide_hk.md` | Links all `*_hk.md` chapters |
| Language policy | `book/user_guide/LANGUAGE.md` | Every `*.md` → `*_hk.md` |
| Execution tasks | `planning/user_guide/tasks.md` | Ordered writing checklist |
| **Full prose** (next) | edit **in place** under `book/user_guide/chapters/` both EN + `_hk` | Labs verified, bilingual |

**Structure is already saved under `book/user_guide/`.**  
**Full prose** expands those chapter files in place (see tasks.md Phase B–D).

---

## Audience tracks

| Track | Start chapters | Goal |
|-------|----------------|------|
| **Operator** | 00 → 09 | Run E1, approve gates, recommend DNA, read special skills |
| **Builder / pack author** | 00 → 10, then 15–17 | Author DNA, agents, packs; prove with evals |
| **Platform / SRE** | 00 → 07, then 15–18 | Runtime, security, Postgres, troubleshooting |
| **Expert all-round** | Full 00–19 + appendices | Teach others; own promote/rollback rules |

---

## Pedagogical principles

1. **Do before theory stack** — each part ends with labs that touch the real product path.
2. **Honest scope** — always separate *executable today* (E1, viral-hook stubs, recommend/special-skills) from residuals (live media, full studio, inflated fleet 100s).
3. **One control plane** — host FastAPI runtime; domain logic stays in packs (N1).
4. **demoMode opt-in** — teach live path (`NEXT_PUBLIC_DEMO_MODE` not `true`) as default product experience.
5. **Illustrate every concept cluster** — SVG next to narrative; regenerate via `_gen_assets.py` if style changes.
6. **Design books are deep reference, not onboarding** — `book/design_phase/*` linked from advanced chapters only.

---

## Document architecture

```text
book/user_guide/              ← CANONICAL USER GUIDE (always save here)
  user_guide.md / user_guide_hk.md
  TOC.md / TOC_hk.md
  README.md / README_hk.md
  LANGUAGE.md                 ← bilingual policy
  chapters/*.md + *_hk.md     ← expand prose in place (pairs required)
  assets/*.svg                ← shared figures (not duplicated per language)

planning/user_guide/          ← plan + generators only
  00_PLAN.md
  tasks.md
  _gen_assets.py
  _gen_chapters.py
  (optional mirror of assets/chapters — not the reader source of truth)
```

Master `user_guide.md` assembly options (pick in Phase C):

- **A (recommended):** thin master with TOC linking to chapter files  
- **B:** single concatenated `user_guide.md` for export/PDF  

---

## Complete structure (summary)

See **[TOC.md](./TOC.md)** for the authoritative table of contents.

| Part | Chapters | Theme |
|------|----------|--------|
| Front | 00 | How to use the guide |
| I Foundations | 01–04 | What it is, layers, install, console tour |
| II Operator core | 05–07 | E1 run, approvals/audit, agents/tools/RBAC |
| III Domains | 08–10 | Packs, recommend, special skills, DNA |
| IV Intelligence | 11–14 | Knowledge/memory, PI, evals/evolution, loops |
| V Expert | 15–19 | Backend, frontend, extend, security, playbooks |
| Appendices | A–C | Glossary, cheatsheet, troubleshooting matrix |

---

## Illustration map

| SVG | Used in chapters |
|-----|------------------|
| `01-learning-path.svg` | 00, 19 |
| `02-system-overview.svg` | 01, 02, 15 |
| `03-install-boot.svg` | 03 |
| `04-console-map.svg` | 04, 16 |
| `05-e1-operator-path.svg` | 05 |
| `06-governance-gates.svg` | 06 |
| `07-agents-tools.svg` | 07 |
| `08-domain-recommend.svg` | 08 |
| `09-special-skills.svg` | 09 |
| `10-workflow-dna.svg` | 10 |
| `11-knowledge-memory.svg` | 11 |
| `12-pi-evolution.svg` | 12, 13 |
| `13-self-improve.svg` | 14 |
| `14-extend-pack.svg` | 17 |
| `15-security-production.svg` | 18 |

Regenerate: `python planning/user_guide/_gen_assets.py`  
Regenerate chapter scaffolds: `python planning/user_guide/_gen_chapters.py` (**overwrites** scaffold text — do not run after full prose without backup).

---

## Writing standards (Phase B)

For each chapter when expanding scaffolds to full prose:

1. **Why** (≤1 screen) → **Concepts** with SVG → **Steps** → **Expected results** → **Pitfalls** → **Next**.
2. Commands dual-noted for **PowerShell** primary (Windows host) + bash where short.
3. Every lab names the **shipped entry point** (UI route, API path, or script).
4. No hard-coded fake skill ids as if they were REGISTRY; demo path called out explicitly.
5. Cross-link `docs/*` and code paths with repo-relative paths.
6. Residual callout box when mentioning video media, production_ready, or scores.
7. **Bilingual:** ship EN `foo.md` and Traditional Chinese `foo_hk.md` together; do not leave one language stale. See `book/user_guide/LANGUAGE.md`.
8. **Do not translate** API paths, env vars, `dna_id` / skill ids, or repo paths — only narrative.

---

## Non-goals of the user guide

- Replacing `book/design_phase` architecture monographs.
- Claiming live Sora/Veo/Runway or full Discover studio.
- Re-scoring agent fleet to fake 100s.
- Second control plane / LangGraph host migration narrative as primary.

---

## Success criteria (guide complete)

- [ ] Reader with no prior context boots stack and finishes E1 using only the guide.
- [ ] Reader recommends viral-hook DNA from brief via UI and understands HiTL.
- [ ] Reader lists 17 special skills from live API/UI and opens one pack folder.
- [ ] Reader explains sandbox → evaluate → canary without mutating production DNA.
- [ ] Reader uses troubleshooting matrix to fix demoMode-on and ready-degraded.
- [ ] All chapters embed working relative SVG paths.
- [ ] Master TOC matches chapter files 1:1.
- [ ] Full Traditional Chinese set: `user_guide_hk.md`, `TOC_hk.md`, every `chapters/*_hk.md`.

---

## Dependencies / sources of truth

| Topic | Source |
|-------|--------|
| Executable claims | `EXECUTABLE_PRODUCT.md` |
| Architecture | `docs/architecture.md`, `structure.md` |
| Usage | `docs/usage.md`, `docs/installation.md` |
| E1 proof | `backend/app/tests/e2e/test_e1_operator_path.py` |
| Domains UI | `frontend/src/types/navigation.ts`, domain panels |
| Video pack | `business/video/` |
| Design depth | `book/design_phase/` |

---

## Next action after this plan

Execute **tasks.md Phase B** chapter-by-chapter full prose into `book/user_guide/`, starting with **ch00–ch05** (operator bootstrap path).
