---
kind: dependency_management
name: Per-Project Dependency Manifests with Locked Resolutions
category: dependency_management
scope:
    - '**'
source_files:
    - backend/pyproject.toml
    - backend/.env.example
    - frontend/package.json
    - frontend/pnpm-lock.yaml
    - frontend/pnpm-workspace.yaml
    - package.json
---

This monorepo manages dependencies per project rather than through a top-level workspace. Each language/runtime has its own manifest and lockfile, with no cross-project dependency sharing.

**Python (backend)**
- Declared in `backend/pyproject.toml` using PEP 621 `[project]` fields.
- Runtime deps are pinned with semver ranges (`>=x.y.z,<z.0.0`) for FastAPI, uvicorn, pydantic, SQLAlchemy, psycopg[binary], asyncpg; Python minimum is `>=3.11`.
- Build system uses setuptools (`setuptools.build_meta`). No virtual-environment or lockfile is committed — developers install via `pip install -e backend/` or `uv pip install -e backend/`.
- Optional runtime features (embeddings, pgvector, Neo4j federation) are toggled via environment variables documented in `backend/.env.example`; these packages are not listed as hard dependencies.

**Node.js (frontend + root scripts)**
- Frontend lives in `frontend/` with its own `package.json`, `pnpm-lock.yaml`, and `pnpm-workspace.yaml` (the latter exists but the repo is not configured as a pnpm workspace — only a single importer is present).
- Production deps use caret ranges (`^x.y.z`) while Next.js and React are pinned to exact versions (`16.2.10`, `19.2.4`) to keep the app shell stable.
- Dev-only tooling (Playwright, Vitest, ESLint, Tailwind v4, TypeScript) is isolated under `devDependencies`.
- Root `package.json` declares orchestration scripts (bootstrap, sync, security, business validation) that run Node `.mjs` files from `scripts/`; it pins the required Node engine at `>=20.0.0` via the `engines` field.

**Lockfiles & reproducibility**
- `frontend/pnpm-lock.yaml` (lockfileVersion 9.0) commits exact resolved package trees with integrity hashes, so CI can reproduce installs deterministically.
- The Python side has no committed lockfile; pinning is done via upper-bound constraints in `pyproject.toml` instead of a `requirements.txt` / `poetry.lock` / `uv.lock`.

**No vendoring or private registries**
- There is no `vendor/`, `node_modules/` committed, no `.npmrc`/`.pypirc`/`PIP_INDEX_URL`, and no `GOPRIVATE` or similar registry overrides. All packages resolve directly from PyPI and the npm registry.

**Rules developers should follow**
- Add new Python dependencies only in `backend/pyproject.toml` under `[project].dependencies`; keep upper bounds `<major.0.0` to avoid breaking changes.
- For the frontend, add production deps under `dependencies` and dev-only tooling under `devDependencies`; prefer exact version pins for framework packages (Next.js, React).
- Always commit the updated `frontend/pnpm-lock.yaml` after adding/changing JS dependencies.
- Do not commit any secrets or local env files; configure optional backends (Postgres, pgvector, Neo4j, LLM endpoints) through `backend/.env` following `backend/.env.example`.
- Keep the root `engines.node >=20.0.0` constraint in sync with the CI Node runtime.