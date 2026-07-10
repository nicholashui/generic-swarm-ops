# `frontend_hk.md`

# Frontend Server（營運主控台）需求、設計與實作計劃

**專案：** Generic Swarm Business Operating System  
**元件：** Frontend Server（ops console）  
**架構權威來源：** `structure.md` / `structure_hk.md`（實作對應 §12）  
**狀態：** 產品標竿 mark ~100 — as-built 位於 `frontend/`  
**最後更新：** 2026-07-10  
**相關：** `frontend.md`（英文原文）· `backend.md` · `backend_hk.md` · `frontend/README.md` · `status.md` · `planning/structure/` · `planning/backend/` · `planning/frontend/` · `planning/gap_analysis_for_structure.md` · `planning/gap_analysis_for_backend.md` · `planning/gap_analysis_for_frontend.md`  

**主要目標：** 建立專業、安全、具回應式設計的 SaaS 前端，讓營運者管理 AI agents、workflows、tools、approvals、knowledge、memory、evaluations、audits、演化沙盒變體、自我改進動作，以及 organization settings。

本文件是 **frontend 需求、設計與實作計劃**（`frontend.md` 之繁體中文／香港表述）。它說明如何把 `structure.md` 架構變成營運主控台。可執行的 **架構 SDD** 位於 `planning/structure/`；**backend API 控制平面 SDD**（BE-01…24）位於 `planning/backend/` — 見 `backend.md` / `backend_hk.md` §24。**Frontend 子功能 SDD**（FE-01…20 需求／設計／任務）位於 `planning/frontend/` — 見 `planning/frontend/README.md`。**As-built 與非目標** 見下方 **§33** 及 `structure.md` / `structure_hk.md` §11.1 / §12。前端始終是展示與互動層 — **授權、執行與治理的唯一真相源是 backend。**

---

## 1. 目的

Frontend server 為平台提供面向使用者的 web application。

介面讓使用者可以：

- 登入並管理工作階段。
- 查看主 dashboard。
- 建立、檢視及管理 AI agents。
- 設定 tools 與 integrations。
- 建立及執行 workflows。
- 審閱 workflow approvals（人機閘門）。
- 管理 knowledge sources 與已索引文件。
- 檢視 memory records。
- 查看 evaluations 與品質指標。
- 監察 process runs。
- 審閱 audit logs。
- 在 run detail 上驅動 **Improve** 管線（reflect → propose → evaluate → canary）。
- 瀏覽 **evolution archive**（沙盒變體與 fitness 排序）。
- 管理 organization settings、users、billing 佔位、security 及 API keys。

Frontend 負責：

- 呈現、互動、路由、版面、UI 狀態、前端驗證、體驗、客戶端即時更新、設計系統實作。

Frontend **不得**承載核心 backend 業務邏輯。

---

## 2. 產品願景

Frontend 應感覺像嚴肅的企業 SaaS 營運平台，而非 generic AI demo。

介面應傳達：信任、可靠、營運清晰、安全、專業、速度、控制、可觀測。

使用者應始終理解：有哪些 agents／workflows、什麼在跑、什麼失敗、什麼待審批、知識源狀態、用了什麼資料、採取了什麼動作、誰做了什麼、什麼需要關注。

---

## 3. 核心設計原則

重大頁面版面應先經 **OpenDesign MCP**（若不可用，必須寫入文件化 fallback — as-built：`frontend/docs/design/open-design-reference.md`）。

工作流：

```text
Trae
  -> OpenDesign MCP（或 documented fallback）
    -> 搜尋設計參考
    -> 選設計系統
    -> 提取 tokens 與版面指引
    -> 產出 layout plan
    -> 實作 React / TypeScript / Tailwind frontend
```

不得只靠 generic AI 記憶做設計。

---

## 4. 範圍

### 4.1 範圍內

- 公開 root／重導；認證頁（login、register、forgot/reset、**accept-invite**）。
- 已驗證 app shell；dashboard。
- Agents／Tools／Workflows／Run detail／Approvals。
- Knowledge／Memory／Evaluations／Processes／Audit。
- **Evolution** 區；**Improve** 於 run detail。
- Organization／user settings；API keys；security；billing 佔位。
- 回應式版面；loading／empty／error；權限感知導航。
- 型別化 API（OpenAPI 產生型別）；即時 run UI。
- Ops profile：`NEXT_PUBLIC_DEMO_MODE=false` 對接 live backend + Postgres。

