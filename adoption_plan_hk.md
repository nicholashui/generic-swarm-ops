# 採用行動計劃

**策略來源：** `adoption.md` v2.3 · `adoption_hk.md` v2.3 · `review_adoption.md`  
**計劃版本：** 3.2（重新思考）  
**日期：** 2026-07-10  
**倉庫：** generic-swarm-ops（主機）× va-agent-swarm（完整影片 Domain Pack）  
**不可妥協：** **N1** ALC · **N2** Domain Pack 主機 · **N3** **全部 114 代理人 + 全部流程 + 專案內保留**  
**策略對照：** `adoption.md` v2.3 rethink（L0／L1／L2 成熟度）  
**英文原文：** `adoption_plan.md`（本檔為繁體中文版）

---

## 0. 重新思考——執行原則（先讀）

### 0.1 先前計劃形態的問題

| 問題 | 為何有害 | 修正 |
|------|----------|------|
| **SPEC 劇場** | 第一次 E2E 前為 114 人寫深度 SPEC.md，耗週而無 runtime 證明 | **L0 目錄** = 資料夾 + 最小 agent_spec + MAP。深度 SPEC = **L2 啟用**工作 |
| **DNA 劇場** | 把 10 原型 + LQR + 六階段 stub 當「完成」卻沒有可跑 | **早期索引全部流程**；**一條可跑 DNA**（脊柱／viral-hook）先於深度 |
| **閘門混淆** | 每個 draft 佔位都強制 ALC → 擋匯入／註冊 | **僅 status→active 或 DNA production_ready 時硬閘**；draft 仍帶 ALC 欄位 |
| **里程碑混淆** | 階段 2「代理人都在」看起來像 N3 完成 | 三層 DoD：**Catalog**、**Spine**、**N3 complete** |
| **命名空間碰撞** | generic 已有 `business_orchestrator`（ops） | 影片元代理人只用 `video.*`（`video.orchestrator` 等）——永不覆寫 ops 種子 |
| **手冊膨脹** | 100+ 微步驟卻無每週成果 | §15 是參考；**§0.3 關鍵路徑**才是每週執行 |
| **N2 vs N3 順序** | 第二領域在脊柱前做會分心 | **example_domain** 只證明 register API；然後 **video 脊柱**，再其他領域 |

### 0.2 成熟度模型（更新 Status 時使用）

| 層級 | 名稱 | 最低門檻 | 計入 |
|------|------|----------|------|
| **L0** | Catalog（目錄） | 資料夾 + ROSTER／MAP + draft `agent_spec.json`（含 ALC 欄位） | N3 存在 |
| **L1** | Indexed（已索引） | 出現在 PROCESSES.md 與／或 DNA stub 與／或 `standby_pool` | N3 可觸達 |
| **L2** | Runtime（執行期） | `active` 或被呼叫；過 ALC 閘；掛可跑 DNA；工具可 stub | Demo／生產路徑 |

**N3 完成** = 全部 114 ≥ **L1**、盤點 CI 綠、流程已索引、保留 CI 開、脊柱 ≥ **L2**。  
**N3 完成不要求：** 114 全 L2、真 Sora／Veo、完整 FE 時間軸編輯器。

### 0.3 關鍵路徑（預設工作只做這個）

**按序執行。** 其餘平行或稍後。

| 順序 | 成果 | 父任務 ID | 時框 |
|------|------|-----------|------|
| **1** | ADR + 批准 | P0-01, P0-02 | 1 日 |
| **2** | L0 目錄：ROSTER、114 目錄、MAP、PROCESSES 索引、盤點腳本 | P0-03…P0-07, N3-CI-01（可提早） | 3–5 日 |
| **3** | 平台：schemas + domain register + example_domain dry-run | DP-01…DP-07 | 1 週 |
| **4** | 平台：agent_id lessons + ALC 在 **active** + E1 仍綠 | ALC-01…ALC-10, REG-01 | 1–2 週 |
| **5** | 脊柱 L2：8–12 代理人夠完整 + viral-hook DNA + stubs + e2e | VID-01…VID-10, FE-01 列表 | 2–3 週 |
| **6** | 流程深度：其餘 DNA 族 + 波次 W2–W5 + 孤兒／保留 CI | N3-P-*, W*, DOD-02 | 持續 |
| **7** | 其他領域 | DP-09／DP-10 | **脊柱 L2 之後**（N2）；完整 N3 可稍後 |

### 0.4 「詳細步驟」現在怎麼用

- **§5** = 待辦（父任務）。  
- **§15** = 卡住或新人上手時的詳細程序。  
- **§0.3** = 團隊本週真正做的事。  
- **不要**要求出脊柱 demo 前跑完每一個 §15 微步驟——關鍵路徑父任務的 **Verify** 閘門必須過。

---

## 1. 如何使用本清單

| 欄位 | 含義 |
|------|------|
| **ID** | 穩定任務 id（`P0-01`、`N3-A-03`、`ALC-02`…） |
| **Step** | 父任務下微步驟 id（`P0-03.s1`、`ALC-02.s3`…）——見 **§15 詳細手冊** |
| **Phase** | 0–5（見 `adoption.md`／`adoption_hk.md` §6） |
| **Workstream** | `GOV` · `N3` · `DP` · `ALC` · `EV` · `VID` · `FE` · `T` · `REG` · `DOC` · `RISK` |
| **Priority** | **P0** 關鍵路徑 · **P1** 階段離開 · **P2** 重要 · **P3** 稍後 |
| **Owner** | `platform` · `video-pack` · `va-specs` · `product` · `both` |
| **Status** | `todo` · `in_progress` · `blocked` · `done` · `leverage`（已存在） |
| **Depends on** | 前置 ID |
| **Acceptance** | 離開準則 |
| **Primary paths** | 要動的檔案／API |

**名冊真相源：** `adoption.md` **Appendix A**（114 個 pack id `video.*`）。  
**CI 合約（N3）：** `count(business/video/agents/*) == 114` 且 MAP 列數 == 114 且無孤兒代理人。

**執行順序：** §5 高層表 → 對關鍵路徑父 ID 打開 **§15** 完成必要 `.sN` → 再標父任務 `done`。

---

## 2. 不可妥協檢查清單（必須一直為真）

| ID | 規則 | Status |
|----|------|--------|
| N3-RULE-01 | 匯入 **全部** va 代理人 1–114；永不丟棄 meta（#53–80）或 support（#81–114） | todo |
| N3-RULE-02 | 匯入 **全部** va 業務流程（六階段 + A–J + LQR + UI 流程文件） | todo |
| N3-RULE-03 | 編排器向下：DNA 由 `video.orchestrator`／`video.planner` 入場 | todo |
| N3-RULE-04 | 每位代理人 ≥1 DNA 步驟 **或** `standby_pool` | todo |
| N3-RULE-05 | 代理人即使未 active 也以 draft／registered 留在 git | todo |
| N3-RULE-06 | 缺代理人資料夾則盤點 CI 失敗 | todo |
| N1-RULE-01 | ALC **硬要求**於 status=`active`／DNA production_ready；draft 帶 ALC 欄位 | todo |
| N2-RULE-01 | 第二包證明主機無 runtime 分叉（**脊柱 L2 之後**） | todo |
| RETHINK-01 | ops 種子（`business_orchestrator` 等）永不被影片元代理人取代 | todo |
| RETHINK-02 | 每週工作跟 §0.3 關鍵路徑，非窮盡 §15 | todo |

---

## 3. 階段總覽

| Phase | 焦點 | 工期 | 離開摘要 |
|-------|------|------|----------|
| **0** | L0 目錄 + ADR | 1–2 週 | ROSTER／MAP／114 目錄（最小 specs）；PROCESSES **索引**；基線綠 |
| **1** | Domain Pack SDK + ALC runtime | 2–3 週 | 註冊；agent_id lessons；ALC 在 **active**；E1 綠 |
| **2** | 目錄 L0 完成 + **脊柱 L2** E2E | 3–5 週 | 114 皆 L0；流程 **索引**；viral-hook **可跑**；非「全部 DNA 已深」 |
| **3** | 脊柱上學習 + 共同演化 | 2–3 週 | 影片 goldens 上 ≥1 適應度改善 |
| **4** | 多包證明 + 安全 + 負載 | 2–3 週 | **脊柱後**第二包；隔離；手冊 |
| **5** | 推向 N3 完成（全員 L1，更多 L2） | 8–16+ 週 | 孤兒=0；流程 DNA 綁定；保留 CI；N3 DoD |

