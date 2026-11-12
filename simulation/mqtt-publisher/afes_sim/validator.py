"""AFES v2 telemetry contract validation: schema artifact + Stage A profile.

Two layers are applied:

1. **Schema layer** - the formal Draft-07 schema copied verbatim from
   docs/TELEMETRY_SCHEMA.md section 8 (see ``schema.py``).
2. **Profile layer** - local correctness properties that the approved data
   dictionary (section 3.1) states in prose but the formal schema does not
   encode, plus Stage A labelling rules. The profile never relaxes the schema;
   it only adds checks:

   * ``message_id`` is a UUID **v4** (RFC 4122 variant);
   * ``timestamp_utc`` uses the exact ``YYYY-MM-DDTHH:mm:ss.sssZ`` UTC form and
     is the same instant as ``timestamp_epoch_ms``;
   * raw ADC values are integers in ``0..4095``; ``ai_inferred_fire_risk`` is in
     ``0.0..1.0``; humidity/battery percentages are in ``0..100``;
     concentrations are non-negative; ``device_uptime_s`` is non-negative;
   * enumerations listed only in the data dictionary (``device_type``,
     ``ai_classification``);
   * no fields outside the documented envelope;
   * Stage A labelling (when ``require_simulated``): ``simulation.is_simulated``
     must be ``true``, a ``scenario_id`` must be present, the device type must be
     ``VIRTUAL_SIM_NODE`` and the MAC must be locally administered, so simulated
     telemetry can never impersonate physical hardware.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .schema import Violation, documented_fields, load_schema, validate_against_schema
from .topics import TopicError, parse_telemetry_topic

ADC_MIN, ADC_MAX = 0, 4095
UTC_MS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
MAC_RE = re.compile(r"^[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}$")
# Plausibility window for epoch milliseconds: 2020-01-01 .. 2100-01-01 UTC.
EPOCH_MS_MIN = 1_577_836_800_000
EPOCH_MS_MAX = 4_102_444_800_000

# Enumerations stated in the data dictionary (section 3.1) but not in section 8.
DEVICE_TYPES = ("YOLO_UNO_S3", "VIRTUAL_SIM_NODE", "CUSTOM_SENSOR_NODE")
AI_CLASSIFICATIONS = ("NORMAL", "SMOKE_SPIKE", "FIRE")
SIMULATED_DEVICE_TYPE = "VIRTUAL_SIM_NODE"

_SCHEMA_CACHE: dict[str, Any] | None = None


def _default_schema() -> dict[str, Any]:
    global _SCHEMA_CACHE
    if _SCHEMA_CACHE is None:
        _SCHEMA_CACHE = load_schema()
    return _SCHEMA_CACHE


@dataclass
class ValidationResult:
    violations: list[Violation] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.violations

    @property
    def codes(self) -> set[str]:
        return {v.code for v in self.violations}

    def summary(self) -> str:
        if self.valid:
            return "VALID"
        return "INVALID: " + "; ".join(str(v) for v in self.violations)


def _get(payload: Any, dotted: str) -> tuple[bool, Any]:
    node = payload
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return False, None
        node = node[part]
    return True, node


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_num(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _profile_violations(
    payload: Any, schema: dict[str, Any], require_simulated: bool
) -> list[Violation]:
    out: list[Violation] = []
    if not isinstance(payload, dict):
        return out

    def add(code: str, path: str, message: str) -> None:
        out.append(Violation(code, path, message))

    # ---- undocumented fields (generator must emit only the contract)
    documented = documented_fields(schema)
    for obj_path, allowed in documented.items():
        present, node = (True, payload) if obj_path == "" else _get(payload, obj_path)
        if present and isinstance(node, dict) and allowed is not None:
            for extra in sorted(set(node) - allowed):
                path = f"{obj_path}.{extra}" if obj_path else extra
                add("PROFILE_UNDOCUMENTED_FIELD", path, "field is not part of the AFES v2 telemetry envelope")

    # ---- message id: UUID v4
    present, message_id = _get(payload, "message_id")
    if present and isinstance(message_id, str):
        try:
            parsed = uuid.UUID(message_id)
            ok = (
                parsed.version == 4
                and parsed.variant == uuid.RFC_4122
                and str(parsed) == message_id.lower()
            )
        except ValueError:
            ok = False
        if not ok:
            add("PROFILE_UUID_V4", "message_id", f"{message_id!r} is not a canonical RFC 4122 UUID v4")

    # ---- timestamps: exact UTC form and epoch coherence
    has_utc, ts_utc = _get(payload, "timestamps.timestamp_utc")
    has_epoch, ts_epoch = _get(payload, "timestamps.timestamp_epoch_ms")
    utc_epoch_ms: int | None = None
    if has_utc and isinstance(ts_utc, str):
        if not UTC_MS_RE.fullmatch(ts_utc):
            add(
                "PROFILE_TIMESTAMP_FORMAT",
                "timestamps.timestamp_utc",
                f"{ts_utc!r} must be UTC 'YYYY-MM-DDTHH:mm:ss.sssZ'",
            )
        else:
            try:
                dt = datetime.strptime(ts_utc, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                utc_epoch_ms = int(dt.timestamp()) * 1000 + dt.microsecond // 1000
            except ValueError:
                add("PROFILE_TIMESTAMP_FORMAT", "timestamps.timestamp_utc", f"{ts_utc!r} is not a real date")
    if has_epoch and _is_int(ts_epoch):
        if not EPOCH_MS_MIN <= ts_epoch < EPOCH_MS_MAX:
            add("PROFILE_EPOCH_RANGE", "timestamps.timestamp_epoch_ms", f"{ts_epoch} outside 2020..2100 window")
        if utc_epoch_ms is not None and utc_epoch_ms != ts_epoch:
            add(
                "PROFILE_TIMESTAMP_MISMATCH",
                "timestamps",
                f"timestamp_utc={ts_utc} ({utc_epoch_ms} ms) != timestamp_epoch_ms={ts_epoch}",
            )
    present, uptime = _get(payload, "timestamps.device_uptime_s")
    if present and _is_num(uptime) and uptime < 0:
        add("PROFILE_UPTIME_NEGATIVE", "timestamps.device_uptime_s", "uptime must be >= 0")

    # ---- readings bounds
    for adc_field in ("readings.smoke_raw_adc", "readings.flame_raw_adc"):
        present, value = _get(payload, adc_field)
        if present and not (_is_int(value) and ADC_MIN <= value <= ADC_MAX):
            add("PROFILE_ADC_RANGE", adc_field, f"{value!r} is not an integer 12-bit ADC count (0..4095)")
    present, risk = _get(payload, "readings.ai_inferred_fire_risk")
    if present and not (_is_num(risk) and 0.0 <= risk <= 1.0):
        add("PROFILE_RISK_RANGE", "readings.ai_inferred_fire_risk", f"{risk!r} not within 0.0..1.0")
    present, humidity = _get(payload, "readings.humidity")
    if present and _is_num(humidity) and not 0.0 <= humidity <= 100.0:
        add("PROFILE_HUMIDITY_RANGE", "readings.humidity", f"{humidity} %RH not within 0..100")
    for conc in ("readings.smoke_ppm", "readings.gas_co_ppm"):
        present, value = _get(payload, conc)
        if present and _is_num(value) and value < 0:
            add("PROFILE_NEGATIVE_CONCENTRATION", conc, f"{value} PPM must be >= 0")
    present, battery = _get(payload, "status.battery_pct")
    if present and _is_num(battery) and not 0.0 <= battery <= 100.0:
        add("PROFILE_BATTERY_RANGE", "status.battery_pct", f"{battery} not within 0..100")
    present, classification = _get(payload, "readings.ai_classification")
    if present and isinstance(classification, str) and classification not in AI_CLASSIFICATIONS:
        add("PROFILE_AI_CLASSIFICATION", "readings.ai_classification", f"{classification!r} not in {AI_CLASSIFICATIONS}")

    # ---- device identity
    present, device_type = _get(payload, "device.device_type")
    if present and isinstance(device_type, str) and device_type not in DEVICE_TYPES:
        add("PROFILE_DEVICE_TYPE", "device.device_type", f"{device_type!r} not in {DEVICE_TYPES}")
    present, mac = _get(payload, "device.mac_address")
    if present and isinstance(mac, str) and not MAC_RE.fullmatch(mac):
        add("PROFILE_MAC_FORMAT", "device.mac_address", f"{mac!r} is not an EUI-48 address")

    # ---- Stage A simulation labelling
    if require_simulated:
        present, is_simulated = _get(payload, "simulation.is_simulated")
        if is_simulated is not True:
            add(
                "PROFILE_NOT_SIMULATED",
                "simulation.is_simulated",
                "Stage A virtual telemetry must carry simulation.is_simulated == true",
            )
        else:
            present, scenario_id = _get(payload, "simulation.scenario_id")
            if not (isinstance(scenario_id, str) and scenario_id.strip()):
                add("PROFILE_SCENARIO_MISSING", "simulation.scenario_id", "simulated payload must name its scenario")
            if isinstance(device_type, str) and device_type in DEVICE_TYPES and device_type != SIMULATED_DEVICE_TYPE:
                add(
                    "PROFILE_DEVICE_TYPE",
                    "device.device_type",
                    f"simulated payload must use {SIMULATED_DEVICE_TYPE}, not physical type {device_type!r}",
                )
            if isinstance(mac, str) and MAC_RE.fullmatch(mac) and not int(mac[:2], 16) & 0x02:
                add(
                    "PROFILE_MAC_NOT_LOCAL",
                    "device.mac_address",
                    "simulated MAC must be locally administered (first octet bit 1 set)",
                )
    return out


def validate_telemetry(
    payload: Any,
    *,
    require_simulated: bool = True,
    schema: dict[str, Any] | None = None,
) -> ValidationResult:
    """Validate one telemetry payload (already parsed from JSON)."""
    schema = schema if schema is not None else _default_schema()
    violations = validate_against_schema(payload, schema)
    violations.extend(_profile_violations(payload, schema, require_simulated))
    return ValidationResult(violations)


def validate_topic(topic: str, payload: Any) -> ValidationResult:
    """Check the topic is the approved telemetry topic for the payload's device."""
    try:
        _tenant, topic_device = parse_telemetry_topic(topic)
    except TopicError as exc:
        return ValidationResult([Violation("TOPIC_FORMAT", "<topic>", str(exc))])
    present, device_id = _get(payload, "device.device_id")
    if present and device_id != topic_device:
        return ValidationResult(
            [Violation("TOPIC_DEVICE_MISMATCH", "<topic>", f"topic device {topic_device!r} != payload {device_id!r}")]
        )
    return ValidationResult()
