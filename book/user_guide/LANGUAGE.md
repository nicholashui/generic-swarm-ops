# User guide language policy

## Rule

Every reader-facing Markdown file under `book/user_guide/` **must** exist in both:

| Language | Pattern | Example |
|----------|---------|---------|
| English | `*.md` (no `_hk` suffix) | `user_guide.md`, `chapters/05-first-workflow-run-e1.md` |
| Traditional Chinese | `*_hk.md` | `user_guide_hk.md`, `chapters/05-first-workflow-run-e1_hk.md` |

## Exceptions (shared, not translated as separate docs)

- `assets/*.svg` — shared figures (labels may stay English for product terms)
- Binary / media if any later

## Do not translate

- API paths (`/api/v1/...`)
- Workflow / agent / skill ids (`wf_video_arch_a_viral_hook_v1`)
- Env vars (`NEXT_PUBLIC_DEMO_MODE`)
- File and package paths
- HTTP methods and status codes

## Maintenance

1. Edit English chapter first (or HK first if authoring in Chinese), then sync the pair.
2. Regenerate HK scaffolds: `python planning/user_guide/_gen_hk.py`
3. Full prose: expand **both** `foo.md` and `foo_hk.md` in place under `book/user_guide/`.
4. Links inside EN docs should offer HK alternate; HK docs should link EN alternate.

## Definition of done (bilingual)

- [ ] Same chapter set EN + HK (00–19, A–C)
- [ ] Masters: `user_guide.md` + `user_guide_hk.md`
- [ ] TOCs: `TOC.md` + `TOC_hk.md`
- [ ] READMEs: `README.md` + `README_hk.md`
- [ ] Cross-links both directions
