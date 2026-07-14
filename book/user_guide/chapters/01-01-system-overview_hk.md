# 第 01-01 章：系統概覽

![System Architecture](../assets/01-01-system-architecture.svg)

## 學習目標

在完成本章後，你將能夠：

1. 描述 Generic Swarm 商業作業系統的六層架構
2. 解釋設計優先層級（安全性 > 可審計性 > 正確性 > 效率 > 自主性）
3. 識別核心概念：Workflow DNA、有界自主、沙箱演化及來源追蹤
4. 理解 Intake Router 及 Business Orchestrator 如何協調工作
5. 將每個架構層對應到其在系統中的角色
6. 闡述為何自主權是透過證據獲得而非預設授予

## 先決條件

- 對軟件架構概念（層次、服務、API）有基本了解
- 熟悉多代理系統的概念（有幫助但非必須）
- 可存取已克隆的 `generic-swarm-ops` 倉庫副本

---

## 1. 什麼是 Generic Swarm 商業作業系統？

Generic Swarm 商業作業系統是一個受治理的、自我改進的多代理系統，旨在：

1. **學習**業務實際如何運作 -- 從文件、專家以及真實事件日誌中學習
2. **提煉**該知識為可重用的規則、技能、工作流程及操作手冊
3. **執行**透過有界、可審計的代理工作流程完成工作
4. **演化**在沙箱中改進這些工作流程 -- 永不直接在生產環境中修改

> **注意：** 這不是聊天機械人或簡單的自動化工具。它是一個完整的業務流程作業系統，具備內建的治理、安全及自我改進能力。

本系統專為需要自動化複雜業務流程的組織而設計，同時保持完整的可審計性、符合法規（包括歐盟 AI 法案）及在關鍵決策點的人工監督。

---

## 2. 設計優先層級

系統遵循嚴格的優先順序來指導每一個設計決策：

```
Safety > Auditability > Correctness > Efficiency > Autonomy
```

| 優先級 | 排名 | 含義 |
|----------|------|---------|
| **安全性** | 第一 | 系統絕不可造成傷害。不可逆操作需要人工審批。每條執行路徑都有回滾計劃。 |
| **可審計性** | 第二 | 每個操作、決策及資料存取都記錄了完整的來源追蹤。無黑箱。 |
| **正確性** | 第三 | 輸出必須準確且有證據支持。幻覺被視為故障。 |
| **效率** | 第四 | 系統應快速且具成本效益，但絕不以犧牲安全性或正確性為代價。 |
| **自主性** | 第五 | 代理只有在透過證據及評估獲得信任後才能獨立行動。 |

> **警告：** 自主性始終是*最低*優先級。系統的設計使得自主行動是按工作流程透過證據獲得的 -- 絕不預設授予。如果效率與安全性之間發生衝突，安全性始終優先。

### 2.1 為何此排序重要

在實踐中，此優先層級意味着：

- 一個可以透過跳過人工閘門來更快執行的工作流程，如果操作是不可逆的，則*不會*跳過（安全性 > 效率）
- 一個產生正確結果但沒有審計軌跡的代理被視為*有缺陷的*（可審計性 > 無審計的正確性）
- 一個完全自主但無法透過評估結果證明其可靠性的代理將被限制在「建議」模式（安全性 > 自主性）

---

## 3. 六層架構

系統分為六個功能層，每層都有明確的職責。所有六層在 Business Orchestrator 的協調下共同運作。

### 3.1 流程智能層

**目的：** 從實際運營軌跡中學習，而不僅僅是從文件和訪談中學習。

流程智能層透過分析事件日誌、工單、CRM/ERP 操作、日曆事件、審批及完成記錄來發現工作實際如何進行。這為工作流程優化提供了實證基礎。

**關鍵代理：**
- **Process Miner Agent** -- 從事件日誌中發現真實工作流程
- **Task Mining Agent** -- 在許可的情況下觀察 UI/人工層面的步驟
- **Conformance Agent** -- 比較實際工作與已記錄的 SOP
- **Bottleneck Analyzer** -- 發現延遲、循環、返工及交接失敗
- **Causal Improvement Agent** -- 提出可能改善結果的干預措施

**制品位置：** `business/process-intelligence/`

```text
business/process-intelligence/
  event-logs/           # 原始運營事件資料
  discovered-processes/ # 已探勘的工作流程模型
  conformance-reports/  # SOP 與實際比較
  bottlenecks/          # 已識別的延遲及循環
  causal-hypotheses/    # 提議的改進措施
```

