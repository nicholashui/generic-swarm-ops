# -*- coding: utf-8 -*-
"""Generate Traditional Chinese (*_hk.md) user guide files under book/user_guide/."""
from __future__ import annotations

from pathlib import Path

BOOK = Path(__file__).resolve().parents[2] / "book" / "user_guide"
CH = BOOK / "chapters"
CH.mkdir(parents=True, exist_ok=True)

# English stem -> (zh title, level, part, time, svg, objectives, outline, labs, sources)
CHAPTERS = [
    {
        "en": "00-how-to-use-this-guide.md",
        "id": "00",
        "title": "如何使用本指南",
        "level": "初學者",
        "part": "前言",
        "time": "15 分鐘",
        "svg": "01-learning-path.svg",
        "objectives": [
            "依目標選擇學習路線（操作員 / 建構者 / SRE）",
            "理解文件地圖：本指南 vs design_phase 設計書 vs structure.md",
            "掌握誠實邊界（可執行 vs 殘留未宣稱）",
        ],
        "outline": [
            "本指南對象（操作員、pack 作者、平台工程師）",
            "多檔結構如何組織（第 I–V 部）",
            "符號：實驗 · API · UI · 注意 · 殘留宣稱",
            "先決條件清單（Node、Python、可選 Postgres、埠口）",
            "與 book/design_phase（架構深讀）及 docs/* 的關係",
            "誠實框：即時媒體、完整 studio、灌水分數 — 不在範圍",
        ],
        "labs": [
            "瀏覽 TOC，標記你的路線（操作員：先 ch01–ch09）",
            "打開 EXECUTABLE_PRODUCT.md，記下 proven vs not-claimed",
        ],
        "sources": [
            "EXECUTABLE_PRODUCT.md",
            "README.md",
            "book/design_phase/book.md（僅設計脈絡）",
        ],
    },
    {
        "en": "01-what-is-this-system.md",
        "id": "01",
        "title": "什麼是 generic-swarm-ops？",
        "level": "初學者",
        "part": "第 I 部 — 基礎",
        "time": "30 分鐘",
        "svg": "02-system-overview.svg",
        "objectives": [
            "用不含行話的一段話說明本系統",
            "說出四個平面：主控台、控制平面、業務 OS、領域包",
            "陳述 N1 規則：領域邏輯在 pack；主機執行 DNA/工具/閘門",
        ],
        "outline": [
            "問題：多智能體工作缺少稽核、閘門或改進迴路",
            "產品名與雙 harness（Trae + Grok）概覽",
            "四平面圖走讀",
            "核心名詞：agent、tool、DNA workflow、run、approval、lesson、domain pack",
            "今日可跑什麼（E1 + viral-hook）vs 設計願景文件",
            "詞彙表入門（連附錄 A）",
        ],
        "labs": [
            "憑記憶畫出四格圖",
            "列出每次執行都會用到的 5 個名詞",
        ],
        "sources": ["docs/architecture.md", "structure.md", "EXECUTABLE_PRODUCT.md"],
    },
    {
        "en": "02-mental-model-and-layers.md",
        "id": "02",
        "title": "心智模型與分層架構",
        "level": "初學者",
        "part": "第 I 部 — 基礎",
        "time": "40 分鐘",
        "svg": "02-system-overview.svg",
        "objectives": [
            "把 repo 資料夾對應到執行層",
            "說明 harness 同步（.trae/.grok）vs 後端 runtime",
            "追蹤請求：UI → API → runtime → tool → audit",
        ],
        "outline": [
            "分層表：starter、business、backend、frontend、generated",
            "Repo 地圖：backend/、frontend/、business/、rules/、scripts/",
            "請求生命週期（操作員點擊 → JSON → DNA 步驟）",
            "持久化：Postgres 主、JSON 快照備援",
            "為何 evolution 不直接就地改 production DNA",
            "常見誤解：第二個 LangGraph 控制平面 — 此處沒有",
        ],
        "labs": [
            "列出根目錄並分層歸類",
            "完整閱讀 docs/architecture.md 一次",
        ],
        "sources": ["docs/architecture.md", "structure.md", "docs/sync.md"],
    },
    {
        "en": "03-install-and-first-boot.md",
        "id": "03",
        "title": "安裝與首次開機",
        "level": "初學者",
        "part": "第 I 部 — 基礎",
        "time": "45–90 分鐘",
        "svg": "03-install-boot.svg",
        "objectives": [
            "完成 bootstrap 並通過 doctor",
            "啟動後端並打通 health/ready",
            "以前端即時 API 啟動（demoMode 關閉）",
        ],
        "outline": [
            "先決條件（OS、Node、Python、pnpm、可選 Docker Postgres）",
            "npm run bootstrap / doctor / sync",
            "後端：pip install -e .、uvicorn、.env 與 DATABASE_URL",
            "JSON 檔模式 vs Postgres（學習時 degraded 何時可接受）",
            "前端：真實產品路徑時 NEXT_PUBLIC_DEMO_MODE 不可為 true",
            "種子帳號 admin@example.com / admin-password",
            "首次開機疑難（埠口、CORS、PYTHONPATH）",
        ],
        "labs": [
            "實驗 A：後端 health/live/ready",
            "實驗 B：前端登入並進入 Dashboard",
            "實驗 C：故意開 demoMode 看 mock，再改回 false",
        ],
        "sources": [
            "docs/installation.md",
            "docs/usage.md",
            "backend/docs/postgres-runbook.md",
            "frontend/README.md",
            "frontend/.env.example",
        ],
    },
    {
        "en": "04-ops-console-tour.md",
        "id": "04",
        "title": "營運主控台導覽",
        "level": "初學者",
        "part": "第 I 部 — 基礎",
        "time": "30 分鐘",
        "svg": "04-console-map.svg",
        "objectives": [
            "走完側欄每一組且無死路",
            "打開 Domains 並認出 recommend 與 special skills 面板",
            "知道稽核日誌與 API 金鑰位置",
        ],
        "outline": [
            "側欄分組：Main、Data、Quality、Security、Admin",
            "路由表：appPaths",
            "Domains 頁面面板",
            "權限閘控項目",
            "命令面板 / 行動版導覽",
            "Demo vs live 的 UI 線索",
        ],
        "labs": [
            "點開 Main 每個項目並記錄空狀態",
            "打開 /app/domains 並找到 recommend-workflow-panel",
        ],
        "sources": [
            "frontend/src/types/navigation.ts",
            "frontend/src/lib/routes/paths.ts",
            "frontend/src/app/app/[...slug]/page.tsx",
        ],
    },
    {
        "en": "05-first-workflow-run-e1.md",
        "id": "05",
        "title": "第一次工作流執行（E1 路徑）",
        "level": "初學者 → 中級",
        "part": "第 II 部 — 操作核心",
        "time": "60 分鐘",
        "svg": "05-e1-operator-path.svg",
        "objectives": [
            "端到端完成 E1 路徑",
            "為旗艦工作流提供必要 payload（case_id）",
            "觀察 run 狀態至完成",
        ],
        "outline": [
            "E1 證明什麼（產品門檻）",
            "旗艦工作流 wf_customer_onboarding_v12",
            "UI 步驟：list → run → approve → complete → improve",
            "對等 API curl 序列",
            "閱讀 run 事件 / console",
            "常見失敗：缺 case_id、角色錯誤、demoMode mock",
            "自動化證明：test_e1_operator_path.py",
        ],
        "labs": [
            "實驗 E1-UI：瀏覽器完成路徑",
            "實驗 E1-API：以 token 登入並執行",
            "實驗 E1-Test：跑 e2e 並讀 assertion 名稱",
        ],
        "sources": [
            "docs/usage.md",
            "reviews/e1_operator_checklist.md",
            "backend/app/tests/e2e/test_e1_operator_path.py",
            "EXECUTABLE_PRODUCT.md",
        ],
    },
    {
        "en": "06-approvals-risk-audit.md",
        "id": "06",
        "title": "核准、風險層級與稽核",
        "level": "中級",
        "part": "第 II 部 — 操作核心",
        "time": "45 分鐘",
        "svg": "06-governance-gates.svg",
        "objectives": [
            "判斷何時需要人工核准",
            "核准/駁回並寫理由，找到稽核軌跡",
            "把 R0–R4 風險層級對到操作行為",
        ],
        "outline": [
            "風險層級與不可逆動作",
            "Approvals 佇列 UX 與決策面板",
            "稽核日誌記錄內容",
            "request_id 用於支援 / 除錯",
            "business/governance/ 產物",
            "規則：60-human-approval、90-governance-risk",
        ],
        "labs": [
            "觸發 billing 閘門並以 reviewer 核准",
            "找到對應稽核日誌",
            "駁回一次並觀察 run 結果",
        ],
        "sources": [
            "docs/governance.md",
            "docs/security.md",
            "business/governance/",
            "rules/60-human-approval.md",
        ],
    },
    {
        "en": "07-agents-tools-rbac.md",
        "id": "07",
        "title": "代理、工具與 RBAC",
        "level": "中級",
        "part": "第 II 部 — 操作核心",
        "time": "45 分鐘",
        "svg": "07-agents-tools.svg",
        "objectives": [
            "建立或檢視含 allowed_tools 的 agent",
            "說明 allow-list 外工具為何失敗",
            "把角色對到主要畫面權限",
        ],
        "outline": [
            "Agent 欄位與狀態",
            "工具適配器目錄（ops + video stub）",
            "Runtime allow-list 強制",
            "RBAC 權限型別",
            "API 金鑰 vs 使用者工作階段",
            "ALC / lessons 預覽（見 ch14）",
        ],
        "labs": [
            "以 UI 表單建立 agent（live 模式）",
            "嘗試 allow-list 外工具（預期可控失敗）",
            "比較 admin 與 operator 可見導覽",
        ],
        "sources": [
            "docs/agents.md",
            "frontend/src/types/permissions.ts",
            "backend/app/infrastructure/tools/",
        ],
    },
    {
        "en": "08-domain-packs-and-recommend.md",
        "id": "08",
        "title": "領域包與工作流推薦",
        "level": "中級",
        "part": "第 III 部 — 領域與 video pack",
        "time": "60 分鐘",
        "svg": "08-domain-recommend.svg",
        "objectives": [
            "說明 domain pack 是什麼、video pack 在哪",
            "提交自由文字 brief 並讀取排序後 DNA 推薦",
            "區分「選擇輔助」與「即時媒體生成」",
        ],
        "outline": [
            "Pack 解剖：manifest、agents、DNA、corpus",
            "Video pack 盤點（114 agents、A–J 原型）",
            "Recommend API + UI 面板",
            "Scale S1–S5 與 confidence 解讀",
            "啟動前 hitl_confirm_required",
            "推薦後可選跑 viral-hook DNA",
            "殘留：production_ready、未宣稱 live Sora/Veo",
        ],
        "labs": [
            "UI：Domains → brief「15s viral TikTok hook」→ 斷言 DNA A 類",
            "CLI：scripts/business/recommend_video_workflow.py",
            "API：POST recommend-workflow（需認證）",
        ],
        "sources": [
            "docs/domain-packs.md",
            "docs/add-domain-pack-runbook.md",
            "business/video/",
            "backend/app/domain/workflows/archetype_selector.py",
            "EXECUTABLE_PRODUCT.md",
        ],
    },
    {
        "en": "09-special-skills-catalog.md",
        "id": "09",
        "title": "特殊技能目錄",
        "level": "中級",
        "part": "第 III 部 — 領域與 video pack",
        "time": "40 分鐘",
        "svg": "09-special-skills.svg",
        "objectives": [
            "從真實 REGISTRY 列出 17 個 special skills（非 demo 列）",
            "讀取 API/UI 的 status/score 欄位",
            "在磁碟找到 integration.json + SKILL.md",
        ],
        "outline": [
            "為何需要 special skills（主機 MVP 綁定 pack 能力）",
            "REGISTRY.json 與 skill_count=17",
            "API GET /domains/video/special-skills",
            "UI SpecialSkillsPanel（demo 關閉）",
            "評分誠實性（嚴格分 vs 灌水 100）",
            "mvp_integrated vs 生產 canary",
        ],
        "labs": [
            "打開 Domains 技能表；列數 = 17",
            "選一個 skill_id；打開 business/video/special_skills/<id>/",
            "以 token 呼叫 GET special-skills 比對 ids",
        ],
        "sources": [
            "business/video/special_skills/REGISTRY.json",
            "special_skill_impl_score.md",
            "backend/app/runtime.py list_video_special_skills",
        ],
    },
    {
        "en": "10-workflow-dna-deep-dive.md",
        "id": "10",
        "title": "工作流 DNA 深入",
        "level": "中級 → 進階",
        "part": "第 III 部 — 領域與 video pack",
        "time": "60 分鐘",
        "svg": "10-workflow-dna.svg",
        "objectives": [
            "讀懂 .dna.json 主要欄位",
            "描述 sandbox → evaluate → canary → promote",
            "定位 viral-hook 與 onboarding DNA",
        ],
        "outline": [
            "DNA 是可執行流程圖（非自由聊天）",
            "步驟結構：agent、tools、action_type、memory、verification",
            "人工閘門與風險中繼資料",
            "版本與 promote 規則",
            "驗證命令 business:validate / evolution checks",
            "上線前作者檢查清單",
        ],
        "labs": [
            "比對兩份 DNA（onboarding vs viral-hook）",
            "執行可用的 DNA 驗證測試",
            "在紙上草擬 3 步玩具 DNA",
        ],
        "sources": [
            "docs/workflow-dna.md",
            "rules/100-evolution-sandbox.md",
            "business/video/workflows/",
        ],
    },
    {
        "en": "11-knowledge-and-memory.md",
        "id": "11",
        "title": "知識與記憶",
        "level": "進階",
        "part": "第 IV 部 — 智能與改進",
        "time": "50 分鐘",
        "svg": "11-knowledge-memory.svg",
        "objectives": [
            "為查詢選擇 Tier 0 或 Tier 1 檢索",
            "在 UI 瀏覽 knowledge 與 memory",
            "說明 provenance 與保留策略",
        ],
        "outline": [
            "分層檢索政策",
            "K1-lite 圖運算子與 federation 匯出",
            "記憶範圍：episodic、semantic、procedural、evaluation",
            "UI /app/knowledge 與 /app/memory",
            "API knowledge search / graph / federate",
            "Provenance 與 retention 連結",
        ],
        "labs": [
            "從 UI 或 API 執行 knowledge 搜尋",
            "檢視 business/knowledge-base 結構",
            "閱讀 retrieval-tier-policy.md",
        ],
        "sources": [
            "docs/knowledge-memory.md",
            "business/knowledge-base/",
            "docs/self-improvement-and-orchestration.md",
        ],
    },
    {
        "en": "12-process-intelligence.md",
        "id": "12",
        "title": "流程智能（Process intelligence）",
        "level": "進階",
        "part": "第 IV 部 — 智能與改進",
        "time": "45 分鐘",
        "svg": "12-pi-evolution.svg",
        "objectives": [
            "檢視 PI 產物",
            "閱讀 discovered / conformance / bottlenecks",
            "把瓶頸連到改進假說",
        ],
        "outline": [
            "為何需要 PI（挖掘真實流程）",
            "business/process-intelligence/ 產物位置",
            "UI Processes",
            "/processes API",
            "從瓶頸到 sandbox 變體提案",
        ],
        "labs": [
            "打開 Processes 頁",
            "檢視一份 PI JSON",
            "為瓶頸寫一條因果假說",
        ],
        "sources": [
            "docs/process-intelligence.md",
            "business/process-intelligence/",
            "rules/80-process-intelligence.md",
        ],
    },
    {
        "en": "13-evaluation-and-evolution.md",
        "id": "13",
        "title": "評測與演化沙箱",
        "level": "進階",
        "part": "第 IV 部 — 智能與改進",
        "time": "60 分鐘",
        "svg": "12-pi-evolution.svg",
        "objectives": [
            "解讀 golden/regression/adversarial 評測",
            "使用 Evolution 檔案庫 UI",
            "陳述 promote 規則與回滾期望",
        ],
        "outline": [
            "business/evals/ 語料配置",
            "Fitness 與 archive",
            "UI /app/evolution",
            "Canary 與版本化 DNA",
            "npm run business:eval 與 evolution:check",
            "禁止：就地改 production DNA",
        ],
        "labs": [
            "打開 Evolution archive",
            "列出 golden tasks 數量（產品門檻 ≥20）",
            "追蹤一份 successful variant JSON（若有）",
        ],
        "sources": [
            "docs/evaluation.md",
            "docs/evolution-sandbox.md",
            "business/evals/",
            "business/evolution/",
        ],
    },
    {
        "en": "14-self-improvement-loops.md",
        "id": "14",
        "title": "自我改進與迴路",
        "level": "進階",
        "part": "第 IV 部 — 智能與改進",
        "time": "50 分鐘",
        "svg": "13-self-improve.svg",
        "objectives": [
            "在完成的 run 上跑 Improve 管線步驟",
            "找到 lessons-learned 產物",
            "說明 loop DNA 的 stop/continue 條件",
        ],
        "outline": [
            "閉環：observe → verify → iterate",
            "UI Improve：Reflect → Propose → Evaluate → Canary",
            "API improvement/* 與 loops/*",
            "Lesson 庫品質控制",
            "自動提案 sandbox 變體",
            "與自演化文獻對照（docs 對映）",
        ],
        "labs": [
            "在完成的 E1 run 執行 Reflect",
            "GET improvement/lessons",
            "讀取 business/evolution/lessons-learned/ 一份 lesson",
        ],
        "sources": [
            "docs/self-improvement-and-orchestration.md",
            "docs/usage.md",
            "backend/app/infrastructure/self_improvement/",
        ],
    },
    {
        "en": "15-backend-runtime-and-apis.md",
        "id": "15",
        "title": "後端 Runtime 與 API",
        "level": "專家",
        "part": "第 V 部 — 專家與生產",
        "time": "75 分鐘",
        "svg": "02-system-overview.svg",
        "objectives": [
            "定位 runtime 進入點與路由模組",
            "認證並呼叫核心 API，注意 request_id",
            "說明 store 後端（Postgres vs JSON）",
        ],
        "outline": [
            "app.main 與 middleware",
            "RuntimeServices 職責",
            "路由圖：auth、workflows、runs、approvals、domains、improvement…",
            "OpenAPI 匯出",
            "測試金字塔：unit vs e2e",
            "閱讀 tool_effects 與 runtime.json 快照",
        ],
        "labs": [
            "在 OpenAPI 找到 recommend-workflow",
            "在 runtime.py 追蹤 recommend_video_workflow",
            "跑 special skills + archetype 單元測試",
        ],
        "sources": [
            "backend/README.md",
            "book/design_phase/book.backend_hk.md",
            "backend/app/api/v1/routes/",
            "backend/app/runtime.py",
        ],
    },
    {
        "en": "16-frontend-deep-dive.md",
        "id": "16",
        "title": "前端深入",
        "level": "專家",
        "part": "第 V 部 — 專家與生產",
        "time": "60 分鐘",
        "svg": "04-console-map.svg",
        "objectives": [
            "說明 client 認證 cookie 與 live-data facade",
            "安全地將新面板接到 backendApi",
            "保持 demoMode 僅 opt-in",
        ],
        "outline": [
            "App shell、側欄、slug 路由器",
            "backendApi 模式",
            "product-data demo vs live",
            "表單：Zod + RHF + formatMutationError",
            "Improve 與 evolution 面板",
            "Vitest + Playwright smoke",
            "以 Domains 風格加功能而不分叉架構",
        ],
        "labs": [
            "閱讀 client.ts recommend + special skills 方法",
            "跑 frontend product-slice 單元測試",
            "追蹤 env.ts 的 demoMode 預設",
        ],
        "sources": [
            "frontend/README.md",
            "frontend/src/lib/api/client.ts",
            "frontend/src/lib/config/env.ts",
            "frontend/docs/api/frontend-api-contract.md",
        ],
    },
    {
        "en": "17-extend-dna-agents-packs.md",
        "id": "17",
        "title": "擴充 DNA、代理與領域包",
        "level": "專家",
        "part": "第 V 部 — 專家與生產",
        "time": "90 分鐘",
        "svg": "14-extend-pack.svg",
        "objectives": [
            "搭建最小 domain pack 或 DNA 擴充",
            "正確註冊工具與 agent allow-list",
            "以 golden task + inventory 證明",
        ],
        "outline": [
            "何時擴 pack vs host",
            "Manifest 與版本矩陣",
            "Agent JSON + DNA 撰寫步驟",
            "Tool adapter stub 模式",
            "inventory_check 與 corpus standalone",
            "反模式：第二控制平面、灌水分數",
        ],
        "labs": [
            "研讀 example_education 或 example_research pack",
            "草擬你的 pack 一頁設計",
            "對 video pack 跑 inventory_check 作參考",
        ],
        "sources": [
            "docs/add-domain-pack-runbook.md",
            "docs/domain-pack-versioning-matrix.md",
            "business/example_education/",
            "scripts/business/",
        ],
    },
    {
        "en": "18-security-ops-troubleshooting.md",
        "id": "18",
        "title": "安全、營運與疑難排解",
        "level": "專家",
        "part": "第 V 部 — 專家與生產",
        "time": "60 分鐘",
        "svg": "15-security-production.svg",
        "objectives": [
            "套用生產就緒檢查清單",
            "診斷常見開機與執行失敗",
            "套用 agentic 安全基本（工具濫用、提示注入意識）",
        ],
        "outline": [
            "種子密碼以外的認證強化",
            "Secrets、CORS、安全標頭",
            "Postgres runbook 要點",
            "Doctor / security 腳本",
            "疑難矩陣（症狀 → 檢查）",
            "事件：核准繞過嘗試",
        ],
        "labs": [
            "跑 npm run doctor 並記錄輸出",
            "用錯誤 DATABASE_URL 弄壞 ready 再恢復",
            "精讀 rules/110-agentic-security.md 重點",
        ],
        "sources": [
            "docs/security.md",
            "docs/troubleshooting.md",
            "backend/docs/postgres-runbook.md",
            "rules/30-security.md",
            "rules/110-agentic-security.md",
        ],
    },
    {
        "en": "19-expert-playbooks-and-checklists.md",
        "id": "19",
        "title": "專家劇本與檢查清單",
        "level": "專家",
        "part": "第 V 部 — 專家與生產",
        "time": "40 分鐘+",
        "svg": "01-learning-path.svg",
        "objectives": [
            "使用角色導向日/週檢查清單",
            "知道 design_phase 書何時當深讀參考",
            "定義個人精通標準",
        ],
        "outline": [
            "操作員每日清單",
            "Pack 作者發布清單",
            "平台 SRE 每週清單",
            "精通量尺（能教 E1、recommend、promote 規則）",
            "下一步：structure.md、design_phase、gap 分析",
            "附錄指標（詞彙、API 速查、命令速查）",
        ],
        "labs": [
            "完成精通自評（每列 1–5）",
            "為組織最重要工作流寫一份劇本",
        ],
        "sources": [
            "reviews/e1_operator_checklist.md",
            "mark_100_verification.md",
            "book/design_phase/",
            "book/user_guide/TOC_hk.md",
        ],
    },
    {
        "en": "A-glossary.md",
        "id": "A",
        "title": "附錄 A — 詞彙表",
        "level": "參考",
        "part": "附錄",
        "time": "參考",
        "svg": None,
        "objectives": ["查詢本指南使用的任何術語"],
        "outline": [
            "Agent、ALC、approval、archetype、audit、bootstrap",
            "Canary、conformance、DNA、domain pack、demoMode",
            "E1、evolution、federation、fitness、gate",
            "Harness、inventory、K1-lite、lesson、loop DNA",
            "Memory scopes、N1、PI、provenance、RBAC",
            "Runtime、special skill、tool_effects、viral-hook",
        ],
        "labs": [],
        "sources": ["本指南 + docs/*"],
    },
    {
        "en": "B-command-and-api-cheatsheet.md",
        "id": "B",
        "title": "附錄 B — 命令與 API 速查",
        "level": "參考",
        "part": "附錄",
        "time": "參考",
        "svg": None,
        "objectives": ["複製 bootstrap、執行、評測與關鍵 API 呼叫"],
        "outline": [
            "npm scripts 表",
            "後端 uvicorn 與 pytest",
            "前端 pnpm",
            "Auth login curl",
            "Recommend + special-skills curl",
            "Improvement API",
        ],
        "labs": [],
        "sources": ["docs/usage.md", "package.json", "frontend/.env.example"],
    },
    {
        "en": "C-troubleshooting-matrix.md",
        "id": "C",
        "title": "附錄 C — 疑難排解矩陣",
        "level": "參考",
        "part": "附錄",
        "time": "參考",
        "svg": None,
        "objectives": ["由症狀跳到修復"],
        "outline": [
            "後端無法啟動",
            "ready degraded",
            "登入失敗",
            "UI 顯示 demo mock",
            "側欄缺少 Domains",
            "Recommend 空白 / mock",
            "Approval 卡住",
            "Inventory check 失敗",
        ],
        "labs": [],
        "sources": ["docs/troubleshooting.md", "ch03、ch05、ch08"],
    },
]


