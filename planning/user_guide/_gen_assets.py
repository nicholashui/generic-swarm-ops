"""Generate SVG assets for user_guide plan chapters."""
from __future__ import annotations

from pathlib import Path

# Canonical publish home for user guide illustrations
ASSETS = Path(__file__).resolve().parents[2] / "book" / "user_guide" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)


def svg_wrap(w: int, h: int, body: str, title: str = "") -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
  <defs>
    <style>
      .bg {{ fill: #0b1220; }}
      .card {{ fill: #121a2b; stroke: #2a3a55; stroke-width: 1.5; }}
      .card-hi {{ fill: #152238; stroke: #3d7eff; stroke-width: 1.8; }}
      .t {{ fill: #e8eef9; font-family: Segoe UI, system-ui, sans-serif; font-size: 14px; }}
      .t-sm {{ fill: #a8b6cc; font-family: Segoe UI, system-ui, sans-serif; font-size: 11px; }}
      .t-title {{ fill: #ffffff; font-family: Segoe UI, system-ui, sans-serif; font-size: 16px; font-weight: 600; }}
      .accent {{ fill: #3d7eff; }}
      .ok {{ fill: #2ecc71; }}
      .line {{ stroke: #4a6080; stroke-width: 1.6; fill: none; }}
      .arrow {{ stroke: #3d7eff; stroke-width: 1.8; fill: none; marker-end: url(#arr); }}
    </style>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#3d7eff"/>
    </marker>
  </defs>
  <rect class="bg" width="{w}" height="{h}" rx="12"/>
  {body}
</svg>
"""


SVGS: dict[str, str] = {
    "01-learning-path.svg": svg_wrap(
        920,
        220,
        """
  <text class="t-title" x="24" y="36">Beginner to expert learning path</text>
  <g>
    <rect class="card-hi" x="24" y="60" width="150" height="120" rx="10"/>
    <text class="t" x="44" y="95">Part I</text>
    <text class="t-sm" x="44" y="120">Mental model</text>
    <text class="t-sm" x="44" y="140">Install and boot</text>
    <text class="t-sm" x="44" y="160">Console tour</text>
  </g>
  <path class="arrow" d="M180 120 H210"/>
  <g>
    <rect class="card" x="210" y="60" width="150" height="120" rx="10"/>
    <text class="t" x="230" y="95">Part II</text>
    <text class="t-sm" x="230" y="120">First E1 run</text>
    <text class="t-sm" x="230" y="140">Approvals</text>
    <text class="t-sm" x="230" y="160">Agents and tools</text>
  </g>
  <path class="arrow" d="M366 120 H396"/>
  <g>
    <rect class="card" x="396" y="60" width="150" height="120" rx="10"/>
    <text class="t" x="416" y="95">Part III</text>
    <text class="t-sm" x="416" y="120">Domains</text>
    <text class="t-sm" x="416" y="140">Recommend DNA</text>
    <text class="t-sm" x="416" y="160">Special skills</text>
  </g>
  <path class="arrow" d="M552 120 H582"/>
  <g>
    <rect class="card" x="582" y="60" width="150" height="120" rx="10"/>
    <text class="t" x="602" y="95">Part IV</text>
    <text class="t-sm" x="602" y="120">Knowledge</text>
    <text class="t-sm" x="602" y="140">PI and evals</text>
    <text class="t-sm" x="602" y="160">Evolution</text>
  </g>
  <path class="arrow" d="M738 120 H768"/>
  <g>
    <rect class="card" x="768" y="60" width="130" height="120" rx="10"/>
    <text class="t" x="788" y="95">Part V</text>
    <text class="t-sm" x="788" y="120">Extend</text>
    <text class="t-sm" x="788" y="140">Secure</text>
    <text class="t-sm" x="788" y="160">Produce</text>
  </g>
""",
        "Learning path",
    ),
    "02-system-overview.svg": svg_wrap(
        920,
        420,
        """
  <text class="t-title" x="24" y="36">System overview — four planes</text>
  <rect class="card" x="40" y="60" width="200" height="90" rx="10"/>
  <text class="t" x="60" y="95">Ops Console</text>
  <text class="t-sm" x="60" y="120">Next.js /app/*</text>
  <text class="t-sm" x="60" y="138">Live API client</text>
  <rect class="card-hi" x="280" y="60" width="200" height="90" rx="10"/>
  <text class="t" x="300" y="95">Control plane</text>
  <text class="t-sm" x="300" y="120">FastAPI + runtime</text>
  <text class="t-sm" x="300" y="138">Auth · DNA · gates</text>
  <rect class="card" x="520" y="60" width="200" height="90" rx="10"/>
  <text class="t" x="540" y="95">Business OS</text>
  <text class="t-sm" x="540" y="120">business/* artifacts</text>
  <text class="t-sm" x="540" y="138">PI · evals · gov</text>
  <rect class="card" x="700" y="200" width="180" height="90" rx="10"/>
  <text class="t" x="720" y="235">Domain packs</text>
  <text class="t-sm" x="720" y="260">video · examples</text>
  <text class="t-sm" x="720" y="278">agents + DNA</text>
  <rect class="card" x="40" y="200" width="200" height="90" rx="10"/>
  <text class="t" x="60" y="235">Agent harness</text>
  <text class="t-sm" x="60" y="260">.trae / .grok</text>
  <text class="t-sm" x="60" y="278">rules · skills</text>
  <rect class="card" x="280" y="200" width="200" height="90" rx="10"/>
  <text class="t" x="300" y="235">Persistence</text>
  <text class="t-sm" x="300" y="260">Postgres / JSON</text>
  <text class="t-sm" x="300" y="278">audit · memory</text>
  <rect class="card" x="520" y="200" width="160" height="90" rx="10"/>
  <text class="t" x="540" y="235">Tools</text>
  <text class="t-sm" x="540" y="260">adapters</text>
  <text class="t-sm" x="540" y="278">tool_effects</text>
  <path class="arrow" d="M240 105 H275"/>
  <path class="arrow" d="M480 105 H515"/>
  <path class="arrow" d="M380 150 V195"/>
  <path class="arrow" d="M620 150 V195"/>
  <path class="arrow" d="M140 150 V195"/>
  <path class="arrow" d="M700 105 H740 V195"/>
  <text class="t-sm" x="40" y="340">N1: domain logic stays in pack · host executes DNA, tools, gates only</text>
  <text class="t-sm" x="40" y="365">No second control plane · evolution never mutates production DNA directly</text>
  <text class="t-sm" x="40" y="390">Executable bar: E1 path + viral-hook DNA (stubs) · not full live media studio</text>
""",
        "System overview",
    ),
    "03-install-boot.svg": svg_wrap(
        900,
        280,
        """
  <text class="t-title" x="24" y="36">First boot sequence</text>
  <g>
    <circle class="accent" cx="70" cy="120" r="28"/>
    <text class="t" x="62" y="125">1</text>
    <text class="t-sm" x="40" y="175">bootstrap</text>
  </g>
  <path class="arrow" d="M105 120 H145"/>
  <g>
    <circle class="accent" cx="180" cy="120" r="28"/>
    <text class="t" x="172" y="125">2</text>
    <text class="t-sm" x="150" y="175">backend</text>
  </g>
  <path class="arrow" d="M215 120 H255"/>
  <g>
    <circle class="accent" cx="290" cy="120" r="28"/>
    <text class="t" x="282" y="125">3</text>
    <text class="t-sm" x="255" y="175">health/ready</text>
  </g>
  <path class="arrow" d="M325 120 H365"/>
  <g>
    <circle class="accent" cx="400" cy="120" r="28"/>
    <text class="t" x="392" y="125">4</text>
    <text class="t-sm" x="370" y="175">frontend</text>
  </g>
  <path class="arrow" d="M435 120 H475"/>
  <g>
    <circle class="accent" cx="510" cy="120" r="28"/>
    <text class="t" x="502" y="125">5</text>
    <text class="t-sm" x="480" y="175">login</text>
  </g>
  <path class="arrow" d="M545 120 H585"/>
  <g>
    <circle class="ok" cx="620" cy="120" r="28"/>
    <text class="t" x="612" y="125">6</text>
    <text class="t-sm" x="590" y="175">E1 path</text>
  </g>
  <rect class="card" x="700" y="70" width="170" height="140" rx="10"/>
  <text class="t" x="720" y="100">Credentials</text>
  <text class="t-sm" x="720" y="125">admin@example.com</text>
  <text class="t-sm" x="720" y="145">admin-password</text>
  <text class="t-sm" x="720" y="175">API :8000</text>
  <text class="t-sm" x="720" y="195">UI :3000</text>
""",
        "Install boot",
    ),
    "04-console-map.svg": svg_wrap(
        920,
        380,
        """
  <text class="t-title" x="24" y="36">Ops console map</text>
  <rect class="card" x="20" y="55" width="160" height="300" rx="10"/>
  <text class="t" x="40" y="85">Sidebar</text>
  <text class="t-sm" x="40" y="115">Dashboard</text>
  <text class="t-sm" x="40" y="135">Agents</text>
  <text class="t" x="40" y="160" fill="#3d7eff">Domains</text>
  <text class="t-sm" x="40" y="185">Tools</text>
  <text class="t-sm" x="40" y="205">Workflows</text>
  <text class="t-sm" x="40" y="225">Approvals</text>
  <text class="t-sm" x="40" y="250">Knowledge</text>
  <text class="t-sm" x="40" y="270">Memory</text>
  <text class="t-sm" x="40" y="290">Evaluations</text>
  <text class="t-sm" x="40" y="310">Processes</text>
  <text class="t-sm" x="40" y="330">Evolution</text>
  <rect class="card-hi" x="200" y="55" width="680" height="300" rx="10"/>
  <text class="t" x="220" y="90">Main content · /app/domains example</text>
  <rect class="card" x="230" y="110" width="280" height="100" rx="8"/>
  <text class="t-sm" x="250" y="140">Recommend workflow</text>
  <text class="t-sm" x="250" y="160">brief to ranked DNA</text>
  <text class="t-sm" x="250" y="180">confidence + alts</text>
  <rect class="card" x="530" y="110" width="280" height="100" rx="8"/>
  <text class="t-sm" x="550" y="140">Special skills</text>
  <text class="t-sm" x="550" y="160">17 pack integrations</text>
  <text class="t-sm" x="550" y="180">status + scores</text>
  <rect class="card" x="230" y="230" width="580" height="90" rx="8"/>
  <text class="t-sm" x="250" y="265">Domain pack roster · N3 agents · not live media studio</text>
  <text class="t-sm" x="250" y="290">Real APIs when NEXT_PUBLIC_DEMO_MODE is not true</text>
""",
        "Console map",
    ),
    "05-e1-operator-path.svg": svg_wrap(
        940,
        240,
        """
  <text class="t-title" x="24" y="36">E1 operator path (flagship)</text>
  <rect class="card" x="20" y="70" width="100" height="70" rx="8"/><text class="t-sm" x="45" y="110">Login</text>
  <path class="arrow" d="M125 105 H150"/>
  <rect class="card" x="150" y="70" width="100" height="70" rx="8"/><text class="t-sm" x="165" y="110">List WFs</text>
  <path class="arrow" d="M255 105 H280"/>
  <rect class="card" x="280" y="70" width="100" height="70" rx="8"/><text class="t-sm" x="300" y="110">Create</text>
  <path class="arrow" d="M385 105 H410"/>
  <rect class="card-hi" x="410" y="70" width="110" height="70" rx="8"/><text class="t-sm" x="430" y="100">Run now</text><text class="t-sm" x="430" y="120">onboarding</text>
  <path class="arrow" d="M525 105 H550"/>
  <rect class="card" x="550" y="70" width="100" height="70" rx="8"/><text class="t-sm" x="565" y="100">Approve</text><text class="t-sm" x="565" y="120">billing</text>
  <path class="arrow" d="M655 105 H680"/>
  <rect class="card" x="680" y="70" width="100" height="70" rx="8"/><text class="t-sm" x="700" y="110">Done</text>
  <path class="arrow" d="M785 105 H810"/>
  <rect class="card" x="810" y="70" width="100" height="70" rx="8"/><text class="t-sm" x="825" y="100">Improve</text><text class="t-sm" x="825" y="120">reflect</text>
  <text class="t-sm" x="20" y="180">Workflow: wf_customer_onboarding_v12 · case_id required · human gate on billing</text>
  <text class="t-sm" x="20" y="205">Proof: backend/app/tests/e2e/test_e1_operator_path.py</text>
""",
        "E1 path",
    ),
    "06-governance-gates.svg": svg_wrap(
        880,
        300,
        """
  <text class="t-title" x="24" y="36">Risk tiers and human gates</text>
  <rect class="card" x="30" y="70" width="180" height="100" rx="10"/>
  <text class="t" x="50" y="105">R0–R1</text>
  <text class="t-sm" x="50" y="130">Read / draft</text>
  <text class="t-sm" x="50" y="150">Auto allowed</text>
  <rect class="card" x="240" y="70" width="180" height="100" rx="10"/>
  <text class="t" x="260" y="105">R2</text>
  <text class="t-sm" x="260" y="130">Reversible write</text>
  <text class="t-sm" x="260" y="150">Soft gate / log</text>
  <rect class="card-hi" x="450" y="70" width="180" height="100" rx="10"/>
  <text class="t" x="470" y="105">R3–R4</text>
  <text class="t-sm" x="470" y="130">Irreversible</text>
  <text class="t-sm" x="470" y="150">Human approve</text>
  <rect class="card" x="660" y="70" width="180" height="100" rx="10"/>
  <text class="t" x="680" y="105">Audit</text>
  <text class="t-sm" x="680" y="130">Every decision</text>
  <text class="t-sm" x="680" y="150">tool_effects</text>
  <text class="t-sm" x="30" y="220">UI: Approvals queue · decision panel · request_id on errors</text>
  <text class="t-sm" x="30" y="245">Policy: business/governance/* · rules/60-human-approval.md</text>
""",
        "Governance",
    ),
    "07-agents-tools.svg": svg_wrap(
        900,
        280,
        """
  <text class="t-title" x="24" y="36">Agents, tools, allow-lists</text>
  <rect class="card" x="40" y="70" width="220" height="140" rx="10"/>
  <text class="t" x="60" y="105">Agent</text>
  <text class="t-sm" x="60" y="130">id · role · status</text>
  <text class="t-sm" x="60" y="150">allowed_tools[]</text>
  <text class="t-sm" x="60" y="170">ALC lessons</text>
  <rect class="card-hi" x="320" y="70" width="220" height="140" rx="10"/>
  <text class="t" x="340" y="105">DNA step</text>
  <text class="t-sm" x="340" y="130">agent + tools</text>
  <text class="t-sm" x="340" y="150">action_type</text>
  <text class="t-sm" x="340" y="170">memory r/w</text>
  <rect class="card" x="600" y="70" width="240" height="140" rx="10"/>
  <text class="t" x="620" y="105">Tool adapter</text>
  <text class="t-sm" x="620" y="130">crm · email · video_*</text>
  <text class="t-sm" x="620" y="150">tool_effects audit</text>
  <text class="t-sm" x="620" y="170">stub vs live</text>
  <path class="arrow" d="M265 140 H315"/>
  <path class="arrow" d="M545 140 H595"/>
""",
        "Agents tools",
    ),
    "08-domain-recommend.svg": svg_wrap(
        900,
        300,
        """
  <text class="t-title" x="24" y="36">Video brief to workflow DNA recommend</text>
  <rect class="card" x="40" y="70" width="200" height="120" rx="10"/>
  <text class="t" x="60" y="110">Operator brief</text>
  <text class="t-sm" x="60" y="140">15s viral TikTok</text>
  <text class="t-sm" x="60" y="160">duration_sec</text>
  <path class="arrow" d="M250 130 H300"/>
  <rect class="card-hi" x="300" y="70" width="240" height="120" rx="10"/>
  <text class="t" x="320" y="105">Selector</text>
  <text class="t-sm" x="320" y="130">archetype_selector</text>
  <text class="t-sm" x="320" y="150">A–J registry</text>
  <path class="arrow" d="M550 130 H600"/>
  <rect class="card" x="600" y="70" width="250" height="120" rx="10"/>
  <text class="t" x="620" y="105">Recommendation</text>
  <text class="t-sm" x="620" y="130">dna_id · scale S1–S5</text>
  <text class="t-sm" x="620" y="150">confidence · alts</text>
  <text class="t-sm" x="40" y="230">API: POST /api/v1/domains/video/recommend-workflow</text>
  <text class="t-sm" x="40" y="255">Example: wf_video_arch_a_viral_hook_v1 (code A)</text>
""",
        "Domain recommend",
    ),
    "09-special-skills.svg": svg_wrap(
        880,
        260,
        """
  <text class="t-title" x="24" y="36">Special skills catalog (video pack)</text>
  <rect class="card" x="40" y="70" width="240" height="120" rx="10"/>
  <text class="t" x="60" y="105">REGISTRY.json</text>
  <text class="t-sm" x="60" y="130">business/video/special_skills</text>
  <text class="t-sm" x="60" y="150">17 integrations</text>
  <path class="arrow" d="M290 130 H340"/>
  <rect class="card-hi" x="340" y="70" width="220" height="120" rx="10"/>
  <text class="t" x="360" y="105">Host API</text>
  <text class="t-sm" x="360" y="130">GET special-skills</text>
  <text class="t-sm" x="360" y="150">status · scores</text>
  <path class="arrow" d="M570 130 H620"/>
  <rect class="card" x="620" y="70" width="200" height="120" rx="10"/>
  <text class="t" x="640" y="105">Ops UI table</text>
  <text class="t-sm" x="640" y="130">skill_id · kind</text>
  <text class="t-sm" x="640" y="150">mvp_integrated</text>
""",
        "Special skills",
    ),
    "10-workflow-dna.svg": svg_wrap(
        920,
        320,
        """
  <text class="t-title" x="24" y="36">Workflow DNA lifecycle</text>
  <rect class="card" x="30" y="70" width="140" height="80" rx="8"/><text class="t-sm" x="50" y="115">Author DNA</text>
  <path class="arrow" d="M175 110 H205"/>
  <rect class="card" x="205" y="70" width="140" height="80" rx="8"/><text class="t-sm" x="225" y="115">Validate</text>
  <path class="arrow" d="M350 110 H380"/>
  <rect class="card" x="380" y="70" width="140" height="80" rx="8"/><text class="t-sm" x="400" y="115">Sandbox run</text>
  <path class="arrow" d="M525 110 H555"/>
  <rect class="card" x="555" y="70" width="140" height="80" rx="8"/><text class="t-sm" x="575" y="115">Evaluate</text>
  <path class="arrow" d="M700 110 H730"/>
  <rect class="card-hi" x="730" y="70" width="150" height="80" rx="8"/><text class="t-sm" x="750" y="105">Canary /</text><text class="t-sm" x="750" y="125">Promote</text>
  <rect class="card" x="30" y="190" width="850" height="90" rx="10"/>
  <text class="t" x="50" y="225">DNA fields (conceptual)</text>
  <text class="t-sm" x="50" y="250">id · steps · agents · tools · memory · verification · risk_tier · human_gates</text>
""",
        "Workflow DNA",
    ),
    "11-knowledge-memory.svg": svg_wrap(
        900,
        280,
        """
  <text class="t-title" x="24" y="36">Knowledge and memory tiers</text>
  <rect class="card" x="40" y="70" width="250" height="140" rx="10"/>
  <text class="t" x="60" y="105">Tier 0 retrieval</text>
  <text class="t-sm" x="60" y="135">keyword + embeddings</text>
  <text class="t-sm" x="60" y="155">fast, broad</text>
  <rect class="card-hi" x="320" y="70" width="250" height="140" rx="10"/>
  <text class="t" x="340" y="105">Tier 1 retrieval</text>
  <text class="t-sm" x="340" y="135">entity multi-hop</text>
  <text class="t-sm" x="340" y="155">K1-lite graph ops</text>
  <rect class="card" x="600" y="70" width="250" height="140" rx="10"/>
  <text class="t" x="620" y="105">Memory scopes</text>
  <text class="t-sm" x="620" y="135">episodic · semantic</text>
  <text class="t-sm" x="620" y="155">procedural · eval</text>
""",
        "Knowledge memory",
    ),
    "12-pi-evolution.svg": svg_wrap(
        920,
        280,
        """
  <text class="t-title" x="24" y="36">Process intelligence to evolution loop</text>
  <rect class="card" x="30" y="70" width="150" height="90" rx="8"/><text class="t-sm" x="50" y="115">Event logs</text>
  <path class="arrow" d="M185 115 H215"/>
  <rect class="card" x="215" y="70" width="150" height="90" rx="8"/><text class="t-sm" x="235" y="115">Discover</text>
  <path class="arrow" d="M370 115 H400"/>
  <rect class="card" x="400" y="70" width="150" height="90" rx="8"/><text class="t-sm" x="420" y="115">Bottlenecks</text>
  <path class="arrow" d="M555 115 H585"/>
  <rect class="card-hi" x="585" y="70" width="150" height="90" rx="8"/><text class="t-sm" x="605" y="115">Sandbox</text>
  <path class="arrow" d="M740 115 H770"/>
  <rect class="card" x="770" y="70" width="120" height="90" rx="8"/><text class="t-sm" x="795" y="115">Canary</text>
  <text class="t-sm" x="30" y="200">UI: Processes · Evolution archive · Improve pipeline on runs</text>
  <text class="t-sm" x="30" y="225">Never promote without evaluate · rollback path required</text>
""",
        "PI evolution",
    ),
    "13-self-improve.svg": svg_wrap(
        900,
        260,
        """
  <text class="t-title" x="24" y="36">Self-improvement closed loop</text>
  <rect class="card" x="50" y="80" width="130" height="70" rx="8"/><text class="t-sm" x="75" y="120">Run ends</text>
  <path class="arrow" d="M185 115 H215"/>
  <rect class="card" x="215" y="80" width="130" height="70" rx="8"/><text class="t-sm" x="250" y="120">Reflect</text>
  <path class="arrow" d="M350 115 H380"/>
  <rect class="card" x="380" y="80" width="130" height="70" rx="8"/><text class="t-sm" x="415" y="120">Lessons</text>
  <path class="arrow" d="M515 115 H545"/>
  <rect class="card" x="545" y="80" width="130" height="70" rx="8"/><text class="t-sm" x="575" y="120">Propose</text>
  <path class="arrow" d="M680 115 H710"/>
  <rect class="card-hi" x="710" y="80" width="140" height="70" rx="8"/><text class="t-sm" x="740" y="120">Loop DNA</text>
  <text class="t-sm" x="50" y="190">APIs: improvement/reflect · lessons · auto-propose · loops/run</text>
""",
        "Self improve",
    ),
    "14-extend-pack.svg": svg_wrap(
        900,
        280,
        """
  <text class="t-title" x="24" y="36">Extend with a domain pack (expert)</text>
  <rect class="card" x="40" y="70" width="180" height="110" rx="10"/><text class="t" x="60" y="105">1. Manifest</text><text class="t-sm" x="60" y="130">agents + DNA</text>
  <path class="arrow" d="M225 125 H255"/>
  <rect class="card" x="255" y="70" width="180" height="110" rx="10"/><text class="t" x="275" y="105">2. Register</text><text class="t-sm" x="275" y="130">inventory</text>
  <path class="arrow" d="M440 125 H470"/>
  <rect class="card" x="470" y="70" width="180" height="110" rx="10"/><text class="t" x="490" y="105">3. Wire tools</text><text class="t-sm" x="490" y="130">allow-list</text>
  <path class="arrow" d="M655 125 H685"/>
  <rect class="card-hi" x="685" y="70" width="180" height="110" rx="10"/><text class="t" x="705" y="105">4. Prove</text><text class="t-sm" x="705" y="130">golden + E2E</text>
  <text class="t-sm" x="40" y="220">Runbook: docs/add-domain-pack-runbook.md</text>
  <text class="t-sm" x="40" y="245">Keep pack logic in business/domain · do not fork control plane</text>
""",
        "Extend pack",
    ),
    "15-security-production.svg": svg_wrap(
        900,
        280,
        """
  <text class="t-title" x="24" y="36">Security and production checklist</text>
  <rect class="card" x="40" y="70" width="250" height="140" rx="10"/>
  <text class="t" x="60" y="105">Identity</text>
  <text class="t-sm" x="60" y="130">password auth</text>
  <text class="t-sm" x="60" y="150">RBAC roles</text>
  <text class="t-sm" x="60" y="170">API keys scoped</text>
  <rect class="card" x="320" y="70" width="250" height="140" rx="10"/>
  <text class="t" x="340" y="105">Runtime</text>
  <text class="t-sm" x="340" y="130">tool allow-lists</text>
  <text class="t-sm" x="340" y="150">human gates R3+</text>
  <text class="t-sm" x="340" y="170">audit completeness</text>
  <rect class="card-hi" x="600" y="70" width="250" height="140" rx="10"/>
  <text class="t" x="620" y="105">Operate</text>
  <text class="t-sm" x="620" y="130">Postgres primary</text>
  <text class="t-sm" x="620" y="150">health/ready</text>
  <text class="t-sm" x="620" y="170">demoMode off</text>
""",
        "Security production",
    ),
}


def main() -> None:
    for name, content in SVGS.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
    print(f"wrote {len(SVGS)} svgs -> {ASSETS}")


if __name__ == "__main__":
    main()