### 3.2 知識層

**目的：** 儲存、組織及檢索所有業務知識，並具備完整的來源追蹤。

知識層維護一個分層檢索系統，結合向量搜尋、基於圖的推理及層次化摘要。它支持八種不同的記憶類型來處理全方位的業務知識。

**記憶類型：**

| 記憶類型 | 儲存內容 | 範例 |
|---|---|---|
| Event | 原始運營日誌 | 「代理在上午 9:42 發送了發票。」 |
| Episodic | 案例敘述 | 「這次續約差點失敗 -- 法務介入太晚了。」 |
| Semantic | 事實/規則 | 「超過 25 萬的企業合約需要法務審查。」 |
| Procedural | 技能/工作流程 | 「如何為新客戶進行入職。」 |
| Decision | 決策 + 原因 | 「我們批准了例外 X 因為 Y。」 |
| Exception | 邊緣案例 | 「如果供應商在 Z 地區，使用替代流程。」 |
| Evaluation | 測試結果 | 「Workflow v12 未通過隱私測試。」 |
| Provenance | 來源歸屬 | 「規則來自 SOP v4 及專家 Alice。」 |

**檢索層級：**

- **Tier 0（預設，最便宜）：** 向量搜尋/關鍵字 + 雜湊嵌入。處理 80%+ 的查詢。
- **Tier 1（關係推理）：** LightRAG-lite 圖層配合實體多跳。回答「誰處理了這個案例，順序如何？」
- **Tier 2（全域綜合，按需）：** RAPTOR 風格的層次化摘要。僅用於全語料庫問題。

**升級規則：** 從 Tier 0 開始，僅當查詢需要關係/多跳時升級到 Tier 1，僅用於全域綜合時升級到 Tier 2。

**制品位置：** `business/knowledge-base/`

### 3.3 執行層

**目的：** 運行由 Workflow DNA 定義的有界、可審計的代理工作流程。

執行層使用有界狀態圖（而非自由形式的集群）來控制工作流程執行。每個步驟都有明確的代理、工具、權限及驗證要求。工具會留下持久的 `tool_effects` 用於審計及回滾。

**執行模式：**
```text
Event -> Intake Router -> Risk Classifier -> Orchestrator
  -> [Research] -> [Execution] -> [Verification] -> [Compliance]
  -> [Human Gate] -> Audit Log + Memory Write
  -> Evaluation -> Evolution Sandbox
```

**核心概念：Workflow DNA**

每個工作流程都由一個 Workflow DNA 文件定義，該文件聲明：
- 具有明確代理及工具的有界步驟
- 記憶讀取及寫入（有範圍限制）
- 護欄（人工審批條件）
- 驗證 required_checks
- 回滾計劃（可逆性）
- 適應度指標及審計日誌寫入要求

**制品位置：** `business/evolution/workflow-dna/`

### 3.4 演化層

**目的：** 在沙箱中提出並測試改進措施，絕不直接修改生產環境。

> **警告：** Evolution Manager 絕不可直接修改生產環境。
> 它只可以：提出變體、在沙箱中測試、與基線比較、請求審批、金絲雀部署，以及在失敗時自動回滾。

演化層實施受控的改進流程：

1. 觀察生產/影子軌跡
2. 偵測故障、瓶頸或機會
3. 生成變體（提示詞/工作流程/工具使用/角色變更）
4. 離線測試對比黃金任務
5. 執行安全 + 對抗性測試
6. 執行合規檢查
7. 在歷史案例上重放（模擬）
8. 如風險等級要求則進行人工審查
9. 金絲雀部署到小範圍
10. 監控指標
11. 提升/回滾/退役
12. 將教訓存入演化記憶

**適應度函數：**

```
F = w_q*Q + w_s*S + w_c*C + w_e*E + w_h*H - w_r*R - w_l*L - w_k*K
```

其中：Q=品質，S=安全性，C=合規性，E=效率，H=人工滿意度，R=風險懲罰，L=延遲懲罰，K=成本懲罰。

**制品位置：** `business/evolution/`

### 3.5 治理層

**目的：** 對所有操作施加風險分層、審批規則及審計要求。

治理層實施與 NIST AI RMF、ISO/IEC 42001 及歐盟 AI 法案要求一致的分層自主模型。

**自主權風險等級：**