def hk_name(en_name: str) -> str:
    if en_name.endswith(".md"):
        return en_name[:-3] + "_hk.md"
    return en_name + "_hk"


def chapter_md(c: dict) -> str:
    en = c["en"]
    hk = hk_name(en)
    svg_block = ""
    if c["svg"]:
        svg_block = (
            f"\n## 插圖\n\n"
            f"![{c['title']}](../assets/{c['svg']})\n\n"
            f"*圖：{c['title']} — 來源 `assets/{c['svg']}`*\n"
        )
    objectives = "\n".join(f"- {o}" for o in c["objectives"])
    outline = "\n".join(f"{i}. {s}" for i, s in enumerate(c["outline"], 1))
    labs = (
        "\n".join(f"- [ ] {lab}" for lab in c["labs"])
        if c["labs"]
        else "_無實驗（參考附錄）。_"
    )
    sources = "\n".join(f"- `{s}`" for s in c["sources"])
    return f"""# 第 {c['id']} 章：{c['title']}

> **語言：** 繁體中文（`_hk`）  
> **狀態：** 骨架於 `book/user_guide/` — 請在此擴寫完整內文  
> **程度：** {c['level']}  
> **部：** {c['part']}  
> **預估時間：** {c['time']}  
> **路徑：** `book/user_guide/chapters/{hk}`  
> **英文對照：** [`{en}`](./{en})

{svg_block}

## 學習目標

{objectives}

## 敘事大綱（擴寫為完整正文）

{outline}

## 實作實驗

{labs}

## 主要來源（未驗證前勿臆造）

{sources}

## 撰寫檢查清單（完整稿）

- [ ] 開場一段說明「為何重要」
- [ ] 步驟指令以 Windows PowerShell 為主，必要時附 bash
- [ ] 每個主要實驗含「預期結果」
- [ ] 相關處標明殘留／未宣稱
- [ ] 交叉連結上一章／下一章（`*_hk.md`）
- [ ] SVG 使用 `../assets/`（與英文版共用圖檔）
- [ ] 術語與英文版一致；產品識別碼（dna_id、API 路徑）不翻譯

## 導覽

- 目錄：[../TOC_hk.md](../TOC_hk.md)
- 主檔：[../user_guide_hk.md](../user_guide_hk.md)
- 英文主檔：[../user_guide.md](../user_guide.md)
- 計畫：[../../../planning/user_guide/00_PLAN.md](../../../planning/user_guide/00_PLAN.md)
"""


