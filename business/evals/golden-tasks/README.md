# Golden Tasks

Store stable business-critical tasks used to detect regressions before promotion.

## Customer onboarding suite

Target: `wf_customer_onboarding_v12` (tier 4).

| Count | Files |
|-------|--------|
| ≥20 | `customer-onboarding-baseline.json` + `customer-onboarding-002.json` … `020.json` |

Each task includes `inputs`, `expected` controls, `success_criteria`, and `provenance`.

Regenerate or extend carefully — sandbox evolution and `npm run business:eval` may load this directory.
