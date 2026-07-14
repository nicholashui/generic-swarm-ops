# 第 2.4 章：流程智能使用

![Process Intelligence Pipeline](../assets/02-04-process-intelligence-pipeline.svg)

## 學習目標

完成本章後，你將能夠：

1. 使用 API 將事件日誌匯入流程智能層
2. 理解事件日誌結構及其必要欄位
3. 使用 PI API 發現流程、檢查符合性並分析瓶頸
4. 導航 `business/process-intelligence/` 下的 PI 產出物資料夾結構
5. 使用 PI 代理程式（流程挖掘器、符合性、瓶頸分析器）
6. 產生和解讀 PI 產出物以改進營運

## 先決條件

開始本章之前，請確保你已經：

- 完成第 2.1 至 2.3 章
- 有一個正在運行且具有 Postgres 連接的後端實例
- 至少有一次已完成的工作流程運行（來自第 2.2 章）
- 理解工作流程執行和 tool_effects

---

## 甚麼是流程智能？

流程智能（PI）是從**實際營運軌跡**而非僅從文件化程序學習的分析層。工作流程 DNA 定義工作*應該*如何發生，而 PI 通過分析真實執行的事件日誌揭示工作*實際*如何發生。

PI 層回答關鍵問題：

- **發現：** 實際運行的流程是甚麼？它們走哪些路徑？
- **符合性：** 實際執行是否匹配定義的工作流程？
- **瓶頸：** 延遲、迴圈和交接失敗在哪裏？
- **改進：** 甚麼干預措施最能改善結果？

> **備註：** 流程智能的靈感來自流程挖掘宣言（IEEE 流程挖掘工作小組）。它將學術流程挖掘技術應用於代理程式驅動的業務作業系統。

---

## PI 管線

流程智能管線遵循以下流程：

```text
POST /api/v1/processes/event-logs
  -> store event in runtime (Postgres document)
  -> recompute discovered processes, conformance, bottlenecks
  -> write JSON under business/process-intelligence/
  -> upsert pi_artifacts collection
```

每次事件匯入觸發一連串分析，更新 PI 產出物集合。這意味着 PI 洞察始終是最新的並反映最新的營運資料。

---

## 事件日誌結構

每個提交到 PI 層的事件必須符合此結構：

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
  risk_tier: "tier_3_execute_reversible"
  human_approved: true
  outcome:
    status: "completed"
    latency_minutes: 42
    quality_score: 0.94
```

### 欄位描述

| 欄位 | 類型 | 必要 | 描述 |
|-------|------|----------|-------------|
| `id` | string | 是 | 唯一事件識別碼（前綴：`evt_`） |
| `timestamp` | ISO 8601 | 是 | 事件發生時間 |
| `actor_type` | enum | 是 | 誰執行的：`human`、`agent` 或 `system` |
| `actor_id` | string | 是 | 參與者的識別碼 |
| `process_id` | string | 是 | 此事件屬於哪個流程 |
| `case_id` | string | 是 | 具體案例/實例識別碼 |
| `activity` | string | 是 | 執行了甚麼活動 |
| `input_refs` | array | 否 | 輸入文件/資料的參考 |
| `output_refs` | array | 否 | 產出物的參考 |
| `tools_used` | array | 否 | 此活動涉及的工具 |
| `decision_point` | boolean | 否 | 是否為決策點 |
| `decision_reason_summary` | string | 否 | 決策的理由 |
| `confidence` | float | 否 | 信心水平（0.0-1.0） |
| `risk_tier` | string | 否 | 操作的風險分類 |
| `human_approved` | boolean | 否 | 人類是否批准了此操作 |
| `outcome.status` | string | 是 | 結果：`completed`、`failed`、`pending` |
| `outcome.latency_minutes` | number | 否 | 此活動花費的時間 |
| `outcome.quality_score` | float | 否 | 品質指標（0.0-1.0） |

> **提示：** 盡可能包含更多可選欄位。每個事件攜帶的上下文越豐富，PI 分析就越深入。決策點和信心分數對瓶頸分析特別有價值。

---

## 逐步指南：匯入事件日誌

### 步驟 1：提交單一事件

```bash
curl -X POST http://127.0.0.1:8000/api/v1/processes/event-logs \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>" \
  -d '{
    "id": "evt_001",
    "timestamp": "2026-07-06T14:00:00Z",
    "actor_type": "agent",
    "actor_id": "governance_officer",
    "process_id": "customer_onboarding",
    "case_id": "customer_12345",
    "activity": "verify_contract",
    "tools_used": ["contract_parser", "policy_retriever"],
    "decision_point": false,
    "outcome": {
      "status": "completed",
      "latency_minutes": 2,
      "quality_score": 0.98
    }
  }'
