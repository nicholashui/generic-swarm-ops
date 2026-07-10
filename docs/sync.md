# Sync

The sync layer generates harness-facing files for **Trae IDE** and **Grok Build** from shared sources (`rules/`, `skills/`, `hooks/`, `mcp-configs/`) and the adapter roster in `scripts/adapters/shared.mjs`.

## Commands

```bash
npm run sync           # write all managed outputs
npm run sync -- --dry-run
npm run sync:check     # verify managed files exist
```

## Adapters

| Adapter | Module | Outputs |
|---------|--------|---------|
| Shared | `scripts/adapters/shared.mjs` | Agent roster, commands, skill map, agent rules |
| Trae | `scripts/adapters/trae.mjs` | `AGENTS.md`, `docs/agents.md`, `docs/trae.md`, `.trae/*` |
| Grok | `scripts/adapters/grok.mjs` | `docs/grok.md`, `.grok/*` |

## Generated Outputs

### Shared / docs

- `AGENTS.md`
- `docs/agents.md`
- `docs/trae.md`
- `docs/grok.md`

### Trae (`.trae/`)

- `.trae/settings.json`
- `.trae/rules/starter.md`
- `.trae/rules/business-operating-system.md`
- `.trae/agents/*.md`
- `.trae/commands/*.md`

### Grok Build (`.grok/`)

- `.grok/rules/starter.md`
- `.grok/rules/business-operating-system.md`
- `.grok/rules/session-start.md`
- `.grok/agents/*.md`
- `.grok/skills/*/SKILL.md` (copied from `skills/**` with frontmatter)
- `.grok/commands/*.md`

## Policy

- Sync does not import downloaded third-party repositories into active harness config.
- Generated agent and command files describe starter validation, business validation, governance checks, security checks, and evolution sandbox controls.
- Trae and Grok stay dual-supported; do not delete one harness tree without an explicit decision.
- Source of truth for skill **bodies** remains `skills/**/SKILL.md`; Grok copies are regenerated on sync.
