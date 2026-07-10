# Process Intelligence

Event logs drive analytics and durable business artifacts.

## Flow

```text
POST /api/v1/processes/event-logs
  → store event in runtime (Postgres document)
  → recompute discovered processes, conformance, bottlenecks
  → write JSON under business/process-intelligence/
  → upsert pi_artifacts collection
```

## Artifact folders

| Path | Content |
|------|---------|
| `business/process-intelligence/discovered-processes/` | Per-process activity maps |
| `…/conformance-reports/` | Expected vs observed activities |
| `…/bottlenecks/` | Approval waits + activity latency |
| `…/event-logs/` | Reference / ops notes |

## APIs

- `POST/GET /api/v1/processes/event-logs`
- `GET /api/v1/processes/discovered`
- `GET /api/v1/processes/conformance`
- `GET /api/v1/processes/bottlenecks`
- `GET /api/v1/processes/summary`
- `GET /api/v1/processes/artifacts`

## Code

- `backend/app/infrastructure/process_intelligence/artifacts.py`
- Runtime `_refresh_pi_artifacts` on ingest
- Tests: `test_p3_pi_evolution.py`, scorecard event ingest tests
