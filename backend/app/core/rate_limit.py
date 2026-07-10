from __future__ import annotations

from collections import defaultdict, deque
from threading import RLock
from time import monotonic
from typing import Callable

from fastapi import Request, Response

from app.runtime import RateLimitedError


class InMemoryRateLimiter:
    def __init__(self, clock: Callable[[], float] | None = None) -> None:
        self._clock = clock or monotonic
        self._lock = RLock()
        self._events: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str, limit: int, window_seconds: int) -> tuple[int, int]:
        now = self._clock()
        with self._lock:
            events = self._events[key]
            while events and now - events[0] >= window_seconds:
                events.popleft()
            if len(events) >= limit:
                retry_after = max(1, int(window_seconds - (now - events[0])))
                raise RateLimitedError(f"Rate limit exceeded for {key}", retry_after=retry_after)
            events.append(now)
            remaining = max(limit - len(events), 0)
            reset = window_seconds if not events else max(0, int(window_seconds - (now - events[0])))
            return remaining, reset


rate_limiter = InMemoryRateLimiter()


def _client_identifier(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def build_rate_limit_dependency(limit: int, window_seconds: int, scope: str):
    def dependency(request: Request, response: Response) -> None:
        key = f"{scope}:{_client_identifier(request)}"
        remaining, reset = rate_limiter.check(key, limit, window_seconds)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset)

    return dependency


def rate_limit_hint(limit: int = 120, window_seconds: int = 60) -> dict[str, int]:
    return {"requests": limit, "window_seconds": window_seconds}
