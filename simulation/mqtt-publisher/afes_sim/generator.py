"""Stage A virtual ESP32-S3 telemetry generator.

Produces payloads that use ONLY the fields of the approved AFES v2 telemetry
envelope (docs/TELEMETRY_SCHEMA.md section 3). Every payload is marked
``simulation.is_simulated = true`` with a ``STAGE_A_SIM_*`` scenario id and the
``VIRTUAL_SIM_NODE`` device type, so it can never be mistaken for Stage B
physical hardware telemetry.
"""

from __future__ import annotations

import hashlib
import random
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Iterator

from .config import FIXTURE_UPTIME_BASE_S, SimulatorConfig
from .scenarios import Scenario, Signal, get_scenario

SCHEMA_VERSION = "2.0"
DEVICE_TYPE = "VIRTUAL_SIM_NODE"
FIRMWARE_VERSION = "2.0.0-sim"
HARDWARE_VERSION = "SIM-v2"
GATEWAY_PROTOCOL = "MQTT"
MESH_ROLE = "ENDPOINT"
ADC_MAX = 4095

# Simulator-local synthetic mapping from smoke PPM to a 12-bit ADC count. It is
# monotonic and bounded but is NOT an MQ-2 calibration curve.
_SMOKE_ADC_OFFSET = 200.0
_SMOKE_ADC_PER_PPM = 4.0


