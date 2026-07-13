# -*- coding: utf-8 -*-
"""Minimal JSON Schema subset validator for Domain Pack Wave 0 (stdlib only)."""
from __future__ import annotations

from typing import Any


class SchemaError(ValueError):
    pass


def _type_ok(value: Any, expected: str | list[str]) -> bool:
    types = [expected] if isinstance(expected, str) else list(expected)
    mapping = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "null": type(None),
    }
    for t in types:
        if t == "number" and isinstance(value, bool):
            continue
        py = mapping.get(t)
        if py and isinstance(value, py):
            return True
    return False


def validate(instance: Any, schema: dict[str, Any], path: str = "$") -> None:
    if "type" in schema:
        t = schema["type"]
        if isinstance(t, list):
            if not any(_type_ok(instance, x) for x in t):
                raise SchemaError(f"{path}: expected type {t}")
        else:
            if not _type_ok(instance, t):
                raise SchemaError(f"{path}: expected type {t}")

    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaError(f"{path}: value not in enum")

    if "minLength" in schema and isinstance(instance, str):
        if len(instance) < schema["minLength"]:
            raise SchemaError(f"{path}: minLength")

    if "minimum" in schema and isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if instance < schema["minimum"]:
            raise SchemaError(f"{path}: minimum")

    if schema.get("type") == "object" or isinstance(instance, dict):
        if not isinstance(instance, dict):
            return
        required = schema.get("required") or []
        for key in required:
            if key not in instance:
                raise SchemaError(f"{path}: missing required '{key}'")
        props = schema.get("properties") or {}
        for key, sub in props.items():
            if key in instance:
                validate(instance[key], sub, f"{path}.{key}")

    if schema.get("type") == "array" or isinstance(instance, list):
        if not isinstance(instance, list):
            return
        if "minItems" in schema and len(instance) < schema["minItems"]:
            raise SchemaError(f"{path}: minItems")
        items = schema.get("items")
        if items:
            if "oneOf" in items:
                for i, el in enumerate(instance):
                    errors = []
                    for branch in items["oneOf"]:
                        try:
                            validate(el, branch, f"{path}[{i}]")
                            break
                        except SchemaError as e:
                            errors.append(str(e))
                    else:
                        raise SchemaError(f"{path}[{i}]: oneOf failed")
            else:
                for i, el in enumerate(instance):
                    validate(el, items, f"{path}[{i}]")
