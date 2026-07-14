# 第 3.4 章：RBAC 與治理配置

## 學習目標

完成本章後，你將能夠：

1. 配置和分配風險層級（0-5）至工作流程步驟和代理
2. 設定具有 SLA 截止期限和升級路徑的人工審批政策
3. 使用最小權限允許清單配置工具權限控制
4. 管理 AI 清單（已註冊代理、使用案例、模型卡）
5. 為高風險（第 4 層以上）操作建立保證案例
6. 設定用於合規和事故回應的審計日誌
7. 將治理配置對齊 NIST AI RMF、ISO 42001 和 EU AI Act 要求

## 先決條件

- 已完成第 3.3 章（進階工作流程自動化）
- 管理員級別的 Generic Swarm Ops 實例存取權限
- 理解風險管理框架
- 熟悉審批佇列操作（第 3.2 章）
- 至少一個已註冊的 Domain Pack 含活躍代理

---

## 架構概覽

![治理風險層級](../assets/03-04-governance-risk-tiers.svg)

Generic Swarm Ops 中的治理建基於分層模型：風險層級定義自主性上限，審批政策定義閘門機制，工具權限強制執行最小權限，審計日誌提供合規驗證的軌跡。治理官是一個運行時組件，攔截工作流程執行以強制執行這些控制。

### 治理構件

系統在 `business/governance/` 下交付和維護以下治理構件：

| 構件 | 用途 | 更新頻率 |
|----------|---------|----------------|
| AI 清單 | 已註冊的代理和使用案例 | 代理註冊/啟動時 |
| 風險層級分配 | 每個步驟/代理的自主性階梯 | 工作流程建立/修改時 |
| 人工審批政策 | 閘門何時觸發、SLA 時間 | 政策變更時 |
| 模型卡 | 旗艦編排器狀態和能力 | 每季 |
| 保證案例 | 第 4/5 層的理由文件 | 層級分配前 |
| 工具權限控制 | 每個代理的最小權限允許清單 | 代理/工具註冊時 |
| 審計日誌 | 所有操作的僅附加記錄 | 持續（運行時） |

---

## 逐步指南：風險層級配置

### 步驟 1：理解自主性階梯

Generic Swarm Ops 定義了六個風險層級，形成自主性階梯：

| 層級 | 名稱 | 允許的行為 | 閘門要求 |
|------|------|-----------------|------------------|
| 0 | 觀察 | 僅記錄和摘要 | 無 |
| 1 | 建議 | 提出建議；人工執行 | 無 |
| 2 | 草案 | 準備構件；人工在發送/執行前批准 | 發送前審批 |
| 3 | 執行（可逆） | 若存在回滾且風險低則可執行 | 需要回滾計劃 |
| 4 | 執行 + 閘門 | 可執行，但人工批准關鍵步驟 | 人工閘門（SLA 限制） |
| 5 | 受限 | 在保證案例存在前不得自主行動 | 保證案例 + 審批 |

> **警告：** 第 5 層（受限）是最受約束的級別。它用於在已記錄的保證案例經過審查和批准之前不應發生任何自主行動的操作。這適用於臨床決策、超過閾值的金融交易，或任何具有潛在不可逆人類影響的操作。

### 步驟 2：分配風險層級至工作流程步驟

工作流程 DNA 檔案中的每個步驟都帶有風險層級分配：

```yaml
# Example: Configuring risk tiers for a customer onboarding workflow
workflow_id: wf_customer_onboarding_v12
domain: ops
risk_tier: 3  # Overall workflow risk tier (highest of any step)

steps:
  - id: intake
    agent: ops.intake_agent
    action: receive_application
    risk_tier: 0  # Observe only - just logging the incoming request

  - id: kyc_check
    agent: ops.kyc_agent
    action: verify_identity
    risk_tier: 1  # Recommend - suggests verification result, human confirms

  - id: credit_assessment
    agent: ops.credit_agent
    action: assess_creditworthiness
    risk_tier: 2  # Draft - prepares credit report, human reviews before sharing

  - id: account_creation
    agent: ops.account_agent
    action: create_account
    risk_tier: 3  # Execute (reversible) - can create account because it can be deleted
    rollback_action: delete_account

  - id: billing_setup
    agent: ops.billing_agent
    action: setup_billing
    risk_tier: 4  # Execute + gate - irreversible financial action, human approves
    requires_approval: true
    approval_role: billing_reviewer
    approval_sla_minutes: 60
```

