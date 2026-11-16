"""Downlink RPC command validation and authorization (docs/TELEMETRY_SCHEMA.md §5)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PERMITTED_ACTIONS = frozenset(
    {
        "PUMP_ON",
        "PUMP_OFF",
        "TEST_ALARM",
        "FULL_SYSTEM_TEST",
        "EMERGENCY_SHUTDOWN",
        "EMERGENCY_RELEASE",
        "RESET_ALERTS",
        "REBOOT_DEVICE",
    }
)

AUTHORIZED_ROLES = frozenset({"ROLE_ADMIN", "ROLE_OPERATOR"})
ADMIN_ONLY_ACTIONS = frozenset({"EMERGENCY_RELEASE", "REBOOT_DEVICE"})
MAX_DURATION_MS = 60_000


@dataclass(frozen=True)
class CommandCheckResult:
    allowed: bool
    reason: str


def validate_downlink_command(command: Any) -> CommandCheckResult:
    """Validate a downlink command/req payload and enforce safety/role checks."""
    if not isinstance(command, dict):
        return CommandCheckResult(False, "COMMAND_NOT_OBJECT")

    if command.get("schema_version") != "2.0":
        return CommandCheckResult(False, "UNSUPPORTED_SCHEMA_VERSION")

    for req_field in ("request_id", "target_device_id", "action", "issuer", "idempotency_key"):
        if not command.get(req_field):
            return CommandCheckResult(False, f"MISSING_{req_field.upper()}")

    action = command["action"]
    if action not in PERMITTED_ACTIONS:
        return CommandCheckResult(False, "UNPERMITTED_ACTION")

    issuer = command["issuer"]
    if not isinstance(issuer, dict):
        return CommandCheckResult(False, "INVALID_ISSUER")
    role = issuer.get("role")
    if role not in AUTHORIZED_ROLES:
        return CommandCheckResult(False, "UNAUTHORIZED_ROLE")

    if action in ADMIN_ONLY_ACTIONS and role != "ROLE_ADMIN":
        return CommandCheckResult(False, "ADMIN_ROLE_REQUIRED")

    params = command.get("parameters") or {}
    if not isinstance(params, dict):
        return CommandCheckResult(False, "INVALID_PARAMETERS")

    if params.get("override_safety_lock") is True and role != "ROLE_ADMIN":
        return CommandCheckResult(False, "UNSAFE_SAFETY_OVERRIDE")

    duration_ms = params.get("duration_ms")
    if duration_ms is not None:
        if (
            not isinstance(duration_ms, int)
            or isinstance(duration_ms, bool)
            or duration_ms <= 0
            or duration_ms > MAX_DURATION_MS
        ):
            return CommandCheckResult(False, "INVALID_DURATION_MS")

    return CommandCheckResult(True, "OK")
