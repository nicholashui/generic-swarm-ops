# 倉庫比較：generic-swarm-ops 與 va-agent-swarm

**日期：** 2026-07-11  
**目的：** 根據對兩個倉庫的深度掃描（structure.md、backend.md、frontend.md、adoption.md 審計 + va 的 study/agents.md、SYSTEM_REFERENCE.md、代理規格、工作流、UI 文件、66 章參考文獻等），詳細比較共同功能、優缺點、評分及差距。  
**方法：** 識別架構、規格與實作中的重疊功能領域。評估實作成熟度、規格深度、生產/影片領域使用準備度，並註明缺失能力。  
**核心洞見：** 兩個倉庫高度互步。`generic-swarm-ops` 是一個**生產就緒的受治理平台**（運行時、治理、演化、後端/前端）。`va-agent-swarm` 是**世界級的研究/規格語料庫**，專注於影片製作多代理系統（114 個代理、詳細功能/技術規格、工作流、LQR、原型、UI 概念），但缺乏可執行的運行時。

---

## 總結表格：整體評分

| 領域 / 功能                      | generic-swarm-ops                          | va-agent-swarm                              | 哪個較佳？                | 評分 (1-10)   | 主要差距 / 建議 |
|----------------------------------|--------------------------------------------|---------------------------------------------|---------------------------|---------------|-----------------|
| **代理定義與名冊**              | 基本種子代理（5 個運營）；領域存根         | **完整的 114 代理名冊**（10 個類別，agents.md + 個別功能/技術規格） | va（規格深度）           | generic: 4<br>va: 9 | 將完整 va 名冊匯入 generic `business/video/agents/` 作為領域包。generic 需要每代理結構 + ALC。 |
| **工作流 / 流程定義與編排**     | 強大的 Workflow DNA 結構、有界狀態圖、運行時執行、SSE | 優秀的影片特定流程（6 階段 E2E、原型 A–J、LQR 家族、SVG、人機圖、編排主幹 #53–#56） | 互步（generic 運行時 + va 領域） | generic: 8<br>va: 8 | 將 va 流程映射到 generic DNA。generic 主幹已就緒；va 提供豐富影片內容。 |
| **知識管理、RAG、記憶**         | 分層混合檢索（LightRAG-lite）、混合記憶類型、來源追溯、代理/組織範圍 | 強大的概念性代理式 RAG、知識路由器規格、參考語料庫（66 章提煉） | generic（實作）          | generic: 7<br>va: 6 | 將 va 參考 + 代理式 RAG 規格種子化到 generic 知識層。新增代理範圍記憶。 |
| **評估與品質保證**              | 完整測試框架（黃金任務、回歸、對抗、人類審查）、EvaluationCard、適應度函數 | 豐富的評分標準、品質閘、批判總線、一致性機制（LQR）、心理對齊 | va（領域評分標準）       | generic: 8<br>va: 7 | 將 va 評分標準/批判機制移植到 generic 評估。generic 有更好的運行時整合。 |
| **治理、風險、審批、安全**      | 優秀：風險等級（0-5）、審批閘、審計日誌、OWASP 映射、工具權限代理、紅隊 | 概念性安全/倫理代理、部分政策提及           | generic（完整實作）      | generic: 9<br>va: 3 | va 規格可為 generic 治理提供領域特定風險覆蓋。 |
| **演化、學習、自我改進**        | 強大沙盒（提出/測試/金絲雀/回滾）、自動反思、教訓、技能沙盒、GEPA 式反思 | 強烈的每代理反思意圖、自我精煉、情景記憶、agent_loop 迭代（v1–v3） | generic（運行時）+ va（意圖） | generic: 8<br>va: 6 | 在 generic 中實作代理學習合約（ALC），採用 va 反思概念。新增代理基因組。 |
| **前端 / UI 管理**              | 生產級 Next.js 運營控制台（儀表板、代理、工作流、運行、Improve、演化存檔、SSE）+ OpenDesign MCP | 詳細的願景 UI 規格（代理管理、管線視覺化、生產規模發現、專案建立、RETHINK_100） | generic（已實作）        | generic: 8<br>va: 7 | 參考 va UI 規格，擴展 generic 前端影片領域頁面。使用 OpenDesign 保持一致。 |
| **後端 / 運行時執行引擎**       | 成熟且已上線 — FastAPI 控制平面、runtime.py（工作流引擎/狀態）、工作者、Postgres runtime_state JSONB、工具效果、SSE | 幾乎沒有（僅 SVG 輔助與旁白腳本）           | generic（遠勝）          | generic: 9<br>va: 1 | va 僅有規格；應作為 Domain Pack 重建在 generic 運行時上。禁止建立第二平台。 |
| **工具整合與配接器**            | 框架就緒（adapters.py 模式、工具權限代理、短暫範圍憑證、效果日誌） | 媒體生成工具概念需求（Sora/Veo 等）、提示工具、一致性工具 | generic（框架）          | generic: 7<br>va: 4 | 新增 video.* 媒體配接器（先用存根供 CI 使用）。va 提供需求。 |
| **文件與研究深度**              | 強大技術架構文件（structure.md 完整層級、backend.md、frontend.md）、SDD、差距分析 | **傑出**影片領域研究（114 代理、66 章提煉、深度代理規格、UI、工作流、system_build_plan） | va（領域研究）           | generic: 7<br>va: 10 | 將 va 作為 generic `business/video/knowledge/` 的權威影片知識種子。保留 va 作為上游研究倉庫。 |
| **流程智慧 / 分析**             | 專用流程智慧層（事件日誌、流程掘掖器、一致性、瓶領、因果代理、PI 產物） | 隱含於工作流/人機圖、部分分析提及           | generic（實作）          | generic: 8<br>va: 4 | va 可提供影片特定流程模型種子化到 generic PI。 |
| **多領域 / 可擴展性**           | 領域包概念正在形成、business/ 擴展點、多包結構 | 單一領域聚焦（影片）+模組化代理規格        | generic（平台設計）      | generic: 7<br>va: 3 | generic 設計用於數十個 MMA 包；va 是完美首個豐富包範例。 |
| **整體生產就緒度**              | 高（產品標準 ~100、E1 通過、已上線運行時/治理） | 低（規格完整、運行時缺失）                 | generic                  | generic: 9<br>va: 2 | 合併：generic = 主機；va = 完整領域包（完整名冊 + 流程）。 |