### 步驟 3：分配風險層級至代理

代理也帶有風險層級，作為其自主行為的上限：

```bash
# Set agent risk tier via API
curl -X PATCH http://127.0.0.1:8000/api/v1/agents/ops.billing_agent \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "risk_tier": 4,
    "risk_justification": "Handles financial transactions that cannot be reversed after 24h"
  }'
```

> **備註：** 若代理的風險層級低於步驟的風險層級，步驟的層級勝出（最嚴格）。代理不能被分配到超出其配置層級的步驟，除非有明確覆寫和保證案例。

### 步驟 4：配置步驟級別層級覆寫

對於特定情境，你可能需要覆寫預設層級：

```yaml
steps:
  - id: emergency_override
    agent: ops.account_agent
    action: freeze_account
    risk_tier: 3
    tier_override:
      condition: "customer.fraud_score > 0.95"
      override_tier: 4
      justification: "High fraud score requires human confirmation before freeze"
```

---

## 逐步指南：人工審批政策

### 步驟 5：定義審批政策

審批政策指定人工閘門何時觸發、誰可以批准，以及適用甚麼 SLA：

```json
{
  "policy_id": "approval_policy_onboarding",
  "workflow_id": "wf_customer_onboarding_v12",
  "rules": [
    {
      "trigger": "risk_tier >= 4",
      "approval_required": true,
      "approver_roles": ["billing_reviewer", "admin"],
      "sla_minutes": 60,
      "escalation": {
        "after_minutes": 45,
        "escalate_to": "admin",
        "notification_channels": ["email", "slack"]
      }
    },
    {
      "trigger": "step.id == 'billing_setup' AND payload.amount > 10000",
      "approval_required": true,
      "approver_roles": ["finance_director"],
      "sla_minutes": 120,
      "require_two_approvers": true
    },
    {
      "trigger": "step.external_api_call == true",
      "approval_required": false,
      "audit_level": "detailed",
      "notification": "team@example.com"
    }
  ],
  "default_sla_minutes": 60,
  "business_hours_only": false
}
```

### 步驟 6：配置升級路徑

當審批 SLA 即將到期時，系統會進行升級：

```json
{
  "escalation_policy": {
    "levels": [
      {
        "level": 1,
        "trigger_minutes": 45,
        "action": "notify",
        "targets": ["original_approver"],
        "channel": "email"
      },
      {
        "level": 2,
        "trigger_minutes": 55,
        "action": "escalate",
        "targets": ["admin"],
        "channel": ["email", "slack"]
      },
      {
        "level": 3,
        "trigger_minutes": 120,
        "action": "auto_reject",
        "reason": "SLA expired without approval",
        "notification": "incident_team@example.com"
      }
    ]
  }
}
```

> **提示：** 始終定義一個最終升級級別，要麼自動拒絕，要麼通知事故團隊。無限期待處理的審批會產生營運風險。

### 步驟 7：監控審批佇列

```bash
# View all pending approvals with SLA status
curl http://127.0.0.1:8000/api/v1/approvals \
  -H "Authorization: Bearer admin-token"
```

前端審批佇列可在 `/app/approvals` 存取，顯示：
- 按 SLA 緊急程度排序的待處理審批請求
- 每個閘門的上下文（甚麼操作、甚麼風險、甚麼資料）
- 一鍵批准/拒絕，附帶強制性備註
- SLA 倒計時和升級狀態

---

## 逐步指南：工具權限控制

### 步驟 8：配置代理工具允許清單

工具權限遵循最小權限原則。每個代理都有明確的可存取工具清單：

```json
{
  "agent_id": "my_domain.analysis_agent",
  "tool_permissions": {
    "allowed": [
      "my_domain.search",
      "my_domain.analyze",
      "knowledge.search",
      "knowledge.graph.query"
    ],
    "denied": [
      "my_domain.delete",
      "admin.*"
    ],
    "scope_restrictions": {
      "my_domain.search": {
        "max_results": 100,
        "allowed_indices": ["domain_docs", "public_knowledge"]
      }
    }
  }
}
```

### 步驟 9：強制執行工具命名空間

工具按領域命名空間以防止跨 Pack 存取：

