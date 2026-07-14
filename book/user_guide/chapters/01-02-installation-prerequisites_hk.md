# 第 01-02 章：安裝先決條件

![Installation Flow](../assets/01-02-installation-flow.svg)

## 學習目標

在完成本章後，你將能夠：

1. 識別 Generic Swarm 商業作業系統的所有必需及可選依賴項
2. 在你的平台上安裝 Node.js 20+、Python 3.11+、PostgreSQL 14+、pnpm 及 Git
3. 驗證每個先決條件已正確安裝及可存取
4. 理解可選依賴項的角色（Neo4j、pgvector、LLM API）
5. 為開發及生產環境配置系統環境變量
6. 排除 Windows、macOS 及 Linux 上的常見安裝問題

## 先決條件

- 運行 Windows 10+、macOS 12+ 或現代 Linux 發行版的開發機器
- 用於安裝系統套件的管理員/sudo 權限
- 至少 8 GB RAM（建議 16 GB）
- 至少 20 GB 可用磁碟空間
- 穩定的互聯網連接用於下載套件

---

## 1. 必需依賴項概覽

Generic Swarm 商業作業系統需要五個核心依賴項：

| 依賴項 | 最低版本 | 目的 |
|-----------|----------------|---------|
| **Node.js** | 20.0+ | 編排腳本、bootstrap、業務命令 |
| **npm** | 10.0+ | 套件管理（與 Node.js 捆綁） |
| **Python** | 3.11+ | 後端運行時（FastAPI、代理、工具） |
| **PostgreSQL** | 14+ | 主要運行時儲存（JSONB 文件） |
| **pnpm** | 8.0+ | 前端套件管理 |
| **Git** | 2.30+ | 版本控制、倉庫操作 |

> **注意：** 系統使用 Node.js 進行編排腳本（`npm run bootstrap`、`npm run business:*`）及 Python 進行 FastAPI 後端。兩者都是完整安裝所必需的。

---

## 2. 安裝 Node.js 20+

Node.js 為所有編排腳本提供運行時，包括 bootstrap 流程、業務層命令及雙線束同步。

### 2.1 Windows 安裝

```bash
# 選項 A：從官方網站下載
# 訪問 https://nodejs.org/ 並下載 LTS 安裝程式（v20+）

# 選項 B：使用 winget（Windows 套件管理器）
winget install OpenJS.NodeJS.LTS

# 選項 C：使用 Chocolatey
choco install nodejs-lts
```

### 2.2 macOS 安裝

```bash
# 選項 A：使用 Homebrew（推薦）
brew install node@20

# 選項 B：使用 nvm（Node Version Manager）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20
nvm use 20
```

### 2.3 Linux 安裝（Ubuntu/Debian）

```bash
# 使用 NodeSource 倉庫
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 驗證安裝
node --version   # 應顯示 v20.x.x
npm --version    # 應顯示 10.x.x
```

### 2.4 Linux 安裝（Fedora/RHEL）

```bash
# 使用 NodeSource 倉庫
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo dnf install -y nodejs

# 驗證
node --version
npm --version
```

### 2.5 驗證

```bash
# 驗證 Node.js 版本（必須為 20+）
node --version
# 預期：v20.x.x 或更高

# 驗證 npm 版本
npm --version
# 預期：10.x.x 或更高

# 快速功能測試
node -e "console.log('Node.js is working:', process.version)"
```

> **警告：** 不支持低於 20 的 Node.js 版本。編排腳本使用了需要 Node.js 20+ 的功能（如原生 fetch 及 structured clone）。

---

## 3. 安裝 Python 3.11+

Python 驅動整個後端運行時，包括 FastAPI 應用程式、代理執行引擎、工具適配器及所有基礎設施服務。

### 3.1 Windows 安裝

```bash
# 選項 A：從官方網站下載
# 訪問 https://www.python.org/downloads/ 並下載 Python 3.11+

# 選項 B：使用 winget
winget install Python.Python.3.11

# 選項 C：使用 Chocolatey
choco install python --version=3.11
```

> **提示：** 在 Windows 安裝過程中，請在安裝精靈中勾選「Add Python to PATH」及「Install pip」選項。

### 3.2 macOS 安裝

