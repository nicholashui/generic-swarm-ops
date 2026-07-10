# Security

Downloaded repositories are untrusted by default. The starter `security` script scans for suspicious scripts, secrets, and overly broad MCP access.

## Business Security Controls

- `npm run business:security` scans business artifacts for obvious secrets
- tool permissions default to least privilege and avoid wildcard scopes
- prompt-injection coverage must include indirect prompt injection scenarios
- high-risk or irreversible workflow steps require explicit human gates
- evolution proposals must remain sandbox-only and retain rollback plans
- self-improvement never rewrites host application code; skill sandbox is promote-gated
- frontend is not authority — backend RBAC, gates, and audit are final

## Runtime controls (shipped)

- PBKDF2 password auth; static tokens smoke-only
- Request IDs, structured error envelopes, rate limits on sensitive routes
- Security headers + CORS on FastAPI
- Tool adapters fail closed; durable `tool_effects` for audit
- Memory scopes + provenance on high-impact writes (poisoning defense)

## Scope

Security controls cover indirect prompt injection, sensitive information disclosure, supply-chain risk, memory poisoning, improper output handling, excessive agency, prompt leakage, vector weaknesses, misinformation, unbounded consumption, tool misuse, and identity abuse.

## Commands

```bash
npm run business:security
npm run business:governance
```
