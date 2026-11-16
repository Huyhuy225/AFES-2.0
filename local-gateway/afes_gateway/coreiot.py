"""CoreIOT HTTPS telemetry sink using Python standard library (no token logging)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


def to_coreiot_telemetry(payload: dict[str, Any]) -> dict[str, Any]:
    """Map AFES 2.0 telemetry envelope to flat CoreIOT telemetry keys while preserving simulation flags."""
    device = payload.get("device", {})
    zone = payload.get("zone", {})
    status = payload.get("status", {})
    readings = payload.get("readings", {})
    actuators = payload.get("actuators", {})
    simulation = payload.get("simulation", {})

    values: dict[str, Any] = {
        "schema_version": payload.get("schema_version"),
        "message_id": payload.get("message_id"),
        "device_id": device.get("device_id"),
        "device_type": device.get("device_type"),
        "zone_id": zone.get("zone_id"),
        "room_code": zone.get("room_code"),
        "system_state": status.get("system_state"),
        "sensor_health": status.get("sensor_health"),
        "rssi_dbm": status.get("rssi_dbm"),
        "temperature": readings.get("temperature"),
        "humidity": readings.get("humidity"),
        "smoke_ppm": readings.get("smoke_ppm"),
        "smoke_raw_adc": readings.get("smoke_raw_adc"),
        "flame_detected": readings.get("flame_detected"),
        "flame_raw_adc": readings.get("flame_raw_adc"),
        "buzzer_active": actuators.get("buzzer_active"),
        "alarm_led_active": actuators.get("alarm_led_active"),
        "water_pump_relay_active": actuators.get("water_pump_relay_active"),
        "override_mode": actuators.get("override_mode"),
        "is_simulated": simulation.get("is_simulated"),
        "scenario_id": simulation.get("scenario_id"),
    }
    if "ai_inferred_fire_risk" in readings:
        values["ai_inferred_fire_risk"] = readings["ai_inferred_fire_risk"]
    if "ai_classification" in readings:
        values["ai_classification"] = readings["ai_classification"]

    ts_ms = payload.get("timestamps", {}).get("timestamp_epoch_ms")
    if isinstance(ts_ms, int):
        return {"ts": ts_ms, "values": values}
    return values


class CoreIOTHttpSink:
    """Publishes validated telemetry to CoreIOT /api/v1/{token}/telemetry."""

    def __init__(self, base_url: str, token: str, timeout_ms: int = 5000) -> None:
        if not token or token.startswith("placeholder_"):
            raise ValueError("COREIOT_DEVICE_PROVISIONING_TOKEN is not configured")
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._timeout_s = max(timeout_ms / 1000.0, 1.0)

    def publish(self, topic: str, payload: dict[str, Any], qos: int = 1) -> None:
        del topic, qos  # HTTP sink targets device telemetry endpoint directly
        url = f"{self._base_url}/api/v1/{self._token}/telemetry"
        body = json.dumps(to_coreiot_telemetry(payload)).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self._timeout_s) as resp:
                if resp.status not in (200, 201, 202, 204):
                    raise RuntimeError(f"CoreIOT HTTP unexpected status {resp.status}")
        except urllib.error.HTTPError as exc:
            # Never include URL/token in exception messages.
            raise RuntimeError(f"CoreIOT HTTP error status={exc.code}") from None
        except urllib.error.URLError as exc:
            raise RuntimeError(f"CoreIOT connection failed: {exc.reason}") from None
