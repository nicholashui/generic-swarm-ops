---
kind: build_system
name: Monorepo Build & Orchestration (Node/Python, No Containerization)
category: build_system
scope:
    - '**'
source_files:
    - package.json
    - backend/pyproject.toml
    - frontend/package.json
    - frontend/pnpm-workspace.yaml
    - .github/workflows/n3-inventory.yml
    - backend/.env.example
    - scripts/export-openapi.mjs
---

This repository has no containerization or Makefile-based build system. The build surface is a thin Node.js orchestrator at the monorepo root that delegates to per-subsystem toolchains: Python `setuptools` for the FastAPI backend and Next.js + pnpm for the frontend. A single GitHub Actions workflow runs one Python inventory check; there is no CI pipeline that builds, tests, or packages either subsystem.

**What is used**
- **Backend**: PEP 517 via `backend/pyproject.toml` with `setuptools.build_meta`; runtime dependencies pinned in `[project]`. No virtualenv or tox configuration — developers install directly into their environment.
- **Frontend**: Next.js 16 app managed by pnpm (`frontend/package.json`, `pnpm-workspace.yaml`). Scripts wrap `next dev/build/start`, ESLint, TypeScript typecheck, Vitest unit tests, and Playwright e2e tests. An OpenAPI contract is exported from the backend and consumed by the frontend via `scripts/export-openapi.mjs`.
- **Root orchestration**: `package.json` scripts call Node `.mjs` helpers under `scripts/` for bootstrap, source download, sync, security checks, business validation, and review flows. These are the only cross-cutting entry points.
- **CI**: One workflow `.github/workflows/n3-inventory.yml` that checks video-pack inventories on push/PR/dispatch using `actions/setup-python@v5` and `python scripts/business/inventory_check.py`.

**Key files**
- `package.json` — monorepo root scripts (bootstrap, doctor, sources, sync, security, review, business gates, test)
- `backend/pyproject.toml` — backend package metadata, Python ≥3.11 constraint, dependency list, setuptools build backend
- `frontend/package.json` — Next.js scripts, Vitest/Playwright/Eslint/TSC, OpenAPI export/generate pipeline
- `frontend/pnpm-workspace.yaml` — pnpm workspace root (no child workspaces declared here)
- `frontend/vitest.config.ts`, `frontend/playwright.config.ts`, `frontend/eslint.config.mjs` — frontend test/lint runners
- `.github/workflows/n3-inventory.yml` — only CI job (video pack inventory)
- `backend/.env.example` — runtime config surface (Postgres URL, JSON store toggle, optional LLM/pgvector/Neo4j flags)
- `scripts/` — Node orchestration harnesses invoked by root scripts (doctor, sync, security, review, business validation, OpenAPI export, etc.)

**Architecture & conventions**
- **No shared lockfile across subprojects**: each subsystem owns its own manifest (`backend/pyproject.toml`, `frontend/package.json`). There is no top-level `requirements.txt` / `poetry.lock` / `pnpm-lock.yaml` aggregation beyond the frontend's lock.
- **OpenAPI as the integration contract**: the frontend generates typed API clients from `openapi.json`, which is produced by `scripts/export-openapi.mjs` against the running backend. This is the de-facto build-time contract between layers.
- **Scripts-first, not task-runner-first**: instead of a Makefile or Rakefile, the project uses `node --test` for the root suite and per-subsystem runners (pytest/Vitest/Playwright) invoked through npm scripts. Cross-cutting concerns (source download, governance checks, evolution sandbox checks) live in `scripts/*.mjs`.
- **Configuration via env vars**: the backend reads all runtime knobs from `GENERIC_SWARM_*` / `DATABASE_*` / `NEO4J_*` variables documented in `backend/.env.example`; there is no build-time config generation.
- **No Dockerfiles, no docker-compose, no Makefile**: despite design docs referencing them, none exist in this tree. Deployment artifacts are not built here.

**Rules developers should follow**
- Add new backend dependencies only in `backend/pyproject.toml`; do not introduce separate `requirements.txt` files.
- Frontend changes go through `pnpm` inside `frontend/`; use `pnpm api:generate` after backend schema changes to keep the generated client in sync.
- Root-level cross-cutting tasks belong in `scripts/*.mjs` and are exposed via `package.json` scripts — avoid adding ad-hoc shell commands at the repo root.
- Tests: run `node --test` for root Node suites, `pytest` under `backend/app/tests/`, `pnpm test` (Vitest) and `pnpm test:e2e` (Playwright) under `frontend/`. There is no single `make test` target.
- Do not commit secrets; copy `backend/.env.example` to `backend/.env` and fill values locally. CI does not inject secrets.