| 捆綁 | 目標 | 含義 |
|------|------|------|
| **Demo**（0–2 關鍵路徑） | 6–9 週 | 目錄 L0 + 脊柱 L2 |
| **平台硬化**（至 4） | 10–16 週 | N2 + 安全 |
| **N3 完成**（至 5） | +8–16 週 | 全員 ≥ L1；脊柱穩 L2；流程索引且綁定 |

---

## 4. 已出貨（leverage——不要重建）

| ID | 能力 | Status | Primary paths |
|----|------|--------|---------------|
| BASE-01 | FastAPI + Postgres 控制平面 | leverage | `backend/app/runtime.py` |
| BASE-02 | Workflow DNA 驗證／啟用 | leverage | `structure_validators.py`、workflows routes |
| BASE-03 | Run 生命週期 + SSE + pause／resume／expire | leverage | `workflow_runs` routes |
| BASE-04 | 本機 tool adapters + `tool_effects` | leverage | `infrastructure/tools/adapters.py` |
| BASE-05 | Run reflect + lesson 庫 + 磁碟 lessons | leverage | `improvement` routes、`self_improvement/*` |
| BASE-06 | Auto-reflect | leverage | `GENERIC_SWARM_AUTO_REFLECT` |
| BASE-07 | 演化沙箱（sandbox_only） | leverage | `evolution` routes、`corpus_eval.py` |
| BASE-08 | Skill sandbox | leverage | `/improvement/skills/*` |
| BASE-09 | FE Improve + Evolution UI | leverage | `improve-run-button.tsx`、`evolution-archive-panel.tsx` |
| BASE-10 | E1 + unit 綠 | leverage | `test_e1_operator_path.py`、`tests/unit/*` |
| BASE-11 | 20 個入職 goldens | leverage | `business/evals/golden-tasks/` |
| BASE-12 | 雙 harness + business:* scripts | leverage | `npm run sync`、`business:validate` |

---

## 5. 主行動表

### 5.1 階段 0 — 完整盤點與骨架

| ID | 任務 | Workstream | Priority | Owner | Status | Depends on | Primary paths | Acceptance |
|----|------|------------|----------|-------|--------|------------|---------------|------------|
| P0-01 | 批准 `adoption.md` v2.3 + 本計劃為執行合約 | GOV | P0 | product | todo | — | `status.md` | 書面批准 |
| P0-02 | ADR：雙倉庫 + pack-on-generic + **N3 保留全部 114 代理人** | GOV | P0 | product | todo | P0-01 | `docs/` 或 `business/governance/` | ADR 禁第二控制平面；禁丟代理人 |
| P0-03 | 自 va `agents.md` 匯出 `business/video/ROSTER.json`（114） | N3 | P0 | both | todo | P0-01 | `business/video/ROSTER.json` | Count == 114；ids 1–114 |
| P0-04 | 匯出 `business/video/PROCESSES.md`（六階段 + A–J + LQR + UI） | N3 | P0 | both | todo | P0-01 | `business/video/PROCESSES.md` | 編排器→葉節點覆蓋 |
| P0-05 | 建立 `business/video/` 骨架（manifest、agents、workflows、evals、knowledge、tools、ui） | DP | P0 | platform | todo | P0-02 | `business/video/**` | 樹存在 |
| P0-06 | 為 Appendix A **每個 pack id** 建佔位目錄 | N3 | P0 | platform | todo | P0-03, P0-05 | `business/video/agents/video.*/` | **114** 目錄 |
| P0-07 | 寫 `business/video/MAP.md` 一代理人一列（va id → pack_id → 來源路徑） | N3 | P0 | both | todo | P0-06 | `MAP.md` | 列數 == 114；無省略 |
| P0-08 | 建立 `business/example_domain/` 骨架（N2 種子） | DP | P0 | platform | todo | P0-02 | `business/example_domain/**` | 最小包樹 |
| P0-09 | 基線綠：unit + E1 + FE lint／typecheck／test | REG | P0 | platform | todo | — | `status.md` | 命令通過 |
| P0-10 | 盤點深度規格模組（research、GCA、aesthetics、DIA、RAG…）入 PROCESSES／MAP | N3 | P1 | va-specs | todo | P0-04 | PROCESSES.md | 模組已列 |
| P0-11 | 風險表 R-01…R-11 指定 Owner | RISK | P1 | product | todo | P0-01 | 本計劃 §8 | Owners 已填 |
| P0-12 | 同步政策：PR 從 va 複製完整名冊到 generic；穩定前不用 submodule | GOV | P1 | product | todo | P0-02 | ADR 附錄 | 決策已記錄 |

**階段 0 離開**

| 檢查 | Status |
|------|--------|
| ROSTER + MAP + 114 目錄 | todo |
| PROCESSES.md 完整（索引） | todo |
| ADR + N3 規則已批准 | todo |
| E1／unit 基線綠 | todo |

---

### 5.2 階段 1 — Domain Pack SDK + ALC

| ID | 任務 | Workstream | Priority | Owner | Status | Depends on | Primary paths | Acceptance |
|----|------|------------|----------|-------|--------|------------|---------------|------------|
| DP-01 | 新增 `business/schemas/domain-manifest.schema.json` | DP | P0 | platform | todo | P0-05 | `business/schemas/` | 正／負 fixtures |
| DP-02 | 新增 `business/schemas/agent-spec.schema.json`（alc、scopes、tools、domain_id） | DP | P0 | platform | todo | P0-07 | `agent-spec.schema.json` | requires_alc 時 ALC 欄位必填 |
| DP-03 | 新增 `business/schemas/learning-log.schema.json`，**必含 agent_id** | DP | P0 | platform | todo | DP-02 | `learning-log.schema.json` | agent_id required |
| DP-04 | Schema 單元測試 | T | P0 | platform | todo | DP-01..03 | tests／fixtures | 綠 |
| DP-05 | Domain register API 與／或 `npm run domain:register` | DP | P0 | platform | todo | DP-01 | `routes/domains.py`、`router.py` | Draft 載入成功 |
| DP-06 | 無效 manifest 失敗封閉 | T | P0 | platform | todo | DP-05 | domains service | 單元拒絕 |
| DP-07 | Dry-run 註冊 `example_domain` | DP | P0 | platform | todo | DP-05, P0-08 | example_domain | 成功 |
| DP-08 | Dry-run 註冊 `video` 包（draft 代理人） | DP | P0 | platform | todo | DP-05, P0-06 | business/video | 成功 |
| ALC-01 | 延伸 `Lesson` + 儲存含 `agent_id`（向後相容） | ALC | P0 | platform | todo | BASE-05 | `lessons.py`、runtime | 舊 lessons 仍可載 |
| ALC-02 | 依 `step.agent`／`agent_id` 拆分 reflect lessons | ALC | P0 | platform | todo | ALC-01 | `reflection.py`、`reflect_on_workflow_run` | 多代理人 → 多 agent_id |
| ALC-03 | `POST /api/v1/improvement/reflect/agent/{agent_id}` | ALC | P0 | platform | todo | ALC-02 | `routes/improvement.py` | 代理人過濾可用 |
| ALC-04 | `GET /lessons?agent_id=` | ALC | P0 | platform | todo | ALC-01 | improvement routes | Query 可用 |
| ALC-05 | 步驟完成後情節寫入（agent scope／agent_episodes） | ALC | P0 | platform | todo | ALC-01 | runtime step loop | Episode 欄位齊 |
| ALC-06 | 步驟前注入 top-k 代理人 lessons + agent memory | ALC | P0 | platform | todo | ALC-05 | step preflight | 單元：inject 被呼叫 |
| ALC-07 | 隔離：代理人 A 不能讀 B 的 episodes | ALC | P0 | platform | todo | ALC-05 | memory policies | 單元拒絕／空 |
| ALC-08 | ALC 閘門於代理人 **activate** | ALC | P0 | platform | todo | DP-02, ALC-02 | `update_agent_status` | 無 ALC 則拒 |
| ALC-09 | DNA `production_ready` 時步驟代理人缺 ALC 則拒 | ALC | P0 | platform | todo | ALC-08 | structure_validators | 單元擋 |
| ALC-10 | Auto-reflect 寫代理人範圍 lessons | ALC | P0 | platform | todo | ALC-02 | `_auto_reflect_if_enabled` | 終端 run 寫 agent lessons |
| ALC-11 | 依 agent_id 的成長／重用 metrics | ALC | P1 | platform | todo | ALC-01 | improvement metrics API | 兩次 run 後非空 |
| ALC-12 | example_domain 代理人 scopes 含 `agent` | DP | P0 | platform | todo | ALC-08, DP-07 | example agent_spec | 可 activate |
| ALC-13 | 自動化測試：同一代理人跨兩次 run 有學習 | T | P0 | platform | todo | ALC-06, ALC-12 | new unit／e2e | 綠 |
| EV-01 | 變體類型 `agent_genome` + 晉升前一律 sandbox_only | EV | P1 | platform | todo | ALC-01 | evolution service | 單元：無直接生產突變 |
| EV-02 | agent_genome 的 promote／rollback 路徑 | EV | P1 | platform | todo | EV-01 | evolution routes | 政策測試 |
| DOC-01 | `docs/domain-packs.md` + structure.md ALC／Domain Pack | DOC | P1 | platform | todo | DP-05, ALC-08 | docs/ | 審閱完成 |
| REG-01 | ALC／runtime 變更後 E1 仍 PASS | REG | P0 | platform | todo | ALC-02, ALC-08 | e2e E1 | 綠 |

