# Migration tasks — implement, review, score **100** per agent

**Status:** **v1 honest reopened** — not fleet-100; see `agent_impl_v1_mark.md` (2026-07-13)
**Order source:** [`agent_implement_order_list.md`](./agent_implement_order_list.md)  
**Prompt source:** per-agent [`video.<id>.md`](./README.md)  
**Agent folder:** `business/video/agents/<id>/`  
**Fleet tooling:** `scripts/business/run_migration_tasks_fleet.py`

## Goal

For **every** of the **114** video agents, in **order seq**:

1. **Implement** the agent materials using its migration prompt.
2. **Review** against the global scorecard.
3. **Score must be 100/100** before the agent is done.
4. **Do not start agent N+1** until agent N is **score 100** (unless blocked + documented).

**Fleet exit:** 114/114 agents at score **100** + inventory + corpus standalone still green. ❌ **Not met (v1 honest).**

---

## Global scorecard (must total **100**)

Score each agent with the same rubric. **Exit requires every dimension at full marks** (100 only).

| Dim | Points | Full-mark criteria (all required) |
|-----|-------:|-----------------------------------|
| **S1 Self-contained SPEC** | 25 | `SPEC.md` is not refer-only; embeds roster/corpus content; no required external `va-agent-swarm/study` primary path; substantial depth (typically ≥8 KB after implement) |
| **S2 Corpus fidelity** | 20 | Relevant `business/video/corpus` (+ va if used) integrated into SPEC and/or `sources/`; core definition does not depend on missing external repo |
| **S3 Prompt execution** | 15 | Full run of `planning/migration/<agent_id>.md` including **role-specific** arXiv / X / YouTube capability research integrated into SPEC |
| **S4 Runtime binding** | 15 | `agent_spec.json` ALC-complete (`requires_alc`, memory scopes include agent, `alc_version`, reflect); design-time vs runtime tools separated; no illegal allow-list expansion |
| **S5 Reachability** | 10 | In ROSTER/MAP/standby; pack_id consistent; DNA or standby reachability noted |
| **S6 Review quality** | 15 | S6 checklist all ✓; no open P0 defects; reviewer confirms total **100** |
| **Total** | **100** | Agent complete **only if 100** |

### Score rules

- Progression is **binary**: **100 = pass**, **&lt;100 = fail → rework → re-review**.
- Incomplete dimension ⇒ total is **not** 100.
- After rework, re-score all dimensions; only then mark `done`.

### S6 review checklist (all must be ✓ for 15 points)

- [ ] Identity: pack_id, va_id, category correct
- [ ] Responsibility / tools / critique / architecture detailed
- [ ] Common structure (or equal depth) present
- [ ] Capability research applied (arXiv + X + YouTube themes from **this** agent’s prompt)
- [ ] N1: video logic stays in pack; no second control plane
- [ ] No auto-promote / sandbox bypass as default runtime behavior
- [ ] `sources/` present when deep docs used, **or** SPEC embeds full needed text
- [ ] Prompt file id matches agent id and folder path

---

## Global gates

### G0 — Pre-flight (once)

- [x] `python scripts/business/inventory_check.py` → `INVENTORY PASS count=114 n3=complete`
- [x] `python scripts/business/check_video_corpus_standalone.py` → `STANDALONE PASS`
- [x] `business/video/corpus/MANIFEST.json` present
- [x] 114 prompts under `planning/migration/video.*.md`

### G1 — Fleet complete (only when all agents = 100)

- [ ] Master table: 114 rows `done` with score **100**
- [x] Inventory still PASS
- [x] Standalone still PASS
- [x] `pytest backend/app/tests/unit/test_video_corpus_standalone.py -q` green
- [ ] `memory/handoff.md` notes fleet 100 completion

---

## Per-agent workflow (every seq)

1. **Implement** — execute `planning/migration/<agent_id>.md`; update agent folder.
2. **Self-check** — S1–S5 full marks.
3. **Review** — S6 checklist all ✓ (critic / second pass).
4. **Score** — must be **100**; else rework.
5. Mark master row + detailed block complete.
6. Only then advance to next order seq.

---

## Master task table (114)

