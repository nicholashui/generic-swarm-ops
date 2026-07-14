# 第 01-04 章：首次配置

![Configuration Overview](../assets/01-04-configuration-overview.svg)

## 學習目標

在完成本章後，你將能夠：

1. 使用種子憑證登入並理解認證模式
2. 為生產環境配置密碼認證
3. 設定初始代理定義並分配角色
4. 建立你的第一個 Workflow DNA 定義
5. 運行業務層驗證命令以驗證配置完整性
6. 理解配置層之間的關係（環境、後端、前端、業務制品）

## 先決條件

- 已完成[第 01-03 章](01-03-initial-setup-wizard.md)且所有服務正在運行
- 後端可在 `http://127.0.0.1:8000` 存取
- 前端可在 `http://localhost:3000` 存取
- PostgreSQL 資料庫已連接（健康端點顯示 `"database": "postgres"`）
- 業務制品已初始化（`npm run business:init` 已完成）

---

## 1. 種子登入及認證

系統隨附種子憑證用於初始存取。理解認證模型對安全操作至關重要。

### 1.1 種子憑證

預設管理員帳戶已預配置：

| 欄位 | 值 |
|-------|-------|
| 電子郵件 | `admin@example.com` |
| 密碼 | `admin-password` |
| 角色 | `admin`（完全存取） |

> **警告：** 這些僅用於開發。在生產環境中，首次登入後立即更改管理員密碼並停用靜態令牌。

### 1.2 認證方式

系統支持兩種認證方式：

| 方式 | 使用場景 | 安全級別 |
|--------|----------|---------------|
| **密碼登入** | 生產操作、瀏覽器存取 | 高（推薦） |
| **靜態 bearer 令牌** | 僅用於 curl 冒煙測試 | 低（僅限開發） |

**密碼登入**產生的會話包含：
- `gso_access_token` cookie（HTTP-only、secure）
- 用於前端狀態的會話用戶 cookie
- 自動會話過期及續期

**靜態令牌**（如 `admin-token`）僅存在於開發期間的快速 curl 測試，絕不應在生產中使用。

### 1.3 逐步指引：首次登入

#### 透過前端控制台

1. 在瀏覽器中打開 `http://localhost:3000`
2. 輸入電子郵件：`admin@example.com`
3. 輸入密碼：`admin-password`
4. 點擊「Sign In」
5. 你應被重定向到主儀表板

#### 透過 API

```bash
# 透過 API 登入
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}' \
  -c cookies.txt

# 使用會話 cookie 進行後續請求
curl -b cookies.txt http://127.0.0.1:8000/api/v1/workflows
```

**登入的預期回應：**
```json
{
  "status": "authenticated",
  "user": {
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

### 1.4 理解角色

RBAC 系統定義三個角色：

| 角色 | 權限 | 預期用戶 |
|------|------------|---------------|
| `admin` | 完全存取：建立、運行、審批、配置、演化 | 系統管理員 |
| `operator` | 建立代理/工作流程、運行工作流程、檢視結果 | 日常操作員 |
| `reviewer` | 審批人工閘門步驟、檢視審計日誌 | 合規審查員 |

> **注意：** 角色分配儲存在 `runtime_state` 資料庫中。種子安裝僅建立 `admin` 角色。可透過 API 或操作控制台建立額外的用戶及角色。

---

## 2. 密碼認證設定

對於生產環境，配置適當的密碼認證。

### 2.1 理解認證流程

```text
User submits email + password
    |
    v
POST /api/v1/auth/login
    |
    v
Backend verifies credentials against stored hash
    |
    v
On success: Set gso_access_token cookie + session user cookie
    |
    v
Frontend stores session, enables navigation
```

### 2.2 建立額外用戶

要在種子管理員之外添加用戶：

```bash
# 透過 API 建立新的操作員用戶
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_session_token>" \
  -d '{
    "email": "operator@company.com",
    "password": "secure-password-here",
    "role": "operator"
  }'
```

### 2.3 建立審查員帳戶

```bash
# 建立審查員用於人工閘門審批
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -H "Cookie: gso_access_token=<your_session_token>" \
  -d '{
    "email": "reviewer@company.com",
    "password": "secure-password-here",
    "role": "reviewer"
  }'
