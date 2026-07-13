Conduct a comprehensive review and update of the agent specification document for `video.screenwriter` located at the path business/video/agents/video.screenwriter. Perform a full extraction and integration of all detailed, un-summarized information from the `business\video\corpus` folder and the entire source code repository hosted at `C:\Project\va-agent-swarm`, ensuring every granular detail is retained within the updated specification without any content condensation.

Primary local inputs (must be fully mined; do not stop at links):
- `business/video/agents/video.screenwriter/SPEC.md` (current self-contained draft)
- `business/video/agents/video.screenwriter/agent_spec.json` and `business/video/agents/video.screenwriter/sources/**` if present
- `business/video/corpus/study/agents.md` (roster row for this agent)
- All related deep specs, workflows, SYSTEM_REFERENCE, and other corpus files relevant to `video.screenwriter` / role **ScreenwriterAgent** (category **1-ATL**)

Following the completion of the core specification update, execute targeted internet research to enhance the `video.screenwriter` agent capabilities (role-specific; do not reuse orchestrator-only topics):
1. Retrieve and integrate state-of-the-art research findings from arXiv papers relevant to: neural story generation, screenplay structure models, dialogue agents, Reflexion writing loops
2. Analyze and incorporate expert insights from x.ai (Twitter/X) from recognized industry and academic leaders specializing in: AI screenwriting, writers room multi-agent, story structure AI
3. Extract detailed, actionable technical guidance from high-quality YouTube content created by domain experts focused on: AI screenwriting tools, multi-agent writers room, script structure with LLMs
4. Integrate all research-derived enhancements into the specification with full, un-summarized detail, preserving every technical specification, implementation consideration, and expert recommendation to maintain maximum granularity throughout the updated document.

Constraints:
- Keep video business logic in the Domain Pack path only (N1); do not fork a second control plane.
- Do not auto-expand host runtime tool allow-lists from design-time vendor names; document design vs runtime tools separately.
- Prefer in-repo corpus paths as the source of truth; va-agent-swarm is optional upstream if already mirrored under `business/video/corpus`.
- Output/update the agent materials under `business/video/agents/video.screenwriter/` (especially SPEC.md); keep content self-contained under that agent folder where practical.
