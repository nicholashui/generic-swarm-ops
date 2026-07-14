# Special skill integration — `research_agent`

**Status:** MVP integrated (2026-07-14)  
**Kind:** agent_family  
**Plan:** [`planning/special/research_agent.md`](../../../planning/special/research_agent.md)  
**Summary:** Research family 66–72 for doc/research production

## Host binding

### Agents
- `video.webresearch` — SPEC 147.4KB, ALC=yes [OK]
- `video.archiveresearch` — SPEC 152.8KB, ALC=yes [OK]
- `video.factchecker` — SPEC 55.9KB, ALC=yes [OK]
- `video.citation` — SPEC 190.2KB, ALC=yes [OK]
- `video.benchmarkresearch` — SPEC 138.2KB, ALC=yes [OK]

### Workflow DNA
- `wf_video_arch_i_documentary_v1` — steps=8 depth=thin_stub_n3 [OK]
- `wf_video_spine_v1` — steps=8 depth=None [OK]

### Host modules
- _None_

## Runtime contract

- Entry agents: `video.orchestrator` / `video.planner` when DNA-bound.
- Tools: host allow-list only; design-time vendors stay in SPEC.
- Irreversible package/publish steps require human gate.
- No second control plane (N1).

Machine manifest: `integration.json`
