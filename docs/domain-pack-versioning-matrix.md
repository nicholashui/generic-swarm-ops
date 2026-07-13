# Domain Pack Versioning Matrix

**Wave:** 4  
**Purpose:** When to bump versions so multi-pack hosts stay compatible.

| Artifact | Field / file | Bump when | Compatible change examples |
|----------|--------------|-----------|----------------------------|
| **Pack manifest** | `business/<d>/manifest.json` → `version` | Agents/workflows added/removed; risk default changes | README-only edits |
| **Agent ALC** | `agent_spec.json` → `alc_version` | Memory scopes, reflect hooks, required ALC fields change | Display name only |
| **Workflow DNA** | `workflows/*.dna.json` → `version` | Steps, tools, gates, risk_tier, rollback change | Comments / provenance text |
| **Golden / evals** | fixture `id` (new id preferred) | Expected gates or rubrics change | Description typo |
| **Tool permission register** | `schema_version` + entry | New tool or action scopes | Docs only |
| **Learning logs** | `learning-log.schema.json` consumers | Schema-required fields | Optional tags |
| **Host platform APIs** | product / OpenAPI | Breaking route or auth changes | Additive GET fields |
| **Domain Pack schemas** | `business/schemas/*.schema.json` | Required property add/remove | Optional properties |

## Compatibility rules

1. **Fail closed:** invalid manifest / missing ALC → refuse register or activate.
2. **Sandbox first:** DNA evolution stays `sandbox_only` until explicit canary/promote.
3. **Inventory:** video pack agent **count** is enforced by CI (114); other packs never reduce it.
4. **Namespaces:** tool and agent ids should be domain-prefixed (`video.*`, `example.*`).

## Suggested semver for pack `version`

| Bump | Meaning |
|------|---------|
| MAJOR | Breaking agent/tool contracts for pack consumers |
| MINOR | New agents, workflows, or evals (backward compatible) |
| PATCH | Docs, rubrics text, non-behavioral fixes |

## Related

- `docs/add-domain-pack-runbook.md`
- `docs/domain-packs.md`
- `planning/improvement/wave-4/`