```bash
# 使用 Homebrew（推薦）
brew install python@3.11

# 驗證正確版本是否啟用
python3 --version
# 預期：Python 3.11.x 或更高

# 如果有多個版本，建立別名
alias python=python3.11
```

### 3.3 Linux 安裝（Ubuntu/Debian）

```bash
# 更新套件列表
sudo apt update

# 安裝 Python 3.11 及開發工具
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# 設為預設（如需要）
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# 驗證
python3 --version
# 預期：Python 3.11.x 或更高
```

### 3.4 Linux 安裝（Fedora/RHEL）

```bash
# Fedora（通常預設有 Python 3.11+）
sudo dnf install -y python3.11 python3-pip python3-devel

# 驗證
python3 --version
```

### 3.5 虛擬環境（推薦）

雖然非嚴格必需（後端使用 `pip install -e .`），但使用虛擬環境可保持系統 Python 整潔：

```bash
# 建立虛擬環境
python3 -m venv ~/.venvs/generic-swarm-ops

# 啟用
# Linux/macOS：
source ~/.venvs/generic-swarm-ops/bin/activate
# Windows：
~\.venvs\generic-swarm-ops\Scripts\activate

# 驗證
which python  # 應指向 venv
python --version
```

### 3.6 驗證

```bash
# 檢查版本
python3 --version
# 預期：Python 3.11.x 或更高

# 檢查 pip
pip3 --version
# 預期：pip 23.x 或更高

# 快速功能測試
python3 -c "import sys; print(f'Python {sys.version} is working')"
```

---

## 4. 安裝 PostgreSQL 14+

PostgreSQL 是 Business Orchestrator 的主要運行時儲存。所有工作流程狀態、代理狀態、運行歷史及審計日誌都持久化在使用 JSONB 文件的 `runtime_state` 表中。

### 4.1 Windows 安裝

```bash
# 選項 A：從 https://www.postgresql.org/download/windows/ 下載安裝程式

# 選項 B：使用 Chocolatey
choco install postgresql14

# 選項 C：使用 Docker（推薦用於開發）
docker run --name gso-postgres -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_DB=generic_swarm_ops -p 5432:5432 -d postgres:14
```

### 4.2 macOS 安裝

```bash
# 使用 Homebrew（推薦）
brew install postgresql@14

# 啟動服務
brew services start postgresql@14

# 建立資料庫
createdb generic_swarm_ops

# 驗證連接
psql generic_swarm_ops -c "SELECT version();"
```

### 4.3 Linux 安裝（Ubuntu/Debian）

```bash
# 安裝 PostgreSQL 14
sudo apt update
sudo apt install -y postgresql-14 postgresql-client-14

# 啟動服務
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 建立用戶及資料庫
sudo -u postgres createuser --interactive
# 輸入要添加的角色名稱：your_username
# 新角色是否為超級用戶？y

sudo -u postgres createdb generic_swarm_ops

# 驗證
psql generic_swarm_ops -c "SELECT version();"
```

### 4.4 Linux 安裝（Fedora/RHEL）

```bash
# 安裝 PostgreSQL
sudo dnf install -y postgresql-server postgresql

# 初始化資料庫
sudo postgresql-setup --initdb

# 啟動及啟用
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 建立資料庫
sudo -u postgres createdb generic_swarm_ops
```

### 4.5 Docker 安裝（所有平台）

對於開發環境，Docker 提供最簡單的設定：

```bash
# 拉取並運行 PostgreSQL 14
docker run --name gso-postgres \
  -e POSTGRES_USER=gso_user \
  -e POSTGRES_PASSWORD=gso_password \
  -e POSTGRES_DB=generic_swarm_ops \
  -p 5432:5432 \
  -d postgres:14

# 驗證運行中
docker ps | grep gso-postgres

# 測試連接
psql postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops \
  -c "SELECT 1;"
```

### 4.6 資料庫配置

安裝後，在 `backend/.env` 中配置連接：

```bash
# backend/.env
DATABASE_URL=postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops
```

> **提示：** 有關 Postgres 管理、備份及故障排除的詳細運營指導，請參閱 `backend/docs/postgres-runbook.md`。

### 4.7 驗證

```bash
# 檢查 PostgreSQL 版本
psql --version
# 預期：psql (PostgreSQL) 14.x 或更高

# 測試資料庫連接
psql postgresql://localhost:5432/generic_swarm_ops -c "SELECT current_database();"
# 預期：generic_swarm_ops
```

