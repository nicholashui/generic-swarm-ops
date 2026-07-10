# 採用計劃：generic-swarm-ops（通用平台）× va-agent-swarm（影片領域）

**版本：** 2.3  
**日期：** 2026-07-10  
**狀態：** 可執行合併策略（產品標竿 mark ~100 之後）——**要求完整 va 代理人名冊 + 完整流程樹**（已重新思考執行順序）  
**作者：** 依 `review_adoption.md` 審閱兩個本機儲存庫  
**審核來源（深度本機掃描 2026-07-10）：**
- `C:\Project\generic-swarm-ops`（https://github.com/nicholashui/generic-swarm-ops）
- `C:\Project\va-agent-swarm`（https://github.com/nicholashui/va-agent-swarm）

**英文原文：** `adoption.md`（本檔為對應繁體中文版，與 **v2.3** 對齊）

### 重新思考（v2.3）——保留什麼、改變什麼

N3 仍然成立：**全部 114 位代理人與全部流程最終都在 generic 內，並永久保留。**  
針對執行風險重新思考後，改變的是**怎麼做**，不是要不要做：

| 保留（不可妥協） | 改變（執行方式） |
|------------------|------------------|
| 完整名冊**保留在倉庫內** | **目錄 ≠ 完整 SPEC。** Wave 0 = ROSTER + 目錄 + MAP + 最小 agent_spec。深度 SPEC 在**代理人啟用時**再填，不是第一次 E2E 前寫完 114 篇長文。 |
| 完整流程**覆蓋** | **先流程索引，後 DNA 深度。** PROCESSES.md 早期列出每一條流程。可跑 DNA 先做脊柱 + 原型 A；B–J／LQR 在脊柱跑通後再加深。 |
| 作用中代理人的 ALC | **ALC 硬閘只在 `active`／`production_ready`**，不擋 draft 佔位（draft 仍帶 `requires_alc: true` 欄位）。 |
| 不做第二控制平面 | 不變——LangGraph／Temporal 願景映射到 generic DNA／步驟。 |
| 保護 E1／mark ~100 | **先平台 ALC + Domain Pack（最小 example）**，再大量影片內容，確保主機保持綠燈。 |

**三個成熟度層級（勿混淆）：**

| 層級 | 名稱 | 含義 | 目標階段 |
|------|------|------|----------|
| **L0 目錄（Catalog）** | 已存在 | 有目錄 + ROSTER／MAP 列 + draft agent_spec | 階段 0–2 前期 |
| **L1 流程已索引（Process-indexed）** | 可觸達 | 出現在 PROCESSES.md／standby_pool／DNA stub | 階段 2 |
| **L2 執行期（Runtime）** | 可運行 | active（或 registered 且被呼叫）、ALC 已強制、工具可 stub、掛在真實 DNA 路徑 | 波次 1–6 |

**結果表述要誠實：**「採用完成（N3）」= 全部代理人 ≥ **L1**、脊柱 ≥ **L2**、盤點 CI 綠、流程已索引。「生產級影片蜂群」= 逐步把更多代理人推到 L2——以月計，不是一個 sprint。

**本 rethink 要避開的失敗模式：**（1）第一次 demo 前堆 114 份空殼 SPEC；（2）只做 viral-hook 就宣稱 N3 完成；（3）雙編排器混淆——營運種子 `business_orchestrator` 留在 **ops 域**；影片只用 `video.orchestrator` 命名空間。

### 研究快照（實證）

| 語料 | 量測事實 |
|------|----------|
| **va** 檔案 | **92** 份 `.md`、**141** 份 script/txt 變體、**19** 份 SVG、**2** 份 `.py`（僅 SVG 輔助） |
| **va** `study/` | **277** 檔；參考章節 **68** 份於 `study/reference/how_to_build_a_video_agent_system/` |
| **va** UI 文件 | **42** 檔於 `study/ui/` |
| **va** 工作流 | 原型 SVG **A–J 共 10** + LQR SVG **6** 於 `study/workflows/` |
| **va** 代理人名冊 | **114** 個唯一代理人，id **1–114**，**10** 大類——自 `study/agents.md` 解析（名稱含 Agent），並與 `SYSTEM_REFERENCE.md` 交叉核對 |
| **va** 深度規格 | 功能／技術：aesthetics、optimization、research、intent、coding、GCA、agentic RAG、podcast、心理側寫／推薦、編劇／策略目標、LLM usage、agent_loop v1–v3、planner v2.0–2.1、system_build_plan 等 |
| **generic** 產品標竿 | Mark **~100**，E1 **PASS**（`status.md`） |
| **generic** API 路由 | auth、users、orgs、agents、tools、workflows、workflow_runs、approvals、governance、knowledge、memory、evaluations、audit_logs、processes、evolution、improvement、loops、settings、health——**無 `domains` 路由** |
| **generic** business schemas | 僅有 WorkflowDNA、EvaluationCard、DecisionRequirementCard、EventLog——**無** agent-spec／domain-manifest／learning-log |
| **generic** 影片包 | **`business/video/` 不存在** |
| **generic** 種子代理人 | 5 個營運代理人：`business_orchestrator`、`quality_compliance_agent`、`execution_agent`、`finance_ops_agent`、`communications_agent` |
| **generic** 工具適配器 | 僅 `audit_log_writer`、`crm`、`billing_system`、`email`、`contract_parser`、`policy_retriever` |
| **generic** 金任務 | **20** 份 customer-onboarding JSON 於 `business/evals/golden-tasks/` |
| **generic** 磁碟 lessons | **約 168** 份 `business/evolution/lessons-learned/run_*.json`（工作流層級） |
| **generic** 學習缺口 | `Lesson` 有 `workflow_id`，**無 `agent_id`**；reflect 寫組織記憶且 `agent=None` |
| **generic** 前端領域 | Improve、evolution archive、run console、user admin、org settings——**無影片領域包 UI** |

---

## 0. 不可妥協要求（審閱合約）

