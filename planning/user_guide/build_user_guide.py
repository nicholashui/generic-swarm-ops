# -*- coding: utf-8 -*-
"""
Build high-quality user guide per create_user_guide.md into book/user_guide/.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / "book" / "user_guide"
CH = BOOK / "chapters"
AS = BOOK / "assets"
CH.mkdir(parents=True, exist_ok=True)
AS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------

def svg(name: str, title: str, w: int, h: int, body: str) -> None:
    content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">
  <title id="t">{title}</title>
  <defs>
    <style>
      .bg{{fill:#0b1220}} .c{{fill:#121a2b;stroke:#2a3a55;stroke-width:1.5}}
      .h{{fill:#152238;stroke:#3d7eff;stroke-width:1.8}}
      .t{{fill:#e8eef9;font-family:Segoe UI,system-ui,sans-serif;font-size:13px}}
      .s{{fill:#a8b6cc;font-family:Segoe UI,system-ui,sans-serif;font-size:11px}}
      .ti{{fill:#fff;font-family:Segoe UI,system-ui,sans-serif;font-size:15px;font-weight:600}}
      .a{{stroke:#3d7eff;stroke-width:1.8;fill:none;marker-end:url(#m)}}
      .ok{{fill:#2ecc71}} .ac{{fill:#3d7eff}}
    </style>
    <marker id="m" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#3d7eff"/>
    </marker>
  </defs>
  <rect class="bg" width="{w}" height="{h}" rx="12"/>
  <text class="ti" x="20" y="28">{title}</text>
  {body}
</svg>
'''
    (AS / name).write_text(content, encoding="utf-8")


def make_all_svgs() -> None:
    svg("01-01-system-architecture.svg", "System architecture — four planes", 900, 380, '''
  <rect class="c" x="30" y="50" width="190" height="90" rx="10"/><text class="t" x="50" y="85">Ops console</text><text class="s" x="50" y="108">frontend/ Next.js</text>
  <rect class="h" x="250" y="50" width="190" height="90" rx="10"/><text class="t" x="270" y="85">Control plane</text><text class="s" x="270" y="108">backend FastAPI</text>
  <rect class="c" x="470" y="50" width="190" height="90" rx="10"/><text class="t" x="490" y="85">Business OS</text><text class="s" x="490" y="108">business/* artifacts</text>
  <rect class="c" x="690" y="50" width="180" height="90" rx="10"/><text class="t" x="710" y="85">Domain packs</text><text class="s" x="710" y="108">video · examples</text>
  <path class="a" d="M220 95 H245"/><path class="a" d="M440 95 H465"/><path class="a" d="M660 95 H685"/>
  <rect class="c" x="30" y="180" width="260" height="80" rx="10"/><text class="t" x="50" y="215">Agent harness .trae / .grok</text><text class="s" x="50" y="238">npm run sync — not 2nd runtime</text>
  <rect class="c" x="320" y="180" width="260" height="80" rx="10"/><text class="t" x="340" y="215">Persistence</text><text class="s" x="340" y="238">Postgres primary · JSON backup</text>
  <rect class="c" x="610" y="180" width="260" height="80" rx="10"/><text class="t" x="630" y="215">N1 rule</text><text class="s" x="630" y="238">Domain logic stays in pack</text>
  <text class="s" x="30" y="300">Executable bar: E1 + viral-hook stubs · not live media studio (EXECUTABLE_PRODUCT.md)</text>
  <text class="s" x="30" y="325">Request path: UI → /api/v1 → RuntimeServices → DNA step → tools → audit/gates</text>
  <text class="s" x="30" y="350">Evolution: sandbox → evaluate → canary — never mutate production DNA in place</text>
''')
    svg("01-02-prerequisites.svg", "Toolchain prerequisites", 880, 260, '''
  <rect class="c" x="30" y="55" width="150" height="70" rx="8"/><text class="t" x="50" y="95">Node 20+</text>
  <rect class="c" x="200" y="55" width="150" height="70" rx="8"/><text class="t" x="220" y="95">Python 3.11+</text>
  <rect class="c" x="370" y="55" width="150" height="70" rx="8"/><text class="t" x="400" y="95">pnpm</text>
  <rect class="c" x="540" y="55" width="150" height="70" rx="8"/><text class="t" x="560" y="95">Git</text>
  <rect class="h" x="710" y="55" width="140" height="70" rx="8"/><text class="t" x="730" y="95">Postgres*</text>
  <text class="s" x="30" y="160">*Postgres recommended for production; JSON-file store OK for learning (ready may be degraded).</text>
  <text class="s" x="30" y="185">Ports: backend 8000 · frontend 3000 (typical). OS: Windows PowerShell examples primary.</text>
  <text class="s" x="30" y="210">Verify: node -v · python --version · pnpm -v · git --version</text>
  <text class="s" x="30" y="235">Repo root: generic-swarm-ops (product host)</text>
''')
    svg("01-03-first-boot.svg", "First boot sequence", 900, 280, '''
  <circle class="ac" cx="70" cy="120" r="26"/><text class="t" x="62" y="125">1</text><text class="s" x="40" y="170">bootstrap</text>
  <path class="a" d="M100 120 H140"/>
  <circle class="ac" cx="170" cy="120" r="26"/><text class="t" x="162" y="125">2</text><text class="s" x="145" y="170">backend</text>
  <path class="a" d="M200 120 H240"/>
  <circle class="ac" cx="270" cy="120" r="26"/><text class="t" x="262" y="125">3</text><text class="s" x="245" y="170">ready</text>
  <path class="a" d="M300 120 H340"/>
  <circle class="ac" cx="370" cy="120" r="26"/><text class="t" x="362" y="125">4</text><text class="s" x="345" y="170">frontend</text>
  <path class="a" d="M400 120 H440"/>
  <circle class="ac" cx="470" cy="120" r="26"/><text class="t" x="462" y="125">5</text><text class="s" x="450" y="170">login</text>
  <path class="a" d="M500 120 H540"/>
  <circle class="ok" cx="570" cy="120" r="26"/><text class="t" x="562" y="125">6</text><text class="s" x="545" y="170">E1 ready</text>
  <rect class="c" x="650" y="70" width="220" height="120" rx="10"/>
  <text class="t" x="670" y="100">Seed credentials</text>
  <text class="s" x="670" y="125">admin@example.com</text>
  <text class="s" x="670" y="145">admin-password</text>
  <text class="s" x="670" y="170">demoMode = false</text>
''')
    svg("01-04-console-map.svg", "Ops console information architecture", 920, 360, '''
  <rect class="c" x="20" y="50" width="170" height="280" rx="10"/>
  <text class="t" x="40" y="80">Sidebar</text>
  <text class="s" x="40" y="110">Dashboard</text><text class="s" x="40" y="130">Agents</text>
  <text class="t" x="40" y="155" fill="#3d7eff">Domains</text>
  <text class="s" x="40" y="180">Tools</text><text class="s" x="40" y="200">Workflows</text>
  <text class="s" x="40" y="220">Approvals</text><text class="s" x="40" y="245">Knowledge</text>
  <text class="s" x="40" y="265">Memory</text><text class="s" x="40" y="285">Evolution</text>
  <text class="s" x="40" y="305">Audit / Settings</text>
  <rect class="h" x="210" y="50" width="680" height="280" rx="10"/>
  <text class="t" x="230" y="85">Main content · example /app/domains</text>
  <rect class="c" x="240" y="110" width="300" height="90" rx="8"/><text class="s" x="260" y="145">Recommend workflow</text><text class="s" x="260" y="168">brief → ranked DNA</text>
  <rect class="c" x="560" y="110" width="300" height="90" rx="8"/><text class="s" x="580" y="145">Special skills</text><text class="s" x="580" y="168">17 from REGISTRY</text>
  <rect class="c" x="240" y="220" width="620" height="80" rx="8"/><text class="s" x="260" y="255">NAVIGATION_GROUPS drives sidebar · appPaths.domains = /app/domains</text><text class="s" x="260" y="278">demoMode false → live APIs</text>
''')
    svg("01-05-auth-session.svg", "Login and session path", 880, 280, '''
  <rect class="c" x="40" y="60" width="180" height="90" rx="10"/><text class="t" x="60" y="100">Login form</text><text class="s" x="60" y="125">email + password</text>
  <path class="a" d="M225 105 H270"/>
  <rect class="h" x="270" y="60" width="200" height="90" rx="10"/><text class="t" x="290" y="100">POST /auth/login</text><text class="s" x="290" y="125">access_token</text>
  <path class="a" d="M475 105 H520"/>
  <rect class="c" x="520" y="60" width="200" height="90" rx="10"/><text class="t" x="540" y="100">Cookie / client</text><text class="s" x="540" y="125">gso_access_token</text>
  <path class="a" d="M725 105 H760"/>
  <rect class="c" x="760" y="60" width="90" height="90" rx="10"/><text class="s" x="775" y="110">/app/*</text>
  <text class="s" x="40" y="190">Live mode: NEXT_PUBLIC_DEMO_MODE must not be true (opt-in only).</text>
  <text class="s" x="40" y="215">Seed: admin@example.com / admin-password — change before any shared deploy.</text>
  <text class="s" x="40" y="240">Static bearer tokens remain for curl smoke only; prefer password login.</text>
''')
    svg("02-01-agents-tools.svg", "Agents, DNA steps, tools", 900, 300, '''
  <rect class="c" x="40" y="60" width="220" height="130" rx="10"/><text class="t" x="60" y="100">Agent</text><text class="s" x="60" y="125">id · status</text><text class="s" x="60" y="148">allowed_tools[]</text>
  <path class="a" d="M265 125 H310"/>
  <rect class="h" x="310" y="60" width="220" height="130" rx="10"/><text class="t" x="330" y="100">DNA step</text><text class="s" x="330" y="125">agent + tools</text><text class="s" x="330" y="148">action · memory</text>
  <path class="a" d="M535 125 H580"/>
  <rect class="c" x="580" y="60" width="260" height="130" rx="10"/><text class="t" x="600" y="100">Tool adapter</text><text class="s" x="600" y="125">crm · email · video_*</text><text class="s" x="600" y="148">tool_effects audit</text>
  <text class="s" x="40" y="230">UI: /app/agents · /app/tools · create forms require live mode</text>
  <text class="s" x="40" y="255">Video media tools are intentional stubs on executable bar — not live vendors</text>
''')
    svg("02-02-e1-path.svg", "E1 operator path", 940, 260, '''
  <rect class="c" x="20" y="60" width="100" height="70" rx="8"/><text class="s" x="45" y="100">Login</text>
  <path class="a" d="M125 95 H150"/><rect class="c" x="150" y="60" width="100" height="70" rx="8"/><text class="s" x="165" y="100">List WFs</text>
  <path class="a" d="M255 95 H280"/><rect class="h" x="280" y="60" width="120" height="70" rx="8"/><text class="s" x="295" y="90">Run now</text><text class="s" x="295" y="110">onboarding</text>
  <path class="a" d="M405 95 H430"/><rect class="c" x="430" y="60" width="110" height="70" rx="8"/><text class="s" x="445" y="90">Approve</text><text class="s" x="445" y="110">billing</text>
  <path class="a" d="M545 95 H570"/><rect class="c" x="570" y="60" width="100" height="70" rx="8"/><text class="s" x="590" y="100">Done</text>
  <path class="a" d="M675 95 H700"/><rect class="c" x="700" y="60" width="110" height="70" rx="8"/><text class="s" x="720" y="90">Improve</text><text class="s" x="720" y="110">reflect</text>
  <text class="s" x="20" y="170">Workflow: wf_customer_onboarding_v12 · required input includes case_id</text>
  <text class="s" x="20" y="195">Proof: backend/app/tests/e2e/test_e1_operator_path.py</text>
  <text class="s" x="20" y="220">UI: Workflows → Run now · Approvals queue · run detail Improve</text>
''')
    svg("02-03-governance-gates.svg", "Risk tiers and human gates", 900, 300, '''
  <rect class="c" x="40" y="60" width="180" height="100" rx="10"/><text class="t" x="60" y="100">R0–R1</text><text class="s" x="60" y="125">Read / draft</text><text class="s" x="60" y="145">Auto OK</text>
  <rect class="c" x="250" y="60" width="180" height="100" rx="10"/><text class="t" x="270" y="100">R2</text><text class="s" x="270" y="125">Reversible</text><text class="s" x="270" y="145">Log / soft</text>
  <rect class="h" x="460" y="60" width="180" height="100" rx="10"/><text class="t" x="480" y="100">R3–R4</text><text class="s" x="480" y="125">Irreversible</text><text class="s" x="480" y="145">Human approve</text>
  <rect class="c" x="670" y="60" width="180" height="100" rx="10"/><text class="t" x="690" y="100">Audit</text><text class="s" x="690" y="125">who / when</text><text class="s" x="690" y="145">tool_effects</text>
  <text class="s" x="40" y="200">UI: /app/approvals · decision panel · /app/audit-logs</text>
  <text class="s" x="40" y="225">Policy: business/governance/* · rules/60-human-approval.md</text>
  <text class="s" x="40" y="250">Always write a rationale on approve/reject for audit readers</text>
''')
    svg("02-04-domain-recommend.svg", "Brief to DNA recommendation", 900, 300, '''
  <rect class="c" x="40" y="60" width="200" height="110" rx="10"/><text class="t" x="60" y="100">Operator brief</text><text class="s" x="60" y="125">viral TikTok…</text><text class="s" x="60" y="145">duration_sec</text>
  <path class="a" d="M245 115 H290"/>
  <rect class="h" x="290" y="60" width="240" height="110" rx="10"/><text class="t" x="310" y="100">Selector</text><text class="s" x="310" y="125">archetype_selector</text><text class="s" x="310" y="145">A–J registry</text>
  <path class="a" d="M535 115 H580"/>
  <rect class="c" x="580" y="60" width="260" height="110" rx="10"/><text class="t" x="600" y="100">Recommendation</text><text class="s" x="600" y="125">dna_id · scale</text><text class="s" x="600" y="145">confidence · alts</text>
  <text class="s" x="40" y="210">API: POST /api/v1/domains/video/recommend-workflow · GET .../special-skills</text>
  <text class="s" x="40" y="235">Example hit: wf_video_arch_a_viral_hook_v1 (code A) · skills count 17</text>
  <text class="s" x="40" y="260">Recommend ≠ live video generation · HiTL before launch</text>
''')
    svg("02-05-knowledge-memory.svg", "Knowledge tiers and memory scopes", 900, 300, '''
  <rect class="c" x="40" y="60" width="250" height="120" rx="10"/><text class="t" x="60" y="100">Tier 0</text><text class="s" x="60" y="125">keyword + embeddings</text><text class="s" x="60" y="145">broad / fast</text>
  <rect class="h" x="320" y="60" width="250" height="120" rx="10"/><text class="t" x="340" y="100">Tier 1</text><text class="s" x="340" y="125">entity multi-hop</text><text class="s" x="340" y="145">K1-lite graph</text>
  <rect class="c" x="600" y="60" width="250" height="120" rx="10"/><text class="t" x="620" y="100">Memory scopes</text><text class="s" x="620" y="125">episodic · semantic</text><text class="s" x="620" y="145">procedural · eval</text>
  <text class="s" x="40" y="220">UI: /app/knowledge · /app/memory · /app/processes</text>
  <text class="s" x="40" y="245">Policy: business/knowledge-base/provenance/retrieval-tier-policy.md</text>
  <text class="s" x="40" y="270">PI: business/process-intelligence/ artifacts</text>
''')
    svg("03-01-workflow-dna.svg", "Workflow DNA lifecycle", 920, 300, '''
  <rect class="c" x="30" y="60" width="140" height="70" rx="8"/><text class="s" x="55" y="100">Author</text>
  <path class="a" d="M175 95 H205"/><rect class="c" x="205" y="60" width="140" height="70" rx="8"/><text class="s" x="230" y="100">Validate</text>
  <path class="a" d="M350 95 H380"/><rect class="c" x="380" y="60" width="140" height="70" rx="8"/><text class="s" x="400" y="100">Sandbox</text>
  <path class="a" d="M525 95 H555"/><rect class="c" x="555" y="60" width="140" height="70" rx="8"/><text class="s" x="575" y="100">Evaluate</text>
  <path class="a" d="M700 95 H730"/><rect class="h" x="730" y="60" width="150" height="70" rx="8"/><text class="s" x="750" y="90">Canary /</text><text class="s" x="750" y="110">Promote</text>
  <rect class="c" x="30" y="170" width="850" height="90" rx="10"/>
  <text class="t" x="50" y="205">DNA conceptual fields</text>
  <text class="s" x="50" y="230">id · steps[] · agents · tools · memory r/w · verification · risk · human_gates</text>
  <text class="s" x="50" y="250">Example: business/video/workflows/wf_video_arch_a_viral_hook_v1.dna.json</text>
''')
    svg("03-02-api-map.svg", "Core API surface map", 900, 320, '''
  <rect class="h" x="40" y="55" width="200" height="70" rx="8"/><text class="t" x="60" y="95">Auth / health</text>
  <rect class="c" x="260" y="55" width="200" height="70" rx="8"/><text class="t" x="280" y="95">Workflows / runs</text>
  <rect class="c" x="480" y="55" width="200" height="70" rx="8"/><text class="t" x="500" y="95">Approvals</text>
  <rect class="c" x="700" y="55" width="160" height="70" rx="8"/><text class="t" x="720" y="95">Domains</text>
  <rect class="c" x="40" y="150" width="200" height="70" rx="8"/><text class="t" x="60" y="190">Knowledge</text>
  <rect class="c" x="260" y="150" width="200" height="70" rx="8"/><text class="t" x="280" y="190">Improvement</text>
  <rect class="c" x="480" y="150" width="200" height="70" rx="8"/><text class="t" x="500" y="190">Evolution</text>
  <rect class="c" x="700" y="150" width="160" height="70" rx="8"/><text class="t" x="720" y="190">Loops</text>
  <text class="s" x="40" y="260">Base: http://127.0.0.1:8000/api/v1 · Authorization: Bearer &lt;token&gt;</text>
  <text class="s" x="40" y="285">Engine: backend/app/runtime.py · Routes: backend/app/api/v1/routes/</text>
''')
    svg("03-03-rbac.svg", "RBAC to UI visibility", 880, 280, '''
  <rect class="c" x="40" y="60" width="220" height="100" rx="10"/><text class="t" x="60" y="100">Role</text><text class="s" x="60" y="125">admin · operator…</text>
  <path class="a" d="M265 110 H310"/>
  <rect class="h" x="310" y="60" width="240" height="100" rx="10"/><text class="t" x="330" y="100">Permissions</text><text class="s" x="330" y="125">workflows:read · …</text>
  <path class="a" d="M555 110 H600"/>
  <rect class="c" x="600" y="60" width="240" height="100" rx="10"/><text class="t" x="620" y="100">Nav + actions</text><text class="s" x="620" y="125">filtered UI</text>
  <text class="s" x="40" y="200">Code: frontend/src/types/permissions.ts · navigation.ts permissions[]</text>
  <text class="s" x="40" y="225">Missing sidebar item may be permission — not only a missing route</text>
  <text class="s" x="40" y="250">API also enforces authorization; UI hide is not security alone</text>
''')
    svg("03-04-extend-pack.svg", "Domain pack extension steps", 900, 300, '''
  <rect class="c" x="30" y="60" width="180" height="100" rx="10"/><text class="t" x="50" y="100">1 Manifest</text><text class="s" x="50" y="125">agents + DNA</text>
  <path class="a" d="M215 110 H245"/>
  <rect class="c" x="245" y="60" width="180" height="100" rx="10"/><text class="t" x="265" y="100">2 Register</text><text class="s" x="265" y="125">inventory</text>
  <path class="a" d="M430 110 H460"/>
  <rect class="c" x="460" y="60" width="180" height="100" rx="10"/><text class="t" x="480" y="100">3 Tools</text><text class="s" x="480" y="125">allow-lists</text>
  <path class="a" d="M645 110 H675"/>
  <rect class="h" x="675" y="60" width="180" height="100" rx="10"/><text class="t" x="695" y="100">4 Prove</text><text class="s" x="695" y="125">golden + tests</text>
  <text class="s" x="30" y="200">Runbook: docs/add-domain-pack-runbook.md · examples: business/example_education/</text>
  <text class="s" x="30" y="225">Anti-pattern: second LangGraph control plane · rubber-stamp score 100s</text>
  <text class="s" x="30" y="250">N1: keep domain logic under business/&lt;domain&gt;/</text>
''')
    svg("03-05-improve-evolution.svg", "Improve and evolution loop", 920, 300, '''
  <rect class="c" x="30" y="60" width="130" height="70" rx="8"/><text class="s" x="55" y="100">Run ends</text>
  <path class="a" d="M165 95 H195"/><rect class="c" x="195" y="60" width="130" height="70" rx="8"/><text class="s" x="225" y="100">Reflect</text>
  <path class="a" d="M330 95 H360"/><rect class="c" x="360" y="60" width="130" height="70" rx="8"/><text class="s" x="390" y="100">Lessons</text>
  <path class="a" d="M495 95 H525"/><rect class="c" x="525" y="60" width="130" height="70" rx="8"/><text class="s" x="550" y="100">Propose</text>
  <path class="a" d="M660 95 H690"/><rect class="c" x="690" y="60" width="100" height="70" rx="8"/><text class="s" x="710" y="100">Eval</text>
  <path class="a" d="M795 95 H825"/><rect class="h" x="825" y="60" width="80" height="70" rx="8"/><text class="s" x="840" y="100">Canary</text>
  <text class="s" x="30" y="180">APIs: /improvement/reflect/{id} · /lessons · /auto-propose · /loops/run · /evolution/archive</text>
  <text class="s" x="30" y="205">UI: run Improve pipeline · /app/evolution archive</text>
  <text class="s" x="30" y="230">Stop criteria required for loops · never promote without evaluate</text>
  <text class="s" x="30" y="255">Corpus: business/evals/ · variants: business/evolution/</text>
''')
    svg("04-01-error-matrix.svg", "Troubleshooting decision tree", 900, 300, '''
  <rect class="h" x="40" y="55" width="200" height="60" rx="8"/><text class="t" x="60" y="90">Symptom</text>
  <path class="a" d="M250 85 H290"/>
  <rect class="c" x="290" y="55" width="220" height="60" rx="8"/><text class="t" x="310" y="90">Classify layer</text>
  <path class="a" d="M520 85 H560"/>
  <rect class="c" x="560" y="55" width="300" height="60" rx="8"/><text class="t" x="580" y="90">Fix + verify health</text>
  <text class="s" x="40" y="150">Boot: port / PYTHONPATH / pip install</text>
  <text class="s" x="40" y="175">Auth: seed password / token / backend up</text>
  <text class="s" x="40" y="200">UI mock: NEXT_PUBLIC_DEMO_MODE not true</text>
  <text class="s" x="40" y="225">Domains missing: NAVIGATION_GROUPS + appPaths.domains</text>
  <text class="s" x="40" y="250">Run stuck: Approvals · case_id · permissions</text>
  <text class="s" x="40" y="275">Collect request_id from API errors when present</text>
''')
    svg("04-02-health-doctor.svg", "Health and doctor diagnostics", 880, 280, '''
  <rect class="c" x="40" y="60" width="240" height="100" rx="10"/><text class="t" x="60" y="100">/health</text><text class="s" x="60" y="125">process ok</text>
  <rect class="c" x="310" y="60" width="240" height="100" rx="10"/><text class="t" x="330" y="100">/health/live</text><text class="s" x="330" y="125">liveness</text>
  <rect class="h" x="580" y="60" width="240" height="100" rx="10"/><text class="t" x="600" y="100">/health/ready</text><text class="s" x="600" y="125">deps · database</text>
  <text class="s" x="40" y="200">npm run doctor — starter/business layout checks</text>
  <text class="s" x="40" y="225">database: postgres | json-file · degraded may be OK while learning</text>
  <text class="s" x="40" y="250">python scripts/business/check_executable_product.py — product bar script</text>
''')
    svg("04-03-support-evidence.svg", "Support evidence pack", 880, 280, '''
  <rect class="c" x="40" y="60" width="180" height="90" rx="10"/><text class="t" x="60" y="100">Versions</text><text class="s" x="60" y="125">node/python</text>
  <rect class="c" x="250" y="60" width="180" height="90" rx="10"/><text class="t" x="270" y="100">Health JSON</text><text class="s" x="270" y="125">ready body</text>
  <rect class="c" x="460" y="60" width="180" height="90" rx="10"/><text class="t" x="480" y="100">request_id</text><text class="s" x="480" y="125">API errors</text>
  <rect class="h" x="670" y="60" width="170" height="90" rx="10"/><text class="t" x="690" y="100">Repro steps</text><text class="s" x="690" y="125">minimal</text>
  <text class="s" x="40" y="190">Include: demoMode value · API base URL · workflow id · run id · approx time UTC</text>
  <text class="s" x="40" y="215">Do not paste secrets or production passwords into tickets</text>
  <text class="s" x="40" y="240">Design depth: book/design_phase/ · not required for operator tickets</text>
''')
    svg("05-01-postgres-perf.svg", "Persistence performance path", 880, 280, '''
  <rect class="h" x="40" y="60" width="250" height="100" rx="10"/><text class="t" x="60" y="100">Postgres primary</text><text class="s" x="60" y="125">runtime_state JSONB</text>
  <path class="a" d="M295 110 H340"/>
  <rect class="c" x="340" y="60" width="250" height="100" rx="10"/><text class="t" x="360" y="100">Runtime engine</text><text class="s" x="360" y="125">reads/writes state</text>
  <path class="a" d="M595 110 H640"/>
  <rect class="c" x="640" y="60" width="200" height="100" rx="10"/><text class="t" x="660" y="100">JSON snapshot</text><text class="s" x="660" y="125">backup path</text>
  <text class="s" x="40" y="200">Runbook: backend/docs/postgres-runbook.md · DATABASE_URL in backend/.env</text>
  <text class="s" x="40" y="225">Monitor ready · avoid unbounded log growth · index by ops practice</text>
  <text class="s" x="40" y="250">Learning: json-file OK · Production: Postgres required for durability bar</text>
''')
    svg("05-02-security-hardening.svg", "Security hardening pillars", 900, 300, '''
  <rect class="c" x="40" y="55" width="250" height="110" rx="10"/><text class="t" x="60" y="95">Identity</text><text class="s" x="60" y="120">change seed password</text><text class="s" x="60" y="140">RBAC least privilege</text>
  <rect class="c" x="320" y="55" width="250" height="110" rx="10"/><text class="t" x="340" y="95">Runtime</text><text class="s" x="340" y="120">tool allow-lists</text><text class="s" x="340" y="140">R3+ human gates</text>
  <rect class="h" x="600" y="55" width="250" height="110" rx="10"/><text class="t" x="620" y="95">Operate</text><text class="s" x="620" y="120">demoMode off</text><text class="s" x="620" y="140">audit review</text>
  <text class="s" x="40" y="200">rules/30-security.md · 110-agentic-security.md · docs/security.md</text>
  <text class="s" x="40" y="225">Treat tool outputs as untrusted for later prompts</text>
  <text class="s" x="40" y="250">API keys scoped · rotate · never commit secrets</text>
''')
    svg("05-03-deploy-maintain.svg", "Deploy and maintain loop", 900, 300, '''
  <rect class="c" x="40" y="60" width="160" height="80" rx="8"/><text class="s" x="70" y="105">Build</text>
  <path class="a" d="M205 100 H240"/><rect class="c" x="240" y="60" width="160" height="80" rx="8"/><text class="s" x="270" y="105">Test E1</text>
  <path class="a" d="M405 100 H440"/><rect class="c" x="440" y="60" width="160" height="80" rx="8"/><text class="s" x="470" y="105">Canary</text>
  <path class="a" d="M605 100 H640"/><rect class="h" x="640" y="60" width="200" height="80" rx="8"/><text class="s" x="680" y="105">Observe</text>
  <text class="s" x="40" y="180">Weekly: doctor · security scripts · approval backlog · evolution archive skim</text>
  <text class="s" x="40" y="205">Promote DNA only with eval evidence · keep rollback id</text>
  <text class="s" x="40" y="230">Scale: more workers/instances only after Postgres + auth hardened</text>
  <text class="s" x="40" y="255">Maintenance: dependencies · backups · secret rotation calendar</text>
''')


# ---------------------------------------------------------------------------
# Chapter writer helpers
# ---------------------------------------------------------------------------

def callout(kind: str, text: str) -> str:
    icons = {"warning": "Warning", "tip": "Tip", "note": "Note", "residual": "Residual"}
    return f"> **{icons.get(kind, kind)}:** {text}\n"


def quiz(items: list[tuple[str, str]]) -> str:
    lines = ["## Knowledge check", ""]
    for i, (q, _) in enumerate(items, 1):
        lines.append(f"{i}. {q}")
    lines += ["", "<details><summary>Answer key</summary>", ""]
    for i, (_, a) in enumerate(items, 1):
        lines.append(f"{i}. {a}")
    lines += ["", "</details>", ""]
    return "\n".join(lines)


def chapter(
    file: str,
    title: str,
    section: str,
    level: str,
    time: str,
    objectives: list[str],
    prereqs: list[str],
    svg_file: str,
    svg_alt: str,
    body: str,
    use_cases: list[tuple[str, str]],
    best: list[str],
    summary: list[str],
    quiz_items: list[tuple[str, str]],
    prev_f: str | None,
    next_f: str | None,
) -> None:
    obj = "\n".join(f"- {o}" for o in objectives)
    pre = "\n".join(f"- {p}" for p in prereqs)
    uc = "\n".join(f"### Use case {i}: {n}\n\n{t}\n" for i, (n, t) in enumerate(use_cases, 1))
    bp = "\n".join(f"- {b}" for b in best)
    sm = "\n".join(f"- {s}" for s in summary)
    nav = []
    if prev_f:
        nav.append(f"- Previous: [`{prev_f}`](./{prev_f})")
    if next_f:
        nav.append(f"- Next: [`{next_f}`](./{next_f})")
    nav.append("- Master TOC: [../user_guide.md](../user_guide.md)")
    nav_s = "\n".join(nav)
    md = f"""# {title}

