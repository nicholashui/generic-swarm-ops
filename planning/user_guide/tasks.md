# User guide build tasks (per `create_user_guide.md`)

## Phase 1 — TOC

- [x] Design five-section TOC with 3–5 chapters each
- [x] Save `planning/user_guide/TOC.md` + `00_PLAN.md`

## Phase 2 — Markdown chapters

- [x] Write 21 section chapters + 2 appendices under `book/user_guide/chapters/`
- [x] Each chapter: objectives, prerequisites, steps, use cases, best practices, summary, quiz
- [x] Naming `NN-MM-slug.md`

## Phase 3 — SVG

- [x] One primary SVG per section chapter (21) in `book/user_guide/assets/`
- [x] Embed with relative paths; broken_embeds=0

## Phase 4 — Compile & QA

- [x] `book/user_guide/user_guide.md` master TOC
- [x] `book/user_guide/README.md` entry
- [x] Product-accurate residuals vs `EXECUTABLE_PRODUCT.md`
- [x] Real ids: E1 workflow, viral-hook DNA, special skills 17

## Generators

```powershell
python planning/user_guide/build_chapters.py
python planning/user_guide/build_chapters_rest.py
```
