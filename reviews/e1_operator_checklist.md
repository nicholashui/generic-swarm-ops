# E1 operator checklist (executed)

**Date:** 2026-07-09  
**Mode:** Automated API/ASGI path (equivalent to demo-off backend ops)

## Result: PASS

| Step | Result |
|------|--------|
| Health ready | `200`, `database: postgres` |
| Login | `admin@example.com` / password → token |
| Live lists | workflows, agents, approvals 200 |
| Create agent | 200 |
| Flagship Run now | `wf_customer_onboarding_v12` with `case_id` |
| Human gate | billing step → approve as reviewer |
| Run complete | all steps completed |
| Audit + memory | present |
| Improve pipeline | reflect → propose sandbox → evaluate **passed** → canary **approved_for_canary** |

## Fix applied during E1

- `execution_agent` / `communications_agent` memory scopes unioned with seed (`organization_memory`) so workflow `memory_reads` no longer fail closed mid-run.

## Automated regression

```bash
cd backend
set PYTHONPATH=.
python -m unittest app.tests.e2e.test_e1_operator_path -v
```

## UI / Playwright

```bash
cd frontend
pnpm exec playwright install chromium   # once
pnpm test:e2e                           # API smoke skips if backend down
E2E_START=1 pnpm test:e2e               # starts Next dev for UI smoke
```
