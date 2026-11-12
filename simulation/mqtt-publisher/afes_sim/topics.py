"""AFES v2 MQTT topic construction for Stage A virtual telemetry.

Only the device telemetry channel from docs/TELEMETRY_SCHEMA.md section 2 is
produced by this simulator:

    afes/v2/{tenant_id}/devices/{device_id}/telemetry   (QoS 1, not retained)
"""

from __future__ import annotations

import re

TOPIC_ROOT = "afes/v2"
TELEMETRY_TOPIC_TEMPLATE = TOPIC_ROOT + "/{tenant_id}/devices/{device_id}/telemetry"
TELEMETRY_QOS = 1
TELEMETRY_RETAIN = False

# Identifier segments must be a single, literal MQTT topic level: no "/", no
# wildcards ("+", "#"), no whitespace or control characters, no leading "$".
TOPIC_SEGMENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_TELEMETRY_TOPIC_RE = re.compile(
    r"^afes/v2/(?P<tenant_id>[^/+#]+)/devices/(?P<device_id>[^/+#]+)/telemetry$"
)


class TopicError(ValueError):
    """Raised when a topic or topic segment violates the AFES v2 hierarchy."""


def validate_segment(name: str, value: object) -> str:
    if not isinstance(value, str) or not TOPIC_SEGMENT_RE.fullmatch(value):
        raise TopicError(
            f"{name} must be 1-64 chars of [A-Za-z0-9._-], starting alphanumeric, "
            f"with no MQTT separators or wildcards; got {value!r}"
        )
    return value


def telemetry_topic(tenant_id: str, device_id: str) -> str:
    """Build the approved device telemetry topic for one virtual node."""
    validate_segment("tenant_id", tenant_id)
    validate_segment("device_id", device_id)
    return TELEMETRY_TOPIC_TEMPLATE.format(tenant_id=tenant_id, device_id=device_id)


def parse_telemetry_topic(topic: str) -> tuple[str, str]:
    """Return (tenant_id, device_id) for a well-formed telemetry topic."""
    match = _TELEMETRY_TOPIC_RE.fullmatch(topic) if isinstance(topic, str) else None
    if match is None:
        raise TopicError(f"not an AFES v2 device telemetry topic: {topic!r}")
    tenant_id = validate_segment("tenant_id", match.group("tenant_id"))
    device_id = validate_segment("device_id", match.group("device_id"))
    return tenant_id, device_id
