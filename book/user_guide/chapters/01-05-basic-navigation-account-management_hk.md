# 第 01-05 章：基本導航及帳戶管理

![Navigation Layout](../assets/01-05-navigation-layout.svg)

## 學習目標

在完成本章後，你將能夠：

1. 導航 Next.js 操作控制台並定位所有主要部分
2. 理解每個導航項目的目的（代理、工作流程、運行、審批、知識、評估、流程、演化）
3. 使用 RBAC（admin、operator、reviewer 角色）管理用戶帳戶
4. 配置會話管理設定（cookie、令牌、過期）
5. 執行常見的帳戶管理任務（建立用戶、分配角色、重設密碼）
6. 從 UI 使用自我改進流程（反思、提議、評估、金絲雀）

## 先決條件

- 已完成[第 01-04 章](01-04-first-time-configuration.md)且系統已完全配置
- 後端運行在 `http://127.0.0.1:8000`
- 前端運行在 `http://localhost:3000`
- 已使用管理員憑證登入（`admin@example.com` / `admin-password`）
- 至少建立了一個代理及一個工作流程

---

## 1. 操作控制台概覽

Generic Swarm Ops 控制台是一個 Next.js 應用程式，為多代理系統提供完整的運營介面。當以 `NEXT_PUBLIC_DEMO_MODE=false` 運行時，它連接到即時 FastAPI 後端獲取即時資料。

### 1.1 控制台 URL 及存取

| 組件 | URL | 目的 |
|-----------|-----|---------|
| 前端控制台 | `http://localhost:3000` | 主要運營介面 |
| 登入頁面 | `http://localhost:3000/login` | 認證入口點 |
| 應用根目錄 | `http://localhost:3000/app` | 登入後儀表板 |

### 1.2 控制台佈局

操作控制台使用標準佈局，具有三個主要區域：

1. **側邊欄導航**（左側）-- 到所有系統部分的主要導航連結
2. **主內容區域**（中央）-- 所選部分的上下文敏感內容
3. **標頭列**（頂部）-- 用戶資訊、會話狀態及全域操作

### 1.3 導航結構

側邊欄提供對八個主要部分的存取：

| 導航項目 | 路徑 | 描述 |
|----------------|------|-------------|
| **Agents** | `/app/agents` | 建立、編輯及監控代理 |
| **Workflows** | `/app/workflows` | 管理 Workflow DNA 定義 |
| **Runs** | `/app/runs` | 檢視活躍及已完成的工作流程運行 |
| **Approvals** | `/app/approvals` | 管理人工閘門審批請求 |
| **Knowledge** | `/app/knowledge` | 搜尋及瀏覽知識庫 |
| **Evaluations** | `/app/evaluations` | 檢視評估結果及指標 |
| **Processes** | `/app/processes` | 流程智能儀表板 |
| **Evolution** | `/app/evolution` | 族群歸檔及適應度指標 |

---

## 2. 代理頁面

**路徑：** `/app/agents`

代理頁面是你建立、配置及監控所有系統代理的地方。

### 2.1 代理列表檢視

導航到代理頁面時，你會看到所有已配置代理的列表，包括：

- 代理名稱及 ID
- 分配的角色（execution、learning、control）
- 當前狀態（active、inactive、restricted）
- 風險等級分配
- 分配的工具

### 2.2 建立代理

1. 點擊 **Create Agent** 按鈕
2. 填寫表單欄位：
   - **Name：** 描述性的代理識別符
   - **Role：** 代理類別（execution、learning、control）
   - **Description：** 清晰解釋代理目的
   - **Tools：** 代理可存取的工具識別符陣列
   - **Risk Tier：** 自主級別（0-5）
   - **Constraints：** 行為限制（最大操作數、記憶範圍）
3. 點擊 **Save**

表單使用 Zod 結構驗證及 React Hook Form 進行輸入處理。驗證錯誤包含 `request_id` 用於除錯。

