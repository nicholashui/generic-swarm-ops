# Spec: Domains

**Route:** `/app/domains`  
**Permission (typical):** workflows:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Multi-domain pack surface: domain inventory, video N3 roster, workflow recommendation, and special-skill registry views.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- DomainPackPanel — pack/agent inventory context
- VideoN3RosterPanel — N3 retention roster status
- RecommendWorkflowPanel — free-text brief → ranked DNA recommendation
- SpecialSkillsPanel — pack special-skill integrations from REGISTRY

## Backend / API contracts

- GET /domains/video/n3-status, /domains/video/archetypes
- POST /domains/video/recommend-workflow
- GET /domains/video/special-skills
- Domain registration APIs / inventory gates (CLI + API waves)

## Architecture mapping

- Domain pack extension layer (structure.md §0 Domain Pack)
- business/<domain_id>/ with manifest, agents, evals; video pack is first rich pack
- Recommend path is real selector logic — not mock when live mode is on

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/domains/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/domains/spec.md`