---

## 5. 安裝 pnpm

pnpm 是 Next.js 前端控制台的套件管理器。對於前端專案，它比 npm 更快且更節省磁碟空間。

### 5.1 使用 Corepack（推薦）

Corepack 與 Node.js 16+ 捆綁，是管理 pnpm 的推薦方式：

```bash
# 啟用 corepack（Linux 上可能需要 sudo）
corepack enable

# 驗證 pnpm 可用
pnpm --version
# 預期：8.x.x 或更高
```

### 5.2 獨立安裝

如果 corepack 不可用或你偏好獨立安裝：

```bash
# 使用 npm
npm install -g pnpm

# 使用 curl（Linux/macOS）
curl -fsSL https://get.pnpm.io/install.sh | sh -

# 使用 PowerShell（Windows）
iwr https://get.pnpm.io/install.ps1 -useb | iex
```

### 5.3 驗證

```bash
# 檢查版本
pnpm --version
# 預期：8.x.x 或更高

# 測試功能
pnpm --help
```

> **注意：** 前端專用 pnpm。不要使用 npm 或 yarn 進行前端依賴管理，因為鎖定檔案格式是 pnpm 特有的。

---

## 6. 安裝 Git

Git 是版本控制、雙線束同步及倉庫操作所必需的。

### 6.1 Windows 安裝

```bash
# 選項 A：從 https://git-scm.com/download/win 下載

# 選項 B：使用 winget
winget install Git.Git

# 選項 C：使用 Chocolatey
choco install git
```

### 6.2 macOS 安裝

```bash
# macOS 透過 Xcode Command Line Tools 包含 Git
xcode-select --install

# 或使用 Homebrew
brew install git
```

### 6.3 Linux 安裝

```bash
# Ubuntu/Debian
sudo apt install -y git

# Fedora/RHEL
sudo dnf install -y git
```

### 6.4 驗證

```bash
# 檢查版本
git --version
# 預期：git version 2.30+ 或更高

# 驗證配置
git config --global user.name
git config --global user.email
```

---

## 7. 可選依賴項

這些依賴項啟用進階功能，但基本操作不需要它們。

### 7.1 Neo4j（圖聯邦）

Neo4j 啟用知識圖聯邦功能，允許多跳實體查詢及關係視覺化。

```bash
# Docker 安裝（推薦）
docker run --name gso-neo4j \
  -e NEO4J_AUTH=neo4j/your_password \
  -p 7474:7474 -p 7687:7687 \
  -d neo4j:5

# 在 backend/.env 中配置
# NEO4J_URI=bolt://localhost:7687
```

**何時安裝：** 僅在你計劃使用具有完整圖聯邦的 Tier 1 知識檢索時才需要（`POST /api/v1/knowledge/graph/federate` 端點）。

### 7.2 pgvector（嵌入搜尋）

pgvector 為 PostgreSQL 添加向量相似性搜尋，在 Tier 0 知識層中啟用語義檢索。

```bash
# 如果使用 Docker PostgreSQL，改用 pgvector 映像：
docker run --name gso-postgres \
  -e POSTGRES_USER=gso_user \
  -e POSTGRES_PASSWORD=gso_password \
  -e POSTGRES_DB=generic_swarm_ops \
  -p 5432:5432 \
  -d pgvector/pgvector:pg14

# 啟用擴展
psql generic_swarm_ops -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

**環境變量：**
```bash
GENERIC_SWARM_PGVECTOR_ENABLED=true
GENERIC_SWARM_EMBEDDINGS_ENABLED=true
```

### 7.3 LLM API 存取（可選評審）

可選的 LLM 評審提供 AI 驅動的工作流程輸出評估：

```bash
# 在環境中啟用評審
GENERIC_SWARM_LLM_CRITIC_ENABLED=true

# 配置你的 LLM API 金鑰（特定於提供商）
# LLM_API_KEY=your_api_key_here
```

**何時安裝：** 僅在你希望在自我改進流程中獲得 AI 驅動的評估反饋時才需要。

---

## 8. 環境變量參考

系統使用的完整環境變量集：

### 8.1 必需變量

| 變量 | 位置 | 值 |
|----------|----------|-------|
| `DATABASE_URL` | `backend/.env` | `postgresql://user:pass@localhost:5432/generic_swarm_ops` |
| `PYTHONPATH` | 後端 shell | `.`（當前目錄） |
| `NEXT_PUBLIC_DEMO_MODE` | 前端 shell | `false`（用於即時操作） |
| `NEXT_PUBLIC_API_BASE_URL` | 前端 shell | `http://127.0.0.1:8000/api/v1` |