### 2.3 代理詳情檢視

點擊任何代理查看其詳情檢視：

- **Configuration 標籤：** 當前設定、工具、約束
- **Activity 標籤：** 此代理最近的操作
- **Metrics 標籤：** 效能資料（操作/天、錯誤率、延遲）
- **Audit 標籤：** 代理操作的完整審計日誌

### 2.4 常見代理操作

```bash
# 透過 API 列出所有代理
curl -b cookies.txt http://127.0.0.1:8000/api/v1/agents

# 取得特定代理詳情
curl -b cookies.txt http://127.0.0.1:8000/api/v1/agents/agent_customer_support_001

# 更新代理配置
curl -X PUT http://127.0.0.1:8000/api/v1/agents/agent_customer_support_001 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"risk_tier": 4, "tools": ["email", "crm", "knowledge_retriever", "escalation"]}'

# 停用代理
curl -X PATCH http://127.0.0.1:8000/api/v1/agents/agent_customer_support_001 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "inactive"}'
```

---

## 3. 工作流程頁面

**路徑：** `/app/workflows`

工作流程頁面管理系統中所有的 Workflow DNA 定義。

### 3.1 工作流程列表檢視

列表顯示所有已註冊的工作流程，包括：

- 工作流程 ID 及人類可讀名稱
- 領域分配
- 版本號
- 步驟數量
- 是否定義了人工閘門
- 當前啟用狀態

### 3.2 建立工作流程

1. 點擊 **Create Workflow**
2. 填寫 DNA 規格（完整結構請參閱第 01-04 章）
3. 表單根據 Workflow DNA 結構進行驗證
4. 點擊 **Save**

> **警告：** 運行時拒絕缺少以下任何內容的 Workflow DNA：高風險步驟的人工閘門、回滾計劃、來源或審計寫入。表單驗證在提交前捕獲這些。

### 3.3 運行工作流程

從工作流程詳情頁面：

1. 點擊 **Run Now**
2. 提供必需的有效負載（例如旗艦工作流程的 `case_id`）
3. 系統透過 Intake Router 路由運行
4. 在 Runs 頁面監控進度

```bash
# 透過 API 運行工作流程
curl -X POST http://127.0.0.1:8000/api/v1/runs \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "workflow_id": "wf_customer_onboarding_v12",
    "payload": {
      "case_id": "customer_12345",
      "signed_contract": "contract_v3",
      "customer_profile": "enterprise_tier",
      "billing_details": "annual_plan"
    }
  }'
```

---

## 4. 運行頁面

**路徑：** `/app/runs`

運行頁面提供所有工作流程執行的即時監控。

### 4.1 運行狀態

| 狀態 | 含義 |
|-------|---------|
| `pending` | 運行已排隊，等待編排器接收 |
| `running` | 正在進行活躍執行 |
| `waiting_approval` | 在人工閘門處暫停 |
| `completed` | 成功完成所有步驟 |
| `failed` | 遇到錯誤 |
| `rolled_back` | 失敗並成功回滾 |

### 4.2 運行詳情檢視

點擊任何運行查看：

- **步驟時間線：** 已完成、活躍及待處理步驟的視覺表示
- **當前狀態：** 運行目前在工作流程中的位置
- **工具效果：** 所有工具操作及其記錄的效果
- **記憶寫入：** 執行期間寫入記憶的內容
- **審計軌跡：** 每個操作及決策的完整日誌

### 4.3 改進流程

在已完成運行的詳情頁面上，你可以存取 **Improve** 按鈕來觸發自我改進流程：

1. **Reflect** -- 分析什麼做得好及什麼失敗
2. **Propose** -- 生成工作流程改進變體
3. **Evaluate** -- 對黃金任務測試變體
4. **Canary** -- 將變體部署到小範圍進行驗證

或點擊 **Run full pipeline** 自動執行所有四個步驟。

