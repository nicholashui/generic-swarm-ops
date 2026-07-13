# Wave 2 Tasks

## T1 [Structure] DNA spine + viral-hook
Create wf_video_spine_v1.dna.json and wf_video_arch_a_viral_hook_v1.dna.json.

## T2 [Structure] standby_pool.json
All 114 pack_ids; spine agents marked `"spine": true` (orchestrator entry `video.orchestrator`).

## T3 [Backend] Video adapters + register
Add video_* stubs to adapters.py and tool-permission-register; ensure load_tools includes them + audit_log_writer if needed.

## T4 [Structure] Golden + knowledge seed
evals/golden + knowledge/seeds.

## T5 [Backend] test_video_spine_e2e.py
Register video pack, activate spine agents with tools, create workflow from DNA, run+approve+reflect.

## T6 [Structure] Update PROCESSES.md / tools/adapters.md / docs

## T7 [Backend] Verification
inventory_check; pytest unit (incl. spine + alc); completion-report.

## By part
| Structure | T1 T2 T4 T6 |
| Backend | T3 T5 T7 |
| Frontend | none required |

*End Phase 3.*