**階段 1 離開：** 註冊可用；agent_id lessons；ALC 閘門；E1 綠。

---

### 5.3 階段 2 — 完整目錄 + 脊柱 E2E

| ID | 任務 | Workstream | Priority | Owner | Status | Depends on | Primary paths | Acceptance |
|----|------|------------|----------|-------|--------|------------|---------------|------------|
| N3-A-01 | **全員 L0：** 最小 agent_spec + stub SPEC（一屏）；深度 SPEC 僅脊柱 | N3 | P0 | video-pack | todo | P0-07, DP-02 | `business/video/agents/**` | 盤點 == 114；脊柱 SPEC 更豐 |
| N3-A-02 | 全部 agent_specs 填 ALC **欄位**（draft OK）；硬閘只在 activate | N3 | P0 | platform | todo | N3-A-01, ALC-08 | agent_spec.json × 114 | Schema 驗證；脊柱 activate 閘測過 |
| N3-P-01 | PROCESSES 覆蓋矩陣（流程 → DNA id → 代理人）——**先索引** | N3 | P0 | both | todo | P0-04 | PROCESSES.md | 每列有目標；status stub／ready |
| N3-P-02 | DNA：**一條可跑** viral-hook + 其他族**輕量 stub**（索引綁定，非全深度） | N3 | P0 | video-pack | todo | N3-P-01, BASE-02 | `business/video/workflows/*.dna.json` | viral-hook 可跑；其餘 schema 過 |
| N3-P-03 | 所有可執行 DNA 宣告 orchestrator／planner 入場 | N3 | P0 | video-pack | todo | N3-P-02 | DNA steps | 入場 = orchestrator／planner |
| VID-01 | 充實脊柱代理人：orchestrator、planner、router、judge、producer、director、screenwriter | VID | P0 | platform | todo | N3-A-01, ALC-08 | runtime／register | status active |
| VID-02 | Intent／DIA + research 模組可跑（深度規格接線） | VID | P0 | video-pack | todo | VID-01 | agents + knowledge | 脊柱 DNA 上 active |
| VID-03 | 撰寫 `wf_video_arch_a_viral_hook_v1`（編排器向下） | VID | P0 | video-pack | todo | N3-P-02, VID-01 | workflows/ | DNA 驗證通過 |
| VID-04 | `video.*` 工具權限登記 | VID | P0 | platform | todo | VID-03 | tool-permission-register.json | 範圍 + 閘門列出 |
| VID-05 | Adapters：media_gen_stub、script_format、qc_stub | VID | P0 | platform | todo | VID-04, BASE-04 | `adapters.py` | tool_effects 單元綠 |
| VID-06 | Golden：鉤子品質 + 人類閘門 | VID | P0 | video-pack | todo | VID-03 | `business/video/evals/` | business:eval 綠 |
| VID-07 | 回歸：不可逆步驟必須人類閘門 | T | P0 | platform | todo | VID-03 | video regression JSON | Pass |
| VID-08 | 對抗：注入不得擴大 allow-list | T | P0 | platform | todo | VID-05 | video adversarial JSON | Pass |
| VID-09 | E2E：queued→running→waiting_for_approval→succeeded | T | P0 | platform | todo | VID-03, VID-05 | new e2e | 綠 |
| VID-10 | E2E：終端後 agent lessons + auto-reflect | T | P0 | platform | todo | VID-09, ALC-10 | e2e | agent_id lessons 非空 |
| VID-11 | Improve 管線 propose sandbox 仍可用 | FE | P1 | platform | todo | VID-10, BASE-09 | ImproveRunButton | sandbox_only 變體 |
| FE-01 | 領域頁列出 **完整 114** 名冊（篩 draft／active） | FE | P0 | platform | todo | N3-A-01 | frontend domains／video | vitest 煙霧 |
| VID-12 | 自 va 參考播種知識（68 章 + 頂規）+ provenance | VID | P1 | va-specs | todo | P0-10 | `knowledge/seeds/` | 有 provenance |
| VID-13 | Tier-0 索引；acting_agent_id 檢索煙霧 | VID | P1 | platform | todo | VID-12 | knowledge APIs | 範圍命中 |
| N3-CI-01 | 盤點腳本：代理人數 ≠ 114 則失敗 | N3 | P0 | platform | todo | N3-A-01 | scripts／或 business:validate | CI 鉤就緒 |
| REG-02 | 客戶入職 E1 仍綠 | REG | P0 | platform | todo | VID-05 | e2e E1 | 無回歸 |
| DOC-02 | 更新 status.md + handoff：脊柱路徑 + N3 目錄狀態 | DOC | P1 | platform | todo | VID-09 | handoff.md | 已文件 |

**階段 2 離開：**（a）專案內 114 皆 L0（b）流程索引完整（c）脊柱 E2E demo。

---

### 5.4 階段 3 — 學習與共同演化

| ID | 任務 | Workstream | Priority | Owner | Status | Depends on | Acceptance |
|----|------|------------|----------|-------|--------|------------|------------|
| EV-03 | 影片 goldens 上多世代沙箱 | EV | P0 | platform | todo | VID-06, EV-01 | ≥2 世代已存 |
| EV-04 | 共同演化：planner genome × aesthetics／director | EV | P1 | platform | todo | EV-03 | 共享適應度記錄 |
| EV-05 | Lesson 效用／重用儀表板（API 或 FE） | ALC | P1 | platform | todo | ALC-11 | 指標可見 |
| EV-06 | 影片提示 skills 經 skill sandbox | EV | P1 | platform | todo | BASE-08, VID-01 | sandbox 後顯式 promote |
| EV-07 | 已學產物治理審閱 | GOV | P0 | product | todo | EV-03 | 簽核；無 auto_promote |
| EV-08 | 證明 ≥1 適應度改善且無生產倒退 | EV | P0 | platform | todo | EV-03 | 書面報告 |
| EV-09 | propose／eval／canary 審計事件 | EV | P0 | platform | todo | EV-03 | 審計存在 |

---

### 5.5 階段 4 — 多包、隔離、安全、負載

