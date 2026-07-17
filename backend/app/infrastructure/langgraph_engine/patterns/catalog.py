"""Orchestration pattern catalog — LG-05 / LG-11."""

from __future__ import annotations

PATTERN_CATALOG: list[dict] = [
    {
        "id": "pipeline",
        "name": "Pipeline",
        "description": "Linear DNA steps as a StateGraph chain with optional human gates.",
        "config_schema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "id": "supervisor",
        "name": "Supervisor",
        "description": "Supervisor agent handoffs to specialists until done or max_handoffs.",
        "config_schema": {
            "type": "object",
            "properties": {
                "supervisor_agent": {"type": "string"},
                "specialists": {"type": "array", "items": {"type": "string"}},
                "max_handoffs": {"type": "integer", "minimum": 1, "maximum": 64, "default": 12},
            },
            "required": ["supervisor_agent", "specialists"],
        },
    },
    {
        "id": "router",
        "name": "Router",
        "description": "Classify then branch to specialist paths (MVP maps to pipeline).",
        "config_schema": {"type": "object", "properties": {"routes": {"type": "object"}}, "additionalProperties": True},
    },
    {
        "id": "critique",
        "name": "Critique loop",
        "description": "Produce → critique → revise/accept with max iterations (MVP maps to pipeline).",
        "config_schema": {"type": "object", "properties": {"max_iterations": {"type": "integer", "default": 3}}},
    },
    {
        "id": "map_reduce",
        "name": "Map-reduce",
        "description": "Fan-out over list items then join (MVP maps to pipeline).",
        "config_schema": {"type": "object", "properties": {"items_key": {"type": "string", "default": "items"}}},
    },
    {
        "id": "pack_spine",
        "name": "Pack spine",
        "description": "Domain pack entry spine — uses DNA steps with pack agents.",
        "config_schema": {"type": "object", "properties": {"entry_agent": {"type": "string"}}, "additionalProperties": True},
    },
]


def get_pattern(pattern_id: str) -> dict | None:
    for item in PATTERN_CATALOG:
        if item["id"] == pattern_id:
            return item
    return None