```

### 2.4 會話管理

會話透過 cookie 管理：

| Cookie | 目的 | 屬性 |
|--------|---------|------------|
| `gso_access_token` | 認證令牌 | HTTP-only、Secure、SameSite |
| Session user | 前端顯示狀態 | JavaScript 可讀 |

```bash
# 檢查當前會話
curl -b cookies.txt http://127.0.0.1:8000/api/v1/auth/me

# 預期回應：
# {"email": "admin@example.com", "role": "admin"}
```

> **提示：** 偏好密碼登入而非靜態令牌。靜態令牌（`admin-token`）繞過適當的會話管理，應僅用於開發期間的快速 curl 冒煙測試。

---

## 3. 初始代理配置

代理是系統的執行單元。每個代理都有定義的角色、工具存取權限及行為約束。

### 3.1 理解代理名冊

系統定義兩類代理：

**控制/元代理：**

| 代理 | 目的 |
|-------|---------|
| Business Orchestrator | 路由工作、管理狀態、擁有全域目標 |
| Evolution Manager | 提出並測試變體（僅限沙箱） |
| Evaluation Harness | 運行黃金/回歸/對抗/重放測試套件 |
| Governance Officer | 施加風險等級、審批規則、審計要求 |
| Security Red-Team | 測試注入、工具濫用、洩漏、不安全自主 |
| Memory Steward | 維護記憶品質、來源、過期 |
| Tool Permission Broker | 授予有範圍的、臨時的工具存取 |
| Incident Commander | 處理故障、回滾、事後覆盤 |

**學習代理：**

| 代理 | 目的 |
|-------|---------|
| Expert Shadow | 觀察專家（經許可） |
| Cognitive Task Analyst | 將訪談轉化為決策卡片 + 啟發法 |
| Process Miner | 從日誌中發現工作流程 |
| Task Mining Agent | 觀察已許可的 UI/人工任務軌跡 |
| Conformance Agent | 比較 SOP 與觀察到的行為 |
| Bottleneck Analyzer | 發現延遲、循環及交接失敗 |
| Causal Improvement Agent | 從證據中提出沙箱實驗 |
| Knowledge Distiller | 將原始材料轉化為規則/技能/操作手冊 |
| Knowledge Curator | 驗證、去重、組織 |

### 3.2 建立你的第一個代理

使用操作控制台或 API 建立代理：

#### 透過操作控制台

1. 在側邊欄中導航到 **Agents**
2. 點擊 **Create Agent**
3. 填寫表單：
   - **Name:** `customer_support_agent`
   - **Role:** `execution`
   - **Description:** `Handles customer support ticket routing and initial response`
   - **Tools:** `["email", "crm", "knowledge_retriever"]`
   - **Risk Tier:** `3`（執行可逆）
4. 點擊 **Save**

#### 透過 API

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "customer_support_agent",
    "role": "execution",
    "description": "Handles customer support ticket routing and initial response",
    "tools": ["email", "crm", "knowledge_retriever"],
    "risk_tier": 3,
    "constraints": {
      "max_actions_per_run": 10,
      "require_human_gate_for": ["irreversible_actions"],
      "memory_scope": ["episodic", "semantic"]
    }
  }'
```

**預期回應：**
```json
{
  "id": "agent_customer_support_001",
  "name": "customer_support_agent",
  "role": "execution",
  "status": "active",
  "created_at": "2026-07-06T14:00:00Z"
}
```

### 3.3 代理配置最佳實踐

1. **最小權限原則** -- 僅授予代理實際需要的工具
2. **設定明確的風險等級** -- 更高等級需要更多監督
3. **定義記憶範圍** -- 限制代理可以讀寫的記憶類型
4. **設定操作限制** -- 使用 `max_actions_per_run` 防止失控執行
5. **記錄目的** -- 清晰的描述有助於治理審查

---

## 4. 首個 Workflow DNA 建立

Workflow DNA 是定義業務流程的核心抽象。你的第一個工作流程應足夠簡單以驗證系統端到端運作。

### 4.1 理解 Workflow DNA 結構

每個 Workflow DNA 必須聲明：

