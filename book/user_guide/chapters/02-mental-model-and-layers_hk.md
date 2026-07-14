# 第 02 章：心智模型與分層架構

> **語言：** 繁體中文（`_hk`）  
> **狀態：** 骨架於 `book/user_guide/` — 請在此擴寫完整內文  
> **程度：** 初學者  
> **部：** 第 I 部 — 基礎  
> **預估時間：** 40 分鐘  
> **路徑：** `book/user_guide/chapters/02-mental-model-and-layers_hk.md`  
> **英文對照：** [`02-mental-model-and-layers.md`](./02-mental-model-and-layers.md)


## 插圖

![心智模型與分層架構](../assets/02-system-overview.svg)

*圖：心智模型與分層架構 — 來源 `assets/02-system-overview.svg`*


## 學習目標

- 把 repo 資料夾對應到執行層
- 說明 harness 同步（.trae/.grok）vs 後端 runtime
- 追蹤請求：UI → API → runtime → tool → audit

## 敘事大綱（擴寫為完整正文）

1. 分層表：starter、business、backend、frontend、generated
2. Repo 地圖：backend/、frontend/、business/、rules/、scripts/
3. 請求生命週期（操作員點擊 → JSON → DNA 步驟）
4. 持久化：Postgres 主、JSON 快照備援
5. 為何 evolution 不直接就地改 production DNA
6. 常見誤解：第二個 LangGraph 控制平面 — 此處沒有

## 實作實驗

- [ ] 列出根目錄並分層歸類
- [ ] 完整閱讀 docs/architecture.md 一次

## 主要來源（未驗證前勿臆造）

- `docs/architecture.md`
- `structure.md`
- `docs/sync.md`

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