| # | 要求 | 本計劃如何強制執行 |
|---|------|-------------------|
| **N1** | **va-agent-swarm** 保留**全部**影片代理人專屬業務邏輯；每個代理人必須具備**強制自主學習**（個體知識成長） | 影片邏輯只放在領域包路徑（`business/video/` + 可選 va 薄倉庫鏡像）。每位代理人草稿即帶 ALC 欄位；**狀態變 `active` 或 DNA `production_ready` 時硬閘**強制 ALC，否則拒絕啟用／晉升。 |
| **N2** | **generic-swarm-ops** 成為可承載數十個多代理人（MMA）系統的**通用基礎**，不限於影片 | 引入 **Domain Pack** 介面、結構描述、註冊掛鉤與隔離，使任何 `business/<domain>/` 上線只需設定與產物，而**不是**分叉 runtime。 |
| **N3** | **採用 va-agent-swarm 的全部代理人與全部業務流程**進入 generic 專案——自**編排器／規劃器／元代理人一路到每一位專精與工作流支援代理人**。**禁止丟棄、歸檔淘汰，或只把代理人長期留在外部 va 倉庫。** | （1）**完整名冊匯入**：va 全目錄 114 代理人／10 類（`study/agents.md` + `SYSTEM_REFERENCE.md`）→ `business/video/agents/`，穩定 id + MAP 可追溯。（2）**完整流程匯入**：每一條 va 業務流程／管線／LQR／原型工作流 → `business/video/workflows/` 下 Workflow DNA（或 DNA 族），含 Orchestrator、Planner、Router、Judge 與對葉節點代理人的交接。（3）**保留政策**：所有代理人永遠以包產物形式**留在專案內**（specs + agent_spec + ALC）；runtime 啟用可分波，但**禁止刪除或「以後再說」省略**。（4）閘門：包 CI／盤點在 MAP 數 < 名冊數或缺少代理人目錄時失敗。 |

**合併形狀（一句話）：**  
generic-swarm-ops = 受治理 runtime + 學習引擎 + MMA 外掛主機；  
va-agent-swarm = **完整**影片領域包——**每一位代理人與每一條業務流程**（編排器 → 專精 → 工作流支援），規格 → Workflow DNA + 代理人 + 評估 + 工具，**強制**每代理人 ALC，且**完整名冊必須保留在專案內**。

### 0.1 完整名冊與完整流程強制令（N3 細節）

| 強制項 | 含義 | 禁止 |
|--------|------|------|
| **全部代理人** | va 定義的每一位代理人（`study/agents.md` 1–10 類、id 1–114）都匯入 generic `business/video/agents/<pack_id>/` | 以「僅 P0 包」當*最終*狀態；省略元代理人或 81–114 支援代理人 |
| **全部業務流程** | 每一條 va 流程／工作流（人→AI 映射、LQR、原型 A–J、系統編排層、批判／QC 網、交付織物等）都表示為 Workflow DNA 或連到 DNA 的包流程文件 | 編排只留在 va 散文；只做 viral-hook 就宣告採用完成 |
| **編排器向下層級** | 流程樹永遠含頂層編排（OrchestratorAgent、PlannerAgent、RouterAgent、JudgeAgent 等價物）**與**其呼叫的每一位下游代理人 | 無編排路徑的孤兒專精；有編排器無專精 |
| **留在專案內** | 包目錄、MAP、manifest，以及（啟用後）runtime 登錄，活在 **generic-swarm-ops** git；va 仍是上游研究／敘事真相源，但**不是**代理人「存在」的唯一位置 | 依賴「需要時再讀 va」；為縮範圍刪除未用代理人資料夾 |

**分階段 vs 完整性（重要；v2.3 成熟度對齊）：**

| 層 | 完整規則 |
|----|----------|
| **L0 倉庫目錄** | 階段 0–2 早期：`business/video/` 有 **114 目錄 + ROSTER + MAP + 最小 agent_spec**（stub SPEC 可接受）。 |
| **L1 流程索引** | 階段 2：每一位代理人出現在 PROCESSES.md 與／或 DNA stub 與／或 `standby_pool`；流程族全部**列在索引**（DNA 深度可後補）。 |
| **L2 Runtime** | 分波：draft → active；ALC 在 **active／production_ready** 硬閘；工具可先 stub。檔案即使未 active 也必須以 draft／registered 留在樹內。 |
| **N3 完成（階段 5）** | 全部代理人 ≥ L1、脊柱 ≥ L2、盤點／保留／孤兒 CI 綠、流程已索引且已綁定 DNA／standby——**不是** 114 位全部 L2。 |
| **MVP（階段 2）** | 證明**脊柱 L2**（編排器 + viral-hook 等），**不得**放棄其餘名冊的 L0；目錄須在 0–2 已齊。 |

---

## 1. 執行摘要

### 1.1 現況（深度掃描 2026-07-10）

**generic-swarm-ops** 是已出貨的**產品標竿平台**（mark ~100，E1 操作者路徑 PASS，見 `status.md`）：

- FastAPI 控制平面 + Postgres `runtime_state` JSONB、RBAC、稽核、審批、SSE（`workflow_runs` 生命週期含 cancel／retry／pause／resume／expire）。
- Workflow DNA + `structure_validators`；演化：propose／evaluate／canary／rollback／archive，強制 **`sandbox_only`**。
- 自我改進 API：`POST /improvement/reflect/{run_id}`、lessons 列表、auto-propose、skill sandbox、loops；前端 `ImproveRunButton` + `evolution-archive-panel`。
- 知識：Tier-0 + K1-lite；雙 harness Trae + Grok；SDD 包 + gap analysis **100/100**。
- 營運種子：**5** 個業務代理人 + **6** 個本機工具適配器 + **20** 個入職金任務 + 旗艦 `wf_customer_onboarding_*`。

**N1–N3 關鍵缺口（磁碟已確認缺失）：**

| 缺口 | 證據 |
|------|------|
| 無影片 Domain Pack | `business/video/` 不存在 |
| 無 Domain Pack SDK | 無 domain-manifest／agent-spec／learning-log schemas；無 `/api/v1/domains` |
| 學習非每代理人 | `lessons.py` 的 `Lesson` 缺 `agent_id`；reflect → 組織記憶 `agent=None` |
| runtime 無名冊 | 種子僅營運代理人，非 Director…ArchiveMaster |
| 無影片工具 | 適配器僅 CRM／billing／email／contract／policy |
| 領域代理人模組為 stub | `backend/app/domain/agents/models.py` 為佔位 |

**va-agent-swarm** 是**完整規格語料庫，幾乎無可執行產品**：

| 區域 | 掃描結果 |
|------|----------|
| 規模 | 92 MD、141 script txt、19 SVG、2 py |
| 名冊 | **114 代理人**（見**附錄 A**），`study/agents.md` 1–10 類 |
| 編排脊柱 | **#53 OrchestratorAgent、#54 PlannerAgent、#55 RouterAgent、#56 JudgeAgent**（+ GateKeeper #57 … SafetyRedTeam #80） |
| 流程 | `SYSTEM_REFERENCE.md` §6 六階段製作管線；原型 **A–J**；**LQR** 六張 SVG；人→AI 工作流文件 |
| 深度規格 | research、optimization、GCA、aesthetics、intent（DIA）、coding、agentic RAG、podcast、心理側寫／推薦、編劇／SGA、LLM usage、agent_loop v1–v3、planner v2.x、system_build_plan |
| 願景棧（**不要重建**） | React 19 + Next 15、FastAPI + **LangGraph + Temporal + Redis**、Sora／Veo／Runway／ElevenLabs——應映射到 generic **as-built** |
| Runtime | **無**（僅 SVG 輔助腳本） |