```bash
# 對已完成的運行觸發反思
curl -X POST http://127.0.0.1:8000/api/v1/improvement/reflect/run_12345 \
  -b cookies.txt

# 生成改進提議
curl -X POST http://127.0.0.1:8000/api/v1/improvement/auto-propose \
  -b cookies.txt

# 運行完整改進循環
curl -X POST http://127.0.0.1:8000/api/v1/loops/run \
  -b cookies.txt
```

---

## 5. 審批頁面

**路徑：** `/app/approvals`

審批頁面顯示所有待處理的人工閘門審批請求。

### 5.1 理解人工閘門

當工作流程步驟滿足 DNA 的 `guardrails.human_approval_required_if` 部分中定義的條件時，人工閘門被觸發。常見觸發器：

- 風險等級高
- 操作不可逆
- 偵測到合約例外
- 值超過閾值
- 合規檢查標記了問題

### 5.2 審批佇列

審批佇列顯示：

- 請求的工作流程及運行 ID
- 需要審批的步驟
- 閘門原因（哪個條件觸發）
- 請求的代理
- 支持證據/上下文
- 等待審批的時間

### 5.3 審批或拒絕

**作為 admin 或 reviewer：**

1. 點擊待處理的審批
2. 審查提供的上下文及證據
3. 點擊 **Approve** 允許步驟繼續
4. 或點擊 **Reject** 停止運行（如已定義則觸發回滾）

```bash
# 透過 API 列出待處理審批
curl -b cookies.txt http://127.0.0.1:8000/api/v1/approvals?status=pending

# 審批特定請求
curl -X POST http://127.0.0.1:8000/api/v1/approvals/approval_001/approve \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"reason": "Contract reviewed and acceptable", "reviewer_notes": "Standard terms"}'

# 拒絕請求
curl -X POST http://127.0.0.1:8000/api/v1/approvals/approval_001/reject \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"reason": "Non-standard liability clause requires legal review"}'
```

> **注意：** 只有具有 `admin` 或 `reviewer` 角色的用戶可以審批或拒絕人工閘門步驟。操作員可以檢視佇列但不能對審批採取行動。

---

## 6. 知識頁面

**路徑：** `/app/knowledge`

知識頁面提供對分層知識檢索系統的存取。

### 6.1 搜尋介面

搜尋介面支持三種檢索模式：

| 模式 | 層級 | 使用場景 |
|------|------|----------|
| **關鍵字/語義** | Tier 0 | 尋找特定段落或概念 |
| **實體/關係** | Tier 1 | 關於關係的多跳查詢 |
| **圖聯邦** | Tier 1+ | 跨領域實體探索 |

### 6.2 搜尋知識

1. 在搜尋框中輸入你的查詢
2. 選擇檢索層級（預設為 Tier 0，如需要自動升級）
3. 檢視帶有來源引用的結果
4. 點擊連結到來源文件

```bash
# 透過 API 搜尋知識
curl -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/knowledge/search?q=contract+review+process&tier=0"

# 基於實體的搜尋（Tier 1）
curl -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/knowledge/search?q=who+approved+contract+12345&tier=1"

# 聯邦導出（需要 Neo4j）
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/graph/federate \
  -b cookies.txt
```

### 6.3 記憶瀏覽器

知識頁面還提供對混合記憶系統的存取：

- **情節記憶：** 案例敘述及歷史上下文
- **語義記憶：** 事實、規則及知識條目
- **決策記憶：** 附帶推理的過往決策
- **評估記憶：** 測試結果及指標

---

## 7. 評估頁面

**路徑：** `/app/evaluations`

評估頁面顯示工作流程、代理及整體系統的評估結果。

### 7.1 評估類型