| order seq | agent id | implement prompt | agent folder | implement | review | score | status |
|----------:|----------|------------------|--------------|:---------:|:------:|------:|--------|
| 1 | `video.orchestrator` | [`video.orchestrator.md`](./video.orchestrator.md) | `business/video/agents/video.orchestrator` | [x] | [x] | 97 | research_strong |
| 2 | `video.planner` | [`video.planner.md`](./video.planner.md) | `business/video/agents/video.planner` | [x] | [x] | 97 | research_strong |
| 3 | `video.router` | [`video.router.md`](./video.router.md) | `business/video/agents/video.router` | [x] | [x] | 96 | research_strong |
| 4 | `video.judge` | [`video.judge.md`](./video.judge.md) | `business/video/agents/video.judge` | [x] | [x] | 96 | research_strong |
| 5 | `video.gatekeeper` | [`video.gatekeeper.md`](./video.gatekeeper.md) | `business/video/agents/video.gatekeeper` | [x] | [x] | 96 | research_strong |
| 6 | `video.producer` | [`video.producer.md`](./video.producer.md) | `business/video/agents/video.producer` | [x] | [x] | 96 | research_strong |
| 7 | `video.director` | [`video.director.md`](./video.director.md) | `business/video/agents/video.director` | [x] | [x] | 96 | research_strong |
| 8 | `video.screenwriter` | [`video.screenwriter.md`](./video.screenwriter.md) | `business/video/agents/video.screenwriter` | [x] | [x] | 96 | research_strong |
| 9 | `video.webresearch` | [`video.webresearch.md`](./video.webresearch.md) | `business/video/agents/video.webresearch` | [x] | [x] | 96 | research_strong |
| 10 | `video.aiqaconsistency` | [`video.aiqaconsistency.md`](./video.aiqaconsistency.md) | `business/video/agents/video.aiqaconsistency` | [x] | [x] | 96 | research_strong |
| 11 | `video.memory` | [`video.memory.md`](./video.memory.md) | `business/video/agents/video.memory` | [x] | [x] | 96 | research_strong |
| 12 | `video.showrunner` | [`video.showrunner.md`](./video.showrunner.md) | `business/video/agents/video.showrunner` | [x] | [x] | 96 | research_strong |
| 13 | `video.casting` | [`video.casting.md`](./video.casting.md) | `business/video/agents/video.casting` | [x] | [x] | 92 | structural_pass |
| 14 | `video.cinematographer` | [`video.cinematographer.md`](./video.cinematographer.md) | `business/video/agents/video.cinematographer` | [x] | [x] | 96 | research_strong |
| 15 | `video.cameraoperator` | [`video.cameraoperator.md`](./video.cameraoperator.md) | `business/video/agents/video.cameraoperator` | [x] | [x] | 86 | structural_pass |
| 16 | `video.dronepilot` | [`video.dronepilot.md`](./video.dronepilot.md) | `business/video/agents/video.dronepilot` | [x] | [x] | 92 | structural_pass |
| 17 | `video.editor` | [`video.editor.md`](./video.editor.md) | `business/video/agents/video.editor` | [x] | [x] | 96 | research_strong |
| 18 | `video.colorist` | [`video.colorist.md`](./video.colorist.md) | `business/video/agents/video.colorist` | [x] | [x] | 95 | research_strong |
| 19 | `video.vfxsupervisor` | [`video.vfxsupervisor.md`](./video.vfxsupervisor.md) | `business/video/agents/video.vfxsupervisor` | [x] | [x] | 92 | structural_pass |
| 20 | `video.animator_2d` | [`video.animator_2d.md`](./video.animator_2d.md) | `business/video/agents/video.animator_2d` | [x] | [x] | 92 | structural_pass |
| 21 | `video.motiongraphics` | [`video.motiongraphics.md`](./video.motiongraphics.md) | `business/video/agents/video.motiongraphics` | [x] | [x] | 94 | structural_pass |
| 22 | `video.storyboard` | [`video.storyboard.md`](./video.storyboard.md) | `business/video/agents/video.storyboard` | [x] | [x] | 94 | structural_pass |
| 23 | `video.conceptartist` | [`video.conceptartist.md`](./video.conceptartist.md) | `business/video/agents/video.conceptartist` | [x] | [x] | 95 | structural_pass |
| 24 | `video.productiondesign` | [`video.productiondesign.md`](./video.productiondesign.md) | `business/video/agents/video.productiondesign` | [x] | [x] | 92 | structural_pass |
| 25 | `video.costumedesign` | [`video.costumedesign.md`](./video.costumedesign.md) | `business/video/agents/video.costumedesign` | [x] | [x] | 92 | structural_pass |
| 26 | `video.mua_makeup` | [`video.mua_makeup.md`](./video.mua_makeup.md) | `business/video/agents/video.mua_makeup` | [x] | [x] | 92 | structural_pass |
| 27 | `video.sounddesign` | [`video.sounddesign.md`](./video.sounddesign.md) | `business/video/agents/video.sounddesign` | [x] | [x] | 96 | research_strong |
| 28 | `video.composer` | [`video.composer.md`](./video.composer.md) | `business/video/agents/video.composer` | [x] | [x] | 96 | research_strong |
| 29 | `video.voiceover` | [`video.voiceover.md`](./video.voiceover.md) | `business/video/agents/video.voiceover` | [x] | [x] | 96 | research_strong |
| 30 | `video.soundmixer` | [`video.soundmixer.md`](./video.soundmixer.md) | `business/video/agents/video.soundmixer` | [x] | [x] | 96 | research_strong |
| 31 | `video.choreography` | [`video.choreography.md`](./video.choreography.md) | `business/video/agents/video.choreography` | [x] | [x] | 92 | structural_pass |
| 32 | `video.musicvideodirector` | [`video.musicvideodirector.md`](./video.musicvideodirector.md) | `business/video/agents/video.musicvideodirector` | [x] | [x] | 92 | structural_pass |
| 33 | `video.comedywriter` | [`video.comedywriter.md`](./video.comedywriter.md) | `business/video/agents/video.comedywriter` | [x] | [x] | 95 | structural_pass |
| 34 | `video.talent` | [`video.talent.md`](./video.talent.md) | `business/video/agents/video.talent` | [x] | [x] | 94 | structural_pass |
| 35 | `video.ugccreator` | [`video.ugccreator.md`](./video.ugccreator.md) | `business/video/agents/video.ugccreator` | [x] | [x] | 86 | structural_pass |
| 36 | `video.socialmediastrategist` | [`video.socialmediastrategist.md`](./video.socialmediastrategist.md) | `business/video/agents/video.socialmediastrategist` | [x] | [x] | 92 | structural_pass |
| 37 | `video.copywriter` | [`video.copywriter.md`](./video.copywriter.md) | `business/video/agents/video.copywriter` | [x] | [x] | 94 | structural_pass |
| 38 | `video.creativedirector` | [`video.creativedirector.md`](./video.creativedirector.md) | `business/video/agents/video.creativedirector` | [x] | [x] | 92 | structural_pass |
| 39 | `video.performancemarketer` | [`video.performancemarketer.md`](./video.performancemarketer.md) | `business/video/agents/video.performancemarketer` | [x] | [x] | 96 | research_strong |
| 40 | `video.instructionaldesign` | [`video.instructionaldesign.md`](./video.instructionaldesign.md) | `business/video/agents/video.instructionaldesign` | [x] | [x] | 92 | structural_pass |
| 41 | `video.sme` | [`video.sme.md`](./video.sme.md) | `business/video/agents/video.sme` | [x] | [x] | 94 | structural_pass |
| 42 | `video.factchecker` | [`video.factchecker.md`](./video.factchecker.md) | `business/video/agents/video.factchecker` | [x] | [x] | 92 | structural_pass |
| 43 | `video.medicalillustrator` | [`video.medicalillustrator.md`](./video.medicalillustrator.md) | `business/video/agents/video.medicalillustrator` | [x] | [x] | 92 | structural_pass |
| 44 | `video.journalist` | [`video.journalist.md`](./video.journalist.md) | `business/video/agents/video.journalist` | [x] | [x] | 96 | research_strong |
| 45 | `video.compliance` | [`video.compliance.md`](./video.compliance.md) | `business/video/agents/video.compliance` | [x] | [x] | 96 | research_strong |
| 46 | `video.finance` | [`video.finance.md`](./video.finance.md) | `business/video/agents/video.finance` | [x] | [x] | 92 | structural_pass |
| 47 | `video.foodstylist` | [`video.foodstylist.md`](./video.foodstylist.md) | `business/video/agents/video.foodstylist` | [x] | [x] | 92 | structural_pass |
| 48 | `video.travelcine` | [`video.travelcine.md`](./video.travelcine.md) | `business/video/agents/video.travelcine` | [x] | [x] | 92 | structural_pass |
| 49 | `video.childrensauthor` | [`video.childrensauthor.md`](./video.childrensauthor.md) | `business/video/agents/video.childrensauthor` | [x] | [x] | 96 | research_strong |
| 50 | `video.audiobooknarrator` | [`video.audiobooknarrator.md`](./video.audiobooknarrator.md) | `business/video/agents/video.audiobooknarrator` | [x] | [x] | 96 | research_strong |
| 51 | `video.signlanguageinterpreter` | [`video.signlanguageinterpreter.md`](./video.signlanguageinterpreter.md) | `business/video/agents/video.signlanguageinterpreter` | [x] | [x] | 92 | structural_pass |
| 52 | `video.localizationqa` | [`video.localizationqa.md`](./video.localizationqa.md) | `business/video/agents/video.localizationqa` | [x] | [x] | 92 | structural_pass |
| 53 | `video.realestatephoto` | [`video.realestatephoto.md`](./video.realestatephoto.md) | `business/video/agents/video.realestatephoto` | [x] | [x] | 92 | structural_pass |
| 54 | `video.promptengineer` | [`video.promptengineer.md`](./video.promptengineer.md) | `business/video/agents/video.promptengineer` | [x] | [x] | 96 | research_strong |
| 55 | `video.avatardesign` | [`video.avatardesign.md`](./video.avatardesign.md) | `business/video/agents/video.avatardesign` | [x] | [x] | 95 | structural_pass |
| 56 | `video.voiceclone` | [`video.voiceclone.md`](./video.voiceclone.md) | `business/video/agents/video.voiceclone` | [x] | [x] | 92 | structural_pass |
| 57 | `video.personalizationengineer` | [`video.personalizationengineer.md`](./video.personalizationengineer.md) | `business/video/agents/video.personalizationengineer` | [x] | [x] | 96 | research_strong |
| 58 | `video.trailereditor` | [`video.trailereditor.md`](./video.trailereditor.md) | `business/video/agents/video.trailereditor` | [x] | [x] | 92 | structural_pass |
| 59 | `video.sportsanalyst` | [`video.sportsanalyst.md`](./video.sportsanalyst.md) | `business/video/agents/video.sportsanalyst` | [x] | [x] | 86 | structural_pass |
| 60 | `video.ideation` | [`video.ideation.md`](./video.ideation.md) | `business/video/agents/video.ideation` | [x] | [x] | 96 | research_strong |
| 61 | `video.narrativearc` | [`video.narrativearc.md`](./video.narrativearc.md) | `business/video/agents/video.narrativearc` | [x] | [x] | 95 | structural_pass |
| 62 | `video.styletransfer` | [`video.styletransfer.md`](./video.styletransfer.md) | `business/video/agents/video.styletransfer` | [x] | [x] | 95 | structural_pass |
| 63 | `video.worldbuilding` | [`video.worldbuilding.md`](./video.worldbuilding.md) | `business/video/agents/video.worldbuilding` | [x] | [x] | 92 | structural_pass |
| 64 | `video.moodboard` | [`video.moodboard.md`](./video.moodboard.md) | `business/video/agents/video.moodboard` | [x] | [x] | 92 | structural_pass |
| 65 | `video.novelty` | [`video.novelty.md`](./video.novelty.md) | `business/video/agents/video.novelty` | [x] | [x] | 95 | structural_pass |
| 66 | `video.emotionalarc` | [`video.emotionalarc.md`](./video.emotionalarc.md) | `business/video/agents/video.emotionalarc` | [x] | [x] | 96 | research_strong |
| 67 | `video.archiveresearch` | [`video.archiveresearch.md`](./video.archiveresearch.md) | `business/video/agents/video.archiveresearch` | [x] | [x] | 96 | research_strong |
| 68 | `video.trendintelligence` | [`video.trendintelligence.md`](./video.trendintelligence.md) | `business/video/agents/video.trendintelligence` | [x] | [x] | 95 | structural_pass |
| 69 | `video.competitorintelligence` | [`video.competitorintelligence.md`](./video.competitorintelligence.md) | `business/video/agents/video.competitorintelligence` | [x] | [x] | 95 | structural_pass |
| 70 | `video.citation` | [`video.citation.md`](./video.citation.md) | `business/video/agents/video.citation` | [x] | [x] | 96 | research_strong |
| 71 | `video.interviewsynthesis` | [`video.interviewsynthesis.md`](./video.interviewsynthesis.md) | `business/video/agents/video.interviewsynthesis` | [x] | [x] | 96 | research_strong |
| 72 | `video.benchmarkresearch` | [`video.benchmarkresearch.md`](./video.benchmarkresearch.md) | `business/video/agents/video.benchmarkresearch` | [x] | [x] | 96 | research_strong |
| 73 | `video.promptoptimizer` | [`video.promptoptimizer.md`](./video.promptoptimizer.md) | `business/video/agents/video.promptoptimizer` | [x] | [x] | 95 | structural_pass |
| 74 | `video.costoptimizer` | [`video.costoptimizer.md`](./video.costoptimizer.md) | `business/video/agents/video.costoptimizer` | [x] | [x] | 95 | structural_pass |
| 75 | `video.latencyoptimizer` | [`video.latencyoptimizer.md`](./video.latencyoptimizer.md) | `business/video/agents/video.latencyoptimizer` | [x] | [x] | 92 | structural_pass |
| 76 | `video.retentionoptimizer` | [`video.retentionoptimizer.md`](./video.retentionoptimizer.md) | `business/video/agents/video.retentionoptimizer` | [x] | [x] | 96 | research_strong |
| 77 | `video.roasoptimizer` | [`video.roasoptimizer.md`](./video.roasoptimizer.md) | `business/video/agents/video.roasoptimizer` | [x] | [x] | 92 | structural_pass |
| 78 | `video.accessibilityoptimizer` | [`video.accessibilityoptimizer.md`](./video.accessibilityoptimizer.md) | `business/video/agents/video.accessibilityoptimizer` | [x] | [x] | 95 | structural_pass |
| 79 | `video.evaluationharness` | [`video.evaluationharness.md`](./video.evaluationharness.md) | `business/video/agents/video.evaluationharness` | [x] | [x] | 96 | research_strong |
| 80 | `video.safetyredteam` | [`video.safetyredteam.md`](./video.safetyredteam.md) | `business/video/agents/video.safetyredteam` | [x] | [x] | 92 | structural_pass |
| 81 | `video.analyst` | [`video.analyst.md`](./video.analyst.md) | `business/video/agents/video.analyst` | [x] | [x] | 96 | research_strong |
| 82 | `video.audiencesim` | [`video.audiencesim.md`](./video.audiencesim.md) | `business/video/agents/video.audiencesim` | [x] | [x] | 96 | research_strong |
| 83 | `video.accessibility` | [`video.accessibility.md`](./video.accessibility.md) | `business/video/agents/video.accessibility` | [x] | [x] | 95 | research_strong |
| 84 | `video.brand` | [`video.brand.md`](./video.brand.md) | `business/video/agents/video.brand` | [x] | [x] | 96 | research_strong |
| 85 | `video.brandstrategist` | [`video.brandstrategist.md`](./video.brandstrategist.md) | `business/video/agents/video.brandstrategist` | [x] | [x] | 96 | research_strong |
| 86 | `video.marketing` | [`video.marketing.md`](./video.marketing.md) | `business/video/agents/video.marketing` | [x] | [x] | 96 | research_strong |
| 87 | `video.seo` | [`video.seo.md`](./video.seo.md) | `business/video/agents/video.seo` | [x] | [x] | 96 | research_strong |
| 88 | `video.community` | [`video.community.md`](./video.community.md) | `business/video/agents/video.community` | [x] | [x] | 95 | research_strong |
| 89 | `video.templatedesign` | [`video.templatedesign.md`](./video.templatedesign.md) | `business/video/agents/video.templatedesign` | [x] | [x] | 96 | research_strong |
| 90 | `video.ux` | [`video.ux.md`](./video.ux.md) | `business/video/agents/video.ux` | [x] | [x] | 88 | structural_pass |
| 91 | `video.trustsafety` | [`video.trustsafety.md`](./video.trustsafety.md) | `business/video/agents/video.trustsafety` | [x] | [x] | 92 | structural_pass |
| 92 | `video.crm` | [`video.crm.md`](./video.crm.md) | `business/video/agents/video.crm` | [x] | [x] | 92 | structural_pass |
| 93 | `video.legal` | [`video.legal.md`](./video.legal.md) | `business/video/agents/video.legal` | [x] | [x] | 94 | structural_pass |
| 94 | `video.festivalstrategist` | [`video.festivalstrategist.md`](./video.festivalstrategist.md) | `business/video/agents/video.festivalstrategist` | [x] | [x] | 88 | structural_pass |
| 95 | `video.critic` | [`video.critic.md`](./video.critic.md) | `business/video/agents/video.critic` | [x] | [x] | 96 | research_strong |
| 96 | `video.lms` | [`video.lms.md`](./video.lms.md) | `business/video/agents/video.lms` | [x] | [x] | 95 | research_strong |
| 97 | `video.learnersim` | [`video.learnersim.md`](./video.learnersim.md) | `business/video/agents/video.learnersim` | [x] | [x] | 95 | structural_pass |
| 98 | `video.continuity` | [`video.continuity.md`](./video.continuity.md) | `business/video/agents/video.continuity` | [x] | [x] | 96 | research_strong |
| 99 | `video.lipsync` | [`video.lipsync.md`](./video.lipsync.md) | `business/video/agents/video.lipsync` | [x] | [x] | 96 | research_strong |
| 100 | `video.musicsupervisor` | [`video.musicsupervisor.md`](./video.musicsupervisor.md) | `business/video/agents/video.musicsupervisor` | [x] | [x] | 96 | research_strong |
| 101 | `video.labela_r` | [`video.labela_r.md`](./video.labela_r.md) | `business/video/agents/video.labela_r` | [x] | [x] | 88 | structural_pass |
| 102 | `video.labeldigital` | [`video.labeldigital.md`](./video.labeldigital.md) | `business/video/agents/video.labeldigital` | [x] | [x] | 88 | structural_pass |
| 103 | `video.deepfakedetection` | [`video.deepfakedetection.md`](./video.deepfakedetection.md) | `business/video/agents/video.deepfakedetection` | [x] | [x] | 92 | structural_pass |
| 104 | `video.comms` | [`video.comms.md`](./video.comms.md) | `business/video/agents/video.comms` | [x] | [x] | 92 | structural_pass |
| 105 | `video.archiveproducer` | [`video.archiveproducer.md`](./video.archiveproducer.md) | `business/video/agents/video.archiveproducer` | [x] | [x] | 88 | structural_pass |
| 106 | `video.standardseditor` | [`video.standardseditor.md`](./video.standardseditor.md) | `business/video/agents/video.standardseditor` | [x] | [x] | 92 | structural_pass |
| 107 | `video.ethics` | [`video.ethics.md`](./video.ethics.md) | `business/video/agents/video.ethics` | [x] | [x] | 94 | structural_pass |
| 108 | `video.channelmanager` | [`video.channelmanager.md`](./video.channelmanager.md) | `business/video/agents/video.channelmanager` | [x] | [x] | 92 | structural_pass |
| 109 | `video.corrections` | [`video.corrections.md`](./video.corrections.md) | `business/video/agents/video.corrections` | [x] | [x] | 92 | structural_pass |
| 110 | `video.mpa` | [`video.mpa.md`](./video.mpa.md) | `business/video/agents/video.mpa` | [x] | [x] | 96 | research_strong |
| 111 | `video.sales` | [`video.sales.md`](./video.sales.md) | `business/video/agents/video.sales` | [x] | [x] | 92 | structural_pass |
| 112 | `video.distributor` | [`video.distributor.md`](./video.distributor.md) | `business/video/agents/video.distributor` | [x] | [x] | 94 | structural_pass |
| 113 | `video.awardsstrategist` | [`video.awardsstrategist.md`](./video.awardsstrategist.md) | `business/video/agents/video.awardsstrategist` | [x] | [x] | 88 | structural_pass |
| 114 | `video.archivemaster` | [`video.archivemaster.md`](./video.archivemaster.md) | `business/video/agents/video.archivemaster` | [x] | [x] | 92 | structural_pass |

