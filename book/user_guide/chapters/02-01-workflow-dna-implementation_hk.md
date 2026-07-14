# 第 2.1 章：工作流程 DNA 實作

![Workflow DNA Schema Structure](../assets/02-01-workflow-dna-structure.svg)

## 學習目標

完成本章後，你將能夠：

1. 理解完整的工作流程 DNA 結構及其組件
2. 使用受限狀態圖模型從零開始建立新的工作流程
3. 定義包含明確代理程式、工具、記憶體讀寫及防護機制的步驟
4. 配置驗證檢查、回復計劃及適應度指標
5. 使用專案內建的驗證工具檢驗工作流程 DNA
6. 應用正式環境工作流程定義的最佳實踐

## 先決條件

開始本章之前，請確保你已經：

- 完成本指南的第 1 節（核心系統基礎）
- 有一個正在運行的後端實例（`uvicorn app.main:app --reload`）
- 能夠存取 `business/` 目錄結構
- 熟悉 YAML 語法及狀態圖概念
- 已配置 Node.js 環境並完成 `npm run bootstrap`

---

## 甚麼是工作流程 DNA？

工作流程 DNA 是核心抽象概念，它捕捉在 Generic Swarm Business OS 中安全、可審計且正確執行業務流程所需的一切。不同於可能走向不可預測路徑的自由形式代理程式群組，工作流程 DNA 強制使用**受限狀態圖**，其中每個步驟、工具、記憶體存取和決策點都被明確宣告。

可以將工作流程 DNA 想像為業務流程的「遺傳密碼」：它編碼了管理工作執行方式的結構、約束、權限和品質指標。正如生物 DNA 包含建構有機體的指令，工作流程 DNA 包含執行業務工作流程的指令。

### 核心設計理念

系統遵循嚴格的設計優先順序：

1. **安全性** - 沒有適當的防護措施，任何操作都不會執行
2. **可審計性** - 每個操作都以完整的來源記錄
3. **正確性** - 驗證檢查確保正確執行
4. **效率** - 僅在安全性和正確性確立後才進行最佳化
5. **自主性** - 通過證據獲得，絕不預設授予

> **備註：** 自主性被刻意放在最後。系統必須先證明它能安全運作，才能獲得更大的獨立性。這通過風險等級系統（第 0-5 級）來強制執行。

---

## 工作流程 DNA 結構

每個正式環境的工作流程 DNA 必須宣告以下組件。讓我們使用旗艦工作流程 `wf_customer_onboarding_v12` 作為範例逐一說明。

### 1. 身份及元資料

```yaml
workflow_dna:
  id: "wf_customer_onboarding_v12"
  name: "Customer Onboarding"
  domain: "operations"
  objective: "Onboard customer with minimal delay and compliance risk."
  owner: "business_orchestrator"
  version: "12.0"
```

每個工作流程需要：

| 欄位 | 用途 | 範例 |
|-------|---------|---------|
| `id` | 帶版本後綴的唯一識別碼 | `wf_customer_onboarding_v12` |
| `name` | 人類可讀名稱 | `Customer Onboarding` |
| `domain` | 業務領域分類 | `operations`、`legal`、`finance` |
| `objective` | 工作流程目標的清晰陳述 | 自然語言目標 |
| `owner` | 負責編排的代理程式 | `business_orchestrator` |
| `version` | 用於變更追蹤的語義版本 | `12.0` |

> **提示：** 使用編碼版本的描述性 ID。這使得在審計日誌和演化歷史中容易識別正在運行的 DNA 版本。

### 2. 輸入及前置條件

```yaml
  inputs: ["signed_contract", "customer_profile", "billing_details"]
  preconditions:
    - "contract_status == signed"
    - "customer_risk_score <= threshold OR legal_approval == true"
```

輸入宣告工作流程在啟動前所需的資料。前置條件是布林表達式，必須在執行開始前評估為 `true`。如果任何前置條件失敗，工作流程將不會啟動。

### 3. 步驟（受限狀態圖）

步驟是工作流程 DNA 的核心。每個步驟宣告：

- 哪個**代理程式**負責執行
- 代理程式被允許使用哪些**工具**（且僅限那些工具）
- 步驟在狀態圖中的位置

```yaml
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
```

> **警告：** 代理程式只能使用在其步驟定義中明確列出的工具。任何嘗試使用未列出工具的行為都會被工具權限代理阻止。這是「最小權限」原則的實踐。

#### 狀態圖的運作方式

運行時預設按順序遍歷圖。每個步驟：

