---
kind: configuration_system
name: Environment-driven Settings via Pydantic-style Dataclass
category: configuration_system
scope:
    - '**'
source_files:
    - backend/app/core/config.py
    - backend/.env.example
    - backend/app/main.py
    - frontend/.env.example
    - frontend/next.config.ts
---

The repository uses a minimal, environment-variable-driven configuration system with no external config library (no pydantic-settings, python-decouple, or YAML/JSON config files consumed at runtime).

**Backend (FastAPI)**
- Single source of truth: `backend/app/core/config.py` defines a frozen dataclass `Settings` whose fields are populated from `os.getenv(...)` with explicit defaults. A module-level `settings = Settings()` is the singleton imported by the app.
- `.env` loading: `dotenv.load_dotenv(backend/.env, override=False)` is invoked at import time so local development can supply values without touching process env. The file is intentionally not committed; `backend/.env.example` documents every supported variable.
- Key variables include `GENERIC_SWARM_*` toggles (app name, API prefix, rate limits, self-improvement flags, LLM critic, embeddings/pgvector), plus standard `DATABASE_URL`, `NEO4J_URI`, and OpenAI-compatible keys (`OPENAI_API_KEY` / `OPENAI_API_BASE`). A helper `sync_database_url` coerces async SQLAlchemy URLs to sync drivers for the in-process RuntimeStore.
- The FastAPI app object in `backend/app/main.py` reads `settings.app_name`, `settings.api_prefix`, and `settings.cors_allowed_origins` at startup to wire CORS and router prefixes.
- `backend/data/runtime.json` is **not** a configuration file — it is the persistent JSON-backed store used when `GENERIC_SWARM_FORCE_JSON_STORE=true` or no `DATABASE_URL` is set.

**Frontend (Next.js)**
- No dedicated config loader; Next.js build-time env vars prefixed `NEXT_PUBLIC_` are injected into the client bundle. `frontend/.env.example` documents `NEXT_PUBLIC_APP_NAME`, `NEXT_PUBLIC_APP_ENV`, `NEXT_PUBLIC_API_BASE_URL`, `NEXT_PUBLIC_DEMO_MODE`, and feature toggles for registration/billing/SSO.
- `next.config.ts` is currently empty (no custom config). All runtime behavior is driven by those `NEXT_PUBLIC_*` variables consumed directly in components/pages.

**Conventions & Rules**
- Every new setting must be added as a typed field on `Settings` with an `os.getenv(...)` default; never read `os.environ` directly elsewhere.
- Secrets go only in process env or `backend/.env`; never commit secrets or `runtime.json`.
- Frontend-only toggles use the `NEXT_PUBLIC_` prefix so they are baked into the static bundle at build time.
- There is no hierarchical merging (no per-environment files, no secret managers, no hot-reload); changing settings requires a restart.