# 第 4.1 章：常見錯誤解決方案

![錯誤解決流程圖](../assets/04-01-error-resolution-flowchart.svg)

## 學習目標

完成本章後，你將能夠：

1. 根據來源層級（引導、後端、前端、演化）識別和分類錯誤
2. 針對每個錯誤類別應用系統化的解決程序
3. 使用診斷命令快速定位根本原因
4. 在不需要外部支援的情況下解決最常見的操作問題
5. 理解失敗關閉行為及其如何保護系統完整性

## 先決條件

在開始本章之前，請確保你已：

- 完成第 1 節的安裝步驟（Node.js 20+、Python 3.11+、PostgreSQL 14+、Git、pnpm）
- 擁有已複製 Generic Swarm Ops 儲存庫的終端機存取權限
- 基本熟悉環境變數和命令列操作
- 已閱讀第 1.1 章（系統架構）以了解分層結構的背景

---

## 1. 錯誤分類框架

Generic Swarm Ops 的錯誤分為四個不同的類別，每個類別對應一個系統層級：

| 類別 | 層級 | 常見觸發原因 |
|------|------|-------------|
| 引導/啟動器 | 基礎設施設定 | 缺少先決條件、來源下載失敗 |
| 後端/Postgres | 執行時服務 | 資料庫連線、認證、記憶體範圍 |
| 前端 | 使用者介面 | 環境設定、API 偏差、測試設定 |
| 演化 | 自我改進 | 證據不完整、推廣受阻 |

> **提示：** 永遠從識別錯誤來源層級開始診斷。先執行 `npm run doctor` 可以排除最基本的問題，然後再深入調查更深層的問題。

---

## 2. 引導和啟動器層級錯誤

### 2.1 來源鎖定失敗

**症狀：** `npm run bootstrap` 失敗並顯示引用 `sources/source-lock.json` 的錯誤。

**根本原因：** 外部來源儲存庫無法複製或鎖定檔案已損壞。

**解決步驟：**

1. 檢查鎖定檔案中的複製失敗：

```bash
cat sources/source-lock.json
```

2. 尋找帶有 `"status": "failed"` 或缺少 `"commit"` 雜湊值的項目。

3. 驗證與鎖定檔案中列出的來源儲存庫的網路連線。

4. 重新執行來源下載：

```bash
npm run sources:download
```

5. 驗證鎖定檔案現在已完成：

```bash
cat sources/source-lock.json | python -m json.tool
```

**預期結果：** `source-lock.json` 中所有項目都顯示成功狀態及有效的提交雜湊值。

> **警告：** 永遠不要手動編輯 `source-lock.json`。務必使用 `npm run sources:download` 來重新產生它。

### 2.2 來源審計警告

**症狀：** `npm run bootstrap` 報告審計警告或 `docs/source-audit.md` 包含未解決的發現。

**根本原因：** 下載的外部來源存在未驗證的授權、完整性問題或政策違規。

**解決步驟：**

1. 查看審計報告：

```bash
cat docs/source-audit.md
```

2. 獨立執行審計命令以查看當前狀態：

```bash
npm run sources:audit
```

3. 對於每個警告，確定該來源是否：
   - 具有適合你用例的可接受授權
   - 通過完整性檢查（雜湊值匹配）
   - 符合你組織的安全政策

4. 通過以下方式處理個別發現：
   - 更新來源設定以接受該授權
   - 從設定中移除有問題的來源
   - 向你的治理流程提交例外申請

**預期結果：** `docs/source-audit.md` 顯示所有來源通過或具有已記錄的例外。

### 2.3 缺少業務種子檔案

**症狀：** `npm run business:validate` 報告缺少必要檔案，或引導程式抱怨缺少業務構件。

**根本原因：** 業務作業系統層尚未初始化，或檔案被意外刪除。

**解決步驟：**

1. 初始化業務層：

```bash
npm run business:init
```

2. 驗證生成的結構：

```bash
ls business/
ls business/process-intelligence/
ls business/evolution/
ls business/governance/
ls business/evals/golden-tasks/
ls business/knowledge-base/
```

3. 執行驗證以確認所有必要檔案存在：

```bash
npm run business:validate
```

**預期結果：** 所有業務目錄包含其所需的種子檔案，且驗證通過。

### 2.4 Schema 和驗證失敗

**症狀：** `npm run business:validate` 報告 schema 違規、來源追溯失敗、風險等級不匹配或工作流程閘門錯誤。

**根本原因：** 業務構件不符合預期的 schema 或元資料不完整。

**解決步驟：**

1. 執行帶有詳細輸出的驗證：

```bash
npm run business:validate
```

