# Spec: Security settings

**Route:** `/app/settings/security`  
**Permission (typical):** settings:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Session, MFA posture, allowed domains, and security controls summary.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Security configuration panels

## Backend / API contracts

- Security policies + OWASP LLM/agentic controls at runtime
- Auth rate limits on login

## Architecture mapping

- Security layer: tool broker, memory-poisoning defense, skill vetting
- Blast-radius control over pure prompt trust

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/settings/security/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/settings/security/spec.md`