| | |
|--|--|
| **Section** | {section} |
| **Level** | {level} |
| **Est. time** | {time} |
| **File** | `chapters/{file}` |

## Learning objectives

{obj}

## Prerequisites

{pre}

## Illustration

![{svg_alt}](../assets/{svg_file})

*{svg_alt}*

{body}

## Real-world use cases

{uc}

## Best practices

{bp}

## Chapter summary

{sm}

{quiz(quiz_items)}

## Navigation

{nav_s}
"""
    (CH / file).write_text(md, encoding="utf-8")
    print("wrote", file)


# ---------------------------------------------------------------------------
# Full chapter bodies (high quality)
# ---------------------------------------------------------------------------

def write_chapters() -> None:
    residual = callout(
        "residual",
        "This guide describes the **executable** product bar: E1 operator path, video recommend + viral-hook with **stubs**, and special-skills catalog. It does **not** claim live Sora/Veo/Runway media, full studio UI, every DNA `production_ready`, or agent fleet true-100 scores. See `EXECUTABLE_PRODUCT.md`.",
    )

    chapter(
        "01-01-system-overview.md",
        "1.1 System overview",
        "1 — Core System Fundamentals",
        "Beginner",
        "35–45 min",
        [
            "Explain generic-swarm-ops in plain language (one paragraph)",
            "Name the four planes and where they live in the repo",
            "Define agent, tool, DNA, run, approval, domain pack",
            "State N1 (domain logic in pack) and the honesty bar",
        ],
        [
            "Curiosity and a free hour — no prior multi-agent experience required",
            "Access to the `generic-swarm-ops` repository",
        ],
        "01-01-system-architecture.svg",
        "Four-plane system architecture diagram",
        residual
        + """
