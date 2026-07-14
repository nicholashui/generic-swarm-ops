# 第 5.2 章：資源分配與最佳化

![資源分配架構](../assets/05-02-resource-allocation-architecture.svg)

## 學習目標

完成本章後，你將能夠：

1. 設定評估語料庫預算以平衡品質和成本
2. 管理記憶體保留政策以控制儲存增長
3. 設定 Loop Engineering 執行排程和資源限制
4. 平衡 LLM API 使用與本地推理的成本效益
5. 實施智能資源分配以最大化系統價值

## 先決條件

- 完成第 5.1 章（性能調校策略）
- 理解演化沙盒和自我改進管道
- 存取系統設定檔案

---

## 1. 評估語料庫預算

### 1.1 理解評估成本

每次評估執行消耗：
- LLM API 呼叫（按權杖計費）
- 資料庫讀寫操作
- 計算時間

### 1.2 預算設定

```yaml
evaluation:
  daily_budget:
    max_golden_task_runs: 50
    max_regression_runs: 20
    max_adversarial_runs: 10
  weekly_budget:
    full_corpus_runs: 2
    variant_evaluations: 5
```

### 1.3 優先級分配

| 評估類型 | 優先級 | 預算份額 |
|---------|--------|---------|
| 黃金任務 | 最高 | 40% |
| 回歸測試 | 高 | 25% |
| 對抗性測試 | 高 | 20% |
| 歷史重放 | 中 | 15% |

---

## 2. 記憶體保留管理

### 2.1 保留政策

```python
MEMORY_RETENTION_POLICY = {
    "event_memory": {"retention_days": 90, "max_entries": 10000},
    "episodic_memory": {"retention_days": 180, "max_entries": 5000},
    "semantic_memory": {"retention_days": 365, "max_entries": None},
    "decision_memory": {"retention_days": 365, "max_entries": None},
    "evaluation_memory": {"retention_days": 180, "max_entries": 2000},
    "lesson_library": {"retention_days": 90, "max_entries": 500},
}
```

### 2.2 歸檔策略

過期的記憶體項目不會立即刪除，而是移至歸檔儲存以供審計用途。

### 2.3 知識庫增長控制

監控知識庫增長率，當接近儲存限制時觸發歸檔程序。

---

## 3. Loop Engineering 資源管理

### 3.1 Loop 執行排程

```yaml
loop_engineering:
  schedules:
    reflect_loop:
      trigger: "after_workflow_completion"
      max_concurrent: 3
      timeout_seconds: 120
    propose_loop:
      trigger: "daily_02:00"
      max_concurrent: 1
      timeout_seconds: 300
    evaluate_loop:
      trigger: "weekly_sunday_03:00"
      max_concurrent: 2
      timeout_seconds: 3600
```

### 3.2 資源限制

```yaml
resource_limits:
  max_memory_mb: 2048
  max_cpu_percent: 50
  max_concurrent_loops: 5
  max_llm_calls_per_loop: 20
```

### 3.3 優先級佇列

當多個 loop 等待執行時，按照優先級排序：安全相關 > 回歸修正 > 性能改進 > 新功能。

---

## 4. LLM API 成本管理

### 4.1 權杖預算

```python
LLM_BUDGET = {
    "daily_token_limit": 1_000_000,
    "per_workflow_limit": 50_000,
    "per_agent_limit": 10_000,
    "emergency_reserve": 100_000,
}
```

### 4.2 成本最佳化策略

1. **使用適當的模型大小：** 簡單任務使用較小的模型
2. **快取重複查詢：** 對相同輸入避免重複 API 呼叫
3. **批次處理：** 合併多個小請求為一個批次
4. **本地推理：** 對低風險任務考慮使用本地模型

### 4.3 使用量監控

```bash
curl -s -b cookies.txt \
  "http://127.0.0.1:8000/api/v1/metrics/llm-usage" \
  | python -m json.tool
```

---

## 5. 儲存最佳化

### 5.1 資料庫儲存

- 定期執行 VACUUM ANALYZE
- 監控表格大小增長
- 設定自動歸檔觸發器

### 5.2 檔案系統儲存

- 壓縮歸檔的審計日誌
- 定期清理暫時檔案
- 監控 `business/` 目錄大小

---

## 6. 實際使用案例

### 使用案例 1：初創公司資源限制

**場景：** 小團隊需要在有限預算下運作 Generic Swarm Ops。

**策略：** 減少每日評估次數、使用較小的 LLM 模型、延長記憶體保留週期、每週而非每日執行完整評估。

**結果：** 月度 LLM 成本從 $500 降至 $150，同時保持 90% 的評估覆蓋率。

### 使用案例 2：企業規模部署

**場景：** 大型組織部署多個領域套件，需要資源隔離。

**策略：** 每個領域分配獨立的資源配額、設定跨領域的資源共享池、優先級佇列確保關鍵工作流程優先。

**結果：** 5 個領域套件同時運作，零資源衝突，100% SLA 合規。

---

## 7. 最佳實踐

1. **設定預警閾值：** 在達到硬限制之前發出警告
2. **定期審查預算：** 每月檢查資源使用模式
3. **漸進式擴展：** 根據實際需求逐步增加資源
4. **保留緊急儲備：** 為意外情況保留 10-20% 的資源
5. **自動化歸檔：** 使用排程任務自動管理資料生命週期

---

## 8. 章節摘要

本章涵蓋了 Generic Swarm Ops 的資源分配與最佳化：

- **評估語料庫預算：** 按優先級分配每日和每週的評估資源
- **記憶體保留：** 設定保留政策和歸檔策略
- **Loop Engineering：** 排程設定和資源限制
- **LLM 成本：** 權杖預算、成本最佳化和使用量監控
- **儲存最佳化：** 資料庫和檔案系統的管理策略