### 8.2 可選變量

| 變量 | 預設值 | 目的 |
|----------|---------|---------|
| `GENERIC_SWARM_AUTO_REFLECT` | `true` | 在終端運行時自動反思 |
| `GENERIC_SWARM_LLM_CRITIC_ENABLED` | `false` | 可選的 LLM 評審用於評估 |
| `GENERIC_SWARM_EMBEDDINGS_ENABLED` | `false` | 啟用基於嵌入的檢索 |
| `GENERIC_SWARM_PGVECTOR_ENABLED` | `false` | 啟用 pgvector 擴展 |
| `NEO4J_URI` | （未設定） | 可選的圖聯邦端點 |

> **提示：** `backend/.env.example` 檔案包含所有可用環境變量及其文檔的模板。

---

## 9. 系統需求驗證

### 步驟 1：運行完整的先決條件檢查

安裝所有依賴項後，按順序驗證它們：

```bash
# 1. Node.js
node --version          # 必須 >= 20.0.0
npm --version           # 必須 >= 10.0.0

# 2. Python
python3 --version       # 必須 >= 3.11.0
pip3 --version          # 必須可用

# 3. PostgreSQL
psql --version          # 必須 >= 14.0

# 4. pnpm
pnpm --version          # 必須 >= 8.0.0

# 5. Git
git --version           # 必須 >= 2.30
```

### 步驟 2：驗證資料庫連接

```bash
# 測試 PostgreSQL 連接
psql postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops \
  -c "SELECT current_database(), version();"
```

### 步驟 3：克隆倉庫（如尚未完成）

```bash
# 克隆倉庫
git clone https://github.com/your-org/generic-swarm-ops.git
cd generic-swarm-ops

# 驗證結構
ls structure.md docs/ business/ backend/ frontend/
```

### 步驟 4：運行 Doctor 命令

安裝後，內建的 doctor 命令會檢查你的環境：

```bash
# 運行系統 doctor
npm run doctor
```

此命令驗證所有必需的依賴項已存在且正確配置。

---

## 10. 平台特定注意事項

### 10.1 Windows 注意事項

- 所有命令請使用 PowerShell 或 Windows Terminal（不是 cmd.exe）
- 環境變量使用 `set VARIABLE=value` 設定（無 `export`）
- 路徑分隔符使用反斜杠（`\`），但大多數命令接受正斜杠
- 推薦使用 Docker Desktop 運行 PostgreSQL 及 Neo4j

```bash
# Windows 環境變量語法
set PYTHONPATH=.
set NEXT_PUBLIC_DEMO_MODE=false
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

### 10.2 macOS 注意事項

- 首先安裝 Xcode Command Line Tools：`xcode-select --install`
- Homebrew（`brew`）是推薦的套件管理器
- 透過 Homebrew 安裝的 PostgreSQL 使用 `brew services` 進行生命周期管理
- 如需要，添加 `export PATH="/usr/local/opt/python@3.11/bin:$PATH"`

### 10.3 Linux 注意事項

- 使用你的發行版的套件管理器安裝系統套件
- 考慮使用 Docker 運行資料庫服務以避免版本衝突
- 確保 `python3` 指向 Python 3.11+（如需要使用 `update-alternatives`）
- 服務管理可能需要 `sudo`（`systemctl`）

---

## 11. 真實使用案例

### 使用案例 1：企業開發團隊設定

**場景：** 一個 10 人開發團隊需要在標準化的開發機器（Ubuntu 22.04 工作站）上設定系統。

**方法：**
1. 建立一個透過 apt 及 Docker 安裝所有先決條件的設定腳本
2. 使用 Docker Compose 運行 PostgreSQL 及 Neo4j 服務
3. 在腳本中固定特定版本以實現可重現性
4. 將環境變量儲存在共享的 `.env.example` 模板中