| ID | 任務 | Workstream | Priority | Owner | Status | Depends on | Acceptance |
|----|------|------------|----------|-------|--------|------------|------------|
| DP-09 | 第二包 example_research 或 podcast-lite（**影片目錄已存在後**） | DP | P0 | platform | todo | DP-08 | 零 runtime 分叉 |
| T-01 | 跨包記憶隔離測試 | T | P0 | platform | todo | DP-09, ALC-07 | 無外洩 |
| T-02 | 負載約 20 並行混合領域 runs | T | P1 | platform | todo | DP-09 | 不崩；不丟 lesson |
| T-03 | evolution archive p95 ~1k 變體（可行時） | T | P2 | platform | todo | EV-03 | 有記錄 |
| T-04 | FE 在 5 路 SSE 下 | FE | P2 | platform | todo | FE-01 | Pass |
| T-05 | 影片工具濫用紅隊 | RISK | P0 | platform | todo | VID-05 | allow-list 守住 |
| T-06 | 提示注入 CI 閘 | T | P0 | platform | todo | VID-08 | 必綠 |
| DOC-03 | 手冊「如何新增 Domain Pack」+ engine_range | DOC | P0 | platform | todo | DP-09, DOC-01 | 已發佈 |
| DOC-04 | PR 閘門：平台 vs 包 | DOC | P1 | product | todo | DOC-03 | 已寫 |
| DOD-01 | 平台 DoD D1–D6（adoption §7.5 平台） | GOV | P0 | product | todo | REG-02, T-01 | 全 true |

**注意：** 階段 4 **不得**標 N3 完成；完整 N3 是階段 5。

---

### 5.6 階段 5 — N3 完成（強制）

#### 5.6.1 啟用波次（代理人）

| ID | Wave | 範圍（adoption.md §5.1） | Workstream | Priority | Owner | Status | Depends on | Acceptance |
|----|------|--------------------------|------------|----------|-------|--------|------------|------------|
| W0 | Catalog | 全部 114 已在樹（階段 2） | N3 | P0 | — | leverage | N3-A-01 | count==114 |
| W1 | Spine active | orchestrator、planner、router、judge、producer、intent/DIA、director、screenwriter、research | VID | P0 | platform | todo | VID-01..03 | active + E2E |
| W2 | QC + creative | aiqaconsistency、aesthetics、optimization、gatekeeper、memory | VID | P0 | video-pack | todo | W1 | 脊柱上 active |
| W3 | Production crafts | 類 2–5 + promptengineer、avatardesign、voiceclone、talent | VID | P0 | video-pack | todo | W2 | gen／post DNA 上 active（可 stub） |
| W4 | Domain + GTM | 類 6–8 其餘 + 教育專精 | VID | P1 | video-pack | todo | W3 | 依 DNA active |
| W5 | Full meta + support | 其餘 #57–80、#81–114 + standby_pool | N3 | P0 | platform | todo | W4 | 全部編排器可達 |
| W6 | Process complete | A–J + LQR + 六階段 + UI 流程 | N3 | P0 | both | todo | W5, N3-P-10 | 盤點 100% |

#### 5.6.2 流程接線任務

| ID | 任務 | Workstream | Priority | Owner | Status | Depends on | Acceptance |
|----|------|------------|----------|-------|--------|------------|------------|
| N3-P-10 | 充實 `wf_video_production_e2e_v1` + 階段子 DNA | N3 | P0 | video-pack | todo | N3-P-02, W2 | 可跑或完整 stub 且真 agent ids |
| N3-P-11 | 充實 `wf_video_arch_a`…`j` 真代理人綁定 | N3 | P0 | video-pack | todo | N3-P-02, W3 | 10 原型 DNA 完成 |
| N3-P-12 | 充實 `wf_video_lqr_*` 族（6 張 LQR SVG） | N3 | P0 | video-pack | todo | N3-P-02, W2 | LQR 覆蓋 |
| N3-P-13 | 深度規格模組（GCA、aesthetics、RAG、DIA、optimization）接 DNA／服務 | N3 | P0 | platform | todo | W2 | 未丟棄；已文件 |
| N3-P-14 | `standby_pool` + router 表覆蓋每位代理人 | N3 | P0 | platform | todo | W5 | 孤兒檢查 == 0 |
| N3-CI-02 | 預設管線孤兒代理人 CI | N3 | P0 | platform | todo | N3-P-14 | 有孤兒則 fail |
| N3-CI-03 | 保留 CI：Appendix A pack_id 目錄被刪則 fail | N3 | P0 | platform | todo | N3-CI-01 | 已強制 |
| N3-A-10 | 按類別啟用其餘代理人（含 ALC） | N3 | P0 | platform | todo | W2–W5 | active 或 registered+可達 |
| FE-02 | `/app/domains/video` 儀表板（階段、資產、名冊狀態） | FE | P1 | platform | todo | FE-01 | 已出貨 |
| FE-03 | 進階時間軸（可選產品決策） | FE | P3 | platform | todo | FE-02 | go／no-go 記錄 |
| DOC-05 | va SYSTEM_REFERENCE 橫幅 → generic 包路徑 | DOC | P2 | va-specs | todo | W1 | 交叉連結 |
| DOC-06 | 可選同步腳本 va→business/video | DOC | P2 | both | todo | W6 | 已文件；預設 dry-run |
| DOD-02 | **N3 DoD** adoption §7.5 完整 va 採用六格 | GOV | P0 | product | todo | W6, N3-CI-02/03 | 全 true |
| DP-10 | 其他領域僅在 **DOD-02 之後** | DP | P2 | product | todo | DOD-02 | N2 不犧牲 N3 |

---

### 5.7 測試矩陣

| ID | 層 | 案例 | Depends on | Status |
|----|----|------|------------|--------|
| T-10 | Unit | ALC activate 被拒 | ALC-08 | todo |
| T-11 | Unit | lessons 有 agent_id + provenance | ALC-01/02 | todo |
| T-12 | Unit | 跨代理人隔離 | ALC-07 | todo |
| T-13 | Unit | 無效 domain manifest | DP-06 | todo |
| T-14 | Unit | agent_genome 不能跳過 sandbox | EV-01 | todo |
| T-15 | Unit | video adapters 寫 tool_effects | VID-05 | todo |
| T-16 | Unit | 盤點 count == 114 | N3-CI-01 | todo |
| T-17 | E2E | 影片脊柱生命週期 + 審批 | VID-09 | todo |
| T-18 | E2E | auto-reflect agent+org lessons | VID-10 | todo |
| T-19 | E2E | E1 仍 PASS | REG-01/02 | todo |
| T-20 | Eval | 影片 golden／regression／adversarial | VID-06..08 | todo |
| T-21 | Eval | 流程 DNA 覆蓋 vs PROCESSES.md | N3-P-10..12 | todo |
| T-22 | Load | 多領域並行 | T-02 | todo |
| T-23 | CI | 孤兒 + 保留閘 | N3-CI-02/03 | todo |

### 5.8 完成定義（DoD）

#### 平台（adoption.md §7.5）

| # | 閘門 | 連結任務 | Status |
|---|------|----------|--------|
| D1 | requires_alc 包強制 ALC | ALC-08/09 | todo |
| D2 | 影片脊柱 E2E 綠 | VID-09/10 | todo |
| D3 | 第二包無 runtime 分叉 | DP-09 | todo |
| D4 | 永不繞過 sandbox_only | EV-01, BASE-07 | todo |
| D5 | Unit + e2e + business:eval 綠 | T-10…T-20 | todo |
| D6 | status.md／handoff 已更新 | DOC-02 | todo |

#### 完整 va 採用 N3（強制）

| # | 閘門 | 連結任務 | Status |
|---|------|----------|--------|
| N3-D1 | 代理人數 + MAP == 114 | N3-A-01, N3-CI-01 | todo |
| N3-D2 | 10 類齊；meta 含 orchestrator／planner／router／judge | N3-A-01, W1 | todo |
| N3-D3 | 全部流程已索引 + DNA／文件 | N3-P-01..12 | todo |
| N3-D4 | 每位代理人編排器可達 | N3-P-14, N3-CI-02 | todo |
| N3-D5 | 保留 CI 已強制 | N3-CI-03 | todo |
| N3-D6 | 波次已文件；未啟用者 draft／registered 仍在 | W0–W6, DOC-02 | todo |

---

## 6. 類別匯入檢查清單（N3 目錄）

配合 Appendix A pack ids。Status = 資料夾+MAP+agent_spec 已存在（階段 2），未必 active。

