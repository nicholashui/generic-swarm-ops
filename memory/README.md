# Memory

Project memory files for handoff, reflections, and long-lived project context.

These files are the **shared, git-backed continuity surface** across Trae IDE and Grok Build. They are not the same as Grok experimental memory (`~/.grok/memory/`) or product business memory (`business/memory/`).

## Files

| Path | Purpose |
|------|---------|
| `handoff.md` | Current progress, blockers, next steps — read at session start |
| `project.md` | Durable project conventions and decisions |
| `reflections/` | Longer retrospectives and notes |

## Discipline

1. **Session start (any harness):** read `handoff.md` and `project.md` when present.
2. **Session end / major milestone:** update `handoff.md` so the next session (Trae or Grok) can resume.
3. **Do not rely on IDE chat history** alone for cross-tool continuity.
4. Optional Grok-only recall: enable experimental memory in Grok config; still keep durable facts here for the team.

## Related

- `business/memory/` — product/domain memory with provenance (not IDE handoff)
- `migrate_to_grok_build.md` — harness migration plan
- `docs/grok.md` / `docs/trae.md` — harness workspace notes
