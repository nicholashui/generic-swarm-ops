# Project Memory

- Project name: **generic-swarm-ops** (https://github.com/nicholashui/generic-swarm-ops) — not “genetic”
- Companion research corpus: **va-agent-swarm** (https://github.com/nicholashui/va-agent-swarm) — video MMA specs only
- Purpose: Governed, auditable, self-improving multi-agent **universal MMA host**; video domain arrives as Domain Pack
- Product bar: mark ~100 (`structure_scorecard_100.md`, `mark_100_verification.md`); E1 path PASS
- Harnesses: Trae IDE (`.trae/`) and Grok Build (`.grok/`) — dual-harness via `npm run sync`
- Stack: Node.js 20+ bootstrap; FastAPI + **Postgres** primary store (`backend/`); Next.js ops console (`frontend/`)
- Shipped: tool adapters + tool_effects, PI disk artifacts, evolution corpus/canary, self-improvement (reflect/lessons/propose/loops), K1-lite graph, FE Improve + `/app/evolution`
- Continuity: use `memory/handoff.md` across sessions and tools
- Policy: external/sources untrusted until audited; evolution sandbox-only until approved; no host code self-rewrite
- **Strategy docs:** `adoption.md` v2.3 (N1/N2/N3, L0/L1/L2); `repo_compare.md`; **`improvements.md` v1.0** (Waves 0–5); **`improvement_prompt.txt`** (SDD: requirements → design → tasks per wave under `planning/improvement/<wave>/`)
- **Merge shape:** generic = host; va = full `business/video/` pack (114 agents + all processes, retained forever); no second platform; no domain pollution of core
- **Next major work (when asked):** execute improvements Waves starting at Wave 0 via full SDD protocol
