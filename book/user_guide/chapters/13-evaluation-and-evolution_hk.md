# 第 13 章：評測與演化沙箱

> **語言：** 繁體中文（`_hk`）  
> **狀態：** 骨架於 `book/user_guide/` — 請在此擴寫完整內文  
> **程度：** 進階  
> **部：** 第 IV 部 — 智能與改進  
> **預估時間：** 60 分鐘  
> **路徑：** `book/user_guide/chapters/13-evaluation-and-evolution_hk.md`  
> **英文對照：** [`13-evaluation-and-evolution.md`](./13-evaluation-and-evolution.md)


## 插圖

![評測與演化沙箱](../assets/12-pi-evolution.svg)

*圖：評測與演化沙箱 — 來源 `assets/12-pi-evolution.svg`*


## 學習目標

- 解讀 golden/regression/adversarial 評測
- 使用 Evolution 檔案庫 UI
- 陳述 promote 規則與回滾期望

## 敘事大綱（擴寫為完整正文）

1. business/evals/ 語料配置
2. Fitness 與 archive
3. UI /app/evolution
4. Canary 與版本化 DNA
5. npm run business:eval 與 evolution:check
6. 禁止：就地改 production DNA

## 實作實驗

- [ ] 打開 Evolution archive
- [ ] 列出 golden tasks 數量（產品門檻 ≥20）
- [ ] 追蹤一份 successful variant JSON（若有）

## 主要來源（未驗證前勿臆造）

- `docs/evaluation.md`
- `docs/evolution-sandbox.md`
- `business/evals/`
- `business/evolution/`

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