---

## 各領域詳細說明

### 1. 代理定義與名冊
- **generic-swarm-ops**：擁有種子運營代理（business_orchestrator、quality_compliance、execution、finance_ops、communications）。領域代理為存根/佔位符。後端結構中有強大註冊概念，但尚未填入 114 個影片專員。
- **va-agent-swarm**：黃金標準 — 完整解析的 114 代理名冊（study/agents.md）、10 個類別（Above-the-Line、Camera、Editorial、Sound、Performance、Distribution、Education、AI-Era、Meta/Orchestration 主幹 #53-80、Workflow Support #81-114），以及數十個代理的深度功能 + 技術規格（aesthetics、research、psychological profile/recommendation、coding、general creative、intent analysis、optimization、podcast、screenwriter/strategic goal、knowledge_router、agent_loop v1-v3、planner v2.x 等）。
- **評分與說明**：va 在**影片領域的規格深度與完整性**上取得決定性勝利。generic 在**運行時註冊基礎**上較佳。**差距**：generic 缺少完整名冊匯入及每代理 `agent_spec.json` + ALC 綁定。**建議**：Wave 0 將全部 114 個匯入 `business/video/agents/<pack_id>/`，使用穩定 ID 與 MAP 可追溯性。永不刪除代理。

### 2. 工作流 / 流程定義與編排
- **generic-swarm-ops**：優秀的 WorkflowDNA 結構（輸入、步驟、代理、工具、護濵、驗證、回滾、適應度）。有界狀態圖執行、運行時引擎、SSE 串流、人類閘。適合一般商業流程（如客戶 onboarding）。
- **va-agent-swarm**：傑出的影片特定分解 — 6 階段 E2E 製作管線、原型 A–J（viral-hook 至 feature-film）、LQR 家族（角色一致性、每鏡頭循環、品質閘、引擎路由、場景流）、人機工作流圖、編排主幹（Orchestrator #53、Planner #54、Router #55、Judge #56 + GateKeeper 等）。
- **評分與說明**：互步。generic 提供**可執行運行時 + DNA 引擎**；va 提供**豐富領域內容**（影片製作逻輯、批判/QC 網格、一致性機制）。**差距**：va 沒有可執行 DNA/運行時；generic 缺少影片特定流程預先匯入。**建議**：將 va 流程映射到 generic WorkflowDNA（需 orchestrator-down 層級）。從主幹 + viral-hook 原型開始 E2E 驗證。

