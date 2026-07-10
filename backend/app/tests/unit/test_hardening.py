import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.core.metrics import RequestMetricsStore
from app.core.rate_limit import InMemoryRateLimiter
from app.runtime import RateLimitedError


class HardeningTests(unittest.TestCase):
    def test_rate_limiter_blocks_after_limit(self):
        current_time = {"value": 0.0}
        limiter = InMemoryRateLimiter(clock=lambda: current_time["value"])

        remaining, reset = limiter.check("client-a", 2, 60)
        self.assertEqual(remaining, 1)
        self.assertEqual(reset, 60)

        remaining, _ = limiter.check("client-a", 2, 60)
        self.assertEqual(remaining, 0)

        with self.assertRaises(RateLimitedError):
            limiter.check("client-a", 2, 60)

        current_time["value"] = 61.0
        remaining, _ = limiter.check("client-a", 2, 60)
        self.assertEqual(remaining, 1)

    def test_metrics_store_aggregates_requests(self):
        store = RequestMetricsStore()
        store.record("GET", "/api/v1/health", 200, 10.0)
        store.record("GET", "/api/v1/health", 500, 30.0)

        snapshot = store.snapshot()
        self.assertEqual(snapshot["request_count"], 2)
        self.assertEqual(snapshot["error_count"], 1)
        self.assertEqual(snapshot["average_duration_ms"], 20.0)
        self.assertEqual(snapshot["routes"][0]["request_count"], 2)
        self.assertEqual(snapshot["routes"][0]["error_count"], 1)


if __name__ == "__main__":
    unittest.main()