```

### 步驟 2：提交批次事件（完整案例）

要為 PI 提供完整的案例歷史，提交所有步驟的事件：

```bash
# Event 1: Contract verification
curl -X POST http://127.0.0.1:8000/api/v1/processes/event-logs \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>" \
  -d '{
    "id": "evt_001",
    "timestamp": "2026-07-06T14:00:00Z",
    "actor_type": "agent",
    "actor_id": "governance_officer",
    "process_id": "customer_onboarding",
    "case_id": "customer_12345",
    "activity": "verify_contract",
    "tools_used": ["contract_parser", "policy_retriever"],
    "outcome": {"status": "completed", "latency_minutes": 2, "quality_score": 0.98}
  }'

# Event 2: Record creation
curl -X POST http://127.0.0.1:8000/api/v1/processes/event-logs \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>" \
  -d '{
    "id": "evt_002",
    "timestamp": "2026-07-06T14:02:00Z",
    "actor_type": "agent",
    "actor_id": "business_orchestrator",
    "process_id": "customer_onboarding",
    "case_id": "customer_12345",
    "activity": "create_customer_record",
    "tools_used": ["crm"],
    "outcome": {"status": "completed", "latency_minutes": 1, "quality_score": 0.95}
  }'

# Event 3: Billing configuration (with human gate)
curl -X POST http://127.0.0.1:8000/api/v1/processes/event-logs \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>" \
  -d '{
    "id": "evt_003",
    "timestamp": "2026-07-06T14:03:00Z",
    "actor_type": "human",
    "actor_id": "reviewer_admin",
    "process_id": "customer_onboarding",
    "case_id": "customer_12345",
    "activity": "configure_billing",
    "tools_used": ["billing_system"],
    "decision_point": true,
    "decision_reason_summary": "Billing config matches contract section 4.2.",
    "human_approved": true,
    "risk_tier": "tier_4_execute_with_gate",
    "outcome": {"status": "completed", "latency_minutes": 8, "quality_score": 0.92}
  }'

# Event 4: Welcome packet
curl -X POST http://127.0.0.1:8000/api/v1/processes/event-logs \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_token>" \
  -d '{
    "id": "evt_004",
    "timestamp": "2026-07-06T14:11:00Z",
    "actor_type": "agent",
    "actor_id": "business_orchestrator",
    "process_id": "customer_onboarding",
    "case_id": "customer_12345",
    "activity": "send_welcome_packet",
    "tools_used": ["email"],
    "outcome": {"status": "completed", "latency_minutes": 1, "quality_score": 0.99}
  }'
```

### 步驟 3：驗證事件儲存

```bash
# Retrieve stored events
curl http://127.0.0.1:8000/api/v1/processes/event-logs \
  -H "Cookie: gso_access_token=<your_token>"
```

### 步驟 4：觸發分析重新計算

事件匯入自動觸發重新計算，但你也可以查詢當前狀態：

```bash
# View process summary
curl http://127.0.0.1:8000/api/v1/processes/summary \
  -H "Cookie: gso_access_token=<your_token>"
