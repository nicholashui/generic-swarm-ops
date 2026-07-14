# 第 01-03 章：初始設定精靈

![Setup Wizard Flow](../assets/01-03-setup-wizard-flow.svg)

## 學習目標

在完成本章後，你將能夠：

1. 使用 `npm run bootstrap` 執行完整的 bootstrap 流程
2. 使用 `npm run business:init` 初始化業務制品層
3. 在 `backend/.env` 中配置 PostgreSQL 資料庫連接
4. 使用 uvicorn 啟動 FastAPI 後端並驗證資料庫連接
5. 使用正確的環境變量啟動 Next.js 前端控制台
6. 使用健康檢查端點驗證完整系統是否正常運作
7. 理解 bootstrap、init 及運行時啟動之間的關係

## 先決條件

- 已安裝並驗證[第 01-02 章](01-02-installation-prerequisites.md)中的所有依賴項
- PostgreSQL 14+ 正在運行且可在 `localhost:5432` 存取
- 已建立名為 `generic_swarm_ops` 的資料庫
- 倉庫已克隆到你的本地機器
- 在倉庫根目錄有終端/shell 存取權限

---

## 1. 設定流程概覽

初始設定遵循六階段流程：

| 階段 | 命令/操作 | 目的 |
|-------|-----------------|---------|
| 1. Bootstrap | `npm run bootstrap` | 建立業務目錄樹、安裝依賴項 |
| 2. 業務初始化 | `npm run business:init` | 建構治理制品、建立評估黃金任務 |
| 3. 環境 | 編輯 `backend/.env` | 配置資料庫 URL 及可選功能 |
| 4. 後端 | `uvicorn app.main:app --reload` | 啟動 FastAPI 控制平面 |
| 5. 前端 | `pnpm dev` | 啟動 Next.js 操作控制台 |
| 6. 驗證 | `GET /api/v1/health/ready` | 確認完整系統連接 |

> **注意：** 這些階段必須按順序執行。後端需要來自第 3 階段的資料庫配置，而前端需要後端正在運行（第 4 階段）才能進行即時 API 連接。

---

## 2. 第 1 階段：Bootstrap

bootstrap 命令是初始化整個系統的入口點。它建立業務目錄結構、下載所需來源並準備工作空間。

### 步驟 1：導航到倉庫根目錄

```bash
cd generic-swarm-ops
```

### 步驟 2：運行 Bootstrap

```bash
npm run bootstrap
```

**此命令的功能：**
1. 建立 `business/` 目錄樹及所有必需的子目錄
2. 初始化啟動線束配置
3. 設定雙線束結構（`.trae/` 及 `.grok/`）
4. 驗證倉庫結構

**預期輸出：**
```text
> generic-swarm-ops@1.0.0 bootstrap
> node scripts/bootstrap.js

Creating business directory structure...
  business/process-intelligence/event-logs/
  business/process-intelligence/discovered-processes/
  business/process-intelligence/conformance-reports/
  business/process-intelligence/bottlenecks/
  business/process-intelligence/causal-hypotheses/
  business/knowledge-base/rules/
  business/knowledge-base/decision-patterns/
  business/knowledge-base/provenance/
  ...
Bootstrap complete.
```

### 步驟 3：驗證 Bootstrap 結果

```bash
# 檢查業務目錄是否已建立
ls business/

# 預期子目錄：
# evals/  evolution/  governance/  knowledge-base/  materials/
# memory/  process-intelligence/  security/  experts/  distilled/
```

> **提示：** 如果 bootstrap 失敗，運行 `npm run doctor` 來診斷缺失的先決條件。doctor 命令會檢查所有依賴項並報告哪些需要注意。

---

## 3. 第 2 階段：業務層初始化

在 bootstrap 建立目錄結構後，`business:init` 會用必需的治理制品及評估測試填充它。

### 步驟 1：初始化業務層

```bash
npm run business:init
```

**此命令的功能：**
1. 建立治理框架（AI 清單、風險等級、審批策略）
2. 生成初始評估黃金任務（至少需要 20 個）
3. 設定演化 Workflow DNA 模板
4. 建立安全基線制品

**預期輸出：**
```text
> generic-swarm-ops@1.0.0 business:init
> node scripts/business/init.js

Initializing governance artifacts...
  business/governance/ai-inventory/
  business/governance/risk-assessments/
  business/governance/human-approval-policy/
Creating evaluation golden tasks...
  business/evals/golden-tasks/ (20 tasks created)
Setting up evolution templates...
  business/evolution/workflow-dna/
Business layer initialization complete.
```

### 步驟 2：驗證業務層

