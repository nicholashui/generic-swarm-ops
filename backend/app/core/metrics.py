from __future__ import annotations

from collections import defaultdict
from threading import RLock


class RequestMetricsStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._request_count = 0
        self._error_count = 0
        self._total_duration_ms = 0.0
        self._by_route: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "errors": 0, "duration_ms": 0.0})

    def record(self, method: str, path: str, status_code: int, duration_ms: float) -> None:
        key = f"{method} {path}"
        with self._lock:
            self._request_count += 1
            self._total_duration_ms += duration_ms
            route = self._by_route[key]
            route["count"] += 1
            route["duration_ms"] += duration_ms
            if status_code >= 400:
                self._error_count += 1
                route["errors"] += 1

    def snapshot(self) -> dict:
        with self._lock:
            routes = []
            for route, values in sorted(self._by_route.items()):
                count = int(values["count"])
                routes.append(
                    {
                        "route": route,
                        "request_count": count,
                        "error_count": int(values["errors"]),
                        "average_duration_ms": round(values["duration_ms"] / max(count, 1), 2),
                    }
                )
            return {
                "request_count": self._request_count,
                "error_count": self._error_count,
                "average_duration_ms": round(self._total_duration_ms / max(self._request_count, 1), 2),
                "routes": routes,
            }


metrics_store = RequestMetricsStore()