**Status:** `todo` · `in_progress` · `rework` · `done`  
**`done` only if:** implement ✓, review ✓, score column **100**.

---

## Detailed tasks per agent (implement + review + score 100)

### T-001 — `video.orchestrator` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 1 / 114 |
| Prompt | [`planning/migration/video.orchestrator.md`](./video.orchestrator.md) |
| Folder | `business/video/agents/video.orchestrator` |

#### Implement

- [x] Execute full prompt [`video.orchestrator.md`](./video.orchestrator.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.orchestrator/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.orchestrator/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.orchestrator/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 13 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **97** |


- [ ] **Final score = 100** (required to close T-001)
- [ ] Master table status → `done`

---
### T-002 — `video.planner` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 2 / 114 |
| Prompt | [`planning/migration/video.planner.md`](./video.planner.md) |
| Folder | `business/video/agents/video.planner` |

#### Implement

- [x] Execute full prompt [`video.planner.md`](./video.planner.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.planner/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.planner/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.planner/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 13 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **97** |


- [ ] **Final score = 100** (required to close T-002)
- [ ] Master table status → `done`

---
### T-003 — `video.router` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 3 / 114 |
| Prompt | [`planning/migration/video.router.md`](./video.router.md) |
| Folder | `business/video/agents/video.router` |

#### Implement

- [x] Execute full prompt [`video.router.md`](./video.router.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.router/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.router/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.router/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-003)
- [ ] Master table status → `done`

---
### T-004 — `video.judge` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 4 / 114 |
| Prompt | [`planning/migration/video.judge.md`](./video.judge.md) |
| Folder | `business/video/agents/video.judge` |

#### Implement

- [x] Execute full prompt [`video.judge.md`](./video.judge.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.judge/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.judge/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.judge/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-004)
- [ ] Master table status → `done`

---
### T-005 — `video.gatekeeper` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 5 / 114 |
| Prompt | [`planning/migration/video.gatekeeper.md`](./video.gatekeeper.md) |
| Folder | `business/video/agents/video.gatekeeper` |

#### Implement

- [x] Execute full prompt [`video.gatekeeper.md`](./video.gatekeeper.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.gatekeeper/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.gatekeeper/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.gatekeeper/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-005)
- [ ] Master table status → `done`

---
### T-006 — `video.producer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 6 / 114 |
| Prompt | [`planning/migration/video.producer.md`](./video.producer.md) |
| Folder | `business/video/agents/video.producer` |

#### Implement

- [x] Execute full prompt [`video.producer.md`](./video.producer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.producer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.producer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.producer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-006)
- [ ] Master table status → `done`

---
### T-007 — `video.director` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 7 / 114 |
| Prompt | [`planning/migration/video.director.md`](./video.director.md) |
| Folder | `business/video/agents/video.director` |

#### Implement

- [x] Execute full prompt [`video.director.md`](./video.director.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.director/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.director/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.director/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-007)
- [ ] Master table status → `done`

---
### T-008 — `video.screenwriter` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 8 / 114 |
| Prompt | [`planning/migration/video.screenwriter.md`](./video.screenwriter.md) |
| Folder | `business/video/agents/video.screenwriter` |

#### Implement

- [x] Execute full prompt [`video.screenwriter.md`](./video.screenwriter.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.screenwriter/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.screenwriter/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.screenwriter/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-008)
- [ ] Master table status → `done`

---
### T-009 — `video.webresearch` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 9 / 114 |
| Prompt | [`planning/migration/video.webresearch.md`](./video.webresearch.md) |
| Folder | `business/video/agents/video.webresearch` |

#### Implement

- [x] Execute full prompt [`video.webresearch.md`](./video.webresearch.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.webresearch/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.webresearch/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.webresearch/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-009)
- [ ] Master table status → `done`

---
### T-010 — `video.aiqaconsistency` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 10 / 114 |
| Prompt | [`planning/migration/video.aiqaconsistency.md`](./video.aiqaconsistency.md) |
| Folder | `business/video/agents/video.aiqaconsistency` |

#### Implement

- [x] Execute full prompt [`video.aiqaconsistency.md`](./video.aiqaconsistency.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.aiqaconsistency/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.aiqaconsistency/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.aiqaconsistency/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-010)
- [ ] Master table status → `done`

---
### T-011 — `video.memory` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 11 / 114 |
| Prompt | [`planning/migration/video.memory.md`](./video.memory.md) |
| Folder | `business/video/agents/video.memory` |

#### Implement

- [x] Execute full prompt [`video.memory.md`](./video.memory.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.memory/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.memory/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.memory/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-011)
- [ ] Master table status → `done`

---
### T-012 — `video.showrunner` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 12 / 114 |
| Prompt | [`planning/migration/video.showrunner.md`](./video.showrunner.md) |
| Folder | `business/video/agents/video.showrunner` |

#### Implement

- [x] Execute full prompt [`video.showrunner.md`](./video.showrunner.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.showrunner/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.showrunner/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.showrunner/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-012)
- [ ] Master table status → `done`

---
### T-013 — `video.casting` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 13 / 114 |
| Prompt | [`planning/migration/video.casting.md`](./video.casting.md) |
| Folder | `business/video/agents/video.casting` |

#### Implement

- [ ] Execute full prompt [`video.casting.md`](./video.casting.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.casting/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.casting/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.casting/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-013)
- [ ] Master table status → `done`

---
### T-014 — `video.cinematographer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 14 / 114 |
| Prompt | [`planning/migration/video.cinematographer.md`](./video.cinematographer.md) |
| Folder | `business/video/agents/video.cinematographer` |

#### Implement

- [x] Execute full prompt [`video.cinematographer.md`](./video.cinematographer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.cinematographer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.cinematographer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.cinematographer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-014)
- [ ] Master table status → `done`

---
### T-015 — `video.cameraoperator` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 15 / 114 |
| Prompt | [`planning/migration/video.cameraoperator.md`](./video.cameraoperator.md) |
| Folder | `business/video/agents/video.cameraoperator` |

#### Implement

- [ ] Execute full prompt [`video.cameraoperator.md`](./video.cameraoperator.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.cameraoperator/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.cameraoperator/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.cameraoperator/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 8 |
| **Total** | **100** | **86** |


- [ ] **Final score = 100** (required to close T-015)
- [ ] Master table status → `done`

---
### T-016 — `video.dronepilot` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 16 / 114 |
| Prompt | [`planning/migration/video.dronepilot.md`](./video.dronepilot.md) |
| Folder | `business/video/agents/video.dronepilot` |

#### Implement

- [ ] Execute full prompt [`video.dronepilot.md`](./video.dronepilot.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.dronepilot/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.dronepilot/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.dronepilot/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-016)
- [ ] Master table status → `done`

---
### T-017 — `video.editor` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 17 / 114 |
| Prompt | [`planning/migration/video.editor.md`](./video.editor.md) |
| Folder | `business/video/agents/video.editor` |

#### Implement

- [x] Execute full prompt [`video.editor.md`](./video.editor.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.editor/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.editor/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.editor/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-017)
- [ ] Master table status → `done`

---
### T-018 — `video.colorist` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 18 / 114 |
| Prompt | [`planning/migration/video.colorist.md`](./video.colorist.md) |
| Folder | `business/video/agents/video.colorist` |

#### Implement

- [x] Execute full prompt [`video.colorist.md`](./video.colorist.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.colorist/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.colorist/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.colorist/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-018)
- [ ] Master table status → `done`

---
### T-019 — `video.vfxsupervisor` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 19 / 114 |
| Prompt | [`planning/migration/video.vfxsupervisor.md`](./video.vfxsupervisor.md) |
| Folder | `business/video/agents/video.vfxsupervisor` |

#### Implement

- [ ] Execute full prompt [`video.vfxsupervisor.md`](./video.vfxsupervisor.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.vfxsupervisor/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.vfxsupervisor/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.vfxsupervisor/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-019)
- [ ] Master table status → `done`

---
### T-020 — `video.animator_2d` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 20 / 114 |
| Prompt | [`planning/migration/video.animator_2d.md`](./video.animator_2d.md) |
| Folder | `business/video/agents/video.animator_2d` |

#### Implement

- [ ] Execute full prompt [`video.animator_2d.md`](./video.animator_2d.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.animator_2d/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.animator_2d/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.animator_2d/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-020)
- [ ] Master table status → `done`

---
### T-021 — `video.motiongraphics` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 21 / 114 |
| Prompt | [`planning/migration/video.motiongraphics.md`](./video.motiongraphics.md) |
| Folder | `business/video/agents/video.motiongraphics` |

#### Implement

- [ ] Execute full prompt [`video.motiongraphics.md`](./video.motiongraphics.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.motiongraphics/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.motiongraphics/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.motiongraphics/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **94** |


- [ ] **Final score = 100** (required to close T-021)
- [ ] Master table status → `done`

---
### T-022 — `video.storyboard` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 22 / 114 |
| Prompt | [`planning/migration/video.storyboard.md`](./video.storyboard.md) |
| Folder | `business/video/agents/video.storyboard` |

#### Implement

- [ ] Execute full prompt [`video.storyboard.md`](./video.storyboard.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.storyboard/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.storyboard/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.storyboard/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **94** |


- [ ] **Final score = 100** (required to close T-022)
- [ ] Master table status → `done`

---
### T-023 — `video.conceptartist` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 23 / 114 |
| Prompt | [`planning/migration/video.conceptartist.md`](./video.conceptartist.md) |
| Folder | `business/video/agents/video.conceptartist` |

#### Implement

- [ ] Execute full prompt [`video.conceptartist.md`](./video.conceptartist.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.conceptartist/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.conceptartist/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.conceptartist/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-023)
- [ ] Master table status → `done`

---
### T-024 — `video.productiondesign` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 24 / 114 |
| Prompt | [`planning/migration/video.productiondesign.md`](./video.productiondesign.md) |
| Folder | `business/video/agents/video.productiondesign` |

#### Implement

- [ ] Execute full prompt [`video.productiondesign.md`](./video.productiondesign.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.productiondesign/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.productiondesign/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.productiondesign/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-024)
- [ ] Master table status → `done`

---
### T-025 — `video.costumedesign` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 25 / 114 |
| Prompt | [`planning/migration/video.costumedesign.md`](./video.costumedesign.md) |
| Folder | `business/video/agents/video.costumedesign` |

#### Implement

- [ ] Execute full prompt [`video.costumedesign.md`](./video.costumedesign.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.costumedesign/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.costumedesign/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.costumedesign/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-025)
- [ ] Master table status → `done`

---
### T-026 — `video.mua_makeup` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 26 / 114 |
| Prompt | [`planning/migration/video.mua_makeup.md`](./video.mua_makeup.md) |
| Folder | `business/video/agents/video.mua_makeup` |

#### Implement

- [ ] Execute full prompt [`video.mua_makeup.md`](./video.mua_makeup.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.mua_makeup/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.mua_makeup/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.mua_makeup/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-026)
- [ ] Master table status → `done`

---
### T-027 — `video.sounddesign` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 27 / 114 |
| Prompt | [`planning/migration/video.sounddesign.md`](./video.sounddesign.md) |
| Folder | `business/video/agents/video.sounddesign` |

#### Implement

- [x] Execute full prompt [`video.sounddesign.md`](./video.sounddesign.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.sounddesign/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.sounddesign/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.sounddesign/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-027)
- [ ] Master table status → `done`

---
### T-028 — `video.composer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 28 / 114 |
| Prompt | [`planning/migration/video.composer.md`](./video.composer.md) |
| Folder | `business/video/agents/video.composer` |

#### Implement

- [x] Execute full prompt [`video.composer.md`](./video.composer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.composer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.composer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.composer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-028)
- [ ] Master table status → `done`

---
### T-029 — `video.voiceover` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 29 / 114 |
| Prompt | [`planning/migration/video.voiceover.md`](./video.voiceover.md) |
| Folder | `business/video/agents/video.voiceover` |

#### Implement

- [x] Execute full prompt [`video.voiceover.md`](./video.voiceover.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.voiceover/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.voiceover/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.voiceover/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-029)
- [ ] Master table status → `done`

---
### T-030 — `video.soundmixer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 30 / 114 |
| Prompt | [`planning/migration/video.soundmixer.md`](./video.soundmixer.md) |
| Folder | `business/video/agents/video.soundmixer` |

#### Implement

- [x] Execute full prompt [`video.soundmixer.md`](./video.soundmixer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.soundmixer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.soundmixer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.soundmixer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-030)
- [ ] Master table status → `done`

---
### T-031 — `video.choreography` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 31 / 114 |
| Prompt | [`planning/migration/video.choreography.md`](./video.choreography.md) |
| Folder | `business/video/agents/video.choreography` |

#### Implement

- [ ] Execute full prompt [`video.choreography.md`](./video.choreography.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.choreography/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.choreography/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.choreography/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-031)
- [ ] Master table status → `done`

---
### T-032 — `video.musicvideodirector` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 32 / 114 |
| Prompt | [`planning/migration/video.musicvideodirector.md`](./video.musicvideodirector.md) |
| Folder | `business/video/agents/video.musicvideodirector` |

#### Implement

- [ ] Execute full prompt [`video.musicvideodirector.md`](./video.musicvideodirector.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.musicvideodirector/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.musicvideodirector/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.musicvideodirector/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-032)
- [ ] Master table status → `done`

---
### T-033 — `video.comedywriter` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 33 / 114 |
| Prompt | [`planning/migration/video.comedywriter.md`](./video.comedywriter.md) |
| Folder | `business/video/agents/video.comedywriter` |

#### Implement

- [ ] Execute full prompt [`video.comedywriter.md`](./video.comedywriter.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.comedywriter/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.comedywriter/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.comedywriter/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-033)
- [ ] Master table status → `done`

---
### T-034 — `video.talent` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 34 / 114 |
| Prompt | [`planning/migration/video.talent.md`](./video.talent.md) |
| Folder | `business/video/agents/video.talent` |

#### Implement

- [ ] Execute full prompt [`video.talent.md`](./video.talent.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.talent/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.talent/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.talent/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **94** |


- [ ] **Final score = 100** (required to close T-034)
- [ ] Master table status → `done`

---
### T-035 — `video.ugccreator` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 35 / 114 |
| Prompt | [`planning/migration/video.ugccreator.md`](./video.ugccreator.md) |
| Folder | `business/video/agents/video.ugccreator` |

#### Implement

- [ ] Execute full prompt [`video.ugccreator.md`](./video.ugccreator.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.ugccreator/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.ugccreator/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.ugccreator/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 8 |
| **Total** | **100** | **86** |


- [ ] **Final score = 100** (required to close T-035)
- [ ] Master table status → `done`

---
### T-036 — `video.socialmediastrategist` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 36 / 114 |
| Prompt | [`planning/migration/video.socialmediastrategist.md`](./video.socialmediastrategist.md) |
| Folder | `business/video/agents/video.socialmediastrategist` |

#### Implement

- [ ] Execute full prompt [`video.socialmediastrategist.md`](./video.socialmediastrategist.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.socialmediastrategist/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.socialmediastrategist/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.socialmediastrategist/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-036)
- [ ] Master table status → `done`

---
### T-037 — `video.copywriter` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 37 / 114 |
| Prompt | [`planning/migration/video.copywriter.md`](./video.copywriter.md) |
| Folder | `business/video/agents/video.copywriter` |

#### Implement

- [ ] Execute full prompt [`video.copywriter.md`](./video.copywriter.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.copywriter/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.copywriter/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.copywriter/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **94** |


- [ ] **Final score = 100** (required to close T-037)
- [ ] Master table status → `done`

---
### T-038 — `video.creativedirector` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 38 / 114 |
| Prompt | [`planning/migration/video.creativedirector.md`](./video.creativedirector.md) |
| Folder | `business/video/agents/video.creativedirector` |

#### Implement

- [ ] Execute full prompt [`video.creativedirector.md`](./video.creativedirector.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.creativedirector/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.creativedirector/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.creativedirector/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-038)
- [ ] Master table status → `done`

---
### T-039 — `video.performancemarketer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 39 / 114 |
| Prompt | [`planning/migration/video.performancemarketer.md`](./video.performancemarketer.md) |
| Folder | `business/video/agents/video.performancemarketer` |

#### Implement

- [x] Execute full prompt [`video.performancemarketer.md`](./video.performancemarketer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.performancemarketer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.performancemarketer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.performancemarketer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-039)
- [ ] Master table status → `done`

---
### T-040 — `video.instructionaldesign` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 40 / 114 |
| Prompt | [`planning/migration/video.instructionaldesign.md`](./video.instructionaldesign.md) |
| Folder | `business/video/agents/video.instructionaldesign` |

#### Implement

- [ ] Execute full prompt [`video.instructionaldesign.md`](./video.instructionaldesign.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.instructionaldesign/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.instructionaldesign/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.instructionaldesign/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-040)
- [ ] Master table status → `done`

---
### T-041 — `video.sme` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 41 / 114 |
| Prompt | [`planning/migration/video.sme.md`](./video.sme.md) |
| Folder | `business/video/agents/video.sme` |

#### Implement

- [ ] Execute full prompt [`video.sme.md`](./video.sme.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.sme/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.sme/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.sme/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **94** |


- [ ] **Final score = 100** (required to close T-041)
- [ ] Master table status → `done`

---
### T-042 — `video.factchecker` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 42 / 114 |
| Prompt | [`planning/migration/video.factchecker.md`](./video.factchecker.md) |
| Folder | `business/video/agents/video.factchecker` |

#### Implement

- [ ] Execute full prompt [`video.factchecker.md`](./video.factchecker.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.factchecker/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.factchecker/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.factchecker/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-042)
- [ ] Master table status → `done`

---
### T-043 — `video.medicalillustrator` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 43 / 114 |
| Prompt | [`planning/migration/video.medicalillustrator.md`](./video.medicalillustrator.md) |
| Folder | `business/video/agents/video.medicalillustrator` |

#### Implement

- [ ] Execute full prompt [`video.medicalillustrator.md`](./video.medicalillustrator.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.medicalillustrator/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.medicalillustrator/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.medicalillustrator/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-043)
- [ ] Master table status → `done`

---
### T-044 — `video.journalist` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 44 / 114 |
| Prompt | [`planning/migration/video.journalist.md`](./video.journalist.md) |
| Folder | `business/video/agents/video.journalist` |

#### Implement

- [x] Execute full prompt [`video.journalist.md`](./video.journalist.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.journalist/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.journalist/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.journalist/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-044)
- [ ] Master table status → `done`

---
### T-045 — `video.compliance` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 45 / 114 |
| Prompt | [`planning/migration/video.compliance.md`](./video.compliance.md) |
| Folder | `business/video/agents/video.compliance` |

#### Implement

- [x] Execute full prompt [`video.compliance.md`](./video.compliance.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.compliance/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.compliance/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.compliance/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-045)
- [ ] Master table status → `done`

---
### T-046 — `video.finance` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 46 / 114 |
| Prompt | [`planning/migration/video.finance.md`](./video.finance.md) |
| Folder | `business/video/agents/video.finance` |

#### Implement

- [ ] Execute full prompt [`video.finance.md`](./video.finance.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.finance/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.finance/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.finance/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-046)
- [ ] Master table status → `done`

---
### T-047 — `video.foodstylist` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 47 / 114 |
| Prompt | [`planning/migration/video.foodstylist.md`](./video.foodstylist.md) |
| Folder | `business/video/agents/video.foodstylist` |

#### Implement

- [ ] Execute full prompt [`video.foodstylist.md`](./video.foodstylist.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.foodstylist/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.foodstylist/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.foodstylist/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-047)
- [ ] Master table status → `done`

---
### T-048 — `video.travelcine` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 48 / 114 |
| Prompt | [`planning/migration/video.travelcine.md`](./video.travelcine.md) |
| Folder | `business/video/agents/video.travelcine` |

#### Implement

- [ ] Execute full prompt [`video.travelcine.md`](./video.travelcine.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.travelcine/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.travelcine/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.travelcine/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-048)
- [ ] Master table status → `done`

---
### T-049 — `video.childrensauthor` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 49 / 114 |
| Prompt | [`planning/migration/video.childrensauthor.md`](./video.childrensauthor.md) |
| Folder | `business/video/agents/video.childrensauthor` |

#### Implement

- [x] Execute full prompt [`video.childrensauthor.md`](./video.childrensauthor.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.childrensauthor/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.childrensauthor/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.childrensauthor/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-049)
- [ ] Master table status → `done`

---
### T-050 — `video.audiobooknarrator` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 50 / 114 |
| Prompt | [`planning/migration/video.audiobooknarrator.md`](./video.audiobooknarrator.md) |
| Folder | `business/video/agents/video.audiobooknarrator` |

#### Implement

- [x] Execute full prompt [`video.audiobooknarrator.md`](./video.audiobooknarrator.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.audiobooknarrator/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.audiobooknarrator/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.audiobooknarrator/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-050)
- [ ] Master table status → `done`

---
### T-051 — `video.signlanguageinterpreter` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 51 / 114 |
| Prompt | [`planning/migration/video.signlanguageinterpreter.md`](./video.signlanguageinterpreter.md) |
| Folder | `business/video/agents/video.signlanguageinterpreter` |

#### Implement

- [ ] Execute full prompt [`video.signlanguageinterpreter.md`](./video.signlanguageinterpreter.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.signlanguageinterpreter/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.signlanguageinterpreter/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.signlanguageinterpreter/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-051)
- [ ] Master table status → `done`

---
### T-052 — `video.localizationqa` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 52 / 114 |
| Prompt | [`planning/migration/video.localizationqa.md`](./video.localizationqa.md) |
| Folder | `business/video/agents/video.localizationqa` |

#### Implement

- [ ] Execute full prompt [`video.localizationqa.md`](./video.localizationqa.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.localizationqa/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.localizationqa/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.localizationqa/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-052)
- [ ] Master table status → `done`

---
### T-053 — `video.realestatephoto` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 53 / 114 |
| Prompt | [`planning/migration/video.realestatephoto.md`](./video.realestatephoto.md) |
| Folder | `business/video/agents/video.realestatephoto` |

#### Implement

- [ ] Execute full prompt [`video.realestatephoto.md`](./video.realestatephoto.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.realestatephoto/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.realestatephoto/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.realestatephoto/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-053)
- [ ] Master table status → `done`

---
### T-054 — `video.promptengineer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 54 / 114 |
| Prompt | [`planning/migration/video.promptengineer.md`](./video.promptengineer.md) |
| Folder | `business/video/agents/video.promptengineer` |

#### Implement

- [x] Execute full prompt [`video.promptengineer.md`](./video.promptengineer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.promptengineer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.promptengineer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.promptengineer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-054)
- [ ] Master table status → `done`

---
### T-055 — `video.avatardesign` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 55 / 114 |
| Prompt | [`planning/migration/video.avatardesign.md`](./video.avatardesign.md) |
| Folder | `business/video/agents/video.avatardesign` |

#### Implement

- [ ] Execute full prompt [`video.avatardesign.md`](./video.avatardesign.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.avatardesign/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.avatardesign/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.avatardesign/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-055)
- [ ] Master table status → `done`

---
### T-056 — `video.voiceclone` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 56 / 114 |
| Prompt | [`planning/migration/video.voiceclone.md`](./video.voiceclone.md) |
| Folder | `business/video/agents/video.voiceclone` |

#### Implement

- [ ] Execute full prompt [`video.voiceclone.md`](./video.voiceclone.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.voiceclone/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.voiceclone/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.voiceclone/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-056)
- [ ] Master table status → `done`

---
### T-057 — `video.personalizationengineer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 57 / 114 |
| Prompt | [`planning/migration/video.personalizationengineer.md`](./video.personalizationengineer.md) |
| Folder | `business/video/agents/video.personalizationengineer` |

#### Implement

- [x] Execute full prompt [`video.personalizationengineer.md`](./video.personalizationengineer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.personalizationengineer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.personalizationengineer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.personalizationengineer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-057)
- [ ] Master table status → `done`

---
### T-058 — `video.trailereditor` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 58 / 114 |
| Prompt | [`planning/migration/video.trailereditor.md`](./video.trailereditor.md) |
| Folder | `business/video/agents/video.trailereditor` |

#### Implement

- [ ] Execute full prompt [`video.trailereditor.md`](./video.trailereditor.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.trailereditor/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.trailereditor/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.trailereditor/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-058)
- [ ] Master table status → `done`

---
### T-059 — `video.sportsanalyst` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 59 / 114 |
| Prompt | [`planning/migration/video.sportsanalyst.md`](./video.sportsanalyst.md) |
| Folder | `business/video/agents/video.sportsanalyst` |

#### Implement

- [ ] Execute full prompt [`video.sportsanalyst.md`](./video.sportsanalyst.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.sportsanalyst/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.sportsanalyst/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.sportsanalyst/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 8 |
| **Total** | **100** | **86** |


- [ ] **Final score = 100** (required to close T-059)
- [ ] Master table status → `done`

---
### T-060 — `video.ideation` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 60 / 114 |
| Prompt | [`planning/migration/video.ideation.md`](./video.ideation.md) |
| Folder | `business/video/agents/video.ideation` |

#### Implement

- [x] Execute full prompt [`video.ideation.md`](./video.ideation.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.ideation/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.ideation/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.ideation/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-060)
- [ ] Master table status → `done`

---
### T-061 — `video.narrativearc` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 61 / 114 |
| Prompt | [`planning/migration/video.narrativearc.md`](./video.narrativearc.md) |
| Folder | `business/video/agents/video.narrativearc` |

#### Implement

- [ ] Execute full prompt [`video.narrativearc.md`](./video.narrativearc.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.narrativearc/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.narrativearc/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.narrativearc/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-061)
- [ ] Master table status → `done`

---
### T-062 — `video.styletransfer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 62 / 114 |
| Prompt | [`planning/migration/video.styletransfer.md`](./video.styletransfer.md) |
| Folder | `business/video/agents/video.styletransfer` |

#### Implement

- [ ] Execute full prompt [`video.styletransfer.md`](./video.styletransfer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.styletransfer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.styletransfer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.styletransfer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-062)
- [ ] Master table status → `done`

---
### T-063 — `video.worldbuilding` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 63 / 114 |
| Prompt | [`planning/migration/video.worldbuilding.md`](./video.worldbuilding.md) |
| Folder | `business/video/agents/video.worldbuilding` |

#### Implement

- [ ] Execute full prompt [`video.worldbuilding.md`](./video.worldbuilding.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.worldbuilding/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.worldbuilding/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.worldbuilding/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-063)
- [ ] Master table status → `done`

---
### T-064 — `video.moodboard` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 64 / 114 |
| Prompt | [`planning/migration/video.moodboard.md`](./video.moodboard.md) |
| Folder | `business/video/agents/video.moodboard` |

#### Implement

- [ ] Execute full prompt [`video.moodboard.md`](./video.moodboard.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.moodboard/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.moodboard/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.moodboard/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-064)
- [ ] Master table status → `done`

---
### T-065 — `video.novelty` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 65 / 114 |
| Prompt | [`planning/migration/video.novelty.md`](./video.novelty.md) |
| Folder | `business/video/agents/video.novelty` |

#### Implement

- [ ] Execute full prompt [`video.novelty.md`](./video.novelty.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.novelty/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.novelty/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.novelty/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-065)
- [ ] Master table status → `done`

---
### T-066 — `video.emotionalarc` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 66 / 114 |
| Prompt | [`planning/migration/video.emotionalarc.md`](./video.emotionalarc.md) |
| Folder | `business/video/agents/video.emotionalarc` |

#### Implement

- [x] Execute full prompt [`video.emotionalarc.md`](./video.emotionalarc.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.emotionalarc/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.emotionalarc/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.emotionalarc/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-066)
- [ ] Master table status → `done`

---
### T-067 — `video.archiveresearch` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 67 / 114 |
| Prompt | [`planning/migration/video.archiveresearch.md`](./video.archiveresearch.md) |
| Folder | `business/video/agents/video.archiveresearch` |

#### Implement

- [x] Execute full prompt [`video.archiveresearch.md`](./video.archiveresearch.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.archiveresearch/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.archiveresearch/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.archiveresearch/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-067)
- [ ] Master table status → `done`

---
### T-068 — `video.trendintelligence` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 68 / 114 |
| Prompt | [`planning/migration/video.trendintelligence.md`](./video.trendintelligence.md) |
| Folder | `business/video/agents/video.trendintelligence` |

#### Implement

- [ ] Execute full prompt [`video.trendintelligence.md`](./video.trendintelligence.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.trendintelligence/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.trendintelligence/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.trendintelligence/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-068)
- [ ] Master table status → `done`

---
### T-069 — `video.competitorintelligence` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 69 / 114 |
| Prompt | [`planning/migration/video.competitorintelligence.md`](./video.competitorintelligence.md) |
| Folder | `business/video/agents/video.competitorintelligence` |

#### Implement

- [ ] Execute full prompt [`video.competitorintelligence.md`](./video.competitorintelligence.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.competitorintelligence/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.competitorintelligence/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.competitorintelligence/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-069)
- [ ] Master table status → `done`

---
### T-070 — `video.citation` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 70 / 114 |
| Prompt | [`planning/migration/video.citation.md`](./video.citation.md) |
| Folder | `business/video/agents/video.citation` |

#### Implement

- [x] Execute full prompt [`video.citation.md`](./video.citation.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.citation/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.citation/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.citation/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-070)
- [ ] Master table status → `done`

---
### T-071 — `video.interviewsynthesis` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 71 / 114 |
| Prompt | [`planning/migration/video.interviewsynthesis.md`](./video.interviewsynthesis.md) |
| Folder | `business/video/agents/video.interviewsynthesis` |

#### Implement

- [x] Execute full prompt [`video.interviewsynthesis.md`](./video.interviewsynthesis.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.interviewsynthesis/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.interviewsynthesis/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.interviewsynthesis/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-071)
- [ ] Master table status → `done`

---
### T-072 — `video.benchmarkresearch` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 72 / 114 |
| Prompt | [`planning/migration/video.benchmarkresearch.md`](./video.benchmarkresearch.md) |
| Folder | `business/video/agents/video.benchmarkresearch` |

#### Implement

- [x] Execute full prompt [`video.benchmarkresearch.md`](./video.benchmarkresearch.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.benchmarkresearch/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.benchmarkresearch/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.benchmarkresearch/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-072)
- [ ] Master table status → `done`

---
### T-073 — `video.promptoptimizer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 73 / 114 |
| Prompt | [`planning/migration/video.promptoptimizer.md`](./video.promptoptimizer.md) |
| Folder | `business/video/agents/video.promptoptimizer` |

#### Implement

- [ ] Execute full prompt [`video.promptoptimizer.md`](./video.promptoptimizer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.promptoptimizer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.promptoptimizer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.promptoptimizer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-073)
- [ ] Master table status → `done`

---
### T-074 — `video.costoptimizer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 74 / 114 |
| Prompt | [`planning/migration/video.costoptimizer.md`](./video.costoptimizer.md) |
| Folder | `business/video/agents/video.costoptimizer` |

#### Implement

- [ ] Execute full prompt [`video.costoptimizer.md`](./video.costoptimizer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.costoptimizer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.costoptimizer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.costoptimizer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-074)
- [ ] Master table status → `done`

---
### T-075 — `video.latencyoptimizer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 75 / 114 |
| Prompt | [`planning/migration/video.latencyoptimizer.md`](./video.latencyoptimizer.md) |
| Folder | `business/video/agents/video.latencyoptimizer` |

#### Implement

- [ ] Execute full prompt [`video.latencyoptimizer.md`](./video.latencyoptimizer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.latencyoptimizer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.latencyoptimizer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.latencyoptimizer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-075)
- [ ] Master table status → `done`

---
### T-076 — `video.retentionoptimizer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 76 / 114 |
| Prompt | [`planning/migration/video.retentionoptimizer.md`](./video.retentionoptimizer.md) |
| Folder | `business/video/agents/video.retentionoptimizer` |

#### Implement

- [x] Execute full prompt [`video.retentionoptimizer.md`](./video.retentionoptimizer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.retentionoptimizer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.retentionoptimizer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.retentionoptimizer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-076)
- [ ] Master table status → `done`

---
### T-077 — `video.roasoptimizer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 77 / 114 |
| Prompt | [`planning/migration/video.roasoptimizer.md`](./video.roasoptimizer.md) |
| Folder | `business/video/agents/video.roasoptimizer` |

#### Implement

- [ ] Execute full prompt [`video.roasoptimizer.md`](./video.roasoptimizer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.roasoptimizer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.roasoptimizer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.roasoptimizer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-077)
- [ ] Master table status → `done`

---
### T-078 — `video.accessibilityoptimizer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 78 / 114 |
| Prompt | [`planning/migration/video.accessibilityoptimizer.md`](./video.accessibilityoptimizer.md) |
| Folder | `business/video/agents/video.accessibilityoptimizer` |

#### Implement

- [ ] Execute full prompt [`video.accessibilityoptimizer.md`](./video.accessibilityoptimizer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.accessibilityoptimizer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.accessibilityoptimizer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.accessibilityoptimizer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-078)
- [ ] Master table status → `done`

---
### T-079 — `video.evaluationharness` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 79 / 114 |
| Prompt | [`planning/migration/video.evaluationharness.md`](./video.evaluationharness.md) |
| Folder | `business/video/agents/video.evaluationharness` |

#### Implement

- [x] Execute full prompt [`video.evaluationharness.md`](./video.evaluationharness.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.evaluationharness/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.evaluationharness/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.evaluationharness/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-079)
- [ ] Master table status → `done`

---
### T-080 — `video.safetyredteam` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 80 / 114 |
| Prompt | [`planning/migration/video.safetyredteam.md`](./video.safetyredteam.md) |
| Folder | `business/video/agents/video.safetyredteam` |

#### Implement

- [ ] Execute full prompt [`video.safetyredteam.md`](./video.safetyredteam.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.safetyredteam/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.safetyredteam/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.safetyredteam/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-080)
- [ ] Master table status → `done`

---
### T-081 — `video.analyst` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 81 / 114 |
| Prompt | [`planning/migration/video.analyst.md`](./video.analyst.md) |
| Folder | `business/video/agents/video.analyst` |

#### Implement

- [x] Execute full prompt [`video.analyst.md`](./video.analyst.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.analyst/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.analyst/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.analyst/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-081)
- [ ] Master table status → `done`

---
### T-082 — `video.audiencesim` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 82 / 114 |
| Prompt | [`planning/migration/video.audiencesim.md`](./video.audiencesim.md) |
| Folder | `business/video/agents/video.audiencesim` |

#### Implement

- [x] Execute full prompt [`video.audiencesim.md`](./video.audiencesim.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.audiencesim/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.audiencesim/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.audiencesim/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-082)
- [ ] Master table status → `done`

---
### T-083 — `video.accessibility` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 83 / 114 |
| Prompt | [`planning/migration/video.accessibility.md`](./video.accessibility.md) |
| Folder | `business/video/agents/video.accessibility` |

#### Implement

- [x] Execute full prompt [`video.accessibility.md`](./video.accessibility.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.accessibility/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.accessibility/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.accessibility/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-083)
- [ ] Master table status → `done`

---
### T-084 — `video.brand` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 84 / 114 |
| Prompt | [`planning/migration/video.brand.md`](./video.brand.md) |
| Folder | `business/video/agents/video.brand` |

#### Implement

- [x] Execute full prompt [`video.brand.md`](./video.brand.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.brand/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.brand/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.brand/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-084)
- [ ] Master table status → `done`

---
### T-085 — `video.brandstrategist` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 85 / 114 |
| Prompt | [`planning/migration/video.brandstrategist.md`](./video.brandstrategist.md) |
| Folder | `business/video/agents/video.brandstrategist` |

#### Implement

- [x] Execute full prompt [`video.brandstrategist.md`](./video.brandstrategist.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.brandstrategist/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.brandstrategist/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.brandstrategist/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-085)
- [ ] Master table status → `done`

---
### T-086 — `video.marketing` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 86 / 114 |
| Prompt | [`planning/migration/video.marketing.md`](./video.marketing.md) |
| Folder | `business/video/agents/video.marketing` |

#### Implement

- [x] Execute full prompt [`video.marketing.md`](./video.marketing.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.marketing/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.marketing/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.marketing/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-086)
- [ ] Master table status → `done`

---
### T-087 — `video.seo` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 87 / 114 |
| Prompt | [`planning/migration/video.seo.md`](./video.seo.md) |
| Folder | `business/video/agents/video.seo` |

#### Implement

- [x] Execute full prompt [`video.seo.md`](./video.seo.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.seo/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.seo/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.seo/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-087)
- [ ] Master table status → `done`

---
### T-088 — `video.community` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 88 / 114 |
| Prompt | [`planning/migration/video.community.md`](./video.community.md) |
| Folder | `business/video/agents/video.community` |

#### Implement

- [x] Execute full prompt [`video.community.md`](./video.community.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.community/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.community/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.community/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-088)
- [ ] Master table status → `done`

---
### T-089 — `video.templatedesign` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 89 / 114 |
| Prompt | [`planning/migration/video.templatedesign.md`](./video.templatedesign.md) |
| Folder | `business/video/agents/video.templatedesign` |

#### Implement

- [x] Execute full prompt [`video.templatedesign.md`](./video.templatedesign.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.templatedesign/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.templatedesign/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.templatedesign/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-089)
- [ ] Master table status → `done`

---
### T-090 — `video.ux` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 90 / 114 |
| Prompt | [`planning/migration/video.ux.md`](./video.ux.md) |
| Folder | `business/video/agents/video.ux` |

#### Implement

- [ ] Execute full prompt [`video.ux.md`](./video.ux.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.ux/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.ux/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.ux/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 16 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **88** |


- [ ] **Final score = 100** (required to close T-090)
- [ ] Master table status → `done`

---
### T-091 — `video.trustsafety` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 91 / 114 |
| Prompt | [`planning/migration/video.trustsafety.md`](./video.trustsafety.md) |
| Folder | `business/video/agents/video.trustsafety` |

#### Implement

- [ ] Execute full prompt [`video.trustsafety.md`](./video.trustsafety.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.trustsafety/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.trustsafety/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.trustsafety/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-091)
- [ ] Master table status → `done`

---
### T-092 — `video.crm` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 92 / 114 |
| Prompt | [`planning/migration/video.crm.md`](./video.crm.md) |
| Folder | `business/video/agents/video.crm` |

#### Implement

- [ ] Execute full prompt [`video.crm.md`](./video.crm.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.crm/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.crm/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.crm/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-092)
- [ ] Master table status → `done`

---
### T-093 — `video.legal` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 93 / 114 |
| Prompt | [`planning/migration/video.legal.md`](./video.legal.md) |
| Folder | `business/video/agents/video.legal` |

#### Implement

- [ ] Execute full prompt [`video.legal.md`](./video.legal.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.legal/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.legal/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.legal/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **94** |


- [ ] **Final score = 100** (required to close T-093)
- [ ] Master table status → `done`

---
### T-094 — `video.festivalstrategist` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 94 / 114 |
| Prompt | [`planning/migration/video.festivalstrategist.md`](./video.festivalstrategist.md) |
| Folder | `business/video/agents/video.festivalstrategist` |

#### Implement

- [ ] Execute full prompt [`video.festivalstrategist.md`](./video.festivalstrategist.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.festivalstrategist/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.festivalstrategist/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.festivalstrategist/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 16 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **88** |


- [ ] **Final score = 100** (required to close T-094)
- [ ] Master table status → `done`

---
### T-095 — `video.critic` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 95 / 114 |
| Prompt | [`planning/migration/video.critic.md`](./video.critic.md) |
| Folder | `business/video/agents/video.critic` |

#### Implement

- [x] Execute full prompt [`video.critic.md`](./video.critic.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.critic/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.critic/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.critic/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-095)
- [ ] Master table status → `done`

---
### T-096 — `video.lms` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 96 / 114 |
| Prompt | [`planning/migration/video.lms.md`](./video.lms.md) |
| Folder | `business/video/agents/video.lms` |

#### Implement

- [x] Execute full prompt [`video.lms.md`](./video.lms.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.lms/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.lms/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.lms/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-096)
- [ ] Master table status → `done`

---
### T-097 — `video.learnersim` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 97 / 114 |
| Prompt | [`planning/migration/video.learnersim.md`](./video.learnersim.md) |
| Folder | `business/video/agents/video.learnersim` |

#### Implement

- [ ] Execute full prompt [`video.learnersim.md`](./video.learnersim.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.learnersim/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.learnersim/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.learnersim/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **95** |


- [ ] **Final score = 100** (required to close T-097)
- [ ] Master table status → `done`

---
### T-098 — `video.continuity` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 98 / 114 |
| Prompt | [`planning/migration/video.continuity.md`](./video.continuity.md) |
| Folder | `business/video/agents/video.continuity` |

#### Implement

- [x] Execute full prompt [`video.continuity.md`](./video.continuity.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.continuity/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.continuity/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.continuity/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-098)
- [ ] Master table status → `done`

---
### T-099 — `video.lipsync` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 99 / 114 |
| Prompt | [`planning/migration/video.lipsync.md`](./video.lipsync.md) |
| Folder | `business/video/agents/video.lipsync` |

#### Implement

- [x] Execute full prompt [`video.lipsync.md`](./video.lipsync.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.lipsync/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.lipsync/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.lipsync/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-099)
- [ ] Master table status → `done`

---
### T-100 — `video.musicsupervisor` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 100 / 114 |
| Prompt | [`planning/migration/video.musicsupervisor.md`](./video.musicsupervisor.md) |
| Folder | `business/video/agents/video.musicsupervisor` |

#### Implement

- [x] Execute full prompt [`video.musicsupervisor.md`](./video.musicsupervisor.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.musicsupervisor/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.musicsupervisor/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.musicsupervisor/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-100)
- [ ] Master table status → `done`

---
### T-101 — `video.labela_r` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 101 / 114 |
| Prompt | [`planning/migration/video.labela_r.md`](./video.labela_r.md) |
| Folder | `business/video/agents/video.labela_r` |

#### Implement

- [ ] Execute full prompt [`video.labela_r.md`](./video.labela_r.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.labela_r/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.labela_r/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.labela_r/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 16 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **88** |


- [ ] **Final score = 100** (required to close T-101)
- [ ] Master table status → `done`

---
### T-102 — `video.labeldigital` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 102 / 114 |
| Prompt | [`planning/migration/video.labeldigital.md`](./video.labeldigital.md) |
| Folder | `business/video/agents/video.labeldigital` |

#### Implement

- [ ] Execute full prompt [`video.labeldigital.md`](./video.labeldigital.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.labeldigital/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.labeldigital/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.labeldigital/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 16 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **88** |


- [ ] **Final score = 100** (required to close T-102)
- [ ] Master table status → `done`

---
### T-103 — `video.deepfakedetection` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 103 / 114 |
| Prompt | [`planning/migration/video.deepfakedetection.md`](./video.deepfakedetection.md) |
| Folder | `business/video/agents/video.deepfakedetection` |

#### Implement

- [ ] Execute full prompt [`video.deepfakedetection.md`](./video.deepfakedetection.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.deepfakedetection/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.deepfakedetection/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.deepfakedetection/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-103)
- [ ] Master table status → `done`

---
### T-104 — `video.comms` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 104 / 114 |
| Prompt | [`planning/migration/video.comms.md`](./video.comms.md) |
| Folder | `business/video/agents/video.comms` |

#### Implement

- [ ] Execute full prompt [`video.comms.md`](./video.comms.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.comms/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.comms/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.comms/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-104)
- [ ] Master table status → `done`

---
### T-105 — `video.archiveproducer` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 105 / 114 |
| Prompt | [`planning/migration/video.archiveproducer.md`](./video.archiveproducer.md) |
| Folder | `business/video/agents/video.archiveproducer` |

#### Implement

- [ ] Execute full prompt [`video.archiveproducer.md`](./video.archiveproducer.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.archiveproducer/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.archiveproducer/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.archiveproducer/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 16 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **88** |


- [ ] **Final score = 100** (required to close T-105)
- [ ] Master table status → `done`

---
### T-106 — `video.standardseditor` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 106 / 114 |
| Prompt | [`planning/migration/video.standardseditor.md`](./video.standardseditor.md) |
| Folder | `business/video/agents/video.standardseditor` |

#### Implement

- [ ] Execute full prompt [`video.standardseditor.md`](./video.standardseditor.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.standardseditor/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.standardseditor/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.standardseditor/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-106)
- [ ] Master table status → `done`

---
### T-107 — `video.ethics` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 107 / 114 |
| Prompt | [`planning/migration/video.ethics.md`](./video.ethics.md) |
| Folder | `business/video/agents/video.ethics` |

#### Implement

- [ ] Execute full prompt [`video.ethics.md`](./video.ethics.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.ethics/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.ethics/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.ethics/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **94** |


- [ ] **Final score = 100** (required to close T-107)
- [ ] Master table status → `done`

---
### T-108 — `video.channelmanager` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 108 / 114 |
| Prompt | [`planning/migration/video.channelmanager.md`](./video.channelmanager.md) |
| Folder | `business/video/agents/video.channelmanager` |

#### Implement

- [ ] Execute full prompt [`video.channelmanager.md`](./video.channelmanager.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.channelmanager/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.channelmanager/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.channelmanager/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-108)
- [ ] Master table status → `done`

---
### T-109 — `video.corrections` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 109 / 114 |
| Prompt | [`planning/migration/video.corrections.md`](./video.corrections.md) |
| Folder | `business/video/agents/video.corrections` |

#### Implement

- [ ] Execute full prompt [`video.corrections.md`](./video.corrections.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.corrections/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.corrections/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.corrections/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-109)
- [ ] Master table status → `done`

---
### T-110 — `video.mpa` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 110 / 114 |
| Prompt | [`planning/migration/video.mpa.md`](./video.mpa.md) |
| Folder | `business/video/agents/video.mpa` |

#### Implement

- [x] Execute full prompt [`video.mpa.md`](./video.mpa.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.mpa/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.mpa/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.mpa/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 25 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 12 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **96** |


- [ ] **Final score = 100** (required to close T-110)
- [ ] Master table status → `done`

---
### T-111 — `video.sales` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 111 / 114 |
| Prompt | [`planning/migration/video.sales.md`](./video.sales.md) |
| Folder | `business/video/agents/video.sales` |

#### Implement

- [ ] Execute full prompt [`video.sales.md`](./video.sales.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.sales/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.sales/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.sales/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-111)
- [ ] Master table status → `done`

---
### T-112 — `video.distributor` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 112 / 114 |
| Prompt | [`planning/migration/video.distributor.md`](./video.distributor.md) |
| Folder | `business/video/agents/video.distributor` |

#### Implement

- [ ] Execute full prompt [`video.distributor.md`](./video.distributor.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.distributor/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.distributor/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.distributor/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 24 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **94** |


- [ ] **Final score = 100** (required to close T-112)
- [ ] Master table status → `done`

---
### T-113 — `video.awardsstrategist` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 113 / 114 |
| Prompt | [`planning/migration/video.awardsstrategist.md`](./video.awardsstrategist.md) |
| Folder | `business/video/agents/video.awardsstrategist` |

#### Implement

- [ ] Execute full prompt [`video.awardsstrategist.md`](./video.awardsstrategist.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.awardsstrategist/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.awardsstrategist/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.awardsstrategist/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 16 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **88** |


- [ ] **Final score = 100** (required to close T-113)
- [ ] Master table status → `done`

---
### T-114 — `video.archivemaster` — **must score 100**

| Field | Value |
|-------|-------|
| Order | 114 / 114 |
| Prompt | [`planning/migration/video.archivemaster.md`](./video.archivemaster.md) |
| Folder | `business/video/agents/video.archivemaster` |

#### Implement

- [ ] Execute full prompt [`video.archivemaster.md`](./video.archivemaster.md) (corpus + va; un-summarized)
- [x] Update `business/video/agents/video.archivemaster/SPEC.md` to self-contained definition (no refer-only stubs)
- [x] Confirm/update `business/video/agents/video.archivemaster/agent_spec.json` ALC + tools policy (design vs runtime)
- [x] Populate `business/video/agents/video.archivemaster/sources/` when deep docs apply (or fully embed in SPEC)
- [x] Integrate **this agent’s** capability research (arXiv / X / YouTube per prompt — not a copy of another agent)

#### Review

- [x] S6 checklist all items ✓
- [ ] Critic pass: no P0 gaps vs corpus for this role
- [x] N1/N3 constraints respected

#### Scorecard (earned must equal max for each row)

| Dim | Max | Earned |
|-----|----:|-------:|
| S1 Self-contained SPEC | 25 | 22 |
| S2 Corpus fidelity | 20 | 20 |
| S3 Prompt execution | 15 | 11 |
| S4 Runtime binding | 15 | 15 |
| S5 Reachability | 10 | 10 |
| S6 Review quality | 15 | 14 |
| **Total** | **100** | **92** |


- [ ] **Final score = 100** (required to close T-114)
- [ ] Master table status → `done`

---

## Progress log

| Date | seq range | count at 100 | notes |
|------|-----------|-------------:|-------|
| 2026-07-13 | — | 0 / 114 | tasks.md created: implement + review + score 100 per agent |

## Related

- [`agent_implement_order_list.md`](./agent_implement_order_list.md)
- [`README.md`](./README.md) — prompt index
- [`../../migration_plan.md`](../../migration_plan.md)
- `python scripts/business/inventory_check.py`
- `python scripts/business/check_video_corpus_standalone.py`