| 類型 | 目的 | 位置 |
|------|---------|----------|
| 黃金任務 | 核心正確性驗證 | `business/evals/golden-tasks/` |
| 回歸測試 | 防止更新工作流程的回歸 | `business/evals/regression-tests/` |
| 對抗測試 | 安全及穩健性測試 | `business/evals/adversarial-tests/` |
| 歷史重放 | 對過去真實案例進行驗證 | `business/evals/human-review-sets/` |
| 基準測試 | 效能及成本指標 | `business/evals/benchmark-results/` |

### 7.2 檢視結果

每次評估運行顯示：

- 被評估的目標工作流程/代理
- 使用的測試集
- 指標（品質分數、合規率、週期時間等）
- 通過/失敗判定
- 提升決策（金絲雀、提升、拒絕）
- 審查員簽署狀態

### 7.3 評估指標

每次評估追蹤的關鍵指標：

```json
{
  "quality_score": 0.94,
  "compliance_pass_rate": 0.99,
  "average_cycle_time_minutes": 38,
  "escalation_rate": 0.12,
  "hallucination_rate": 0.01,
  "unauthorized_tool_attempts": 0,
  "cost_per_case_usd": 0.42
}
```

---

## 8. 流程頁面

**路徑：** `/app/processes`

流程頁面提供對流程智能層輸出的存取。

### 8.1 流程智能制品

| 制品類型 | 目的 |
|---------------|---------|
| 事件日誌 | 原始運營事件資料 |
| 已發現流程 | 從實際行為探勘的工作流程模型 |
| 合規報告 | SOP 與實際工作比較 |
| 瓶頸 | 已識別的延遲、循環及交接失敗 |
| 因果假設 | 帶有證據的改進提議 |

### 8.2 檢視流程圖

頁面顯示已發現的流程圖，展示：

- 實際採取的工作流程路徑（不僅是已記錄的 SOP）
- 每條路徑的頻率
- 每步驟的平均持續時間
- 與預期行為的偏差點
- 帶有延遲指標的瓶頸位置

### 8.3 合規性分析

比較已記錄的程序與實際行為：

- 哪些步驟在實踐中被跳過？
- 人們在哪裡偏離 SOP？
- 哪些未記錄的步驟經常被執行？
- 交接失敗在哪裡發生？

---

## 9. 演化頁面

**路徑：** `/app/evolution`

演化頁面顯示工作流程變體的族群歸檔及其適應度。

### 9.1 族群歸檔

演化族群顯示：

- 所有工作流程變體（當前及歷史）
- 每個變體的適應度分數
- 血統（哪個變體衍生自哪個父體）
- 提升狀態（金絲雀、已提升、已退役、失敗）
- 與基線的比較

### 9.2 適應度指標儀表板

每個變體在多個維度上評分：

```text
F = w_q*Q + w_s*S + w_c*C + w_e*E + w_h*H - w_r*R - w_l*L - w_k*K
```

儀表板視覺化：
- 跨變體代次的品質分數趨勢
- 安全/合規分數（這些絕不可回歸）
- 效率改進（週期時間、成本）
- 人工滿意度評分
- 多目標優化的 Pareto 前沿

### 9.3 變體生命周期

```text
Proposed -> Testing -> Evaluated -> [Canary | Rejected]
  -> Monitoring -> [Promoted | Rolled Back | Retired]
```

```bash
# 透過 API 檢視演化歸檔
curl -b cookies.txt http://127.0.0.1:8000/api/v1/evolution/archive \
  | python3 -m json.tool
```

---

## 10. 帳戶管理

### 10.1 RBAC 模型

系統實施基於角色的存取控制，具有三個預定義角色：

| 角色 | 建立 | 運行 | 審批 | 配置 | 演化 |
|------|--------|-----|---------|-----------|--------|
| `admin` | 是 | 是 | 是 | 是 | 是 |
| `operator` | 是 | 是 | 否 | 否 | 否 |
| `reviewer` | 否 | 否 | 是 | 否 | 否 |

### 10.2 建立用戶帳戶

**作為管理員：**