```yaml
# Tool permission enforcement rules
tool_permissions:
  enforcement: "strict"  # Options: strict, warn, audit
  rules:
    - agents in "video.*" can only access tools in "video.*" and "shared.*"
    - agents in "research.*" can only access tools in "research.*" and "shared.*"
    - no agent can access "admin.*" tools without explicit override
    - wildcards are discouraged and logged as warnings
```

> **警告：** 工具適配器採用關閉失敗策略。若工具不在代理的允許清單中，呼叫會被拒絕並記錄。這是刻意設計的：系統偏好假陰性（阻止合法呼叫）而非假陽性（允許未授權存取）。

### 步驟 10：驗證工具權限

```bash
# Check what tools an agent can access
curl http://127.0.0.1:8000/api/v1/agents/my_domain.analysis_agent \
  -H "Authorization: Bearer admin-token" | jq '.tool_permissions'

# Run security scan on business artifacts
npm run business:security
```
---

## 逐步指南：AI 清單管理

### 步驟 11：查看 AI 清單

AI 清單追蹤所有已註冊的代理、其能力、風險分配和營運狀態：

```bash
# List all agents in the inventory
curl http://127.0.0.1:8000/api/v1/agents \
  -H "Authorization: Bearer admin-token"
```

**回應：**

```json
{
  "agents": [
    {
      "id": "ops.billing_agent",
      "domain": "ops",
      "status": "active",
      "risk_tier": 4,
      "alc_enabled": true,
      "last_active": "2024-01-15T10:30:00Z",
      "total_runs": 342,
      "tools_assigned": 5,
      "model_card_ref": "governance/model-cards/billing-agent.md"
    }
  ],
  "total": 120,
  "by_status": {"active": 98, "draft": 15, "inactive": 7},
  "by_risk_tier": {"0": 20, "1": 35, "2": 28, "3": 10, "4": 4, "5": 1}
}
```

### 步驟 12：建立模型卡

模型卡記錄代理的能力、限制和預期用途：

```markdown
# Model Card: ops.billing_agent

## Overview
- **Agent ID:** ops.billing_agent
- **Domain:** ops (Operations)
- **Risk Tier:** 4 (Execute + Gate)
- **Status:** Active
- **Last Updated:** 2024-01-15

## Intended Use
Automated billing account setup for new customers after all verification steps pass.

## Capabilities
- Create billing accounts in payment processor
- Set up recurring payment schedules
- Configure payment methods

## Limitations
- Cannot process refunds (requires admin action)
- Cannot modify existing billing for amounts > $50,000
- Requires human gate for all irreversible actions

## Ethical Considerations
- Financial transactions require full audit trail
- Customer consent must be verified before any billing action
- No discriminatory pricing decisions

## Performance Metrics
- Accuracy: 99.2% (based on 342 runs)
- Average processing time: 12 seconds
- Escalation rate: 3.5%
```

### 步驟 13：建立保證案例

對於第 4 層和第 5 層操作，保證案例記錄操作為何是安全的：

```json
{
  "assurance_case_id": "ac_billing_setup_001",
  "agent_id": "ops.billing_agent",
  "step_id": "billing_setup",
  "risk_tier": 4,
  "created_by": "admin@example.com",
  "created_at": "2024-01-10T09:00:00Z",
  "status": "approved",
  "claims": [
    {
      "claim": "Billing setup is bounded to verified customers only",
      "evidence": [
        "KYC verification passes before billing step (workflow enforced)",
        "Credit check confirms customer identity",
        "Two-step verification on payment method"
      ]
    },
    {
      "claim": "All actions are reversible within 24 hours",
      "evidence": [
        "Billing API supports account deletion within grace period",
        "Rollback action defined in workflow DNA",
        "Automated rollback tested in regression suite"
      ]
    },
    {
      "claim": "Human oversight prevents financial harm",
      "evidence": [
        "Human gate requires reviewer approval before execution",
        "SLA ensures timely review (60 minutes)",
        "Escalation to admin if SLA approaches expiry"
      ]
    }
  ],
  "risks_mitigated": [
    "Unauthorized billing",
    "Incorrect amount charging",
    "Customer identity fraud"
  ],
  "residual_risks": [
    "Payment processor outage (mitigated by retry logic)",
    "Reviewer fatigue on high-volume days (mitigated by escalation)"
  ],
  "review_cadence": "quarterly"
}
```