| Cat | Range | Count | 啟用波次 | Catalog status |
|-----|-------|-------|----------|----------------|
| 1 ATL | 1–5 | 5 | W1（producer／director／screenwriter）+ W4 其餘 | todo |
| 2 Cam | 6–8 | 3 | W3 | todo |
| 3 Edit | 9–18 | 10 | W3 | todo |
| 4 Snd | 19–22 | 4 | W3 | todo |
| 5 Perf | 23–27 | 5 | W3 | todo |
| 6 Dist | 28–31 | 4 | W4 | todo |
| 7 Edu | 32–45 | 14 | W4 | todo |
| 8 AI | 46–52 | 7 | W2–W3 | todo |
| 9 Meta | 53–80 | 28 | W1 脊柱 + W5 其餘 | todo |
| 10 Sup | 81–114 | 34 | W5 | todo |
| **合計** | **1–114** | **114** | — | todo |

---

## 7. 流程匯入檢查清單（N3）

| 流程族 | DNA／產物目標 | Status |
|--------|---------------|--------|
| 六階段 E2E 製作 | `wf_video_production_e2e_v1` + 階段子 | todo |
| 原型 A viral-hook | `wf_video_arch_a_viral_hook_v1` | todo |
| 原型 B–J | `wf_video_arch_b` … `j` | todo |
| LQR（6 SVG） | `wf_video_lqr_*` | todo |
| 人↔AI 工作流圖 | PROCESSES.md 覆蓋矩陣 | todo |
| 批判／QC／交付織物 | DNA 內評估步驟 + 審批 | todo |
| 代理人管理／UI 流程 | FE 領域路由 | todo |
| 深度規格模組（GCA、aesthetics、RAG、DIA…） | 服務 + DNA 掛鉤 | todo |
| system_build_plan M0–M12 重定向 | DOC 註 pack-on-generic | todo |

---

## 8. 風險緩解行動

| ID | 風險 | 緩解任務 | Priority | Owner | Status | Linked |
|----|------|----------|----------|-------|--------|--------|
| R-01 | 雙平台重寫 | 強制 ADR；拒絕 va 再建第二 FastAPI／LangGraph 主機 | P0 | product | todo | P0-02 |
| R-02 | 遺失 va 保真度 | 種子 provenance；MAP 1:1 | P0 | video-pack | todo | VID-12, P0-07 |
| R-03 | N3 未完成／丟代理人 | Wave 0 完整匯入；階段 5 強制；保留 CI | P0 | product | todo | N3-CI-03, DOD-02 |
| R-04 | 孤兒代理人 | standby_pool + 孤兒 CI | P0 | platform | todo | N3-P-14 |
| R-05 | 共享記憶污染 | ALC 隔離測試 | P0 | platform | todo | ALC-07, T-01 |
| R-06 | 演化倒退 | 適應度 + 人類閘 + 審計；禁 auto_promote | P0 | platform | todo | EV-07/09 |
| R-07 | 媒體 API 成本 | CI stubs；allow-lists | P0 | platform | todo | VID-05 |
| R-08 | 破壞 E1／mark-100 | 每平台 PR 跑 REG-01/02 | P0 | platform | todo | REG-* |
| R-09 | 遷移遺失 | 包進 git；更名前備份 | P1 | platform | todo | P0-05 |
| R-10 | 文件語言漂移 | 包內 EN 規格為準；HK 腳本留 va | P2 | both | todo | N3-A-01 |
| R-11 | 階段 2 範圍爆炸 | 早期完整目錄；分波啟用 | P0 | product | todo | P0-06, W* |

---

## 9. 首 30 日

| 週 | 焦點 IDs | 成果 |
|----|----------|------|
| **1** | P0-01…P0-09、DP-01/02 草稿 | 合約、114 目錄、MAP、ROSTER、PROCESSES、基線綠 |
| **2** | DP-03…DP-08、ALC-01…ALC-05、ALC-08 | 註冊 + agent_id lessons + activate 閘 |
| **3** | ALC-06/07/10/13、EV-01、REG-01、DOC-01、N3-A-01 開始 | 行動前檢索；E1 綠；開始 L0 SPEC |
| **4** | N3-A-01/02、N3-P-02/03、VID-01…VID-10、FE-01、N3-CI-01、DOC-02 | 目錄完成 + 脊柱 E2E |

| 30 日成功 | Status |
|-----------|--------|
| 114 代理人目錄 + MAP | todo |
| ALC + domain register 可用 | todo |
| 脊柱 E2E + 人類閘 + agent lessons | todo |
| E1 仍 PASS | todo |

---

## 10. 關鍵路徑

```text
P0 批准/ADR → ROSTER+MAP+114 目錄 → 基線綠
        │
        ▼
 schemas → domain register → ALC agent_id lessons + 閘門 → REG E1
        │
        ▼
 N3-A 全員 L0 agent_spec → 流程索引/DNA stubs → 脊柱代理人 + viral-hook E2E
        │
        ├──► 階段 3 多世代學習
        │
        ├──► 階段 4 第二包 + 隔離（非 N3 完成）
        │
        └──► 階段 5 波次 W2–W6 + 流程接線 + 孤兒/保留 CI → DOD-02 N3 DONE
```

---

## 11. 擁有權摘要

| Owner | 主要 IDs |
|-------|----------|
| **platform** | DP-*、ALC-*、EV-*、REG-*、N3-CI-*、多數 T-*、VID adapters／runtime |
| **video-pack** | N3-A-*、N3-P-*、VID DNA／evals、MAP 內容 |
| **va-specs** | P0-03/04/10、VID-12、DOC-05、保真度 |
| **product** | P0-01/02/11、EV-07、DOD-*、DP-10 閘、R-01/R-03 |
| **both** | P0-07、W6、R-10 |

---

## 12. 進度匯總

| 桶 | ~數 | todo | leverage | done |
|----|-----|------|----------|------|
| BASE | 12 | 0 | 12 | 0 |
| 階段 0 | 12 | 12 | 0 | 0 |
| 階段 1 | 22 | 22 | 0 | 0 |
| 階段 2 | 20 | 20 | 0 | 0 |
| 階段 3 | 7 | 7 | 0 | 0 |
| 階段 4 | 10 | 10 | 0 | 0 |
| 階段 5 波次 + 流程 | 18 | 17 | 1 | 0 |
| 測試 | 14 | 14 | 0 | 0 |
| 風險 | 11 | 11 | 0 | 0 |
| **合計** | **~126** | **~113** | **13** | **0** |

隨工作更新 Status 儲存格。**DOD-02 為真前 N3 未完成。**

---

## 13. 相關文件

| 文件 | 角色 |
|------|------|
| `adoption.md` v2.3 | 策略 + Appendix A 名冊 + Appendix B 就緒度 |
| `adoption_hk.md`／`adoption_hk.script.txt` | 繁中策略 + YouTube 腳本 |
| `adoption_plan.md` | 本計劃英文原文 |
| `review_adoption.md` | 原始審閱簡報 |
| `status.md`／`memory/handoff.md` | 即時狀態 |
| va `study/agents.md` | 權威 114 名稱 |
| va `study/SYSTEM_REFERENCE.md` | 流程整合圖 |

---

## 14. 變更紀錄

| 版本 | 日期 | 說明 |
|------|------|------|
| 1.0 | 2026-07-10 | 自 adoption.md v2 初表 |
| 2.0 | 2026-07-10 | 研究導向 BASE leverage + as-built 缺口 |
| 3.0 | 2026-07-10 | 對齊 adoption.md v2.2 N3 |
| 3.1 | 2026-07-10 | §15 詳細微步驟手冊 |
| 3.2 | 2026-07-10 | Rethink：§0 原則；L0／L1／L2；關鍵路徑 §0.3 |
| **3.2-hk** | **2026-07-10** | **本檔：** `adoption_plan.md` 繁體中文完整翻譯 |

---

## 15. 詳細逐步手冊

每個 §5 父任務拆成有序微步驟。  
**關鍵路徑父任務（§0.3）：** 標 `done` 前完成其微步驟。  
**非關鍵父任務：** 需要時再用手冊；不要擋住脊柱 demo。  
命令預設倉庫根目錄 `generic-swarm-ops`；路徑用正斜線。

### 15.0 手冊慣例

