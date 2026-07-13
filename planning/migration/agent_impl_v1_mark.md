# Agent implementation v1 marks

**Date:** 2026-07-13  
**Scope:** all 114 video agents under `business/video/agents/`  
**Rubric:** S1–S6 from `planning/migration/tasks.md` (max 100)  
**Pass rule:** true complete only at **100**; v1 does **not** award automatic 100.

## Executive summary

| Metric | Value |
|--------|------:|
| Agents judged | 114 |
| Mean score | 93.8 |
| True 100 / done | 0 |
| near_pass (≥90-ish / research_strong) | 49 |
| structural_strong | 65 |
| structural_ok | 0 |
| partial | 0 |
| weak | 0 |

### What v1 did

1. **Reverted** false `tasks.md` fleet-100 / done claims from the fast rubber-stamp run.
2. **Re-ran research sections:** replaced cookie-cutter multi-agent boilerplate with **role-family** research mapped to each agent’s migration prompt topics.
3. **Re-scored** every agent on S1–S6 with mechanical + critic caps (thin SPEC and weak S3 limit S6).
4. **Did not** claim full live arXiv/X/YouTube primary harvest for all 114 — residual listed per row.

### Grade legend

| Grade | Meaning |
|-------|---------|
| `near_pass` | High total; research stronger; still not auto-100 without live primary sources + human critic |
| `structural_strong` | SPEC/ALC/reachability solid; S3 role research still incomplete for full 15 |
| `structural_ok` | Usable self-contained agent pack materials; depth or research gaps |
| `partial` | Materials present but thin or incomplete dimensions |
| `weak` | Major gaps |

### Status legend (tasks.md)

| Status | Meaning |
|--------|---------|
| `structural_pass` | S4/S5 and baseline SPEC present; not fleet-done |
| `research_strong` | Better S3 integration; still open for true 100 |
| `needs_work` | Below structural bar for comfortable L2 use |

## Master quality table