```bash
# 運行驗證以確保所有制品格式正確
npm run business:validate
```

**預期輸出：**
```text
> generic-swarm-ops@1.0.0 business:validate
> node scripts/business/validate.js

Validating business artifacts...
  governance: PASS (inventory, risk-tiers, approval-policy)
  evals: PASS (20 golden tasks, schemas valid)
  evolution: PASS (workflow-dna templates present)
  security: PASS (threat-models, tool-permissions)
All validations passed.
```

### 步驟 3：運行額外治理檢查

```bash
# 檢查治理層完整性
npm run business:governance

# 檢查安全基線
npm run business:security
```

> **警告：** 不要跳過驗證步驟。運行時會拒絕引用缺失治理制品的工作流程。及早運行 `business:validate` 可在這些問題成為運行時錯誤之前捕獲它們。

---

## 4. 第 3 階段：環境配置

系統需要環境變量用於資料庫連接、API 路由及可選功能旗標。

### 步驟 1：建立後端環境檔案

```bash
# 複製範例環境檔案
cp backend/.env.example backend/.env
```

### 步驟 2：配置資料庫 URL

編輯 `backend/.env` 並設定 `DATABASE_URL`：

```bash
# backend/.env
DATABASE_URL=postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops
```

將 `gso_user` 及 `gso_password` 替換為你的實際 PostgreSQL 憑證。

### 步驟 3：設定 PYTHONPATH

後端需要 `PYTHONPATH=.` 以正確解析模組：

```bash
# 在 shell 中設定（Linux/macOS）
export PYTHONPATH=.

# 或在 Windows 上
set PYTHONPATH=.
```

### 步驟 4：配置可選功能

根據需要向 `backend/.env` 添加可選設定：

```bash
# backend/.env（完整範例）
DATABASE_URL=postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops

# 在終端運行時自動反思（預設：true）
GENERIC_SWARM_AUTO_REFLECT=true

# 可選 LLM 評審（預設：false）
GENERIC_SWARM_LLM_CRITIC_ENABLED=false

# 可選嵌入（預設：false）
GENERIC_SWARM_EMBEDDINGS_ENABLED=false

# 可選 pgvector（預設：false）
GENERIC_SWARM_PGVECTOR_ENABLED=false

# 可選 Neo4j 圖聯邦
# NEO4J_URI=bolt://localhost:7687
```

### 步驟 5：配置前端環境

在終端會話中設定前端環境變量：

```bash
# Linux/macOS
export NEXT_PUBLIC_DEMO_MODE=false
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1

# Windows
set NEXT_PUBLIC_DEMO_MODE=false
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

> **注意：** 設定 `NEXT_PUBLIC_DEMO_MODE=false` 至關重要。當設為 `true` 時，前端使用模擬資料而非連接到即時後端 API。對於生產操作，這必須始終為 `false`。

---

## 5. 第 4 階段：後端啟動

FastAPI 後端是整個系統的控制平面。它處理認證、工作流程執行、知識檢索及所有 API 操作。

### 步驟 1：導航到後端目錄

```bash
cd backend
```

### 步驟 2：安裝 Python 依賴項

```bash
python -m pip install -e .
```

這會以可編輯模式安裝後端套件，包括所有必需的依賴項（FastAPI、uvicorn、psycopg2、pydantic 及基礎設施套件）。

### 步驟 3：啟動後端伺服器

```bash
# 確保 PYTHONPATH 已設定
export PYTHONPATH=.  # Linux/macOS
# 或：set PYTHONPATH=.  # Windows

# 使用熱重載啟動 uvicorn
uvicorn app.main:app --reload
```

**預期輸出：**
```text
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to stop)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Application startup complete.
```

### 步驟 4：驗證後端健康

在新的終端視窗中：

```bash
# 檢查健康端點
curl http://127.0.0.1:8000/api/v1/health/ready
```

**預期回應：**
```json
{
  "database": "postgres",
  "status": "healthy"
}
```

> **警告：** 如果健康檢查返回 `"database": "json_file"` 而非 `"database": "postgres"`，你的 `DATABASE_URL` 配置不正確或 PostgreSQL 未運行。系統會退回到 JSON 檔案儲存，這僅適用於種子及恢復，不適用於生產操作。

### 步驟 5：驗證 API 文檔

FastAPI 後端自動生成互動式 API 文檔：

```bash
# 在瀏覽器中打開
# Swagger UI：http://127.0.0.1:8000/docs
# ReDoc：http://127.0.0.1:8000/redoc
```

---

## 6. 第 5 階段：前端啟動

Next.js 前端提供操作控制台，用於管理代理、工作流程、運行、審批及自我改進流程。

### 步驟 1：導航到前端目錄

```bash
cd frontend
```

### 步驟 2：安裝前端依賴項

```bash
pnpm install
```

**預期輸出：**
```text
Packages: +XXX
Progress: resolved XXX, reused XXX, downloaded 0, added XXX, done
```

### 步驟 3：啟動開發伺服器

```bash
# 確保環境變量已設定
export NEXT_PUBLIC_DEMO_MODE=false
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1

