# 通用群體業務操作系統

### 完整技術手冊

**專案：** `generic-swarm-ops`
**入門規格：** `1.2.0-trae-only` · **業務規格：** `2.1`（研究整合版） · **產品標竿：** mark ~100
**目標環境：** Trae IDE + Grok Build（雙 harness）
**技術棧：** Node.js 20+（引導）· Python / FastAPI + Postgres（後端）· Next.js / React / TypeScript / Tailwind（前端）

---

> 本手冊是 `generic-swarm-ops` 系統的唯一完整參考資料。它由儲存庫中的真實來源文件
> 整合而成——包括 `starter.md`、`tasks.md`、`status.md`、`structure.md` / `structure_hk.md`、
> `backend.md` / `backend_hk.md`、`frontend.md` / `frontend_hk.md`、`plan_to_mark_100.md`、
> `docs/self-improvement-and-orchestration.md`，以及 `planning/structure/`、`planning/backend/`、
> `planning/frontend/` 下的 SDD 規格包與三份 gap analysis（結構／後端／前端產品標竿 100/100）——
> 並詳細描述每個組件、工作流程、架構決策和實作細節，讓任何讀者都能完整深入地理解整個系統。

---

## 目錄

1. [簡介與閱讀指南](#1-簡介與閱讀指南)
2. [這個系統是什麼](#2-這個系統是什麼)
3. [核心原則與設計優先順序](#3-核心原則與設計優先順序)
4. [高層架構](#4-高層架構)
5. [入門層：環境契約](#5-入門層環境契約)
6. [第一層——流程智慧](#6-第一層流程智慧)
7. [第二層——知識、蒸餾與混合記憶](#7-第二層知識蒸餾與混合記憶)
8. [第三層——執行：工作流DNA](#8-第三層執行工作流dna)
9. [第四層——演化引擎（沙盒）](#9-第四層演化引擎沙盒)
10. [第五層——治理、風險與合規](#10-第五層治理風險與合規)
11. [第六層——安全](#11-第六層安全)
12. [評估系統](#12-評估系統)
13. [代理名冊](#13-代理名冊)
14. [人機互動規則](#14-人機互動規則)
15. [後端 API 伺服器](#15-後端-api-伺服器)
16. [前端應用程式](#16-前端應用程式)
17. [儲存庫結構與引導程序](#17-儲存庫結構與引導程序)
18. [實作狀態](#18-實作狀態)
19. [端對端演練：客戶入職](#19-端對端演練客戶入職)
20. [操作指南：常見任務](#20-操作指南常見任務)
21. [90天部署計劃](#21-90天部署計劃)
22. [詞彙表](#22-詞彙表)
23. [參考資料](#23-參考資料)

---

## 1. 簡介與閱讀指南

`generic-swarm-ops` 是融合為一體的兩件事。

首先，它是一個**可執行的 Trae IDE 入門儲存庫**。它能夠下載、審計、篩選和同步大量參考來源
（技能、代理、命令、MCP 配置、規則）到受治理的 Trae 工作空間。這些行為來自 `starter.md`。

其次，它是一個**通用群體業務操作系統**——一個受治理、自我改進的多代理系統，能夠學習企業
實際運作方式，將知識蒸餾為可重複使用的資產，通過有邊界和可審計的代理工作流程執行工作，
並在沙盒而非生產環境中演化這些工作流程。這些行為來自 `structure.md`，並通過真實的
FastAPI 後端（`backend.md`）和 Next.js 前端（`frontend.md`）對外暴露。

這兩半是有意分層的。入門層是*環境契約*——使專案成為合法 Trae 專案的檔案、腳本、清單和
安全規則。業務層是*領域架構*——使專案發揮作用的代理、工作流程、記憶、治理和評估機制。
當兩者似乎衝突時，規則很簡單：**遵循更嚴格的安全、可審計性、治理和安全要求。**

**如何閱讀本手冊。** 第2–4章提供心智模型。第5章涵蓋入門環境。第6–14章逐步介紹六個架構層
加上評估、代理名冊和人機互動。第15–16章描述運行中的軟體（後端和前端）。第17–18章涵蓋
儲存庫及其當前建置狀態。第19–21章是實務內容：端對端演練、操作指南和部署計劃。
第22–23章以詞彙表和參考資料結尾。

全文插圖以 SVG 檔案形式儲存於本手冊旁的 [`book/assets/`](assets/) 目錄中。每張圖片都有
標題並在正文中引用。

---

## 2. 這個系統是什麼

通用群體業務操作系統是一個受治理、自我改進的多代理系統，它做四件事：

1. **學習**企業實際運作方式——從文件、從專家，以及關鍵地從真實事件日誌。
2. **蒸餾**這些知識成為可重複使用的規則、技能、工作流程和手冊。
3. **執行**工作通過有邊界、可審計的代理工作流程。
4. **演化**這些工作流程在沙盒中——絕不直接在生產環境。

![系統概覽——六個層被評估和演化包裹](assets/01-system-overview.svg)

*圖 2.1——系統一目了然。事件通過入口和風險路由器進入，流向業務協調器，並通過六個協作層。
每個動作都寫入審計日誌和記憶，進行評估，在需要時由人類審查，然後才會被考慮進入沙盒演化。*

設計是刻意保守的。自主權不是預設授予的；它是**按工作流程通過證據賺取的**。一個工作流程
從只允許觀察開始，隨著積累通過的評估、回滾計劃和人類簽核，它爬上自主梯（第10章）。
這就是將本系統與無約束「群體」區分開來的地方：圖，而非模型，掌握權威。

---

## 3. 核心原則與設計優先順序

七項原則支配系統中的每個決策：

1. **證據優於意見。** 從真實追蹤記錄學習，而不僅從人們說他們做什麼學習。
2. **有邊界的自主。** 每個動作都有風險等級、權限範圍，以及在需要時的人類關卡。
3. **一切都是可測試的。** 沒有代理、提示或工作流程能在不通過評估的情況下進入生產。
4. **沙盒演化。** 演化引擎只提出建議；它絕不直接變更生產環境。
5. **始終有來源追溯。** 每條規則、決策和記憶都能追溯到來源。
6. **可逆性優先。** 優先選擇可逆動作；其餘需要回滾計劃。
7. **以人為中心。** 顯示信心、顯示證據、讓修正變得容易。

這些原則通過明確的優先順序表達：

> **安全 → 可審計性 → 正確性 → 效率 → 自主性。**

這個順序不是裝飾。它解決權衡。如果讓工作流程更自主會降低可審計性，可審計性勝出。
如果更快的檢索路徑會削弱安全，安全勝出。整個系統的構建使得安全、可審計、正確的行為
也是預設行為。

---

## 4. 高層架構

系統頂部是一個**入口 + 風險路由器**。每個事件或請求——新工單、API 呼叫、排程作業——
都先到達這裡，被分類風險，並交給**業務協調器**，一個擁有全局目標並路由工作的狀態圖控制器。

從協調器，工作流經六個協作層：

- **流程智慧**（第6章）——從事件日誌學習真實工作流程。
- **知識 + 記憶**（第7章）——檢索增強知識，配備差異化記憶系統和始終在線的來源追溯。
- **執行工作流程**（第8章）——由「工作流DNA」描述的有邊界狀態圖。
- **治理**（第10章）——風險等級、審批規則和審計要求。
- **安全**（第11章）——對抗測試、提示注入防禦和爆炸半徑控制。
- **演化**（第9章）——提出和測試變體的沙盒。

一切都被**評估**系統包裹（第12章）。每次運行的輸出都寫入**審計日誌**和**記憶**，
然後進行評估，並（在風險等級需要時）由人類審查，然後才會考慮任何沙盒演化。

關鍵的架構洞見是將*權威*與*智能*分離。語言模型在圖的節點內提供智能。
圖——確定性、可檢查的代碼——提供權威：它強制執行狀態、權限和人機迴圈關卡。
安全和治理在模型之外確定性執行，因為「系統提示不是安全控制」。

---

## 5. 入門層：環境契約

在業務系統能夠存在之前，儲存庫必須是一個合法、可執行的 Trae 專案。這就是 `starter.md`
的工作，而且它已經在本儲存庫中完全實作並通過驗證（見第 18 章）。

### 5.1 目的與範圍

入門層建立一個可執行儲存庫，能夠**下載、審計、篩選和同步參考來源**到 Trae IDE 工作空間，
包括專案規則、自定義代理、技能、命令、MCP 配置和支援文件。它刻意限制為**只支援 Trae
IDE**——其他編輯器的輸出（`CLAUDE.md`、`GEMINI.md`、`.cursor/`、`.codex/`、Copilot 指示
檔案）明確不在範圍內。

入門層支援兩種模式：

- **自我引導模式（self-bootstrap）**——在當前儲存庫中實作入門儲存庫本身。
- **建立新專案模式（create-new-project）**——從規格生成一個新的下游專案。

### 5.2 不可妥協的成果

入門層「不只是文件」。命令 `npm run bootstrap` 必須執行一個真實的流程，順序如下：

```text
doctor
→ 建立所需目錄
→ 驗證 sources/manifest.json
→ 複製／更新所有啟用的 GitHub 來源
→ 寫入 sources/source-lock.json
→ 生成 docs/source-audit.md
→ 執行安全冒煙檢查
→ 執行同步預覽（sync dry-run）
→ 執行測試
```

除非參考儲存庫已實際下載到 `external/sources/`，否則專案不算完成。

### 5.3 來源清單與不受信任來源規則

`sources/manifest.json` 列出每一個上游參考儲存庫——ECC（「Everything Claude Code」）參考、
官方 Anthropic／OpenAI／Google 儲存庫、Model Context Protocol 伺服器與註冊表、GitHub MCP
伺服器、AGENTS.md 規格、Karpathy 風格行為規則、記憶與「超能力」技能參考、最佳實踐與發現
清單、社群子代理，以及安全規則集。每一筆記錄都帶有 `priority`、`tier`、`quarantine` 旗標和
`import_policy`。

安全模型是嚴格的，而且是整個專案的核心：

- 下載的儲存庫只存在於 `external/sources/` 底下，而且被 **git 忽略**——絕不提交。
- 它們是**不受信任的參考輸入**。下載器只會複製和檢查元數據。它絕不執行安裝腳本、
  `npm install`、`curl | bash`，或來自下載儲存庫的掛鉤，也絕不寫入專案根目錄以外的地方。
- 只有**經過篩選、審計、歸因**的材料才能複製到第一方目錄（`rules/`、`skills/`、`hooks/`、
  `mcp-configs/`、`docs/`），而且當影響較高時，必須經人類批准後才能進行。

必需來源若複製失敗即為致命錯誤；選用來源若失敗則只是記錄下來、非致命，除非傳入
`--strict`。已封存來源（`enabled: false`）預設絕不會被下載。

### 5.4 來源鎖定與來源審計

下載後，`sources/source-lock.json` 為每一個來源記錄已解析的 URL、提交、分支、最後提交元數
據、偵測到的授權檔案、套件檔案、隔離狀態和匯入政策。接著 `scripts/source-audit.mjs` 會讀取
清單和鎖定檔案，生成 `docs/source-audit.md`——一份逐來源的報告，當某來源沒有授權、包含遠端
執行的安裝腳本、已被封存、需要憑證、會修改全域代理配置，或附帶需要廣泛檔案系統／網路存取
的 MCP 伺服器時，就將它標記為**不安全、不宜自動匯入**。首次審計會把大部分儲存庫標記為「大量
匯入被拒，等待人類審查」。

### 5.5 同步層與生成的檔案

同步層會從第一方的 `rules/`、`skills/`、`hooks/` 和 `mcp-configs/` 重新生成 Trae 工作空間
輸出（`AGENTS.md`、`docs/agents.md`、`docs/trae.md`、`.trae/settings.json`、
`.trae/rules/`、`.trae/agents/`、`.trae/commands/`）。每一個生成的檔案都帶有標頭：

```text
<!-- AUTO-GENERATED by starter. Do not edit directly.
Source: rules/, skills/, hooks/, mcp-configs/
Run: npm run sync
-->
```

這就是為什麼儲存庫根目錄的 `AGENTS.md` 應該永不手動編輯；它是由 `npm run sync` 重新生成的。

![儲存庫佈局與引導管線](assets/12-repo-and-bootstrap.svg)

*圖 5.1——左邊是結合入門層、業務層、後端、前端與本書的儲存庫佈局。右邊是
`npm run bootstrap` 管線。任何一個必需步驟失敗都會導致整個引導失敗。*

---

## 6. 第一層——流程智慧

大多數「群體」設計只從文件和訪談中學習。這個系統堅持要從**實際營運追蹤記錄**中學習：工單、
CRM／ERP 操作、行事曆事件、電子郵件、審批、檔案編輯、API 呼叫和完成記錄。流程挖掘會把這些
日誌轉化為可發現的工作流程模型、合規檢查和瓶頸分析——也就是「影子模式（Shadow Mode）」的
實證版本。

![流程智慧層——事件來源、事件日誌與挖掘代理](assets/02-process-intelligence.svg)

*圖 6.1——原始事件來源被正規化成結構化事件日誌，流程挖掘代理再把它轉化為已發現流程、合規
報告、瓶頸分析和因果假設。*

### 6.1 流程挖掘代理

五個專門代理在這一層運作：

- **流程挖掘代理（Process Miner）**——從事件日誌發現真實工作流程。
- **任務挖掘代理（Task Mining）**——在許可的情況下觀察 UI／人類級別的步驟。
- **合規代理（Conformance）**——把實際工作與記錄的 SOP 進行比較。
- **瓶頸分析器（Bottleneck Analyzer）**——找出延遲、迴圈、返工和交接失敗。
- **因果改進代理（Causal Improvement）**——提出可能改善結果的干預措施。

### 6.2 事件日誌 Schema

事件日誌是實證學習的原子單位。每一個事件都捕捉了誰、對哪個案例、用了哪些工具，做了什麼，
以及結果為何：

```yaml
event:
  id: "evt_..."
  timestamp: "2026-07-06T14:03:00Z"
  actor_type: "human | agent | system"
  actor_id: "user_or_agent_id"
  process_id: "customer_onboarding"
  case_id: "customer_12345"
  activity: "review_contract"
  input_refs: ["doc_contract_v3"]
  output_refs: ["approval_decision_789"]
  tools_used: ["crm", "email"]
  decision_point: true
  decision_reason_summary: "Contract had non-standard liability clause."
  confidence: 0.82
  risk_tier: "medium"
  human_approved: true
  outcome:
    status: "completed"
    latency_minutes: 42
    quality_score: 0.94
```

儲存庫隨附這個結構的機器可讀 JSON Schema
（`business/schemas/event-log.schema.json`），以及一份符合規範的範例。允許的 `actor_type` 值
為 `human`、`agent` 和 `system`；允許的風險等級是六個具名等級
（`tier_0_observe` 到 `tier_5_restricted`），與第 10 章的自主梯相對應。

### 6.3 輸出的去向

已發現的流程和合規報告會提供給三個下游消費者：知識蒸餾管線（把重複出現的模式轉化為規則和
手冊）、評估系統（把歷史案例當作重放集），以及演化沙盒（從失敗和瓶頸中挖掘改進機會）。這些
產物存放在 `business/process-intelligence/` 底下的 `event-logs/`、`discovered-processes/`、
`conformance-reports/`、`bottlenecks/` 和 `causal-hypotheses/` 中。

---

## 7. 第二層——知識、蒸餾與混合記憶

文件和訪談仍然重要——但專家知識很大程度上是**隱性**的。哪些線索重要、什麼時候要覆蓋規則、
什麼時候「感覺不對」——這些都沒有寫下來。這一層的工作是捕捉隱性知識、蒸餾它，並把它儲存在一
個配備成本分層檢索堆疊的差異化記憶系統中。

### 7.1 誘發方法

單一一個「專家影子（Expert Shadow）」代理是不夠的。系統使用一套源自認知任務分析
（Cognitive Task Analysis）和關鍵決策方法（Critical Decision Method）的多方法捕捉工具包：

| 方法 | 最適用於 | 輸出 |
|---|---|---|
| 影子模式 | 真實動作 | 事件日誌、動作追蹤 |
| 關鍵決策訪談 | 罕見／高風險判斷 | 決策需求卡 |
| 大聲思考會話 | 例行專家工作 | 逐步啟發法 |
| 例外訪談 | 邊緣案例 | 例外庫 |
| 回顧審查 | 已完成案例 | 經驗教訓 |
| 學徒模式 | 專家教導群體 | 技能、手冊 |

### 7.2 決策需求卡

關鍵決策方法會產生一張**決策需求卡（Decision Requirement Card）**——對一個高風險決策點的
結構化記錄，會命名專家注意到的線索、正常動作、例外路徑、紅旗，以及所需的證據：

```yaml
decision_requirement:
  id: "drc_contract_exception_001"
  domain: "legal_operations"
  decision_point: "approve_non_standard_clause"
  expert_sources: ["senior_counsel_A", "contract_manager_B"]
  context_signals: ["customer_size", "liability_cap", "jurisdiction", "renewal_value"]
  cues_experts_notice:
    - "Clause shifts uncapped indirect damages to company."
    - "Customer insists on governing law outside approved list."
  normal_action: "route_to_legal_review"
  exception_paths:
    - condition: "enterprise_customer AND pre-approved fallback accepted"
      action: "approve_with_note"
  red_flags: ["unlimited liability", "data protection indemnity"]
  required_evidence: ["contract_diff", "customer_risk_profile", "approval_history"]
  risk_tier: "high"
  human_approval_required: true
  validation_tests:
    - "Does recommendation match senior counsel decision on historical cases?"
  confidence: 0.78
  last_reviewed: "2026-07-06"
```

儲存庫隨附一份 JSON Schema
（`business/schemas/decision-requirement-card.schema.json`）和範例，卡片則存放在
`business/experts/decision-requirement-cards/` 底下。

### 7.3 混合記憶

單一一個通用的「知識庫」是不夠的。長時間運行的代理需要**差異化記憶**——原始觀察、高層反思和
可檢索的長期儲存，這是 Generative Agents 和階層式記憶代理設計等研究所驗證過的模式。

![混合記憶類型與範圍規則](assets/04-hybrid-memory.svg)

*圖 7.1——八種記憶類型，各有獨特角色，加上支配每一次查詢和寫入的範圍與來源追溯規則。*

| 記憶類型 | 儲存 | 範例 |
|---|---|---|
| 事件（Event） | 原始營運日誌 | 「代理於上午 9:42 寄出發票。」 |
| 情節（Episodic） | 案例敘事 | 「這次續約差點失敗——法務太晚才被拉進來。」 |
| 語義（Semantic） | 事實／規則 | 「超過 25 萬的企業合約需要法務審查。」 |
| 程序（Procedural） | 技能／工作流程 | 「如何入職一個新客戶。」 |
| 決策（Decision） | 決策＋原因 | 「我們批准了例外 X，因為 Y。」 |
| 例外（Exception） | 邊緣案例 | 「若供應商位於 Z 區域，則使用替代流程。」 |
| 評估（Evaluation） | 測試結果 | 「工作流程 v12 未通過隱私測試。」 |
| 來源（Provenance） | 來源歸因 | 「這條規則來自 SOP v4 和專家 Alice。」 |

記憶預設從不會全域可用。每一次查詢都會考慮組織、用戶、代理、工作流程、部門、敏感性、有效期
和政策。高影響的寫入需要來源追溯和人類審查——這是系統的**記憶中毒防禦**，因為中毒記憶是一個
已命名的代理風險類別。

### 7.4 分層混合檢索

檢索堆疊刻意避開 GraphRAG 風格的社群摘要，因為它逐分塊萃取和生成社群報告的做法，會讓初始索
引和重新索引對一個持續攝入文件和事件日誌的系統來說昂貴得令人卻步。取而代之的是，它使用一個
**成本分層**堆疊，大多數查詢永遠不會碰到昂貴的層。

![以 LightRAG 為核心的分層混合檢索](assets/03-tiered-retrieval.svg)

*圖 7.2——查詢從最便宜的層開始，只有當需要關係推理或全語料庫綜合時才升級。一個始終在線的來
源層會為每一個答案附上來源。*

- **第 0 層——向量搜索**（預設、最便宜）。對分塊文件做語義相似度比對。沒有圖、沒有額外的
  LLM 呼叫。處理大多數「找出相關段落」的查詢。
- **第 1 層——LightRAG 圖層**（關係推理）。一個以圖為基礎的文字索引，具備雙層檢索（低層實體
  特定＋高層主題）和**增量更新**——新文件和事件可以直接加入而不需重建圖。這個增量特性正是選
  擇 LightRAG 的主要原因。它能回答關係型問題，例如「哪些義務依賴於這份合約？」或「誰碰過這
  個案例，順序為何？」。
- **第 2 層——階層式摘要**（RAPTOR 風格，選用，按需）。一棵遞迴叢集並摘要的樹，只為那些會頻
  繁出現全語料庫問題（例如「失敗入職案例中反覆出現的根本原因」）的語料庫而懶惰建立。
- **始終在線——來源層。** 每一個答案都會引用它的來源文件、專家、事件日誌或決策，無論是由哪
  一層提供服務。

升級規則會把 80% 以上的流量保持最便宜的層：從第 0 層開始，只有當查詢需要關係或多跳推理時才
升級到第 1 層，只有需要全域綜合時才升級到第 2 層。如果不想要自行建置，像 AnythingLLM 或
RAGFlow 這類現成平台可以託管這套堆疊，並把 LightRAG 放在它們後面。檢索會在脈絡相關性、答案
相關性和忠實度上分開評分，因為一個弱的檢索器會悄悄毒害每一個依賴它的代理。

### 7.5 知識資料夾結構

業務知識存放在 `business/` 底下的一個固定結構中：`process-intelligence/`、
`knowledge-base/`（規則、決策模式、例外、最佳實踐、隱性知識、來源）、`experts/`、
`materials/`、`distilled/`（技能、提示、工作流程、檢查清單、手冊）、`memory/`、`evals/`、
`governance/`、`security/` 和 `evolution/`。

---

## 8. 第三層——執行：工作流 DNA

執行不會以自由形式的群體發生。它發生在一個**有邊界的狀態圖**內，其結構由一個稱為
**工作流 DNA（Workflow DNA）** 的 schema 描述。推理與行動迴圈（ReAct 風格的思考、動作與觀察
交錯）在一個*節點內部*是有用的，但圖本身會強制執行狀態、權限和人機迴圈關卡。

![工作流 DNA 作為有邊界的狀態圖，連同其契約與驗證器](assets/05-workflow-dna.svg)

*圖 8.1——上方是執行圖，左下是每一份工作流 DNA 必須攜帶的強制聲明，右下是驗證器拒絕一個生
產工作流程的條件。*

### 8.1 工作流 DNA Schema

每一個工作流程都是一份完整、自我描述的契約：

```yaml
workflow_dna:
  id: "wf_customer_onboarding_v12"
  name: "Customer Onboarding"
  domain: "operations"
  objective: "Onboard customer with minimal delay and compliance risk."
  owner: "business_orchestrator"
  version: "12.0"
  inputs: ["signed_contract", "customer_profile", "billing_details"]
  preconditions:
    - "contract_status == signed"
    - "customer_risk_score <= threshold OR legal_approval == true"
  steps:
    - id: "verify_contract"
      agent: "quality_compliance_agent"
      tools: ["contract_parser", "policy_retriever"]
    - id: "create_customer_record"
      agent: "execution_agent"
      tools: ["crm"]
    - id: "configure_billing"
      agent: "finance_ops_agent"
      tools: ["billing_system"]
    - id: "send_welcome_packet"
      agent: "communications_agent"
      tools: ["email"]
  memory_reads: ["contract_rules", "customer_exceptions", "past_failures"]
  memory_writes: ["event_log", "decision_memory", "lessons_learned"]
  guardrails:
    human_approval_required_if:
      - "risk_tier == high"
      - "contract_exception_detected == true"
      - "tool_action_is_irreversible == true"
  verification:
    required_checks:
      - "crm_record_created"
      - "billing_config_validated"
      - "welcome_packet_sent"
      - "audit_log_complete"
  rollback:
    reversible: true
    rollback_steps: ["disable_customer_record", "void_initial_invoice", "notify_ops_owner"]
  fitness_metrics:
    - "cycle_time"
    - "error_rate"
    - "customer_satisfaction"
    - "compliance_pass_rate"
    - "human_escalation_rate"
    - "cost_per_case"
```

每一份工作流 DNA 都必須聲明：有邊界的狀態圖步驟、明確代理、明確工具、記憶讀寫聲明、護欄、
驗證檢查、回滾計劃、適應度指標，以及審計日誌寫入要求。儲存庫隨附
`business/schemas/workflow-dna.schema.json` 和範例，而驗證器
（`scripts/business/validate-business.mjs`）會**拒絕任何生產工作流程**，只要它沒有為高風險、
不可逆或例外處理動作加入人類關卡，或者缺乏不可逆動作的回滾計劃。

### 8.2 執行模式

運行時會把 DNA 實現為一台帶關卡的線性狀態機：

```text
事件 → 入口路由器 → 風險分類器 → 協調器
   → [研究] → [執行] → [驗證] → [合規] → [人類關卡]
   → 審計日誌＋記憶寫入 → 評估 → 演化沙盒
```

每一次過渡都是一個檢查點。在一個步驟運行之前，運行時會檢查取消信號、權限和治理；如果護欄要
求就請求批准；然後執行代理或工具；儲存步驟輸出；發送串流事件；並寫入一筆審計日誌。這正是後
端工作者執行一次運行的方式（第 15 章）。

---

## 9. 第四層——演化引擎（沙盒化）

演化引擎是讓系統變得「通用」和「自我改進」的原因。所有提出的變體在受閘 promote 成功前都是
**`sandbox_only`**。它也是最危險的組件，所以它被包裹在整個架構中唯一最重要的一條規則裡。

### 9.1 不可妥協的規則

> **演化管理器絕不可直接變更生產環境。**
> 它只能：提出變體 → 在沙盒測試 → 與基線比較 → 請求批准 → 金絲雀部署 → 失敗時自動回滾。

這單一一條約束，就把一個有風險的自主群體轉化成一個受控、可審計的系統。

![沙盒化的演化管線與其推廣關卡](assets/06-evolution-sandbox.svg)

*圖 9.1——十二步的演化管線完全在沙盒內運行。一個變體只有在通過右側每一項推廣要求後才會被推
廣。*

### 9.2 適應度函數

變體從不會依主觀偏好來評分。每一個變體都用一個明確的加權函數來評分：

$$F = w_q Q + w_s S + w_c C + w_e E + w_h H - w_r R - w_l L - w_k K$$

其中 $Q$＝品質、$S$＝安全、$C$＝合規、$E$＝效率、$H$＝人類滿意度，而 $R$、$L$、$K$ 分別是風
險、延遲和成本懲罰。對於真正衝突的目標，系統會使用**帕累托選擇（Pareto selection）**，而不
是把一切折疊成單一個純量。

### 9.3 管線

1. 觀察生產／影子追蹤。
2. 偵測失敗、瓶頸或機會。
3. 生成變體（提示／工作流程／工具使用／角色／專家模式的交叉組合）。
4. 離線對著金任務（golden tasks）測試。
5. 執行安全＋對抗測試。
6. 執行合規檢查。
7. 在歷史案例上重放（模擬）。
8. 若風險等級需要則進行人類審查。
9. 金絲雀部署到小範圍。
10. 監控指標。
11. 推廣／回滾／退役。
12. 把教訓存入演化記憶。

自然語言反思在這裡是一個強大的優化器：像 GEPA 這類反思式提示演化方法顯示，*少數*幾條軌跡，
經過語言診斷，就能勝過許多輪純量獎勵的強化學習——這對資料稀少的業務場景是很合適的。這些迴圈
永遠都待在上面那些沙盒關卡之內。

### 9.4 推廣規則

一個變體只有在滿足以下全部條件時才會被推廣：(1) 改善了目標指標，(2) 沒有讓安全或合規倒退，
(3) 通過回歸和對抗測試，(4) 有回滾計劃，(5) 有完整的審計日誌，以及 (6) 在風險等級需要時有
人類簽核。演化產物存放在 `business/evolution/` 底下的 `workflow-dna/`、`successful-variants/`、
`failed-experiments/`、`mutation-history/` 和 `lessons-learned/` 中。`business:evolution:check`
腳本會強制要求：沒有基線比較、回歸結果、對抗結果、合規檢查、回滾計劃，以及在風險等級需要時
的批准記錄，就不得暗示任何已推廣的生產變更。

---

## 10. 第五層——治理、風險與合規

治理會錨定在既有的框架上，而不是自己發明一套：

- **NIST AI RMF（AI 100-1）**——可信賴 AI 的 map／measure／manage 風險骨幹。
- **ISO/IEC 42001**——全球第一套人工智慧管理系統標準，圍繞 Plan-Do-Check-Act 方法論建立，
  用以建立、實施、維護和持續改進一套 AI 管理系統；它涵蓋風險管理、AI 系統影響評估、生命週期
  管理，以及第三方供應商監督。
- **歐盟 AI 法案（EU AI Act）**——若系統觸及歐盟用戶、勞工或受規範決策即適用。該法案已於
  2024 年 8 月 1 日生效；禁止性做法與 AI 素養義務自 2025 年 2 月 2 日起適用，通用 AI 模型義
  務自 2025 年 8 月 2 日起適用。時間表仍在變動——附錄三的高風險義務正透過 Digital Omnibus 從
  2026 年 8 月 2 日延後到 2027 年 12 月 2 日，但這要等到正式通過才會產生法律效力。這一點直接
  相關，因為該法案會把用於就業相關決策的 AI——招募、候選人篩選、績效評估、任務分配、勞工監
  控、升遷和解雇——歸類為高風險。如果這個群體系統碰觸到這些，就要預期在風險管理、資料治理、
  技術文件、記錄保存、透明度、人類監督、準確性、穩健性、網路安全、上市後監控和事件通報等方
  面會有要求。

*（上面的法規摘要是為符合授權限制而改寫；如需權威細節，請參閱 `structure.md` 所引用的主要
來源。）*

### 10.1 自主風險等級

自主權是按工作流程賺取的，這座梯有六級。

![六個自主風險等級](assets/07-risk-tiers.svg)

*圖 10.1——自主梯。一個工作流程從第 0 級開始，只有隨著證據累積才往上爬；第 5 級在有任何自
主動作之前，需要一份完整的保證案例（assurance case）。*

| 級別 | 自主程度 | 允許的行為 |
|---|---|---|
| 0 | 觀察 | 只能記錄與摘要。 |
| 1 | 建議 | 提出建議；由人類執行。 |
| 2 | 起草 | 準備產物；人類批准後才能發送／執行。 |
| 3 | 執行（可逆） | 若存在回滾且風險低即可執行。 |
| 4 | 執行＋關卡 | 可執行，但關鍵步驟需人類批准。 |
| 5 | 受限 | 在保證案例存在之前，不得有任何自主動作。 |

### 10.2 強制性產物

治理是以文件為支撐的。強制產物包括：AI 清單、用例風險分級、人類審批政策、審計日誌、事件響
應計劃、回滾計劃、資料保留政策、供應商／模型登記、工具權限登記、保證案例，以及模型卡。儲存
庫在 `business/governance/` 底下播種這些（例如 `ai-inventory/`、
`use-case-risk-tiering/risk-tiers.json`、`human-approval-policy/policy.md`、模型卡與保證案例
範本），而 `business:governance` 腳本會驗證它們的存在。

### 10.3 後端中的治理

在運行時，治理由後端的一個政策引擎來強制執行（第 15 章）。在工作流程或一個步驟運行之前，引
擎會評估政策並回傳下列之一：`allow`、`deny`、`require_approval`、`require_evaluation` 或
`require_redaction`。風險等級以 `low`、`medium`、`high` 和 `critical` 來表達，並對應到上面的
等級。高風險或不可逆的動作會讓運行暫停在 `waiting_for_approval`，直到人類做出決定。
## 11. 第六層——安全

代理系統會把攻擊面擴大到遠超傳統應用安全。有兩份 OWASP 參考適用：**LLM 應用程式 2025 年十
大風險**用於模型層，**代理應用程式 2026 年十大風險**用於自主層，其中突顯的威脅包括代理行為
劫持（Agent Behavior Hijacking）、工具誤用與利用（Tool Misuse and Exploitation），以及身分
與特權濫用（Identity and Privilege Abuse）。

有兩個設計事實支撐了整個安全態勢。第一，**間接提示注入**是多數代理系統的關鍵威脅，即使在對
齊和過濾之後，也應假設注入仍可能發生——所以爆炸半徑控制至關重要。第二，**系統提示不是安全控
制**；如果秘密在提示裡，它已經沒了。因此安全是在 **LLM 之外、確定性**地強制執行。

![代理安全與爆炸半徑控制](assets/08-security-controls.svg)

*圖 11.1——不受信任的輸入永遠被當作資料，絕不是指令。一道確定性的政策關卡——具備最小權
限、範圍化憑證和審批關卡——立於模型和任何真實工具或動作之間。控制矩陣把每一項控制對應到它
的 OWASP LLM 風險。*

### 11.1 控制矩陣（對應 OWASP LLM 2025）

| 風險 | OWASP | 控制 |
|---|---|---|
| 提示注入（尤指間接） | LLM01 | 將所有檢索到／用戶內容視為不受信任；指令與資料分離；爆炸半徑限制。 |
| 敏感資訊揭露 | LLM02 | 對輸出／日誌做 DLP；秘密絕不放入提示；保留期限限制。 |
| 供應鏈 | LLM03 | 模型／工具／轉接器登記；來源追溯；相依性＋SBOM 掃描。 |
| 資料與模型中毒 | LLM04 | 審查微調／LoRA；驗證檢索來源；對記憶做寫入過濾。 |
| 不當的輸出處理 | LLM05 | 將模型輸出視為不受信任輸入；執行前先淨化。 |
| 過度自主 | LLM06 | 依風險分級的自主；最小權限；審批關卡。 |
| 系統提示外洩 | LLM07 | 提示中不放秘密／角色；在外部強制執行授權。 |
| 向量／嵌入弱點 | LLM08 | 向量儲存做租戶隔離；中毒內容偵測。 |
| 不實資訊 | LLM09 | 溯源＋引用；顯示信心；高風險時人類審查。 |
| 無限制消耗 | LLM10 | 速率限制、逾時、預算上限（「denial-of-wallet」防禦）。 |

### 11.2 額外的代理控制

除了矩陣之外，還有五項代理控制適用：

- **工具權限經紀人（Tool Permission Broker）**——為每個任務提供狹窄、臨時、範圍化的憑證。
- **記憶中毒防禦**——對高影響的記憶寫入做來源追溯加人類審查。
- **技能／外掛審查**——第三方代理技能是一個活的供應鏈攻擊向量；要掃描並釘選版本。
- **全面可觀察性**——跨模型呼叫、工具呼叫和代理對代理流量的一條審計追蹤。
- **AI 事件響應**——為生成式 AI 特定事件定義的執行手冊。

儲存庫在 `business/security/` 底下播種安全產物——威脅模型與事件報告範本、一份
`tool-permission-register.json`，以及用於提示注入測試和紅隊結果的資料夾。`business:security`
腳本會掃描業務產物，尋找意外洩漏的秘密、過於寬泛的工具權限、不安全的工具描述、敏感動作缺
少人類關卡，以及提示注入測試覆蓋的缺口。它補強而非取代入門層的 `npm run security` 冒煙檢查。

---

## 12. 評估系統

評估是多數群體設計中最大的缺口，而在這裡它包裹了其他每一層。每一個代理、技能、工作流程和提
示都必須擁有八項評估資產：

1. 一個金任務集（golden task set）。
2. 回歸測試。
3. 對抗測試。
4. 一個人類審查集。
5. 一個歷史重放集。
6. 一個成本／延遲基準。
7. 一個業務結果指標。
8. 一個安全／合規分數。

評估會在真實的、多步驟、使用工具的環境中進行——AgentBench 和 SWE-bench 等代理基準測試的
教訓就是：隔離的提示測試無法預測真實任務效能。

### 12.1 評估卡

結果會被捕捉到一張結構化的卡片中：

```yaml
evaluation:
  target: "wf_customer_onboarding_v12"
  eval_type: "workflow_regression"
  test_set: "historical_onboarding_cases_q2"
  metrics:
    quality_score: 0.94
    compliance_pass_rate: 0.99
    average_cycle_time_minutes: 38
    escalation_rate: 0.12
    hallucination_rate: 0.01
    unauthorized_tool_attempts: 0
    cost_per_case_usd: 0.42
  result: "pass"
  promotion_decision: "canary_only"
  reviewer: "ops_lead"
```

儲存庫隨附 `business/schemas/evaluation-card.schema.json` 和範例。`business:eval` 線束會載入
評估卡、驗證指標欄位，並回報通過／失敗／阻塞——而且它**絕不自動推廣工作流程**。第一版以預覽
模式運行（`npm run business:eval -- --dry-run`）。

檢索會與生成分開，在脈絡相關性、答案相關性和忠實度上評估，因為一個弱的檢索器會悄悄讓每一個
下游代理退化。

---

## 13. 代理名冊

系統定義了一支由專門代理組成的名冊，分為三組。控制／元代理掌握權威；學習代理取得並策展知
識；執行／領域代理做具體工作。

![完整的代理名冊](assets/13-agent-roster.svg)

*圖 13.1——控制／元代理、學習代理，以及執行／領域代理。每一份代理文件都會指定其目的、允許
與禁止的動作、風險等級行為、所需證據、記憶規則、人類審批觸發條件，以及驗證命令。*

**控制／元（Control / Meta）**

| 代理 | 目的 |
|---|---|
| 業務協調器（Business Orchestrator） | 路由工作、管理狀態、擁有全局目標。 |
| 演化管理器（Evolution Manager） | 提出並測試變體（僅限沙盒）。 |
| 評估線束（Evaluation Harness） | 運行金任務／回歸／對抗／重放套件。 |
| 治理官（Governance Officer） | 套用風險等級、審批規則、審計要求。 |
| 安全紅隊（Security Red-Team） | 測試注入、工具誤用、洩漏、不安全自主。 |
| 記憶管家（Memory Steward） | 維護記憶品質、來源、有效期。 |
| 工具權限經紀人（Tool Permission Broker） | 授予範圍化、臨時的工具存取。 |
| 事件指揮官（Incident Commander） | 處理失敗、回滾、事後分析。 |

**學習（Learning）**

| 代理 | 目的 |
|---|---|
| 專家影子（Expert Shadow） | （在許可下）觀察專家。 |
| 認知任務分析師（Cognitive Task Analyst） | 把訪談轉成決策卡＋啟發法。 |
| 流程挖掘器（Process Miner） | 從日誌發現工作流程。 |
| 任務挖掘代理（Task Mining） | 在許可下觀察 UI／人類級別步驟。 |
| 合規代理（Conformance） | 把實際工作與記錄的 SOP 比較。 |
| 瓶頸分析器（Bottleneck Analyzer） | 找出延遲、迴圈、返工、交接失敗。 |
| 因果改進代理（Causal Improvement） | 提出可能改善結果的干預措施。 |
| 知識蒸餾器（Knowledge Distiller） | 把原始材料轉成規則／技能／手冊。 |
| 知識策展人（Knowledge Curator） | 驗證、去重、整理。 |

**執行／領域（Execution / Domain，範例）**：品質合規代理（Quality Compliance）、執行代理
（Execution）、財務營運代理（Finance Ops），以及通信代理（Communications）。

每一個代理在 `.trae/agents/` 底下都有一份文件，描述其目的、允許的動作、禁止的動作、風險等級
行為、所需證據、記憶讀寫規則、人類審批觸發條件，以及驗證命令。

---

## 14. 人機互動規則

綜合超過二十年的指引（微軟的《人機互動指引》，Guidelines for Human-AI Interaction），群體必
須：顯示信心和不確定性；解釋所使用的證據；在執行動作前先預覽；讓修正只需一次點擊；允許覆
蓋；把被拒絕的建議存為訓練資料；在脈絡薄弱時請求澄清；並且絕不把不確定性藏在自信的語言背
後。

這些規則不是理想——它們被接線到產品介面裡。前端（第 16 章）會顯示運行狀態、證據和審批檢查
點；被拒絕的建議會變成訓練信號；而破壞性動作永遠是明確且經確認的。

---

## 15. 後端 API 伺服器

後端不是一個薄代理。它是**受治理的智能與控制層**。前端從不直接接觸代理、資料庫、工作流程引
擎、LLM 提供者、向量儲存或內部工具——一切都通過 API。

> 前端＝用戶體驗層
> 後端 API＝受治理的智能與控制層
> 代理＝專門的工作者
> 工作流程＝結構化的業務執行路徑
> 治理＝風險與審批控制
> 審計＝信任與可追溯層

![後端分層架構](assets/09-backend-architecture.svg)

*圖 15.1——四層架構：API 路由（薄）、服務＋領域邏輯（豐富），以及基礎設施轉接器（與提供者
無關）。橫切中介軟體處理認證、RBAC、速率限制、幂等性、請求 ID、錯誤封套、指標和安全標頭。*

### 15.1 技術堆疊

```text
後端框架：FastAPI（Python）
資料庫：PostgreSQL
向量搜索：pgvector / Qdrant / Weaviate / Pinecone
佇列：Redis + Celery/RQ/Arq，或 Temporal
快取：Redis
物件儲存：S3 相容
LLM 提供者層：與提供者無關的抽象
認證：JWT / OAuth2 / SSO-ready
API 風格：REST + SSE 用於串流
文件：OpenAPI（自動生成）
容器化：無（沒有 Docker）
```

**As-built（產品標竿 ~100）：** FastAPI + **Postgres** 作為主控制平面儲存（`runtime_state`
JSONB）、JSON 檔快照作備份／種子、**PBKDF2** 密碼雜湊、組織範圍 RBAC、request ID、metrics，
以及程序內 run 推進 + **SSE**（佇列／worker 後端仍屬架構相容）。工具執行用本機 adapters 寫入
持久 `tool_effects`。演化與改進 API 強制變體保持 **`sandbox_only`**，直至受閘 canary／promote。
多 worker Temporal、常駐大規模 Redis／向量網、以及外部即時 CRM／email SaaS adapters 屬產品標
竿 **非目標**。

### 15.2 六項核心設計原則

1. **API 優先**——所有功能都可透過有文件、有版本的 API 存取。
2. **預設安全**——每個端點都要求認證（除非明確公開）；每個敏感操作都檢查授權；每次執行都可
   審計。
3. **治理優先**——後端在代理或工作流程執行*之前*就決定一個動作是否被允許，會評估用戶權限、
   工作流程權限、資料存取權限、風險等級、審批要求、工具存取權限，以及政策合規。
4. **人機迴圈**——高風險動作（寄出外部電子郵件、修改客戶記錄、刪除資料、發布內容、批准財務
   動作、變更工作流程定義或治理政策）會暫停並請求人類批准。
5. **審計一切**——每一個重要動作都會產生一筆審計事件；審計日誌是只能附加的。
6. **長任務用工作者**——代理工作流程透過佇列運行，而不是在 API 請求執行緒內：
   `前端 → 後端 API → 佇列 → 工作者 → 資料庫 → 把更新串流回前端`。

### 15.3 API 路由

所有路由都在 `/api/v1/` 底下。完整的介面涵蓋：`auth`、`users`、`organizations`、`agents`、
`tools`、`workflows`、`workflow_runs`（含 **cancel／retry／pause／resume／expire**）、
`approvals`、`governance`、`knowledge`、`memory`、`evaluations`、`audit_logs`、`processes`、
`evolution`、`improvement`、`loops`、`settings`，以及 `health`（包含 `/live` 和 `/ready`
子路由）。路由檔案很薄——它們驗證輸入、呼叫服務並回傳回應。

**SDD：** 後端子功能規格在 `planning/backend/`，**BE-01…BE-24**（`requirements.md`／`design.md`／
`tasks.md` v2.2，含 Deliverable 程式路徑）。索引：
`planning/backend/TASK_TO_CODE_TRACEABILITY.md`。落差分析：
`planning/gap_analysis_for_backend.md`（**100/100**）。

### 15.4 認證與授權

認證支援 JWT 存取權杖（含刷新權杖輪換）、用於服務整合的 API 金鑰，以及選用的 OAuth2／OIDC。
角色包括 Owner、Admin、Manager、Operator、Reviewer、Viewer 和 ServiceAccount。權限以
`resource:action` 配對表達（例如 `workflows:run`、`approvals:approve`）。授權系統被設計成可
支援未來的 ABAC 規則，例如 `user.department == resource.department` 或
`workflow.risk_level <= user.max_risk_level`。

每一筆資料庫查詢都會以 `organization_id` 範圍化——組織 A 的用戶永遠無法存取組織 B 的資料。
敏感資源會額外強制執行部門限制、ACL 規則、角色權限和政策檢查。

### 15.5 資料模型

二十個核心實體：`Organization`、`User`、`Role`、`Permission`、`APIKey`、`Agent`、`Tool`、
`Workflow`、`WorkflowVersion`、`WorkflowRun`、`WorkflowRunStep`、`ApprovalRequest`、
`GovernancePolicy`、`KnowledgeDocument`、`KnowledgeChunk`、`MemoryItem`、`EvaluationRun`、
`AuditLog`、`ProcessMetric` 和 `Notification`。每一個實體都帶有 `organization_id` 以做租戶隔
離——即使在目前的單租戶建置中也一樣，好讓多租戶之後變得直截了當。

關鍵實體關係：

- 一個 `Workflow` 有多筆 `WorkflowVersion` 記錄；同一時間只有一筆是 `current_version_id`。
  版本在啟用後即不可變。
- 一筆 `WorkflowRun` 會記錄所執行的確切 `workflow_version_id`，而不只是工作流程 ID，所以結
  果永遠可重現。
- 每一筆 `WorkflowRun` 有多筆 `WorkflowRunStep` 記錄——DNA 定義中的每一步一筆。
- 一個 `ApprovalRequest` 綁定到一個特定的 `workflow_run_id`，並可選地綁定一個
  `workflow_run_step_id`。
- 一個 `KnowledgeDocument` 有多筆 `KnowledgeChunk` 記錄，持有分塊內容和向量嵌入參照。
- 一個 `MemoryItem` 帶有 `scope` 欄位（`user`、`team`、`department`、`organization`、
  `agent`、`workflow`），記憶存取政策會在每次讀取時評估它。

### 15.6 工作流程運行生命週期

從 API 呼叫到完成的完整生命週期：

```text
1. POST /api/v1/workflows/{id}/runs，帶 Idempotency-Key 標頭
2. 後端驗證權限與治理——deny 或 require_approval 會立即回傳
3. 建立 WorkflowRun，狀態：queued
4. 排入工作者佇列
5. 工作者載入運行 → 標記 running
6. 對每一步：
   a. 檢查取消信號
   b. 檢查權限＋治理（deny / require_approval）
   c. 若需批准 → 建立 ApprovalRequest → 狀態：waiting_for_approval
   d. SSE 事件：approval.requested 串流到前端
   e. 審閱者透過 POST /approvals/{id}/approve 批准
   f. 工作者恢復 → 執行代理／工具／評估／條件
   g. 步驟輸出持久化 → WorkflowRunStep 更新
   h. SSE 事件：step.completed 串流
   i. 寫入審計日誌條目
7. 執行最終評估檢查
8. 輸出持久化 → WorkflowRun 狀態：completed
9. SSE 事件：run.completed 串流
```

幂等性金鑰可防止重複運行：如果同一個用戶為同一個工作流程傳送同一個金鑰，就會回傳現有的運
行，而不是建立一個新的。

![工作流程運行時序圖](assets/10-workflow-run-sequence.svg)

*圖 15.2——完整的工作流程運行時序，顯示 API、佇列、工作者、治理、審批暫停，以及回傳前端的
SSE 串流。*

### 15.7 知識攝取管線

```text
1. 用戶上傳文件 → 存入物件儲存
2. 建立 KnowledgeDocument（狀態：uploaded）
3. 索引作業排入佇列（狀態：processing）
4. 工作者：萃取文字 → 分塊 → 嵌入 → 儲存向量
5. KnowledgeDocument 狀態：indexed
```

檢索在回傳任何結果之前，會強制執行組織範圍化、部門限制、敏感性等級和 ACL 規則。每一次敏感
的知識存取都會寫入一筆審計事件。

### 15.8 以伺服器傳送事件（SSE）串流

後端在 `GET /api/v1/workflow-runs/{id}/stream` 發送 SSE 事件。事件類型包括：`run.started`、
`run.status_changed`、`step.started`、`step.completed`、`step.failed`、`approval.requested`、
`approval.approved`、`approval.rejected`、`evaluation.completed`、`run.completed`、
`run.failed`，以及 `log.message`。每個事件都帶有 `workflow_run_id`、`step_id`（如適用）、
`status`、`message` 和 `timestamp`。

### 15.9 安全控制

後端實作了：生產環境的 HTTPS、密碼雜湊（**as-built 為 PBKDF2**）、JWT 過期與刷新輪換、API
金鑰雜湊、每端點速率限制（記憶體內、可配置）、檔案上傳驗證、帶請求 ID 的結構化錯誤封套（絕
不洩漏內部堆疊追蹤）、安全標頭（Content-Security-Policy、X-Frame-Options、
X-Content-Type-Options、Strict-Transport-Security），以及 CORS 限制。提示注入防護會把受信任
的系統指令與不受信任的檢索內容分開、防止檢索到的文字授予工具權限，並在每次工具呼叫前要求
政策檢查。工具執行使用**本機 adapters** 並寫入持久 `tool_effects`（失敗封閉）；外部即時
CRM／email SaaS adapters 屬產品標竿**非目標**。

### 15.10 可觀察性

每一筆日誌記錄都包含 `timestamp`、`request_id`、`organization_id`（如有）、`user_id`、
`action`、`status`、`duration` 和錯誤碼。`/api/v1/health/live` 路由檢查 API 行程序是否在運
行；`/api/v1/health/ready` 檢查資料庫、Redis、佇列、向量儲存和物件儲存。一個受保護的指標端
點會彙總請求數、延遲、錯誤率、工作流程運行時長、工作流程失敗率、佇列深度、審批等待時間、
LLM 權杖使用量，以及 LLM 成本。

### 15.11 實作階段

後端依 BE-01…24 分階段建置：專案設置與健康 → 認證與使用者／組織（含邀請）→ 審計 → 代理與
工具登記 → 工作流程定義 → 執行引擎（生命週期 + SSE）→ 治理與審批 → 知識與記憶 → 評估 →
流程智能 → 演化沙盒與自我改進 → DNA 驗證 → 強化與生產就緒。驗收見 `status.md` 與
`planning/backend/*/tasks.md`。

---

## 16. 前端應用程式

前端是一個專業的企業 SaaS **營運主控台（ops console）**。它絕不能看起來像一個通用的 AI 展
示。它應該隨時傳達信任、可靠性、營運清晰度、安全、專業、速度、控制和可觀察性。前端只負責呈
現與互動——**授權、執行與治理的真相源永遠是後端。**

![前端架構與產品介面](assets/11-frontend-architecture.svg)

*圖 16.1——Next.js 前端位於瀏覽器與後端 API 之間。應用外殼（側邊欄、頁首、命令面板、組織切
換器）包覆所有已認證頁面。完整的產品介面涵蓋 14 個路由群組。*

### 16.1 技術堆疊

```text
框架：      Next.js（App Router）+ React + TypeScript
樣式：      Tailwind CSS + 設計權杖
表單：      React Hook Form + Zod
API 客戶端：從後端 OpenAPI schema 生成的型別化客戶端
即時：      伺服器傳送事件（SSE），用於工作流程運行時間軸
測試：      Playwright（e2e）+ Vitest/Jest（單元）+ React Testing Library + axe
套件管理器：pnpm
部署：      pnpm build + pnpm start（無 Docker）
```

OpenDesign MCP 的要求規定，在建立或大幅變更任何主要頁面佈局之前，Trae 必須呼叫 `opendesign`
MCP 伺服器來搜尋設計參考、萃取權杖，並產出佈局計劃。在目前的建置中 OpenDesign MCP 不可用，
所以回退工作流程已獲批准並記錄於 `frontend/docs/design/open-design-reference.md`。

### 16.2 設計系統

權杖類別涵蓋：Color、Typography、Spacing、Radii、Shadows、Borders、Surfaces、Status 顏色、
Motion、Z-index 和 Breakpoints。權杖檔案位於 `frontend/src/design/tokens.ts` 和
`frontend/src/design/theme.ts`。狀態顏色嚴格語義化：Success、Warning、Error、Info、Neutral、
Running、Pending、Paused、Cancelled、Draft 和 Published——在所有運行狀態、代理狀態和工具狀態
之間一致套用。

等寬字型用於 ID、日誌、API 金鑰、JSON 片段、工具呼叫載荷和追蹤 ID。動作是細微的——只用於抽
屜開關、命令面板、浮動通知、骨架載入、狀態轉換和時間軸更新。

### 16.3 渲染策略

應用採用混合方法。伺服器組件處理靜態佈局、初始資料擷取（可安全傳遞工作階段 cookie 之處）、
元資料，以及基本頁面組合。客戶端組件處理命令面板、即時運行時間軸、模態框、抽屜、帶篩選的資
料表、工作流程建構器，以及日誌檢視器。

路由保護只在 UX 層級套用：未認證用戶被重導到 `/login`；缺乏組織存取權的用戶被重導到一個拒
絕存取頁面；缺乏某路由權限的用戶會看到 `403 Access Denied`。後端授權仍是最終權威——一個被
隱藏的按鈕從不被當作安全控制。

### 16.4 資訊架構

公開路由：`/`、`/login`、`/register`、`/forgot-password`、`/reset-password`、
`/accept-invite`。

`/app` 底下的已認證路由：

| 群組 | 路由 |
|---|---|
| 主要 | `/app`（儀表板）、`/app/agents`、`/app/agents/new`、`/app/agents/[agentId]` |
| 工具 | `/app/tools`、`/app/tools/[toolId]` |
| 工作流程 | `/app/workflows`、`/app/workflows/new`、`/app/workflows/[workflowId]` |
| 運行 | `/app/workflow-runs/[runId]` |
| 審批 | `/app/approvals`、`/app/approvals/[approvalId]` |
| 知識 | `/app/knowledge`、`/app/knowledge/sources`、`/app/knowledge/documents`、`/app/knowledge/search` |
| 記憶 | `/app/memory`、`/app/memory/[memoryId]` |
| 品質 | `/app/evaluations`、`/app/processes`、**`/app/evolution`** |
| 安全 | `/app/audit-logs` |
| 管理 | `/app/settings/*`（組織、用戶、角色、帳務、api-keys、安全、整合、個人資料） |

側邊欄導覽分組為：主要（儀表板、代理、工作流程、審批）→ 資料（知識、記憶）→ 品質（評估、
流程、**演化**）→ 安全（審計日誌）→ 管理（設定）。

全域頁首帶有麵包屑、全域搜尋或命令按鈕、環境指示器、組織切換器、通知和用戶選單。命令面板
（`Cmd/Ctrl + K`）提供快速操作：建立代理、建立工作流程、搜尋知識、開啟最近的工作流程運行、
審查審批、邀請用戶、開啟 API 金鑰、開啟審計日誌、開啟安全設定、啟動評估、新增知識來源。

### 16.5 詳細的關鍵頁面

**儀表板（`/app`）**——營運總覽：代理健康卡、工作流程運行活動、待審批、知識庫健康、評估摘
要、最近的審計事件、流程狀態，以及快速操作。如果沒有代理或工作流程，會顯示一份入職清單（建
立代理 → 新增工具 → 新增知識 → 建立工作流程 → 運行 → 審查）。

**工作流程運行詳情（`/app/workflow-runs/[runId]`）**——最重要的頁面。載入時連接 SSE
（`WorkflowRunConsole`）。顯示即時時間軸、步驟詳情、即時日誌、工具呼叫、輸入／輸出、審批狀
態、錯誤（含 `request_id`），以及操作者動作：**取消、重試、暫停、恢復、逾期**（後端生命週期
API）。狀態含 Queued、Running、Waiting for Approval、**Paused**、Succeeded、Failed、
Cancelled、**Expired** 等。同頁 **Improve** 面板：Reflect → Propose → Evaluate → Canary（僅
backend 沙盒 API；禁止 client 改 production DNA）。

**審批（`/app/approvals`）**——審閱者看到待審批請求，附帶風險等級、脈絡，以及觸發它的工作
流程運行。可批准或拒絕並附備註。UI **禁止**靜默 auto-approve。

**演化（`/app/evolution`）**——沙盒族群／fitness 歸檔；evaluate／canary／promote 只呼叫
backend evolution APIs。

**知識（`/app/knowledge`）**——上傳文件、監控索引狀態、搜尋已索引語料庫、依來源類型瀏覽，
並查看文件分塊與敏感性等級。

**審計日誌（`/app/audit-logs`）**——只能附加的事件串流，可依執行者、動作、資源類型、資源 ID
和時間範圍搜尋。前端對系統 audit **唯讀**（不建立系統紀錄）。

**接受邀請（`/accept-invite`）**——公開表單 `POST /api/v1/users/invitations/accept`（token、
password、可選 name）；成功後寫入 session 進入 `/app`。

**設定——使用者與組織**——`UserAdminPanel` 邀請（`POST /users/invitations`）與
enable／disable（`PATCH /users/{id}`）；`OrganizationSettingsForm` 載入並
`PATCH /organizations/{id}`。

### 16.6 角色感知 UI

角色：Owner、Admin、Developer、Operator、Reviewer、Viewer、Billing Manager、Security
Auditor。前端會隱藏用戶無法執行的動作、為受限動作顯示帶說明的停用狀態，並為禁止的路由顯示
拒絕存取頁面。它從不依賴隱藏的 UI 作為安全控制——那項職責屬於後端。

### 16.7 SDD 與驗證狀態

**SDD：** 前端子功能在 `planning/frontend/`，**FE-01…FE-20**（`requirements.md`／`design.md`
v2.1／`tasks.md` v2.3）。索引：`README.md`、`TASK_TO_CODE_TRACEABILITY.md`、
`DESIGN_QUALITY_SCORE.md`、`TASKS_QUALITY_SCORE.md`。落差分析：
`planning/gap_analysis_for_frontend.md`（**100/100**）。

**Ops profile：** `NEXT_PUBLIC_DEMO_MODE=false` 對接 live FastAPI + Postgres 才是產品真相路徑；
demo 模式僅供 UI 預覽。

前端已通過以下驗證：

```bash
cd frontend && pnpm install   # pass
cd frontend && pnpm lint      # pass（0 error／0 warning，useWatch 修正後）
cd frontend && pnpm typecheck # pass
cd frontend && pnpm test      # pass
cd frontend && pnpm build     # pass
```

---

## 17. 儲存庫結構與引導

儲存庫是一個三層蛋糕：**入門層**（Trae IDE + Grok Build 雙 harness 環境契約）、**業務層**
（schema、驗證器、治理、安全、演化），以及**實作層**（後端＋前端），並加上 **planning/**
SDD 規格包。

### 17.1 頂層佈局

```text
generic-swarm-ops/
├── starter.md, structure.md, structure_hk.md, tasks.md, status.md
├── backend.md, backend_hk.md, frontend.md, frontend_hk.md
├── package.json, README.md, AGENTS.md
├── .trae/          （Trae — npm run sync 生成）
├── .grok/          （Grok Build — 雙 harness）
├── sources/, external/, scripts/, rules/, skills/, hooks/, mcp-configs/
├── business/       （PI、知識、專家、evals、治理、安全、演化…）
├── backend/        （FastAPI app/ + unit／e2e）
├── frontend/       （Next.js src/、docs/design/、tests/unit/）
├── planning/       （structure/ · backend/ · frontend/ SDD + gap_analysis_for_*.md）
├── docs/, examples/, tests/, memory/, reviews/, suggestions/
└── book/           （book.md、book_hk.md、book.*.md 手冊、腳本、assets/）
```

### 17.2 引導管線

`npm run bootstrap` 會協調完整的驗證序列。每一個必需步驟都必須通過，否則引導就會失敗。

```text
doctor
→ 建立所需目錄
→ 驗證 sources/manifest.json
→ 複製／更新所有啟用的 GitHub 來源
→ 寫入 sources/source-lock.json
→ 生成 docs/source-audit.md
→ 執行安全冒煙檢查
→ 執行同步預覽（生成 Trae 輸出）
→ 執行業務初始化
→ 執行業務驗證
→ 執行業務治理檢查
→ 執行業務安全檢查
→ 執行業務演化沙盒檢查
→ 執行測試（Node 內建測試執行器）
```

選用來源（priority：optional）的失敗會被記錄並回報，但不會讓引導失敗，除非啟用嚴格模式。必
需來源的失敗是致命的。

### 17.3 來源下載與審計

`sources/manifest.json` 列出 27 個上游儲存庫——官方 Anthropic／OpenAI／Google 儲存庫、MCP
伺服器、agent-skills 參考、Karpathy 風格行為規則、記憶架構，以及最佳實踐／發現清單。每一個來
源都帶有 `priority`（`required`／`optional`）、`tier`（core、official、standard、
behavior-rules、memory、skills、best-practices、discovery、security、cursor、agents、
historical）、`quarantine` 旗標，以及 `import_policy`（curated-only、reference-only、
never-import）。

下載器（`scripts/source-download.mjs`）會把儲存庫淺層複製到 `external/sources/`，並在
`sources/source-lock.json` 中記錄已解析的 URL、提交、分支、最後提交元資料、授權檔案、套件檔
案、隔離狀態和匯入政策。它絕不執行安裝腳本、`npm install`、`curl | bash`、掛鉤，也絕不把儲
存庫內容複製到使用中的 Trae 配置。

審計器（`scripts/source-audit.mjs`）會在某來源沒有授權、包含遠端執行的安裝腳本、已被封存、
需要憑證、會修改全域代理配置，或附帶需要廣泛檔案系統／網路存取的 MCP 伺服器時，把它標記為不
宜自動匯入。首次審計會把大部分儲存庫標記為「大量匯入被拒，等待人類審查」。

### 17.4 驗證命令

在建置中執行的每一條驗證命令都通過了（記錄於 `status.md`）：

```bash
npm run doctor                      # pass
npm run sources:download            # pass（26 個成功，0 個失敗，0 個跳過）
npm run sources:audit               # pass
npm run security                    # pass
npm run sync -- --dry-run           # pass
npm run business:init               # pass
npm run business:validate           # pass
npm run business:governance         # pass
npm run business:security           # pass
npm run business:evolution:check    # pass
npm run business:eval -- --dry-run  # pass
npm run test                        # pass
npm run bootstrap                   # pass

python -m compileall backend/app                                   # pass
python -m unittest discover -s backend/app/tests/unit -p "test_*.py" # pass
python -c "import fastapi; print(fastapi.__version__)"             # pass
python -c "import sys; sys.path.insert(0, 'backend'); from app.main import app; print({'route_count': len(app.routes), 'title': app.title})" # pass
python -c "import sys; sys.path.insert(0, 'backend'); from app.runtime import runtime; user = runtime.authenticate('admin-token'); run = runtime.start_workflow_run('wf_customer_onboarding_v12', user, {'case_id': 'smoke_case'}); print({'run_status': run['status'], 'approval_request_id': run['approval_request_id']})" # pass

cd frontend && pnpm install     # pass
cd frontend && pnpm lint        # pass（0 error／0 warning）
cd frontend && pnpm typecheck   # pass
cd frontend && pnpm test        # pass
cd frontend && pnpm build       # pass
```

---

## 18. 實作狀態

儲存庫已關閉 **產品標竿 mark ~100**（`plan_to_mark_100.md` P0–P5），並附 E1 操作者路徑證據、
完整後端／前端 SDD 規格包，以及結構／後端／前端 gap analysis 皆 **100/100**。

### 18.1 當前階段

**產品標竿完成**（scorecard 100/100）。E1 API 路徑 **PASS**。自我改進 + Loop Engineering +
K1-lite 知識編排 **已出貨**。前端 residual（accept-invite、pause／resume／expire、使用者邀請
／停用、組織 PATCH）**已出貨**。

### 18.2 已建立的內容

- 入門 + 雙 harness：Trae（`.trae/`）與 Grok Build（`.grok/`），經 `npm run sync`。
- `business/` 業務 OS 樹：schemas、evals（≥20 golden）、治理、安全、演化與 PI 產物。
- FastAPI 控制平面：**Postgres 主儲存**（`runtime_state` JSONB）、JSON 備份、PBKDF2、RBAC、
  速率限制、request ID、metrics；邀請、組織 PATCH、run lifecycle APIs。
- **真實 tool adapters** + 持久 `tool_effects`。
- Workflow DNA 執行：allow-list、memory scopes、human gates、eval `block_on_fail`。
- Process intelligence：ingest → 摘要 + 磁碟產物。
- Evolution：corpus 沙盒評估、fitness、canary、promote、rollback、archive；變體在受閘晉升前保持
  **`sandbox_only`**。
- Self-improvement：auto-reflect、lessons、auto-propose `sandbox_only` 變體、Loop DNA runner、
  skill sandbox（不改 host 程式）。
- Knowledge：Tier-0／Tier-1、K1-lite、federation export。
- Next.js 運營主控台：live 模式、真實表單、OpenAPI 型別、Run now、Improve、`/app/evolution`、
  accept-invite live、UserAdminPanel、OrganizationSettingsForm、run 全生命週期控制、lint 乾淨
  （useWatch）、unit + build 綠燈。
- **SDD：** `planning/structure/`（01–17）、`planning/backend/`（BE-01…24）、
  `planning/frontend/`（FE-01…20）及 task→code 索引。
- **Gap analyses：** structure／backend／frontend 各 **100/100**。
- 驗證：unit/e2e、`mark_100_verification.md`、`reviews/e1_operator_checklist.md`。

### 18.3 當前阻礙

產品標竿無阻礙。可選 UI dogfood 與 PR 合併屬流程步驟，非產品缺口。

### 18.4 下一步（mark 100 非目標）

- 外部 CRM/email 真實 adapters（本機 adapters 仍為預設）。
- 完整 LightRAG / Neo4j 生產 mesh；大規模真實 embedding + pgvector。
- Playwright CI 常駐伺服器；DGM 式 host 自我改寫 **仍不在範圍**。
- 在 `business/` 下持續擴充有 provenance 的領域內容。
- 可選衛生：backend OpenAPI 變更後 `pnpm api:generate`。

---

## 19. 端對端演練：客戶入職

這一章追蹤一個客戶入職請求，從到達到通過每一層，顯示每個階段發生什麼事、涉及哪些代理、執行
哪些檢查，以及人類在何處介入。

### 19.1 觸發

一份已簽署的合約透過入口端點到達。請求帶有已簽署的 PDF、客戶資料和帳務詳情：

```json
POST /api/v1/workflows/wf_customer_onboarding_v12/runs
{
  "inputs": {
    "signed_contract": "contract_abc123.pdf",
    "customer_profile": {
      "company_name": "Acme Corp",
      "industry": "manufacturing",
      "employee_count": 850,
      "annual_revenue": 45000000
    },
    "billing_details": {
      "billing_contact": "finance@acmecorp.com",
      "payment_terms": "net_30",
      "currency": "USD"
    }
  }
}
```

`Idempotency-Key` 標頭確保網路重試不會建立重複的入職嘗試。

### 19.2 入口與風險分類

**入口＋風險路由器**接收請求並執行一次分類：

1. 解析傳入的載荷。
2. 對照已知風險指標檢查客戶資料（產業、管轄區、規模、法規風險）。
3. 指派風險等級：`low`、`medium`、`high` 或 `critical`。
4. 記錄分類決定。

對 Acme Corp，路由器將請求分類為 `medium` 風險：這是一家標準管轄區內的成熟製造公司，沒有法
規旗標，合約金額中等。風險等級被寫入審計日誌並附加到工作流程運行記錄。

### 19.3 協調器交接

**業務協調器**接收分類後的請求，並載入 `wf_customer_onboarding_v12` 的工作流 DNA。協調器：

1. 驗證前置條件：合約狀態為 `signed`，且客戶風險分數低於閾值。
2. 初始化一筆新的 `WorkflowRun` 記錄，狀態 `queued`。
3. 將運行排入工作者佇列。
4. 將運行 ID 連同一個串流 URL 回傳給呼叫者。

### 19.4 逐步執行

工作者取出運行，開始執行 DNA 步驟。

**步驟 1：驗證合約**

- 代理：`quality_compliance_agent`
- 工具：`contract_parser`、`policy_retriever`
- 動作：
  - 解析已簽署的 PDF 並萃取關鍵條款。
  - 從知識庫檢索合約規則（第 0 層向量搜索）。
  - 檢查非標準條款、不尋常的責任條款和缺失部分。
  - 將合約與 `business/experts/decision-requirement-cards/` 中的決策需求卡比較。
- 結果：合約含一條標準責任條款，無紅旗。代理記錄信心分數 `0.91`，並記錄驗證決定。
- 記憶寫入：事件日誌條目、決策記憶記錄。

**步驟 2：建立客戶記錄**

- 代理：`execution_agent`
- 工具：`crm`
- 動作：
  - 在 CRM 系統建立一筆新客戶記錄。
  - 將已簽署的合約連結到客戶資料。
  - 將客戶狀態設為 `onboarding_in_progress`。
- 結果：客戶記錄 `CUST-2026-7842` 建立成功。
- 記憶寫入：事件日誌條目、語義記憶更新（客戶已存在）。
- 護欄檢查：這個動作是可逆的（記錄可被停用），所以對中等風險客戶不需要人類批准。

**步驟 3：配置帳務**

- 代理：`finance_ops_agent`
- 工具：`billing_system`
- 動作：
  - 以提供的付款條件建立帳務帳戶。
  - 生成初始發票排程。
  - 依客戶管轄區配置稅務設定。
- 結果：帳務帳戶 `BA-2026-3291` 配置完成，net-30 條件、USD 貨幣。
- 記憶寫入：事件日誌條目、程序記憶（帳務配置流程）。

**步驟 4：寄送歡迎包**

- 代理：`communications_agent`
- 工具：`email`
- 動作：
  - 從 `business/distilled/playbooks/` 取回歡迎包範本。
  - 以客戶特定詳情個人化電子郵件。
  - 將電子郵件排入寄送佇列。
- 護欄檢查：寄送外部電子郵件是不可逆動作。護欄指定
  `human_approval_required_if: tool_action_is_irreversible == true`。工作流程暫停於
  `waiting_for_approval`。
- 記憶寫入：事件日誌條目、審批請求建立。

### 19.5 人類關卡

建立一筆審批請求：

```yaml
approval_request:
  id: "apr_20260708_welcome_001"
  workflow_run_id: "wr_20260708_onboarding_001"
  step_id: "send_welcome_packet"
  risk_tier: "medium"
  context:
    customer_name: "Acme Corp"
    email_recipient: "contact@acmecorp.com"
    email_subject: "Welcome to Our Platform"
    preview_url: "/api/v1/approvals/apr_20260708_welcome_001/preview"
  created_at: "2026-07-08T14:30:00Z"
  status: "pending"
```

被指派的審閱者收到通知。審閱者：

1. 在前端開啟審批頁面。
2. 審查客戶資料、合約驗證結果，以及草稿歡迎電子郵件。
3. 點擊**批准**，附上選用備註：「標準歡迎包，看起來沒問題。」

工作者恢復、寄出電子郵件，並把步驟標記為完成。

### 19.6 驗證與完成

所有步驟完成後，協調器執行驗證檢查：

- ✅ CRM 記錄已建立
- ✅ 帳務配置已驗證
- ✅ 歡迎包已寄出
- ✅ 審計日誌完整

工作流程運行被標記為 `completed`。最終輸出被寫入：

```json
{
  "status": "completed",
  "customer_id": "CUST-2026-7842",
  "billing_account_id": "BA-2026-3291",
  "welcome_email_sent": true,
  "completed_at": "2026-07-08T14:45:00Z",
  "total_cycle_time_minutes": 15
}
```

### 19.7 評估與記憶

評估線束把完成的運行拿去對回歸測試套件執行：

- 品質分數：`0.94`
- 合規通過率：`1.0`
- 週期時間：`15 分鐘`（低於 30 分鐘目標）
- 人類升級率：`0.25`（四步一次審批）

所有指標都落在可接受範圍內。評估結果存於 `business/evals/benchmark-results/`。

記憶被更新：

- **事件記憶**：每一個動作的完整審計追蹤。
- **語義記憶**：「Acme Corp 是製造業的活躍客戶。」
- **程序記憶**：入職工作流程成功完成，含一次人類關卡。
- **決策記憶**：審閱者以標準備註批准了歡迎電子郵件。

### 19.8 演化考量

演化沙盒觀察已完成的運行。週期時間為 15 分鐘——遠低於目標。未偵測到瓶頸。工作流程在可接受
參數內運作，所以不提出變體。

如果週期時間顯著高於目標，或人類升級率異常高，演化引擎可能會提出一個變體：對低風險客戶預先
批准標準歡迎電子郵件。那個變體接著會進入沙盒管線：生成、測試、跑對抗檢查、與基線比較，並只
在人類簽核後才推廣。

---

## 20. 操作指南：常見任務

這一章提供最常見操作的實用配方。

### 20.1 新增一個工作流程

1. 在 `business/evolution/workflow-dna/` 建立一份工作流 DNA 檔案：

   ```yaml
   workflow_dna:
     id: "wf_invoice_processing_v1"
     name: "Invoice Processing"
     domain: "finance"
     objective: "Process incoming invoices with appropriate approvals."
     owner: "finance_ops_agent"
     version: "1.0"
     inputs: ["invoice_document", "vendor_profile"]
     preconditions:
       - "invoice_format == valid"
     steps:
       - id: "extract_invoice_data"
         agent: "finance_ops_agent"
         tools: ["invoice_parser"]
       - id: "match_purchase_order"
         agent: "finance_ops_agent"
         tools: ["erp"]
       - id: "route_for_approval"
         agent: "governance_officer"
         tools: ["approval_system"]
     memory_reads: ["vendor_history", "approval_rules"]
     memory_writes: ["event_log", "decision_memory"]
     guardrails:
       human_approval_required_if:
         - "invoice_amount > 10000"
         - "vendor_risk_tier == high"
     verification:
       required_checks:
         - "invoice_recorded_in_erp"
         - "approval_obtained"
     rollback:
       reversible: true
       rollback_steps: ["void_invoice_entry", "notify_ap_team"]
     fitness_metrics:
       - "processing_time"
       - "approval_accuracy"
       - "vendor_satisfaction"
   ```

2. 驗證 schema：

   ```bash
   npm run business:validate
   ```

3. 在後端註冊工作流程：

   ```python
   from app.domain.workflows import WorkflowService

   workflow_service = WorkflowService()
   workflow_service.register_workflow("wf_invoice_processing_v1")
   ```

4. 在 `business/evals/golden-tasks/invoice-processing/` 建立金任務。

5. 執行評估線束：

   ```bash
   npm run business:eval
   ```

### 20.2 捕捉專家知識

1. 安排與一位領域專家進行關鍵決策訪談。

2. 使用關鍵決策方法進行訪談：

   - 找出專家曾做過的一個特定高風險決策。
   - 探究他們注意到的線索、考慮過的替代方案，以及選擇背後的推理。
   - 記錄例外條件和紅旗。

3. 在 `business/experts/decision-requirement-cards/` 建立一張決策需求卡：

   ```yaml
   decision_requirement:
     id: "drc_payment_exception_001"
     domain: "accounts_payable"
     decision_point: "approve_rush_payment"
     expert_sources: ["senior_ap_manager"]
     context_signals: ["vendor_relationship", "payment_amount", "due_date"]
     cues_experts_notice:
       - "Vendor is a critical supplier with history of on-time delivery."
       - "Rush is due to internal processing delay, not vendor fault."
     normal_action: "process_through_standard_workflow"
     exception_paths:
       - condition: "critical_supplier AND internal_delay_confirmed"
         action: "expedite_with_oversight"
     red_flags: ["vendor_has_pending_disputes", "rush_requested_by_unknown_contact"]
     required_evidence: ["vendor_payment_history", "internal_delay_documentation"]
     risk_tier: "medium"
     human_approval_required: true
     validation_tests:
       - "Does recommendation match senior AP manager on historical rush payments?"
     confidence: 0.85
     last_reviewed: "2026-07-08"
   ```

4. 驗證卡片：

   ```bash
   npm run business:validate
   ```

5. 把卡片加入知識蒸餾佇列，以轉換為工作流程規則。

### 20.3 提出一個工作流程變體

1. 透過瓶頸分析或人類回饋找出改進機會。

2. 在 `business/evolution/workflow-dna/wf_variant_proposal.yaml` 記錄建議變更。

3. 執行演化沙盒檢查：

   ```bash
   npm run business:evolution:check
   ```

4. 沙盒會：
   - 生成變體。
   - 對著金任務測試。
   - 執行安全與對抗測試。
   - 與基線比較。
   - 若風險等級需要則請求人類審查。

5. 若獲批准，變體進入金絲雀部署，部署到有限範圍。

6. 在金絲雀期間監控指標。

7. 依結果推廣、回滾或退役。

### 20.4 回應安全事件

1. 透過監控、警報或人類報告識別事件。

2. 觸發**事件指揮官**代理。

3. 遵循事件響應執行手冊：

   ```text
   1. 遏制：隔離受影響系統，撤銷被洩漏的憑證。
   2. 溝通：通知利害關係人，開始事件日誌。
   3. 調查：判斷根本原因、影響範圍與爆炸半徑。
   4. 補救：套用修復、修補弱點、更新控制。
   5. 恢復：恢復服務、驗證完整性。
   6. 事後分析：記錄經驗教訓、更新安全控制。
   ```

4. 在 `business/security/incident-reports/` 建立事件報告。

5. 視需要更新威脅模型和安全控制。

### 20.5 審計一筆已完成的工作流程運行

1. 在前端前往審計日誌頁面：`/app/audit-logs`。

2. 依工作流程運行 ID 或日期範圍篩選。

3. 審查完整的事件追蹤：

   - 誰發起了這次運行？
   - 執行了哪些步驟？
   - 做了哪些決策？
   - 是否有任何人工批准？
   - 最終結果為何？

4. 匯出審計日誌以供合規報告。

5. 若偵測到異常，觸發治理審查。

---

## 21. 90 天部署計劃

這一節提供部署通用群體業務作業系統的分階段方法。

### 21.1 第一階段：基礎建設（第 1–14 天）

**目標：**

- 建立技術基礎。
- 部署核心基礎設施。
- 初始化治理產物。

**關鍵活動：**

| 天 | 活動 |
|---|---|
| 1–2 | 執行 `npm run bootstrap`，驗證所有驗證檢查通過。 |
| 3–4 | 配置後端資料庫、佇列和向量儲存。 |
| 5–6 | 將 FastAPI 後端部署到目標環境。 |
| 7–8 | 部署 Next.js 前端。 |
| 9–10 | 完成 AI 清單與用例風險分級。 |
| 11–12 | 定義人類審批政策。 |
| 13–14 | 建立審計日誌與監控。 |

**交付物：**

- 運行中的後端與前端。
- 已完成的 `business/governance/ai-inventory/`。
- `business/governance/use-case-risk-tiering/risk-tiers.json` 中的風險等級定義。
- `business/governance/human-approval-policy/policy.md` 中的人類審批政策。
- 審計日誌基礎設施運作中。

### 21.2 第二階段：影子學習（第 15–30 天）

**目標：**

- 開始捕捉真實營運資料。
- 進行專家訪談。
- 開始建立知識庫。

**關鍵活動：**

| 天 | 活動 |
|---|---|
| 15–17 | 為選定流程啟用影子模式。 |
| 18–20 | 配置從關鍵系統（CRM、ERP、電子郵件）捕捉事件日誌。 |
| 21–23 | 與領域專家進行關鍵決策訪談。 |
| 24–26 | 建立前 10 張決策需求卡。 |
| 27–28 | 將基礎文件攝入知識庫。 |
| 29–30 | 以測試查詢驗證檢索堆疊。 |

**交付物：**

- 事件日誌流入 `business/process-intelligence/event-logs/`。
- `business/experts/decision-requirement-cards/` 中至少 10 張決策需求卡。
- 初始知識庫已填入規則、SOP 與最佳實踐。
- 檢索準確度高於定義的閾值。

### 21.3 第三階段：受控副駕駛（第 31–60 天）

**目標：**

- 部署第一批有邊界工作流程。
- 為低風險與中風險任務啟用副駕駛模式。
- 建立評估基線。

**關鍵活動：**

| 天 | 活動 |
|---|---|
| 31–35 | 設計並驗證第一個工作流 DNA（例如客戶入職）。 |
| 36–40 | 以第 1 級（建議）自主部署工作流程到生產。 |
| 41–45 | 為工作流程建立金任務與回歸測試。 |
| 46–50 | 在成功評估後，逐漸將自主提升到第 2 級（起草）。 |
| 51–55 | 為中風險流程部署額外工作流程。 |
| 56–60 | 建立評估節奏與報告。 |

**交付物：**

- 至少三個工作流程在第 1–2 級自主下運行於生產。
- 評估線束每週運行。
- 回歸測試套件對已部署工作流程覆蓋率 >90%。
- 人類升級率在目標範圍內。

### 21.4 第四階段：演化沙盒（第 61–90 天）

**目標：**

- 啟動演化引擎。
- 開始系統性地改進工作流程。
- 將選定工作流程移到第 3 級自主。

**關鍵活動：**

| 天 | 活動 |
|---|---|
| 61–65 | 啟動演化沙盒。 |
| 66–70 | 生成並測試第一批工作流程變體。 |
| 71–75 | 在人類審查後推廣成功變體。 |
| 76–80 | 將已證實的工作流程自主提升到第 3 級（執行可逆）。 |
| 81–85 | 擴充監控以納入演化指標。 |
| 86–90 | 進行全面系統審查並規劃下一季。 |

**交付物：**

- 演化引擎以沙盒模式運行。
- 至少一個工作流程變體被推廣到生產。
- 選定工作流程在第 3 級自主下運作。
- 涵蓋全部六層的完整指標儀表板。
- 含經驗教訓與下一步的季度審查文件。

### 21.5 成功標準

到 90 天結束時，系統應達成：

| 指標 | 目標 |
|---|---|
| 引導驗證 | 所有檢查通過 |
| 事件日誌捕捉 | 來自至少 3 個系統、超過 10,000 個事件 |
| 決策需求卡 | ≥10 個已記錄的高風險決策 |
| 生產中的工作流程 | ≥3 個在第 1–2 級，1 個在第 3 級 |
| 評估覆蓋率 | 對已部署工作流程 >90% |
| 人類升級率 | 低風險工作流程 <25% |
| 週期時間改善 | 至少一個流程有可量化的改善 |
| 安全事件 | 零關鍵事件 |
| 審計完整性 | 100% 動作已記錄且可追溯 |

---

## 22. 詞彙表

**代理（Agent）**
在工作流程圖內執行特定任務的專門軟體組件。代理在有邊界權限內運作，並受治理控制約束。

**審計日誌（Audit Log）**
系統中所有動作、決策與事件的只能附加記錄。審計日誌提供可追溯性，對合規與除錯不可或缺。

**自主梯（Autonomy Ladder）**
根據累積證據，授予工作流程遞增自主等級的六級系統：第 0 級（觀察）到第 5 級（受限）。

**爆炸半徑（Blast Radius）**
一個被攻陷或失靈代理的潛在影響範圍。爆炸半徑控制限制了代理能存取或修改什麼。

**有邊界狀態圖（Bounded State Graph）**
工作流經預定義狀態、具明確過渡、權限與人類關卡的執行模型——有別於自由形式、無約束的代理
行為。

**業務協調器（Business Orchestrator）**
路由工作、管理全域狀態，並協調六個架構層的控制代理。

**金絲雀部署（Canary Deployment）**
一種部署策略，新變體先發布給一小群用戶或案例，再做全面推出，以便監控並快速回滾。

**決策需求卡（Decision Requirement Card）**
對一個高風險決策點的結構化記錄，捕捉專家注意到的線索、正常動作、例外路徑、紅旗，以及所需
證據。

**評估線束（Evaluation Harness）**
對代理、工作流程與提示執行金任務、回歸測試、對抗測試與歷史重放集的系統。

**演化沙盒（Evolution Sandbox）**
一個隔離環境，演化管理器在其中於任何生產部署之前提出、測試並驗證工作流程變體。

**適應度函數（Fitness Function）**
用來依品質、安全、合規、效率、人類滿意度與成本為工作流程變體評分的明確加權函數。

**金任務集（Golden Task Set）**
一組策展過、具代表性的任務，用來評估代理與工作流程效能。

**治理官（Governance Officer）**
負責套用風險等級、審批規則與審計要求的代理。

**護欄（Guardrails）**
工作流 DNA 中定義的約束，指定何時需要人類批准、哪些動作被禁止，以及哪些條件觸發升級。

**人類關卡（Human Gate）**
工作流程中的一個檢查點，必須有人類批准，執行才能繼續。

**混合記憶（Hybrid Memory）**
具八種類型的差異化記憶系統：事件、情節、語義、程序、決策、例外、評估與來源。

**幂等性金鑰（Idempotency Key）**
API 請求中包含的唯一識別碼，用來防止重試時的重複操作。

**事件指揮官（Incident Commander）**
負責處理失敗、協調回滾並主持事後分析的代理。

**間接提示注入（Indirect Prompt Injection）**
一種攻擊，惡意指令被嵌入在檢索到的內容（文件、電子郵件、資料庫記錄）中，LLM 隨後把它們解
讀為命令。

**知識蒸餾（Knowledge Distillation）**
把原始材料（文件、事件日誌、專家訪談）轉換成結構化規則、技能、工作流程與手冊的過程。

**LightRAG**
一個以圖為基礎、具雙層檢索與增量更新的文字索引，用作關係推理查詢的第 1 層檢索層。

**記憶中毒（Memory Poisoning）**
一種攻擊，對抗性內容被注入記憶系統，以影響未來的代理行為。

**流程智慧（Process Intelligence）**
透過流程挖掘、任務挖掘與合規檢查，從事件日誌中發現真實工作流程的層。

**來源追溯（Provenance）**
把每一條規則、決策與記憶追蹤回其來源文件、專家或事件日誌。

**ReAct**
一種推理與行動模式，模型在單一執行步驟內交錯思考、動作與觀察。

**風險等級（Risk Tier）**
與一個工作流程、動作或決策相關的風險等級分類：low、medium、high 或 critical。

**回滾計劃（Rollback Plan）**
在一個動作失敗或產生不良結果時，用來逆轉該動作的一系列已記錄步驟。

**影子模式（Shadow Mode）**
一種觀察模式，代理觀看人類專家執行工作並記錄其動作，但不採取任何自主動作。

**SSE（伺服器傳送事件，Server-Sent Events）**
一種從後端把即時更新串流到前端的協定，用於工作流程運行進度。

**分層檢索（Tiered Retrieval）**
成本分層的檢索堆疊：第 0 層（向量搜索）、第 1 層（LightRAG 圖）、第 2 層（階層式摘要），
外加一個始終在線的來源層。

**工具權限經紀人（Tool Permission Broker）**
為每個任務的工具存取授予狹窄、臨時、範圍化憑證的代理。

**工作流 DNA（Workflow DNA）**
一個工作流程的完整、自我描述契約，包括步驟、代理、工具、記憶存取、護欄、驗證、回滾與適應
度指標。

**工作流程運行（WorkflowRun）**
一個工作流程的單次執行實例，有它自己的輸入、狀態與輸出。

---

## 23. 參考資料

### 標準與框架

- **NIST AI 風險管理框架（AI 100-1）**。美國國家標準與技術研究院，2023 年。
  https://www.nist.gov/itl/ai-risk-management-framework

- **ISO/IEC 42001:2023**。人工智慧——管理系統。國際標準化組織，2023 年。
  https://www.iso.org/standard/42001

- **歐盟 AI 法案**。第 2024/1689 號法規，制定人工智慧調和規則。歐洲議會與理事會，2024 年。
  https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

- **OWASP LLM 應用程式 2025 年十大風險**。開放全球應用安全專案。
  https://genai.owasp.org/

- **OWASP 代理應用程式 2026 年十大風險**。開放全球應用安全專案。
  https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

### 學術參考

- Amershi, S. 等人。"Guidelines for Human-AI Interaction." CHI 2019.
  https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/

- Hoffman, R. R., Crandall, B., & Shadbolt, N. "Use of the Critical Decision Method to Elicit
  Expert Knowledge: A Case Study in the Methodology of Cognitive Task Analysis." Human Factors,
  1998.

- Park, J. S. 等人。"Generative Agents: Interactive Simulacra of Human Behavior." UIST 2023.
  https://arxiv.org/abs/2304.03442

- Yao, S. 等人。"ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023.
  https://arxiv.org/abs/2210.03629

- Lewis, P. 等人。"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS
  2020. https://arxiv.org/abs/2005.11401

- Liu, X. 等人。"AgentBench: Evaluating LLMs as Agents." ICLR 2024.
  https://arxiv.org/abs/2308.03688

- Agrawal, A. 等人。"GEPA: Generative Evolution of Prompted Agents." 2024.
  https://arxiv.org/abs/2404.06065

### 流程挖掘

- IEEE 流程挖掘任務小組。"Process Mining Manifesto." 2011.
  https://www.win.tue.nl/ieeetfpm/doku.php?id=shared:process_mining_manifesto

### LightRAG 與檢索

- LightRAG：Simple and Fast Retrieval-Augmented Generation.
  https://github.com/HKUDS/LightRAG

- RAPTOR：Recursive Abstractive Processing for Tree-Organized Retrieval.
  https://arxiv.org/abs/2401.18059

### 平台參考

- AnythingLLM. https://useanything.com/

- RAGFlow. https://ragflow.io/

- Model Context Protocol. https://modelcontextprotocol.io/

- Trae IDE 文件. https://docs.trae.ai/

### 本專案來源真相（Repository）

- 架構：`structure.md`、`structure_hk.md`；SDD `planning/structure/`；gap
  `planning/gap_analysis_for_structure.md`
- 後端：`backend.md`、`backend_hk.md`；SDD `planning/backend/`（BE-01…24）；gap
  `planning/gap_analysis_for_backend.md`；手冊 `book/book.backend_hk.md`
- 前端：`frontend.md`、`frontend_hk.md`；SDD `planning/frontend/`（FE-01…20）；gap
  `planning/gap_analysis_for_frontend.md`；手冊 `book/book.frontend_hk.md`
- 延續：`status.md`、`memory/handoff.md`、`mark_100_verification.md`、
  `reviews/e1_operator_checklist.md`

---

*全書完*

---

