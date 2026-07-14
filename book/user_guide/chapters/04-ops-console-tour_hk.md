# 第 04 章：營運主控台導覽

> **語言：** 繁體中文（`_hk`）  
> **狀態：** 骨架於 `book/user_guide/` — 請在此擴寫完整內文  
> **程度：** 初學者  
> **部：** 第 I 部 — 基礎  
> **預估時間：** 30 分鐘  
> **路徑：** `book/user_guide/chapters/04-ops-console-tour_hk.md`  
> **英文對照：** [`04-ops-console-tour.md`](./04-ops-console-tour.md)


## 插圖

![營運主控台導覽](../assets/04-console-map.svg)

*圖：營運主控台導覽 — 來源 `assets/04-console-map.svg`*


## 學習目標

- 走完側欄每一組且無死路
- 打開 Domains 並認出 recommend 與 special skills 面板
- 知道稽核日誌與 API 金鑰位置

## 敘事大綱（擴寫為完整正文）

1. 側欄分組：Main、Data、Quality、Security、Admin
2. 路由表：appPaths
3. Domains 頁面面板
4. 權限閘控項目
5. 命令面板 / 行動版導覽
6. Demo vs live 的 UI 線索

## 實作實驗

- [ ] 點開 Main 每個項目並記錄空狀態
- [ ] 打開 /app/domains 並找到 recommend-workflow-panel

## 主要來源（未驗證前勿臆造）

- `frontend/src/types/navigation.ts`
- `frontend/src/lib/routes/paths.ts`
- `frontend/src/app/app/[...slug]/page.tsx`

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