# 啟動 Next.js 開發伺服器
pnpm dev
```

**預期輸出：**
```text
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Ready in Xs
```

### 步驟 4：驗證前端存取

打開瀏覽器並導航到 `http://localhost:3000`。你應該看到 Generic Swarm Ops 控制台登入頁面。

> **提示：** 如果前端顯示「Demo Mode」或顯示佔位資料，請驗證 `NEXT_PUBLIC_DEMO_MODE` 已設為 `false` 且後端正在運行。前端需要即時後端連接才能進入操作模式。

---

## 7. 第 6 階段：完整系統驗證

所有服務運行後，執行全面驗證。

### 步驟 1：健康檢查

```bash
# 後端健康
curl -s http://127.0.0.1:8000/api/v1/health/ready | python3 -m json.tool
```

預期：
```json
{
  "database": "postgres",
  "status": "healthy"
}
```

### 步驟 2：列出可用工作流程

```bash
curl -s http://127.0.0.1:8000/api/v1/workflows | python3 -m json.tool
```

這應該返回已註冊工作流程定義的列表，包括旗艦 `wf_customer_onboarding_v12`。

### 步驟 3：列出可用代理

```bash
curl -s http://127.0.0.1:8000/api/v1/agents | python3 -m json.tool
```

這應該返回具有已配置代理的代理名冊。

### 步驟 4：測試認證

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}'
```

預期：帶有會話令牌的成功認證回應。

### 步驟 5：前端連接檢查

1. 在瀏覽器中打開 `http://localhost:3000`
2. 使用 `admin@example.com` / `admin-password` 登入
3. 導航到代理頁面 -- 應顯示即時代理資料
4. 導航到工作流程頁面 -- 應顯示已註冊的工作流程

### 步驟 6：運行業務層驗證

```bash
# 從倉庫根目錄
npm run business:validate
npm run business:governance
npm run business:security
```

所有三個命令都應無錯誤通過。

---

## 8. 理解啟動順序

### 8.1 為何此順序重要

設定階段具有嚴格的依賴關係：

```text
bootstrap ─┬─► business:init ──► environment config
            │                           │
            │                           ▼
            │                    backend startup
            │                           │
            │                           ▼
            │                    frontend startup
            │                           │
            │                           ▼
            └──────────────────► full verification
```

- **bootstrap** 必須首先運行，因為它建立了 `business:init` 填充的目錄結構
- **business:init** 必須在後端之前運行，因為運行時在啟動時載入治理制品
- **後端**必須在前端之前啟動，因為前端調用後端 API 獲取即時資料
- **驗證**確認所有層已連接且正常運作

### 8.2 後端啟動時發生什麼

當 uvicorn 啟動 FastAPI 應用程式（`app.main:app`）時，會發生以下情況：

1. 註冊中間件（請求 ID 注入、CORS、安全標頭）
2. 透過 `DATABASE_URL` 建立資料庫連接
3. 如果 `runtime_state` 表為空，則從 `backend/data/runtime.json` 載入種子資料
4. 為所有模組（auth、workflows、agents、runs 等）註冊 API 路由
5. 初始化自我改進模組（如果 `GENERIC_SWARM_AUTO_REFLECT=true`）

### 8.3 前端啟動時發生什麼

當 Next.js 啟動（`pnpm dev`）時，它：

1. 讀取環境變量（`NEXT_PUBLIC_DEMO_MODE`、`NEXT_PUBLIC_API_BASE_URL`）
2. 如果 `DEMO_MODE=false`，配置 API 用戶端連接到後端
3. 設定具有每個系統功能頁面的應用路由器
4. 初始化 Zod 驗證結構用於表單
5. 註冊 React Hook Form 處理器用於代理/工作流程建立

---

## 9. 設定後命令參考

初始設定後，以下命令可用於持續操作：

### 9.1 編排命令

```bash
# 重新運行 bootstrap（可安全重複）
npm run bootstrap

# 系統健康檢查
npm run doctor

# 下載外部來源
npm run sources:download

# 審計已下載的來源
npm run sources:audit

# 重新生成雙線束檔案
npm run sync

# 檢查同步狀態
npm run sync:check
```

### 9.2 業務層命令