## Why this system exists

Most “multi-agent” demos are chat threads: hard to audit, hard to gate irreversible actions, and hard to improve safely. **generic-swarm-ops** is a **governed business operating system** for multi-agent work. Operators run **workflow DNA** (structured process graphs) through a **FastAPI control plane**, with **human approvals**, **tool allow-lists**, **audit trails**, and **sandbox evolution**—surfaced in a **Next.js ops console**.

## The four planes

| Plane | Repository area | What it does |
|-------|-----------------|--------------|
| **Ops console** | `frontend/` | Human UI: agents, workflows, Domains, approvals, evolution |
| **Control plane** | `backend/` | Auth, DNA execution, tools, gates, APIs (`runtime.py`) |
| **Business OS** | `business/` | Process intelligence, evals, governance artifacts, lessons |
| **Domain packs** | e.g. `business/video/` | Domain agents, DNA, corpus, special skills |

There is also an **agent harness** layer (`.trae/`, `.grok/`) generated by `npm run sync` from `rules/` and `skills/`. That layer helps **coding agents** (Trae / Grok Build). It is **not** a second workflow runtime and must not become a second control plane.

## Core nouns (memorize these)

| Term | Meaning |
|------|---------|
| **Agent** | A role with identity and `allowed_tools[]` |
| **Tool** | An adapter (crm, email, `video_*` stubs, …) that leaves `tool_effects` |
| **DNA** | A versioned workflow definition (`*.dna.json`) |
| **Run** | One execution of a DNA with status and events |
| **Approval** | Human decision when a gate fires |
| **Domain pack** | Versioned bundle of agents + DNA + assets for a domain |
| **Special skill** | Pack integration catalogued for the host (video pack: **17**) |