def write_user_guide_hk() -> None:
    lines = [
        "# Generic Swarm Ops — 使用者指南（繁體中文）",
        "",
        "**初學者 → 專家。** 逐步深入理解並操作本系統。",
        "",
        "| | |",
        "|--|--|",
        "| **位置** | `book/user_guide/`（權威目錄） |",
        "| **章節** | [`chapters/*_hk.md`](./chapters/) |",
        "| **插圖** | [`assets/`](./assets/)（中英共用） |",
        "| **完整目錄** | [`TOC_hk.md`](./TOC_hk.md) |",
        "| **英文版** | [`user_guide.md`](./user_guide.md) |",
        "| **撰寫計畫** | [`../../planning/user_guide/00_PLAN.md`](../../planning/user_guide/00_PLAN.md) |",
        "| **設計專書** | [`../design_phase/`](../design_phase/) |",
        "",
        "> **範圍誠實聲明：** 已驗證路徑包含 E1 操作員流程，以及 video pack 的 recommend／viral-hook DNA（stub）。"
        "即時媒體供應商與完整 studio **不在宣稱範圍** — 見 `EXECUTABLE_PRODUCT.md`。",
        "",
        "---",
        "",
        "## 語言與命名慣例",
        "",
        "| 英文 | 繁中 |",
        "|------|------|",
        "| `*.md` | `*_hk.md` |",
        "| `user_guide.md` | `user_guide_hk.md` |",
        "| `TOC.md` | `TOC_hk.md` |",
        "| `chapters/00-….md` | `chapters/00-…_hk.md` |",
        "",
        "產品識別碼、API 路徑、檔名、`dna_id` **維持英文**，僅敘事與標題翻譯。",
        "",
        "---",
        "",
        "## 學習路徑",
        "",
        "![初學者到專家學習路徑](./assets/01-learning-path.svg)",
        "",
        "| 路線 | 由此開始 |",
        "|------|----------|",
        "| **操作員** | [00](./chapters/00-how-to-use-this-guide_hk.md) → 第 I–III 部 |",
        "| **建構者** | 操作員路徑 + [10 DNA](./chapters/10-workflow-dna-deep-dive_hk.md) + [17 擴充](./chapters/17-extend-dna-agents-packs_hk.md) |",
        "| **平台 / SRE** | 第 I–II 部 + [15 後端](./chapters/15-backend-runtime-and-apis_hk.md)–[18 安全](./chapters/18-security-ops-troubleshooting_hk.md) |",
        "| **專家** | 全部章節 + 附錄 |",
        "",
        "---",
        "",
        "## 前言",
        "",
        "- [00 — 如何使用本指南](./chapters/00-how-to-use-this-guide_hk.md)",
        "",
        "## 第 I 部 — 基礎（初學者）",
        "",
        "- [01 — 什麼是 generic-swarm-ops？](./chapters/01-what-is-this-system_hk.md)",
        "- [02 — 心智模型與分層架構](./chapters/02-mental-model-and-layers_hk.md)",
        "- [03 — 安裝與首次開機](./chapters/03-install-and-first-boot_hk.md)",
        "- [04 — 營運主控台導覽](./chapters/04-ops-console-tour_hk.md)",
        "",
        "## 第 II 部 — 操作核心",
        "",
        "- [05 — 第一次工作流執行（E1 路徑）](./chapters/05-first-workflow-run-e1_hk.md)",
        "- [06 — 核准、風險層級與稽核](./chapters/06-approvals-risk-audit_hk.md)",
        "- [07 — 代理、工具與 RBAC](./chapters/07-agents-tools-rbac_hk.md)",
        "",
        "## 第 III 部 — 領域與 video pack",
        "",
        "- [08 — 領域包與工作流推薦](./chapters/08-domain-packs-and-recommend_hk.md)",
        "- [09 — 特殊技能目錄](./chapters/09-special-skills-catalog_hk.md)",
        "- [10 — 工作流 DNA 深入](./chapters/10-workflow-dna-deep-dive_hk.md)",
        "",
        "## 第 IV 部 — 智能與改進",
        "",
        "- [11 — 知識與記憶](./chapters/11-knowledge-and-memory_hk.md)",
        "- [12 — 流程智能](./chapters/12-process-intelligence_hk.md)",
        "- [13 — 評測與演化沙箱](./chapters/13-evaluation-and-evolution_hk.md)",
        "- [14 — 自我改進與迴路](./chapters/14-self-improvement-loops_hk.md)",
        "",
        "## 第 V 部 — 專家與生產",
        "",
        "- [15 — 後端 Runtime 與 API](./chapters/15-backend-runtime-and-apis_hk.md)",
        "- [16 — 前端深入](./chapters/16-frontend-deep-dive_hk.md)",
        "- [17 — 擴充 DNA、代理與領域包](./chapters/17-extend-dna-agents-packs_hk.md)",
        "- [18 — 安全、營運與疑難排解](./chapters/18-security-ops-troubleshooting_hk.md)",
        "- [19 — 專家劇本與檢查清單](./chapters/19-expert-playbooks-and-checklists_hk.md)",
        "",
        "## 附錄",
        "",
        "- [A — 詞彙表](./chapters/A-glossary_hk.md)",
        "- [B — 命令與 API 速查](./chapters/B-command-and-api-cheatsheet_hk.md)",
        "- [C — 疑難排解矩陣](./chapters/C-troubleshooting-matrix_hk.md)",
        "",
        "---",
        "",
        "## 系統一覽",
        "",
        "![系統總覽](./assets/02-system-overview.svg)",
        "",
        "---",
        "",
        "## 維護方式",
        "",
        "1. **權威使用者指南** = `book/user_guide/`。",
        "2. 每個英文 `*.md` 必須有對應繁中 `*_hk.md`。",
        "3. 擴寫正文時中英同步更新；識別碼不翻譯。",
        "4. 插圖共用 `assets/`（不複製成 `_hk.svg`）。",
        "",
    ]
    (BOOK / "user_guide_hk.md").write_text("\n".join(lines), encoding="utf-8")