```bash
# 建立操作員帳戶
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "email": "operator@company.com",
    "password": "strong-password-123",
    "role": "operator"
  }'

# 建立審查員帳戶
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "email": "reviewer@company.com",
    "password": "strong-password-456",
    "role": "reviewer"
  }'
```

### 10.3 會話管理

會話透過 HTTP-only cookie 管理：

| 設定 | 值 | 目的 |
|---------|-------|---------|
| Cookie 名稱 | `gso_access_token` | 認證令牌 |
| HTTP-only | `true` | 防止 JavaScript 存取（XSS 保護） |
| Secure | `true`（生產） | 需要 HTTPS |
| SameSite | `Strict` | 防止 CSRF 攻擊 |

**檢查你的當前會話：**

```bash
curl -b cookies.txt http://127.0.0.1:8000/api/v1/auth/me
# 返回：{"email": "admin@example.com", "role": "admin"}
```

**登出：**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/logout -b cookies.txt
# 使會話令牌無效
```

### 10.4 密碼管理

> **警告：** 在生產中始終使用強密碼。種子密碼 `admin-password` 有意設為弱密碼且必須更改。

```bash
# 更改密碼（作為已登入用戶）
curl -X POST http://127.0.0.1:8000/api/v1/auth/change-password \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "current_password": "admin-password",
    "new_password": "new-strong-password-789"
  }'
```

### 10.5 靜態令牌（僅限開發）

靜態 bearer 令牌用於快速 curl 測試：

```bash
# 使用靜態令牌（僅限開發）
curl -H "Authorization: Bearer admin-token" \
  http://127.0.0.1:8000/api/v1/workflows
```

> **警告：** 靜態令牌（`admin-token` 等）繞過適當的會話管理。它們僅用於開發期間的 curl 冒煙測試。絕不要在生產中或自動化整合中使用。

---

## 11. 操作員運行時流程（E1 路徑）

標準操作員運行時流程（E1）展示完整系統的運作：

### 步驟 1：登入

使用密碼認證登入（產生會話 cookie）。

### 步驟 2：列出工作流程及代理

導航到工作流程及代理頁面查看可用資源。

### 步驟 3：建立代理/工作流程

使用真實表單（Zod + React Hook Form 驗證）或使用旗艦 `wf_customer_onboarding_v12`。

### 步驟 4：立即運行

使用有效有效負載點擊 **Run Now**（旗艦需要 `case_id`）。

### 步驟 5：審批人工閘門步驟

作為審查員，審批觸發人工閘門的帳單步驟。

### 步驟 6：檢查結果

檢視審計日誌、記憶寫入、評估及流程摘要。

### 步驟 7：改進

在運行詳情頁面，點擊 **Improve** 進入自我改進流程：
- 對運行進行反思
- 提出工作流程變體
- 對黃金任務進行評估
- 金絲雀部署（或運行完整流程）

### 步驟 8：檢視演化

導航到 `/app/evolution` 查看帶有適應度分數的族群歸檔。

---

## 12. 真實使用案例

### 使用案例 1：日常運營監控

**場景：** 運營經理希望有一個早晨例行程序來檢查系統健康及審查待處理審批。

**導航工作流程：**

1. 登入 `http://localhost:3000`
2. 檢查 **Runs** 頁面 -- 審查夜間任何失敗或卡住的運行
3. 檢查 **Approvals** 頁面 -- 審批或升級待處理的人工閘門
4. 檢查 **Evaluations** 頁面 -- 審查任何回歸測試失敗
5. 檢查 **Processes** 頁面 -- 尋找新的瓶頸偵測
6. 審查 **Evolution** 頁面 -- 檢查是否有變體準備提升

**腳本化監控的 API 等效：**