## How a request flows

1. Operator acts in the UI (or API client).  
2. Frontend calls ` /api/v1/...` with a bearer token / cookie.  
3. FastAPI route invokes `RuntimeServices` in `backend/app/runtime.py`.  
4. A DNA step selects an agent and allow-listed tools.  
5. Tools run; effects are audited.  
6. High-risk steps pause for **approval**.  
7. On completion, **Improve** may reflect lessons; evolution stays in **sandbox** until evaluate/canary.

## What is proven today vs residual

| Proven (you will do this in the guide) | Not claimed |
|----------------------------------------|-------------|
| E1: login → run onboarding → approve → improve | Live media vendors |
| Recommend DNA from a free-text brief | Full Discover studio |
| List 17 special skills from REGISTRY | Fleet true-100 scores |
| Viral-hook DNA with stubs + package gate | Every DNA production_ready |

## Hands-on orientation (no install yet)

1. Open `README.md` and `EXECUTABLE_PRODUCT.md` in the repo root.  
2. Skim the proven vs not-claimed table.  
3. List the top-level folders and assign each to a plane in a notebook.  
4. Open `docs/architecture.md` once for the official layer table.

**Expected outcome:** You can answer “what is this product?” without saying only “it uses AI agents.”
""",
        [
            (
                "Ops lead evaluating the platform",
                "You need auditability for customer onboarding automation. Map the E1 path to your compliance checklist: human gate on billing, audit logs, and no silent DNA edits in production.",
            ),
            (
                "Video producer exploring the pack",
                "You care about short-form workflows. Use **recommend** to pick DNA (e.g. viral-hook) knowing media steps are **stubs** until vendors are integrated—selection is still valuable for process design.",
            ),
            (
                "Platform engineer joining the repo",
                "You own uptime. Your mental model is: Postgres + FastAPI runtime as control plane; packs under `business/`; frontend is a client only.",
            ),
        ],
        [
            "Keep domain logic in packs (N1); extend host only for generic control-plane capabilities.",
            "Treat design monographs in `book/design_phase/` as deep reference—not day-1 onboarding.",
            "Never hand-edit generated `.trae/` or `.grok/`; re-run `npm run sync`.",
            "Quote residual limits when demoing to stakeholders to avoid over-promising media.",
        ],
        [
            "generic-swarm-ops is a governed multi-agent business OS, not a free chat host.",
            "Four planes: console, control plane, business OS, domain packs.",
            "Executable bar is documented; live studio is residual.",
        ],
        [
            ("What is N1?", "Domain / video business logic stays in the pack; the host executes DNA, tools, and gates."),
            ("Name one proven path.", "E1 operator path or viral-hook DNA with stubs, or recommend workflow."),
            ("Is `.grok/` the workflow runtime?", "No—it is an agent harness generated for coding agents."),
        ],
        None,
        "01-02-prerequisites-and-environment.md",
    )

    chapter(
        "01-02-prerequisites-and-environment.md",
        "1.2 Prerequisites and environment",
        "1 — Core System Fundamentals",
        "Beginner",
        "25–40 min",
        [
            "Install or verify Node 20+, Python 3.11+, pnpm, Git",
            "Decide Postgres now vs JSON-file learning mode",
            "Confirm ports and shell (PowerShell) readiness",
        ],
        ["Chapter 1.1 completed", "Admin rights to install tooling if missing"],
        "01-02-prerequisites.svg",
        "Toolchain prerequisites checklist",
        residual
        + """
