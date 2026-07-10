"""SQLAlchemy engine/session helpers for Postgres (backend/.env DATABASE_URL)."""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from app.core.config import settings


@lru_cache(maxsize=1)
def get_engine():
    if not settings.use_postgres or not settings.sync_database_url:
        return None
    from sqlalchemy import create_engine

    return create_engine(
        settings.sync_database_url,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_pre_ping=settings.database_pool_pre_ping,
        future=True,
    )


def get_session():
    """Return a sync Session, or None when Postgres is not configured."""
    engine = get_engine()
    if engine is None:
        return None
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return SessionLocal()


def database_status() -> dict[str, Any]:
    engine = get_engine()
    if engine is None:
        return {
            "backend": "json-file",
            "configured": bool(settings.database_url),
            "force_json": settings.force_json_store,
            "reachable": None,
        }
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        return {
            "backend": "postgres",
            "configured": True,
            "force_json": False,
            "reachable": True,
            "pool_size": settings.database_pool_size,
        }
    except Exception as exc:  # noqa: BLE001 — surface health without crashing
        return {
            "backend": "postgres",
            "configured": True,
            "force_json": False,
            "reachable": False,
            "error": str(exc.__class__.__name__),
        }