```yaml
workflow_dna:
  id: "unique_workflow_identifier"
  name: "Human-readable name"
  domain: "business_domain"
  objective: "What this workflow achieves"
  owner: "business_orchestrator"
  version: "1.0"
  inputs: ["required_input_data"]
  preconditions: ["conditions_that_must_be_true"]
  steps: [...]            # 有界執行步驟
  guardrails: {...}       # 人工審批條件
  verification: {...}     # 必需的執行後檢查
  rollback: {...}         # 可逆性計劃
  fitness_metrics: [...]  # 如何衡量成功
```

### 4.2 建立簡單工作流程

讓我們建立一個基本的「文件審查」工作流程作為你的第一個 Workflow DNA：

#### 透過操作控制台

1. 在側邊欄中導航到 **Workflows**
2. 點擊 **Create Workflow**
3. 填寫表單：

```yaml
# 文件審查的 Workflow DNA
id: "wf_document_review_v1"
name: "Document Review"
domain: "operations"
objective: "Review and approve submitted documents with compliance checks."
owner: "business_orchestrator"
version: "1.0"
inputs: ["document_id", "submitter_id", "document_type"]
preconditions:
  - "document_status == submitted"
  - "submitter_id is valid"
steps:
  - id: "classify_document"
    agent: "knowledge_distiller"
    tools: ["document_classifier"]
    description: "Determine document type and applicable rules"
  - id: "compliance_check"
    agent: "governance_officer"
    tools: ["policy_retriever", "compliance_checker"]
    description: "Verify document meets compliance requirements"
  - id: "human_review"
    agent: "business_orchestrator"
    tools: []
    description: "Human reviewer approves or rejects"
    human_gate: true
  - id: "finalize"
    agent: "business_orchestrator"
    tools: ["document_store", "notification"]
    description: "Store approved document and notify submitter"
guardrails:
  human_approval_required_if:
    - "compliance_check.risk_score > 0.7"
    - "document_type == confidential"
verification:
  required_checks:
    - "document_classified"
    - "compliance_verified"
    - "human_approved"
    - "audit_log_complete"
rollback:
  reversible: true
  rollback_steps: ["revert_document_status", "notify_submitter_of_rejection"]
fitness_metrics:
  - "review_cycle_time"
  - "compliance_pass_rate"
  - "rejection_rate"
```

#### 透過 API

```bash
curl -X POST http://127.0.0.1:8000/api/v1/workflows \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "id": "wf_document_review_v1",
    "name": "Document Review",
    "domain": "operations",
    "objective": "Review and approve submitted documents with compliance checks.",
    "version": "1.0",
    "inputs": ["document_id", "submitter_id", "document_type"],
    "steps": [
      {"id": "classify_document", "agent": "knowledge_distiller", "tools": ["document_classifier"]},
      {"id": "compliance_check", "agent": "governance_officer", "tools": ["policy_retriever"]},
      {"id": "human_review", "agent": "business_orchestrator", "human_gate": true},
      {"id": "finalize", "agent": "business_orchestrator", "tools": ["document_store"]}
    ],
    "guardrails": {
      "human_approval_required_if": ["compliance_check.risk_score > 0.7"]
    },
    "verification": {
      "required_checks": ["document_classified", "compliance_verified", "audit_log_complete"]
    },
    "rollback": {
      "reversible": true,
      "rollback_steps": ["revert_document_status"]
    },
    "fitness_metrics": ["review_cycle_time", "compliance_pass_rate"]
  }'
```

### 4.3 理解旗艦工作流程

系統隨附旗艦工作流程：`wf_customer_onboarding_v12`。研究其結構以理解生產級 Workflow DNA：

```bash
# 檢視旗艦工作流程
curl -b cookies.txt http://127.0.0.1:8000/api/v1/workflows/wf_customer_onboarding_v12 \
  | python3 -m json.tool
```

旗艦工作流程的關鍵特性：
- **4 個有界步驟**具有明確的代理及工具分配
- **記憶讀取**來自 `contract_rules`、`customer_exceptions`、`past_failures`
- **記憶寫入**到 `event_log`、`decision_memory`、`lessons_learned`
- **人工閘門**用於高風險、合約例外及不可逆操作
- **驗證** CRM 記錄、帳單配置、歡迎套件及審計日誌
- **回滾計劃**包含具體的逆轉步驟
- **6 個適應度指標**用於演化追蹤

---

## 5. 業務層驗證

配置代理及工作流程後，驗證整個業務層以確保一致性及完整性。

### 5.1 運行驗證

```bash
# 從倉庫根目錄
npm run business:validate
```