```bash
#!/bin/bash
# team-setup.sh - 企業團隊先決條件安裝
set -e

echo "Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

echo "Installing Python 3.11..."
sudo apt install -y python3.11 python3.11-venv python3-pip

echo "Installing Git..."
sudo apt install -y git

echo "Enabling pnpm via corepack..."
corepack enable

echo "Starting PostgreSQL via Docker..."
docker run --name gso-postgres \
  -e POSTGRES_USER=gso_user \
  -e POSTGRES_PASSWORD=gso_password \
  -e POSTGRES_DB=generic_swarm_ops \
  -p 5432:5432 -d postgres:14

echo "All prerequisites installed. Run 'npm run doctor' to verify."
```

### 使用案例 2：CI/CD 流水線設定

**場景：** 在 CI/CD 流水線（GitHub Actions）中設定先決條件用於自動化測試。

**方法：**
```yaml
# .github/workflows/test.yml 摘錄
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_USER: gso_user
          POSTGRES_PASSWORD: gso_password
          POSTGRES_DB: generic_swarm_ops
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: corepack enable
      - run: npm run bootstrap
```

### 使用案例 3：使用 Docker Compose 進行本地開發

**場景：** 開發者希望以最少的手動設定在本地運行所有服務。

**方法：**
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg14
    environment:
      POSTGRES_USER: gso_user
      POSTGRES_PASSWORD: gso_password
      POSTGRES_DB: generic_swarm_ops
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  neo4j:
    image: neo4j:5
    environment:
      NEO4J_AUTH: neo4j/gso_password
    ports:
      - "7474:7474"
      - "7687:7687"

volumes:
  pgdata:
```

```bash
# 啟動所有服務
docker compose -f docker-compose.dev.yml up -d

# 配置 backend/.env
echo "DATABASE_URL=postgresql://gso_user:gso_password@localhost:5432/generic_swarm_ops" > backend/.env
```

---

## 12. 安裝問題排除

### 常見問題：Node.js 版本過舊

**症狀：** `npm run bootstrap` 因語法錯誤或「unexpected token」訊息而失敗。

**修復：**
```bash
# 檢查版本
node --version
# 如果低於 v20，升級：
nvm install 20 && nvm use 20
# 或從 NodeSource 重新安裝
```

### 常見問題：找不到 Python

**症狀：** `python` 命令找不到，或指向 Python 2.x。

**修復：**
```bash
# 檢查可用版本
which python3
python3 --version

# 如需要建立別名
alias python=python3

# 或使用 update-alternatives（Linux）
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
```

### 常見問題：PostgreSQL 連接被拒

**症狀：** 後端啟動時收到端口 5432「connection refused」錯誤。

**修復：**
```bash
# 檢查 PostgreSQL 是否運行中
sudo systemctl status postgresql
# 或用於 Docker：
docker ps | grep postgres

# 如需要啟動
sudo systemctl start postgresql
# 或：
docker start gso-postgres

# 驗證連接
psql postgresql://localhost:5432/generic_swarm_ops -c "SELECT 1;"
```

### 常見問題：pnpm 無法識別

**症狀：** 安裝後出現 `pnpm: command not found`。

**修復：**
```bash
# 重新啟用 corepack
corepack enable

# 或全域安裝
npm install -g pnpm