---

## 逐步指南：審計日誌

### 步驟 14：理解審計日誌結構

審計日誌是僅附加的，捕獲所有操作、工具呼叫、審批和進化事件：

```json
{
  "log_id": "audit_001",
  "timestamp": "2024-01-15T12:05:30Z",
  "event_type": "tool_execution",
  "agent_id": "ops.billing_agent",
  "run_id": "run_abc123",
  "step_id": "billing_setup",
  "action": "create_billing_account",
  "tool": "ops.billing_create",
  "tool_effects": {
    "type": "create",
    "resource": "billing_account",
    "resource_id": "ba_xyz789",
    "reversible": true,
    "reversal_window_hours": 24
  },
  "risk_tier": 4,
  "approved_by": "reviewer@example.com",
  "approval_id": "appr_xyz789",
  "request_id": "req_f47ac10b",
  "outcome": "success"
}
```

### 步驟 15：查詢審計日誌

```bash
# View audit logs (accessible at /app/audit-logs in frontend)
curl "http://127.0.0.1:8000/api/v1/audit-logs?run_id=run_abc123" \
  -H "Authorization: Bearer admin-token"

# Filter by event type
curl "http://127.0.0.1:8000/api/v1/audit-logs?event_type=approval&since=24h" \
  -H "Authorization: Bearer admin-token"

# Filter by agent
curl "http://127.0.0.1:8000/api/v1/audit-logs?agent_id=ops.billing_agent&limit=50" \
  -H "Authorization: Bearer admin-token"
```

> **備註：** 審計日誌為每次工具執行記錄持久的 `tool_effects`。這使事後分析代理採取了甚麼操作成為可能，並有足夠的細節來重建完整的執行歷史。

---

## 監管框架對齊

### 步驟 16：NIST AI RMF 映射

Generic Swarm Ops 治理映射到 NIST AI 風險管理框架：

| NIST 功能 | GSO 實作 |
|---------------|-------------------|
| **GOVERN** | 風險層級分配、審批政策、AI 清單 |
| **MAP** | 使用案例風險分層、模型卡、能力文件 |
| **MEASURE** | 適應度指標、評估語料庫、審計日誌 |
| **MANAGE** | 回滾計劃、事故回應、升級政策 |

### 步驟 17：ISO 42001 對齊

對於追求 ISO 42001（AI 管理系統）認證的組織：

| ISO 42001 要求 | GSO 構件 |
|-----------------------|-------------|
| AI 政策 | 治理配置 + 審批政策 |
| 風險評估 | 風險層級分配 + 保證案例 |
| 組織目標 | 模型卡 + 能力文件 |
| 能力 | 代理規格 + ALC 配置 |
| 監控和度量 | 審計日誌 + 適應度指標 |
| 內部審計 | 評估語料庫 + 治理審查佇列 |
| 管理審查 | 群體檔案 + 改善指標 |
| 持續改善 | 進化管線 + 自我改善迴圈 |

### 步驟 18：EU AI Act 考量

EU AI Act 按風險等級分類 AI 系統。關鍵考量：

| AI Act 類別 | GSO 映射 | 需要的行動 |
|-----------------|-------------|-----------------|
| 被禁止的實踐 | 不適用（無社會評分、操縱） | 記錄排除 |
| 高風險（附錄 III） | 就業決策、信用評分 | 第 4-5 層，附完整保證案例 |
| 有限風險 | 客戶互動、內容生成 | 第 2-3 層，附透明度通知 |
| 最低風險 | 內部記錄、摘要 | 第 0-1 層，標準審計 |

> **備註：** 若你的集群涉及與就業相關的決策（招募、績效評估、任務分配、晉升或終止），EU AI Act 將其歸類為高風險。這觸發風險管理、資料治理、技術文件、人工監督和上市後監控的要求。

對於高風險 AI Act 合規，確保：
- 完整可追溯性（審計日誌涵蓋每個決策點）
- 人工監督（第 4 層以上閘門，附 SLA 限制的審批）
- 技術文件（模型卡 + 保證案例）
- 準確性和穩健性測試（評估語料庫 + 對抗測試）
- 記錄保存（僅附加審計日誌，永不刪除）

---

## 治理驗證命令

