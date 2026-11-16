"""Configuration loader for the AFES 2.0 Local Gateway."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(dotenv_path: Path) -> None:
    """Populate os.environ from a local .env file without overriding existing vars."""
    if not dotenv_path.is_file():
        return
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


@dataclass(frozen=True)
class GatewayConfig:
    gateway_id: str = "GW-LOCAL-PC01"
    tenant_id: str = "default"
    health_host: str = "127.0.0.1"
    health_port: int = 8080
    mqtt_broker_url: str = "mqtt://localhost:1883"
    mqtt_client_id: str = "afes-local-gateway-dev"
    mqtt_username: str = "placeholder_mqtt_user"
    mqtt_password: str = "placeholder_local_mqtt_password"
    coreiot_base_url: str = "https://coreiot.example.local"
    coreiot_token: str = "placeholder_coreiot_provisioning_token"
    coreiot_timeout_ms: int = 5000
    dedup_cache_size: int = 1024
    buffer_max_size: int = 500
    log_level: str = "info"

    @classmethod
    def from_env(cls, dotenv_path: Path | None = None) -> "GatewayConfig":
        """Build configuration from .env and environment variables with safe defaults."""
        default_env = Path(__file__).resolve().parents[2] / ".env"
        _load_dotenv(dotenv_path or default_env)
        return cls(
            gateway_id=os.getenv("GATEWAY_ID", "GW-LOCAL-PC01"),
            tenant_id=os.getenv("AFES_TENANT_ID", "default"),
            health_host=os.getenv("GATEWAY_HEALTH_HOST", "127.0.0.1"),
            health_port=int(os.getenv("GATEWAY_HEALTH_PORT", "8080")),
            mqtt_broker_url=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"),
            mqtt_client_id=os.getenv("MQTT_CLIENT_ID", "afes-local-gateway-dev"),
            mqtt_username=os.getenv("MQTT_USERNAME", "placeholder_mqtt_user"),
            mqtt_password=os.getenv("MQTT_PASSWORD", "placeholder_local_mqtt_password"),
            coreiot_base_url=os.getenv("COREIOT_API_BASE_URL", "https://coreiot.example.local").rstrip("/"),
            coreiot_token=os.getenv("COREIOT_DEVICE_PROVISIONING_TOKEN", "placeholder_coreiot_provisioning_token"),
            coreiot_timeout_ms=int(os.getenv("COREIOT_TIMEOUT_MS", "5000")),
            dedup_cache_size=int(os.getenv("GATEWAY_DEDUP_CACHE_SIZE", "1024")),
            buffer_max_size=int(os.getenv("GATEWAY_BUFFER_MAX_SIZE", "500")),
            log_level=os.getenv("LOG_LEVEL", "info"),
        )

    def redacted_summary(self) -> dict[str, object]:
        """Return non-sensitive operational config for logs and health endpoints."""
        return {
            "gateway_id": self.gateway_id,
            "tenant_id": self.tenant_id,
            "health_bind": f"{self.health_host}:{self.health_port}",
            "mqtt_broker_url": self.mqtt_broker_url,
            "mqtt_client_id": self.mqtt_client_id,
            "coreiot_base_url": self.coreiot_base_url,
            "coreiot_token_configured": not self.coreiot_token.startswith("placeholder_"),
            "dedup_cache_size": self.dedup_cache_size,
            "buffer_max_size": self.buffer_max_size,
            "log_level": self.log_level,
        }