**檢查內容：**
- 所有治理制品存在且符合結構
- 評估黃金任務格式正確（最少需要 20 個）
- Workflow DNA 定義具有必填欄位
- 制品之間的交叉引用正確解析
- 安全基線已就位

**預期輸出（成功）：**
```text
Validating business artifacts...
  governance: PASS
  evals: PASS (20+ golden tasks)
  evolution: PASS
  security: PASS
  knowledge-base: PASS
All validations passed.
```

### 5.2 治理驗證

```bash
npm run business:governance
```

**檢查內容：**
- AI 清單已填充
- 活躍工作流程有風險等級分配
- 人工審批策略涵蓋所有 tier-4+ 操作
- 審計日誌保留策略已定義
- AI 組件有模型卡片
- 保證案例已記錄

### 5.3 安全驗證

```bash
npm run business:security
```

**檢查內容：**
- 暴露介面有威脅模型
- 工具權限已定義（允許列表）
- 提示詞注入測試夾具已存在
- 紅隊結果已記錄
- 事件回應計劃存在

### 5.4 演化就緒檢查

```bash
npm run business:evolution:check
```

**檢查內容：**
- Workflow DNA 定義具有適應度指標
- 黃金任務覆蓋率足以進行演化評估
- 基線測量值存在用於比較
- 沙箱配置有效

### 5.5 評估乾跑

```bash
npm run business:eval -- --dry-run
```

**功能：**
- 從 `business/evals/golden-tasks/` 載入所有黃金任務
- 驗證每個任務定義
- 報告哪些工作流程有評估覆蓋
- 不實際執行評估（乾跑模式）

---

## 6. 配置層說明

系統使用分層配置模型，每層服務於不同的目的：

### 6.1 第 1 層：系統環境變量

這些在作業系統層級控制基礎設施行為：

```bash
GENERIC_SWARM_AUTO_REFLECT=true      # 在終端運行時自動反思
GENERIC_SWARM_LLM_CRITIC_ENABLED=false  # 可選 AI 評審
GENERIC_SWARM_EMBEDDINGS_ENABLED=false  # 嵌入檢索
GENERIC_SWARM_PGVECTOR_ENABLED=false    # pgvector 擴展
```

### 6.2 第 2 層：後端 .env

資料庫連接及後端特定設定：

```bash
# backend/.env
DATABASE_URL=postgresql://user:pass@localhost:5432/generic_swarm_ops
NEO4J_URI=bolt://localhost:7687  # 可選
```

### 6.3 第 3 層：前端環境

前端路由及模式配置：

```bash
NEXT_PUBLIC_DEMO_MODE=false
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

### 6.4 第 4 層：業務制品

儲存在 `business/` 目錄中的聲明式配置：

```text
business/governance/         - 風險等級、審批策略、清單
business/evals/              - 黃金任務、回歸測試
business/evolution/          - Workflow DNA、變體、教訓
business/security/           - 威脅模型、權限
business/knowledge-base/     - 規則、來源追蹤、檢索策略
```

> **注意：** 配置層按順序套用。環境變量覆蓋預設值。後端 .env 提供資料庫連接。前端 env 控制 UI 模式。業務制品定義聲明式治理及評估配置。

---

## 7. 驗證你的配置

### 步驟 1：完整健康檢查

```bash
curl -s http://127.0.0.1:8000/api/v1/health/ready | python3 -m json.tool
```

確認：`"database": "postgres"`

### 步驟 2：認證測試

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}' \
  -c cookies.txt

# 驗證會話
curl -b cookies.txt http://127.0.0.1:8000/api/v1/auth/me
```

### 步驟 3：代理列表

```bash
curl -b cookies.txt http://127.0.0.1:8000/api/v1/agents | python3 -m json.tool
```

### 步驟 4：工作流程列表

```bash
curl -b cookies.txt http://127.0.0.1:8000/api/v1/workflows | python3 -m json.tool
```

### 步驟 5：業務驗證套件

```bash
npm run business:validate
npm run business:governance
npm run business:security
npm run business:evolution:check
```

所有命令都應無錯誤通過。

---

## 8. 真實使用案例

### 使用案例 1：入職新團隊成員

**場景：** 新操作員加入團隊，需要權限運行工作流程但不能審批敏感操作。

**配置步驟：**