### 1.2 目標終態

```text
┌──────────────────────────────────────────────────────────────────────┐
│ generic-swarm-ops  （通用 MMA 主機）                                   │
│  runtime · 治理 · 評估 · 演化 · ALC 強制                               │
│  Domain Pack SDK · schemas · APIs · FE 營運主控台外殼                   │
└───────────────┬───────────────────────────────┬──────────────────────┘
                │ 註冊完整名冊                   │ 註冊
                ▼                               ▼
     business/video/ （完整 va 包）     business/<下一領域>/
     全部代理人 (1–114, 10 類)         agents · workflows · tools
     全部流程 (編排器→葉節點)           evals · knowledge seeds
     workflows · tools · evals · seeds ALC 綁定強制
     ALC 綁定強制 · 永久保留
```

- **va 倉庫** 繼續做上游**研究／旁白／雙語腳本**真相源；**已採用的代理人與流程的權威副本住在 generic** `business/video/`，不得移除。
- **generic 倉庫** 以 Domain Pack 承載**完整影片蜂群**（非硬編碼特例），並承載未來其他領域包。
- 層級保留：**Orchestrator／Planner／Router／Judge → 類別專精 → 工作流支援代理人**，以 Workflow DNA 圖表達，並可隨時間呼叫完整名冊。

### 1.3 成功定義

**平台／學習（N1–N2）**

1. Domain Pack + ALC 對影片可用（第二示範包證明 N2）。
2. 每一位**作用中**代理人在 run 後有 agent 範圍 lessons + 記憶成長。
3. 演化提案在受閘晉升前保持 **`sandbox_only`**；禁止 host 程式自我改寫。

**完整 va 採用（N3）——全部必達（L0／L1／L2 表述）**

4. **代理人完整（≥ L1）：** `business/video/agents/` 含 va 名冊每一位（10 類／114）；`MAP.md` 一對一；盤點 CI 通過；每人可經 DNA 或 `standby_pool` 觸達。
5. **流程完整（索引 + 綁定）：** 所有 va 業務流程在 PROCESSES.md 索引；對應 Workflow DNA 或連結文件存在於 `business/video/workflows/`（深度可分波，但不得永遠只寫在 va 散文）。
6. **編排器向下完整性：** 至少一條可跑 DNA 族自 `video.orchestrator`／`video.planner` 起（**不是** ops 的 `business_orchestrator`）；可路由到專精（工具可 stub）。
7. **保留：** 不得刪除名冊代理人；未啟用者維持 `draft`／`registered` 並帶 ALC 欄位。
8. **Runtime 脊柱（≥ L2）：** 至少一條 E2E（如 viral-hook）含人類閘門與稽核；其餘代理人分波升到 L2，且不丟 L0 產物。

---

## 2. 兩倉庫完整稽核

### 2.1 generic-swarm-ops — 架構

| 層 | 位置 | 成熟度 |
|----|------|--------|
| 入門／雙 harness | `.trae/`、`.grok/`、`scripts/sync.mjs` | 高 |
| 業務 OS 產物 | `business/`（schemas、≥20 golden、治理、PI、演化 lessons） | 高 |
| 後端 API | `backend/app/api/v1`、`runtime.py`、domain + infrastructure | 高（產品標竿） |
| 前端營運主控台 | `frontend/` Next.js | 高 |
| 演化沙箱 | APIs + corpus eval + archive UI | 中–高 |
| 自我改進 | reflect／lessons／auto-propose／loops／skill sandbox | 中（偏工作流中心） |
| 代理人實作 | 登錄 + 種子代理人；`backend/app/domain/agents` | **薄**——非領域專家 |
| 多領域外掛主機 | 僅隱含於 `business/` | **缺正式 Domain Pack 合約** |
| 每代理人學習強制 | 部分 memory scopes | **缺強制 ALC** |

**優勢：** 生產導向治理；可用 run 生命週期 + SSE + tool_effects；演化從不直接改生產 DNA（`sandbox_only`）；自我改進文件地圖；SDD + gap 關閉結構／後端／前端標竿；擴充點為 `business/` + Workflow DNA schema。

**技術債：** 代理人學習非個體化；無 Domain Pack SDK；演化適應度多半在 workflow DNA；缺多模態媒體工具；文件願景棧 vs as-built（Postgres JSONB + 程序內 run）；大型 `external/sources/` 僅參考。

**應保留／延伸（不要重寫）：** `runtime.py`、演化 promote／canary／rollback、FE Improve + evolution archive、既有 schemas、演化沙箱／人類審批／安全規則。

### 2.2 va-agent-swarm — 架構

| 區域 | 位置 | 成熟度 |
|------|------|--------|
| 系統地圖 | `study/SYSTEM_REFERENCE.md` | 規格完整（願景棧） |
| 代理人名冊（114） | `study/agents.md` | 規格完整 |
| 工作流／LQR／SVG | `study/workflows/` | 設計完整 |
| 深度規格 | aesthetics、optimization、research、psychological_*、coding、creative、intent、screenwriter、podcast、agentic_rag、agent_loop v1–v3 等 | 規格完整 |
| 建置計劃 | `study/system_build_plan.md`（M0–M12） | **計劃**可實作，無建置 |
| 專案啟動／迴圈 | `project_starter_*`、`agent_loop_creator_*`、`plan/` | 迭代研究 |
| Runtime／測試／CI | — | **缺席** |

**優勢：** 影片領域拆解極深；明確 self-refine／Reflexion／情節記憶意圖；system_build_plan 垂直切片哲學（G1–G7）；雙語／腳本利於知識播種。

**技術債：** 架構薄弱（無可執行後端前端）；規格蔓延；假設 LangGraph／Temporal／Redis 棧；學習僅描述；範圍 114 代理人——**N3 要求完整匯入與保留**，runtime 以脊柱先啟用，而非永久子集。

**應遷移關鍵資產（權威副本在 generic 包；va 為上游）：** 完整 1–114 名冊；完整流程樹；品質閘／批判；Agentic RAG；參考語料；可列出完整名冊的 FE 領域路由。

### 2.3 互補適配矩陣

| 關注點 | generic 現況 | va 現況 | 合併後擁有者 |
|--------|--------------|--------|--------------|
| 認證、RBAC、稽核 | 強 | 無 | generic |
| 工作流執行 | 強 | 僅規格 | generic |
| 演化沙箱 | 強 | 僅命名 | generic（+ 代理人基因體） |
| 影片創意邏輯 | 無 | 強規格 | **va／business/video** |
| 每代理人學習 | 弱 | 僅規格 | **generic ALC 對所有包強制** |
| 營運 UI | 強 ops console | 願景規格 | generic + 影片頁 |
| 對 N 個 MMA 通用性 | 部分 | 不適用 | generic Domain Pack |