2. 對於每種失敗類型，檢查相應的構件並修正問題（schema 違規需要修正資料格式、來源追溯失敗需要添加元資料、風險等級不匹配需要對齊宣告的等級）。

3. 修正後重新執行驗證：

```bash
npm run business:validate
```

**預期結果：** 所有驗證檢查通過，無錯誤。

### 2.5 安全掃描失敗

**症狀：** `npm run business:security` 報告檔案中有密鑰、不安全的權限或提示注入覆蓋率不足。

**根本原因：** 業務構件包含敏感資料、設定過於寬鬆或缺少對抗性測試覆蓋。

**解決步驟：**

1. 執行安全掃描：

```bash
npm run business:security
```

2. 按類別處理發現：移除硬編碼憑證、收緊權限範圍、添加對抗性測試案例。

3. 重新執行以驗證修正：

```bash
npm run business:security
```

**預期結果：** 安全掃描完成，無發現。

---

## 3. 後端和 Postgres 錯誤

### 3.1 健康端點未顯示 Postgres

**症狀：** `GET /api/v1/health/ready` 未返回 `"database": "postgres"`，或健康檢查完全失敗。

**根本原因：** `DATABASE_URL` 環境變數缺失或不正確，或 PostgreSQL 未在執行。

**解決步驟：**

1. 檢查你的後端環境檔案：

```bash
cat backend/.env
```

2. 驗證 `DATABASE_URL` 存在且格式正確：

```
DATABASE_URL=postgresql://user:pass@localhost:5432/generic_swarm_ops
```

3. 驗證 PostgreSQL 正在執行：

```bash
pg_isready -h localhost -p 5432
```

4. 如果 PostgreSQL 未在執行，啟動它（使用 systemd、Homebrew 或 Docker）。

5. 驗證資料庫存在：

```bash
psql -U user -h localhost -l | grep generic_swarm_ops
```

6. 如果缺失，建立它：

```bash
createdb -U user -h localhost generic_swarm_ops
```

7. 重新啟動後端並檢查健康狀態：

```bash
curl http://127.0.0.1:8000/api/v1/health/ready
```

**預期結果：** 健康端點返回包含 `"database": "postgres"` 的 JSON。

> **注意：** 主要資料儲存是 Postgres JSONB。JSON 檔案儲存僅作備份。如果資料庫在重新啟動後看起來是空的，請確保你連接到相同的 PostgreSQL 實例和資料庫。

### 3.2 重新啟動後資料庫為空

**症狀：** 重新啟動後端服務後資料似乎遺失。

**根本原因：** 主要儲存是 Postgres JSONB，JSON 檔案僅作備份。你可能連接到了不同的資料庫實例。

**解決步驟：**

1. 驗證你的 `DATABASE_URL` 指向正確的實例。
2. 檢查資料庫中是否有資料：

```bash
psql "$DATABASE_URL" -c "SELECT count(*) FROM runtime_state;"
```

3. 如果使用 Docker，確保容器是同一個（未在沒有卷的情況下重新建立）。
4. 對於持久性 Docker 儲存，務必使用命名卷。

**預期結果：** 資料在後端重新啟動後保持持久。

### 3.3 認證失敗

**症狀：** API 呼叫返回 401 未授權或 403 禁止存取錯誤。

**根本原因：** 認證方法不正確或憑證已過期。

**解決步驟：**

1. 使用密碼登入（首選方法）：

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin-password"}'
```

2. 回應會設定一個 cookie `gso_access_token`。在後續請求中使用它。

3. 如果收到 403 錯誤，驗證目標端點的 RBAC 權限。

> **警告：** 靜態 bearer 權杖（`admin-token`）僅用於 curl 冒煙測試。實際操作時務必使用密碼登入。

**預期結果：** 認證成功且 API 呼叫返回預期資料。

### 3.4 工具步驟失敗關閉

**症狀：** 涉及工具適配器的工作流程步驟失敗，顯示缺少輸入或拒絕執行的錯誤。

**根本原因：** 工具適配器使用失敗關閉行為 - 如果必要輸入缺失或無效，它們會拒絕執行。

**解決步驟：**

1. 檢查失敗步驟的 `tool_effects` 審計日誌。
2. 尋找失敗的特定適配器。
3. 驗證工作流程步驟設定中是否提供了所有必要輸入。
4. 修正工作流程步驟輸入並重試。

**預期結果：** 工具適配器成功執行並記錄適當的 `tool_effects`。

> **提示：** 失敗關閉行為是一個安全功能。它防止代理在資訊不完整的情況下執行操作。

### 3.5 旗艦工作流程在記憶體範圍上失敗

**症狀：** 旗艦工作流程（`wf_customer_onboarding_v12`）的執行在中途因記憶體範圍錯誤而失敗。

**根本原因：** 工作流程中的代理需要正確的 `allowed_memory_scopes`。種子/正規化聯集必須包含組織級別的範圍。

**解決步驟：**

1. 檢查失敗代理的當前記憶體範圍設定。
2. 驗證 `allowed_memory_scopes` 包含所有必要的範圍。
3. 更新代理的記憶體範圍設定：

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/agents/<agent_id> \
  -b "gso_access_token=<token>" \
  -H "Content-Type: application/json" \
  -d '{"allowed_memory_scopes": ["agent", "organization", "workflow"]}'
```