1. 接收當前工作流程狀態
2. 指定的代理程式使用允許的工具執行其工作
3. 工具呼叫產生持久的 `tool_effects` 記錄
4. 步驟報告其結果（成功/失敗）
5. 控制權傳遞到下一步驟（或在失敗時觸發回復）

```text
verify_contract --> create_customer_record --> configure_billing --> send_welcome_packet
                                                     |
                                              [HUMAN GATE]
                                          (approval required)
```

### 4. 記憶體讀取及寫入

```yaml
  memory_reads: ["contract_rules", "customer_exceptions", "past_failures"]
  memory_writes: ["event_log", "decision_memory", "lessons_learned"]
```

記憶體存取是有範圍且明確的：

- **memory_reads** - 工作流程在執行期間可以存取的資訊
- **memory_writes** - 工作流程在執行後將持久化的資訊
- **allowed_memory_scopes** - 運行時強制執行可存取的記憶體命名空間

運行時在每次讀寫操作中強制執行 `allowed_memory_scopes`。種子代理程式為旗艦入職路徑聯合 `organization_memory`。記憶體項目獨立於知識檢索攜帶來源資訊。

> **備註：** 自動反思的經驗教訓會寫入 `organization_memory` 和 `improvement_lessons`。這使得跨工作流程運行的持續學習成為可能。

### 5. 防護機制（人工審批條件）

```yaml
  guardrails:
    human_approval_required_if:
      - "risk_tier == high"
      - "contract_exception_detected == true"
      - "tool_action_is_irreversible == true"
```

防護機制定義了工作流程**必須暫停**並等待人工審批的條件。這是系統針對高風險操作的主要安全機制。

三個標準防護條件是：

1. **風險等級為高** - 整體工作流程或步驟被歸類為需要監督的風險級別
2. **偵測到例外** - 發現了意料之外的情況（例如非標準合約條款）
3. **不可逆操作** - 下一個工具呼叫無法撤銷（例如付款、帳單設定）

當任何防護條件被滿足時，運行時會建立一個**人工閘門**，阻止執行直到授權審查人員批准繼續。

### 6. 驗證（必要檢查）

```yaml
  verification:
    required_checks:
      - "crm_record_created"
      - "billing_config_validated"
      - "welcome_packet_sent"
      - "audit_log_complete"
```

驗證檢查確認工作流程正確完成。每項檢查代表對執行後系統狀態的可測試斷言。系統可以選擇性地使用 `block_on_fail` 來防止在任何檢查失敗時將運行標記為成功。

### 7. 回復計劃

```yaml
  rollback:
    reversible: true
    rollback_steps: ["disable_customer_record", "void_initial_invoice", "notify_ops_owner"]
```

每個工作流程必須宣告它是否可逆，如果可逆，需要哪些步驟來撤銷其效果。驗證器將拒絕任何以下情況的 DNA：

- 高風險操作缺少回復計劃
- 不可逆操作未被標記
- 回復步驟參考了工作流程不可用的工具

### 8. 適應度指標

```yaml
  fitness_metrics:
    - "cycle_time"
    - "error_rate"
    - "customer_satisfaction"
    - "compliance_pass_rate"
    - "human_escalation_rate"
    - "cost_per_case"
```

適應度指標定義了演化引擎如何評估工作流程效能。這些驅動用於變體選擇的適應度函數：

```
F = w_q*Quality + w_s*Safety + w_c*Compliance + w_e*Efficiency + w_h*Human_satisfaction
    - w_r*Risk_penalty - w_l*Latency_penalty - w_k*Cost_penalty
```

---

## 逐步指南：建立新的工作流程 DNA

按照以下編號步驟從零開始建立工作流程。

### 步驟 1：定義業務流程

在撰寫任何 YAML 之前，先記錄：

- 這個流程的目標是甚麼？
- 涉及的參與者（代理程式）是誰？
- 每個參與者需要甚麼工具？
- 決策點在哪裏？
- 甚麼可能出錯，如何撤銷？

### 步驟 2：建立 YAML 檔案

在適當的位置建立新檔案：

```bash
# Navigate to the business schemas directory
cd business/schemas/

# Create your workflow DNA file
touch my_workflow_dna.yaml
```

### 步驟 3：撰寫身份區塊

```yaml
workflow_dna:
  id: "wf_invoice_processing_v1"
  name: "Invoice Processing"
  domain: "finance"
  objective: "Process incoming invoices with accuracy and compliance."
  owner: "business_orchestrator"
  version: "1.0"
```

### 步驟 4：定義輸入及前置條件

```yaml
  inputs: ["invoice_document", "vendor_profile", "purchase_order"]
  preconditions:
    - "invoice_document != null"
    - "vendor_status == approved"
    - "purchase_order_exists == true"
```