def write_toc_hk() -> None:
    rows = []
    for c in CHAPTERS:
        if c["id"] in ("A", "B", "C"):
            continue
        hk = hk_name(c["en"])
        svg = c["svg"] or "—"
        rows.append(
            f"| {c['id']} | {c['title']} | [chapters/{hk}](./chapters/{hk}) | {c['level']} | {svg} | {c['time']} |"
        )
    app_rows = []
    for c in CHAPTERS:
        if c["id"] not in ("A", "B", "C"):
            continue
        hk = hk_name(c["en"])
        app_rows.append(f"| {c['id']} | {c['title']} | [chapters/{hk}](./chapters/{hk}) |")

    text = f"""# 使用者指南 — 完整目錄（繁體中文）

**產品：** generic-swarm-ops  
**權威目錄：** `book/user_guide/`  
**主檔：** [`user_guide_hk.md`](./user_guide_hk.md)  
**英文目錄：** [`TOC.md`](./TOC.md)  
**章節：** `chapters/*_hk.md`  
**插圖：** [`assets/`](./assets/)（中英共用）

---

## 閱讀地圖

![初學者到專家學習路徑](./assets/01-learning-path.svg)

| 路線 | 建議路徑 |
|------|----------|
| 操作員 | 前言 → 第 I–III 部（至 special skills） |
| 建構者 | 操作員 + DNA + 擴充 |
| 平台 / SRE | 第 I–II 部 + 第 V 部（15–18）+ 附錄 B–C |
| 專家 | 全書 + 附錄 |

---

## 命名慣例

| 英文檔 | 繁中檔 |
|--------|--------|
| `foo.md` | `foo_hk.md` |
| `user_guide.md` | `user_guide_hk.md` |

---

## 章節一覽

| 章 | 標題 | 檔案 | 程度 | SVG | 時間 |
|----|------|------|------|-----|------|
{chr(10).join(rows)}

---

## 附錄

| ID | 標題 | 檔案 |
|----|------|------|
{chr(10).join(app_rows)}

---

## 章節數

- 敘事章：**20**（00–19）× 中英  
- 附錄：**3**（A–C）× 中英  
- SVG：**15**（共用）
"""
    (BOOK / "TOC_hk.md").write_text(text, encoding="utf-8")


