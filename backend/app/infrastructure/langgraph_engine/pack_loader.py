"""Load domain pack graph JSON packages — LG-10."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_BUSINESS_ROOT = Path(__file__).resolve().parents[4] / "business"


@lru_cache(maxsize=32)
def _list_graph_files(domain_id: str) -> tuple[str, ...]:
    root = _BUSINESS_ROOT / domain_id / "graphs"
    if not root.is_dir():
        return ()
    return tuple(str(p) for p in sorted(root.glob("*.graph.json")))


def load_pack_graph(domain_id: str, graph_id: str | None = None) -> dict[str, Any] | None:
    """Load a pack graph by id, or first graph in domain if id omitted."""
    paths = _list_graph_files(domain_id)
    if not paths:
        return None
    for path in paths:
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(data, dict):
            continue
        gid = data.get("id") or Path(path).stem
        data["id"] = gid
        data["domain_id"] = domain_id
        data["path"] = path
        if graph_id is None or gid == graph_id or Path(path).stem == graph_id:
            return data
    return None


def list_pack_graphs(domain_id: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for path in _list_graph_files(domain_id):
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if isinstance(data, dict):
            out.append(
                {
                    "id": data.get("id") or Path(path).stem,
                    "name": data.get("name") or data.get("id") or Path(path).stem,
                    "pattern": (data.get("orchestration") or {}).get("pattern"),
                    "domain_id": domain_id,
                }
            )
    return out