```bash
# Run governance validation checks
npm run business:governance

# Run security controls check
npm run business:security

# Check evolution compliance
npm run business:evolution:check

# Full business validation (schemas + governance + security)
npm run business:validate
```

---

## 進階：審計日誌分析

### 識別治理缺口

使用審計日誌查詢識別治理配置缺口：

```bash
# Find steps executing without approval that should have gates
curl "http://127.0.0.1:8000/api/v1/audit-logs?event_type=tool_execution&risk_tier_min=4&approved_by=null" \
  -H "Authorization: Bearer admin-token"

# Find tool calls that were denied (potential misconfiguration)
curl "http://127.0.0.1:8000/api/v1/audit-logs?event_type=tool_denied&since=7d" \
  -H "Authorization: Bearer admin-token"

# Find escalation events (SLA pressure indicators)
curl "http://127.0.0.1:8000/api/v1/audit-logs?event_type=approval_escalated&since=30d" \
  -H "Authorization: Bearer admin-token"
```

### 審計日誌保留政策

不同的監管框架要求不同的保留期限：

| 法規 | 最低保留期 | GSO 配置 |
|-----------|-------------------|-------------------|
| SOX（金融） | 7 年 | `data_retention_days: 2555` |
| HIPAA（醫療） | 6 年 | `data_retention_days: 2190` |
| GDPR（EU 私隱） | 盡可能短 | `data_retention_days: 365`（或更少） |
| PCI-DSS（支付） | 1 年 | `data_retention_days: 365` |
| EU AI Act（高風險） | 使用期間 + 10 年 | `data_retention_days: 3650` |
| 內部合規 | 組織特定 | 按政策配置 |

> **警告：** 當多項法規適用於同一工作流程（例如受 HIPAA 和 PCI-DSS 管轄的醫療計費工作流程）時，使用最嚴格（最長）的保留期限。

### 從審計資料建立合規報告

```bash
# Generate a compliance summary for the last quarter
curl "http://127.0.0.1:8000/api/v1/audit-logs?since=90d&format=summary" \
  -H "Authorization: Bearer admin-token"
```

**範例摘要回應：**

```json
{
  "period": "2024-Q1",
  "total_events": 15420,
  "by_type": {
    "tool_execution": 8500,
    "approval_granted": 420,
    "approval_denied": 15,
    "tool_denied": 230,
    "evolution_event": 85,
    "login_event": 1200
  },
  "governance_metrics": {
    "approval_sla_compliance": 0.97,
    "mean_approval_time_minutes": 22,
    "escalation_rate": 0.03,
    "unauthorized_tool_attempts": 230,
    "all_blocked": true
  },
  "risk_tier_distribution": {
    "tier_0": 4200,
    "tier_1": 3100,
    "tier_2": 2800,
    "tier_3": 1500,
    "tier_4": 420,
    "tier_5": 0
  }
}
```
---

## 進階：事故回應

### AI 專用事故回應手冊

當治理偵測到異常時，遵循此手冊：

```markdown
## AI Incident Response Steps

1. **Detect** - Audit log alert fires (unauthorized tool attempt, SLA breach, or anomalous behavior)
2. **Contain** - Immediately elevate the agent's risk tier to 5 (Restricted)
3. **Assess** - Review the full audit trail for the affected agent and run
4. **Remediate** - Fix the root cause (tool permissions, approval policy, or agent configuration)
5. **Verify** - Run adversarial tests against the fix
6. **Restore** - Lower risk tier only after verification passes
7. **Document** - Update the assurance case with incident details and remediation
```

```bash
# Step 2: Emergency containment - restrict the agent
curl -X PATCH http://127.0.0.1:8000/api/v1/agents/my_domain.suspect_agent \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{"risk_tier": 5, "risk_justification": "INCIDENT-001: Elevated pending investigation"}'

# Step 3: Pull the audit trail
curl "http://127.0.0.1:8000/api/v1/audit-logs?agent_id=my_domain.suspect_agent&since=24h&limit=500" \
  -H "Authorization: Bearer admin-token" > incident_001_audit.json

# Step 5: Run adversarial evaluation
curl -X POST http://127.0.0.1:8000/api/v1/evolution/variants/var_fix/evaluate \
  -H "Authorization: Bearer admin-token"
```

---

## 疑難排解

