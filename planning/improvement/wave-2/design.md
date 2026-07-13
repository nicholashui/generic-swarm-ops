# Wave 2 Design — Spine E2E

## 1. Architecture

```text
business/video/
  agents/ (114 L0) + standby_pool.json
  workflows/wf_video_spine_v1.dna.json
           wf_video_arch_a_viral_hook_v1.dna.json
  evals/golden/video-spine-viral-hook.json
  knowledge/seeds/*.md

register_domain(video) → agents draft
activate spine agents (ALC) → active
create_workflow(DNA) → status active
start_run → dispatch
  orchestrator → planner → director → screenwriter → webresearch
  → media_gen_stub → qc_stub → human_gate package → complete
approve → complete → reflect (agent_id lessons)
```

## 2. Spine agents (active set)

| pack_id | Role |
|---------|------|
| video.orchestrator | Entry |
| video.planner | Plan |
| video.director | Creative |
| video.screenwriter | Script |
| video.webresearch | Research |
| video.producer | Gate/package |
| video.aiqaconsistency | QC |

Router/judge optional in viral-hook thin path; listed in standby_pool.

## 3. Tools

| tool_id | Adapter | Gate |
|---------|---------|------|
| video_media_gen_stub | local fake asset | no |
| video_script_format | local script blob | no |
| video_qc_stub | local QC pass | no |
| video_package_stub | package deliverable | **human gate** via step human_gate_required |

## 4. DNA shape

Reuse workflow-dna.schema.json. `production_ready: false` for spine.  
Steps use video agents + stubs. Last step next: `["complete"]`.

## 5. N1/N2/N3

- N1: all under business/video; ALC on activate  
- N2: host adapters generic; tool ids namespaced  
- N3: 114 dirs + standby_pool; no deletes  

## 6. Files

```text
planning/improvement/wave-2/{requirements,design,tasks,completion-report}.md
business/video/workflows/wf_video_spine_v1.dna.json
business/video/workflows/wf_video_arch_a_viral_hook_v1.dna.json
business/video/standby_pool.json
business/video/evals/golden/video-spine-viral-hook.json
business/video/knowledge/seeds/spine-orchestration.md
business/security/tool-permissions/tool-permission-register.json  # MOD
backend/app/infrastructure/tools/adapters.py  # MOD
backend/app/runtime.py  # load_tools video stubs
backend/app/tests/unit/test_video_spine_e2e.py  # NEW
```

## 7. Structure / Backend / Frontend

- Structure: DNA, seeds, standby, golden  
- Backend: adapters, tools seed, e2e test  
- Frontend: no required change (DomainPackPanel from W1)

*End Phase 2.*