| order | agent_id | role | cat | SPEC KB | src | S1 | S2 | S3 | S4 | S5 | S6 | **total** | grade | status | top gaps |
|------:|----------|------|-----|--------:|----:|---:|---:|---:|---:|---:|---:|----------:|-------|--------|----------|
| 1 | `video.orchestrator` | OrchestratorAgent | 9-Meta | 472.9 | 20 | 25 | 20 | 13 | 15 | 10 | 14 | **97** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 2 | `video.planner` | PlannerAgent | 9-Meta | 553.1 | 23 | 25 | 20 | 13 | 15 | 10 | 14 | **97** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 3 | `video.router` | RouterAgent | 9-Meta | 263.6 | 19 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 4 | `video.judge` | JudgeAgent | 9-Meta | 246.7 | 19 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 5 | `video.gatekeeper` | GateKeeperAgent | 9-Meta | 235.8 | 12 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 6 | `video.producer` | ProducerAgent / EP | 1-ATL | 303.9 | 12 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 7 | `video.director` | DirectorAgent | 1-ATL | 318.4 | 19 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 8 | `video.screenwriter` | ScreenwriterAgent | 1-ATL | 234.1 | 11 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 9 | `video.webresearch` | WebResearchAgent | 9-Meta | 147.4 | 8 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 10 | `video.aiqaconsistency` | AIQAConsistencyAgent | 8-AI | 146.4 | 9 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 11 | `video.memory` | MemoryAgent | 9-Meta | 293.1 | 24 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 12 | `video.showrunner` | ShowrunnerAgent | 1-ATL | 192.9 | 8 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 13 | `video.casting` | CastingAgent | 1-ATL | 66.5 | 9 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 14 | `video.cinematographer` | CinematographerAgent (DoP) | 2-Cam | 140.8 | 8 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 15 | `video.cameraoperator` | CameraOperatorAgent | 2-Cam | 28.5 | 5 | 22 | 20 | 11 | 15 | 10 | 8 | **86** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor, thin SPEC |
| 16 | `video.dronepilot` | DronePilotAgent | 2-Cam | 35.0 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor, thin SPEC |
| 17 | `video.editor` | EditorAgent | 3-Edit | 257.4 | 18 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 18 | `video.colorist` | ColoristAgent | 3-Edit | 110.1 | 11 | 24 | 20 | 12 | 15 | 10 | 14 | **95** | near_pass | `research_strong` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 19 | `video.vfxsupervisor` | VFXSupervisorAgent | 3-Edit | 67.1 | 7 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 20 | `video.animator_2d` | AnimatorAgent (2D/3D) | 3-Edit | 71.1 | 8 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 21 | `video.motiongraphics` | MotionGraphicsAgent | 3-Edit | 79.0 | 8 | 24 | 20 | 11 | 15 | 10 | 14 | **94** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 22 | `video.storyboard` | StoryboardAgent | 3-Edit | 90.5 | 10 | 24 | 20 | 11 | 15 | 10 | 14 | **94** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 23 | `video.conceptartist` | ConceptArtistAgent | 3-Edit | 88.2 | 9 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 24 | `video.productiondesign` | ProductionDesignAgent | 3-Edit | 58.0 | 6 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 25 | `video.costumedesign` | CostumeDesignAgent | 3-Edit | 44.1 | 5 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 26 | `video.mua_makeup` | MUAAgent (Makeup/Hair/SFX) | 3-Edit | 60.7 | 6 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 27 | `video.sounddesign` | SoundDesignAgent | 4-Snd | 121.3 | 7 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 28 | `video.composer` | ComposerAgent | 4-Snd | 198.6 | 12 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 29 | `video.voiceover` | VoiceOverAgent | 4-Snd | 116.4 | 6 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 30 | `video.soundmixer` | SoundMixerAgent (Re-recording) | 4-Snd | 161.4 | 10 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 31 | `video.choreography` | ChoreographyAgent | 5-Perf | 43.8 | 7 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 32 | `video.musicvideodirector` | MusicVideoDirectorAgent | 5-Perf | 36.6 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor, thin SPEC |
| 33 | `video.comedywriter` | ComedyWriterAgent | 5-Perf | 90.4 | 5 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 34 | `video.talent` | TalentAgent (On-camera) | 5-Perf | 82.8 | 8 | 24 | 20 | 11 | 15 | 10 | 14 | **94** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 35 | `video.ugccreator` | UGCCreatorAgent | 5-Perf | 29.0 | 4 | 22 | 20 | 11 | 15 | 10 | 8 | **86** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor, thin SPEC |
| 36 | `video.socialmediastrategist` | SocialMediaStrategistAgent | 6-Dist | 52.0 | 6 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 37 | `video.copywriter` | CopywriterAgent | 6-Dist | 79.4 | 8 | 24 | 20 | 11 | 15 | 10 | 14 | **94** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 38 | `video.creativedirector` | CreativeDirectorAgent | 6-Dist | 56.5 | 6 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 39 | `video.performancemarketer` | PerformanceMarketerAgent | 6-Dist | 221.9 | 6 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 40 | `video.instructionaldesign` | InstructionalDesignAgent | 7-Edu | 47.7 | 5 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 41 | `video.sme` | SMEAgent (Subject-Matter Expert) | 7-Edu | 95.0 | 11 | 24 | 20 | 11 | 15 | 10 | 14 | **94** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 42 | `video.factchecker` | FactCheckerAgent | 7-Edu | 55.9 | 5 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 43 | `video.medicalillustrator` | MedicalIllustratorAgent | 7-Edu | 37.1 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor, thin SPEC |
| 44 | `video.journalist` | JournalistAgent | 7-Edu | 125.5 | 7 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 45 | `video.compliance` | ComplianceAgent (Legal) | 7-Edu | 131.1 | 15 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 46 | `video.finance` | FinanceAgent | 7-Edu | 66.2 | 6 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 47 | `video.foodstylist` | FoodStylistAgent | 7-Edu | 37.0 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor, thin SPEC |
| 48 | `video.travelcine` | TravelCineAgent | 7-Edu | 41.7 | 5 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 49 | `video.childrensauthor` | ChildrensAuthorAgent | 7-Edu | 99.0 | 5 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 50 | `video.audiobooknarrator` | AudiobookNarratorAgent | 7-Edu | 115.9 | 5 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 51 | `video.signlanguageinterpreter` | SignLanguageInterpreterAgent | 7-Edu | 37.2 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor, thin SPEC |
| 52 | `video.localizationqa` | LocalizationQAAgent (Linguist) | 7-Edu | 45.0 | 5 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 53 | `video.realestatephoto` | RealEstatePhotoAgent / 3D Scan | 7-Edu | 37.0 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor, thin SPEC |
| 54 | `video.promptengineer` | PromptEngineerAgent / GeneratorOperator | 8-AI | 183.0 | 11 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 55 | `video.avatardesign` | AvatarDesignAgent | 8-AI | 95.4 | 6 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 56 | `video.voiceclone` | VoiceCloneAgent / LipSyncSpecialist | 8-AI | 58.5 | 6 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 57 | `video.personalizationengineer` | PersonalizationEngineerAgent | 8-AI | 272.4 | 8 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 58 | `video.trailereditor` | TrailerEditorAgent | 8-AI | 53.1 | 5 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 59 | `video.sportsanalyst` | SportsAnalystAgent / TelestratorOp | 8-AI | 28.8 | 4 | 22 | 20 | 11 | 15 | 10 | 8 | **86** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor, thin SPEC |
| 60 | `video.ideation` | IdeationAgent | 9-Meta | 108.3 | 12 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 61 | `video.narrativearc` | NarrativeArcAgent | 9-Meta | 90.5 | 9 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 62 | `video.styletransfer` | StyleTransferAgent | 9-Meta | 93.4 | 9 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 63 | `video.worldbuilding` | WorldBuildingAgent | 9-Meta | 67.8 | 8 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 64 | `video.moodboard` | MoodBoardAgent | 9-Meta | 71.7 | 9 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 65 | `video.novelty` | NoveltyAgent / Anti-Cliché Critic | 9-Meta | 91.1 | 10 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 66 | `video.emotionalarc` | EmotionalArcAgent | 9-Meta | 115.2 | 9 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 67 | `video.archiveresearch` | ArchiveResearchAgent | 9-Meta | 152.8 | 7 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 68 | `video.trendintelligence` | TrendIntelligenceAgent | 9-Meta | 90.0 | 7 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 69 | `video.competitorintelligence` | CompetitorIntelligenceAgent | 9-Meta | 85.9 | 5 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 70 | `video.citation` | CitationAgent | 9-Meta | 190.2 | 13 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 71 | `video.interviewsynthesis` | InterviewSynthesisAgent | 9-Meta | 102.5 | 7 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 72 | `video.benchmarkresearch` | BenchmarkResearchAgent | 9-Meta | 138.2 | 7 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 73 | `video.promptoptimizer` | PromptOptimizerAgent | 9-Meta | 80.6 | 10 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 74 | `video.costoptimizer` | CostOptimizerAgent | 9-Meta | 88.0 | 10 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 75 | `video.latencyoptimizer` | LatencyOptimizerAgent | 9-Meta | 68.3 | 8 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 76 | `video.retentionoptimizer` | RetentionOptimizerAgent | 9-Meta | 272.1 | 11 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 77 | `video.roasoptimizer` | ROASOptimizerAgent | 9-Meta | 63.3 | 6 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 78 | `video.accessibilityoptimizer` | AccessibilityOptimizerAgent | 9-Meta | 85.3 | 8 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 79 | `video.evaluationharness` | EvaluationHarnessAgent | 9-Meta | 262.7 | 9 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 80 | `video.safetyredteam` | SafetyRedTeamAgent | 9-Meta | 68.1 | 7 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 81 | `video.analyst` | AnalystAgent | 10-Sup | 138.1 | 9 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 82 | `video.audiencesim` | AudienceSimAgent | 10-Sup | 317.5 | 11 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 83 | `video.accessibility` | AccessibilityAgent | 10-Sup | 116.3 | 10 | 24 | 20 | 12 | 15 | 10 | 14 | **95** | near_pass | `research_strong` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 84 | `video.brand` | BrandAgent | 10-Sup | 149.8 | 12 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 85 | `video.brandstrategist` | BrandStrategistAgent | 10-Sup | 125.2 | 5 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 86 | `video.marketing` | MarketingAgent | 10-Sup | 326.1 | 9 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 87 | `video.seo` | SEOAgent | 10-Sup | 251.2 | 7 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 88 | `video.community` | CommunityAgent | 10-Sup | 112.7 | 10 | 24 | 20 | 12 | 15 | 10 | 14 | **95** | near_pass | `research_strong` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 89 | `video.templatedesign` | TemplateDesignAgent | 10-Sup | 148.5 | 4 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 90 | `video.ux` | UXAgent | 10-Sup | 48.6 | 3 | 22 | 16 | 11 | 15 | 10 | 14 | **88** | structural_strong | `structural_pass` | S1 depth, S2 corpus, S3 role research (live primary sources), S6 critic rigor |
| 91 | `video.trustsafety` | TrustSafetyAgent | 10-Sup | 55.1 | 5 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 92 | `video.crm` | CRMAgent | 10-Sup | 55.7 | 6 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 93 | `video.legal` | LegalAgent | 10-Sup | 92.2 | 8 | 24 | 20 | 11 | 15 | 10 | 14 | **94** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 94 | `video.festivalstrategist` | FestivalStrategistAgent | 10-Sup | 48.9 | 3 | 22 | 16 | 11 | 15 | 10 | 14 | **88** | structural_strong | `structural_pass` | S1 depth, S2 corpus, S3 role research (live primary sources), S6 critic rigor |
| 95 | `video.critic` | CriticAgent | 10-Sup | 220.3 | 21 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 96 | `video.lms` | LMSAgent | 10-Sup | 97.8 | 9 | 24 | 20 | 12 | 15 | 10 | 14 | **95** | near_pass | `research_strong` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 97 | `video.learnersim` | LearnerSimAgent | 10-Sup | 94.2 | 4 | 25 | 20 | 11 | 15 | 10 | 14 | **95** | structural_strong | `structural_pass` | S3 role research (live primary sources), S6 critic rigor |
| 98 | `video.continuity` | ContinuityAgent | 10-Sup | 118.6 | 8 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 99 | `video.lipsync` | LipSyncAgent | 10-Sup | 113.3 | 6 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 100 | `video.musicsupervisor` | MusicSupervisorAgent | 10-Sup | 130.5 | 4 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 101 | `video.labela_r` | LabelA&RAgent | 10-Sup | 50.8 | 3 | 22 | 16 | 11 | 15 | 10 | 14 | **88** | structural_strong | `structural_pass` | S1 depth, S2 corpus, S3 role research (live primary sources), S6 critic rigor |
| 102 | `video.labeldigital` | LabelDigitalAgent | 10-Sup | 48.9 | 3 | 22 | 16 | 11 | 15 | 10 | 14 | **88** | structural_strong | `structural_pass` | S1 depth, S2 corpus, S3 role research (live primary sources), S6 critic rigor |
| 103 | `video.deepfakedetection` | DeepfakeDetectionAgent | 10-Sup | 61.9 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 104 | `video.comms` | CommsAgent | 10-Sup | 54.6 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 105 | `video.archiveproducer` | ArchiveProducerAgent | 10-Sup | 49.0 | 3 | 22 | 16 | 11 | 15 | 10 | 14 | **88** | structural_strong | `structural_pass` | S1 depth, S2 corpus, S3 role research (live primary sources), S6 critic rigor |
| 106 | `video.standardseditor` | StandardsEditorAgent | 10-Sup | 58.2 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 107 | `video.ethics` | EthicsAgent | 10-Sup | 79.6 | 6 | 24 | 20 | 11 | 15 | 10 | 14 | **94** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 108 | `video.channelmanager` | ChannelManagerAgent | 10-Sup | 53.0 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 109 | `video.corrections` | CorrectionsAgent | 10-Sup | 73.8 | 7 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 110 | `video.mpa` | MPAAgent | 10-Sup | 248.9 | 26 | 25 | 20 | 12 | 15 | 10 | 14 | **96** | near_pass | `research_strong` | S3 role research (live primary sources), S6 critic rigor |
| 111 | `video.sales` | SalesAgent | 10-Sup | 56.1 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 112 | `video.distributor` | DistributorAgent | 10-Sup | 78.9 | 8 | 24 | 20 | 11 | 15 | 10 | 14 | **94** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 113 | `video.awardsstrategist` | AwardsStrategistAgent | 10-Sup | 49.1 | 3 | 22 | 16 | 11 | 15 | 10 | 14 | **88** | structural_strong | `structural_pass` | S1 depth, S2 corpus, S3 role research (live primary sources), S6 critic rigor |
| 114 | `video.archivemaster` | ArchiveMasterAgent | 10-Sup | 50.2 | 4 | 22 | 20 | 11 | 15 | 10 | 14 | **92** | structural_strong | `structural_pass` | S1 depth, S3 role research (live primary sources), S6 critic rigor |