---

## 3. 目標架構（重新設計）

### 3.1 Domain Pack 合約（通用 MMA 接入）

每個 MMA 系統（影片為先）都是 **Domain Pack**：

```text
business/<domain_id>/
  manifest.json          # id、version、risk_default、entrypoints
  README.md
  agents/
    <agent_id>/
      agent_spec.json    # role、tools、memory scopes、ALC flags
      SPEC.md            # 人類可讀領域邏輯（來自 va）
      prompts/  rubrics/
  workflows/
    <workflow_id>.dna.json
  tools/adapters.md
  evals/ golden/ regression/ adversarial/
  knowledge/seeds/
  policies/risk-overrides.md
  ui/routes.md
```

**`manifest.json` 最小欄位** 用途：宣告 `domain_id`、版本、顯示名、預設風險、`requires_alc: true`、代理人與工作流清單、知識種子萬用字元、工具命名空間 `video.`。

**註冊掛鉤：** `POST /api/v1/domains/register` 或 CLI；DNA 驗證器 + ALC 閘門；工具 allow-list；評估包自動發現；可選 FE `/app/domains/video/*`。

### 3.2 代理人學習合約（ALC）——所有代理人強制

**要修的問題：** generic 目前在 **run** 層級反思，成長未綁定到**每個代理人**。

| 能力 | 必要行為 | 儲存／API |
|------|----------|-----------|
| 情節寫入 | 步驟完成後寫 `agent_id`、`run_id`、`step_id`、結果、批判 | memory scope `agent` 或 `agent_episodes` |
| 反思 | run 後抽取**標記 agent_id** 的 lessons | 延伸 `reflect_on_agent` |
| 行動前檢索 | 步驟預檢載入 top-k 代理人 lessons + 記憶 | Runtime 步驟護欄 |
| 提案 skill／DNA 微調 | 重複失敗 → **`sandbox_only`** 代理人基因體提案 | improvement + evolution |
| 來源追溯 | source_refs、captured_by、recorded_at | 既有 provenance |
| 指標 | knowledge_growth、lesson_reuse、human_gate_rate_delta | metrics 端點 |

**啟用規則（v2.3）：** 當 domain `requires_alc` 為真且代理人要變 **`active`**（或 DNA **`production_ready`**）時，若缺 ALC 版本、缺 `agent` memory scope、缺 reflect 掛鉤 → **拒絕**。draft／registered 匯入不應被擋，但仍須預填 ALC 欄位。影片包全部代理人 `requires_alc: true`（N1）。

### 3.3 代理人基因體 vs 工作流 DNA

| 概念 | 內容 | 演化 |
|------|------|------|
| Workflow DNA | 步驟圖、工具、閘門、適應度 | 既有沙箱（保留） |
| Agent genome | 提示、評分規準、工具偏好、檢索政策、批判權重 | 新增 `sandbox_only` 變體；晉升新版本 |

共同演化 = 基因體族群 + 共享 golden 上的 workflow DNA。

### 3.4 編排模式（依 DNA 可設定）

階層主管+專精、管線+品質閘、Router 交接、平行 fan-out+join+QC、批判以評估步驟表達。**先映射 generic 步驟機**；僅 DNA 表達不了才引入外部圖引擎。

### 3.5 va 業務邏輯放哪裡（N1）

| 資產 | 權威位置 | va 角色 |
|------|----------|---------|
| 影片代理人規格 | `business/video/agents/**` | 上游撰寫／研究／腳本 |
| 影片工作流 | `business/video/workflows/**` | 同上 |
| 工具 adapters | generic backend + pack `tools/` | 僅規格 |
| 旁白腳本 | va 或 `business/video/content/` | 內容可留 va |
| 控制平面 | 僅 generic | **禁止重做** |

**重整 va 薄弱核心：** 停止把 va 當第二平台（FastAPI+LangGraph+Temporal 複製品）；重建為 generic 上的**完整**領域包；`system_build_plan.md` 里程碑**重定向**到 Domain Pack + ALC + generic APIs。

### 3.6 為數十個 MMA 模組化（N2）

Domain Pack SDK、穩定 `/api/v1/*`、擴充 schemas、`organization_id`+`domain_id` 隔離、包內 env 密鑰、FE `/app/domains/{id}`、每包測試標記、包 semver 獨立於平台。

---

## 4. Generic 學習規格（平台工作）

適用每一個未來 MMA 包。

### 4.1 Schema 新增

- `agent-spec.schema.json`（含 alc、scopes、tools、domain_id、risk、provenance）
- `domain-manifest.schema.json`
- `learning-log.schema.json`（**必含 agent_id**）

### 4.2 Runtime 變更

| 變更 | 行為 |
|------|------|
| 代理人範圍 lessons | 依 `step.agent_id` 拆分；lesson 上記 agent_id |
| `POST .../reflect/agent/{agent_id}` | 僅代理人反思 |
| 步驟前記憶注入 | LLM／工具前檢索 |
| ALC 驗證 | 無 ALC 阻擋啟用／production_ready |
| 代理人基因體提案 | `agent_genome` + `sandbox_only` |
| 指標 | `GET .../metrics?agent_id=` |
| 領域註冊 | 新 routes + CLI |
| 自動反思 | 延伸寫入代理人 lessons |

### 4.3 代理人學習適應度

品質／安全／合規／lesson 重用／知識成長加權，減人類升級與風險；提案仍受沙箱閘門。

### 4.4 仍屬非目標

DGM 式 host 自我改寫；無人值守生產晉升；LightRAG／Neo4j 作 MVP 硬依賴；常駐多 worker Temporal（後期可選）。

---

## 5. 影片領域重整（va → generic 上的包）

### 5.0 完整採用範圍（N3）——名冊與流程（掃描核實）

**代理人（完整目錄——必須全部留在專案）**

| 類 | 範圍 | 數 | 錨點名稱（掃描核實） | 匯入規則 |
|----|------|----|----------------------|----------|
| 1 台上主創 | 1–5 | 5 | Director → Casting | 全部匯入；保留 |
| 2 攝影燈光 | 6–8 | 3 | DoP、CameraOperator、DronePilot | 全部匯入；保留 |
| 3 剪輯調色 | 9–18 | 10 | Editor → MUA | 全部匯入；保留 |
| 4 聲音音樂 | 19–22 | 4 | SoundDesign → SoundMixer | 全部匯入；保留 |
| 5 表演編舞 | 23–27 | 5 | Choreography → UGCCreator | 全部匯入；保留 |
| 6 發行行銷 | 28–31 | 4 | SocialMediaStrategist → PerformanceMarketer | 全部匯入；保留 |
| 7 教育領域 | 32–45 | 14 | InstructionalDesign → RealEstatePhoto | 全部匯入；保留 |
| 8 AI 時代專精 | 46–52 | 7 | PromptEngineer → SportsAnalyst | 全部匯入；保留 |
| 9 專精**元代理人** | 53–80 | 28 | **Orchestrator、Planner、Router、Judge**、GateKeeper、Memory、各優化器、SafetyRedTeam… | 全部匯入；保留——**編排脊柱** |
| 10 工作流支援 | 81–114 | 34 | Analyst → ArchiveMaster | 全部匯入；保留 |
| **合計** | **1–114** | **114** | 完整列表 + pack id：**附錄 A** | **N3 強制** |

