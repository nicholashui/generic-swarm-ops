# Backend API Server 說明書

## 一本把 `backend_hk.md` 講清楚的後端設計書

> **實作現況（mark ~100）：** 本說明書源自 backend 計劃 `backend_hk.md`（英文原文 `backend.md`）。產品標竿已關閉：Postgres `runtime_state` 主控平面、本機 tool adapters + `tool_effects`、PI 磁碟產物、演化沙盒（corpus／canary／rollback）、自我改進（reflect／lessons／auto-propose／loops／skill sandbox）、K1-lite、生產 DNA 驗證、E1 操作路徑。  
> **SDD 規格包：** `planning/backend/`（`requirements.md`／`design.md`／`tasks.md`，BE-01–24；tasks **v2.2** 含 **Deliverable code paths**）。  
> **證據：** `status.md`、`backend/README.md`、`planning/gap_analysis_for_backend.md`（100/100）、`planning/backend/TASK_TO_CODE_TRACEABILITY.md`、`reviews/e1_operator_checklist.md`。  
> **前端契約：** `frontend.md` §33（營運台只經 `/api/v1` 呼叫本 backend）。

**來源文件：** `backend_hk.md`（backend 需求、設計與實作計劃；§24 為 as-built 實作對應）  
**英文對照：** `backend.md`  
**目的：** 把偏工程規格的內容，改寫成較容易閱讀、向管理層與跨職能團隊解釋，但仍保留核心技術資訊的說明書。  
**適合讀者：** 業務負責人、營運主管、架構師、安全與治理人員、後端／全端工程師，以及需要理解「控制平面如何落地」的人。

---

## 閱讀指南

這本書主要回答八個問題：

1. 這個 backend 到底是甚麼，為甚麼前端不能直接碰 agents 與資料庫？
2. 設計優先次序與核心原則如何約束每一個 API？
3. 系統邊界與高層架構如何把請求變成受治理的執行？
4. 認證、權限、使用者／組織、代理與工具如何組成安全底座？
5. Workflow DNA 如何定義、執行、關卡、回滾與串流？
6. 知識、記憶、評估、流程智能如何服務執行層？
7. 演化沙盒與自我改進為甚麼永遠不能直接改生產？
8. 本倉庫的 SDD 規格包（`planning/backend/`）與 as-built 程式如何對應 `backend_hk.md`？

內容順序：

1. 先定位 backend 的角色  
2. 再講目標、技術棧、邊界與原則  
3. 拆開功能域與 API 契約  
4. 最後補非功能需求、資料模型要點、完成定義，以及 **§14 實作對應（來源 §24）**

---

## 目錄