def write_readme_hk() -> None:
    text = """# 使用者指南（繁體中文）

**權威位置：** `book/user_guide/`

| 檔案 / 資料夾 | 用途 |
|---------------|------|
| **[user_guide_hk.md](./user_guide_hk.md)** | 繁中主入口 |
| **[TOC_hk.md](./TOC_hk.md)** | 繁中目錄 |
| **[chapters/*_hk.md](./chapters/)** | 各章繁中 |
| **[assets/](./assets/)** | SVG 插圖（中英共用） |
| [user_guide.md](./user_guide.md) | 英文主入口 |

## 開始閱讀

開啟 **[user_guide_hk.md](./user_guide_hk.md)**。

## 翻譯慣例

- 每個英文 `*.md` → 對應 `*_hk.md`（繁體中文）
- API 路徑、`dna_id`、程式識別碼 **不翻譯**
- 插圖不另建 `_hk.svg`

## 相關

| 路徑 | 角色 |
|------|------|
| [`../design_phase/`](../design_phase/) | 設計專書（含 `*_hk` 設計稿） |
| [`../../planning/user_guide/`](../../planning/user_guide/) | 僅撰寫計畫 |
"""
    (BOOK / "README_hk.md").write_text(text, encoding="utf-8")


def write_language_policy() -> None:
    text = """# User guide language policy

## Rule

Every reader-facing Markdown file under `book/user_guide/` **must** exist in both:

| Language | Pattern | Example |
|----------|---------|---------|
| English | `*.md` (no `_hk` suffix) | `user_guide.md`, `chapters/05-first-workflow-run-e1.md` |
| Traditional Chinese | `*_hk.md` | `user_guide_hk.md`, `chapters/05-first-workflow-run-e1_hk.md` |

## Exceptions (shared, not translated as separate docs)

- `assets/*.svg` — shared figures (labels may stay English for product terms)
- Binary / media if any later

## Do not translate

- API paths (`/api/v1/...`)
- Workflow / agent / skill ids (`wf_video_arch_a_viral_hook_v1`)
- Env vars (`NEXT_PUBLIC_DEMO_MODE`)
- File and package paths
- HTTP methods and status codes

## Maintenance

1. Edit English chapter first (or HK first if authoring in Chinese), then sync the pair.
2. Regenerate HK scaffolds: `python planning/user_guide/_gen_hk.py`
3. Full prose: expand **both** `foo.md` and `foo_hk.md` in place under `book/user_guide/`.
4. Links inside EN docs should offer HK alternate; HK docs should link EN alternate.

## Definition of done (bilingual)

- [ ] Same chapter set EN + HK (00–19, A–C)
- [ ] Masters: `user_guide.md` + `user_guide_hk.md`
- [ ] TOCs: `TOC.md` + `TOC_hk.md`
- [ ] READMEs: `README.md` + `README_hk.md`
- [ ] Cross-links both directions
"""
    (BOOK / "LANGUAGE.md").write_text(text, encoding="utf-8")