def format_utc_ms(epoch_ms: int) -> str:
    """Format epoch milliseconds as ``YYYY-MM-DDTHH:mm:ss.sssZ`` (UTC)."""
    dt = datetime.fromtimestamp(epoch_ms // 1000, tz=timezone.utc)
    return f"{dt:%Y-%m-%dT%H:%M:%S}.{epoch_ms % 1000:03d}Z"


def virtual_mac(device_id: str) -> str:
    """Deterministic, locally administered unicast MAC for a virtual node.

    The first octet is 0x02 (locally administered, unicast), so a simulated
    MAC can never collide with a vendor-assigned (physical) ESP32-S3 address.
    """
    digest = hashlib.sha256(device_id.encode("utf-8")).digest()
    return ":".join(f"{b:02X}" for b in (0x02, 0x00, digest[0], digest[1], digest[2], digest[3]))


def _clamp_adc(value: float) -> int:
    return max(0, min(ADC_MAX, int(round(value))))


class TelemetryGenerator:
    """Stateful generator for one virtual node running one scenario."""

    def __init__(
        self,
        config: SimulatorConfig,
        *,
        clock_ms: Callable[[], int] | None = None,
    ) -> None:
        self.config = config
        self.scenario: Scenario = get_scenario(config.scenario)
        seed = config.effective_seed
        self._seeded = seed is not None
        # random.Random(int) seeding is stable across CPython versions.
        self._rng = random.Random(seed) if seed is not None else random.Random()
        self._clock_ms = clock_ms or (lambda: time.time_ns() // 1_000_000)
        self._start_epoch_ms = config.effective_start_epoch_ms
        self._uptime_base_s = FIXTURE_UPTIME_BASE_S if self._start_epoch_ms is not None else 0
        self._first_epoch_ms: int | None = None
        self._index = 0

    @property
    def topic(self) -> str:
        return self.config.topic

    # ---------------------------------------------------------------- signals
    def _progress(self) -> float:
        total = self.config.count
        if total <= 1:
            return 0.0
        return min(1.0, self._index / (total - 1))

    def _signal(self, signal: Signal) -> float:
        value = signal.start + (signal.end - signal.start) * self._progress()
        if self.config.noise and signal.noise_sigma > 0:
            value += self._rng.gauss(0.0, signal.noise_sigma)
        value = signal.band.clamp(value)
        rounded = round(value, signal.decimals)
        # Rounding must not push a value back outside its band.
        rounded = signal.band.clamp(rounded)
        return float(rounded) if signal.decimals else float(int(round(rounded)))

    def _message_id(self) -> str:
        if self._seeded:
            return str(uuid.UUID(int=self._rng.getrandbits(128), version=4))
        return str(uuid.uuid4())

    def _epoch_ms(self) -> int:
        if self._start_epoch_ms is not None:
            return self._start_epoch_ms + self._index * self.config.interval_ms
        return int(self._clock_ms())

    # ---------------------------------------------------------------- payload
    def next_payload(self) -> dict[str, Any]:
        cfg = self.config
        sc = self.scenario
        epoch_ms = self._epoch_ms()
        if self._first_epoch_ms is None:
            self._first_epoch_ms = epoch_ms
        uptime_s = self._uptime_base_s + max(0, epoch_ms - self._first_epoch_ms) // 1000

        message_id = self._message_id()
        temperature = self._signal(sc.temperature_c)
        humidity = self._signal(sc.humidity_pct)
        smoke_ppm = self._signal(sc.smoke_ppm)
        gas_co = self._signal(sc.gas_co_ppm)
        flame_adc = _clamp_adc(self._signal(sc.flame_raw_adc))
        risk = self._signal(sc.fire_risk)
        smoke_adc_noise = self._rng.gauss(0.0, 4.0) if cfg.noise else 0.0
        smoke_adc = _clamp_adc(_SMOKE_ADC_OFFSET + smoke_ppm * _SMOKE_ADC_PER_PPM + smoke_adc_noise)
        rssi_noise = self._rng.gauss(0.0, 1.5) if cfg.noise else 0.0
        rssi = max(-90, min(-30, int(round(-55 + rssi_noise))))

        payload: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "message_id": message_id,
            "correlation_id": None,
            "device": {
                "device_id": cfg.device_id,
                "device_type": DEVICE_TYPE,
                "firmware_version": FIRMWARE_VERSION,
                "hardware_version": HARDWARE_VERSION,
                "mac_address": virtual_mac(cfg.device_id),
            },
            "zone": {
                "zone_id": cfg.zone_id,
                "room_code": cfg.room_code,
                "building_id": cfg.building_id,
                "floor_level": cfg.floor_level,
            },
            "gateway": {
                "gateway_id": cfg.gateway_id,
                "protocol": GATEWAY_PROTOCOL,
                "mesh_role": MESH_ROLE,
            },
            "timestamps": {
                "timestamp_utc": format_utc_ms(epoch_ms),
                "timestamp_epoch_ms": epoch_ms,
                "device_uptime_s": uptime_s,
            },
            "status": {
                "system_state": sc.system_state,
                "sensor_health": sc.sensor_health,
                "battery_pct": None,
                "rssi_dbm": rssi,
            },
            "readings": {
                "temperature": temperature,
                "humidity": humidity,
                "smoke_ppm": smoke_ppm,
                "smoke_raw_adc": smoke_adc,
                "flame_detected": sc.flame_detected,
                "flame_raw_adc": flame_adc,
                "gas_co_ppm": gas_co,
                "ai_inferred_fire_risk": risk,
                "ai_classification": sc.ai_classification,
            },
            "actuators": {
                "buzzer_active": sc.buzzer_active,
                "alarm_led_active": sc.alarm_led_active,
                "water_pump_relay_active": sc.water_pump_relay_active,
                "exhaust_fan_active": sc.exhaust_fan_active,
                "override_mode": sc.override_mode,
            },
            "simulation": {
                "is_simulated": True,
                "scenario_id": sc.scenario_id,
                "synthetic_noise_added": bool(cfg.noise),
            },
        }
        self._index += 1
        return payload

    def generate(self, count: int | None = None) -> Iterator[dict[str, Any]]:
        total = self.config.count if count is None else count
        for _ in range(total):
            yield self.next_payload()


def generate_payloads(config: SimulatorConfig, count: int | None = None) -> list[dict[str, Any]]:
    """Convenience helper returning a list of payloads for ``config``."""
    return list(TelemetryGenerator(config).generate(count))