| 慣例 | 含義 |
|------|------|
| `va/` | `C:\Project\va-agent-swarm`（或 clone 路徑） |
| `gso/` | `C:\Project\generic-swarm-ops` |
| **Verify** | 下一步前必須通過 |
| **Stop** | 硬閘——失敗勿繼續 |
| Stub SPEC | 最小 SPEC.md：名稱、va id、類別、3–5 點職責、來源連結、status `draft` |
| Full SPEC | 職責 + 工具 + 批判夥伴 + ALC 註 + 有深度規格時的 provenance |

**每日循環（建議）：**

| 步 | 行動 |
|----|------|
| 1 | 從關鍵路徑（§10／§0.3）取下一個父 ID |
| 2 | 打開下方對應手冊小節 |
| 3 | 依序執行 `.s1`、`.s2`…；勾 Status |
| 4 | 跑該父任務 **Verify** |
| 5 | 提交 `feat(adoption): <parent-id> <short>` |
| 6 | 若動了 `runtime.py` 或 routes，重跑 REG 基線 |

---

### 15.1 階段 0 手冊

#### P0-01 — 批准策略

| Step | 行動 | Status |
|------|------|--------|
| P0-01.s1 | 打開 `adoption.md` v2.3 與本計劃；確認理解 N1／N2／N3 | todo |
| P0-01.s2 | 在 `status.md` Latest update 記錄批准：日期 +「adoption v2.3 + plan v3.2 已批准」 | todo |
| P0-01.s3 | 可選：開 GitHub issue／milestone「Video Domain Pack N3」連到本計劃 | todo |

**Verify：** `status.md` 有批准註記。

#### P0-02 — ADR

| Step | 行動 | Status |
|------|------|--------|
| P0-02.s1 | 若無則建 `docs/adr/` | todo |
| P0-02.s2 | 寫 `docs/adr/0001-video-domain-pack-on-generic.md`：Context、Decision、Consequences | todo |
| P0-02.s3 | Decision 必須含：（a）generic 唯一控制平面；（b）va 不做第二 LangGraph／Temporal 主機；（c）114 代理人住 `business/video/agents/`；（d）禁止刪除名冊代理人 | todo |
| P0-02.s4 | 自 `business/video/README.md` 連到 ADR | todo |

**Verify：** ADR 存在且含四條決策。

#### P0-03 — 匯出 ROSTER.json（114）

| Step | 行動 | Status |
|------|------|--------|
| P0-03.s1 | 打開 `va/study/agents.md` | todo |
| P0-03.s2 | 解析表列 `\| N \| **NameAgent**`，N=1..114（僅 Agent 名稱列） | todo |
| P0-03.s3 | 交叉核對類別計數：5+3+10+4+5+4+14+7+28+34 = 114 | todo |
| P0-03.s4 | 若無則建 `gso/business/video/` | todo |
| P0-03.s5 | 寫 `business/video/ROSTER.json` 陣列物件：`id`、`name`、`category`、`pack_id`（用 adoption Appendix A） | todo |
| P0-03.s6 | JSON 可解析；`length == 114`；`id` 與 `pack_id` 唯一 | todo |

**Verify：** `(Get-Content business/video/ROSTER.json -Raw | ConvertFrom-Json).Count` 期望 114。  
**Stop** 若 ≠ 114。

#### P0-04 — 匯出 PROCESSES.md

| Step | 行動 | Status |
|------|------|--------|
| P0-04.s1 | 讀 `va/study/SYSTEM_REFERENCE.md` §6.1（六階段） | todo |
| P0-04.s2 | 列出原型 `A-*.svg`…`J-*.svg`（10） | todo |
| P0-04.s3 | 列出 `lqr-*.svg`（6） | todo |
| P0-04.s4 | 列出 `va/study/ui/*.md`（EN） | todo |
| P0-04.s5 | 寫 PROCESSES.md：編排脊柱、六階段 E2E、A–J、LQR、UI、深度規格模組 | todo |
| P0-04.s6 | 每列含 process_id、source_path、target_dna_id、entry_agent、status | todo |

**Verify：** 文檔提到 Orchestrator #53／Planner #54、階段 1–6、A–J、LQR。

#### P0-05 — 骨架 business/video/

| Step | 行動 | Status |
|------|------|--------|
| P0-05.s1 | 建 dirs：agents／workflows／evals/{golden,regression,adversarial}／knowledge/seeds／tools／policies／ui | todo |
| P0-05.s2 | 寫 README：目的、N3 規則、連 ROSTER／MAP／PROCESSES／ADR | todo |
| P0-05.s3 | 草稿 manifest.json：`domain_id: "video"`、`requires_alc: true`、`version: "0.1.0"` | todo |
| P0-05.s4 | 寫 tools/adapters.md 列計劃中 `video.*` 工具 | todo |

#### P0-06 — 114 佔位目錄

| Step | 行動 | Status |
|------|------|--------|
| P0-06.s1 | 對 ROSTER 每個 pack_id 建 `business/video/agents/<pack_id>/` | todo |
| P0-06.s2 | 每目錄：`agent_spec.json`（draft）、`SPEC.md`（stub）、`prompts/.gitkeep`、`rubrics/.gitkeep` | todo |
| P0-06.s3 | agent_spec 最小欄位：id、va_id、name、domain_id、status draft、requires_alc true、allowed_memory_scopes 含 agent、hooks.reflect true、alc_version | todo |
| P0-06.s4 | 目錄數 == 114 | todo |

**Verify：** `(Get-ChildItem business/video/agents -Directory).Count` 期望 114。**Stop** 若 ≠。

#### P0-07 — MAP.md

| Step | 行動 | Status |
|------|------|--------|
| P0-07.s1 | 建 MAP 表頭：va_id｜name｜pack_id｜category｜va_source｜generic_path｜runtime_status｜notes | todo |
| P0-07.s2 | ROSTER 每列一列；generic_path = `business/video/agents/<pack_id>/` | todo |
| P0-07.s3 | 有深度規格則 va_source 指該檔，否則 agents.md#id | todo |
| P0-07.s4 | 列數 == 114 | todo |

#### P0-08 — example_domain

| Step | 行動 | Status |
|------|------|--------|
| P0-08.s1 | 建 example_domain 類似子樹（較小） | todo |
| P0-08.s2 | 1–2 玩具代理人如 example.worker、example.reviewer，含 ALC 欄位 | todo |
| P0-08.s3 | 一條玩具 DNA 檔（階段 1 再補齊有效 DNA） | todo |
| P0-08.s4 | README 說明僅 N2 用途 | todo |

#### P0-09 — 基線綠

| Step | 行動 | Status |
|------|------|--------|
| P0-09.s1 | 根目錄跑 status.md 所述測試 | todo |
| P0-09.s2 | backend unit suite | todo |
| P0-09.s3 | e2e test_e1_operator_path | todo |
| P0-09.s4 | frontend pnpm lint／typecheck／test | todo |
| P0-09.s5 | 證據寫入 status.md 或 reviews 日誌 | todo |

**Stop** 若 E1 失敗——階段 1 改碼前先修。

#### P0-10／P0-11／P0-12

| Step | 行動 | Status |
|------|------|--------|
| P0-10.s1 | 列舉 va/study 規格檔 | todo |
| P0-10.s2 | PROCESSES 加模組→檔案→包目標表 | todo |
| P0-10.s3 | coding agent 標 sandbox-only／不改 host | todo |
| P0-11.s1 | §8 風險表填 Owner | todo |
| P0-12.s1 | ADR 附錄：同步 = PR 複製；submodule 延後 | todo |
| P0-12.s2 | 文件「Wave 0 後代理人不得只活在 va」 | todo |

---

### 15.2 階段 1 手冊（Domain Pack + ALC）

#### DP-01…DP-03 — Schemas

| Step | 行動 | Status |
|------|------|--------|
| DP-01.s1 | 參考 workflow-dna.schema.json 風格 | todo |
| DP-01.s2 | domain-manifest：required domain_id、version、requires_alc、agents[]、workflows[] | todo |
| DP-02.s1 | agent-spec：required id、domain_id、status、requires_alc、allowed_memory_scopes、hooks.reflect、alc_version | todo |
| DP-02.s2 | requires_alc true 時必須含 scope `"agent"` | todo |
| DP-03.s1 | learning-log：required agent_id、text／lesson_text、provenance | todo |
| DP-0x.s_fix | 正／負 fixtures | todo |

#### DP-05 — Domain register

