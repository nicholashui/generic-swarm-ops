# Spec: Full-page document viewer

**Route:** `/app/docs`  
**Permission (typical):** authenticated (app shell)  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Dedicated markdown viewer for static files under public/docs via ?md= path.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- FullPageMarkdownDocument
- Query parameter md=/docs/...

## Backend / API contracts

- No API — static files from Next public/

## Architecture mapping

- Help system per help_spec.md: route-derived docs + full page + drawer

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/docs/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/docs/spec.md`