| 等級 | 自主級別 | 允許的行為 |
|---|---|---|
| 0 | 觀察 | 僅記錄及摘要 |
| 1 | 建議 | 提出建議；人工執行 |
| 2 | 草擬 | 準備制品；人工在發送/執行前審批 |
| 3 | 執行（可逆） | 如存在回滾且風險低則可行動 |
| 4 | 執行 + 閘門 | 可行動，但人工審批關鍵步驟 |
| 5 | 受限 | 在存在保證案例之前不可自主行動 |

**強制治理制品：**
- AI 清單
- 用例風險分層
- 人工審批策略
- 審計日誌
- 事件回應計劃
- 回滾計劃
- 資料保留策略
- 模型卡片
- 保證案例

**制品位置：** `business/governance/`

### 3.6 安全層

**目的：** 對抗性測試、威脅建模及爆炸半徑控制。

安全層同時涵蓋 OWASP LLM 應用程式 Top 10（2025）及 OWASP 代理應用程式 Top 10（2026）。主要威脅模型認知到間接提示詞注入無法完全防止 -- 因此爆炸半徑控制至關重要。

**關鍵控制措施：**
- **Tool Permission Broker** -- 每個任務的窄範圍、臨時、有限定的憑證
- **記憶中毒防禦** -- 對高影響記憶寫入的來源追蹤 + 人工審查
- **技能/插件審查** -- 第三方代理技能經掃描及固定
- **完全可觀察性** -- 跨模型調用、工具調用、代理間流量的單一審計軌跡
- **AI 事件回應** -- 針對 GenAI 特定事件的已定義操作手冊

**核心原則：** 系統提示詞不是安全控制措施。在 LLM 之外確定性地實施安全。

**制品位置：** `business/security/`

---

## 4. Intake Router 及 Business Orchestrator

### 4.1 Intake Router

進入系統的每個事件或請求都通過 Intake Router，它：

1. 分類傳入請求的風險級別
2. 確定適用哪個 Workflow DNA
3. 路由到適當的編排路徑
4. 施加初始安全篩選

路由器作為單一入口點，確保沒有請求能繞過治理或安全控制措施。

### 4.2 Business Orchestrator

Business Orchestrator 是中央協調者 -- 一個由 Postgres 控制平面支持的狀態圖控制器。它：

- 在六層之間路由工作
- 管理工作流程狀態轉換
- 實施人工在環閘門
- 透過權限代理協調工具存取
- 在工作流程完成後觸發評估及演化

**運行時持久化：** 編排器在 Postgres 的 `runtime_state` 表中使用 JSONB 文件儲存所有狀態。JSON 檔案備份（`backend/data/runtime.json`）用於種子/恢復目的。

```bash
# 健康檢查確認資料庫連接
curl http://127.0.0.1:8000/api/v1/health/ready
# 回應：{"database": "postgres", "status": "healthy"}
```

---

## 5. 核心概念

### 5.1 Workflow DNA

Workflow DNA 是定義可執行業務流程的核心抽象。每個 Workflow DNA 文件都是一個完整、自包含的規格，包括：

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
      agent: "governance_officer"
      tools: ["contract_parser", "policy_retriever"]
    - id: "create_customer_record"
      agent: "business_orchestrator"
      tools: ["crm"]
    - id: "configure_billing"
      agent: "tool_permission_broker"
      tools: ["billing_system"]
    - id: "send_welcome_packet"
      agent: "business_orchestrator"
      tools: ["email"]
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
    rollback_steps: ["disable_customer_record", "void_initial_invoice"]
  fitness_metrics:
    - "cycle_time"
    - "error_rate"
    - "customer_satisfaction"
    - "compliance_pass_rate"
```

> **提示：** 本系統中的旗艦工作流程是 `wf_customer_onboarding_v12`。在建立自己的工作流程之前，請研究其 DNA 定義以理解完整模式。

### 5.2 有界自主

有界自主意味着每個代理行動都有：
- 一個**風險等級**（0-5）決定所需的監督級別
- 一個**權限範圍**定義代理可以存取的工具及資料
- 一個**人工閘門**用於高風險或不可逆操作

系統拒絕任何缺少以下內容的 Workflow DNA：
- 高風險步驟的人工閘門
- 回滾計劃
- 來源文件
- 審計寫入步驟

### 5.3 沙箱演化

演化引擎在一個不可協商的規則下運作：它絕不可直接修改生產環境。所有改進都經過：

```text
Propose -> Test in sandbox -> Compare to baseline -> Request approval
  -> Canary deploy -> Auto-rollback on failure