```bash
# 1. 建立操作員帳戶
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "email": "newoperator@company.com",
    "password": "secure-password",
    "role": "operator"
  }'

# 2. 操作員現在可以：
#    - 建立及運行工作流程
#    - 檢視代理活動及運行結果
#    - 不能審批人工閘門步驟（需要 reviewer 角色）
#    - 不能修改系統配置（需要 admin 角色）
```

**治理意涵：** `operator` 角色自動繼承 `business/governance/human-approval-policy/` 中定義的約束。他們可以執行 tier-3（可逆）操作但不能審批 tier-4（閘門）操作。

### 使用案例 2：設定合規工作流程

**場景：** 法律團隊需要一個工作流程，透過多個審批閘門路由合約審查，並具有完整的審計軌跡。

**配置步驟：**

```yaml
# 合約合規的 Workflow DNA
workflow_dna:
  id: "wf_contract_compliance_v1"
  name: "Contract Compliance Review"
  domain: "legal_operations"
  objective: "Ensure all contracts meet regulatory and internal compliance requirements."
  owner: "business_orchestrator"
  version: "1.0"
  inputs: ["contract_id", "customer_id", "contract_value"]
  preconditions:
    - "contract_status == pending_review"
  steps:
    - id: "initial_screening"
      agent: "governance_officer"
      tools: ["contract_parser", "policy_retriever"]
    - id: "risk_assessment"
      agent: "governance_officer"
      tools: ["risk_scorer"]
    - id: "legal_review"
      agent: "business_orchestrator"
      human_gate: true
      description: "Senior counsel reviews high-value or high-risk contracts"
    - id: "final_approval"
      agent: "business_orchestrator"
      human_gate: true
      description: "Contract manager signs off"
    - id: "archive"
      agent: "business_orchestrator"
      tools: ["document_store", "audit_writer"]
  guardrails:
    human_approval_required_if:
      - "contract_value > 250000"
      - "risk_assessment.score > 0.8"
      - "jurisdiction not in approved_list"
  verification:
    required_checks:
      - "screening_complete"
      - "risk_assessed"
      - "legal_reviewed"
      - "approval_documented"
      - "audit_log_complete"
  rollback:
    reversible: true
    rollback_steps: ["revert_contract_status", "notify_stakeholders"]
  fitness_metrics:
    - "review_cycle_time"
    - "compliance_pass_rate"
    - "escalation_rate"
    - "cost_per_review"
```

### 使用案例 3：配置自動反思

**場景：** 團隊希望系統自動從每次完成的工作流程運行中學習並儲存改進建議。

**配置：**

```bash
# 在環境中啟用自動反思
export GENERIC_SWARM_AUTO_REFLECT=true

# 重啟後端以套用更改
# （或它預設已為 true）
```

**結果：** 每次工作流程運行到達終態（完成、失敗或逾時）後，系統自動：

1. 調用 `POST /api/v1/improvement/reflect/{run_id}`
2. 分析什麼有效什麼失敗
3. 將教訓儲存在 `business/evolution/lessons-learned/`
4. 可選地提出工作流程改進（如果條件滿足）

```bash
# 檢視累積的教訓
curl -b cookies.txt http://127.0.0.1:8000/api/v1/improvement/lessons \
  | python3 -m json.tool
```

---

## 9. 最佳實踐

1. **立即更改種子憑證** -- `admin@example.com` / `admin-password` 組合是公開的。為生產設定強密碼。

2. **從一開始使用基於角色的存取** -- 即使在開發中，也建立單獨的操作員及審查員帳戶以測試 RBAC 行為。

3. **從簡單工作流程開始** -- 你的第一個 Workflow DNA 應該很小（2-3 步驟）以驗證系統運作。逐步增加複雜性。

4. **始終包含回滾計劃** -- 運行時拒絕沒有回滾規格的 DNA。從第一天就養成這個習慣。

5. **每次更改後運行驗證** -- `npm run business:validate` 及早捕獲錯誤。將其整合到你的開發工作流程中。

6. **清晰記錄代理目的** -- 治理審查需要理解每個代理做什麼及為什麼它有其分配的工具。

7. **監控自動反思輸出** -- 從自動反思中學到的教訓提供對工作流程效能及故障模式的寶貴洞察。

