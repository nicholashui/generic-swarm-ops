# -*- coding: utf-8 -*-
"""Generate business/video L0 catalog from adoption.md Appendix A (N3).

Idempotent. Writes ROSTER.json, MAP.md, agent dirs + minimal agent_spec + SPEC stub.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "business" / "video"
AGENTS = VIDEO / "agents"

# Appendix A — adoption.md (pack_id canonical). Do not drop rows.
ROSTER: list[dict] = [
    {"id": 1, "name": "DirectorAgent", "category": "1-ATL", "pack_id": "video.director"},
    {"id": 2, "name": "ProducerAgent / EP", "category": "1-ATL", "pack_id": "video.producer"},
    {"id": 3, "name": "ScreenwriterAgent", "category": "1-ATL", "pack_id": "video.screenwriter"},
    {"id": 4, "name": "ShowrunnerAgent", "category": "1-ATL", "pack_id": "video.showrunner"},
    {"id": 5, "name": "CastingAgent", "category": "1-ATL", "pack_id": "video.casting"},
    {"id": 6, "name": "CinematographerAgent (DoP)", "category": "2-Cam", "pack_id": "video.cinematographer"},
    {"id": 7, "name": "CameraOperatorAgent", "category": "2-Cam", "pack_id": "video.cameraoperator"},
    {"id": 8, "name": "DronePilotAgent", "category": "2-Cam", "pack_id": "video.dronepilot"},
    {"id": 9, "name": "EditorAgent", "category": "3-Edit", "pack_id": "video.editor"},
    {"id": 10, "name": "ColoristAgent", "category": "3-Edit", "pack_id": "video.colorist"},
    {"id": 11, "name": "VFXSupervisorAgent", "category": "3-Edit", "pack_id": "video.vfxsupervisor"},
    {"id": 12, "name": "AnimatorAgent (2D/3D)", "category": "3-Edit", "pack_id": "video.animator_2d"},
    {"id": 13, "name": "MotionGraphicsAgent", "category": "3-Edit", "pack_id": "video.motiongraphics"},
    {"id": 14, "name": "StoryboardAgent", "category": "3-Edit", "pack_id": "video.storyboard"},
    {"id": 15, "name": "ConceptArtistAgent", "category": "3-Edit", "pack_id": "video.conceptartist"},
    {"id": 16, "name": "ProductionDesignAgent", "category": "3-Edit", "pack_id": "video.productiondesign"},
    {"id": 17, "name": "CostumeDesignAgent", "category": "3-Edit", "pack_id": "video.costumedesign"},
    {"id": 18, "name": "MUAAgent (Makeup/Hair/SFX)", "category": "3-Edit", "pack_id": "video.mua_makeup"},
    {"id": 19, "name": "SoundDesignAgent", "category": "4-Snd", "pack_id": "video.sounddesign"},
    {"id": 20, "name": "ComposerAgent", "category": "4-Snd", "pack_id": "video.composer"},
    {"id": 21, "name": "VoiceOverAgent", "category": "4-Snd", "pack_id": "video.voiceover"},
    {"id": 22, "name": "SoundMixerAgent (Re-recording)", "category": "4-Snd", "pack_id": "video.soundmixer"},
    {"id": 23, "name": "ChoreographyAgent", "category": "5-Perf", "pack_id": "video.choreography"},
    {"id": 24, "name": "MusicVideoDirectorAgent", "category": "5-Perf", "pack_id": "video.musicvideodirector"},
    {"id": 25, "name": "ComedyWriterAgent", "category": "5-Perf", "pack_id": "video.comedywriter"},
    {"id": 26, "name": "TalentAgent (On-camera)", "category": "5-Perf", "pack_id": "video.talent"},
    {"id": 27, "name": "UGCCreatorAgent", "category": "5-Perf", "pack_id": "video.ugccreator"},
    {"id": 28, "name": "SocialMediaStrategistAgent", "category": "6-Dist", "pack_id": "video.socialmediastrategist"},
    {"id": 29, "name": "CopywriterAgent", "category": "6-Dist", "pack_id": "video.copywriter"},
    {"id": 30, "name": "CreativeDirectorAgent", "category": "6-Dist", "pack_id": "video.creativedirector"},
    {"id": 31, "name": "PerformanceMarketerAgent", "category": "6-Dist", "pack_id": "video.performancemarketer"},
    {"id": 32, "name": "InstructionalDesignAgent", "category": "7-Edu", "pack_id": "video.instructionaldesign"},
    {"id": 33, "name": "SMEAgent (Subject-Matter Expert)", "category": "7-Edu", "pack_id": "video.sme"},
    {"id": 34, "name": "FactCheckerAgent", "category": "7-Edu", "pack_id": "video.factchecker"},
    {"id": 35, "name": "MedicalIllustratorAgent", "category": "7-Edu", "pack_id": "video.medicalillustrator"},
    {"id": 36, "name": "JournalistAgent", "category": "7-Edu", "pack_id": "video.journalist"},
    {"id": 37, "name": "ComplianceAgent (Legal)", "category": "7-Edu", "pack_id": "video.compliance"},
    {"id": 38, "name": "FinanceAgent", "category": "7-Edu", "pack_id": "video.finance"},
    {"id": 39, "name": "FoodStylistAgent", "category": "7-Edu", "pack_id": "video.foodstylist"},
    {"id": 40, "name": "TravelCineAgent", "category": "7-Edu", "pack_id": "video.travelcine"},
    {"id": 41, "name": "ChildrensAuthorAgent", "category": "7-Edu", "pack_id": "video.childrensauthor"},
    {"id": 42, "name": "AudiobookNarratorAgent", "category": "7-Edu", "pack_id": "video.audiobooknarrator"},
    {"id": 43, "name": "SignLanguageInterpreterAgent", "category": "7-Edu", "pack_id": "video.signlanguageinterpreter"},
    {"id": 44, "name": "LocalizationQAAgent (Linguist)", "category": "7-Edu", "pack_id": "video.localizationqa"},
    {"id": 45, "name": "RealEstatePhotoAgent / 3D Scan", "category": "7-Edu", "pack_id": "video.realestatephoto"},
    {"id": 46, "name": "PromptEngineerAgent / GeneratorOperator", "category": "8-AI", "pack_id": "video.promptengineer"},
    {"id": 47, "name": "AvatarDesignAgent", "category": "8-AI", "pack_id": "video.avatardesign"},
    {"id": 48, "name": "VoiceCloneAgent / LipSyncSpecialist", "category": "8-AI", "pack_id": "video.voiceclone"},
    {"id": 49, "name": "AIQAConsistencyAgent", "category": "8-AI", "pack_id": "video.aiqaconsistency"},
    {"id": 50, "name": "PersonalizationEngineerAgent", "category": "8-AI", "pack_id": "video.personalizationengineer"},
    {"id": 51, "name": "TrailerEditorAgent", "category": "8-AI", "pack_id": "video.trailereditor"},
    {"id": 52, "name": "SportsAnalystAgent / TelestratorOp", "category": "8-AI", "pack_id": "video.sportsanalyst"},
    {"id": 53, "name": "OrchestratorAgent", "category": "9-Meta", "pack_id": "video.orchestrator"},
    {"id": 54, "name": "PlannerAgent", "category": "9-Meta", "pack_id": "video.planner"},
    {"id": 55, "name": "RouterAgent", "category": "9-Meta", "pack_id": "video.router"},
    {"id": 56, "name": "JudgeAgent", "category": "9-Meta", "pack_id": "video.judge"},
    {"id": 57, "name": "GateKeeperAgent", "category": "9-Meta", "pack_id": "video.gatekeeper"},
    {"id": 58, "name": "MemoryAgent", "category": "9-Meta", "pack_id": "video.memory"},
    {"id": 59, "name": "IdeationAgent", "category": "9-Meta", "pack_id": "video.ideation"},
    {"id": 60, "name": "NarrativeArcAgent", "category": "9-Meta", "pack_id": "video.narrativearc"},
    {"id": 61, "name": "StyleTransferAgent", "category": "9-Meta", "pack_id": "video.styletransfer"},
    {"id": 62, "name": "WorldBuildingAgent", "category": "9-Meta", "pack_id": "video.worldbuilding"},
    {"id": 63, "name": "MoodBoardAgent", "category": "9-Meta", "pack_id": "video.moodboard"},
    {"id": 64, "name": "NoveltyAgent / Anti-Cliché Critic", "category": "9-Meta", "pack_id": "video.novelty"},
    {"id": 65, "name": "EmotionalArcAgent", "category": "9-Meta", "pack_id": "video.emotionalarc"},
    {"id": 66, "name": "WebResearchAgent", "category": "9-Meta", "pack_id": "video.webresearch"},
    {"id": 67, "name": "ArchiveResearchAgent", "category": "9-Meta", "pack_id": "video.archiveresearch"},
    {"id": 68, "name": "TrendIntelligenceAgent", "category": "9-Meta", "pack_id": "video.trendintelligence"},
    {"id": 69, "name": "CompetitorIntelligenceAgent", "category": "9-Meta", "pack_id": "video.competitorintelligence"},
    {"id": 70, "name": "CitationAgent", "category": "9-Meta", "pack_id": "video.citation"},
    {"id": 71, "name": "InterviewSynthesisAgent", "category": "9-Meta", "pack_id": "video.interviewsynthesis"},
    {"id": 72, "name": "BenchmarkResearchAgent", "category": "9-Meta", "pack_id": "video.benchmarkresearch"},
    {"id": 73, "name": "PromptOptimizerAgent", "category": "9-Meta", "pack_id": "video.promptoptimizer"},
    {"id": 74, "name": "CostOptimizerAgent", "category": "9-Meta", "pack_id": "video.costoptimizer"},
    {"id": 75, "name": "LatencyOptimizerAgent", "category": "9-Meta", "pack_id": "video.latencyoptimizer"},
    {"id": 76, "name": "RetentionOptimizerAgent", "category": "9-Meta", "pack_id": "video.retentionoptimizer"},
    {"id": 77, "name": "ROASOptimizerAgent", "category": "9-Meta", "pack_id": "video.roasoptimizer"},
    {"id": 78, "name": "AccessibilityOptimizerAgent", "category": "9-Meta", "pack_id": "video.accessibilityoptimizer"},
    {"id": 79, "name": "EvaluationHarnessAgent", "category": "9-Meta", "pack_id": "video.evaluationharness"},
    {"id": 80, "name": "SafetyRedTeamAgent", "category": "9-Meta", "pack_id": "video.safetyredteam"},
    {"id": 81, "name": "AnalystAgent", "category": "10-Sup", "pack_id": "video.analyst"},
    {"id": 82, "name": "AudienceSimAgent", "category": "10-Sup", "pack_id": "video.audiencesim"},
    {"id": 83, "name": "AccessibilityAgent", "category": "10-Sup", "pack_id": "video.accessibility"},
    {"id": 84, "name": "BrandAgent", "category": "10-Sup", "pack_id": "video.brand"},
    {"id": 85, "name": "BrandStrategistAgent", "category": "10-Sup", "pack_id": "video.brandstrategist"},
    {"id": 86, "name": "MarketingAgent", "category": "10-Sup", "pack_id": "video.marketing"},
    {"id": 87, "name": "SEOAgent", "category": "10-Sup", "pack_id": "video.seo"},
    {"id": 88, "name": "CommunityAgent", "category": "10-Sup", "pack_id": "video.community"},
    {"id": 89, "name": "TemplateDesignAgent", "category": "10-Sup", "pack_id": "video.templatedesign"},
    {"id": 90, "name": "UXAgent", "category": "10-Sup", "pack_id": "video.ux"},
    {"id": 91, "name": "TrustSafetyAgent", "category": "10-Sup", "pack_id": "video.trustsafety"},
    {"id": 92, "name": "CRMAgent", "category": "10-Sup", "pack_id": "video.crm"},
    {"id": 93, "name": "LegalAgent", "category": "10-Sup", "pack_id": "video.legal"},
    {"id": 94, "name": "FestivalStrategistAgent", "category": "10-Sup", "pack_id": "video.festivalstrategist"},
    {"id": 95, "name": "CriticAgent", "category": "10-Sup", "pack_id": "video.critic"},
    {"id": 96, "name": "LMSAgent", "category": "10-Sup", "pack_id": "video.lms"},
    {"id": 97, "name": "LearnerSimAgent", "category": "10-Sup", "pack_id": "video.learnersim"},
    {"id": 98, "name": "ContinuityAgent", "category": "10-Sup", "pack_id": "video.continuity"},
    {"id": 99, "name": "LipSyncAgent", "category": "10-Sup", "pack_id": "video.lipsync"},
    {"id": 100, "name": "MusicSupervisorAgent", "category": "10-Sup", "pack_id": "video.musicsupervisor"},
    {"id": 101, "name": "LabelA&RAgent", "category": "10-Sup", "pack_id": "video.labela_r"},
    {"id": 102, "name": "LabelDigitalAgent", "category": "10-Sup", "pack_id": "video.labeldigital"},
    {"id": 103, "name": "DeepfakeDetectionAgent", "category": "10-Sup", "pack_id": "video.deepfakedetection"},
    {"id": 104, "name": "CommsAgent", "category": "10-Sup", "pack_id": "video.comms"},
    {"id": 105, "name": "ArchiveProducerAgent", "category": "10-Sup", "pack_id": "video.archiveproducer"},
    {"id": 106, "name": "StandardsEditorAgent", "category": "10-Sup", "pack_id": "video.standardseditor"},
    {"id": 107, "name": "EthicsAgent", "category": "10-Sup", "pack_id": "video.ethics"},
    {"id": 108, "name": "ChannelManagerAgent", "category": "10-Sup", "pack_id": "video.channelmanager"},
    {"id": 109, "name": "CorrectionsAgent", "category": "10-Sup", "pack_id": "video.corrections"},
    {"id": 110, "name": "MPAAgent", "category": "10-Sup", "pack_id": "video.mpa"},
    {"id": 111, "name": "SalesAgent", "category": "10-Sup", "pack_id": "video.sales"},
    {"id": 112, "name": "DistributorAgent", "category": "10-Sup", "pack_id": "video.distributor"},
    {"id": 113, "name": "AwardsStrategistAgent", "category": "10-Sup", "pack_id": "video.awardsstrategist"},
    {"id": 114, "name": "ArchiveMasterAgent", "category": "10-Sup", "pack_id": "video.archivemaster"},
]


def agent_spec(row: dict) -> dict:
    return {
        "id": row["pack_id"],
        "va_id": row["id"],
        "name": row["name"],
        "domain_id": "video",
        "role": row["name"],
        "category": row["category"],
        "status": "draft",
        "requires_alc": True,
        "allowed_memory_scopes": ["agent", "organization"],
        "alc_version": "1.0",
        "hooks": {"reflect": True},
        "tools": [],
        "risk_tier": "tier_2_draft",
        "critique_rubric_ref": None,
        "provenance": {
            "source_refs": [
                "va-agent-swarm/study/agents.md",
                "adoption.md#appendix-a",
            ],
            "captured_by": "wave-0-catalog",
            "framework": "domain_pack_l0",
        },
    }


def write_spec_md(row: dict) -> str:
    return (
        f"# {row['name']}\n\n"
        f"- **va_id:** {row['id']}\n"
        f"- **pack_id:** `{row['pack_id']}`\n"
        f"- **category:** {row['category']}\n"
        f"- **status:** draft (L0 Catalog)\n"
        f"- **source:** `va-agent-swarm/study/agents.md` (id {row['id']})\n"
        f"- **policy:** N3 retention — do not delete this directory.\n"
        f"- **deep SPEC:** deferred until activation wave (adoption.md v2.3 rethink).\n"
    )


def main() -> None:
    assert len(ROSTER) == 114, len(ROSTER)
    pack_ids = [r["pack_id"] for r in ROSTER]
    assert len(pack_ids) == len(set(pack_ids)), "duplicate pack_id"

    for sub in (
        "agents",
        "workflows",
        "tools",
        "evals/golden",
        "evals/regression",
        "evals/adversarial",
        "knowledge/seeds",
        "policies",
        "ui",
    ):
        (VIDEO / sub).mkdir(parents=True, exist_ok=True)

    roster_out = []
    for row in ROSTER:
        entry = {
            **row,
            "va_source": "va-agent-swarm/study/agents.md",
        }
        roster_out.append(entry)
        d = AGENTS / row["pack_id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "prompts").mkdir(exist_ok=True)
        (d / "rubrics").mkdir(exist_ok=True)
        (d / "prompts" / ".gitkeep").write_text("", encoding="utf-8")
        (d / "rubrics" / ".gitkeep").write_text("", encoding="utf-8")
        (d / "agent_spec.json").write_text(
            json.dumps(agent_spec(row), indent=2) + "\n", encoding="utf-8"
        )
        (d / "SPEC.md").write_text(write_spec_md(row), encoding="utf-8")

    (VIDEO / "ROSTER.json").write_text(
        json.dumps(roster_out, indent=2) + "\n", encoding="utf-8"
    )

    map_lines = [
        "# Video Domain Pack MAP (N3)",
        "",
        "Source: adoption.md Appendix A · va-agent-swarm/study/agents.md",
        "",
        "| va_id | name | pack_id | category | va_source | generic_path | runtime_status | notes |",
        "|------:|------|---------|----------|-----------|--------------|----------------|-------|",
    ]
    for row in ROSTER:
        path = f"business/video/agents/{row['pack_id']}/"
        map_lines.append(
            f"| {row['id']} | {row['name']} | `{row['pack_id']}` | {row['category']} | "
            f"agents.md#{row['id']} | `{path}` | draft | L0 |"
        )
    map_lines.append("")
    (VIDEO / "MAP.md").write_text("\n".join(map_lines), encoding="utf-8")

    dirs = [p for p in AGENTS.iterdir() if p.is_dir()]
    print(f"ROSTER={len(roster_out)} dirs={len(dirs)}")
    if len(dirs) != 114:
        raise SystemExit(f"expected 114 agent dirs, got {len(dirs)}")


if __name__ == "__main__":
    main()