## Category rollup

| category | n | mean total | min | max |
|----------|--:|-----------:|----:|----:|
| 1-ATL | 5 | 95.2 | 92 | 96 |
| 10-Sup | 34 | 93.2 | 88 | 96 |
| 2-Cam | 3 | 91.3 | 86 | 96 |
| 3-Edit | 10 | 93.4 | 92 | 96 |
| 4-Snd | 4 | 96.0 | 96 | 96 |
| 5-Perf | 5 | 91.8 | 86 | 95 |
| 6-Dist | 4 | 93.5 | 92 | 96 |
| 7-Edu | 14 | 93.3 | 92 | 96 |
| 8-AI | 7 | 93.3 | 86 | 96 |
| 9-Meta | 28 | 95.1 | 92 | 97 |

## Priority rework queue (v1 residual)

### Thin SPECs (<40 KB) — deepen corpus embeds first

| order | agent_id | KB | total | gaps |
|------:|----------|---:|------:|------|
| 15 | `video.cameraoperator` | 28.5 | 86 | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 59 | `video.sportsanalyst` | 28.8 | 86 | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 35 | `video.ugccreator` | 29.0 | 86 | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 16 | `video.dronepilot` | 35.0 | 92 | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 32 | `video.musicvideodirector` | 36.6 | 92 | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 47 | `video.foodstylist` | 37.0 | 92 | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 53 | `video.realestatephoto` | 37.0 | 92 | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 43 | `video.medicalillustrator` | 37.1 | 92 | S1 depth, S3 role research (live primary sources), S6 critic rigor |
| 51 | `video.signlanguageinterpreter` | 37.2 | 92 | S1 depth, S3 role research (live primary sources), S6 critic rigor |