### 4.2 範圍外

- Workflow／agent／tool 執行引擎。
- 以前端為唯一授權真相。
- 直接寫入資料庫、背景 job、embedding／索引。
- 密鑰儲存、瀏覽器內 provider API key。
- 建立 audit 系統紀錄、計費計算。
- 靜默改寫 production DNA；host 應用自我改寫 UI。
- 最終認證驗證（backend 為準）。

Backend 仍是 authn／authz、執行、知識、記憶、評估、治理、audit、組織安全的真相源。

---

## 5. 建議技術棧

```text
Next.js · React · TypeScript · Tailwind CSS
```

```text
Browser -> Next.js Frontend Server -> Backend API (FastAPI) -> services
```

建議架構：hybrid 渲染 — 靜態／殼用 server components；即時時間軸、表單、command palette、modal 等用 client components。

---

## 6. 執行期職責

| Frontend | Backend |
|----------|---------|
| 渲染、路由、前端路由保護（UX） | 認證驗證、授權、角色權限 |
| 呼叫 API、UI session | Agent／workflow／tool 持久化與執行 |
| 顯示資料與錯誤、即時更新 | 審批狀態轉移、audit 寫入 |
| 角色感知導航、tokens、靜態資產、a11y | 知識索引、記憶寫入、評估、治理、密鑰 |

**邊界規則：** Frontend 可請求動作；Backend 決定是否允許。隱藏按鈕不是安全機制。

---

## 7. 應用架構

```text
User Browser --HTTPS--> Next.js Frontend --API--> Backend
  Auth · Agents · Tools · Workflows · Runs · Approvals
  Knowledge · Memory · Evaluation · Audit · Organization
```

受保護路由：`/app/*`  
- 未登入 → `/login`  
- 無 org／權限 → 選 org 或 403 Access Denied（UX only）  
- Backend 授權為最終依據  

---

## 8–11. OpenDesign、Trae 規則與 prompts

與 `frontend.md` §8–11 一致：

- 重大 layout 前呼叫 `opendesign` MCP；不可用則 **documented fallback**。
- 專案規則：API-first、前端不執行工作流、不把 client 權限當最終授權。
- Trae prompts 應要求對齊 design tokens、EARS 需求、以及 `planning/frontend/` 規格。

As-built：`frontend/docs/design/open-design-reference.md` 記錄 fallback。

---

## 12. 資訊架構

### 12.1 主要路由

```text
/
/login  /register  /forgot-password  /reset-password  /accept-invite

/app
/app/agents  /app/agents/new  /app/agents/[agentId]
/app/tools   /app/tools/[toolId]
/app/workflows  /app/workflows/new  /app/workflows/[workflowId]
/app/workflow-runs/[runId]
/app/approvals  /app/approvals/[approvalId]
/app/knowledge  /app/knowledge/sources  /app/knowledge/search  ...
/app/memory
/app/evaluations  /app/processes
/app/audit-logs
/app/evolution
/app/settings  /app/settings/organization  /app/settings/users
/app/settings/roles  /app/settings/billing  /app/settings/api-keys
/app/settings/security  /app/settings/integrations  /app/settings/profile
```

As-built：多數已驗證區可由動態 `/app/[...slug]` 面板提供；上述 URL 仍是導航與 deep link 的 **資訊架構**。

### 12.2 導航分組

```text
Main: Dashboard · Agents · Workflows · Approvals
Data: Knowledge · Memory
Quality: Evaluations · Processes · Evolution
Security: Audit Logs
Admin: Settings
```

### 12.3–12.4 Header 與 Command palette

Header：breadcrumbs、command／搜尋、環境指示、org switcher、通知、user menu。  
Command palette：`Cmd/Ctrl+K` — 建立 agent／workflow、搜尋知識、最近 run、審批、邀請、API keys、audit、security、評估、知識源等。

---

## 13. 使用者角色與權限

