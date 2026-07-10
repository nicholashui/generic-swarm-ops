# AI / Agent Incident Response Plan

## Scope

GenAI and multi-agent incidents: prompt injection, tool misuse, data leakage, runaway cost,
unsafe autonomy, poisoned memory, and failed rollback.

## Severity

| Level | Description | Response |
|-------|-------------|----------|
| SEV-1 | Active data breach, unrestricted tool access, production mutation without gate | Immediate contain + human war-room |
| SEV-2 | Failed gate bypass attempt, elevated hallucination on high-risk path | Pause workflows, investigate |
| SEV-3 | Single-tenant anomaly, reversible error with audit trail | Standard ticket |

## Containment steps

1. Disable affected workflow (`status=disabled`) and revoke API keys if compromised.
2. Freeze evolution canaries; block promotion.
3. Preserve audit logs and run traces (do not delete evidence).
4. Rotate secrets that may have entered prompts or logs.
5. Notify Incident Commander agent role + human owner.

## Recovery

1. Root-cause note in `business/security/incident-reports/`.
2. Regression/adversarial tests covering the failure mode.
3. Re-enable only after governance sign-off for the risk tier.

## Related

- structure.md §7 Security
- Tool Permission Broker + Memory Steward rules
