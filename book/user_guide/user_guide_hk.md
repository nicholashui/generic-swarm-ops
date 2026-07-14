# Generic Swarm Ops — 使用者指南（繁體中文）

**初學者 → 專家。** 逐步深入理解並操作本系統。

| | |
|--|--|
| **位置** | `book/user_guide/`（權威目錄） |
| **章節** | [`chapters/*_hk.md`](./chapters/) |
| **插圖** | [`assets/`](./assets/)（中英共用） |
| **完整目錄** | [`TOC_hk.md`](./TOC_hk.md) |
| **英文版** | [`user_guide.md`](./user_guide.md) |
| **撰寫計畫** | [`../../planning/user_guide/00_PLAN.md`](../../planning/user_guide/00_PLAN.md) |
| **設計專書** | [`../design_phase/`](../design_phase/) |

> **範圍誠實聲明：** 已驗證路徑包含 E1 操作員流程，以及 video pack 的 recommend／viral-hook DNA（stub）。即時媒體供應商與完整 studio **不在宣稱範圍** — 見 `EXECUTABLE_PRODUCT.md`。

---

## 語言與命名慣例

| 英文 | 繁中 |
|------|------|
| `*.md` | `*_hk.md` |
| `user_guide.md` | `user_guide_hk.md` |
| `TOC.md` | `TOC_hk.md` |
| `chapters/00-….md` | `chapters/00-…_hk.md` |

產品識別碼、API 路徑、檔名、`dna_id` **維持英文**，僅敘事與標題翻譯。

---

## 學習路徑

![初學者到專家學習路徑](./assets/01-learning-path.svg)

| 路線 | 由此開始 |
|------|----------|
| **操作員** | [00](./chapters/00-how-to-use-this-guide_hk.md) → 第 I–III 部 |
| **建構者** | 操作員路徑 + [10 DNA](./chapters/10-workflow-dna-deep-dive_hk.md) + [17 擴充](./chapters/17-extend-dna-agents-packs_hk.md) |
| **平台 / SRE** | 第 I–II 部 + [15 後端](./chapters/15-backend-runtime-and-apis_hk.md)–[18 安全](./chapters/18-security-ops-troubleshooting_hk.md) |
| **專家** | 全部章節 + 附錄 |

---

## 前言

- [00 — 如何使用本指南](./chapters/00-how-to-use-this-guide_hk.md)

## 第 I 部 — 基礎（初學者）

- [01 — 什麼是 generic-swarm-ops？](./chapters/01-what-is-this-system_hk.md)
- [02 — 心智模型與分層架構](./chapters/02-mental-model-and-layers_hk.md)
- [03 — 安裝與首次開機](./chapters/03-install-and-first-boot_hk.md)
- [04 — 營運主控台導覽](./chapters/04-ops-console-tour_hk.md)

## 第 II 部 — 操作核心

- [05 — 第一次工作流執行（E1 路徑）](./chapters/05-first-workflow-run-e1_hk.md)
- [06 — 核准、風險層級與稽核](./chapters/06-approvals-risk-audit_hk.md)
- [07 — 代理、工具與 RBAC](./chapters/07-agents-tools-rbac_hk.md)

## 第 III 部 — 領域與 video pack

- [08 — 領域包與工作流推薦](./chapters/08-domain-packs-and-recommend_hk.md)
- [09 — 特殊技能目錄](./chapters/09-special-skills-catalog_hk.md)
- [10 — 工作流 DNA 深入](./chapters/10-workflow-dna-deep-dive_hk.md)

## 第 IV 部 — 智能與改進

- [11 — 知識與記憶](./chapters/11-knowledge-and-memory_hk.md)
- [12 — 流程智能](./chapters/12-process-intelligence_hk.md)
- [13 — 評測與演化沙箱](./chapters/13-evaluation-and-evolution_hk.md)
- [14 — 自我改進與迴路](./chapters/14-self-improvement-loops_hk.md)

## 第 V 部 — 專家與生產

- [15 — 後端 Runtime 與 API](./chapters/15-backend-runtime-and-apis_hk.md)
- [16 — 前端深入](./chapters/16-frontend-deep-dive_hk.md)
- [17 — 擴充 DNA、代理與領域包](./chapters/17-extend-dna-agents-packs_hk.md)
- [18 — 安全、營運與疑難排解](./chapters/18-security-ops-troubleshooting_hk.md)
- [19 — 專家劇本與檢查清單](./chapters/19-expert-playbooks-and-checklists_hk.md)

## 附錄

- [A — 詞彙表](./chapters/A-glossary_hk.md)
- [B — 命令與 API 速查](./chapters/B-command-and-api-cheatsheet_hk.md)
- [C — 疑難排解矩陣](./chapters/C-troubleshooting-matrix_hk.md)

---

## 系統一覽

![系統總覽](./assets/02-system-overview.svg)

---

## 維護方式

1. **權威使用者指南** = `book/user_guide/`。
2. 每個英文 `*.md` 必須有對應繁中 `*_hk.md`。
3. 擴寫正文時中英同步更新；識別碼不翻譯。
4. 插圖共用 `assets/`（不複製成 `_hk.svg`）。