權威來源：`study/agents.md` §1–10、`SYSTEM_REFERENCE.md` §3。va 日後新增代理人則 MAP 與目錄成長；**禁止為縮範圍丟棄代理人**。

**額外深度規格系統（以包模組／共享服務採用，不得丟棄）：** Research、Process Optimization、GCA/SSOR、Agentic RAG、DIA、Coding（僅 sandbox）、LLM usage、Podcast、Aesthetics、Strategic goal／編劇 SGA、心理側寫／推薦、複雜問題模型、agent_loop 設計、planner v2.x、common agent structure——對應 `study/` 規格檔，映射到 pack 服務或相關代理人。

**業務流程（完整——編排器到葉節點）**

| 流程族 | 來源 | Generic 目標 |
|--------|------|--------------|
| **六階段 E2E 製作** | SYSTEM_REFERENCE §6.1 | `wf_video_production_e2e_v1`（+ 子階段 DNA） |
| 階段 1 意圖與規劃 | DIA → Planner → Producer | 脊柱 DNA |
| 階段 2 創意 | Director + Screenwriter + GCA | DNA + GCA 服務 |
| 階段 3 前期 | Casting、美術、概念、服裝、Research | DNA + research adapters |
| 階段 4 拍攝／生成 | PromptEngineer、DoP、Talent、聲音、Composer、VO | DNA + **媒體 stubs** |
| 階段 5 後期 | Editor、Colorist、VFX、Animator、Mixer、AIQAConsistency | DNA + QC stubs |
| 階段 6 交付與優化 | Social、PerformanceMarketer、Trailer、Personalization、Optimization | DNA + 打包 stubs |
| **原型 A–J** | `A-viral-hook.svg` … `J-feature-film.svg` | `wf_video_arch_a` … `j` |
| **LQR** | lqr-pipeline-overview 等六圖 | `wf_video_lqr_*` |
| 人 vs AI 工作流圖 | human／ai_agent_video_production_workflow | 流程索引 + 覆蓋矩陣 |
| 批判／QC／交付 | agents.md + SYSTEM_REFERENCE 層 | 評估步驟 + 審批 |
| 代理人管理／UI | `study/ui/*` | generic FE 領域路由 |
| 系統建置里程碑 | system_build_plan M0–M12 | 重定向到 Domain Pack + ALC |

**層級規則：** 可執行流程 DNA **必須**自 **Orchestrator（#53）與／或 Planner（#54）** 進入（需要時 Router #55／Judge #56）。每一位名冊代理人必須出現在 ≥1 個 DNA 步驟**或** orchestrator 的 `standby_pool` 路由（孤兒代理人檢查 = 0）。

### 5.1 Runtime 啟用波次（先完整目錄，再脊柱）

`system_build_plan` **G2** 與原型 **A（viral hook）** 只用來**啟用並證明脊柱**，**不**限制名冊保留範圍。

**脊柱管線（第一條 E2E）：**

```text
video.orchestrator / video.planner
  → intent (DIA) → video.producer 閘門
  → video.director + video.screenwriter (+ GCA 服務)
  → research / aesthetics（深度規格模組）
  → media_gen_stub → video.aiqaconsistency / QC stub
  → human_gate（需要時）→ package_metadata
```

Viral-hook DNA：`wf_video_arch_a_viral_hook_v1`（自 `A-viral-hook.svg`）。

| 波次 | 範圍 | Runtime 目標 |
|------|------|--------------|
| **0 — 目錄（L0）** | **全部 114** 目錄 + MAP + **最小** agent_spec（附錄 A）；深度 SPEC 非此波必做 | `draft`／`registered`；ALC **欄位**齊 |
| **1 — 脊柱作用中（L2）** | `video.orchestrator`、planner、router、judge、producer、intent/DIA、director、screenwriter、research | `active` + ALC 硬閘；viral-hook E2E |
| **2 — QC + 創意服務** | aiqaconsistency、aesthetics、optimization、GateKeeper、Memory | 脊柱上 active |
| **3 — 製作工藝** | 類 2–5 + PromptEngineer、Avatar、VoiceClone、Talent | 生成／後期 DNA（可 stub） |
| **4 — 領域與 GTM** | 類 6–8 其餘 + 教育專精 | 依 DNA 族 active |
| **5 — 完整元＋支援** | 其餘 #57–80、#81–114 + standby_pool | 全部編排器可達 |
| **6 — 流程完成** | A–J + LQR + 六階段 E2E + UI 流程 | 盤點 + 流程索引 100% |

媒體工具（Sora／Veo／Kling／ElevenLabs…）→ generic **adapter + CI stubs** 先（`adapters.py` 模式）；註冊於 `video.*` + `tool-permission-register.json`。

### 5.2–5.4 映射、知識播種、前端

va 概念映射 generic：DAG→DNA 步驟；self-refine→步驟迴圈+ALC；共享產物→run 輸出；人機閘→Approval API；批判匯流排→評估步驟；Temporal 願景→worker／佇列可選後期。

知識：策展規格與 68 章參考 → `business/video/knowledge/seeds/` 帶 provenance；Tier-0 索引；`acting_agent_id` 檢索。

前端：A 重用 ops console；B `/app/domains/video`（管線／資產）；C 進階時間軸可選；須能列出**完整名冊**（篩選 active／draft）。

---

## 6. 分階段遷移路線圖

**原則：** generic 為基底；va 重建為**完整**領域包 + ALC（完整名冊 + 完整流程），非平行棧，亦非永久代理人子集。

| 階段 | 焦點 | 示意工期 | 離開條件摘要 |
|------|------|----------|--------------|
| **0** | L0 目錄 + ADR | 1–2 週 | ROSTER／MAP／114 目錄（最小 spec）；PROCESSES **索引**；基線綠 |
| **1** | Domain Pack SDK + ALC | 2–3 週 | 註冊；agent_id lessons；ALC 在 **active** 硬閘；E1 綠 |
| **2** | 全目錄 L0 + **脊柱 L2** E2E | 3–5 週 | 114 皆 L0；流程已索引；viral-hook **可跑**；非「全部 DNA 已深」 |
| **3** | 脊柱上學習 + 共同演化 | 2–3 週 | ≥1 適應度改善；稽核完整 |
| **4** | 多包證明 + 安全 + 負載 | 2–3 週 | **脊柱之後**第二包；隔離；手冊 |
| **5** | 推向 N3 完成（全員 ≥L1，更多 L2） | 8–16+ 週 | 無孤兒；流程 DNA 綁定；保留 CI；N3 DoD |