### 步驟 5：定義步驟

將每個業務活動映射到一個具有代理程式和允許工具的步驟：

```yaml
  steps:
    - id: "extract_invoice_data"
      agent: "business_orchestrator"
      tools: ["contract_parser"]
    - id: "match_purchase_order"
      agent: "governance_officer"
      tools: ["crm", "policy_retriever"]
    - id: "approve_payment"
      agent: "tool_permission_broker"
      tools: ["billing_system"]
    - id: "record_transaction"
      agent: "business_orchestrator"
      tools: ["crm", "audit"]
    - id: "notify_accounts_payable"
      agent: "business_orchestrator"
      tools: ["email"]
```

### 步驟 6：配置記憶體存取

```yaml
  memory_reads: ["vendor_rules", "payment_exceptions", "approval_history"]
  memory_writes: ["event_log", "decision_memory", "transaction_log"]
```

### 步驟 7：設定防護機制

```yaml
  guardrails:
    human_approval_required_if:
      - "invoice_amount > approval_threshold"
      - "vendor_risk_score == high"
      - "three_way_match_failed == true"
```

### 步驟 8：定義驗證及回復

```yaml
  verification:
    required_checks:
      - "invoice_data_extracted"
      - "po_matched"
      - "payment_approved_or_rejected"
      - "transaction_recorded"
      - "audit_log_complete"
  rollback:
    reversible: true
    rollback_steps: ["void_payment", "revert_transaction", "notify_finance_team"]
```

### 步驟 9：加入適應度指標

```yaml
  fitness_metrics:
    - "processing_time"
    - "accuracy_rate"
    - "compliance_score"
    - "cost_per_invoice"
    - "exception_rate"
```

### 步驟 10：驗證工作流程

執行驗證指令以確保你的 DNA 滿足所有正式環境要求：

```bash
npm run business:validate
```

驗證器檢查：

- 所有高風險操作都有人工閘門
- 所有不可逆操作都有回復計劃
- 所有記憶體寫入都宣告了來源
- 需要審計日誌寫入
- 所有參考的工具都存在於工具註冊表中
- 所有參考的代理程式都存在於代理程式名冊中

如果驗證失敗，你將收到具體的錯誤訊息，指出哪些要求未滿足。

```bash
# Additional evolution check
npm run business:evolution:check
```

第二個指令驗證你的工作流程與演化引擎的沙盒測試要求相容。

---

## 運行時執行流程

一旦工作流程 DNA 通過驗證並部署，以下是其運行時的執行方式：

### 1. 操作員啟動運行

操作員通過 API 或前端的 **Run Now** 按鈕發起執行：

```bash
# API approach
curl -X POST http://127.0.0.1:8000/api/v1/workflows/wf_customer_onboarding_v12/runs \
  -H "Content-Type: application/json" \
  -d '{"case_id": "customer_12345"}'
```

或通過 Next.js 操作控制台：

1. 導航至 **Workflows**
2. 選擇工作流程
3. 點擊 **Run Now**
4. 提供所需的負載（例如 `case_id`）

### 2. 運行時遍歷圖

運行時引擎按順序處理每個步驟：

```text
Step 1: verify_contract
  Agent: governance_officer
  Tools: contract_parser, policy_retriever
  Result: contract verified, no exceptions
  tool_effects: [parse_result, policy_check_result]

Step 2: create_customer_record
  Agent: business_orchestrator
  Tools: crm
  Result: record created (CRM ID: cust_456)
  tool_effects: [crm_create_result]

Step 3: configure_billing
  Agent: tool_permission_broker
  Tools: billing_system
  ** HUMAN GATE TRIGGERED ** (irreversible action)
  Waiting for reviewer approval...
  [Reviewer approves]
  Result: billing configured
  tool_effects: [billing_config_result]

Step 4: send_welcome_packet
  Agent: business_orchestrator
  Tools: email
  Result: welcome email sent
  tool_effects: [email_send_result]
```

### 3. 人工閘門暫停不可逆步驟

當達到 `configure_billing` 步驟時，運行時偵測到它涉及一個不可逆操作（帳單設定無法輕易撤銷）。它建立一個人工閘門：

- 運行狀態變更為 `awaiting_approval`
- 通知發送給指定的審查人員
- 步驟在審查人員批准之前不會執行
- 所有上下文（合約詳情、客戶記錄、建議的帳單配置）都呈現給審查人員

### 4. 終端狀態的自動反思

當工作流程達到終端狀態（完成或失敗）時，系統可能自動：