建議角色：Owner · Admin · Developer · Operator · Reviewer · Viewer · Billing Manager · Security Auditor。

- 前端：依 `/auth/me` 或角色矩陣做 **UX 層** 隱藏／停用。
- 後端：最終 403／允許。
- 缺權限資料時 **fail closed**。

---

## 14–15. 核心版面與視覺

- 企業營運密度：可掃描表格、清晰狀態、克制動效。
- Status badges：running／succeeded／failed／awaiting approval／paused／cancelled／expired 等。
- 設計 tokens：色彩、字型、間距、狀態語義（`src/design/*`）。

---

## 16. 頁面需求（摘要 + as-built 重點）

### 16.1–16.3 公開與認證

- `/` 落地或重導。
- `/login`：提交至 `POST /api/v1/auth/login`；成功建立 session → `/app`；錯誤顯示 message + `request_id`。
- `/register`：若後端關閉，顯示 invite-only。
- **`/accept-invite`（§16.3a）**  
  - `POST /api/v1/users/invitations/accept` `{ token, password, name? }`  
  - 公開端點；成功後寫入 session 並導向 `/app`。  
  - As-built：`AcceptInviteForm` + `backendApi.acceptInvitation`；`?token=` 預填。

### 16.4 Dashboard

營運總覽：metric cards、pending approvals、failed runs、onboarding checklist、quick actions。

### 16.5–16.9 Agents／Tools

列表／建立／詳情；Zod + react-hook-form 真實建立；不在瀏覽器執行 agent／tool。

### 16.10–16.12 Workflows

列表／建立／詳情；**Run Now** → 後端 start run → 導向 run detail。

### 16.13 Workflow Run Detail（關鍵頁）

- 狀態、timeline、logs、即時 SSE（降級 reconnect／poll 意圖）。
- 動作：cancel／retry／**pause／resume／expire**（as-built：`WorkflowRunConsole`）。
- **Improve**：Reflect → Propose → Evaluate → Canary（僅 backend API；禁止 client 改 production DNA）。
- 待審批 callout → approvals。

### 16.13a Evolution Archive

`/app/evolution` — 沙盒變體 fitness 列表；evaluate／canary／promote 經 backend；無 client DNA rewrite。

### 16.14–16.15 Approvals

列表／詳情；明確 approve／reject；禁止靜默 auto-approve。

### 16.16–16.23 Knowledge／Memory／Evals／Processes／Audit

以 backend 讀取為主；搜尋 debounce；audit **唯讀**（前端不建立系統 audit 紀錄）。

### 16.24–16.28 Settings

- Hub 與子路由。
- **Users**：`UserAdminPanel` — 列表、invite（`POST /users/invitations`）、disable／enable（`PATCH /users/{id}`）。
- **Organization**：`OrganizationSettingsForm` — `GET` + `PATCH /organizations/{id}`。
- **API keys**：列表／遮罩；建立後一次性顯示密鑰（若後端回傳）。
- Billing：佔位即可，不虛構收費。

---

## 17. 可重用元件

Button、Input、Card、DataTable、StatusBadge、MetricCard、EmptyState、ErrorState、Skeleton、Timeline、LogViewer、Section、command palette、domain panels（run console、improve、approvals、evolution、user admin、org form）等。

---

## 18. 資料夾結構（as-built 對齊）

```text
frontend/
  src/app/          # routes: login, accept-invite, app/*
  src/components/   # ui, layout, domain, auth
  src/lib/          # api, auth, config, realtime, forms, data, errors
  src/design/       # tokens, theme, status
  src/hooks/  src/stores/  src/types/
  tests/unit/  e2e/
  docs/api/  docs/design/
  openapi.json
```

---

## 19. 環境變數

| 變數 | 用途 |
|------|------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend `/api/v1` base |
| `NEXT_PUBLIC_DEMO_MODE` | `false` = ops（live）；`true`/unset = UI demo |

**Ops profile（產品標竿）：** `NEXT_PUBLIC_DEMO_MODE=false` + 運行中的 FastAPI + Postgres。

密鑰不得使用 `NEXT_PUBLIC_` 前綴暴露。

---

## 20. API 整合

