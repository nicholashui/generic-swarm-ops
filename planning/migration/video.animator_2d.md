Conduct a comprehensive review and update of the agent specification document for `video.animator_2d` located at the path business/video/agents/video.animator_2d. Perform a full extraction and integration of all detailed, un-summarized information from the `business\video\corpus` folder and the entire source code repository hosted at `C:\Project\va-agent-swarm`, ensuring every granular detail is retained within the updated specification without any content condensation.

Primary local inputs (must be fully mined; do not stop at links):
- `business/video/agents/video.animator_2d/SPEC.md` (current self-contained draft)
- `business/video/agents/video.animator_2d/agent_spec.json` and `business/video/agents/video.animator_2d/sources/**` if present
- `business/video/corpus/study/agents.md` (roster row for this agent)
- All related deep specs, workflows, SYSTEM_REFERENCE, and other corpus files relevant to `video.animator_2d` / role **AnimatorAgent (2D/3D)** (category **3-Edit**)

Following the completion of the core specification update, execute targeted internet research to enhance the `video.animator_2d` agent capabilities (role-specific; do not reuse orchestrator-only topics):
1. Retrieve and integrate state-of-the-art research findings from arXiv papers relevant to: neural animation, VFX supervision agents, storyboard generation, motion synthesis, ControlNet video
2. Analyze and incorporate expert insights from x.ai (Twitter/X) from recognized industry and academic leaders specializing in: AI VFX, AI animation, AI storyboarding
3. Extract detailed, actionable technical guidance from high-quality YouTube content created by domain experts focused on: AI VFX pipelines, animation agents, storyboard generators
4. Integrate all research-derived enhancements into the specification with full, un-summarized detail, preserving every technical specification, implementation consideration, and expert recommendation to maintain maximum granularity throughout the updated document.

Constraints:
- Keep video business logic in the Domain Pack path only (N1); do not fork a second control plane.
- Do not auto-expand host runtime tool allow-lists from design-time vendor names; document design vs runtime tools separately.
- Prefer in-repo corpus paths as the source of truth; va-agent-swarm is optional upstream if already mirrored under `business/video/corpus`.
- Output/update the agent materials under `business/video/agents/video.animator_2d/` (especially SPEC.md); keep content self-contained under that agent folder where practical.