1. **反思**運行 - 分析甚麼做得好、甚麼可以改進
2. **寫入經驗教訓**到 `organization_memory` 和 `improvement_lessons`
3. **自動提議**一個僅限沙盒的變體（如果偵測到改進機會）

```text
Run completed -> auto_reflect -> write lessons -> (optional) auto_propose variant
```

> **警告：** 提議的變體絕不會修改正式環境 DNA。它們僅存在於演化沙盒中，直到通過評估、灰度測試，以及（在需要時）人工簽核。

### 5. 工具效果追蹤

執行期間的每個工具呼叫都會產生一個持久的 `tool_effects` 記錄：

```json
{
  "step_id": "create_customer_record",
  "tool": "crm",
  "action": "create",
  "input": {"name": "Acme Corp", "type": "enterprise"},
  "output": {"id": "cust_456", "status": "active"},
  "timestamp": "2026-07-06T14:05:22Z",
  "reversible": true,
  "rollback_action": "disable_customer_record"
}
```

這些記錄提供：

- 所有系統互動的完整審計軌跡
- 合規性和治理審查的證據
- 演化引擎適應度計算的資料
- 流程智能挖掘的輸入

---

## 實際應用案例

### 案例 1：客戶入職（旗艦）

`wf_customer_onboarding_v12` 工作流程展示了完整的 DNA 模式：

- **領域：** 營運
- **步驟：** 4 個（驗證合約、建立記錄、配置帳單、發送歡迎包）
- **人工閘門：** 帳單配置（不可逆）
- **適應度指標：** 週期時間、錯誤率、客戶滿意度、合規通過率
- **關鍵學習：** 帳單人工閘門捕捉到配置錯誤，否則將需要與支付處理器進行人工干預

**業務價值：** 將入職時間從 3 天平均減少至 38 分鐘，500+ 案例中零合規違規。

### 案例 2：發票處理

發票處理工作流程展示了財務營運的 DNA：

- **領域：** 財務
- **步驟：** 5 個（提取資料、匹配採購訂單、審批付款、記錄交易、通知應付帳款）
- **人工閘門：** 超過門檻的付款審批或三方匹配失敗時
- **適應度指標：** 處理時間、準確率、合規分數
- **關鍵學習：** 三方匹配驗證（發票 vs 採購訂單 vs 收貨單）在到達人工審查之前捕捉了 94% 的差異

**業務價值：** 每月處理 2,000+ 張發票，準確率 99.2%，將平均處理時間從 45 分鐘減少至 8 分鐘。

### 案例 3：合約續期

合約續期工作流程展示了法律營運的 DNA：

- **領域：** 法律
- **步驟：** 6 個（審查條款、檢查合規性、提議更新、法律審查閘門、執行續期、通知各方）
- **人工閘門：** 非標準條款或高價值合約的法律審查
- **適應度指標：** 續期週期時間、合規率、客戶保留率
- **關鍵學習：** 通過 contract_parser 工具的例外偵測識別需要法律升級的非標準責任條款

**業務價值：** 將合約續期週期從 2 週減少至 3 天，所有非標準條款都正確升級進行法律審查。

---

## 最佳實踐

### 1. 從最簡可行的工作流程開始

不要嘗試在第一個 DNA 版本中編碼每個邊緣案例。從正常路徑開始，然後迭代：

```yaml
# v1: Just the core steps
steps:
  - id: "intake"
    agent: "business_orchestrator"
    tools: ["crm"]
  - id: "process"
    agent: "business_orchestrator"
    tools: ["email"]
```

### 2. 始終宣告回復計劃

即使你認為工作流程是低風險的，也要定義回復步驟。驗證器要求任何修改外部狀態的步驟都有回復計劃。

### 3. 使用具體的工具列表

絕不要讓代理程式存取其特定步驟不需要的工具：

```yaml
# Bad: too many tools
- id: "send_email"
  agent: "business_orchestrator"
  tools: ["email", "crm", "billing", "audit"]  # Why does email need billing?

# Good: minimal tools
- id: "send_email"
  agent: "business_orchestrator"
  tools: ["email"]
```

### 4. 定義有意義的適應度指標

選擇反映實際業務價值的指標，而非僅僅技術效能：

```yaml
fitness_metrics:
  - "customer_satisfaction"    # Business outcome
  - "compliance_pass_rate"     # Risk management
  - "cycle_time"               # Efficiency
  - "cost_per_case"            # Economics
```

### 5. 明確地版本化你的 DNA

使用 ID 後綴進行版本追蹤。這使演化引擎能夠比較變體：

```yaml
id: "wf_customer_onboarding_v12"   # Current production
# Evolution might create:
# "wf_customer_onboarding_v12_variant_a" (sandbox only)
```

