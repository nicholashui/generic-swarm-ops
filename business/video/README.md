# Video Production Domain Pack

**Domain id:** `video`  
**Host:** generic-swarm-ops (universal MMA platform)  
**Upstream research (optional):** [va-agent-swarm](https://github.com/nicholashui/va-agent-swarm)  
**In-pack corpus (required SoT):** `business/video/corpus/` — full copy of va study/plan/root (see `corpus/README.md`, `migration_plan.md`)

## Standalone rule

Coding agents and humans must be able to work **without** `C:\Project\va-agent-swarm` on disk:

1. Read `agents/<pack_id>/SPEC.md` — **self-contained** (embedded roster + §11 common structure + deep specs + workflow passages). Not a refer-only stub.
2. Read `agents/<pack_id>/sources/` — copied related corpus/va files for that agent.
3. Full tree also under `corpus/study|plan|root/` (MANIFEST 325 files).
4. Integrity: `python scripts/business/check_video_corpus_standalone.py`  
   Re-enrich: `python scripts/business/enrich_video_agent_specs.py --write`

## N3 retention policy (mandatory)

- **All 114 agents** from `adoption.md` Appendix A live under `agents/<pack_id>/`.
- **Do not delete** agent directories to “reduce scope.”
- Runtime activation may stay `draft` until later waves; **catalog presence is forever**.
- Inventory CI fails if count ≠ 114 or MAP incomplete.

## Non-negotiables

- **N1:** Video business logic stays in this pack only (not host core).
- **N2:** Pack uses Domain Pack schemas shared by other domains.
- **N3:** Full roster + process index; orchestrator-down hierarchy.

## Namespace

- Video meta agents: `video.orchestrator`, `video.planner`, `video.router`, `video.judge`, …
- Ops seed agent `business_orchestrator` remains **ops domain** — never overwrite with video.

## Layout

| Path | Role |
|------|------|
| `ROSTER.json` | 114 agents machine roster |
| `MAP.md` | va_id → pack_id → path |
| `PROCESSES.md` | Process index (DNA depth later) |
| `manifest.json` | Domain pack manifest (draft) |
| `agents/*` | agent_spec + **expanded SPEC.md** (from corpus agents.md) |
| `corpus/` | Full va knowledge mirror (325 files) |
| `workflows/` | DNA files (Wave 2+) |
| `knowledge/seeds/` | Optional retrieval seeds |

## Related

- `migration_plan.md` — copy-all plan  
- `adoption.md` v2.4 §5.0 / Appendix A  
- `improvements.md` Waves 0–5  

- `docs/domain-packs.md`  
