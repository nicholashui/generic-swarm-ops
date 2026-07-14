# Generic Swarm 商業作業系統 - 用戶指南

> 一份全面的實務指南，涵蓋部署、運營及優化 Generic Swarm 多代理商業作業系統。

**版本：** 2.1（研究整合版）
**最後更新：** 2026 年 7 月

---

## 關於本指南

本用戶指南分為五個循序漸進的章節。每個章節建基於前一章節的知識，帶領你從初始安裝到進階自訂及生產規模的優化。

**系統設計優先順序**（嚴格排列）：

1. 安全性
2. 可審計性
3. 正確性
4. 效率
5. 自主性

> **提示：** 如果你是 Generic Swarm Ops 的新手，請從第一節開始，按順序完成每一章。有經驗的操作員可以直接跳到最相關的章節。

---

## 目錄

### 第一節：核心系統基礎

初學者級別內容，涵蓋系統架構、安裝、首次設定、配置及基本導航。

| 章節 | 標題 | 描述 |
|---------|-------|-------------|
| [01-01](chapters/01-01-system-overview.md) | 系統概覽 | 六層架構、設計優先順序、核心概念 |
| [01-02](chapters/01-02-installation-prerequisites.md) | 安裝先決條件 | Node.js、Python、PostgreSQL、pnpm、Git 設定 |
| [01-03](chapters/01-03-initial-setup-wizard.md) | 初始設定精靈 | Bootstrap、business:init、資料庫、後端/前端啟動 |
| [01-04](chapters/01-04-first-time-configuration.md) | 首次配置 | 種子登入、代理設定、首個 Workflow DNA、驗證 |
| [01-05](chapters/01-05-basic-navigation-account-management.md) | 基本導航及帳戶管理 | 操作控制台導覽、RBAC、會話管理 |

**第一節學習目標：**
- 理解六層架構及設計優先順序
- 在你的平台上安裝所有先決條件
- 完成初始 bootstrap 及資料庫設定
- 配置系統以供首次使用
- 導航操作控制台及管理用戶帳戶

---

### 第二節：中級工作流程

中級內容，涵蓋工作流程實作、業務流程演練、工具整合、流程智能及知識協作。

| 章節 | 標題 | 描述 |
|---------|-------|-------------|
| [02-01](chapters/02-01-workflow-dna-implementation.md) | Workflow DNA 實作 | 從零開始建立有界狀態圖工作流程 |
| [02-02](chapters/02-02-business-process-walkthroughs.md) | 業務流程演練 | 端到端工作流程範例及模式 |
| [02-03](chapters/02-03-tool-adapter-integration.md) | 工具適配器整合 | 建構及配置工具適配器 |
| [02-04](chapters/02-04-process-intelligence-usage.md) | 流程智能使用 | 事件日誌、流程探勘、合規性、瓶頸 |
| [02-05](chapters/02-05-knowledge-memory-collaboration.md) | 知識與記憶協作 | 分層檢索、記憶類型、來源追蹤 |

**第二節學習目標：**
- 實作生產就緒的 Workflow DNA 定義
- 完成完整的業務流程範例演練
- 整合具有適當效果追蹤的工具適配器
- 使用流程智能發現真實運營工作流程
- 管理分層知識檢索及協作系統

---

### 第三節：進階自訂

進階內容，涵蓋領域套件開發、API 整合、進階工作流程自動化、RBAC 治理及多領域部署。

| 章節 | 標題 | 描述 |
|---------|-------|-------------|
| [03-01](chapters/03-01-custom-domain-pack-development.md) | 自訂領域套件開發 | 多領域擴展、清單結構、清單閘門 |
| [03-02](chapters/03-02-api-integration-extension.md) | API 整合與擴展 | 透過 REST API 建立整合 |
| [03-03](chapters/03-03-advanced-workflow-automation.md) | 進階工作流程自動化 | 演化沙箱、變體生成、金絲雀部署 |
| [03-04](chapters/03-04-rbac-governance-configuration.md) | RBAC 與治理配置 | 風險分層、審批策略、合規框架 |
| [03-05](chapters/03-05-multi-domain-white-labeling.md) | 多領域與白標部署 | 領域隔離、白標部署、聯邦 |