| Step | 行動 | Status |
|------|------|--------|
| DP-05.s1 | 新增 routes/domains.py POST /register（auth + RBAC） | todo |
| DP-05.s2 | 載入器：讀 manifest、驗證 schema、代理人入 org draft（不強制 active） | todo |
| DP-05.s3 | router 掛 `/domains` | todo |
| DP-05.s4 | 可選 CLI domain:register --domain video --dry-run | todo |
| DP-05.s5 | 單元：video + example dry-run | todo |

#### ALC-01 — Lesson.agent_id

| Step | 行動 | Status |
|------|------|--------|
| ALC-01.s1 | lessons.py 加 agent_id 可選欄位 | todo |
| ALC-01.s2 | to_dict／from_dict 含 agent_id | todo |
| ALC-01.s3 | 去重鍵：text + workflow_id + agent_id | todo |
| ALC-01.s4 | retrieve(..., agent_id=) 可過濾 | todo |
| ALC-01.s5 | 單元：無 agent_id 舊資料可載 | todo |

#### ALC-02 — 依步驟代理人拆 reflect

| Step | 行動 | Status |
|------|------|--------|
| ALC-02.s1 | 每步讀 step agent／agent_id | todo |
| ALC-02.s2 | lessons 標該 agent_id；缺則 null + 工作流層 | todo |
| ALC-02.s3 | _write_memory 有 agent 時傳入（勿永遠 None） | todo |
| ALC-02.s4 | 單元：多代理人 run → ≥2 不同 agent_id | todo |

#### ALC-03／04 — 代理人反思 API

| Step | 行動 | Status |
|------|------|--------|
| ALC-03.s1 | POST reflect/agent/{agent_id} | todo |
| ALC-03.s2 | 只過濾該代理人 | todo |
| ALC-04.s1 | GET lessons?agent_id= | todo |
| ALC-04.s2 | 需要時 api:generate | todo |

#### ALC-05…ALC-07 — 情節、注入、隔離

| Step | 行動 | Status |
|------|------|--------|
| ALC-05.s1 | 步驟完成寫 episode | todo |
| ALC-05.s2 | 存 agent_episodes 或 scope agent | todo |
| ALC-06.s1 | 步驟前 load top-k lessons + memory | todo |
| ALC-06.s2 | 附在 step context injected_lessons | todo |
| ALC-06.s3 | 單元 assert retrieve 用對 agent_id | todo |
| ALC-07.s1 | A 寫／B 讀 → 空或 403 | todo |
| ALC-07.s2 | memory search 強制 acting_agent_id | todo |

#### ALC-08／09 — 啟用閘

| Step | 行動 | Status |
|------|------|--------|
| ALC-08.s1 | **僅** update 到 active 時檢查 ALC（draft 可匯入） | todo |
| ALC-08.s2 | 錯誤碼 alc_required | todo |
| ALC-09.s1 | production_ready 時每個 active 步驟代理人須過 ALC | todo |
| ALC-09.s2 | 單元：production_ready + 非 ALC → 拒；draft DNA + draft 代理人 → 可 | todo |

#### ALC-10…REG-01

| Step | 行動 | Status |
|------|------|--------|
| ALC-10.s1 | auto-reflect 走 ALC-02 路徑 | todo |
| ALC-10.s2 | 磁碟 artifact 含 agent_id（有則） | todo |
| ALC-11.s1 | GET metrics?agent_id= | todo |
| ALC-12.s1 | example 含 agent scope 後 activate | todo |
| ALC-13.s1 | run1 lessons；run2 uses 增加 | todo |
| EV-01.s1 | agent_genome 強制 sandbox_only | todo |
| EV-01.s2 | 拒直接生產突變 | todo |
| REG-01.s1 | 階段 1 合併後重跑 E1 + unit | todo |
| DOC-01.s1 | domain-packs.md | todo |
| DOC-01.s2 | structure.md 短節連結 | todo |

---

### 15.3 階段 2 手冊（目錄 + 脊柱）

#### N3-A-01 — 全員 L0（非全員長文）

| Step | 行動 | Status |
|------|------|--------|
| N3-A-01.s1 | 按類 1→10 批次（不跳 meta／support）——**僅 L0** | todo |
| N3-A-01.s2 | 確認 MAP + 目錄 + P0-06 最小 agent_spec | todo |
| N3-A-01.s3 | Stub SPEC：一段職責 + 連 va agents.md id + draft（**非**深度規格傾倒） | todo |
| N3-A-01.s4 | **僅脊柱**（orchestrator、planner、router、judge、producer、director、screenwriter + intent／research）：較完整 SPEC | todo |
| N3-A-01.s5 | 其餘深度 SPEC 延到**啟用波次**（階段 5／W*） | todo |
| N3-A-01.s6 | 每批後盤點 == 114 | todo |

#### N3-A-02／N3-P-01…03

| Step | 行動 | Status |
|------|------|--------|
| N3-A-02.s1 | 腳本驗證全部 agent_spec vs schema | todo |
| N3-A-02.s2 | 修缺 agent scope／reflect | todo |
| N3-A-02.s3 | manifest agents[] = 全部 114 pack_ids | todo |
| N3-P-01.s1 | 擴 PROCESSES 矩陣 | todo |
| N3-P-02.s1 | 建 e2e、arch_a…j、lqr_* DNA 檔（輕量 stub OK） | todo |
| N3-P-02.s2 | 滿足 workflow-dna.schema 必填；production_ready false | todo |
| N3-P-02.s3 | 步驟命名真實 pack_ids | todo |
| N3-P-03.s1 | 第一步 agent = video.orchestrator 或 video.planner | todo |

**DNA stub 做法：** 複製 `business/examples/workflow-dna.example.json` → 改 id → 步驟代理人改 video pack ids → domain video → production_ready false。

#### VID-01…VID-05

| Step | 行動 | Status |
|------|------|--------|
| VID-01.s1 | 脊柱 agent_spec 過 ALC | todo |
| VID-01.s2 | 註冊 video 包 | todo |
| VID-01.s3 | 啟用脊柱 active | todo |
| VID-01.s4 | 非脊柱維持 draft | todo |
| VID-02.s1 | DIA 映射 intent 路徑 | todo |
| VID-02.s2 | research 接 knowledge 搜尋 | todo |
| VID-02.s3 | 脊柱 DNA 加 intent→research 步驟 | todo |
| VID-03.s1 | 自 A-viral-hook + SYSTEM_REFERENCE 寫步驟 | todo |
| VID-03.s2 | 建議序：orchestrator/planner→intent→producer→director/screenwriter→research/aesthetics→media_stub→qc→gate?→package | todo |
| VID-03.s3 | 不可逆步驟 human_gate_required true | todo |
| VID-03.s4 | 驗證 DNA；建版本；evals 前勿 production_ready | todo |
| VID-04.s1 | 登記 video_media_gen_stub 等 | todo |
| VID-05.s1 | adapters.py 實作 _effect | todo |
| VID-05.s2 | 進 TOOL_ADAPTERS | todo |
| VID-05.s3 | 單元 tool_effects | todo |

#### VID-06…DOC-02