```

這確保即使系統的自我改進能力也是安全且可審計的。

### 5.4 來源追蹤

每條規則、決策及記憶條目都可追溯到一個來源。來源追蹤層確保你始終可以回答：

- 這條規則從哪裡來的？（SOP 版本、專家訪談、事件日誌）
- 誰批准了這個決策？
- 什麼證據支持這個建議？
- 這個知識最後何時被驗證的？

---

## 6. 系統組件一覽

### 6.1 後端運行時

| 組件 | 位置 | 目的 |
|-----------|----------|---------|
| FastAPI 應用程式 | `backend/app/main.py` | 主應用程式、中間件、CORS |
| 運行時引擎 | `backend/app/runtime.py` | 受治理的執行、閘門、記憶 |
| 工具適配器 | `backend/app/infrastructure/tools/adapters.py` | 真實工具執行 + 效果 |
| 自我改進 | `backend/app/infrastructure/self_improvement/` | 反思、教訓、提議 |
| Loop engineering | `backend/app/infrastructure/loop_engineering/` | Loop DNA + 運行器 |
| 知識 | `backend/app/infrastructure/knowledge/` | 分層檢索 + 嵌入 |
| 知識編排 | `backend/app/infrastructure/knowledge_orchestration/` | K1-lite 圖操作 |
| 流程智能 | `backend/app/infrastructure/process_intelligence/` | PI 磁碟制品 |
| 演化 | `backend/app/infrastructure/evolution/` | 語料庫評估、變體 |

### 6.2 前端控制台

Next.js 操作控制台（位於 `http://localhost:3000/`）提供用於以下功能的網頁介面：

- 管理代理及工作流程
- 執行工作流程及監控執行情況
- 審批人工閘門步驟
- 檢視審計日誌及記憶
- 運行自我改進流程（反思、提議、評估、金絲雀）
- 瀏覽演化族群歸檔

### 6.3 業務制品層

```text
business/
  process-intelligence/   # 事件日誌 + PI 輸出
  knowledge-base/         # 規則、來源追蹤、檢索
  experts/                # 檔案、影子日誌、DRC
  materials/              # 文件、法規、SOP
  distilled/              # 技能、提示詞、工作流程
  memory/                 # 情節、語義、程序
  evals/                  # 黃金任務、回歸、對抗
  governance/             # 清單、模型卡片、風險等級
  security/              # 威脅模型、紅隊結果
  evolution/             # DNA、變體、教訓
```

---

## 7. 探索架構（逐步指引）

按照以下步驟在你自己的機器上探索系統架構：

### 步驟 1：檢閱架構來源文件

```bash
# 打開架構真相來源
cat structure.md | head -100
```

倉庫根目錄的 `structure.md` 檔案是權威的架構文件。它包含 600+ 行，涵蓋所有六層的詳細資訊。

### 步驟 2：檢查業務制品樹

```bash
# 列出頂層業務資料夾
ls business/
```

預期輸出：
```
evals/  evolution/  governance/  knowledge-base/  materials/
memory/  process-intelligence/  security/  experts/  distilled/
```

### 步驟 3：檢查後端 API 結構

```bash
# 檢視主 FastAPI 應用程式
cat backend/app/main.py | head -50
```

關鍵 API 路由組：
- `/api/v1/auth/` -- 認證端點
- `/api/v1/workflows/` -- 工作流程 CRUD 及執行
- `/api/v1/agents/` -- 代理管理
- `/api/v1/runs/` -- 運行監控
- `/api/v1/approvals/` -- 人工閘門管理
- `/api/v1/knowledge/` -- 知識檢索
- `/api/v1/memory/` -- 記憶存取
- `/api/v1/processes/` -- 流程智能
- `/api/v1/evolution/` -- 演化歸檔
- `/api/v1/improvement/` -- 自我改進 API
- `/api/v1/loops/` -- Loop 運行器
- `/api/v1/health/` -- 系統健康

### 步驟 4：檢查前端導航

```bash
# 列出前端應用頁面
ls frontend/src/app/
```

Next.js 應用路由器為每個主要系統功能（代理、工作流程、運行、審批、知識、評估、流程、演化）提供頁面。

### 步驟 5：驗證雙線束

```bash
# 檢查同步命令
npm run sync
```