**第三節學習目標：**
- 為新業務領域開發並註冊自訂領域套件
- 透過 REST API 整合外部系統
- 配置具有演化沙箱的進階工作流程自動化
- 設定符合企業合規的 RBAC 及治理策略
- 部署具有適當隔離的多領域配置

---

### 第四節：故障排除與支援

故障排除內容，涵蓋常見錯誤解決、診斷工具、系統健康監控及支援資源。

| 章節 | 標題 | 描述 |
|---------|-------|-------------|
| [04-01](chapters/04-01-common-error-resolution.md) | 常見錯誤解決 | Bootstrap、後端、前端、演化錯誤修復 |
| [04-02](chapters/04-02-diagnostic-tools-walkthrough.md) | 診斷工具導覽 | npm run doctor、健康端點、日誌分析 |
| [04-03](chapters/04-03-system-health-monitoring.md) | 系統健康監控 | 指標、告警、儀表板、運行時間追蹤 |
| [04-04](chapters/04-04-support-community-resources.md) | 支援與社區資源 | 文檔、社區、升級路徑 |

**第四節學習目標：**
- 解決所有系統層面的常見運營錯誤
- 使用診斷工具快速識別系統問題
- 透過適當的指標及告警監控系統健康
- 存取支援資源及社區渠道

---

### 第五節：優化與擴展

生產優化內容，涵蓋效能調校、資源分配、大規模部署及安全強化與維護。

| 章節 | 標題 | 描述 |
|---------|-------|-------------|
| [05-01](chapters/05-01-performance-tuning-strategies.md) | 效能調校策略 | 資料庫優化、後端調校、檢索效率 |
| [05-02](chapters/05-02-resource-allocation-optimization.md) | 資源分配與優化 | 評估語料庫預算、記憶保留、Loop Engineering |
| [05-03](chapters/05-03-large-scale-deployment.md) | 大規模部署 | 水平擴展、領域隔離、CI/CD、Docker |
| [05-04](chapters/05-04-security-hardening-maintenance.md) | 安全強化與維護 | OWASP 控制措施、代理安全、長期維護 |

**第五節學習目標：**
- 為生產工作負載調校系統效能
- 管理所有組件的資源分配及預算
- 以水平擴展及領域隔離進行企業級部署
- 實施符合 OWASP LLM Top 10 控制措施的全面安全強化
- 透過歸檔、版本控制及審計維護長期系統健康

---

## 先決條件

在開始本指南之前，請確保你具備：

- 基本的命令列介面操作知識
- 對 REST API 及 JSON 的理解
- 可用的開發機器（Windows、macOS 或 Linux）
- 至少 8 GB RAM 及 20 GB 可用磁碟空間

## 使用慣例

本指南通篇使用以下慣例：

| 慣例 | 含義 |
|------------|---------|
| `等寬字體` | 命令、檔案路徑、程式碼或配置值 |
| **粗體** | 重要術語或界面元素 |
| > **提示：** | 有用的建議及快捷方式 |
| > **警告：** | 如不謹慎遵循可能導致問題的操作 |
| > **注意：** | 額外的上下文或說明 |

## 快速參考

| 資源 | 位置 |
|----------|----------|
| 系統架構 | `structure.md`（倉庫根目錄） |
| 安裝文檔 | `docs/installation.md` |
| 使用參考 | `docs/usage.md` |
| 後端 API | `http://127.0.0.1:8000/api/v1/` |
| 前端控制台 | `http://localhost:3000/` |
| 健康檢查 | `GET /api/v1/health/ready` |
| 業務制品 | `business/` 目錄 |

---

*本指南是 Generic Swarm 商業作業系統文檔套件的一部分。*
*有關架構詳情，請參閱 `structure.md`。有關設計原理，請參閱 `book/design_phase/`。*