| Step | 行動 | Status |
|------|------|--------|
| VID-06.s1 | video/evals/golden 仿 onboarding | todo |
| VID-07.s1 | 去掉 human_gate 必須驗證失敗 | todo |
| VID-08.s1 | 惡意輸入不得擴大工具表 | todo |
| VID-09.s1 | e2e test_video_spine_path | todo |
| VID-09.s2 | auth→run→approve→succeeded | todo |
| VID-10.s1 | reflect 後 spine agent_id lessons | todo |
| FE-01.s1 | /app/domains/video 或 domain=video 篩選 | todo |
| FE-01.s2 | 列 114 + 狀態徽章 | todo |
| FE-01.s3 | vitest | todo |
| N3-CI-01.s1 | 讀 ROSTER + 掃 agents/* | todo |
| N3-CI-01.s2 | 缺 pack_id 失敗 | todo |
| N3-CI-01.s3 | 掛 business:validate 或 video:inventory | todo |
| VID-11.s1 | Improve reflect→propose；sandbox_only | todo |
| VID-12.s1 | 種子 provenance va@sha | todo |
| VID-13.s1 | 索引 + acting_agent_id 搜 | todo |
| REG-02.s1 | 合併 adapters 後重跑 E1 | todo |
| DOC-02.s1 | status + handoff 寫操作路徑與 114 | todo |

---

### 15.4 階段 3 手冊（學習）

| 父 ID | 微步驟 | Status |
|-------|--------|--------|
| EV-03 | s1 自失敗建 ≥2 沙箱變體；s2 各評影片 goldens；s3 存 fitness archive | todo |
| EV-04 | s1 突變 planner genome；s2 突變 aesthetics／director；s3 聯合評分 | todo |
| EV-05 | s1 暴露 metrics；s2 顯示 reuse／utility | todo |
| EV-06 | s1 _sandbox 提案 skill；s2 僅人類 promote | todo |
| EV-07 | s1 治理清單審；s2 記決策；s3 確認無 auto_promote | todo |
| EV-08 | s1 基線指標；s2 演化後指標；s3 無自動改生產 DNA | todo |
| EV-09 | s1 查演化審計；s2 assert propose／eval／canary | todo |

---

### 15.5 階段 4 手冊

| 父 ID | 微步驟 | Status |
|-------|--------|--------|
| DP-09 | s1 第二包骨架；s2 無改 runtime 核心註冊；s3 一條玩具 DNA | todo |
| T-01 | s1 整合測 video memory vs 外域 agent_id；s2 空／拒 | todo |
| T-02 | s1 N=20 並行；s2 不崩；s3 lesson 數穩定 | todo |
| T-03 | s1 量 archive 延遲；s2 記 p95 | todo |
| T-04 | s1 五路 SSE；s2 FE 可用 | todo |
| T-05 | s1 工具濫用案例；s2 allow-list 守住 | todo |
| T-06 | s1 對抗進 CI 必綠；s2 回歸 fail pipeline | todo |
| DOC-03 | s1 Add Domain Pack 手冊；s2 engine_range | todo |
| DOC-04 | s1 平台 PR 清單；s2 包 PR 清單 | todo |
| DOD-01 | s1 僅有證據時勾 D1–D6 | todo |

---

### 15.6 階段 5 手冊（N3 完成）

#### 每波啟用檢查清單（W2–W5 套用）

| Step | 行動 | Status |
|------|------|--------|
| Wx.s1 | 自 §5.6.1 選本波 pack_ids | todo |
| Wx.s2 | agent_spec ALC 驗證 | todo |
| Wx.s3 | 每人在 ≥1 DNA 步驟或進 standby_pool | todo |
| Wx.s4 | activate 或維持 registered standby | todo |
| Wx.s5 | 煙霧：含新代理人的 DNA | todo |
| Wx.s6 | 更新 MAP runtime_status | todo |
| Wx.s7 | 重跑盤點 + 孤兒檢查 | todo |

#### N3-P-10…14／CI／DOD-02

| Step | 行動 | Status |
|------|------|--------|
| N3-P-10.s1 | SYSTEM_REFERENCE 六階段映射步驟組 | todo |
| N3-P-10.s2 | 綁真實 pack_ids（媒體 stub） | todo |
| N3-P-10.s3 | 入場 orchestrator／planner；不可逆 human gate | todo |
| N3-P-10.s4 | 驗證 DNA；可選 dry-run | todo |
| N3-P-11.s1 | 各 SVG B–J 列主要階段 | todo |
| N3-P-11.s2 | 充實 DNA + 編排入場 | todo |
| N3-P-11.s3 | 長片級可經 standby 引用全名冊 | todo |
| N3-P-11.s4 | 10／10 原型覆蓋 | todo |
| N3-P-12.s1 | 每 LQR SVG 一 DNA 或父 DNA + 子流文件 | todo |
| N3-P-12.s2 | 含 continuity／AIQA／quality-gate 代理人 | todo |
| N3-P-12.s3 | PROCESSES LQR 列 ready | todo |
| N3-P-13.s1 | GCA 作導演／編劇共享服務 | todo |
| N3-P-13.s2 | aesthetics 掛生成步驟 | todo |
| N3-P-13.s3 | Agentic RAG → 知識管線 | todo |
| N3-P-13.s4 | DIA → intent 步驟 | todo |
| N3-P-13.s5 | optimization 連交付 DNA | todo |
| N3-P-13.s6 | coding agent 僅 sandbox（文件化） | todo |
| N3-P-14.s1 | standby_pool.json 含 114 pack_ids | todo |
| N3-P-14.s2 | router／orchestrator 可選 pool | todo |
| N3-P-14.s3 | 孤兒腳本：不在 DNA 且不在 pool → fail | todo |
| N3-CI-02.s1 | 孤兒檢查進 CI | todo |
| N3-CI-03.s1 | 刪 Appendix 目錄 → fail | todo |
| N3-A-10.s1 | 按波次檢查清單啟用其餘 | todo |
| FE-02.s1 | 儀表板：階段、資產、名冊狀態計數 | todo |
| DOC-05.s1 | va SYSTEM_REFERENCE 橫幅 | todo |
| DOC-06.s1 | 同步腳本；預設 dry-run | todo |
| DOD-02.s1 | 收集 N3-D1…D6 證據連結 | todo |
| DOD-02.s2 | status.md 簽「N3 complete」 | todo |
| DP-10.s1 | 僅 DOD-02 後排其他領域 | todo |

---

### 15.7 測試執行細節

| Test ID | 詳細步驟 | Status |
|---------|----------|--------|
| T-10 | 建缺 agent scope 代理人 → activate → 期望 4xx alc_required | todo |
| T-11 | 多代理人 run reflect → GET lessons?agent_id= → 非空 + provenance | todo |
| T-12 | A 寫 episode；B 讀 → 空／拒 | todo |
| T-13 | POST domains/register 壞 manifest → 400 | todo |
| T-14 | propose agent_genome 帶生產突變 → 拒 | todo |
| T-15 | 呼叫 video_media_gen_stub → 有 tool_effects | todo |
| T-16 | 盤點腳本 exit 0 僅當 114 | todo |
| T-17 | 完整影片脊柱 e2e | todo |
| T-18 | e2e 後 reflect → agent lessons | todo |
| T-19 | E1 e2e 綠 | todo |
| T-20 | business:eval 含 video 包 | todo |
| T-21 | 腳本：PROCESSES 每 DNA 檔存在 | todo |
| T-22 | 負載 20 並行 | todo |
| T-23 | CI 含 inventory+orphan+retention | todo |

---

### 15.8 操作手冊（階段 2 後脊柱 demo）

| Step | 行動 | Status |
|------|------|--------|
| OP.s1 | 依 backend README 起 Postgres + FastAPI | todo |
| OP.s2 | 前端 `NEXT_PUBLIC_DEMO_MODE=false` | todo |
| OP.s3 | 種子 admin 登入 | todo |
| OP.s4 | 確認影片代理人可見（114 列表／篩選） | todo |
| OP.s5 | 開 `wf_video_arch_a_viral_hook_v1` run | todo |
| OP.s6 | 需要則批准人類閘門 | todo |
| OP.s7 | Improve → Reflect；確認 agent lessons | todo |
| OP.s8 | Propose 沙箱變體；確認 sandbox_only | todo |
| OP.s9 | 證據寫入 handoff.md | todo |

---

### 15.9 DoD 證據檢查清單

| 閘門 | 所需證據產物 | Status |
|------|--------------|--------|
| D1 ALC | 單元 log T-10 + 程式 ref ALC-08 | todo |
| D2 脊柱 E2E | T-17 log + run_id | todo |
| D3 第二包 | DP-09 dry-run 輸出 | todo |
| D4 sandbox_only | T-14 + evolution 測試 | todo |
| D5 套件綠 | CI URL 或本機 log 包 | todo |
| D6 Handoff | status.md + handoff 段落 | todo |
| N3-D1 | 盤點腳本輸出 114 | todo |
| N3-D2 | MAP 類別計數 | todo |
| N3-D3 | PROCESSES 列 ready | todo |
| N3-D4 | 孤兒腳本 exit 0 | todo |
| N3-D5 | 保留 CI job 存在 | todo |
| N3-D6 | 波次表狀態 done | todo |

---

*採用行動計劃 v3.2 繁體中文版完（對齊 `adoption_plan.md`）*