### 3. 知識管理、RAG、記憶
- **generic-swarm-ops**：分層混合檢索（Tier 0 預設向量、Tier 1 LightRAG-lite 用於關係、Tier 2 層級摘要可選）、混合記憶類型（事件、情景、語義、程序、決策、例外、評估、來源）、代理/組織範圍、永遠來源追溯。
- **va-agent-swarm**：對代理式 RAG 的強大概念支援、知識路由器代理規格、龐大提煉參考語料庫（study/reference/how_to_build_a_video_agent_system 下的 66 章）、意圖分析、研究規格。
- **評分與說明**：generic 在**已實作檢索 + 記憶架構**上較佳。va 在**影片領域知識深度**上較佳（研究、美學、心理對齊、一致性規則）。**差距**：generic 學習目前較偏工作流而非每代理；va 缺少運行時 RAG 接線。**建議**：將 va 參考語料庫 + 代理式 RAG 規格種子化到 generic 知識層，並完整來源追溯。擴展 generic 以支援代理範圍情景記憶與 pre-act 檢索。

### 4. 評估與品質保證
- **generic-swarm-ops**：成熟測試框架（黃金任務、回歸、對抗、人類審查集、歷史重播、成本/延遲基準、商業指標、安全/合規）。EvaluationCard 結構、帶 Pareto 選擇的適應度函數。
- **va-agent-swarm**：優秀的領域評分標準（美學、心理對齊、LQR 中的一致性、品質閘、批判總線、人機工作流覆蓋矩陣）。
- **評分與說明**：generic 在**運行時評估整合與測試框架**上較強。va 在**影片特定品質標準與評分**上較強。**差距**：va 評分標準尚未轉為可執行形式。**建議**：將 va 評分標準/批判機制移植到 generic EvaluationCard 同步驟護濵。用於影片黃金任務。

### 5. 治理、風險、審批、安全
- **generic-swarm-ops**：生產級 — 風險等級（0 觀察至 5 受限）、審批閘、審計日誌、OWASP LLM + Agentic 映射、工具權限代理、紅隊、威脅模型、模型卡、保證案例、NIST/ISO/EU AI Act 對齊。
- **va-agent-swarm**：概念性（倫理代理、規格中部分政策提及、元代理中的安全紅隊），但無已實作治理層。
- **評分與說明**：generic 在**已實作治理與安全控制**上遠勝。va 可貢獻領域特定風險覆蓋與倫理代理。**差距**：va 缺少運行時治理。**建議**：所有包皆使用 generic 治理；在 `business/video/policies/` 內擴展 va 啟發的影片風險政策。

### 6. 演化、學習、自我改進
- **generic-swarm-ops**：強大沙盒紀律（提出 → 測試 → 金絲雀 → 提升/回滾，永不直接修改生產）、自動反思、教訓學習、技能沙盒、GEPA 式自然語言反思、改進 API、帶人類閘的適應度。
- **va-agent-swarm**：優秀的意圖與迭代歷史 — 帶自我精煉/Reflexion 的 agent_loop v1–v3、情景記憶概念、planner 迭代、RETHINK_100 文化、UI 規格中的自我改進循環。
- **評分與說明**：generic 在**沙盒化運行時演化**上較佳。va 在**每代理反思意圖與迭代模式**上較佳。**差距**：generic 學習目前較偏工作流而非每代理；va 缺少可執行演化。**建議**：在 generic 中實作強制代理學習合約（ALC）（按 agent_id 標記的情景寫入、反思、pre-act 檢索、沙盒提案）。採用 va 反思模式。

### 7. 前端 / UI 管理
- **generic-swarm-ops**：生產級 Next.js 運營控制台，含儀表板、代理/工作流/運行管理、審批佇列、知識瀏覽器、演化存檔、Improve 按鈕、SSE 即時更新、權限感知導航、載入/空/錯誤狀態、OpenDesign MCP 工作流。
- **va-agent-swarm**：詳細的願景 UI 規格（代理管理儀表板、生產管線視覺化、規模/品質發現、專案建立流程、架構溝通、RETHINK_100 改進、master shell、surface map）。
- **評分與說明**：generic 在**已實作、回應式、即時運營控制台**上較佳。va 在**影片領域特定 UI 概念與流程**上較佳。**差距**：generic 缺少專用影片領域頁面。**建議**：參考 va UI 規格，擴展 generic 前端 `/app/domains/video/*` 路由。統一應用 OpenDesign。

### 8. 後端 / 運行時執行引擎
- **generic-swarm-ops**：成熟且已上線 — FastAPI 控制平面、runtime.py（工作流引擎/狀態）、工作者、Postgres runtime_state JSONB、工具效果、SSE、auth/RBAC、領域模型、服務層。
- **va-agent-swarm**：幾乎不存在（僅 SVG 生成輔助與旁白腳本；無後端、無運行時、無執行引擎）。
- **評分與說明**：generic 壓倒性較佳。va **僅有規格**。**差距**：va 沒有可執行核心。**建議**：將 va **完全作為領域包** 重建在 generic 運行時上（`business/video/` ）。禁止建立第二平台（LangGraph/Temporal 重複禁止）。

