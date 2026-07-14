# 第 16 章：前端深入

> **語言：** 繁體中文（`_hk`）  
> **狀態：** 骨架於 `book/user_guide/` — 請在此擴寫完整內文  
> **程度：** 專家  
> **部：** 第 V 部 — 專家與生產  
> **預估時間：** 60 分鐘  
> **路徑：** `book/user_guide/chapters/16-frontend-deep-dive_hk.md`  
> **英文對照：** [`16-frontend-deep-dive.md`](./16-frontend-deep-dive.md)


## 插圖

![前端深入](../assets/04-console-map.svg)

*圖：前端深入 — 來源 `assets/04-console-map.svg`*


## 學習目標

- 說明 client 認證 cookie 與 live-data facade
- 安全地將新面板接到 backendApi
- 保持 demoMode 僅 opt-in

## 敘事大綱（擴寫為完整正文）

1. App shell、側欄、slug 路由器
2. backendApi 模式
3. product-data demo vs live
4. 表單：Zod + RHF + formatMutationError
5. Improve 與 evolution 面板
6. Vitest + Playwright smoke
7. 以 Domains 風格加功能而不分叉架構

## 實作實驗

- [ ] 閱讀 client.ts recommend + special skills 方法
- [ ] 跑 frontend product-slice 單元測試
- [ ] 追蹤 env.ts 的 demoMode 預設

## 主要來源（未驗證前勿臆造）

- `frontend/README.md`
- `frontend/src/lib/api/client.ts`
- `frontend/src/lib/config/env.ts`
- `frontend/docs/api/frontend-api-contract.md`

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