### S3 < 10 — role-specific live research still required for true 100

Count: **0** / 114

## How to reach true 100 (per agent)

1. Mine all related `business/video/corpus/**` for the role (unsummarized embeds or sources/).
2. Live arXiv + X + YouTube for **this** prompt’s topics; integrate full findings into SPEC.
3. Independent S6 critic pass (no open P0).
4. Only then set score **100** and status `done` in `tasks.md`.

## Tooling

- Generator: `scripts/business/migration_impl_v1_honest.py`
- Related: `scripts/business/append_migration_research.py` (superseded for grading by this v1 pass)

<!-- agent_impl_v1_mark · 2026-07-13 · n=114 -->


---

## Honesty addendum — skeptical recalibration (2026-07-13)

> **Is mean ~94 too good to be true?**  
> **Yes, as a claim of “implementation quality.”**  
> **No, as a claim that “folders/ALC/roster mostly exist.”**

### Why the soft v1 scorer looked ultra-good

| Soft scorer behavior | Effect |
|----------------------|--------|
| Gave high S1 for any SPEC ≥ ~25–80 KB | Rewards bulk embeds, not unique role depth |
| Gave S3 ≈ 11–13 for role-family research bank | Treats topic mapping as near-complete research |
| Gave S4/S5 near-max when ALC + ROSTER present | Correct for wiring — but dominates the total |
| Capped S6 only mildly | Automated “review” is not a real critic |
| Result mean **~93.8** | Looks like “almost done” when S3/S6 are still open |

