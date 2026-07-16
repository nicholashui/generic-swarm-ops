# Spec: Indexed documents

**Route:** `/app/knowledge/documents`  
**Permission (typical):** knowledge:read  
**Sources:** `structure.md`, `backend.md`, `frontend.md`, `help_spec.md`, as-built console under `frontend/src`

## Purpose

Document corpus used for grounded retrieval.

## Design priorities

```text
Safety > Auditability > Correctness > Efficiency > Autonomy
```

Autonomy is earned with evaluation evidence. Evolution must not mutate production DNA directly.

## UI surface

- Document table (title, source, status, updated)
- Detail view for a single document

## Backend / API contracts

- Document index entries from knowledge service
- Chunking and embeddings when enabled

## Architecture mapping

- Chunked content supports tier-0 retrieval; provenance links back to sources

## Non-goals

- Frontend must not embed core orchestration logic, raw DB access, or unconstrained tool execution.
- Help markdown here is documentation only; it does not change runtime policy.

## Related paths

- User guide: `/docs/app/knowledge/documents/user_guide.md`
- Full-page view: `/app/docs?md=/docs/app/knowledge/documents/spec.md`