### 常見治理問題

| 問題 | 症狀 | 解決方案 |
|-------|----------|------------|
| 審批閘門未觸發 | 第 4 層步驟未經審批即執行 | 驗證工作流程 DNA 中的 `requires_approval: true` |
| SLA 升級未觸發 | 截止期限接近時無通知 | 檢查升級政策配置和通知渠道 |
| 工具權限過於嚴格 | 代理無法完成步驟 | 審查工具允許清單；明確添加必要工具 |
| 審計日誌缺口 | 某些操作缺少事件 | 驗證審計中介軟件是否啟動；檢查錯誤日誌條目 |
| 保證案例被拒絕 | 無法啟動第 5 層操作 | 審查聲明和證據；確保所有風險都已解決 |
| 角色配置錯誤 | 用戶無法批准/拒絕 | 驗證用戶角色分配與政策中的 `approver_roles` 相符 |

### 除錯審批政策

```bash
# Check which policy applies to a specific step
curl "http://127.0.0.1:8000/api/v1/workflows/wf_customer_onboarding_v12" \
  -H "Authorization: Bearer admin-token" | jq '.steps[] | select(.id == "billing_setup") | {risk_tier, requires_approval, approval_role}'

# Check user roles
curl http://127.0.0.1:8000/api/v1/auth/me \
  -H "Authorization: Bearer admin-token" | jq '.role, .permissions'

# Verify pending approvals are visible to the correct role
curl http://127.0.0.1:8000/api/v1/approvals \
  -H "Authorization: Bearer reviewer-token"
```

---

## 真實使用案例

### 使用案例 1：金融服務合規

一家銀行為貸款審批工作流程配置治理：

```yaml
workflow_id: wf_loan_approval_v3
domain: banking
risk_tier: 4

steps:
  - id: application_review
    risk_tier: 1  # Recommend: suggest eligibility, human decides
    approval_policy:
      trigger: "always"
      approver_roles: ["loan_officer"]

  - id: credit_scoring
    risk_tier: 2  # Draft: prepare credit report
    audit_level: "detailed"
    data_retention_days: 2555  # 7 years for financial regulations

  - id: loan_decision
    risk_tier: 5  # Restricted: no autonomous lending decisions
    assurance_case_required: true
    human_decision_only: true

  - id: disbursement
    risk_tier: 4  # Execute + gate: irreversible financial transfer
    approval_policy:
      approver_roles: ["senior_loan_officer", "compliance_officer"]
      require_two_approvers: true
      sla_minutes: 240
```

關鍵治理決策：
- 貸款決策為第 5 層（受限），因為根據 EU AI Act，自主貸款決策屬高風險
- 撥款需要兩個批准者以處理不可逆金融轉帳
- 所有信用評分資料保留 7 年（監管要求）
- 每個步驟都有詳細審計日誌以用於合規驗證

### 使用案例 2：醫療營運治理

一個醫院系統為病人排程配置治理：

```json
{
  "workflow_id": "wf_patient_scheduling_v1",
  "domain": "healthcare_ops",
  "governance_config": {
    "overall_risk_tier": 3,
    "hipaa_mode": true,
    "data_classification": "phi",
    "steps": {
      "triage": {
        "risk_tier": 1,
        "note": "Advisory only - never makes clinical decisions"
      },
      "schedule_appointment": {
        "risk_tier": 3,
        "rollback_action": "cancel_appointment",
        "note": "Reversible - can always cancel"
      },
      "prescription_reminder": {
        "risk_tier": 4,
        "approval_required": true,
        "note": "Patient communication requires clinician review"
      }
    },
    "audit_config": {
      "retain_days": 2555,
      "phi_redaction": true,
      "access_logging": true
    }
  }
}
```

### 使用案例 3：具有動態風險層級的電子商務

一個線上零售商根據訂單金額使用條件風險層級：

```yaml
workflow_id: wf_order_fulfillment_v2
domain: ecommerce

steps:
  - id: order_processing
    risk_tier: 3  # Execute (reversible) - can cancel order
    tier_override:
      - condition: "order.total > 5000"
        override_tier: 4
        justification: "High-value orders require human confirmation"
      - condition: "customer.is_new AND order.total > 1000"
        override_tier: 4
        justification: "New customer large orders flagged for fraud review"

  - id: shipping
    risk_tier: 3
    tier_override:
      - condition: "shipping.international == true"
        override_tier: 4
        justification: "International shipping has customs and return complexity"

  - id: refund_processing
    risk_tier: 4  # Always gated - financial reversal
    approval_policy:
      approver_roles: ["customer_service_lead"]
      sla_minutes: 30
```