**階段 0：** 匯出名冊 1–114；流程**索引**；114 佔位 + **最小** agent_spec（L0）；MAP；ADR（權威在 generic 包；ops 與 `video.*` 命名空間分離）。

**階段 2：** 全員 L0；脊柱代理人較完整 SPEC；**一條**可跑 viral-hook DNA（L2）；其他流程族可輕量 stub／索引；工具 stubs；E2E；FE 列 114。深度 SPEC／B–J／LQR 深度放階段 5。

**階段 5 為 N3 強制完成，非可選**（全員 ≥ L1、脊柱 ≥ L2，非 114 全 L2）。

示意：Demo（L0 目錄 + 脊柱 L2）6–9 週；至階段 4 約 10–16 週；**N3 完成另加 8–16+ 週**。

---

## 7. 測試策略

### 7.1 單元

ALC 閘門；lessons 含 agent_id／provenance；跨代理人隔離；非 sandbox 突變阻擋；無效 manifest 失敗封閉。

### 7.2 整合

影片 DNA 生命週期；auto-reflect 雙 lessons；tool_effects；包隔離；Improve+evolution 仍綠。

### 7.3 領域評估

va 評分規準 → `business/video/evals/`；不可逆工具人類閘門回歸；提示注入不得擴大 allow-list。

### 7.4 負載

約 20 並行混合領域 runs；並行 reflect 不丟 lesson；archive p95；5 路 SSE 下主控台可回應。GPU 媒體生成負載不在 CI。

### 7.5 完成定義（DoD）

**平台：** ALC 強制；脊柱 E2E；第二包無 runtime 分叉；sandbox_only；單元+e2e+business:eval 綠；status／handoff 更新。

**完整 va 採用（N3）——對齊 L0／L1／L2：**

- [ ] `business/video/agents/` + MAP 數 == 114（全員 ≥ L0）  
- [ ] 10 類齊；元代理人含 `video.orchestrator`／`planner`／`router`／`judge`（非 ops 種子）  
- [ ] 全部 va 業務流程已在 PROCESSES 索引，並有 DNA／連結（≥ L1 覆蓋）  
- [ ] 每位代理人編排器可達（DNA 步驟或 standby_pool）  
- [ ] 保留政策 CI（刪除名冊代理人則失敗）  
- [ ] 脊柱 ≥ L2；啟用波次已文件；未啟用者 draft／registered 仍在專案  
- [ ] **不**要求 114 位全部 L2 才算 N3 完成

---

## 8. 風險緩解

| 風險 | 可能 | 影響 | 緩解 |
|------|------|------|------|
| 雙平台重寫 | 中 | 高 | ADR 禁止；僅 pack 路徑 |
| 遺失 va 保真度 | 中 | 高 | 種子 provenance；MAP；保留 va |
| 範圍爆炸／N3 未完成 | 高 | 高 | **Wave 0 先完整匯入**；分波啟用；禁丟棄；階段 5 強制 |
| 孤兒代理人 | 中 | 高 | standby_pool + 孤兒 CI |
| 學習污染共享記憶 | 中 | 高 | 代理人 scopes + 隔離測試 |
| 演化倒退 | 中 | 高 | 適應度 + 人類閘 + 回滾；禁 auto_promote |
| 媒體 API 成本 | 高 | 中 | CI stubs；預算閘；allow-list |
| 破壞 mark-100／E1 | 中 | 高 | 每 PR 回歸 |
| 文件語言分歧 | 中 | 低 | 包內 EN 規格為準；HK 腳本留 va |

**衝突政策：** 平台安全／治理 > 領域便利；領域創意僅在 pack 檔內 > 平台預設；va 版本衝突偏好 SYSTEM_REFERENCE + 最新 agent_loop／planner。

---

## 9. 長期維運與重用

版本：平台 semver；包獨立 semver + `engine_range`；代理人基因體 `agent_id@version` 晉升後不可變。

貢獻：va 規格與／或 generic `business/video` PR；平台 PR 需 E1+單元+演化測試；包 PR 需 schema+evals+ALC；tier≥4 工具人類審。

文件：`adoption.md`／`adoption_hk.md`、`docs/domain-packs.md`、`business/video/README.md`、structure／backend／frontend 於 ALC／pack 落地時更新；va SYSTEM_REFERENCE 加「已在 generic pack 路徑實作」橫幅。

新 MMA 重用：複製 example_domain → 填 manifest／代理人／DNA／golden → 註冊 → ALC 啟用 → E2E。**影片 N3 完成前**，其他領域不得犧牲影片完整採用。

擁有權：Runtime／ALC／SDK → generic 核心；影片創意規格 → va／影片包；共享 schemas → generic RFC；工具廠商 → 包擁有者 + 平台審。

---

## 10. 實作清單（首 30 日）

**第 1 週**

- [ ] 批准 adoption **v2.3**（N3 + L0／L1／L2 rethink）  
- [ ] ADR：雙倉庫 + pack-on-generic + **全部 va 代理人專案內保留** + ops／video 命名空間分離  
- [ ] 骨架 `business/video/` + `business/example_domain/`  
- [ ] 匯出完整名冊 + 流程**索引**；建立**全部代理人 L0 佔位**（最小 agent_spec，非深 SPEC）  
- [ ] 起草 agent-spec／domain-manifest schemas  

**第 2–3 週**

- [ ] 代理人範圍 lessons + reflect API（`agent_id`）  
- [ ] ALC **active** 硬閘（draft 可匯入）  
- [ ] Domain register dry-run（example + video）  
- [ ] MAP.md 對**整份** 114 名冊一對一  

**第 4 週**

- [ ] 脊柱代理人（較完整 SPEC）+ viral-hook DNA（`video.orchestrator` 向下）  
- [ ] Stub 工具 + golden eval  
- [ ] 目錄完整閘門（L0 數 == 114）  
- [ ] E2E 脊柱 L2 demo + status／handoff 更新

---

## 11. 可追溯性：`review_adoption.md` → 本文件

| 審閱要求 | 位置 |
|----------|------|
| 兩倉庫完整稽核 | §2 |
| 分階段路線圖 | §6 |
| 對所有 MMA 強制的 generic 學習 | §3.2、§4 |
| 強化 va 薄弱核心、保留影片邏輯 | §3.5、§5 |
| 模組化／APIs／schemas／掛鉤 | §3.1、§3.6 |
| 測試策略 | §7 |
| 維運、版本、貢獻、文件 | §9 |
| 風險緩解 | §8 |
| N1／N2 | §0 |
| **N3 全部代理人 + 全部流程 + 保留** | **§0、§0.1、§1.3、§5.0–5.1、§6 階段 0／2／5、§7.5、附錄 A／B** |
| **v2.3 Rethink（L0／L1／L2、執行順序）** | **文首「重新思考」、§0.1 分階段表、§1.3、§6、§7.5、§10** |