```

---

## PI API 參考

### 事件日誌管理

| 方法 | 端點 | 用途 |
|--------|----------|---------|
| `POST` | `/api/v1/processes/event-logs` | 匯入新事件 |
| `GET` | `/api/v1/processes/event-logs` | 檢索已儲存的事件 |

### 分析端點

| 方法 | 端點 | 用途 |
|--------|----------|---------|
| `GET` | `/api/v1/processes/discovered` | 檢視已發現的流程模型 |
| `GET` | `/api/v1/processes/conformance` | 檢視符合性報告 |
| `GET` | `/api/v1/processes/bottlenecks` | 檢視瓶頸分析 |
| `GET` | `/api/v1/processes/summary` | 檢視整體 PI 摘要 |
| `GET` | `/api/v1/processes/artifacts` | 列出所有已產生的產出物 |

### 使用發現 API

```bash
# Discover processes from accumulated event logs
curl http://127.0.0.1:8000/api/v1/processes/discovered \
  -H "Cookie: gso_access_token=<your_token>"
```

預期回應：

```json
{
  "discovered_processes": [
    {
      "process_id": "customer_onboarding",
      "activity_count": 4,
      "case_count": 15,
      "activities": [
        "verify_contract",
        "create_customer_record",
        "configure_billing",
        "send_welcome_packet"
      ],
      "common_paths": [
        {
          "path": ["verify_contract", "create_customer_record", "configure_billing", "send_welcome_packet"],
          "frequency": 0.87
        },
        {
          "path": ["verify_contract", "create_customer_record", "send_welcome_packet"],
          "frequency": 0.13,
          "note": "billing skipped for free-tier customers"
        }
      ]
    }
  ]
}
```

### 使用符合性 API

```bash
# Check conformance against defined workflows
curl http://127.0.0.1:8000/api/v1/processes/conformance \
  -H "Cookie: gso_access_token=<your_token>"
```

預期回應：

```json
{
  "conformance_reports": [
    {
      "process_id": "customer_onboarding",
      "expected_flow": ["verify_contract", "create_customer_record", "configure_billing", "send_welcome_packet"],
      "conformance_rate": 0.87,
      "deviations": [
        {
          "case_id": "customer_678",
          "deviation_type": "skipped_activity",
          "activity_skipped": "configure_billing",
          "reason": "free_tier_customer",
          "severity": "low"
        },
        {
          "case_id": "customer_901",
          "deviation_type": "extra_activity",
          "extra_activity": "escalate_to_legal",
          "reason": "non_standard_contract_clause",
          "severity": "medium"
        }
      ]
    }
  ]
}
```

### 使用瓶頸 API

```bash
# Analyze bottlenecks
curl http://127.0.0.1:8000/api/v1/processes/bottlenecks \
  -H "Cookie: gso_access_token=<your_token>"
