from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os


def _load_dotenv() -> None:
    """Load backend/.env if present (does not override existing process env)."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    backend_root = Path(__file__).resolve().parents[2]
    env_path = backend_root / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)


_load_dotenv()


def _cors_origins_from_env() -> list[str]:
    """Parse CORS origins; never return bare '*' when using credentialed browser clients."""
    raw = os.getenv("GENERIC_SWARM_CORS_ALLOWED_ORIGINS", "").strip()
    dev_defaults = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]
    if not raw or raw == "*":
        return dev_defaults
    origins = [part.strip() for part in raw.split(",") if part.strip() and part.strip() != "*"]
    return origins or dev_defaults


def sync_database_url(url: str | None) -> str | None:
    """Convert async SQLAlchemy URLs to a sync driver for RuntimeStore."""
    if not url:
        return None
    # Prefer psycopg3 for sync access from the existing synchronous runtime
    if url.startswith("postgresql+asyncpg://"):
        return "postgresql+psycopg://" + url[len("postgresql+asyncpg://") :]
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://") :]
    if url.startswith("postgresql://") and "+psycopg" not in url and "+asyncpg" not in url:
        return "postgresql+psycopg://" + url[len("postgresql://") :]
    return url


@dataclass(slots=True)
class Settings:
    app_name: str = os.getenv("GENERIC_SWARM_APP_NAME", "generic-swarm-ops-backend")
    api_prefix: str = os.getenv("GENERIC_SWARM_API_PREFIX", "/api/v1")
    environment: str = os.getenv("GENERIC_SWARM_ENV", "development")
    # Explicit origins required when allow_credentials=True (browsers reject ACAO: * + credentials).
    # Override with GENERIC_SWARM_CORS_ALLOWED_ORIGINS=comma,separated,list
    cors_allowed_origins: list[str] = field(
        default_factory=lambda: _cors_origins_from_env()
    )
    rate_limit_enabled: bool = os.getenv("GENERIC_SWARM_RATE_LIMIT_ENABLED", "true").lower() == "true"
    auth_rate_limit_per_minute: int = int(os.getenv("GENERIC_SWARM_AUTH_RATE_LIMIT_PER_MINUTE", "12"))
    workflow_write_rate_limit_per_minute: int = int(
        os.getenv("GENERIC_SWARM_WORKFLOW_WRITE_RATE_LIMIT_PER_MINUTE", "30")
    )
    # Persistence — Postgres from backend/.env (DATABASE_URL)
    database_url: str | None = field(default_factory=lambda: os.getenv("DATABASE_URL"))
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    database_max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "5"))
    database_pool_pre_ping: bool = os.getenv("DATABASE_POOL_PRE_PING", "true").lower() == "true"
    # Force JSON file store even if DATABASE_URL is set (tests / offline)
    force_json_store: bool = os.getenv("GENERIC_SWARM_FORCE_JSON_STORE", "false").lower() == "true"
    # Self-improvement
    auto_reflect: bool = os.getenv("GENERIC_SWARM_AUTO_REFLECT", "true").lower() == "true"
    # Optional LLM critic (HTTP OpenAI-compatible chat completions). Empty = rule-based only.
    llm_critic_enabled: bool = os.getenv("GENERIC_SWARM_LLM_CRITIC_ENABLED", "false").lower() == "true"
    llm_api_base: str | None = field(default_factory=lambda: os.getenv("GENERIC_SWARM_LLM_API_BASE") or os.getenv("OPENAI_API_BASE"))
    llm_api_key: str | None = field(default_factory=lambda: os.getenv("GENERIC_SWARM_LLM_API_KEY") or os.getenv("OPENAI_API_KEY"))
    llm_model: str = os.getenv("GENERIC_SWARM_LLM_MODEL", "gpt-4o-mini")
    # Embeddings / pgvector
    embeddings_enabled: bool = os.getenv("GENERIC_SWARM_EMBEDDINGS_ENABLED", "true").lower() == "true"
    pgvector_enabled: bool = os.getenv("GENERIC_SWARM_PGVECTOR_ENABLED", "false").lower() == "true"
    # Neo4j federation (optional export / bolt)
    neo4j_uri: str | None = field(default_factory=lambda: os.getenv("NEO4J_URI"))
    neo4j_user: str | None = field(default_factory=lambda: os.getenv("NEO4J_USER"))
    neo4j_password: str | None = field(default_factory=lambda: os.getenv("NEO4J_PASSWORD"))

    @property
    def sync_database_url(self) -> str | None:
        return sync_database_url(self.database_url)

    @property
    def use_postgres(self) -> bool:
        return bool(self.sync_database_url) and not self.force_json_store


settings = Settings()