---

## 12. 參考資料（本機）——掃描錨點

**generic-swarm-ops：** `status.md`、`mark_100_verification.md`、structure／backend／frontend、`docs/self-improvement-and-orchestration.md`、`docs/evolution-sandbox.md`、`docs/workflow-dna.md`、`backend/app/runtime.py`、improvement／evolution／workflow_runs 路由、`self_improvement/*`、`tools/adapters.py`、`corpus_eval.py`、workflow-dna schema、golden-tasks、tool-permission-register、FE domain 元件、gap analyses、E1 checklist／e2e、`adoption_plan.md`。

**va-agent-swarm：** `study/agents.md`（**權威 114 名冊**）、`SYSTEM_REFERENCE.md`、ai／human video production workflow、system_build_plan、workflows A–J 與 lqr-*、各 `*_agent_*specification*`、agent_loop*、`plan/planner_agent_v2.*`、`study/ui/*`、reference 68 章、project_starter（歸檔，勿分叉第二棧）。

---

## 13. 變更紀錄

| 版本 | 日期 | 說明 |
|------|------|------|
| 1.0 | 2026-07-09 | 初始合併願景與路線圖 |
| 2.0 | 2026-07-10 | review_adoption 執行；N1／N2 Domain Pack + ALC |
| 2.1 | 2026-07-10 | **N3** 完整名冊 + 完整流程 + 專案內保留 |
| 2.2 | 2026-07-10 | 深度雙倉掃描；114 附錄；流程圖；generic 缺口矩陣 |
| **2.3** | **2026-07-10** | **重新思考：** L0／L1／L2 成熟度；目錄 ≠ 完整 SPEC；ALC 硬閘僅 active；先流程索引後 DNA 深度；ops vs `video.orchestrator`；N3 完成 vs 生產級誠實表述；本 HK 與英文 v2.3 對齊 |

---

## 附錄 A — 完整 va 代理人名冊（N3 匯入清單）

**來源：** `va-agent-swarm/study/agents.md`（每個 id 首次出現的 Agent 名稱列）。  
**規則：** 為**每一列**建立 `business/video/agents/<pack_id>/`；永不刪除。  
（代理人英文名與 pack id 與英文 `adoption.md` Appendix A 一致，便於 CI／MAP 對照。）

