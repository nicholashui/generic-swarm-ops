# Plan: Detail-complete User Guide (per `create_user_guide.md`)

## Instruction source

Execute **`create_user_guide.md`** at repo root. Quality bar: beginner→expert, real product paths for **generic-swarm-ops**, no thin scaffolds.

## Output locations

| Artifact | Path |
|----------|------|
| Plan + TOC | `planning/user_guide/` |
| Published guide | `book/user_guide/` |
| Chapters | `book/user_guide/chapters/NN-MM-slug.md` |
| SVGs | `book/user_guide/assets/NN-MM-*.svg` |
| Master entry | `book/user_guide/README.md`, `book/user_guide/user_guide.md` |

## Five required sections (instruction)

1. Core System Fundamentals (Beginner)
2. Intermediate Workflows (Skill-Building)
3. Advanced Customization (Expert)
4. Troubleshooting & Support
5. Optimization & Scaling (Advanced Expert)

Each section: **3–5** subchapters with learning objectives.

## Chapter inventory (21)

See **[TOC.md](./TOC.md)** for full list, objectives, and progression.

## Per-chapter template (mandatory)

1. Title + level + estimated time  
2. Learning objectives  
3. Prerequisites  
4. Embedded SVG (`../assets/NN-MM-….svg`) with alt text  
5. Conceptual / technical explanation  
6. Numbered hands-on steps (exact commands/values)  
7. Expected outcomes  
8. UI references (`/app/...`, panel names) where relevant  
9. 2–3 real-world use cases  
10. Best practices  
11. Chapter summary  
12. Knowledge check quiz (3–5 questions + answer key)  
13. Next chapter link  

## Honesty constraints (product-accurate)

Align with `EXECUTABLE_PRODUCT.md`: claim E1, recommend/viral-hook stubs, 17 special skills catalog; do **not** claim live Sora/Veo studio, fleet true-100, or second control plane.

## Phases

| Phase | Status |
|-------|--------|
| 1 TOC design | This folder |
| 2 Markdown chapters | `book/user_guide/chapters/` |
| 3 SVG illustrations | `book/user_guide/assets/` |
| 4 Compile + QA | `user_guide.md`, link check, residual review |

## Success criteria

- [x] TOC covers all five instruction sections  
- [x] Every TOC chapter has matching `.md` + SVG embed  
- [x] Steps use real seed login, ports, workflow ids, API paths  
- [x] Cold beginner can boot and complete E1 using only the guide  
- [x] Expert chapters cover DNA, RBAC, packs, evolution, hardening  
- [x] Troubleshooting covers demoMode, Domains nav, ready degraded  