### 6. 推廣前先測試

始終在 DNA 到達正式環境之前進行驗證：

```bash
# Validate schema and constraints
npm run business:validate

# Check evolution compatibility
npm run business:evolution:check

# Run governance checks
npm run business:governance

# Run security checks
npm run business:security
```

### 7. 慷慨使用防護機制

有疑問時，加入人工閘門。在證明安全性之後移除閘門比在事故之後再加入要容易得多：

```yaml
guardrails:
  human_approval_required_if:
    - "risk_tier >= 3"
    - "amount > 1000"
    - "first_time_for_customer == true"
```

### 8. 記錄決策點

對於代理程式做出非平凡決策的步驟，確保在事件日誌中捕捉 `decision_reason_summary`。這為治理審查提供證據，並幫助演化引擎理解為何選擇某些路徑。

---

## 本章總結

在本章中，你學習了：

- **工作流程 DNA** 是將業務流程編碼為受限狀態圖的核心結構
- 每個 DNA 宣告**步驟、代理程式、工具、記憶體、防護機制、驗證、回復和適應度指標**
- **受限狀態圖**模型通過明確約束每個步驟能做甚麼來防止不可預測的代理程式行為
- **人工閘門**自動暫停不可逆或高風險操作的執行
- **工具效果**為每次工具互動建立持久的審計軌跡
- **自動反思**使持續學習成為可能而不修改正式環境工作流程
- **驗證**（`npm run business:validate`）強制執行正式環境安全要求
- 演化引擎可以提議改進但**絕不直接修改正式環境**

---

## 知識檢查測驗

測試你對工作流程 DNA 概念的理解：

**問題 1：** 系統的五個設計優先順序是甚麼，按順序排列？

<details>
<summary>顯示答案</summary>
安全性、可審計性、正確性、效率、自主性。自主性通過證據獲得，絕不預設授予。
</details>

**問題 2：** 當工作流程步驟觸發人工閘門條件時會發生甚麼？

<details>
<summary>顯示答案</summary>
運行時在該步驟暫停執行，將運行狀態變更為 `awaiting_approval`，通知指定的審查人員並提供完整上下文，且在授權審查人員明確批准繼續之前不會進行。
</details>

**問題 3：** 列舉至少四個 DNA 驗證器會拒絕工作流程的條件。

<details>
<summary>顯示答案</summary>
驗證器在以下情況拒絕 DNA：(1) 高風險操作缺少人工閘門，(2) 不可逆操作缺少回復計劃，(3) 記憶體寫入缺少來源，(4) 未宣告審計日誌寫入，(5) 參考的工具不存在於註冊表中，(6) 參考的代理程式不存在於名冊中。
</details>

**問題 4：** `memory_reads` 和 `allowed_memory_scopes` 之間有甚麼區別？

<details>
<summary>顯示答案</summary>
`memory_reads` 宣告工作流程打算存取的具體記憶體項目。`allowed_memory_scopes` 是運行時強制執行機制，限制哪些記憶體命名空間實際可存取 - 它充當權限邊界。工作流程只能讀取落在其允許範圍內的項目。
</details>

**問題 5：** 演化引擎如何使用適應度指標？

<details>
<summary>顯示答案</summary>
演化引擎使用適應度指標計算加權適應度分數（F）來比較工作流程變體。分數結合品質、安全性、合規性、效率和人類滿意度（正面因素），同時懲罰風險、延遲和成本。只有在改進目標指標而不降低安全性或合規性的情況下，變體才會被推廣。
</details>

**問題 6：** 甚麼是 `tool_effects`，為何它們重要？

<details>
<summary>顯示答案</summary>
`tool_effects` 是工作流程執行期間每次工具呼叫建立的持久記錄。它們捕捉工具名稱、操作、輸入、輸出、時間戳、可逆性狀態和回復操作。它們之所以重要，因為提供：(1) 完整的審計軌跡，(2) 合規審查的證據，(3) 演化引擎的資料，以及 (4) 流程智能挖掘的輸入。
</details>

**問題 7：** 為何系統使用受限狀態圖而非自由形式代理程式群組？

<details>
<summary>顯示答案</summary>
受限狀態圖在結構層面強制執行狀態、權限和人在迴路中的閘門。雖然 ReAct 風格的推理迴路在單個節點內很有用，但圖本身防止代理程式走向不可預測的路徑、存取未授權的工具或繞過安全控制。這使得系統在設計上就是可審計、可測試和安全的。
</details>

---

## 下一步

在下一章中，你將使用客戶入職工作流程完成完整的業務流程執行，從頭到尾體驗 E1 操作員路徑。
