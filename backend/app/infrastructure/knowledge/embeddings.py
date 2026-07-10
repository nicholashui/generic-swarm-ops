"""Deterministic local embeddings for Tier-0 retrieval (no external model required).

Optional pgvector persistence when GENERIC_SWARM_PGVECTOR_ENABLED=true and Postgres up.
"""
from __future__ import annotations

import hashlib
import math
import re
from typing import Any


def tokenize(text: str) -> list[str]:
    return [t for t in re.split(r"\W+", (text or "").lower()) if len(t) > 2]


def embed_text(text: str, *, dims: int = 64) -> list[float]:
    """Hashing trick embedding — stable, offline, good enough for local ranking demos."""
    vec = [0.0] * dims
    for token in tokenize(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "big") % dims
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vec[idx] += sign
    # L2 normalize
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [round(v / norm, 6) for v in vec]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    return sum(x * y for x, y in zip(a, b))


def rank_by_embedding(query: str, documents: list[dict[str, Any]], *, top_k: int = 20) -> list[tuple[dict[str, Any], float]]:
    q = embed_text(query)
    scored: list[tuple[dict[str, Any], float]] = []
    for doc in documents:
        emb = doc.get("embedding")
        if not emb:
            blob = f"{doc.get('title', '')} {doc.get('content', '')}"
            emb = embed_text(blob)
        score = cosine_similarity(q, emb)
        scored.append((doc, score))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:top_k]


def try_upsert_pgvector(document_id: str, embedding: list[float], settings: Any) -> dict[str, Any]:
    """Best-effort pgvector table write. Never fails the request hard."""
    if not getattr(settings, "pgvector_enabled", False) or not getattr(settings, "use_postgres", False):
        return {"stored": False, "reason": "pgvector_disabled"}
    try:
        from sqlalchemy import text
        from app.infrastructure.database.session import get_engine

        engine = get_engine()
        if engine is None:
            return {"stored": False, "reason": "no_engine"}
        vector_literal = "[" + ",".join(str(float(x)) for x in embedding) + "]"
        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS knowledge_embeddings (
                        document_id TEXT PRIMARY KEY,
                        embedding TEXT NOT NULL,
                        dims INT NOT NULL,
                        updated_at TIMESTAMPTZ DEFAULT NOW()
                    )
                    """
                )
            )
            # Store as JSON text for portability even without vector extension installed
            conn.execute(
                text(
                    """
                    INSERT INTO knowledge_embeddings (document_id, embedding, dims)
                    VALUES (:id, :emb, :dims)
                    ON CONFLICT (document_id) DO UPDATE
                    SET embedding = EXCLUDED.embedding, dims = EXCLUDED.dims, updated_at = NOW()
                    """
                ),
                {"id": document_id, "emb": vector_literal, "dims": len(embedding)},
            )
        return {"stored": True, "backend": "postgres_table", "dims": len(embedding)}
    except Exception as exc:  # noqa: BLE001
        return {"stored": False, "reason": str(exc)}
