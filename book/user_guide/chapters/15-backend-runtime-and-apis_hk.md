# 第 15 章：後端 Runtime 與 API

> **語言：** 繁體中文（`_hk`）  
> **狀態：** 骨架於 `book/user_guide/` — 請在此擴寫完整內文  
> **程度：** 專家  
> **部：** 第 V 部 — 專家與生產  
> **預估時間：** 75 分鐘  
> **路徑：** `book/user_guide/chapters/15-backend-runtime-and-apis_hk.md`  
> **英文對照：** [`15-backend-runtime-and-apis.md`](./15-backend-runtime-and-apis.md)


## 插圖

![後端 Runtime 與 API](../assets/02-system-overview.svg)

*圖：後端 Runtime 與 API — 來源 `assets/02-system-overview.svg`*


## 學習目標

- 定位 runtime 進入點與路由模組
- 認證並呼叫核心 API，注意 request_id
- 說明 store 後端（Postgres vs JSON）

## 敘事大綱（擴寫為完整正文）

1. app.main 與 middleware
2. RuntimeServices 職責
3. 路由圖：auth、workflows、runs、approvals、domains、improvement…
4. OpenAPI 匯出
5. 測試金字塔：unit vs e2e
6. 閱讀 tool_effects 與 runtime.json 快照

## 實作實驗

- [ ] 在 OpenAPI 找到 recommend-workflow
- [ ] 在 runtime.py 追蹤 recommend_video_workflow
- [ ] 跑 special skills + archetype 單元測試

## 主要來源（未驗證前勿臆造）

- `backend/README.md`
- `book/design_phase/book.backend_hk.md`
- `backend/app/api/v1/routes/`
- `backend/app/runtime.py`

## 撰寫檢查清單（完整稿）

- [ ] 開場一段說明「為何重要」
- [ ] 步驟指令以 Windows PowerShell 為主，必要時附 bash
- [ ] 每個主要實驗含「預期結果」
- [ ] 相關處標明殘留／未宣稱
- [ ] 交叉連結上一章／下一章（`*_hk.md`）
- [ ] SVG 使用 `../assets/`（與英文版共用圖檔）
- [ ] 術語與英文版一致；產品識別碼（dna_id、API 路徑）不翻譯

## 導覽

- 目錄：[../TOC_hk.md](../TOC_hk.md)
- 主檔：[../user_guide_hk.md](../user_guide_hk.md)
- 英文主檔：[../user_guide.md](../user_guide.md)
- 計畫：[../../../planning/user_guide/00_PLAN.md](../../../planning/user_guide/00_PLAN.md)