```bash
# 初始化業務制品
npm run business:init

# 驗證所有制品
npm run business:validate

# 檢查治理完整性
npm run business:governance

# 運行安全基線
npm run business:security

# 檢查演化就緒度
npm run business:evolution:check

# 運行評估（乾跑）
npm run business:eval -- --dry-run
```

### 9.3 後端命令

```bash
cd backend

# 安裝/更新依賴項
python -m pip install -e .

# 使用熱重載啟動
uvicorn app.main:app --reload

# 運行單元測試
python -m unittest discover -s app/tests/unit -p "test_*.py"

# 運行端到端測試
python -m unittest discover -s app/tests/e2e -p "test_*.py"
```

### 9.4 前端命令

```bash
cd frontend

# 安裝依賴項
pnpm install

# 啟動開發伺服器
pnpm dev

# 運行 linter
pnpm lint

# 運行型別檢查
pnpm typecheck

# 運行測試
pnpm test
```

---

## 10. 自我改進 API 端點

後端公開以下自我改進 API 用於演化流程：

| 方法 | 路徑 | 目的 |
|--------|------|---------|
| POST | `/api/v1/improvement/reflect/{run_id}` | 對已完成的運行進行反思 |
| GET | `/api/v1/improvement/lessons` | 檢索已儲存的教訓 |
| POST | `/api/v1/improvement/auto-propose` | 生成工作流程改進提議 |
| POST | `/api/v1/loops/run` | 執行自我改進循環 |
| GET | `/api/v1/evolution/archive` | 檢視演化族群歸檔 |
| POST | `/api/v1/knowledge/graph/federate` | 推送到知識圖（需要 Neo4j） |

---

## 11. 真實使用案例

### 使用案例 1：多服務開發環境

**場景：** 開發者需要同時在後端及前端工作，兩端都有熱重載。

**方法：**

打開三個終端視窗：

```bash
# 終端 1：後端
cd backend
export PYTHONPATH=.
uvicorn app.main:app --reload --port 8000

# 終端 2：前端
cd frontend
export NEXT_PUBLIC_DEMO_MODE=false
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
pnpm dev

# 終端 3：業務驗證（定期運行）
npm run business:validate
```

對 Python 檔案的更改觸發後端重載。對 TypeScript/React 檔案的更改觸發前端重載。業務制品更改按需驗證。

### 使用案例 2：無頭 API 專用設定

**場景：** 團隊希望在不使用前端的情況下運行系統，僅使用 API 調用進行整合測試或無頭自動化。

**方法：**

```bash
# 僅啟動後端
cd backend
export PYTHONPATH=.
export DATABASE_URL=postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops
uvicorn app.main:app --reload

# 使用 curl 測試
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}'

# 列出工作流程
curl http://127.0.0.1:8000/api/v1/workflows

# 觸發工作流程運行
curl -X POST http://127.0.0.1:8000/api/v1/runs \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "wf_customer_onboarding_v12", "payload": {"case_id": "test_001"}}'
```

### 使用案例 3：資料庫重置及重新種子

**場景：** 經過大量測試後，開發者希望將系統重置為初始狀態。

**方法：**

```bash
# 停止後端（在後端終端中按 Ctrl+C）

# 刪除並重新建立資料庫
psql postgresql://localhost:5432/postgres -c "DROP DATABASE generic_swarm_ops;"
psql postgresql://localhost:5432/postgres -c "CREATE DATABASE generic_swarm_ops;"

# 重新初始化業務制品
npm run business:init
npm run business:validate

# 重啟後端（它將從 runtime.json 種子）
cd backend
uvicorn app.main:app --reload

# 驗證健康
curl http://127.0.0.1:8000/api/v1/health/ready
# 應顯示：{"database": "postgres"}
```

---

## 12. 最佳實踐

1. **啟動後始終驗證健康** -- `GET /api/v1/health/ready` 端點應始終返回 `"database": "postgres"`。如果返回 `"json_file"`，立即修復你的資料庫配置。

2. **開發中使用熱重載** -- uvicorn 的 `--reload` 旗標及 `pnpm dev` 命令都支持熱重載，無需手動重啟。

3. **任何制品更改後運行 `business:validate`** -- 這在結構違規及缺失引用成為運行時錯誤之前捕獲它們。

4. **保持環境變量一致** -- 後端啟動及直接資料庫操作使用相同的 `DATABASE_URL`。不一致會導致微妙的錯誤。

5. **按順序啟動服務** -- 資料庫優先，然後後端，然後前端。逆序會導致可能令人困惑的連接錯誤。