**System is not ultra-good at craft research.** It *is* solid at structural host wiring (ALC, roster, standby, inventory gates).

### Harsh reviewer scores (this section)

Same S1–S6 max points, but:

- S3 hard-capped at **10** without live arXiv/X/YouTube primary integration  
- S6 hard-capped at **9** without independent human critic  
- Thin SPECs / table-dumps heavily discounted on S1/S2  

| Metric | Soft v1 | Harsh recal |
|--------|--------:|------------:|
| Mean total | 93.8 | **74.4** |
| Median | — | **78** |
| Min / Max | — | **62 / 85** |
| True 100 | 0 | **0** |
| ≥ 90 | many | **0** |
| ≥ 80 | most | **28** |
| ≥ 70 | almost all | **69** |
| < 60 | 0 | **0** |

| Harsh grade | Count |
|-------------|------:|
| `usable_structural` | 68 |
| `partial_materials` | 45 |
| `strong_structural_not_done` | 1 |

| Dim means (harsh) | S1 | S2 | S3 | S4 | S5 | S6 |
|-------------------|---:|---:|---:|---:|---:|---:|
| | 18.3 | 16.4 | 7.4 | 15.0 | 10.0 | 7.4 |

**Read the pattern:** S4≈15 and S5≈10 are real. **S3≈5–7 and S6≈6–8 are the truth about research/review.** Soft totals hid that by stacking easy points.