1. [Backend 是甚麼](#chapter-1)
2. [主要目標與技術棧](#chapter-2)
3. [系統邊界與高層架構](#chapter-3)
4. [核心設計原則](#chapter-4)
5. [安全底座：認證、授權、使用者與組織](#chapter-5)
6. [代理、工具與 Workflow DNA](#chapter-6)
7. [執行引擎：Run、步驟、關卡與串流](#chapter-7)
8. [治理、審計、知識、記憶與評估](#chapter-8)
9. [流程智能、演化沙盒與自我改進](#chapter-9)
10. [非功能需求與工程約束](#chapter-10)
11. [API 契約與資料模型要點](#chapter-11)
12. [資料夾結構與工程分層](#chapter-12)
13. [完成定義與操作證明](#chapter-13)
14. [實作對應：SDD 規格包與 as-built](#chapter-14)

---

<a id="chapter-1"></a>
## 1. Backend 是甚麼

### 1.1 最簡單的定義

Backend API Server 是 `structure.md`／`structure_hk.md` 所描述業務作業系統的 **受治理控制層**。

它透過安全的 API 對外暴露系統能力，讓前端、管理主控台、CLI、自動化工具或外部整合，可以安全地與：

- agents（代理）
- workflows（工作流程）
- knowledge／memory（知識與記憶）
- governance／approvals（治理與審批）
- evaluations（評估）
- audit logs（審計）
- process intelligence（流程智能）
- evolution sandbox（演化沙盒）
- self-improvement loops（自我改進）

互動。

### 1.2 前端不能直接做甚麼

前端 **不得** 直接存取：

- agents 執行環境  
- databases  
- workflow engines  
- LLM providers  
- vector stores  
- 內部工具  

所有存取都必須經由 Backend API Server。

簡而言之：

```text
Frontend = 使用者體驗層
Backend API = 受治理的智能與控制層
Agents = 專門化工作者
Workflows = 結構化業務執行路徑
Governance = 風險與審批控制
Audit = 信任與可追溯層
```

### 1.3 與架構文件的關係

- `structure_hk.md`：整體系統 **架構願景**（權威來源）  
- `backend_hk.md`／本書：如何把架構變成 **可執行的 API 控制平面**  
- `frontend.md`：營運台如何 **只透過 API** 操作系統  
- `planning/backend/`：把 backend 計劃拆成 01–24 個子功能（requirements／design／tasks）

---

<a id="chapter-2"></a>
## 2. 主要目標與技術棧

### 2.1 主要目標

建立一個 backend server，封裝系統架構的完整功能，並以 **版本化 API** 對外提供，至少支援：

- 安全驗證與 RBAC  
- agent 編排與登錄  
- workflow 定義、版本、執行與追蹤  
- 人類審批關卡  
- memory／knowledge 檢索  
- audit logging  
- evaluation 與品質檢查  
- process intelligence  
- evolution sandbox（propose → evaluate → canary → promote／rollback）  
- self-improvement（reflect、lessons、auto-propose、skill sandbox、loop runner）  
- 生產 DNA 安全檢查（activate／production_ready 前）  
- 背景／非阻塞長任務  
- 向前端串流更新  
- 可擴展整合  

### 2.2 建議技術棧（與 as-built）

規格建議：

```text
Backend Framework: FastAPI
Language: Python
Database: PostgreSQL（主控制平面；as-built：runtime_state JSONB）
Vector Search: pgvector（可選）等
Queue: Redis + Celery／Temporal（進階）；as-built：行程內執行引擎
Auth: JWT / OAuth2 / SSO-ready
API Style: REST first + SSE streaming
Documentation: OpenAPI from FastAPI
```

**產品標竿本地不強制 Docker。** 已配置 Postgres 時，JSON 檔只作 **備份／種子**，不是線上權威寫入路徑。

### 2.3 為何選 API First

前端與整合方只應依賴 **公開 API 契約**，不應依賴內部資料庫形狀或 agent 私有介面。契約變更必須版本化（`/api/v1`）。

---

<a id="chapter-3"></a>
## 3. 系統邊界與高層架構

### 3.1 Backend 擁有甚麼

Backend 擁有並控制：

- API 存取與身份驗證  
- 授權與權限  
- agent／workflow 執行請求  
- governance 檢查與審批關卡  
- audit 事件  
- knowledge／memory 存取  
- process intelligence  
- evaluations  
- 背景工作與整合適配器  

Backend **不是** 把請求盲目轉發給 agents 的薄代理；它必須強制執行權限、政策、workflow 規則、風險控制、可審計性與資料邊界。

### 3.2 高層資料流

```text
Frontend / CLI / Integration
        │
        ▼
   FastAPI /api/v1
        │
        ├─ AuthN / AuthZ / rate limit / request_id
        ▼
   Services + Runtime
        │
        ├─ Governance / Approvals
        ├─ Workflow Engine (DNA steps)
        ├─ Tool adapters + tool_effects
        ├─ Knowledge / Memory / Retrieval
        ├─ Evaluation
        ├─ Evolution (sandbox_only)
        ├─ Self-improvement
        └─ Audit + Stream events
                │
                ▼
   Postgres runtime_state (+ optional vector / LLM / object storage)
```

### 3.3 與六層架構的銜接

`structure_hk.md` 的六層（流程智能、知識、執行、演化、治理、安全）全部由評估包裹。Backend 是把這些層 **變成 HTTP／執行引擎／持久狀態** 的落地點。

---

<a id="chapter-4"></a>
## 4. 核心設計原則

### 4.1 七條工程原則

| 原則 | 含義 |
|------|------|
| **API First** | 前端只依賴 API 契約 |
| **預設安全** | 未明確公開的端點一律要認證 |
| **Governance First** | 高風險動作先過政策與關卡 |
| **Human-in-the-Loop** | 不可逆／高風險步驟必須人類批准 |
| **重要事項可審計** | 登入、執行、審批、權限變更等都寫 audit |
| **長任務非阻塞** | 長工作異步或 worker；API 快速回 run id |
| **前端簡化** | 智能、控制、安全、信任強制在 server |

### 4.2 與架構優先次序一致

任何功能取捨仍服從：

**安全性 → 可審計性 → 正確性 → 效率 → 自主性**

自主性不是預設給出，而是用評估證據與關卡逐步賺取。

---

<a id="chapter-5"></a>
## 5. 安全底座：認證、授權、使用者與組織

### 5.1 認證

最低要求：

- 登入／登出／token refresh  
- 密碼重設（若使用密碼）  
- API key（機器客戶端）  
- 可選 SSO／OAuth 就緒  

As-built 重點：

- 密碼 PBKDF2  
- `disabled`／`invited` 使用者不可登入  
- 敏感 auth 端點有 rate limit  

### 5.2 授權（RBAC）

建議角色：Owner、Admin、Manager、Operator、Reviewer、Viewer、ServiceAccount。

權限字串覆蓋 agents、workflows、runs、knowledge、memory、governance、approvals、audit、evaluations、settings、users、organizations 等。

**伺服器端強制**：客戶端自稱權限不算數。

### 5.3 使用者與組織（含 as-built 補齊）

支援組織、使用者、角色、邀請、服務帳戶、API keys。即使單租戶，資料模型仍帶 `organization_id`。

**As-built API 補充：**

| 能力 | 路徑 |
|------|------|
| 使用者列表／建立 | `GET/POST /api/v1/users` |
| 取得／更新／停用 | `GET/PATCH /api/v1/users/{id}` |
| 邀請列表／建立 | `GET/POST /api/v1/users/invitations` |
| 接受邀請（公開） | `POST /api/v1/users/invitations/accept` |
| 組織列表／詳情／更新 | `GET/PATCH /api/v1/organizations...` |

停用使用者會撤銷其 live tokens。

---

<a id="chapter-6"></a>
## 6. 代理、工具與 Workflow DNA

### 6.1 Agent Registry

每個 agent 應有：id、名稱、版本、允許工具、允許記憶範圍、風險等級、輸入／輸出 schema、狀態（draft／active／disabled／archived）。

禁用或封存的 agent 不可再啟動新步驟（除非有明確覆寫政策）。

### 6.2 Tool Registry 與 Broker

工具只能經 backend 控制的權限使用。高風險工具要治理規則與／或審批。

**As-built broker 交集：**

```text
agent.allowed_tools ∩ DNA step.tools ∩ RBAC ∩ 人類關卡
```

**As-built 執行：** 本機 adapters；副作用寫入可持久 `tool_effects`（失敗封閉，不把錯誤當成功）。Live CRM／email SaaS 屬非目標。

### 6.3 Workflow 定義與版本

Workflow 是多步驟業務過程：agents、條件、審批、記憶讀寫、工具、評估、輸出。

狀態：draft／active／disabled／archived。  
Run 必須 pin 到 **特定 workflow version**。  
**Activate／production_ready** 前要過生產 DNA 驗證。

---

<a id="chapter-7"></a>
## 7. 執行引擎：Run、步驟、關卡與串流

### 7.1 Workflow Run

每次執行產生 `workflow_run`。狀態包括：

```text
queued, running, waiting_for_approval, paused,
completed, failed, cancelled, expired, retry_queued, …
```

記錄：輸入、輸出、錯誤、當前步驟、審批狀態、評估結果、成本／用量等。

### 7.2 步驟追蹤

每步有 pending／running／waiting_for_approval／completed／failed／skipped／cancelled 等狀態，以及 agent／tool、輸入輸出、重試次數。

### 7.3 啟動流程（規範順序）

1. 認證  
2. 授權 `workflows:execute`  
3. 載入 workflow 版本  
4. 驗證輸入 schema  
5. governance pre-check  
6. 建立 queued run + audit  
7. 回傳 `workflow_run_id`  
8. 引擎執行步驟  
9. 前端 poll 或 SSE 串流  

支援 **Idempotency-Key**：同一使用者同一 key 不重複開 run。

### 7.4 As-built 生命週期 API

| 動作 | Endpoint |
|------|----------|
| 取消 | `POST .../workflow-runs/{id}/cancel` |
| 暫停 | `POST .../pause` |
| 恢復 | `POST .../resume`（→ queued） |
| 逾期 | `POST .../expire` |
| 重試 | `POST .../retry` |
| 串流 | `GET .../stream`（SSE） |

### 7.5 人類關卡

高風險、不可逆、外部動作等情境 → 建立 approval → run 進入 `waiting_for_approval` → 批准後才可繼續；拒絕則停止門控動作。

---

<a id="chapter-8"></a>
## 8. 治理、審計、知識、記憶與評估

### 8.1 Governance

治理層決定：workflow 可否跑、步驟可否執行、工具可否用、資料可否讀、是否要人批、輸出可否放行。

風險等級：low／medium／high／critical。  
政策動作：allow／deny／require_approval／require_evaluation／require_redaction。

### 8.2 Audit Logging

重要動作必須寫 audit（登入、workflow 變更、run 生命週期、審批、知識上傳、記憶敏感存取、權限變更、API key 等）。  
API 上 audit **唯讀**，客戶端不能改歷史。

### 8.3 Knowledge Base

上傳、索引、chunk、embed、搜尋、ACL、封存。  
As-built：分層檢索 Tier-0（預設）／Tier-1 multi-hop lite；結果帶 provenance；檢索內容當不可信資料。

### 8.4 Memory System

多 scope（短期、長期、user／team／department／org／workflow／agent 等），強制 ACL 與敏感度。  
Agent 不得讀寫未允許的 scope。

### 8.5 Evaluation System

對重要輸出與 workflow 做 schema／政策／安全／成本等評估。  
必要失敗可阻擋放行或 promote。  
演化用 **corpus eval** 打適應度。

---

<a id="chapter-9"></a>
## 9. 流程智能、演化沙盒與自我改進

### 9.1 Process Intelligence

提供 metrics、瓶頸、失敗、成本、審批延遲等。  
As-built：聚合 run／事件資料 + 寫入 `business/process-intelligence/` 產物；**不**直接改生產 DNA。

### 9.2 Evolution Sandbox（不可談判）

**Evolution Manager 絕不能直接改生產。** 只能：

```text
提出變體 → 沙盒測試 → 與基線比較 → 請求批准
→ 金絲雀 → 失敗自動回滾 → 通過才版本化晉升
```

API 強制 `sandbox_only`；**禁止** DGM 式改寫 host 應用程式碼。

### 9.3 Self-Improvement

```text
run 結束 →（可選 auto）reflect → lessons
→ auto-propose 沙盒變體 → 仍走 evaluate／canary 路徑
skill 寫入 _sandbox → 顯式 promote
loop DNA runner 有界迭代
```

前端 Improve 管線（Reflect → Propose → Evaluate → Canary）只呼叫這些 API。

### 9.4 生產 DNA 安全

`structure_validators` + `business:validate`：風險分級、關卡、回滾、來源欄位。  
驗證失敗 → 拒絕 activate／production_ready；可記錄 rejection lesson，**不**突變生產 DNA。

---

<a id="chapter-10"></a>
## 10. 非功能需求與工程約束

### 10.1 安全

- 受保護路由要 AuthN；資源要 AuthZ  
- 驗證 request body；上傳消毒  
- 密鑰不進 repo、不進 log、不回傳給客戶端  
- 敏感端點 rate limit  
- 提示注入假設仍可能：安全在 LLM **之外** 以確定性控制執行  
- 檢索／用戶／工具 I／O 當資料，不當指令  

### 10.2 可靠、可觀測、可維護

- 優雅錯誤與安全錯誤信封（含 `request_id`）  
- health／live／ready（ready 報告資料庫狀態；可 `GENERIC_SWARM_REQUIRE_POSTGRES`）  
- 結構化 log 與 metrics  
- 分層：routes → services → domain → infrastructure  

---

<a id="chapter-11"></a>
## 11. API 契約與資料模型要點

### 11.1 版本與信封

- 公開 API 前綴：`/api/v1`  
- 成功：一致 `data`／`meta` 風格（見規格）  
- 錯誤：code、message、`request_id`；生產不回 stack  
- OpenAPI 由 FastAPI 產生；前端 `pnpm api:generate`  

### 11.2 主要端點族群

認證、agents、tools、workflows、workflow-runs、approvals、knowledge、memory、governance、evaluations、audit-logs、processes、evolution、improvement、loops、settings、users、organizations。

### 11.3 核心實體（概念）

Organization、User、Agent、Workflow、WorkflowVersion、WorkflowRun、WorkflowRunStep、ApprovalRequest、KnowledgeDocument／Chunk、MemoryItem、EvaluationRun、AuditLog，以及 as-built 的 evolution variants、lessons、tool_effects 等集合。

---

<a id="chapter-12"></a>
## 12. 資料夾結構與工程分層

As-built 大致對應：

```text
backend/app/
  main.py              # ASGI 入口
  runtime.py           # 編排與狀態門面
  api/v1/routes/       # HTTP
  core/                # config, auth, permissions, errors, rate_limit
  domain/              # 領域邏輯
  services/            # 應用服務
  infrastructure/      # DB, adapters, retrieval, evolution, validators
  schemas/             # Pydantic 契約
  tests/unit|e2e/      # 驗證
```

任務→程式碼索引：`planning/backend/TASK_TO_CODE_TRACEABILITY.md`。

---

<a id="chapter-13"></a>
## 13. 完成定義與操作證明

### 13.1 首個生產就緒清單（摘要）

認證、列表與啟動 workflow、輸入驗證、權限、audit、長任務、步驟執行、狀態與串流、審批關卡、知識搜尋 ACL、記憶控制、評估阻擋不安全輸出、OpenAPI、關鍵測試、部署文件、無硬編碼密鑰。

### 13.2 產品標竿 mark ~100 追加項

```text
21. DATABASE_URL 時 Postgres 為主持久層
22. 本機 adapters 寫入 tool_effects
23. Evolution 強制 sandbox_only 路徑
24. Self-improvement reflect／lessons／auto-propose
25. activate／production_ready DNA 驗證
26. E1 e2e：login → run → gate → complete → improve
```

### 13.3 操作證明

E1 路徑與清單：`backend/app/tests/e2e/test_e1_operator_path.py`、`reviews/e1_operator_checklist.md`。  
單元與 e2e 以倉庫 `status.md` 與 CI／本地 unittest 為準。

---

<a id="chapter-14"></a>
## 14. 實作對應：SDD 規格包與 as-built

本章對應 `backend_hk.md` **§24**。

### 14.1 文件關係

| 文件 | 角色 |
|------|------|
| `structure.md`／`structure_hk.md` | 架構願景 SoT |
| `planning/structure/` | 架構 SDD 01–17 |
| `backend.md`／`backend_hk.md` | Backend 計劃 |
| `planning/backend/nn_*/` | Backend 子功能 SDD 01–24 |
| `backend/` | As-built FastAPI |
| `frontend.md`／`frontend/` | 營運台 |
| `planning/gap_analysis_for_backend.md` | 任務 vs 實作落差（產品標竿 100／100） |

### 14.2 能力關卡（backend 份額）

| 階段 | structure 分帶 | Backend as-built |
|------|----------------|------------------|
| A 基礎 | 第 1–14 日 | Auth、RBAC、audit、health／ready、seed、business 驗證 |
| B 影子學習 | 第 15–30 日 | 事件／process APIs；PI 產物；knowledge 攝取／搜尋 |
| C 受控副駕駛 | 第 31–60 日 | Postgres 主存；DNA runs；關卡；Tier-0／1；adapters；DNA 檢查 |
| D 演化沙盒 | 第 61–90 日 | corpus eval、canary／rollback、SI 迴圈、skill sandbox |

### 14.3 As-built 一覽（不削弱架構）

| 主題 | As-built |
|------|----------|
| 控制平面 | FastAPI + Postgres JSONB；JSON 備份／種子 |
| Tools | 本機 adapters + `tool_effects` |
| Broker | allow-list ∩ DNA ∩ RBAC ∩ gates |
| PI | 服務 + 磁碟產物 |
| 檢索 | Tier-0／1 lite；完整商用圖稍後 |
| 演化 | 僅沙盒；不改 host 程式 |
| 自我改進 | reflect／lessons／propose／loops |
| DNA 安全 | validators on activate |
| 操作證明 | E1 路徑 |
| 使用者／組織 | 邀請、disable、org PATCH |
| Run 生命週期 | pause／resume／expire |

### 14.4 Backend 子功能 01–24（摘要）

| nn | 子功能 |
|----|--------|
| 01 | 平台憲章、邊界、原則 |
| 02 | 技術棧與專案骨架 |
| 03 | 持久控制平面 |
| 04 | API 契約與錯誤信封 |
| 05 | 認證與身份 |
| 06 | 授權與 RBAC |
| 07 | 使用者、組織、租戶 |
| 08 | Agent 登錄 |
| 09 | 工具、adapters、broker |
| 10 | Workflow 定義與版本 |
| 11 | Run 執行引擎 |
| 12 | 治理政策與風險 |
| 13 | 人類審批關卡 |
| 14 | 審計日誌 |
| 15 | 知識庫與檢索 |
| 16 | 記憶系統 |
| 17 | 評估系統 |
| 18 | 流程智能 |
| 19 | 串流、健康、可觀測 |
| 20 | 演化沙盒 APIs |
| 21 | 自我改進與 loops |
| 22 | 生產 DNA 安全 |
| 23 | 安全加固與 NFR |
| 24 | 測試策略與操作路徑 |

每項均有：`requirements.md` → `design.md` → `tasks.md`（含 **Deliverable code paths**）。

### 14.5 明確非目標（目前產品標竿）

- 完整商用 LightRAG／Neo4j 生產 mesh  
- 外部 live CRM／email／billing SaaS adapters  
- DGM 式 host 自我改寫  
- 常駐多 worker Temporal／Celery 作為硬性要求  
- 每工具 ephemeral OAuth broker  
- 無限填滿 `business/` 每一葉節點  

### 14.6 營運入口

| 層 | 入口 |
|----|------|
| 程式 | `backend/app/main.py`、`runtime.py`、`infrastructure/*` |
| 持久 | `DATABASE_URL` → Postgres（`docs/postgres-runbook.md`） |
| 語料 | `business/` |
| 延續 | `memory/handoff.md`、`status.md` |
| UI | `frontend/` |
| 任務→碼 | `planning/backend/TASK_TO_CODE_TRACEABILITY.md` |

### 14.7 一句話總結

`backend_hk.md` 描述的不是「再多幾個 HTTP 路由」，而是把 **受治理、可審計、可評估、只在沙盒演化** 的商業作業系統，落成 **唯一可信的 API 控制平面**。前端可以漂亮，但 **政策、權限、DNA 與生產安全永遠在 backend**。

---

## 附錄：建議延伸閱讀

- 架構：`structure_hk.md`、`book/book.structure_hk.md`  
- Backend 計劃：`backend_hk.md`、`backend.md`  
- 前端契約：`frontend.md` §33  
- SDD：`planning/backend/README.md`  
- 落差：`planning/gap_analysis_for_backend.md`  
- 現況：`status.md`、`backend/README.md`