6. **使用種子憑證進行初始測試** -- `admin@example.com` / `admin-password` 是預配置的。在生產中更改這些。

7. **查閱 `backend/docs/postgres-runbook.md`** -- 了解資料庫特定操作如備份、還原及結構遷移。

---

## 13. 章節摘要

在本章中，你完成了完整的初始設定流程：

- **第 1 階段（Bootstrap）：** 使用 `npm run bootstrap` 建立業務目錄結構
- **第 2 階段（業務初始化）：** 使用 `npm run business:init` 填充治理及評估制品
- **第 3 階段（環境）：** 配置 `backend/.env` 的 `DATABASE_URL` 並設定前端環境變量（`NEXT_PUBLIC_DEMO_MODE=false`、`NEXT_PUBLIC_API_BASE_URL`）
- **第 4 階段（後端）：** 使用 `uvicorn app.main:app --reload` 啟動 FastAPI 伺服器
- **第 5 階段（前端）：** 使用 `pnpm dev` 啟動 Next.js 控制台
- **第 6 階段（驗證）：** 透過 API 端點及瀏覽器存取確認完整系統健康

系統現在已正常運作，可以進行首次配置（下一章）。

---

## 14. 知識檢查問答

**問題 1：** bootstrap 系統的正確命令是什麼？

a) `npm start`
b) `npm run bootstrap`
c) `npm run init`
d) `npm run setup`

<details>
<summary>答案</summary>
<b>b)</b> <code>npm run bootstrap</code> 建立業務目錄結構並初始化工作空間。它是在新克隆中要運行的第一個命令。
</details>

---

**問題 2：** `NEXT_PUBLIC_DEMO_MODE=false` 做什麼？

a) 完全禁用前端
b) 在 UI 中啟用深色模式
c) 將前端連接到即時後端 API 而非模擬資料
d) 禁用認證

<details>
<summary>答案</summary>
<b>c)</b> 設定 <code>NEXT_PUBLIC_DEMO_MODE=false</code> 將前端設為操作模式，連接到由 <code>NEXT_PUBLIC_API_BASE_URL</code> 指定的即時後端 API。設為 <code>true</code> 時，前端使用模擬/演示資料。
</details>

---

**問題 3：** 資料庫正確連接時健康端點返回什麼？

a) `{"status": "ok"}`
b) `{"database": "postgres", "status": "healthy"}`
c) `{"connected": true}`
d) `{"health": "green"}`

<details>
<summary>答案</summary>
<b>b)</b> <code>GET /api/v1/health/ready</code> 在正確連接到 PostgreSQL 時返回 <code>{"database": "postgres"}</code>。如果返回 <code>"json_file"</code>，表示資料庫配置不正確。
</details>

---

**問題 4：** 服務必須以什麼順序啟動？

a) 前端、後端、資料庫
b) 資料庫、前端、後端
c) 資料庫、後端、前端
d) 後端、資料庫、前端

<details>
<summary>答案</summary>
<b>c)</b> 資料庫（PostgreSQL）必須首先運行，然後是後端（連接到資料庫），然後是前端（連接到後端 API）。
</details>

---

**問題 5：** 什麼命令驗證所有業務制品格式正確？

a) `npm run doctor`
b) `npm run business:validate`
c) `npm run business:check`
d) `npm test`

<details>
<summary>答案</summary>
<b>b)</b> <code>npm run business:validate</code> 根據結構檢查所有業務制品並驗證交叉引用。<code>npm run doctor</code> 檢查系統先決條件，而非制品有效性。
</details>

---

**問題 6：** 如果後端在沒有有效 `DATABASE_URL` 的情況下啟動會怎樣？

a) 它立即崩潰
b) 它退回到 JSON 檔案儲存（不適用於生產）
c) 它建立 SQLite 資料庫
d) 它等待資料庫可用

<details>
<summary>答案</summary>
<b>b)</b> 後端退回使用 <code>backend/data/runtime.json</code> 作為基於檔案的儲存。這僅適用於種子及恢復，不適用於生產。健康端點在此狀態下會報告 <code>"database": "json_file"</code>。
</details>

---

**問題 7：** 應該複製哪個檔案來建立後端環境配置？

a) `backend/config.example`
b) `backend/.env.example`
c) `backend/settings.yml`
d) `backend/environment.json`

<details>
<summary>答案</summary>
<b>b)</b> 將 <code>backend/.env.example</code> 複製到 <code>backend/.env</code> 並為你的環境自訂值。此檔案記錄了所有可用的變量。
</details>

---

## 下一章

繼續閱讀[第 01-04 章：首次配置](01-04-first-time-configuration.md)以配置認證、代理及你的第一個工作流程。
