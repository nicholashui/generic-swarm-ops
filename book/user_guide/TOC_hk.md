# 使用者指南 — 完整目錄（繁體中文）

**產品：** generic-swarm-ops  
**權威目錄：** `book/user_guide/`  
**主檔：** [`user_guide_hk.md`](./user_guide_hk.md)  
**英文目錄：** [`TOC.md`](./TOC.md)  
**章節：** `chapters/*_hk.md`  
**插圖：** [`assets/`](./assets/)（中英共用）

---

## 閱讀地圖

![初學者到專家學習路徑](./assets/01-learning-path.svg)

| 路線 | 建議路徑 |
|------|----------|
| 操作員 | 前言 → 第 I–III 部（至 special skills） |
| 建構者 | 操作員 + DNA + 擴充 |
| 平台 / SRE | 第 I–II 部 + 第 V 部（15–18）+ 附錄 B–C |
| 專家 | 全書 + 附錄 |

---

## 命名慣例

| 英文檔 | 繁中檔 |
|--------|--------|
| `foo.md` | `foo_hk.md` |
| `user_guide.md` | `user_guide_hk.md` |

---

## 章節一覽

| 章 | 標題 | 檔案 | 程度 | SVG | 時間 |
|----|------|------|------|-----|------|
| 00 | 如何使用本指南 | [chapters/00-how-to-use-this-guide_hk.md](./chapters/00-how-to-use-this-guide_hk.md) | 初學者 | 01-learning-path.svg | 15 分鐘 |
| 01 | 什麼是 generic-swarm-ops？ | [chapters/01-what-is-this-system_hk.md](./chapters/01-what-is-this-system_hk.md) | 初學者 | 02-system-overview.svg | 30 分鐘 |
| 02 | 心智模型與分層架構 | [chapters/02-mental-model-and-layers_hk.md](./chapters/02-mental-model-and-layers_hk.md) | 初學者 | 02-system-overview.svg | 40 分鐘 |
| 03 | 安裝與首次開機 | [chapters/03-install-and-first-boot_hk.md](./chapters/03-install-and-first-boot_hk.md) | 初學者 | 03-install-boot.svg | 45–90 分鐘 |
| 04 | 營運主控台導覽 | [chapters/04-ops-console-tour_hk.md](./chapters/04-ops-console-tour_hk.md) | 初學者 | 04-console-map.svg | 30 分鐘 |
| 05 | 第一次工作流執行（E1 路徑） | [chapters/05-first-workflow-run-e1_hk.md](./chapters/05-first-workflow-run-e1_hk.md) | 初學者 → 中級 | 05-e1-operator-path.svg | 60 分鐘 |
| 06 | 核准、風險層級與稽核 | [chapters/06-approvals-risk-audit_hk.md](./chapters/06-approvals-risk-audit_hk.md) | 中級 | 06-governance-gates.svg | 45 分鐘 |
| 07 | 代理、工具與 RBAC | [chapters/07-agents-tools-rbac_hk.md](./chapters/07-agents-tools-rbac_hk.md) | 中級 | 07-agents-tools.svg | 45 分鐘 |
| 08 | 領域包與工作流推薦 | [chapters/08-domain-packs-and-recommend_hk.md](./chapters/08-domain-packs-and-recommend_hk.md) | 中級 | 08-domain-recommend.svg | 60 分鐘 |
| 09 | 特殊技能目錄 | [chapters/09-special-skills-catalog_hk.md](./chapters/09-special-skills-catalog_hk.md) | 中級 | 09-special-skills.svg | 40 分鐘 |
| 10 | 工作流 DNA 深入 | [chapters/10-workflow-dna-deep-dive_hk.md](./chapters/10-workflow-dna-deep-dive_hk.md) | 中級 → 進階 | 10-workflow-dna.svg | 60 分鐘 |
| 11 | 知識與記憶 | [chapters/11-knowledge-and-memory_hk.md](./chapters/11-knowledge-and-memory_hk.md) | 進階 | 11-knowledge-memory.svg | 50 分鐘 |
| 12 | 流程智能（Process intelligence） | [chapters/12-process-intelligence_hk.md](./chapters/12-process-intelligence_hk.md) | 進階 | 12-pi-evolution.svg | 45 分鐘 |
| 13 | 評測與演化沙箱 | [chapters/13-evaluation-and-evolution_hk.md](./chapters/13-evaluation-and-evolution_hk.md) | 進階 | 12-pi-evolution.svg | 60 分鐘 |
| 14 | 自我改進與迴路 | [chapters/14-self-improvement-loops_hk.md](./chapters/14-self-improvement-loops_hk.md) | 進階 | 13-self-improve.svg | 50 分鐘 |
| 15 | 後端 Runtime 與 API | [chapters/15-backend-runtime-and-apis_hk.md](./chapters/15-backend-runtime-and-apis_hk.md) | 專家 | 02-system-overview.svg | 75 分鐘 |
| 16 | 前端深入 | [chapters/16-frontend-deep-dive_hk.md](./chapters/16-frontend-deep-dive_hk.md) | 專家 | 04-console-map.svg | 60 分鐘 |
| 17 | 擴充 DNA、代理與領域包 | [chapters/17-extend-dna-agents-packs_hk.md](./chapters/17-extend-dna-agents-packs_hk.md) | 專家 | 14-extend-pack.svg | 90 分鐘 |
| 18 | 安全、營運與疑難排解 | [chapters/18-security-ops-troubleshooting_hk.md](./chapters/18-security-ops-troubleshooting_hk.md) | 專家 | 15-security-production.svg | 60 分鐘 |
| 19 | 專家劇本與檢查清單 | [chapters/19-expert-playbooks-and-checklists_hk.md](./chapters/19-expert-playbooks-and-checklists_hk.md) | 專家 | 01-learning-path.svg | 40 分鐘+ |

---

## 附錄

| ID | 標題 | 檔案 |
|----|------|------|
| A | 附錄 A — 詞彙表 | [chapters/A-glossary_hk.md](./chapters/A-glossary_hk.md) |
| B | 附錄 B — 命令與 API 速查 | [chapters/B-command-and-api-cheatsheet_hk.md](./chapters/B-command-and-api-cheatsheet_hk.md) |
| C | 附錄 C — 疑難排解矩陣 | [chapters/C-troubleshooting-matrix_hk.md](./chapters/C-troubleshooting-matrix_hk.md) |

---

## 章節數

- 敘事章：**20**（00–19）× 中英  
- 附錄：**3**（A–C）× 中英  
- SVG：**15**（共用）