雙線束為 Trae（`.trae/`）及 Grok Build（`.grok/`）開發環境生成受管理的代理/規則檔案。

---

## 8. 真實使用案例

### 使用案例 1：自動化客戶入職

**場景：** 一家 B2B SaaS 公司需要為企業客戶進行入職，包括合規檢查、合約驗證、帳單設定及歡迎通訊。

**系統如何處理：**

1. **流程智能層**探勘歷史入職事件日誌以發現實際執行的步驟（不僅是已記錄的 SOP）
2. **知識層**儲存合約規則、客戶例外及過往失敗
3. 一個 **Workflow DNA**（`wf_customer_onboarding_v12`）定義有界步驟：
   - 驗證合約（Governance Officer + contract_parser 工具）
   - 建立客戶記錄（Orchestrator + CRM 工具）
   - 配置帳單（Tool Permission Broker + billing_system）
   - 發送歡迎套件（Orchestrator + email 工具）
4. **治理層**在 risk_tier 高或偵測到合約例外時實施人工閘門
5. **演化層**透過分析週期時間、錯誤率及客戶滿意度分數持續改進工作流程

**結果：** 入職時間從數天縮短到數小時，同時保持完整的合規可審計性。人工專家僅在真正複雜的案例中介入。

### 使用案例 2：法規合規監控

**場景：** 一家金融服務公司需要追蹤不斷變化的法規（歐盟 AI 法案、ISO 42001）並確保所有 AI 驅動的流程保持合規。

**系統如何處理：**

1. **知識層**攝取法規文件並維護來源記錄
2. **治理層**將每個工作流程對應到適用法規及所需的風險評估
3. **Conformance Agent** 持續檢查實際操作是否符合已記錄的合規要求
4. 當法規變更時，**演化層**提出更新的工作流程變體，在部署前對合規要求進行測試
5. **審計日誌**為法規審計提供完整的可追溯性

**結果：** 公司在無需手動追蹤試算表的情況下維持持續合規。審計員可以將任何決策追溯到其法規依據及審批鏈。

### 使用案例 3：知識工作者增強

**場景：** 一家諮詢公司希望從資深顧問那裡擷取專家知識，並以結構化指導的形式提供給初級員工。

**系統如何處理：**

1. **Expert Shadow Agent** 觀察資深顧問（經許可）並記錄決策模式
2. **Cognitive Task Analyst** 將訪談轉化為決策需求卡片，記錄上下文信號、專家注意到的線索及例外路徑
3. **Knowledge Distiller** 將原始觀察轉化為儲存在 `business/distilled/` 中的可重用操作手冊及檢查清單
4. 初級顧問以**建議模式**（Tier 1）與系統互動，接收引用具體專家來源的建議
5. 隨着時間推移，當評估分數提高時，某些工作流程獲得更高的自主等級

**結果：** 機構知識被保存及可存取，而非鎖定在個別專家腦中。新員工在保持品質標準的同時更快上手。

---

## 9. 最佳實踐

### 架構理解

1. **始終從 `structure.md` 開始** -- 它是系統架構的唯一真相來源。所有其他文檔是精煉而非取代它。

2. **尊重優先層級** -- 在做設計決策時，始終檢查你的選擇是否與更高優先級的關注點衝突。安全性勝過一切。

3. **按層次思考** -- 每層都有明確的職責。抵制建立繞過層邊界的橫切功能的誘惑。

### 運營意識

4. **操作前檢查健康** -- 在運行工作流程之前始終驗證 `GET /api/v1/health/ready` 返回 `"database": "postgres"`。

5. **審閱治理制品** -- 在部署任何新工作流程之前，確保所有所需的治理制品已就位（`npm run business:governance`）。

6. **信任評估系統** -- 絕不提升未通過黃金任務評估、回歸測試及對抗性測試的工作流程變體。

### 開發心態

7. **證據優於意見** -- 系統從真實軌跡中學習，而非假設。在可用時始終以實際事件日誌資料為基礎進行更改。

8. **有界優於開放** -- 偏好明確、有界的工作流程而非開放式的代理自由。狀態圖實施安全；自由形式的集群則不會。

9. **始終有來源** -- 每條規則、決策或知識條目必須引用其來源。無文件記錄的知識是不受信任的知識。

---

## 10. 章節摘要

在本章中，你學到了：

