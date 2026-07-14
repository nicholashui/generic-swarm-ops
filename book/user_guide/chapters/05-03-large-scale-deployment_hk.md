# 第 5.3 章：大規模部署

![大規模部署架構](../assets/05-03-large-scale-deployment.svg)

## 學習目標

完成本章後，你將能夠：

1. 設計水平擴展的 Generic Swarm Ops 部署架構
2. 設定領域隔離以確保多租戶安全
3. 建立 CI/CD 管道以自動化部署流程
4. 使用 Docker 容器化實現可重複的部署
5. 實施藍綠部署和金絲雀發布策略

## 先決條件

- 完成第 5.1 和 5.2 章（性能調校和資源分配）
- 熟悉 Docker 和容器編排概念
- 理解 CI/CD 管道基礎
- 存取生產或預生產環境

---

## 1. 水平擴展架構

### 1.1 元件擴展策略

| 元件 | 擴展方式 | 考量因素 |
|------|---------|---------|
| FastAPI 後端 | 水平（多實例） | 無狀態設計，共享 PostgreSQL |
| PostgreSQL | 垂直 + 讀取副本 | 主寫/副讀分離 |
| 知識儲存 | 水平（分片） | 按領域分片 |
| 前端 | 水平 + CDN | 靜態資源快取 |
| 演化沙盒 | 隔離實例 | 每個領域獨立 |

### 1.2 負載平衡設定

```nginx
upstream gso_backend {
    least_conn;
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    listen 443 ssl;
    location /api/ {
        proxy_pass http://gso_backend;
        proxy_set_header X-Request-ID $request_id;
    }
}
```

### 1.3 會話親和性

工作流程執行使用 PostgreSQL 進行狀態管理，因此後端實例是無狀態的，不需要會話親和性。

---

## 2. 領域隔離

### 2.1 多租戶架構

```text
Shared Infrastructure:
  - PostgreSQL (schema isolation)
  - FastAPI runtime (namespace isolation)
  - Governance engine (shared)

Per-Domain:
  - business/<domain_id>/ (artifact isolation)
  - Memory scopes (namespace prefix)
  - Tool adapters (domain-specific)
  - Eval corpus (independent)
```

### 2.2 資料隔離

每個領域套件的資料通過命名空間前綴完全隔離：

```sql
-- 每個領域使用獨立的 schema
CREATE SCHEMA domain_legal;
CREATE SCHEMA domain_healthcare;
CREATE SCHEMA domain_ecommerce;
```

### 2.3 網路隔離

在容器化部署中，使用網路政策限制跨領域通訊。

---

## 3. CI/CD 管道

### 3.1 管道階段

```yaml
pipeline:
  stages:
    - name: validate
      steps:
        - npm run doctor
        - npm run business:validate
        - npm run business:security
    - name: test
      steps:
        - backend unit tests
        - frontend lint + typecheck + test
        - business:eval --dry-run
    - name: build
      steps:
        - docker build -t gso-backend .
        - docker build -t gso-frontend ./frontend
    - name: deploy
      steps:
        - deploy to staging
        - run smoke tests
        - deploy to production (manual gate)
```

### 3.2 自動化驗證

每次推送自動執行：

```bash
npm run business:validate
npm run business:security
npm run business:governance
cd backend && python -m unittest discover -s app/tests/unit -p "test_*.py"
cd frontend && pnpm lint && pnpm typecheck && pnpm test
```

---

## 4. Docker 容器化

### 4.1 後端 Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY business/ /business/
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### 4.2 Docker Compose

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:14
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  backend:
    build: .
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@postgres:5432/gso
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    depends_on:
      - backend
    environment:
      NEXT_PUBLIC_API_BASE_URL: http://backend:8000/api/v1
    ports:
      - "3000:3000"

volumes:
  pgdata:
```

---

## 5. 部署策略

### 5.1 藍綠部署

維護兩個相同的生產環境（藍和綠），在它們之間切換流量。

### 5.2 金絲雀發布

先將新版本部署到一小部分使用者，監控指標，然後逐步擴展。

### 5.3 回滾程序

```bash
# 快速回滾到上一個版本
docker tag gso-backend:previous gso-backend:current
docker-compose up -d backend
```

---

## 6. 監控和可觀察性

### 6.1 分散式追蹤

使用 `X-Request-ID` 標頭跨服務追蹤請求。

### 6.2 集中式日誌

將所有服務的日誌聚合到集中式日誌系統（如 ELK 或 Datadog）。

### 6.3 指標收集

監控每個服務實例的健康、延遲和錯誤率。

---

## 7. 實際使用案例

### 使用案例 1：區域部署

**場景：** 需要在多個地理區域部署以滿足資料駐留要求。

**策略：** 每個區域獨立的 PostgreSQL 實例，共享的領域套件定義，區域特定的治理政策。

### 使用案例 2：漸進式遷移

**場景：** 從單體部署遷移到微服務架構。

**策略：** 先容器化現有部署，然後逐步分離元件，最後實現水平擴展。

---

## 8. 最佳實踐

1. **基礎設施即程式碼：** 使用 Terraform 或類似工具管理基礎設施
2. **不可變部署：** 不要修補執行中的容器，重新部署新版本
3. **健康檢查：** 每個服務都必須暴露健康端點
4. **優雅關閉：** 確保服務能夠完成進行中的工作流程再關閉
5. **密鑰管理：** 使用密鑰管理服務，不要在設定中硬編碼
6. **災難恢復：** 定期測試備份恢復程序

---

## 9. 章節摘要

本章涵蓋了 Generic Swarm Ops 的大規模部署：

- **水平擴展：** 無狀態後端設計允許多實例部署
- **領域隔離：** 通過 schema 和命名空間確保多租戶安全
- **CI/CD：** 自動化驗證和部署管道
- **容器化：** Docker 和 Docker Compose 設定
- **部署策略：** 藍綠部署和金絲雀發布
- **監控：** 分散式追蹤、集中式日誌和指標收集
