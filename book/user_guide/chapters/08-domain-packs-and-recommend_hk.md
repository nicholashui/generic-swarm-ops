# 第 08 章：領域包與工作流推薦

> **語言：** 繁體中文（`_hk`）  
> **狀態：** 骨架於 `book/user_guide/` — 請在此擴寫完整內文  
> **程度：** 中級  
> **部：** 第 III 部 — 領域與 video pack  
> **預估時間：** 60 分鐘  
> **路徑：** `book/user_guide/chapters/08-domain-packs-and-recommend_hk.md`  
> **英文對照：** [`08-domain-packs-and-recommend.md`](./08-domain-packs-and-recommend.md)


## 插圖

![領域包與工作流推薦](../assets/08-domain-recommend.svg)

*圖：領域包與工作流推薦 — 來源 `assets/08-domain-recommend.svg`*


## 學習目標

- 說明 domain pack 是什麼、video pack 在哪
- 提交自由文字 brief 並讀取排序後 DNA 推薦
- 區分「選擇輔助」與「即時媒體生成」

## 敘事大綱（擴寫為完整正文）

1. Pack 解剖：manifest、agents、DNA、corpus
2. Video pack 盤點（114 agents、A–J 原型）
3. Recommend API + UI 面板
4. Scale S1–S5 與 confidence 解讀
5. 啟動前 hitl_confirm_required
6. 推薦後可選跑 viral-hook DNA
7. 殘留：production_ready、未宣稱 live Sora/Veo

## 實作實驗

- [ ] UI：Domains → brief「15s viral TikTok hook」→ 斷言 DNA A 類
- [ ] CLI：scripts/business/recommend_video_workflow.py
- [ ] API：POST recommend-workflow（需認證）

## 主要來源（未驗證前勿臆造）

- `docs/domain-packs.md`
- `docs/add-domain-pack-runbook.md`
- `business/video/`
- `backend/app/domain/workflows/archetype_selector.py`
- `EXECUTABLE_PRODUCT.md`

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
