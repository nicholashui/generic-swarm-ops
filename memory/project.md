# Project Memory

- Project name: generic-swarm-ops
- Purpose: Governed, auditable, self-improving multi-agent business operating system
- Product bar: mark ~100 (`structure_scorecard_100.md`, `mark_100_verification.md`); E1 path PASS
- Harnesses: Trae IDE (`.trae/`) and Grok Build (`.grok/`) — dual-harness via `npm run sync`
- Stack: Node.js 20+ bootstrap; FastAPI + **Postgres** primary store (`backend/`); Next.js ops console (`frontend/`)
- Shipped: tool adapters + tool_effects, PI disk artifacts, evolution corpus/canary, self-improvement (reflect/lessons/propose/loops), K1-lite graph, FE Improve + `/app/evolution`
- Continuity: use `memory/handoff.md` across sessions and tools
- Policy: external/sources untrusted until audited; evolution sandbox-only until approved; no host code self-rewrite