### 9. 工具整合與配接器
- **generic-swarm-ops**：框架就緒（adapters.py 模式、工具權限代理、短暫範圍憑證、效果日誌）。目前種子偏運營（CRM、email、billing、contract_parser、policy_retriever）。
- **va-agent-swarm**：媒體生成工具概念需求（Sora、Veo、Kling、ElevenLabs 等）、提示工具、一致性工具。
- **評分與說明**：generic 在**整合框架**上較佳。va 在**影片媒體工具需求**上較佳。**差距**：generic 缺少 video.* 媒體配接器。**建議**：新增影片領域配接器（先用存根供 CI，之後接真實供應商並設速率限制/預算）。

### 10. 文件與研究深度
- **generic-swarm-ops**：強大技術架構文件（structure.md 完整層級、backend.md、frontend.md）、SDD 流程、差距分析、產品標準證據。
- **va-agent-swarm**：傑出的影片領域研究深度 — 114 個代理規格、66 章「如何建立影片代理系統」提煉、許多代理的深度功能/技術規格、system_build_plan（M0–M12）、UI 設計、工作流、人機圖、agent_loop/planner 迭代、RETHINK_100 文化。
- **評分與說明**：va 在**領域研究與規格豐富度**上明顯勝出。generic 在**平台架構文件**上較強。**差距**：va 研究尚未接線到可執行系統。**建議**：將 va 作為權威上游研究/旁白倉庫。將其參考語料庫與規格種子化到 generic `business/video/knowledge/` 與代理包，並完整來源追溯。

### 11–12. 流程智慧與多領域可擴展性
- **generic-swarm-ops**：專用流程智慧層（事件日誌、掘掖器/一致性/瓶領/因果代理、PI 產物）。支援多 MMA 系統的領域包設計。
- **va-agent-swarm**：工作流與人機圖中隱含流程模型。單一領域（影片）聚焦。
- **評分與說明**：generic 在兩者上均較佳。**建議**：使用 va 影片流程豐富 generic PI。generic 架構已支援數十個包 — va 是理想首個豐富範例。

---

## 缺失功能 / 差距摘要

**generic-swarm-ops 中缺失或薄弱之處**：
- 完整影片代理名冊（114 個）與領域特定規格/評分標準。
- 影片製作流程（原型、LQR、6 階段 E2E、一致性機制）。
- 豐富影片領域知識語料庫與代理式 RAG 模式。
- 每代理學習合約（ALC）強制執行與代理範圍記憶。
- 影片特定媒體工具配接器。
- 專用影片領域 UI 頁面與管線視覺化。

**va-agent-swarm 中缺失或薄弱之處**：
- 任何生產後端/運行時/執行引擎。
- 治理、風險等級、審批、審計、安全控制。
- 演化沙盒與運行時自我改進。
- Workflow DNA 執行 + SSE + 工作者。
- 工具整合框架與權限代理。
- 可擴展多租戶後端（auth、RBAC、狀態管理）。
- 帶即時更新的生產前端運營控制台。

**兩者皆強（互步）之功能**：
- 代理概念與迭代（va 規格 + generic 運行時）。
- 工作流/流程思維（va 領域內容 + generic DNA 引擎）。
- 評估/品質（va 評分標準 + generic 測試框架）。
- 自我改進意圖（va 反思模式 + generic 沙盒）。

---

## 最終建議

**最佳合併策略（與 adoption.md v2.3 一致）**：
- **generic-swarm-ops** = 通用受治理 MMA 主機/平台（保留並擴展其運行時、治理、演化、後端/前端、領域包 SDK）。
- **va-agent-swarm** = 完整影片領域包（將**完整 114 代理名冊 + 完整流程**匯入 `business/video/`，並在 generic 專案中永久保留）。va 倉庫保留為上游研究、規格、旁白/腳本來源之真。
- **關鍵行動**：
  1. Wave 0：完整目錄匯入（目錄 + MAP + 全部 114 個最小規格）。
  2. 在 generic 中實作 ALC + 代理範圍學習。
  3. 將 va 流程映射到 WorkflowDNA（先從主幹開始）。
  4. 將 va 知識/參考種子化到 generic。
  5. 擴展前端加入影片領域視圖。
  6. 新增影片媒體工具配接器（存根 → 真實）。
- **成果**：具備自主每代理學習、受治理執行、未來可擴展至其他領域的生產就緒影片 swarm。無重複、無第二平台。

此比較確認，當正確合併為平台 + 豐富領域包時，兩個倉庫共同構成強大基礎。

*repo_compare.md 結束*