# 驗證
pnpm --version
```

### 常見問題：權限被拒

**症狀：** 安裝命令因「EACCES」或「Permission denied」而失敗。

**修復：**
```bash
# 絕不使用 sudo 進行 npm install -g（改為配置 npm 前綴）
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# 添加到 shell 配置檔
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
```

---

## 13. 最佳實踐

1. **使用精確版本** -- 固定 Node.js 及 Python 到特定主版本以避免團隊成員之間的相容性問題。

2. **資料庫使用 Docker** -- 在開發中使用 Docker 運行 PostgreSQL（及可選的 Neo4j）。它避免了版本衝突且清理簡單。

3. **Python 使用虛擬環境** -- 即使後端使用 `pip install -e .`，虛擬環境也能防止污染你的系統 Python。

4. **檢查 `.env.example`** -- `backend/.env.example` 檔案記錄了所有可用的環境變量。將其複製到 `backend/.env` 並自訂。

5. **運行 `npm run doctor`** -- 在任何安裝更改後，運行 doctor 命令以驗證你的環境正確配置。

6. **保持 Git 更新** -- 一些雙線束功能需要 Git 2.30+ 用於 sparse checkout 及其他現代功能。

7. **分配足夠資源** -- 系統需要至少 8 GB RAM。如果在本地同時運行 Docker 容器及應用程式，建議 16 GB。

---

## 14. 章節摘要

在本章中，你學到了：

- 系統需要 Node.js 20+、Python 3.11+、PostgreSQL 14+、pnpm 8+ 及 Git 2.30+
- 每個依賴項可以在 Windows、macOS 及 Linux 上使用特定平台的套件管理器安裝
- PostgreSQL 是主要運行時儲存，Docker 是開發環境的推薦方法
- 可選依賴項（Neo4j、pgvector、LLM API）啟用進階功能但基本操作不需要
- 環境變量控制系統行為，其中 `DATABASE_URL` 及 `NEXT_PUBLIC_DEMO_MODE` 最為關鍵
- `npm run doctor` 命令驗證你的完整安裝
- 常見問題（版本錯誤、連接失敗、權限錯誤）都有上述記錄的直接解決方案

---

## 15. 知識檢查問答

測試你對安裝先決條件的理解：

**問題 1：** 系統所需的最低 Node.js 版本是什麼？

a) Node.js 16
b) Node.js 18
c) Node.js 20
d) Node.js 22

<details>
<summary>答案</summary>
<b>c)</b> Node.js 20+。編排腳本使用了需要此版本的功能。
</details>

---

**問題 2：** 安裝 pnpm 的推薦方式是什麼？

a) npm install -g pnpm
b) corepack enable
c) brew install pnpm
d) apt install pnpm

<details>
<summary>答案</summary>
<b>b)</b> corepack enable。Corepack 與 Node.js 16+ 捆綁，無需全域安裝即可提供對 pnpm 的管理存取。
</details>

---

**問題 3：** Business Orchestrator 使用哪個資料庫表進行狀態儲存？

a) `workflow_state`
b) `runtime_state`
c) `agent_registry`
d) `orchestrator_state`

<details>
<summary>答案</summary>
<b>b)</b> <code>runtime_state</code> 表使用 JSONB 文件儲存所有編排器狀態，並在 <code>backend/data/runtime.json</code> 有 JSON 檔案備份。
</details>

---

**問題 4：** 哪個環境變量控制前端是否連接到即時後端 API？

a) `API_MODE`
b) `NEXT_PUBLIC_DEMO_MODE`
c) `FRONTEND_LIVE`
d) `GSO_LIVE_API`

<details>
<summary>答案</summary>
<b>b)</b> <code>NEXT_PUBLIC_DEMO_MODE=false</code> 將前端設為操作模式，連接到由 <code>NEXT_PUBLIC_API_BASE_URL</code> 指定的即時後端 API。
</details>

---

**問題 5：** 何時需要 Neo4j？

a) 始終需要 -- 它是核心依賴項
b) 僅用於具有完整圖聯邦的 Tier 1 知識檢索
c) 僅用於前端控制台
d) 僅用於運行評估

<details>
<summary>答案</summary>
<b>b)</b> Neo4j 是可選的，僅在需要具有完整圖聯邦的 Tier 1 知識檢索時才需要（<code>POST /api/v1/knowledge/graph/federate</code> 端點）。系統在沒有它的情況下使用 K1-lite 圖操作符正常運作。
</details>

---

**問題 6：** 什麼命令驗證所有先決條件已正確安裝？

a) `npm run verify`
b) `npm run check`
c) `npm run doctor`
d) `npm run test`

<details>
<summary>答案</summary>
<b>c)</b> <code>npm run doctor</code> 驗證所有必需的依賴項已存在且正確配置。
</details>

---

**問題 7：** 開發中 PostgreSQL 的推薦方法是什麼？

a) 透過套件管理器原生安裝
b) 使用託管雲端服務
c) 使用 Docker
d) 改用 SQLite

<details>
<summary>答案</summary>
<b>c)</b> Docker 是推薦用於開發的方法，因為它避免了版本衝突、清理簡單，並且能輕鬆使用如 pgvector 的擴展。
</details>

---

## 下一章

繼續閱讀[第 01-03 章：初始設定精靈](01-03-initial-setup-wizard.md)以完成完整的 bootstrap 及啟動流程。