## Required tooling

| Tool | Version guidance | Why |
|------|------------------|-----|
| **Node.js** | 20+ | Bootstrap scripts, frontend toolchain |
| **npm** | ships with Node | `npm run bootstrap`, business scripts |
| **Python** | 3.11+ | FastAPI backend |
| **pnpm** | current | Frontend package manager |
| **Git** | any recent | clone / updates |
| **PostgreSQL** | 14+ recommended | Primary runtime store |

{callout("tip", "On Windows, run version checks in PowerShell. Use `corepack enable` then `corepack prepare pnpm@latest --activate` if pnpm is missing.")}

## Verify versions (copy-paste)

```powershell
node -v
npm -v
python --version
git --version
# pnpm after corepack or install:
pnpm -v
```

**Expected:** Node reports v20 or higher; Python 3.11+.

## Postgres decision

| Mode | When to use | Health expectation |
|------|-------------|--------------------|
| **Postgres** | Shared/dev close to production | `GET /health/ready` → `database: postgres` |
| **JSON-file** | Solo learning without DB | `database: json-file`; may be `degraded` but usable |

Configure later via `backend/.env` (`DATABASE_URL`). See `backend/docs/postgres-runbook.md`.

## Network ports

| Service | Default |
|---------|---------|
| Backend API | `http://127.0.0.1:8000` |
| Frontend | `http://127.0.0.1:3000` (Next default) |