```bash
#!/bin/bash
# morning-check.sh

echo "=== System Health ==="
curl -s http://127.0.0.1:8000/api/v1/health/ready | python3 -m json.tool

echo "=== Pending Approvals ==="
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/approvals?status=pending" | python3 -m json.tool

echo "=== Failed Runs (last 24h) ==="
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/runs?status=failed&since=24h" | python3 -m json.tool

echo "=== Evolution Candidates ==="
curl -s -b cookies.txt \
  http://127.0.0.1:8000/api/v1/evolution/archive | python3 -m json.tool
```

### 使用案例 2：入職合規審查員

**場景：** 新合規官員需要存取權限來審批工作流程步驟，但不能建立或修改代理/工作流程。

**步驟：**

1. 作為管理員，建立審查員帳戶：
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"email": "compliance@company.com", "password": "secure-pwd", "role": "reviewer"}'
```

2. 審查員現在可以：
   - 檢視所有頁面（代理、工作流程、運行等）
   - 在審批頁面審批或拒絕人工閘門步驟
   - 檢視審計日誌及評估結果
   - 不能建立或修改代理、工作流程或系統配置

3. 培訓審查員：
   - 如何閱讀審批上下文及證據
   - 何時審批、升級或拒絕
   - 如何添加審查員備註用於審計軌跡

### 使用案例 3：開發者整合測試

**場景：** 開發者希望使用 UI 及 API 端到端測試新工作流程。

**步驟：**

1. 透過工作流程頁面（UI）建立新工作流程
2. 透過 API 使用測試資料運行：
```bash
curl -X POST http://127.0.0.1:8000/api/v1/runs \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"workflow_id": "wf_test_v1", "payload": {"case_id": "test_001"}}'
```
3. 在運行頁面（UI）監控執行
4. 在審批頁面（UI）審批任何人工閘門
5. 在運行詳情頁面（UI）觸發改進：
   - 點擊 Improve -> Reflect
   - 審查反思輸出
   - 點擊 Propose 生成變體
6. 檢查演化頁面的新變體
7. 從 API 運行評估：
```bash
curl -X POST http://127.0.0.1:8000/api/v1/loops/run -b cookies.txt
```

---

## 13. 最佳實踐

1. **一致使用側邊欄導航** -- 每個部分對應特定的系統功能。避免收藏繞過上下文的深層連結。

2. **每日檢查審批** -- 待處理的人工閘門會阻塞工作流程完成。無人處理的審批造成瓶頸。

3. **演化運行後審查評估** -- 在提升任何變體之前，驗證其評估分數達到你的品質標準。

4. **適當使用角色** -- 不要給每個人管理員存取權限。職責分離（操作員建立、審查員審批）是治理要求。

5. **監控演化頁面** -- 它顯示你自我改進流程的健康狀況。陳舊的族群表示系統未在學習。

6. **利用流程智能** -- 流程頁面揭示工作實際如何進行，通常與已記錄的程序不同。將此用於工作流程設計。

7. **保持會話安全** -- 完成後登出，使用強密碼，並確保生產中設定了 `Secure` cookie 旗標（需要 HTTPS）。

8. **使用 API 端點進行自動化** -- 雖然 UI 方便互動工作，但可重複的操作應使用帶有適當認證的 API。

---

## 14. 章節摘要

在本章中，你學會了導航完整的操作控制台：

- **八個導航部分：** Agents、Workflows、Runs、Approvals、Knowledge、Evaluations、Processes、Evolution
- **代理頁面：** 建立、配置及監控具有定義角色及工具權限的系統代理
- **工作流程頁面：** 管理 Workflow DNA 定義及觸發運行
- **運行頁面：** 監控執行、檢查審計軌跡及觸發改進流程
- **審批頁面：** 處理人工閘門審批請求（僅 admin/reviewer）
- **知識頁面：** 搜尋帶有來源追蹤的分層檢索系統
- **評估頁面：** 審查黃金任務結果及回歸指標
- **流程頁面：** 檢視已發現的流程、合規性及瓶頸
- **演化頁面：** 瀏覽族群歸檔及適應度指標
- **帳戶管理：** 建立用戶、分配角色（admin/operator/reviewer）、管理會話及理解認證模式
- **E1 操作員流程：** 登入、列出、建立、運行、審批、檢查、改進、演化

---

## 15. 知識檢查問答

**問題 1：** 操作控制台有多少個主要導航部分？

a) 5
b) 6
c) 8
d) 10

<details>
<summary>答案</summary>
<b>c)</b> 八個部分：Agents、Workflows、Runs、Approvals、Knowledge、Evaluations、Processes 及 Evolution。
</details>

---

**問題 2：** 哪個頁面顯示自我改進流程（Reflect、Propose、Evaluate、Canary）？

a) Evolution 頁面
b) 運行詳情頁面（透過 Improve 按鈕）
c) Workflows 頁面
d) Evaluations 頁面

<details>
<summary>答案</summary>
<b>b)</b> 自我改進流程透過點擊已完成運行詳情頁面的 <b>Improve</b> 按鈕存取。Evolution 頁面顯示結果（族群歸檔）但流程是從運行詳情觸發的。
</details>

---

**問題 3：** 哪些角色可以審批人工閘門工作流程步驟？

a) 僅 admin
b) Admin 及 operator
c) Admin 及 reviewer
d) 所有角色

<details>
<summary>答案</summary>
<b>c)</b> 只有 <code>admin</code> 及 <code>reviewer</code> 角色可以審批或拒絕人工閘門步驟。<code>operator</code> 角色可以檢視審批佇列但不能採取行動。
</details>

---

**問題 4：** 演化頁面的族群歸檔顯示什麼？

a) 所有待處理審批
b) 帶有適應度分數、血統及提升狀態的工作流程變體
c) 知識庫條目
d) 代理配置歷史

<details>
<summary>答案</summary>
<b>b)</b> 族群歸檔顯示所有工作流程變體（當前及歷史），包括其適應度分數、血統（父子關係）、提升狀態（金絲雀、已提升、已退役）及與基線的比較。
</details>

---

**問題 5：** 透過系統的標準操作員路徑（E1）是什麼？

a) 建立、運行、完成
b) 登入、列出、建立、運行、審批、檢查、改進、演化
c) 配置、部署、監控
d) 安裝、設定、運行

<details>
<summary>答案</summary>
<b>b)</b> E1 操作員路徑是：登入（密碼）、列出工作流程/代理、建立代理/工作流程、使用有效負載立即運行、審批人工閘門步驟、檢查結果（審計/記憶/評估）、改進（反思/提議/評估/金絲雀）及檢視演化。
</details>

---

**問題 6：** 在哪裡可以找到流程探勘結果（從事件日誌中發現的工作流程）？

a) Knowledge 頁面
b) Workflows 頁面
c) Processes 頁面
d) Evolution 頁面

<details>
<summary>答案</summary>
<b>c)</b> Processes 頁面（<code>/app/processes</code>）顯示流程智能輸出，包括已發現的流程、合規報告及瓶頸分析。
</details>

---

**問題 7：** 前端用什麼表單驗證技術進行代理/工作流程建立？

a) jQuery validate
b) 原生 HTML5 驗證
c) Zod 結構配合 React Hook Form
d) Formik 配合 Yup

<details>
<summary>答案</summary>
<b>c)</b> 前端使用 Zod 結構驗證配合 React Hook Form（RHF）進行所有建立表單。驗證錯誤包含 <code>request_id</code> 用於除錯。
</details>

---

## 下一節

你已完成**第一節：核心系統基礎**。你現在對系統架構、安裝、設定、配置及透過操作控制台的日常操作有了紮實的理解。

繼續閱讀**第二節：中級工作流程**，從[第 02-01 章：Workflow DNA 編寫](02-01-workflow-dna-authoring.md)開始，學習如何從零開始建立生產級工作流程定義。
