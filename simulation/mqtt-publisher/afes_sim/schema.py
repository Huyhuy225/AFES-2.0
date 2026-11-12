"""Offline JSON-Schema (Draft-07 subset) validation for AFES v2 telemetry.

The schema artifact ``simulation/test-data/schema/afes_v2_telemetry.schema.json``
is a verbatim copy of the formal schema in docs/TELEMETRY_SCHEMA.md section 8
(a test asserts they stay identical). This module interprets exactly the
keywords used by that artifact. Any other keyword makes ``load_schema`` fail
loudly instead of being silently ignored, so a future contract change cannot
pass unvalidated.

No third-party package is required, which keeps offline tests dependency-free.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

SIMULATION_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA_PATH = SIMULATION_ROOT / "test-data" / "schema" / "afes_v2_telemetry.schema.json"

SUPPORTED_KEYWORDS = frozenset(
    {
        "$schema",
        "title",
        "description",
        "type",
        "required",
        "properties",
        "enum",
        "minimum",
        "maximum",
        "minLength",
        "format",
    }
)
SUPPORTED_FORMATS = frozenset({"uuid", "date-time"})

UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
# RFC 3339 date-time (the definition used by JSON Schema "date-time").
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$"
)


class SchemaError(RuntimeError):
    """The schema artifact uses something this validator does not support."""


class PayloadDecodeError(ValueError):
    """The payload is not strict JSON (e.g. NaN/Infinity or malformed)."""


@dataclass(frozen=True)
class Violation:
    code: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"[{self.code}] {self.path or '<root>'}: {self.message}"


def _reject_constant(token: str) -> Any:
    raise PayloadDecodeError(f"non-finite JSON number {token!r} is not allowed")


def loads_strict(text: str | bytes) -> Any:
    """Parse JSON rejecting NaN/Infinity (not valid JSON per RFC 8259)."""
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    try:
        return json.loads(text, parse_constant=_reject_constant)
    except json.JSONDecodeError as exc:
        raise PayloadDecodeError(f"invalid JSON: {exc}") from exc


def _check_keywords(node: Any, path: str) -> None:
    if not isinstance(node, dict):
        raise SchemaError(f"schema node at {path or '<root>'} must be an object")
    unknown = set(node) - SUPPORTED_KEYWORDS
    if unknown:
        raise SchemaError(f"unsupported schema keyword(s) {sorted(unknown)} at {path or '<root>'}")
    fmt = node.get("format")
    if fmt is not None and fmt not in SUPPORTED_FORMATS:
        raise SchemaError(f"unsupported format {fmt!r} at {path or '<root>'}")
    for name, child in node.get("properties", {}).items():
        _check_keywords(child, f"{path}.{name}" if path else name)


def load_schema(path: str | Path = DEFAULT_SCHEMA_PATH) -> dict[str, Any]:
    schema = loads_strict(Path(path).read_text(encoding="utf-8"))
    _check_keywords(schema, "")
    return schema


def documented_fields(schema: dict[str, Any]) -> dict[str, set[str] | None]:
    """Map each object path ('' for root) to its documented property names."""
    result: dict[str, set[str] | None] = {}

    def walk(node: dict[str, Any], path: str) -> None:
        props = node.get("properties")
        if props is not None:
            result[path] = set(props)
            for name, child in props.items():
                walk(child, f"{path}.{name}" if path else name)

    walk(schema, "")
    return result


# --------------------------------------------------------------------- types
def _is_type(value: Any, json_type: str) -> bool:
    if json_type == "object":
        return isinstance(value, dict)
    if json_type == "array":
        return isinstance(value, list)
    if json_type == "string":
        return isinstance(value, str)
    if json_type == "boolean":
        return isinstance(value, bool)
    if json_type == "null":
        return value is None
    if json_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool) and (
            not isinstance(value, float) or math.isfinite(value)
        )
    if json_type == "integer":
        if isinstance(value, bool):
            return False
        if isinstance(value, int):
            return True
        # Draft-07: a number with a zero fractional part is an integer.
        return isinstance(value, float) and math.isfinite(value) and value.is_integer()
    raise SchemaError(f"unsupported JSON type {json_type!r}")


def _json_equal(a: Any, b: Any) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    return a == b


def _format_ok(value: str, fmt: str) -> bool:
    if fmt == "uuid":
        return bool(UUID_RE.fullmatch(value))
    if fmt == "date-time":
        if not RFC3339_RE.fullmatch(value):
            return False
        try:
            datetime.fromisoformat(value.replace("z", "Z").replace("t", "T"))
        except ValueError:
            return False
        return True
    raise SchemaError(f"unsupported format {fmt!r}")


def validate_against_schema(instance: Any, schema: dict[str, Any], path: str = "") -> list[Violation]:
    """Validate ``instance`` against a schema node; return all violations."""
    violations: list[Violation] = []

    declared = schema.get("type")
    if declared is not None:
        types = declared if isinstance(declared, list) else [declared]
        if not any(_is_type(instance, t) for t in types):
            violations.append(
                Violation("SCHEMA_TYPE", path, f"expected type {declared}, got {type(instance).__name__}")
            )
            return violations  # further keywords are meaningless for the wrong type

    if "enum" in schema and not any(_json_equal(instance, option) for option in schema["enum"]):
        violations.append(Violation("SCHEMA_ENUM", path, f"{instance!r} not in {schema['enum']}"))

    is_number = isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if is_number and "minimum" in schema and instance < schema["minimum"]:
        violations.append(Violation("SCHEMA_MINIMUM", path, f"{instance} < minimum {schema['minimum']}"))
    if is_number and "maximum" in schema and instance > schema["maximum"]:
        violations.append(Violation("SCHEMA_MAXIMUM", path, f"{instance} > maximum {schema['maximum']}"))

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            violations.append(
                Violation("SCHEMA_MIN_LENGTH", path, f"length {len(instance)} < minLength {schema['minLength']}")
            )
        if "format" in schema and not _format_ok(instance, schema["format"]):
            violations.append(Violation("SCHEMA_FORMAT", path, f"{instance!r} is not a valid {schema['format']}"))

    if isinstance(instance, dict):
        for name in schema.get("required", []):
            if name not in instance:
                child_path = f"{path}.{name}" if path else name
                violations.append(Violation("SCHEMA_REQUIRED", child_path, "required property is missing"))
        for name, child_schema in schema.get("properties", {}).items():
            if name in instance:
                child_path = f"{path}.{name}" if path else name
                violations.extend(validate_against_schema(instance[name], child_schema, child_path))

    return violations
