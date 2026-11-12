"""Environment-variable configuration for the Stage A telemetry simulator.

All settings come from ``AFES_SIM_*`` environment variables (optionally loaded
from a local, git-ignored ``.env`` file). No credentials, tokens or production
endpoints are embedded here; the defaults target a loopback broker and are only
used when the operator explicitly selects the MQTT transport.
"""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Mapping

from .scenarios import DEFAULT_SCENARIO, SCENARIOS
from .topics import TopicError, telemetry_topic, validate_segment

ENV_PREFIX = "AFES_SIM_"

# Reproducible fixture mode anchors: 2026-11-12T04:20:00.000Z is the instant
# used by the approved Stage A example in docs/TELEMETRY_SCHEMA.md section 7.1;
# seed 6 refers to GitHub Issue #6.
FIXTURE_START_EPOCH_MS = 1794457200000
FIXTURE_SEED = 6
FIXTURE_UPTIME_BASE_S = 3600

LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})

_TRUE = frozenset({"1", "true", "yes", "on"})
_FALSE = frozenset({"0", "false", "no", "off", ""})


class ConfigError(ValueError):
    """Raised for invalid or unsafe simulator configuration."""


@dataclass(frozen=True)
class SimulatorConfig:
    # Identity / topic coordinates
    tenant_id: str = "stage-a-sim"
    device_id: str = "SIM-ESP32-101"
    gateway_id: str = "GW-LOCAL-PC01"
    zone_id: str = "ZONE-101"
    room_code: str = "ROOM-101"
    building_id: str = "BLDG-CSE"
    floor_level: int = 1
    # Generation
    scenario: str = DEFAULT_SCENARIO
    seed: int | None = None
    fixture_mode: bool = False
    start_epoch_ms: int | None = None
    interval_ms: int = 2000
    count: int = 10
    noise: bool = True
    # MQTT transport (only used with --transport mqtt)
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_client_id: str = ""
    mqtt_username: str = ""
    mqtt_pass: str = field(default="", repr=False)
    mqtt_tls: bool = False
    mqtt_tls_ca_file: str = ""
    mqtt_keepalive_s: int = 60
    mqtt_connect_timeout_s: float = 5.0
    mqtt_connect_attempts: int = 3
    mqtt_retry_backoff_s: float = 1.0
    allow_insecure_remote_auth: bool = False

    # ------------------------------------------------------------------ helpers
    @property
    def effective_seed(self) -> int | None:
        if self.seed is not None:
            return self.seed
        return FIXTURE_SEED if self.fixture_mode else None

    @property
    def effective_start_epoch_ms(self) -> int | None:
        if self.start_epoch_ms is not None:
            return self.start_epoch_ms
        return FIXTURE_START_EPOCH_MS if self.fixture_mode else None

    @property
    def effective_client_id(self) -> str:
        return self.mqtt_client_id or f"afes-stage-a-sim-{self.device_id}"

    @property
    def topic(self) -> str:
        return telemetry_topic(self.tenant_id, self.device_id)

    @property
    def has_credentials(self) -> bool:
        return bool(self.mqtt_username or self.mqtt_pass)

    def with_overrides(self, **changes: object) -> "SimulatorConfig":
        clean = {k: v for k, v in changes.items() if v is not None}
        return replace(self, **clean).validated()

    def redacted(self) -> dict[str, object]:
        """Return a log-safe view of the configuration (credentials masked)."""
        data = asdict(self)
        data["mqtt_pass"] = "***" if self.mqtt_pass else ""
        data["mqtt_username"] = "***" if self.mqtt_username else ""
        return data

    def validated(self) -> "SimulatorConfig":
        problems: list[str] = []
        for name in ("tenant_id", "device_id", "gateway_id"):
            try:
                validate_segment(name, getattr(self, name))
            except TopicError as exc:
                problems.append(str(exc))
        if len(self.device_id) < 3:
            problems.append("device_id must be at least 3 characters (schema minLength)")
        for name in ("zone_id", "room_code", "building_id"):
            if not getattr(self, name).strip():
                problems.append(f"{name} must not be empty")
        if self.scenario not in SCENARIOS:
            problems.append(
                f"scenario must be one of {sorted(SCENARIOS)}; got {self.scenario!r}"
            )
        if not 100 <= self.interval_ms <= 3_600_000:
            problems.append("interval_ms must be between 100 and 3600000")
        if not 1 <= self.count <= 100_000:
            problems.append("count must be between 1 and 100000")
        if not 1 <= self.mqtt_port <= 65535:
            problems.append("mqtt_port must be between 1 and 65535")
        if not 1 <= self.mqtt_connect_attempts <= 20:
            problems.append("mqtt_connect_attempts must be between 1 and 20")
        if self.mqtt_connect_timeout_s <= 0 or self.mqtt_retry_backoff_s < 0:
            problems.append("mqtt timeouts/backoff must be positive")
        if self.start_epoch_ms is not None and self.start_epoch_ms < 0:
            problems.append("start_epoch_ms must be >= 0")
        if (
            self.has_credentials
            and not self.mqtt_tls
            and self.mqtt_host.lower() not in LOOPBACK_HOSTS
            and not self.allow_insecure_remote_auth
        ):
            problems.append(
                "refusing to send MQTT credentials in cleartext to a non-loopback host; "
                "set AFES_SIM_MQTT_TLS=true (or explicitly AFES_SIM_ALLOW_INSECURE_REMOTE_AUTH=true "
                "for an isolated lab network)"
            )
        if problems:
            raise ConfigError("; ".join(problems))
        return self

    # --------------------------------------------------------------- factories
    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "SimulatorConfig":
        env = os.environ if env is None else env
        reader = _EnvReader(env)
        defaults = cls()
        cfg = cls(
            tenant_id=reader.text("TENANT_ID", defaults.tenant_id),
            device_id=reader.text("DEVICE_ID", defaults.device_id),
            gateway_id=reader.text("GATEWAY_ID", defaults.gateway_id),
            zone_id=reader.text("ZONE_ID", defaults.zone_id),
            room_code=reader.text("ROOM_CODE", defaults.room_code),
            building_id=reader.text("BUILDING_ID", defaults.building_id),
            floor_level=reader.integer("FLOOR_LEVEL", defaults.floor_level),
            scenario=reader.text("SCENARIO", defaults.scenario),
            seed=reader.optional_integer("SEED"),
            fixture_mode=reader.boolean("FIXTURE_MODE", defaults.fixture_mode),
            start_epoch_ms=reader.optional_integer("START_EPOCH_MS"),
            interval_ms=reader.integer("INTERVAL_MS", defaults.interval_ms),
            count=reader.integer("COUNT", defaults.count),
            noise=reader.boolean("NOISE", defaults.noise),
            mqtt_host=reader.text("MQTT_HOST", defaults.mqtt_host),
            mqtt_port=reader.integer("MQTT_PORT", defaults.mqtt_port),
            mqtt_client_id=reader.text("MQTT_CLIENT_ID", defaults.mqtt_client_id),
            mqtt_username=reader.text("MQTT_USERNAME", ""),
            mqtt_pass=reader.text("MQTT_PASSWORD", ""),
            mqtt_tls=reader.boolean("MQTT_TLS", defaults.mqtt_tls),
            mqtt_tls_ca_file=reader.text("MQTT_TLS_CA_FILE", ""),
            mqtt_keepalive_s=reader.integer("MQTT_KEEPALIVE_S", defaults.mqtt_keepalive_s),
            mqtt_connect_timeout_s=reader.number(
                "MQTT_CONNECT_TIMEOUT_S", defaults.mqtt_connect_timeout_s
            ),
            mqtt_connect_attempts=reader.integer(
                "MQTT_CONNECT_ATTEMPTS", defaults.mqtt_connect_attempts
            ),
            mqtt_retry_backoff_s=reader.number(
                "MQTT_RETRY_BACKOFF_S", defaults.mqtt_retry_backoff_s
            ),
            allow_insecure_remote_auth=reader.boolean(
                "ALLOW_INSECURE_REMOTE_AUTH", defaults.allow_insecure_remote_auth
            ),
        )
        reader.raise_if_errors()
        return cfg.validated()