def patch_english_masters() -> None:
    ug = BOOK / "user_guide.md"
    if ug.exists():
        t = ug.read_text(encoding="utf-8")
        if "user_guide_hk.md" not in t:
            t = t.replace(
                "| **Design monographs** | [`../design_phase/`](../design_phase/) |",
                "| **Traditional Chinese** | [`user_guide_hk.md`](./user_guide_hk.md) · [`TOC_hk.md`](./TOC_hk.md) |\n"
                "| **Design monographs** | [`../design_phase/`](../design_phase/) |",
            )
            if "## Front matter" in t and "繁體中文" not in t:
                t = t.replace(
                    "## Front matter",
                    "> 繁體中文版：[user_guide_hk.md](./user_guide_hk.md)\n\n## Front matter",
                )
            ug.write_text(t, encoding="utf-8")

    toc = BOOK / "TOC.md"
    if toc.exists():
        t = toc.read_text(encoding="utf-8")
        if "TOC_hk.md" not in t:
            t = t.replace(
                "**Writing plan (only):** `planning/user_guide/`",
                "**Writing plan (only):** `planning/user_guide/`  \n"
                "**Traditional Chinese TOC:** [`TOC_hk.md`](./TOC_hk.md) · master [`user_guide_hk.md`](./user_guide_hk.md)",
            )
            toc.write_text(t, encoding="utf-8")

    readme = BOOK / "README.md"
    if readme.exists():
        t = readme.read_text(encoding="utf-8")
        if "user_guide_hk.md" not in t:
            t = t.replace(
                "Open **[user_guide.md](./user_guide.md)**.",
                "Open **[user_guide.md](./user_guide.md)** (English) or **[user_guide_hk.md](./user_guide_hk.md)** (繁體中文).\n\n"
                "Language policy: [`LANGUAGE.md`](./LANGUAGE.md) — every `*.md` has a `*_hk.md` pair.",
            )
            readme.write_text(t, encoding="utf-8")

    # Patch EN chapter nav + ZH link
    for c in CHAPTERS:
        en_path = CH / c["en"]
        if not en_path.exists():
            continue
        t = en_path.read_text(encoding="utf-8")
        hk = hk_name(c["en"])
        if f"{hk}" not in t or "繁體中文" not in t:
            # ensure bilingual nav
            if "## Navigation" in t:
                if "Traditional Chinese" not in t and "繁體中文" not in t:
                    t = t.replace(
                        "## Navigation\n",
                        f"## Navigation\n\n"
                        f"- 繁體中文：[`{hk}`](./{hk})\n",
                    )
            en_path.write_text(t, encoding="utf-8")


def main() -> None:
    write_language_policy()
    write_user_guide_hk()
    write_toc_hk()
    write_readme_hk()
    for c in CHAPTERS:
        path = CH / hk_name(c["en"])
        path.write_text(chapter_md(c), encoding="utf-8")
    patch_english_masters()
    en = list(CH.glob("*.md"))
    hk = list(CH.glob("*_hk.md"))
    # non-hk chapter count
    en_only = [p for p in en if not p.name.endswith("_hk.md")]
    print(f"book={BOOK}")
    print(f"chapters_en={len(en_only)} chapters_hk={len(hk)}")
    print(f"user_guide_hk={(BOOK / 'user_guide_hk.md').exists()}")
    print(f"TOC_hk={(BOOK / 'TOC_hk.md').exists()}")
    missing = []
    for c in CHAPTERS:
        if not (CH / c["en"]).exists():
            missing.append(c["en"])
        if not (CH / hk_name(c["en"])).exists():
            missing.append(hk_name(c["en"]))
    if missing:
        print("MISSING", missing)
    else:
        print("pair_check=OK")


if __name__ == "__main__":
    main()