- Generic Swarm 商業作業系統是一個受治理的、自我改進的多代理系統，從真實運營中學習、執行有界工作流程，並在沙箱中安全演化
- 設計優先層級（安全性 > 可審計性 > 正確性 > 效率 > 自主性）指導系統中的每個決策
- 六層協同運作：流程智能、知識、執行、演化、治理及安全
- Intake Router 及 Business Orchestrator 透過由 Postgres 支持的有界狀態圖協調所有工作
- Workflow DNA 定義了具備內建護欄、回滾計劃及適應度指標的完整、自包含的工作流程規格
- 自主權是透過證據（評估結果）獲得而非預設授予
- 演化引擎提出改進但絕不直接修改生產環境

---

## 11. 知識檢查問答

測試你對系統架構的理解：

**問題 1：** 系統中設計優先順序的正確排列是什麼？

a) 自主性 > 效率 > 正確性 > 可審計性 > 安全性
b) 安全性 > 可審計性 > 正確性 > 效率 > 自主性
c) 正確性 > 安全性 > 效率 > 可審計性 > 自主性
d) 安全性 > 正確性 > 可審計性 > 自主性 > 效率

<details>
<summary>答案</summary>
<b>b)</b> 安全性 > 可審計性 > 正確性 > 效率 > 自主性。
自主性始終是最低優先級，必須透過證據獲得。
</details>

---

**問題 2：** 哪一層負責透過分析事件日誌及運營軌跡來發現工作實際如何進行？

a) 知識層
b) 執行層
c) 流程智能層
d) 演化層

<details>
<summary>答案</summary>
<b>c)</b> 流程智能層。它使用流程探勘、任務探勘及合規性檢查從實際運營資料中學習，而非僅從已記錄的程序中學習。
</details>

---

**問題 3：** 演化引擎的不可協商規則是什麼？

a) 它必須始終改善效率指標
b) 它絕不可直接修改生產環境
c) 它必須每個週期生成至少 10 個變體
d) 它必須在無人工監督的情況下運行

<details>
<summary>答案</summary>
<b>b)</b> Evolution Manager 絕不可直接修改生產環境。它只可以提出變體、在沙箱中測試、與基線比較、請求審批、金絲雀部署，以及在失敗時自動回滾。
</details>

---

**問題 4：** 在哪個自主等級代理可以在無人工審批的情況下執行可逆操作？

a) Tier 0（觀察）
b) Tier 1（建議）
c) Tier 3（執行可逆）
d) Tier 5（受限）

<details>
<summary>答案</summary>
<b>c)</b> Tier 3（執行可逆）。在此等級，如果存在回滾且風險低，代理可以行動。更高風險的操作需要 Tier 4（執行 + 閘門）配合人工審批。
</details>

---

**問題 5：** 知識層中預設（最便宜）的檢索層級是什麼，它處理多少百分比的查詢？

a) Tier 1（圖層），處理 50% 的查詢
b) Tier 0（向量搜尋），處理 80%+ 的查詢
c) Tier 2（層次化摘要），處理 90% 的查詢
d) Tier 0（向量搜尋），處理 40% 的查詢

<details>
<summary>答案</summary>
<b>b)</b> Tier 0（向量搜尋/關鍵字 + 雜湊嵌入）是預設值並處理 80%+ 的查詢。系統僅在需要關係推理或全域綜合時升級到更高層級。
</details>

---

**問題 6：** 如果提交的 Workflow DNA 沒有回滾計劃會怎樣？

a) 它會帶警告運行
b) 它會被運行時拒絕
c) 它會在僅觀察模式下運行
d) 它會被自動分配一個回滾計劃

<details>
<summary>答案</summary>
<b>b)</b> 運行時拒絕沒有閘門、沒有回滾、缺少來源或沒有審計寫入的 DNA。這是由系統確定性地實施的，而非由 LLM。
</details>

---

**問題 7：** 哪個 Postgres 表儲存 Business Orchestrator 的運行時狀態？

a) `workflow_state`
b) `runtime_state`
c) `agent_state`
d) `orchestrator_log`

<details>
<summary>答案</summary>
<b>b)</b> <code>runtime_state</code> 表儲存代表完整編排器狀態的 JSONB 文件。位於 <code>backend/data/runtime.json</code> 的 JSON 檔案備份在資料庫為空時作為種子來源。
</details>

---

## 下一章

繼續閱讀[第 01-02 章：安裝先決條件](01-02-installation-prerequisites.md)以學習如何設定具備所有必需依賴項的開發環境。