| # | va Agent | Cat | Pack id（權威） |
|---|----------|-----|-----------------|
| 1 | DirectorAgent | 1-ATL | `video.director` |
| 2 | ProducerAgent / EP | 1-ATL | `video.producer` |
| 3 | ScreenwriterAgent | 1-ATL | `video.screenwriter` |
| 4 | ShowrunnerAgent | 1-ATL | `video.showrunner` |
| 5 | CastingAgent | 1-ATL | `video.casting` |
| 6 | CinematographerAgent (DoP) | 2-Cam | `video.cinematographer` |
| 7 | CameraOperatorAgent | 2-Cam | `video.cameraoperator` |
| 8 | DronePilotAgent | 2-Cam | `video.dronepilot` |
| 9 | EditorAgent | 3-Edit | `video.editor` |
| 10 | ColoristAgent | 3-Edit | `video.colorist` |
| 11 | VFXSupervisorAgent | 3-Edit | `video.vfxsupervisor` |
| 12 | AnimatorAgent (2D/3D) | 3-Edit | `video.animator_2d` |
| 13 | MotionGraphicsAgent | 3-Edit | `video.motiongraphics` |
| 14 | StoryboardAgent | 3-Edit | `video.storyboard` |
| 15 | ConceptArtistAgent | 3-Edit | `video.conceptartist` |
| 16 | ProductionDesignAgent | 3-Edit | `video.productiondesign` |
| 17 | CostumeDesignAgent | 3-Edit | `video.costumedesign` |
| 18 | MUAAgent (Makeup/Hair/SFX) | 3-Edit | `video.mua_makeup` |
| 19 | SoundDesignAgent | 4-Snd | `video.sounddesign` |
| 20 | ComposerAgent | 4-Snd | `video.composer` |
| 21 | VoiceOverAgent | 4-Snd | `video.voiceover` |
| 22 | SoundMixerAgent (Re-recording) | 4-Snd | `video.soundmixer` |
| 23 | ChoreographyAgent | 5-Perf | `video.choreography` |
| 24 | MusicVideoDirectorAgent | 5-Perf | `video.musicvideodirector` |
| 25 | ComedyWriterAgent | 5-Perf | `video.comedywriter` |
| 26 | TalentAgent (On-camera) | 5-Perf | `video.talent` |
| 27 | UGCCreatorAgent | 5-Perf | `video.ugccreator` |
| 28 | SocialMediaStrategistAgent | 6-Dist | `video.socialmediastrategist` |
| 29 | CopywriterAgent | 6-Dist | `video.copywriter` |
| 30 | CreativeDirectorAgent | 6-Dist | `video.creativedirector` |
| 31 | PerformanceMarketerAgent | 6-Dist | `video.performancemarketer` |
| 32 | InstructionalDesignAgent | 7-Edu | `video.instructionaldesign` |
| 33 | SMEAgent (Subject-Matter Expert) | 7-Edu | `video.sme` |
| 34 | FactCheckerAgent | 7-Edu | `video.factchecker` |
| 35 | MedicalIllustratorAgent | 7-Edu | `video.medicalillustrator` |
| 36 | JournalistAgent | 7-Edu | `video.journalist` |
| 37 | ComplianceAgent (Legal) | 7-Edu | `video.compliance` |
| 38 | FinanceAgent | 7-Edu | `video.finance` |
| 39 | FoodStylistAgent | 7-Edu | `video.foodstylist` |
| 40 | TravelCineAgent | 7-Edu | `video.travelcine` |
| 41 | ChildrensAuthorAgent | 7-Edu | `video.childrensauthor` |
| 42 | AudiobookNarratorAgent | 7-Edu | `video.audiobooknarrator` |
| 43 | SignLanguageInterpreterAgent | 7-Edu | `video.signlanguageinterpreter` |
| 44 | LocalizationQAAgent (Linguist) | 7-Edu | `video.localizationqa` |
| 45 | RealEstatePhotoAgent / 3D Scan | 7-Edu | `video.realestatephoto` |
| 46 | PromptEngineerAgent / GeneratorOperator | 8-AI | `video.promptengineer` |
| 47 | AvatarDesignAgent | 8-AI | `video.avatardesign` |
| 48 | VoiceCloneAgent / LipSyncSpecialist | 8-AI | `video.voiceclone` |
| 49 | AIQAConsistencyAgent | 8-AI | `video.aiqaconsistency` |
| 50 | PersonalizationEngineerAgent | 8-AI | `video.personalizationengineer` |
| 51 | TrailerEditorAgent | 8-AI | `video.trailereditor` |
| 52 | SportsAnalystAgent / TelestratorOp | 8-AI | `video.sportsanalyst` |
| 53 | OrchestratorAgent | 9-Meta | `video.orchestrator` |
| 54 | PlannerAgent | 9-Meta | `video.planner` |
| 55 | RouterAgent | 9-Meta | `video.router` |
| 56 | JudgeAgent | 9-Meta | `video.judge` |
| 57 | GateKeeperAgent | 9-Meta | `video.gatekeeper` |
| 58 | MemoryAgent | 9-Meta | `video.memory` |
| 59 | IdeationAgent | 9-Meta | `video.ideation` |
| 60 | NarrativeArcAgent | 9-Meta | `video.narrativearc` |
| 61 | StyleTransferAgent | 9-Meta | `video.styletransfer` |
| 62 | WorldBuildingAgent | 9-Meta | `video.worldbuilding` |
| 63 | MoodBoardAgent | 9-Meta | `video.moodboard` |
| 64 | NoveltyAgent / Anti-Cliché Critic | 9-Meta | `video.novelty` |
| 65 | EmotionalArcAgent | 9-Meta | `video.emotionalarc` |
| 66 | WebResearchAgent | 9-Meta | `video.webresearch` |
| 67 | ArchiveResearchAgent | 9-Meta | `video.archiveresearch` |
| 68 | TrendIntelligenceAgent | 9-Meta | `video.trendintelligence` |
| 69 | CompetitorIntelligenceAgent | 9-Meta | `video.competitorintelligence` |
| 70 | CitationAgent | 9-Meta | `video.citation` |
| 71 | InterviewSynthesisAgent | 9-Meta | `video.interviewsynthesis` |
| 72 | BenchmarkResearchAgent | 9-Meta | `video.benchmarkresearch` |
| 73 | PromptOptimizerAgent | 9-Meta | `video.promptoptimizer` |
| 74 | CostOptimizerAgent | 9-Meta | `video.costoptimizer` |
| 75 | LatencyOptimizerAgent | 9-Meta | `video.latencyoptimizer` |
| 76 | RetentionOptimizerAgent | 9-Meta | `video.retentionoptimizer` |
| 77 | ROASOptimizerAgent | 9-Meta | `video.roasoptimizer` |
| 78 | AccessibilityOptimizerAgent | 9-Meta | `video.accessibilityoptimizer` |
| 79 | EvaluationHarnessAgent | 9-Meta | `video.evaluationharness` |
| 80 | SafetyRedTeamAgent | 9-Meta | `video.safetyredteam` |
| 81 | AnalystAgent | 10-Sup | `video.analyst` |
| 82 | AudienceSimAgent | 10-Sup | `video.audiencesim` |
| 83 | AccessibilityAgent | 10-Sup | `video.accessibility` |
| 84 | BrandAgent | 10-Sup | `video.brand` |
| 85 | BrandStrategistAgent | 10-Sup | `video.brandstrategist` |
| 86 | MarketingAgent | 10-Sup | `video.marketing` |
| 87 | SEOAgent | 10-Sup | `video.seo` |
| 88 | CommunityAgent | 10-Sup | `video.community` |
| 89 | TemplateDesignAgent | 10-Sup | `video.templatedesign` |
| 90 | UXAgent | 10-Sup | `video.ux` |
| 91 | TrustSafetyAgent | 10-Sup | `video.trustsafety` |
| 92 | CRMAgent | 10-Sup | `video.crm` |
| 93 | LegalAgent | 10-Sup | `video.legal` |
| 94 | FestivalStrategistAgent | 10-Sup | `video.festivalstrategist` |
| 95 | CriticAgent | 10-Sup | `video.critic` |
| 96 | LMSAgent | 10-Sup | `video.lms` |
| 97 | LearnerSimAgent | 10-Sup | `video.learnersim` |
| 98 | ContinuityAgent | 10-Sup | `video.continuity` |
| 99 | LipSyncAgent | 10-Sup | `video.lipsync` |
| 100 | MusicSupervisorAgent | 10-Sup | `video.musicsupervisor` |
| 101 | LabelA&RAgent | 10-Sup | `video.labela_r` |
| 102 | LabelDigitalAgent | 10-Sup | `video.labeldigital` |
| 103 | DeepfakeDetectionAgent | 10-Sup | `video.deepfakedetection` |
| 104 | CommsAgent | 10-Sup | `video.comms` |
| 105 | ArchiveProducerAgent | 10-Sup | `video.archiveproducer` |
| 106 | StandardsEditorAgent | 10-Sup | `video.standardseditor` |
| 107 | EthicsAgent | 10-Sup | `video.ethics` |
| 108 | ChannelManagerAgent | 10-Sup | `video.channelmanager` |
| 109 | CorrectionsAgent | 10-Sup | `video.corrections` |
| 110 | MPAAgent | 10-Sup | `video.mpa` |
| 111 | SalesAgent | 10-Sup | `video.sales` |
| 112 | DistributorAgent | 10-Sup | `video.distributor` |
| 113 | AwardsStrategistAgent | 10-Sup | `video.awardsstrategist` |
| 114 | ArchiveMasterAgent | 10-Sup | `video.archivemaster` |

**盤點 CI 合約：**  
`count(business/video/agents/*) == 114` 且附錄 A 每個 `pack_id` 存在且 MAP 列數 == 114。

---

## 附錄 B — Generic as-built vs N3 就緒度

| 能力 | As-built 路徑／事實 | N3 行動 |
|------|---------------------|---------|
| 主機 runtime | `backend/app/runtime.py` | 延伸；不要替換 |
| Workflow DNA | `business/schemas/workflow-dna.schema.json` | 撰寫全部影片 DNA |
| 演化沙箱 | `/api/v1/evolution/*` | 保持 sandbox_only；後期加代理人基因體 |
| Reflect／lessons | `/api/v1/improvement/*`、`lessons.py` | 加 `agent_id` + 每代理人檢索 |
| 工具 | `adapters.py`（6 個營運工具） | 加 `video.*` stubs + 登錄 |
| 種子代理人 | 5 個營運代理人 | 保留；**另加** 114 影片代理人 |
| Domain pack | **缺失** | 建立 `business/video/` + schemas + 註冊 API |
| FE | ops console domain 元件 | 列出完整名冊；篩選 draft／active |
| E1／mark 100 | 綠燈 | **每 PR 保護** |

---

*採用計劃 v2.3 完（繁體中文，對齊 `adoption.md`）*