```

預期回應：

```json
{
  "bottleneck_analysis": [
    {
      "process_id": "customer_onboarding",
      "bottlenecks": [
        {
          "activity": "configure_billing",
          "type": "approval_wait",
          "avg_latency_minutes": 8.5,
          "p95_latency_minutes": 45,
          "contributing_factors": [
            "human_gate_approval_required",
            "reviewer_availability"
          ],
          "suggested_intervention": "Pre-validate billing in verify_contract step to reduce gate frequency"
        },
        {
          "activity": "verify_contract",
          "type": "activity_latency",
          "avg_latency_minutes": 2.3,
          "p95_latency_minutes": 12,
          "contributing_factors": [
            "complex_contract_parsing",
            "multiple_policy_checks"
          ],
          "suggested_intervention": "Cache frequently-used policy results"
        }
      ]
    }
  ]
}
```

---

## PI 產出物資料夾

PI 層將持久的 JSON 產出物寫入 `business/process-intelligence/` 下的檔案系統：

| 路徑 | 內容 |
|------|---------|
| `business/process-intelligence/discovered-processes/` | 每個流程的活動映射 |
| `business/process-intelligence/conformance-reports/` | 預期 vs 觀察到的活動 |
| `business/process-intelligence/bottlenecks/` | 審批等待 + 活動延遲 |
| `business/process-intelligence/event-logs/` | 參考 / 營運備註 |

### 產出物範例：已發現流程

```json
// business/process-intelligence/discovered-processes/customer_onboarding.json
{
  "process_id": "customer_onboarding",
  "discovered_at": "2026-07-06T15:00:00Z",
  "version": 3,
  "activity_map": {
    "nodes": [
      {"id": "verify_contract", "agent": "governance_officer", "avg_duration_min": 2.3},
      {"id": "create_customer_record", "agent": "business_orchestrator", "avg_duration_min": 1.1},
      {"id": "configure_billing", "agent": "tool_permission_broker", "avg_duration_min": 8.5},
      {"id": "send_welcome_packet", "agent": "business_orchestrator", "avg_duration_min": 0.8}
    ],
    "edges": [
      {"from": "verify_contract", "to": "create_customer_record", "frequency": 1.0},
      {"from": "create_customer_record", "to": "configure_billing", "frequency": 0.87},
      {"from": "create_customer_record", "to": "send_welcome_packet", "frequency": 0.13},
      {"from": "configure_billing", "to": "send_welcome_packet", "frequency": 1.0}
    ]
  },
  "total_cases_analyzed": 45,
  "avg_total_cycle_time_min": 12.7
}
```

### 產出物範例：符合性報告

```json
// business/process-intelligence/conformance-reports/customer_onboarding_2026_q3.json
{
  "process_id": "customer_onboarding",
  "report_period": "2026-Q3",
  "generated_at": "2026-07-06T15:00:00Z",
  "conformance_rate": 0.87,
  "total_cases": 45,
  "conforming_cases": 39,
  "deviation_categories": {
    "skipped_activity": 4,
    "extra_activity": 2,
    "reordered_activities": 0,
    "repeated_activity": 0
  }
}
```

### 產出物範例：瓶頸報告

```json
// business/process-intelligence/bottlenecks/customer_onboarding_current.json
{
  "process_id": "customer_onboarding",
  "analyzed_at": "2026-07-06T15:00:00Z",
  "cases_analyzed": 45,
  "identified_bottlenecks": [
    {
      "activity": "configure_billing",
      "bottleneck_type": "approval_wait",
      "severity": "medium",
      "avg_wait_minutes": 8.5,
      "impact_on_total_cycle": 0.67,
      "recommendation": "Pre-validate billing config to reduce gate triggers"
    }
  ]
}
```

---

## PI 代理程式

流程智能層實作為一組專門的服務（非獨立的 LLM 代理程式）來分析事件資料：

### 流程挖掘器代理程式

**用途：** 從事件日誌模式中發現真實的工作流程。

- 分析跨案例的事件序列
- 識別常見的活動路徑
- 偵測流程變體（替代路徑）
- 增量更新已發現的流程模型

### 符合性代理程式

**用途：** 將實際工作與文件化的 SOP 和工作流程 DNA 進行比較。

- 將觀察到的路徑映射到預期的 DNA 步驟序列
- 識別偏差：跳過的步驟、額外步驟、重新排序
- 分類偏差嚴重程度
- 產生每個流程的符合性報告

### 瓶頸分析器代理程式

**用途：** 發現延遲、迴圈、返工和交接失敗。

- 計算活動持續時間統計（平均、p50、p95、最大值）
- 識別審批等待作為瓶頸因素
- 偵測迴圈（案例中重複的活動）
- 識別代理程式之間的交接延遲
- 提出按預期影響排名的干預建議

### 任務挖掘代理程式

**用途：** 在允許的情況下觀察 UI/人類層面的步驟。

- 捕捉人類互動模式
- 識別可以自動化的人工步驟
- 測量人類任務持續時間作為基準比較

### 因果改進代理程式

**用途：** 提出可能改善結果的干預措施。

- 分析流程變化與結果之間的相關性
- 產生關於因果因素的假設
- 提議沙盒實驗來測試干預措施
- 追蹤實驗結果以供學習

---

## 逐步指南：產生 PI 產出物

### 步驟 1：確保有足夠的事件資料

PI 分析需要最少數量的事件才能產出有意義的結果。對於可靠的發現：

- 每個流程至少 5 個案例
- 每個案例至少 3 個活動
- 事件跨越多個時間段

### 步驟 2：通過 API 匯入事件

使用 POST 端點提交事件（如前所示）。

### 步驟 3：檢查發現結果

```bash
curl http://127.0.0.1:8000/api/v1/processes/discovered \
  -H "Cookie: gso_access_token=<your_token>"