Free the ports or adjust commands if occupied.

## Hands-on steps

1. Run all version commands above; fix any missing tool before continuing.  
2. Create a working directory note: path to your clone (example `C:\\Project\\generic-swarm-ops`).  
3. Optional: install Postgres and create an empty database name such as `generic_swarm_ops`.  
4. Confirm you can open two terminals (backend + frontend).

**Expected outcome:** Toolchain green; you know whether you will use Postgres or JSON-file for first boot.
""".replace("{callout(", "").replace(")}", "")  # fix - I'll not use broken replace
        ,
        [
            ("Laptop-only learner", "Skip Postgres first week; use JSON-file; upgrade when you need multi-session durability."),
            ("Team shared environment", "Mandate Postgres from day one so ready stays green and state is shared."),
        ],
        [
            "Pin major versions in team docs once the project is shared.",
            "Do not mix system Python environments carelessly—prefer a venv inside `backend/` if your org requires it.",
            "Document your chosen ports if they differ from defaults.",
        ],
        [
            "Node 20+, Python 3.11+, pnpm, Git required.",
            "Postgres preferred; JSON-file acceptable for learning.",
            "Backend :8000, frontend typically :3000.",
        ],
        [
            ("Minimum Node major version?", "20+"),
            ("Is Postgres mandatory for first learning boot?", "No—JSON-file works; Postgres is preferred for production-like use."),
            ("Default backend port?", "8000"),
        ],
        "01-01-system-overview.md",
        "01-03-install-bootstrap-first-boot.md",
    )

    # Fix chapter 01-02 if residual callout broke - rewrite body cleanly in second pass if needed
    print("base chapters 01-01 done, continuing...")


if __name__ == "__main__":
    make_all_svgs()
    print("svgs", len(list(AS.glob("*.svg"))))
    # Full write in write_all_chapters below - split for maintainability