class _EnvReader:
    def __init__(self, env: Mapping[str, str]) -> None:
        self._env = env
        self._errors: list[str] = []

    def _raw(self, key: str) -> str | None:
        value = self._env.get(ENV_PREFIX + key)
        return None if value is None else value.strip()

    def text(self, key: str, default: str) -> str:
        value = self._raw(key)
        return default if value is None or value == "" else value

    def integer(self, key: str, default: int) -> int:
        value = self._raw(key)
        if value is None or value == "":
            return default
        try:
            return int(value, 10)
        except ValueError:
            self._errors.append(f"{ENV_PREFIX}{key} must be an integer")
            return default

    def optional_integer(self, key: str) -> int | None:
        value = self._raw(key)
        if value is None or value == "":
            return None
        try:
            return int(value, 10)
        except ValueError:
            self._errors.append(f"{ENV_PREFIX}{key} must be an integer")
            return None

    def number(self, key: str, default: float) -> float:
        value = self._raw(key)
        if value is None or value == "":
            return default
        try:
            return float(value)
        except ValueError:
            self._errors.append(f"{ENV_PREFIX}{key} must be a number")
            return default

    def boolean(self, key: str, default: bool) -> bool:
        value = self._raw(key)
        if value is None:
            return default
        lowered = value.lower()
        if lowered in _TRUE:
            return True
        if lowered in _FALSE:
            return False if lowered else default
        self._errors.append(f"{ENV_PREFIX}{key} must be a boolean (true/false)")
        return default

    def raise_if_errors(self) -> None:
        if self._errors:
            raise ConfigError("; ".join(self._errors))


def load_env_file(path: str | os.PathLike[str]) -> dict[str, str]:
    """Parse a minimal KEY=VALUE env file (comments and blank lines ignored)."""
    values: dict[str, str] = {}
    file_path = Path(path)
    if not file_path.is_file():
        raise ConfigError(f"env file not found: {file_path}")
    for lineno, raw in enumerate(file_path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        key, sep, value = line.partition("=")
        if not sep or not key.strip():
            raise ConfigError(f"{file_path}:{lineno}: expected KEY=VALUE")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def build_environment(env_file: str | None = None) -> dict[str, str]:
    """Merge an optional env file with the process environment (process wins)."""
    merged: dict[str, str] = {}
    if env_file:
        merged.update(load_env_file(env_file))
    merged.update(os.environ)
    return merged
