from __future__ import annotations

import json
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("generic-swarm-ops-backend")


def log_api_request(
    request_id: str,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    client_ip: str,
) -> None:
    logger.info(
        json.dumps(
            {
                "request_id": request_id,
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration_ms": round(duration_ms, 2),
                "client_ip": client_ip,
            },
            sort_keys=True,
        )
    )


def log_exception(request_id: str | None, method: str, path: str, message: str) -> None:
    logger.error(
        json.dumps(
            {
                "request_id": request_id,
                "method": method,
                "path": path,
                "message": message,
            },
            sort_keys=True,
        )
    )