- 僅呼叫版本化 `/api/v1/*`。
- 型別：`pnpm api:generate` → `src/lib/api/generated/openapi.d.ts`。
- 錯誤：顯示 message 與 `request_id`（`AppError`）。
- Facade：`src/lib/api/client.ts`（`backendApi`）。

主要合約域：auth、users、invitations、organizations、agents、tools、workflows、runs（含 pause／resume／expire）、approvals、knowledge、memory、evaluations、processes、audit、evolution、improvement。

---

## 21. 即時 Run 更新

- 優先 SSE（`EventSource` / stream）。
- 連線狀態指示；錯誤時 reconnecting。
- 事件去重；不在瀏覽器執行步驟。

---

## 22–23. Loading／Empty／Error 與無障礙

- 主要資料頁必須有 loading／empty／error。
- Error 含 `request_id` 時應顯示。
- 鍵盤可操作、表單標籤、焦點管理；狀態不只靠顏色。
- 目標：WCAG 2.2 AA 實務。

---

## 24–26. 安全、效能、可觀測

- 無 provider secrets 於 client bundle；XSS-safe 渲染。
- 列表可分頁／合理體量；重元件可 code-split。
- 錯誤關聯 `request_id`；不向終端使用者傾倒 stack／密鑰。

---

## 27. 測試需求

- Unit（vitest）、lint、typecheck、build。
- E2E smoke 可在伺服器未啟動時 skip（非 always-on CI 硬性要求）。
- As-built：unit 綠燈；build 通過。

---

## 28. 實作計劃（對應 phases → FE 規格）

| Phase | 內容 | FE SDD |
|-------|------|--------|
| 0–1 | 合約、scaffold | FE-01–02 |
| 2–3 | OpenDesign／tokens | FE-03 |
| 4–5 | Auth、shell | FE-05–04、FE-06–07 |
| 6–10 | Dashboard…approvals | FE-08–12 |
| 11–13 | Knowledge…settings | FE-13–16 |
| Evolution／Improve | 沙盒與改進 | FE-17–18 |
| 14 | 品質與發佈 | FE-19–20 |

完整任務見 `planning/frontend/*/tasks.md`。

---

## 29–31. 產品想法、驗收、DoD

- 每頁：可達路由、權限感知、三態、API 或文件化 stub、無 charter 違規。
- 產品標竿驗收見 §33.7。

---

## 32. 最終 Frontend 規則

1. Backend 是授權與執行真相源。  
2. 前端不執行 agents／workflows／tools。  
3. 不靜默改 production DNA。  
4. 重大 layout 用 OpenDesign 或 documented fallback。  
5. 變更 API 後 `pnpm api:generate`。  
6. Ops profile 才是產品真相路徑。  

---

## 33. 實作對應（structure §11.1／§12 + backend SDD）

本節記錄 **產品標竿 mark ~100** 下前端計劃如何落地。證據：`status.md`、`frontend/README.md`、`planning/gap_analysis_for_frontend.md`、`planning/frontend/*`。

### 33.1 文件關係

| 文件 | 角色 |
|------|------|
| `structure.md` / `structure_hk.md` | 架構願景與 SoT |
| `planning/structure/nn_*/` | 架構 SDD 01–17 |
| `backend.md` / `backend_hk.md` | Backend 計劃 + as-built §24 |
| `planning/backend/nn_*/` | BE-01…24 子功能 SDD |
| `frontend.md` | 英文 frontend 計劃 |
| `frontend_hk.md`（本檔） | 繁中／香港表述 |
| `planning/frontend/nn_*/` | FE-01…20 需求／設計／任務 |
| `planning/gap_analysis_for_frontend.md` | 任務 vs 實作（產品標竿 100/100） |
| `frontend/` | As-built Next.js ops console |
| `backend/` | As-built FastAPI 控制平面 |

**依賴規則：** 前端永不重做 backend 政策。新功能必須呼叫版本化 `/api/v1/*`，並在 schema 變更後 `pnpm api:generate`。

### 33.2 能力閘（structure §11.1 前端份額）