```

### 步驟 4：運行符合性檢查

```bash
curl http://127.0.0.1:8000/api/v1/processes/conformance \
  -H "Cookie: gso_access_token=<your_token>"
```

### 步驟 5：分析瓶頸

```bash
curl http://127.0.0.1:8000/api/v1/processes/bottlenecks \
  -H "Cookie: gso_access_token=<your_token>"
```

### 步驟 6：審查已產生的產出物

```bash
# List all PI artifacts
ls business/process-intelligence/

# View discovered processes
cat business/process-intelligence/discovered-processes/customer_onboarding.json

# View conformance reports
cat business/process-intelligence/conformance-reports/

# View bottleneck analysis
cat business/process-intelligence/bottlenecks/
```

### 步驟 7：使用產出物 API

```bash
curl http://127.0.0.1:8000/api/v1/processes/artifacts \
  -H "Cookie: gso_access_token=<your_token>"
```

---

## 程式碼參考

PI 實作位於：

| 路徑 | 用途 |
|------|---------|
| `backend/app/infrastructure/process_intelligence/artifacts.py` | 核心產出物產生 |
| 運行時 `_refresh_pi_artifacts` | 在每次事件匯入時觸發 |
| `test_p3_pi_evolution.py` | PI 演化整合測試 |
| 記分卡事件匯入測試 | 驗證 PI 管線完整性 |

---

## 實際應用案例

### 案例 1：識別審批瓶頸

一家公司通過 PI 發現帳單人工閘門為每次入職週期平均增加 8.5 分鐘。然而，92% 的閘門在審查人員可用時 30 秒內就被批准。

**PI 洞察：** 瓶頸不在閘門決策本身，而在審查人員的可用性。建議的干預措施：實施自動升級，在 5 分鐘後路由到備份審查人員。

**結果：** 實施升級後，p95 閘門延遲從 45 分鐘降至 8 分鐘。

### 案例 2：偵測流程漂移

PI 符合性分析揭示 13% 的入職案例跳過了帳單配置步驟。調查顯示這些是通過企業工作流程處理的免費方案客戶。

**PI 洞察：** 工作流程 DNA 未考慮免費方案路徑。看起來像錯誤的符合性偏差實際上是合法的業務變體。

**結果：** 團隊為免費方案入職建立了獨立的 DNA 變體，將符合率提高到 98% 並為免費方案案例減少了 6 分鐘的週期時間。

### 案例 3：相關品質和延遲

PI 分析顯示一個相關性：`verify_contract` 花費超過 5 分鐘的案例，最終結果的 `quality_score` 高出 3 倍。因果改進代理程式假設徹底的合約審查能提早發現問題，防止下游問題。

**PI 洞察：** 合約驗證中的「瓶頸」實際上在提供價值。將其最佳化掉會降低品質。

**結果：** 團隊調整了適應度函數，在合約驗證步驟中將品質權重設定高於純週期時間。

---

## 最佳實踐

### 1. 匯入所有可用事件

不要在匯入前過濾事件。PI 在完整案例歷史下效果最好：

```bash
# Good: submit all activities including minor ones
# Bad: only submit "important" activities
```

### 2. 包含決策上下文

在適用時始終填充 `decision_point`、`decision_reason_summary` 和 `confidence`。這些欄位使因果改進代理程式能夠理解為何選擇某些路徑。

### 3. 使用一致的 process_id 和 case_id

確保同一流程的所有事件使用相同的 `process_id` 值，同一案例的所有事件使用相同的 `case_id` 值。不一致會使分析碎片化。

### 4. 定期審查符合性報告

安排每週符合性審查以儘早發現流程漂移：

- 符合率下降？調查偏差
- 新的偏差模式？考慮 DNA 更新
- 一致的偏差？可能表示合法的變體

### 5. 根據瓶頸建議採取行動

PI 瓶頸分析提供可行的建議。將這些輸入到演化引擎：

```text
PI identifies bottleneck -> Improvement pipeline proposes variant -> 
Sandbox evaluation -> Canary deployment -> Promote if metrics improve
```

### 6. 將 PI 與演化結果相關聯

追蹤演化引擎的改進是否實際解決了 PI 識別的瓶頸：

- 提議的變體是否減少了閘門延遲？
- 新路徑是否改善了符合性？
- 最佳化是否影響了品質分數？

---

## 本章總結

在本章中，你學習了：

- **流程智能**分析真實營運軌跡（事件日誌）以揭示工作實際如何發生
- 事件通過 `POST /api/v1/processes/event-logs` 匯入，使用涵蓋參與者、活動、工具、決策和結果的豐富結構
- PI 提供三個核心分析：**流程發現**（存在哪些路徑）、**符合性**（實際 vs 預期）和**瓶頸分析**（延遲在哪裏）
- 產出物寫入 `business/process-intelligence/` 下的四個子資料夾：discovered-processes、conformance-reports、bottlenecks 和 event-logs
- 五個 PI 代理程式協作：流程挖掘器、任務挖掘、符合性、瓶頸分析器和因果改進
- PI 洞察輸入演化引擎以進行基於證據的工作流程改進

---

## 知識檢查測驗

測試你對流程智能的理解：

**問題 1：** 事件日誌結構中的必要欄位是甚麼？

<details>
<summary>顯示答案</summary>
必要欄位是：`id`、`timestamp`、`actor_type`、`actor_id`、`process_id`、`case_id`、`activity` 和 `outcome.status`。所有其他欄位（tools_used、decision_point、confidence 等）是可選的但建議填寫。
</details>

**問題 2：** 當事件通過 POST 端點匯入時會發生甚麼？

<details>
<summary>顯示答案</summary>
事件：(1) 作為文件儲存在 Postgres 運行時中，(2) 觸發已發現流程、符合性和瓶頸的重新計算，(3) 將更新的 JSON 產出物寫入 `business/process-intelligence/` 下，以及 (4) 更新 pi_artifacts 集合。
</details>

**問題 3：** 四個 PI 產出物資料夾是甚麼，每個包含甚麼？

<details>
<summary>顯示答案</summary>
(1) `discovered-processes/` - 顯示常見路徑和頻率的每個流程活動映射，(2) `conformance-reports/` - 預期 vs 觀察到的活動比較及偏差分析，(3) `bottlenecks/` - 審批等待和活動延遲分析及建議，(4) `event-logs/` - 參考資料和營運備註。
</details>

**問題 4：** 列舉五個 PI 代理程式及其主要用途。

<details>
<summary>顯示答案</summary>
(1) 流程挖掘器 - 從事件日誌模式發現真實的工作流程，(2) 任務挖掘代理程式 - 在允許的情況下觀察 UI/人類層面的步驟，(3) 符合性代理程式 - 將實際工作與 SOP 和 DNA 進行比較，(4) 瓶頸分析器 - 發現延遲、迴圈、返工和交接失敗，(5) 因果改進代理程式 - 提出可能改善結果的干預措施。
</details>

**問題 5：** PI 層與靜態工作流程文件有何不同？

<details>
<summary>顯示答案</summary>
靜態文件描述工作應該如何發生（預期流程）。PI 通過檢查已完成案例的真實事件日誌分析工作實際如何發生。PI 可以發現未文件化的路徑、識別預期與實際流程之間的偏差、揭示文件中不可見的瓶頸，以及為改進決策提供量化證據。
</details>

**問題 6：** PI 瓶頸分析與演化引擎之間有甚麼關係？

<details>
<summary>顯示答案</summary>
PI 識別具有具體指標（延遲、頻率、影響）的瓶頸並建議干預措施。這些建議輸入到自我改進管線：演化引擎可以自動提議解決 PI 識別瓶頸的變體，然後在沙盒中針對黃金任務測試這些變體。如果變體改善了瓶頸指標而不降低其他指標，它可以通過灰度流程推廣。
</details>

---

## 下一步

在下一章中，你將學習知識和記憶體協作層如何提供分層檢索、多種記憶體類型和圖形編排以實現智能資訊存取。
