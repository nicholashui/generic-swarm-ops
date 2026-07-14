# 第 17 章：擴充 DNA、代理與領域包

> **語言：** 繁體中文（`_hk`）  
> **狀態：** 骨架於 `book/user_guide/` — 請在此擴寫完整內文  
> **程度：** 專家  
> **部：** 第 V 部 — 專家與生產  
> **預估時間：** 90 分鐘  
> **路徑：** `book/user_guide/chapters/17-extend-dna-agents-packs_hk.md`  
> **英文對照：** [`17-extend-dna-agents-packs.md`](./17-extend-dna-agents-packs.md)


## 插圖

![擴充 DNA、代理與領域包](../assets/14-extend-pack.svg)

*圖：擴充 DNA、代理與領域包 — 來源 `assets/14-extend-pack.svg`*


## 學習目標

- 搭建最小 domain pack 或 DNA 擴充
- 正確註冊工具與 agent allow-list
- 以 golden task + inventory 證明

## 敘事大綱（擴寫為完整正文）

1. 何時擴 pack vs host
2. Manifest 與版本矩陣
3. Agent JSON + DNA 撰寫步驟
4. Tool adapter stub 模式
5. inventory_check 與 corpus standalone
6. 反模式：第二控制平面、灌水分數

## 實作實驗

- [ ] 研讀 example_education 或 example_research pack
- [ ] 草擬你的 pack 一頁設計
- [ ] 對 video pack 跑 inventory_check 作參考

## 主要來源（未驗證前勿臆造）

- `docs/add-domain-pack-runbook.md`
- `docs/domain-pack-versioning-matrix.md`
- `business/example_education/`
- `scripts/business/`

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