4. 重試旗艦工作流程的執行。

**預期結果：** 旗艦工作流程完成所有步驟，不再出現記憶體範圍錯誤。

### 3.6 匯入和 PYTHONPATH 錯誤

**症狀：** 從後端目錄執行測試或啟動伺服器時出現 Python 匯入錯誤。

**根本原因：** `PYTHONPATH` 環境變數未設定為後端目錄。

**解決步驟：**

1. 導航到後端目錄並設定 PYTHONPATH：

```bash
cd backend
export PYTHONPATH=.
```

2. 驗證匯入正常運作：

```bash
python -c "from app.main import app; print('Import OK')"
```

**預期結果：** 沒有 `ModuleNotFoundError` 或 `ImportError` 訊息。

> **注意：** 在執行任何後端命令之前務必設定 `PYTHONPATH=.`。

---

## 4. 前端錯誤

### 4.1 僅顯示示範資料（卡在示範模式）

**症狀：** 前端僅顯示示範/模擬資料，而不是來自後端的即時資料。

**根本原因：** `NEXT_PUBLIC_DEMO_MODE` 環境變數設定為 `true`，或 API 基礎 URL 未設定。

**解決步驟：**

1. 設定必要的環境變數：

```bash
cd frontend
export NEXT_PUBLIC_DEMO_MODE=false
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

2. 或者，建立 `frontend/.env.local` 檔案設定這些變數。

3. 驗證後端正在執行並重新啟動前端。

**預期結果：** 前端顯示來自後端 API 的即時資料。

### 4.2 變更操作未顯示詳細資訊

**症狀：** 前端中的 API 變更操作錯誤顯示通用錯誤訊息。

**根本原因：** 後端錯誤封裝包含 `message` 和 `request_id` 欄位，需要檢查網路標籤才能看到。

**解決步驟：** 開啟瀏覽器開發者工具，在網路標籤中找到失敗的請求，使用 `request_id` 在後端日誌中追蹤錯誤。

> **提示：** `request_id` 是你最有價值的除錯工具。它將前端錯誤連接到確切的後端日誌條目。

### 4.3 Playwright 冒煙測試被跳過

**症狀：** 端到端測試被跳過或失敗，因為服務不可用。

**根本原因：** Playwright E2E 測試需要後端和前端都在執行。

**解決步驟：** 在不同終端機分別啟動後端和前端，然後執行 E2E 測試。

### 4.4 OpenAPI 類型偏差

**症狀：** 前端中的 TypeScript 類型錯誤引用 API 回應結構。

**根本原因：** 產生的 OpenAPI 客戶端類型與當前後端 API schema 不同步。

**解決步驟：**

1. 確保後端正在執行。
2. 重新產生前端 API 類型：

```bash
cd frontend
pnpm api:generate
```

3. 執行類型檢查：

```bash
pnpm typecheck
```

**預期結果：** `pnpm typecheck` 通過，無錯誤。

---

## 5. 演化和自我改進錯誤

### 5.1 變體卡在沙盒中

**症狀：** 演化變體從未出現在生產環境中，仍然留在沙盒目錄中。

**根本原因：** 這是預期的行為。變體保持在沙盒中，直到完成完整的評估和金絲雀流程。`auto_promote` 始終被阻止。

**解決步驟：**

1. 檢查變體的當前狀態：

```bash
ls business/distilled/skills/_sandbox/
```

2. 驗證評估已完成：

```bash
npm run business:evolution:check
```

3. 遵循推廣管道：評估、金絲雀部署、明確推廣。

**預期結果：** 變體僅在完成完整證據鏈後才被推廣。

> **警告：** 永遠不要嘗試通過手動將檔案移動到生產目錄來繞過沙盒。治理系統要求所有推廣都具有完整的證據鏈。

### 5.2 推廣證據不完整

**症狀：** `npm run business:evolution:check` 報告變體推廣缺少證據。

**根本原因：** 推廣管道要求在變體可以被推廣之前具備評估分數、金絲雀結果和治理簽核。

**解決步驟：**

1. 執行演化檢查以查看缺少什麼：

```bash
npm run business:evolution:check
```

2. 對於缺少的評估，執行：`npm run business:eval -- --variant <variant_name>`
3. 對於缺少的金絲雀結果，通過操作控制台部署。
4. 對於缺少的治理簽核，確保模型卡已更新並獲得批准。

**預期結果：** 所有證據要求都已滿足，變體有資格進行推廣。

---

## 6. 實際使用案例範例

### 使用案例 1：新開發者入職

**場景：** 一位新開發者加入團隊，在複製儲存庫後無法讓系統運作。

**診斷路徑：** 執行 `npm run doctor` 發現版本問題，逐步升級先決條件，設定代理伺服器，最終通過健康檢查確認系統運作。

**結果：** 通過系統化的錯誤解決，在 30 分鐘內完成全端執行。

### 使用案例 2：生產工作流程失敗

**場景：** 旗艦客戶入職工作流程在計費步驟失敗。

**診斷路徑：** 通過審計日誌檢查 `tool_effects`，發現有效載荷中缺少 `case_id`，使用修正後的有效載荷重新執行。

**結果：** 通過審計軌跡檢查在 5 分鐘內識別根本原因。

### 使用案例 3：演化管道受阻

**場景：** 一個有前途的變體已被提出但不會推廣到生產環境。

**診斷路徑：** 執行演化檢查，發現缺少金絲雀證據，依序完成評估、金絲雀部署和推廣。

**結果：** 通過安全管道的系統化推廣需要 2-3 天，但確保無退化。

---

## 7. 最佳實踐

### 系統化診斷方法

1. **先識別層級：** 在嘗試修正之前，務必確定錯誤來源的層級。
2. **先執行診斷，再手動調查：** 使用 `npm run doctor`、`npm run business:validate` 和 `npm run business:security`。
3. **先檢查明顯問題：** 環境變數、服務可用性和資料庫連線佔問題的 80%。
4. **使用審計軌跡：** `tool_effects` 和審計日誌提供完整記錄。
5. **修正後驗證：** 務必重新執行診斷命令確認修正。

### 預防策略

- 在任何系統更新後執行 `npm run doctor`
- 在提交業務構件之前執行 `npm run business:validate`
- 將 `npm run business:security` 作為預提交工作流程的一部分
- 在 shell 設定檔中保留 `PYTHONPATH`
- 使用 `.env.local` 檔案來持久化環境設定

---

## 8. 章節摘要

本章涵蓋了 Generic Swarm Ops 所有四個層級常見錯誤的系統化解決：

- **引導/啟動器層級：** 來源鎖定失敗、審計警告、缺少業務種子、驗證失敗和安全掃描問題
- **後端/Postgres：** 資料庫連線、認證、工具適配器失敗關閉行為、記憶體範圍設定和 PYTHONPATH 問題
- **前端：** 示範模式設定、變更操作錯誤檢查、E2E 測試設定和 OpenAPI 類型偏差
- **演化：** 沙盒限定的變體行為、推廣證據要求和完整的推廣管道

關鍵原則是系統化診斷：識別層級、執行適當的診斷命令、遵循解決步驟並驗證修正。

---

## 9. 知識檢測測驗

**問題 1：** 你的後端健康端點返回 JSON 但未顯示 `"database": "postgres"`。需要檢查哪三項？

<details>
<summary>答案</summary>

1. 驗證 `DATABASE_URL` 在 `backend/.env` 中正確設定
2. 確認 PostgreSQL 正在執行（使用 `pg_isready`）
3. 確保 URL 中的資料庫名稱與現有資料庫匹配

</details>

**問題 2：** 全新複製後，`npm run business:validate` 報告缺少檔案。應該先執行什麼命令？

<details>
<summary>答案</summary>

執行 `npm run business:init` 來種植所需的業務層檔案，然後重新執行 `npm run business:validate` 進行確認。

</details>

**問題 3：** 前端僅顯示示範資料。必須設定哪兩個環境變數？

<details>
<summary>答案</summary>

1. `NEXT_PUBLIC_DEMO_MODE=false`（停用示範模式）
2. `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1`（指向即時後端）

</details>

**問題 4：** 工具適配器因失敗關閉錯誤而拒絕執行。應該在哪裏查看？

<details>
<summary>答案</summary>

檢查審計日誌中的 `tool_effects`。查詢 `event_type=tool.executed` 的事件以了解拒絕原因。

</details>

**問題 5：** 為什麼沙盒變體不能自動推廣到生產環境？

<details>
<summary>答案</summary>

`auto_promote` 在設計上始終被阻止。變體必須完成完整的管道：評估、金絲雀和明確的人工批准推廣。

</details>
