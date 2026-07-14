# 第 09 章：特殊技能目錄

> **語言：** 繁體中文（`_hk`）  
> **狀態：** 骨架於 `book/user_guide/` — 請在此擴寫完整內文  
> **程度：** 中級  
> **部：** 第 III 部 — 領域與 video pack  
> **預估時間：** 40 分鐘  
> **路徑：** `book/user_guide/chapters/09-special-skills-catalog_hk.md`  
> **英文對照：** [`09-special-skills-catalog.md`](./09-special-skills-catalog.md)


## 插圖

![特殊技能目錄](../assets/09-special-skills.svg)

*圖：特殊技能目錄 — 來源 `assets/09-special-skills.svg`*


## 學習目標

- 從真實 REGISTRY 列出 17 個 special skills（非 demo 列）
- 讀取 API/UI 的 status/score 欄位
- 在磁碟找到 integration.json + SKILL.md

## 敘事大綱（擴寫為完整正文）

1. 為何需要 special skills（主機 MVP 綁定 pack 能力）
2. REGISTRY.json 與 skill_count=17
3. API GET /domains/video/special-skills
4. UI SpecialSkillsPanel（demo 關閉）
5. 評分誠實性（嚴格分 vs 灌水 100）
6. mvp_integrated vs 生產 canary

## 實作實驗

- [ ] 打開 Domains 技能表；列數 = 17
- [ ] 選一個 skill_id；打開 business/video/special_skills/<id>/
- [ ] 以 token 呼叫 GET special-skills 比對 ids

## 主要來源（未驗證前勿臆造）

- `business/video/special_skills/REGISTRY.json`
- `special_skill_impl_score.md`
- `backend/app/runtime.py list_video_special_skills`

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