---

## 最佳實踐

### 風險層級分配

1. **從保守開始，之後放鬆。** 初始分配較高的風險層級，只有在審計日誌和評估指標提供充分證據後才降低。

2. **工作流程層級應等於最大步驟層級。** 絕不將整體工作流程風險層級設定為低於其最高風險步驟。

3. **記錄層級理由。** 每個第 3 層以上的分配都應有書面理由，解釋為甚麼該自主性級別是適當的。

4. **每季審查層級。** 隨着工作流程成熟和證據累積，應基於實際表現資料重新評估風險層級。

### 審批政策

5. **始終定義升級路徑。** 每個審批閘門都應有定義的 SLA 到期升級。無限期待處理的審批是營運失敗。

6. **對不可逆操作使用雙批准者規則。** 對於金融交易、資料刪除或外部通訊，要求兩個審查者的獨立確認。

7. **設定現實的 SLA。** 考慮營業時間、審查者可用性和操作的關鍵性。過於緊迫的 SLA 會導致審批疲勞。

### 工具權限

8. **預設拒絕，明確允許。** 每個工具存取都應明確授予。絕不在生產中使用萬用字元。

9. **限定工具參數範圍。** 超出二元允許/拒絕之外，限制參數（最大結果數、允許的索引、資源限制）以最小化爆炸半徑。

10. **審計工具使用模式。** 監控代理實際使用哪些工具與允許使用的工具。未使用的權限應被撤銷。

### 合規

11. **將每個工作流程映射到監管類別。** 部署前，確定適用哪些法規（EU AI Act、HIPAA、PCI-DSS 等）並相應配置。

12. **按法規保留審計日誌。** 不同法規有不同的保留要求。根據最嚴格的適用法規按步驟配置 `data_retention_days`。

13. **在評估語料庫中測試治理。** 在你的對抗測試集中包含治理特定的測試情境（審批超時、升級觸發、工具拒絕）。

---

## 本章摘要

在本章中，你學會了如何：

- 配置六個風險層級（0-5）並理解自主性階梯
- 將風險層級分配至工作流程步驟和代理
- 建立具有 SLA 截止期限和升級路徑的人工審批政策
- 使用命名空間化允許清單設定工具權限控制
- 使用模型卡和代理文件管理 AI 清單
- 為第 4/5 層操作建立保證案例
- 配置用於合規和事故回應的審計日誌
- 將治理對齊 NIST AI RMF、ISO 42001 和 EU AI Act
- 使用治理驗證命令驗證配置

治理系統確保增加的自主性始終受到成比例的監督限制。低風險操作（第 0-1 層）自由進行，中度操作（第 2-3 層）有護欄，高風險操作（第 4-5 層）需要在執行前明確的人工判斷。

---

## 知識檢查

1. **列出所有六個風險層級及其名稱和閘門要求。第 3 層和第 4 層之間的關鍵差異是甚麼？**

2. **若一個風險層級為 3 的代理被分配到風險層級為 4 的工作流程步驟會怎樣？哪個層級勝出？**

3. **描述升級政策結構。三個典型的升級級別是甚麼，每個採取甚麼行動？**

4. **為甚麼工具適配器「關閉失敗」？偏好假陰性而非假陽性的安全理由是甚麼？**

5. **甚麼是保證案例？何時需要一個，它必須包含甚麼？**

6. **審計日誌結構如何捕獲工具效果？為甚麼 `reversible` 和 `reversal_window_hours` 重要？**

7. **將四個 NIST AI RMF 功能（GOVERN、MAP、MEASURE、MANAGE）映射到具體的 GSO 構件。**

8. **根據 EU AI Act，哪些類型的 AI 使用案例被歸類為「高風險」？這需要甚麼 GSO 配置？**

9. **一個工作流程處理標準訂單（< $100）和高級訂單（> $5000）。你如何配置動態風險層級覆寫？**

10. **部署新工作流程前應運行哪些治理驗證命令？每個命令檢查甚麼？**