| 階段 | structure 區間 | Frontend as-built |
|------|----------------|-------------------|
| A 基礎 | Days 1–14 | 認證、app shell、權限導航、健康空／錯態 |
| B 影子學習 | Days 15–30 | Knowledge／memory／process 視圖 |
| C 可控副駕駛 | Days 31–60 | Live ops：真實表單、run-now、run detail、人機閘、OpenAPI client |
| D 演化沙盒 | Days 61–90 | Improve 管線；`/app/evolution`；evaluate／canary 僅 backend |

### 33.3 As-built 主題對照

| 主題 | 意圖 | As-built |
|------|------|----------|
| Ops console | 以人為中心 | `frontend/` Next.js |
| Live vs demo | 真實營運路徑 | `DEMO_MODE=false` + live BE／Postgres |
| 表單／變更 | 正確 + 可審計 | Zod + RHF；錯誤含 `request_id` |
| 人機閘 | 有界自主 | 審批面板；backend 授權 |
| 自我改進 UI | 反思迴圈 | Improve 四步於 run detail |
| 演化 UI | 僅沙盒 | evolution archive；無 client DNA rewrite |
| 認證／邀請 | 帳號生命週期 | login live；accept-invite → accept API |
| Settings | 使用者／組織 | UserAdminPanel；OrganizationSettingsForm；API keys |
| Run 生命週期 | 營運干預 | cancel／retry／pause／resume／expire |

### 33.3a 必須遵守的 Backend 合約

| 域 | Backend API（`/api/v1`） | FE 表面 |
|----|-------------------------|---------|
| Auth | login／refresh／logout／me／api-keys | Login、session |
| Users | GET／POST／PATCH users | Settings users |
| Invitations | GET／POST invitations；POST accept | Invite + `/accept-invite` |
| Organizations | GET／PATCH organizations | Settings organization |
| Runs | start、list、stream、cancel、retry | Run detail |
| Run lifecycle | pause／resume／expire | Run detail 動作 |
| Approvals | list、decision | Approvals |
| Evolution | variants、archive、evaluate、promote | `/app/evolution` |
| Improvement | reflect、auto-propose、… | Improve 管線 |
| Knowledge／memory／eval／PI／audit | 對應 BE 路由 | 各 domain 區 |

### 33.5 明確非目標（現產品標竿）

- Always-on Playwright 永久伺服器  
- 完整商業 LightRAG／Neo4j 圖探索產品  
- 即時外部 CRM／email／billing SaaS 管理台  
- DGM 式 host 自我改寫 UI  
- 以前端權限取代 backend 授權  
- 無限填滿每個 `business/` 葉節點內容  

### 33.6 執行入口

| 層 | 入口 |
|----|------|
| Frontend | `frontend/` |
| API | `backend/` FastAPI |
| FE SDD | `planning/frontend/` |
| 差距分析 | `planning/gap_analysis_for_frontend.md` |
| OpenAPI | `pnpm api:generate` |
| Ops profile | `NEXT_PUBLIC_DEMO_MODE=false` + BE + Postgres |

### 33.7 相對 mark ~100 的驗收（已出貨）

```text
- Auth + app shell + 動態 /app domain 表面
- 真實 agent／workflow 建立表單
- Run now + 有效 payload
- Improve 管線於 run detail
- /app/evolution archive
- 型別化 API client + OpenAPI 產生
- Accept-invite → POST invitations/accept
- Settings：邀請／停用使用者 + organization PATCH
- Run detail：cancel／retry／pause／resume／expire
- lint / typecheck / unit tests / build 綠燈
- planning/frontend FE-01…20 SDD 完整
- gap_analysis_for_frontend 產品標竿 100/100
```

**可選衛生工作（非產品標竿阻斷）：** backend schema 變更後執行 `pnpm api:generate`。

先前驗收清單中的完整 billing、always-on E2E CI、OpenDesign 永遠可用等，維持 **願景或非目標**，不阻斷 mark ~100 — 對齊 `structure.md` §12.4 與 `backend.md` §24.5。

---

## 文件控制

| 欄位 | 值 |
|------|-----|
| 英文原文 | `frontend.md` |
| 本檔 | `frontend_hk.md` |
| 同步日期 | 2026-07-10 |
| 實作目錄 | `frontend/` |
| 子功能規格 | `planning/frontend/nn_*/` |

**完。**