### Harsh master table

| order | agent_id | soft_v1 | **harsh** | Δ | S1 | S2 | S3 | S4 | S5 | S6 | KB | harsh grade | gaps |
|------:|----------|--------:|----------:|--:|---:|---:|---:|---:|---:|---:|---:|-------------|------|
| 1 | `video.orchestrator` | 97 | **85** | -12 | 23 | 18 | 10 | 15 | 10 | 9 | 472.9 | `strong_structural_not_done` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 2 | `video.planner` | 97 | **84** | -13 | 23 | 18 | 9 | 15 | 10 | 9 | 553.1 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 3 | `video.router` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 263.6 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 4 | `video.judge` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 246.7 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 5 | `video.gatekeeper` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 235.8 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 6 | `video.producer` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 303.9 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 7 | `video.director` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 318.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 8 | `video.screenwriter` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 234.1 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 9 | `video.webresearch` | 96 | **81** | -15 | 23 | 18 | 7 | 15 | 10 | 8 | 147.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 10 | `video.aiqaconsistency` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 146.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 11 | `video.memory` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 293.1 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 12 | `video.showrunner` | 96 | **81** | -15 | 23 | 18 | 7 | 15 | 10 | 8 | 192.9 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 13 | `video.casting` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 66.5 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 14 | `video.cinematographer` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 140.8 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 15 | `video.cameraoperator` | 86 | **62** | -24 | 12 | 12 | 7 | 15 | 10 | 6 | 28.5 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 16 | `video.dronepilot` | 92 | **62** | -30 | 12 | 12 | 7 | 15 | 10 | 6 | 35.0 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 17 | `video.editor` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 257.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 18 | `video.colorist` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 110.1 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 19 | `video.vfxsupervisor` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 67.1 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 20 | `video.animator_2d` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 71.1 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 21 | `video.motiongraphics` | 94 | **76** | -18 | 18 | 18 | 7 | 15 | 10 | 8 | 79.0 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 22 | `video.storyboard` | 94 | **76** | -18 | 18 | 18 | 7 | 15 | 10 | 8 | 90.5 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 23 | `video.conceptartist` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 88.2 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 24 | `video.productiondesign` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 58.0 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 25 | `video.costumedesign` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 44.1 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 26 | `video.mua_makeup` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 60.7 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 27 | `video.sounddesign` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 121.3 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 28 | `video.composer` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 198.6 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 29 | `video.voiceover` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 116.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 30 | `video.soundmixer` | 96 | **81** | -15 | 23 | 18 | 7 | 15 | 10 | 8 | 161.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 31 | `video.choreography` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 43.8 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 32 | `video.musicvideodirector` | 92 | **62** | -30 | 12 | 12 | 7 | 15 | 10 | 6 | 36.6 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 33 | `video.comedywriter` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 90.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 34 | `video.talent` | 94 | **76** | -18 | 18 | 18 | 7 | 15 | 10 | 8 | 82.8 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 35 | `video.ugccreator` | 86 | **62** | -24 | 12 | 12 | 7 | 15 | 10 | 6 | 29.0 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 36 | `video.socialmediastrategist` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 52.0 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 37 | `video.copywriter` | 94 | **76** | -18 | 18 | 18 | 7 | 15 | 10 | 8 | 79.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 38 | `video.creativedirector` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 56.5 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 39 | `video.performancemarketer` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 221.9 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 40 | `video.instructionaldesign` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 47.7 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 41 | `video.sme` | 94 | **76** | -18 | 18 | 18 | 7 | 15 | 10 | 8 | 95.0 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 42 | `video.factchecker` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 55.9 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 43 | `video.medicalillustrator` | 92 | **62** | -30 | 12 | 12 | 7 | 15 | 10 | 6 | 37.1 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 44 | `video.journalist` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 125.5 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 45 | `video.compliance` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 131.1 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 46 | `video.finance` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 66.2 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 47 | `video.foodstylist` | 92 | **62** | -30 | 12 | 12 | 7 | 15 | 10 | 6 | 37.0 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 48 | `video.travelcine` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 41.7 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 49 | `video.childrensauthor` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 99.0 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 50 | `video.audiobooknarrator` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 115.9 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 51 | `video.signlanguageinterpreter` | 92 | **62** | -30 | 12 | 12 | 7 | 15 | 10 | 6 | 37.2 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 52 | `video.localizationqa` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 45.0 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 53 | `video.realestatephoto` | 92 | **62** | -30 | 12 | 12 | 7 | 15 | 10 | 6 | 37.0 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 54 | `video.promptengineer` | 96 | **81** | -15 | 23 | 18 | 7 | 15 | 10 | 8 | 183.0 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 55 | `video.avatardesign` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 95.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 56 | `video.voiceclone` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 58.5 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 57 | `video.personalizationengineer` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 272.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 58 | `video.trailereditor` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 53.1 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 59 | `video.sportsanalyst` | 86 | **62** | -24 | 12 | 12 | 7 | 15 | 10 | 6 | 28.8 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 60 | `video.ideation` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 108.3 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 61 | `video.narrativearc` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 90.5 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 62 | `video.styletransfer` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 93.4 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 63 | `video.worldbuilding` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 67.8 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 64 | `video.moodboard` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 71.7 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 65 | `video.novelty` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 91.1 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 66 | `video.emotionalarc` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 115.2 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 67 | `video.archiveresearch` | 96 | **81** | -15 | 23 | 18 | 7 | 15 | 10 | 8 | 152.8 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 68 | `video.trendintelligence` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 90.0 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 69 | `video.competitorintelligence` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 85.9 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 70 | `video.citation` | 96 | **81** | -15 | 23 | 18 | 7 | 15 | 10 | 8 | 190.2 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 71 | `video.interviewsynthesis` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 102.5 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 72 | `video.benchmarkresearch` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 138.2 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 73 | `video.promptoptimizer` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 80.6 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 74 | `video.costoptimizer` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 88.0 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 75 | `video.latencyoptimizer` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 68.3 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 76 | `video.retentionoptimizer` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 272.1 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 77 | `video.roasoptimizer` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 63.3 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 78 | `video.accessibilityoptimizer` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 85.3 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 79 | `video.evaluationharness` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 262.7 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 80 | `video.safetyredteam` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 68.1 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 81 | `video.analyst` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 138.1 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 82 | `video.audiencesim` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 317.5 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 83 | `video.accessibility` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 116.3 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 84 | `video.brand` | 96 | **81** | -15 | 23 | 18 | 7 | 15 | 10 | 8 | 149.8 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 85 | `video.brandstrategist` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 125.2 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 86 | `video.marketing` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 326.1 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 87 | `video.seo` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 251.2 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 88 | `video.community` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 112.7 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 89 | `video.templatedesign` | 96 | **81** | -15 | 23 | 18 | 7 | 15 | 10 | 8 | 148.5 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 90 | `video.ux` | 88 | **64** | -24 | 14 | 12 | 7 | 15 | 10 | 6 | 48.6 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 91 | `video.trustsafety` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 55.1 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 92 | `video.crm` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 55.7 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 93 | `video.legal` | 94 | **76** | -18 | 18 | 18 | 7 | 15 | 10 | 8 | 92.2 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 94 | `video.festivalstrategist` | 88 | **64** | -24 | 14 | 12 | 7 | 15 | 10 | 6 | 48.9 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 95 | `video.critic` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 220.3 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 96 | `video.lms` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 97.8 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 97 | `video.learnersim` | 95 | **78** | -17 | 20 | 18 | 7 | 15 | 10 | 8 | 94.2 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 98 | `video.continuity` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 118.6 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 99 | `video.lipsync` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 113.3 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 100 | `video.musicsupervisor` | 96 | **78** | -18 | 20 | 18 | 7 | 15 | 10 | 8 | 130.5 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 101 | `video.labela_r` | 88 | **64** | -24 | 14 | 12 | 7 | 15 | 10 | 6 | 50.8 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 102 | `video.labeldigital` | 88 | **64** | -24 | 14 | 12 | 7 | 15 | 10 | 6 | 48.9 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 103 | `video.deepfakedetection` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 61.9 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 104 | `video.comms` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 54.6 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 105 | `video.archiveproducer` | 88 | **64** | -24 | 14 | 12 | 7 | 15 | 10 | 6 | 49.0 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 106 | `video.standardseditor` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 58.2 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 107 | `video.ethics` | 94 | **76** | -18 | 18 | 18 | 7 | 15 | 10 | 8 | 79.6 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 108 | `video.channelmanager` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 53.0 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 109 | `video.corrections` | 92 | **69** | -23 | 16 | 15 | 7 | 15 | 10 | 6 | 73.8 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 110 | `video.mpa` | 96 | **84** | -12 | 23 | 18 | 9 | 15 | 10 | 9 | 248.9 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 111 | `video.sales` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 56.1 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 112 | `video.distributor` | 94 | **76** | -18 | 18 | 18 | 7 | 15 | 10 | 8 | 78.9 | `usable_structural` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 113 | `video.awardsstrategist` | 88 | **64** | -24 | 14 | 12 | 7 | 15 | 10 | 6 | 49.1 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |
| 114 | `video.archivemaster` | 92 | **67** | -25 | 14 | 15 | 7 | 15 | 10 | 6 | 50.2 | `partial_materials` | S1 not full depth, S2 corpus thin/generic, S3 no live primary research |

### Bottom line

1. **Not ultra-good end-to-end.** Structural host pack materials are genuinely advanced (inventory 114, ALC, standby, large SPECs for spine).
2. **Too good to be true** if you read soft ~94 as “almost production-complete agents.”
3. **Believe harsh ~74 mean** as “usable catalog + wiring; research/critic still open.”
4. **Believe 0 × 100** — that part was already honest.

<!-- harsh_recalibration · 2026-07-13 · mean=74.4 -->