8. **保持適應度指標可測量** -- 如「品質」之類的抽象指標需要具體定義。使用如 `cycle_time_minutes` 或 `error_count` 的具體測量。

---

## 10. 章節摘要

在本章中，你為首次使用配置了系統：

- **認證：** 使用種子憑證（`admin@example.com` / `admin-password`）登入，理解了密碼與令牌認證，並學習了 RBAC 角色（admin、operator、reviewer）
- **代理：** 建立了具有定義角色、工具、風險等級及約束的第一個代理
- **工作流程：** 建立了具有步驟、護欄、驗證檢查、回滾計劃及適應度指標的第一個 Workflow DNA
- **驗證：** 運行了 `business:validate`、`business:governance`、`business:security` 及 `business:evolution:check` 以驗證配置完整性
- **配置層：** 理解了環境變量、後端 .env、前端 env 及業務制品如何協同工作

系統現在已完全配置，可以進行日常操作。

---

## 11. 知識檢查問答

**問題 1：** 種子登入憑證是什麼？

a) `root@system.local` / `password`
b) `admin@example.com` / `admin-password`
c) `system@generic-swarm.io` / `admin123`
d) `admin@admin.com` / `changeme`

<details>
<summary>答案</summary>
<b>b)</b> 種子憑證是 <code>admin@example.com</code> / <code>admin-password</code>。這些在生產中應立即更改。
</details>

---

**問題 2：** 哪個角色可以審批人工閘門工作流程步驟？

a) `operator`
b) `admin` 及 `reviewer`
c) 僅 `admin`
d) 任何已認證用戶

<details>
<summary>答案</summary>
<b>b)</b> <code>admin</code>（完全存取）及 <code>reviewer</code>（僅審批）都可以審批人工閘門步驟。<code>operator</code> 角色可以運行工作流程但不能審批閘門步驟。
</details>

---

**問題 3：** 密碼登入後哪個 cookie 儲存認證令牌？

a) `session_id`
b) `auth_token`
c) `gso_access_token`
d) `jwt_token`

<details>
<summary>答案</summary>
<b>c)</b> <code>gso_access_token</code> cookie 儲存認證令牌。它是 HTTP-only 及 secure 的，防止 JavaScript 從潛在的 XSS 攻擊中存取。
</details>

---

**問題 4：** 如果提交的 Workflow DNA 沒有回滾計劃會怎樣？

a) 它被接受並帶有警告
b) 它被運行時拒絕
c) 它在受限模式下運行
d) 系統自動生成預設回滾

<details>
<summary>答案</summary>
<b>b)</b> 運行時拒絕沒有回滾計劃的 Workflow DNA。這是確定性地實施以維護安全優先級。
</details>

---

**問題 5：** `npm run business:governance` 檢查什麼？

a) 程式碼格式化
b) 資料庫結構
c) AI 清單、風險等級、審批策略、模型卡片、保證案例
d) 前端路由

<details>
<summary>答案</summary>
<b>c)</b> <code>npm run business:governance</code> 驗證治理制品，包括 AI 清單、風險等級分配、人工審批策略、審計日誌保留、模型卡片及保證案例。
</details>

---

**問題 6：** 生產環境推薦的認證方式是什麼？

a) 靜態 bearer 令牌
b) 帶會話 cookie 的密碼登入
c) 標頭中的 API 金鑰
d) 使用外部提供商的 OAuth2

<details>
<summary>答案</summary>
<b>b)</b> 產生會話 cookie（<code>gso_access_token</code>）的密碼登入是推薦的方式。靜態令牌僅用於開發期間的 curl 冒煙測試，絕不應在生產中使用。
</details>

---

**問題 7：** 哪個環境變量控制自動運行後反思？

a) `GENERIC_SWARM_LLM_CRITIC_ENABLED`
b) `GENERIC_SWARM_AUTO_REFLECT`
c) `GENERIC_SWARM_EVOLUTION_ENABLED`
d) `AUTO_IMPROVE_MODE`

<details>
<summary>答案</summary>
<b>b)</b> <code>GENERIC_SWARM_AUTO_REFLECT</code>（預設：true）控制系統是否自動對已完成的運行進行反思並儲存教訓。
</details>

---

## 下一章

繼續閱讀[第 01-05 章：基本導航及帳戶管理](01-05-basic-navigation-account-management.md)以學習如何導航操作控制台及有效管理用戶帳戶。
