# 第 01 章：什麼是 generic-swarm-ops？

> **語言：** 繁體中文（`_hk`）  
> **狀態：** 骨架於 `book/user_guide/` — 請在此擴寫完整內文  
> **程度：** 初學者  
> **部：** 第 I 部 — 基礎  
> **預估時間：** 30 分鐘  
> **路徑：** `book/user_guide/chapters/01-what-is-this-system_hk.md`  
> **英文對照：** [`01-what-is-this-system.md`](./01-what-is-this-system.md)


## 插圖

![什麼是 generic-swarm-ops？](../assets/02-system-overview.svg)

*圖：什麼是 generic-swarm-ops？ — 來源 `assets/02-system-overview.svg`*


## 學習目標

- 用不含行話的一段話說明本系統
- 說出四個平面：主控台、控制平面、業務 OS、領域包
- 陳述 N1 規則：領域邏輯在 pack；主機執行 DNA/工具/閘門

## 敘事大綱（擴寫為完整正文）

1. 問題：多智能體工作缺少稽核、閘門或改進迴路
2. 產品名與雙 harness（Trae + Grok）概覽
3. 四平面圖走讀
4. 核心名詞：agent、tool、DNA workflow、run、approval、lesson、domain pack
5. 今日可跑什麼（E1 + viral-hook）vs 設計願景文件
6. 詞彙表入門（連附錄 A）

## 實作實驗

- [ ] 憑記憶畫出四格圖
- [ ] 列出每次執行都會用到的 5 個名詞

## 主要來源（未驗證前勿臆造）

- `docs/architecture.md`
- `structure.md`
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
