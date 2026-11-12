"""Command-line interface for the AFES 2.0 Stage A virtual telemetry simulator.

Usage examples (from repository root):

    # Offline deterministic telemetry generation (no broker, no credentials):
    PYTHONPATH=simulation/mqtt-publisher python -m afes_sim publish \\
        --fixture-mode --scenario normal --count 3

    # Offline contract validation of committed JSON / JSONL fixtures:
    PYTHONPATH=simulation/mqtt-publisher python -m afes_sim validate \\
        simulation/test-data/fixtures/valid/stage_a_normal_seed6.json
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Sequence, TextIO

from .config import ConfigError, SimulatorConfig, build_environment
from .publisher import (
    STAGE_A_BANNER,
    ContractRejectionError,
    MemoryTransport,
    PahoMqttTransport,
    PublishTransportError,
    StdoutTransport,
    TelemetryPublisher,
    Transport,
)
from .scenarios import SCENARIOS
from .schema import DEFAULT_SCHEMA_PATH, PayloadDecodeError, SchemaError, load_schema, loads_strict
from .validator import validate_telemetry, validate_topic


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="afes_sim",
        description=(
            f"{STAGE_A_BANNER} AFES 2.0 hardware-independent virtual ESP32-S3 "
            "telemetry simulator and offline MQTT contract validator."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    pub = sub.add_parser(
        "publish",
        help="Generate and validate Stage A virtual telemetry and emit via stdout, memory, or MQTT.",
    )
    pub.add_argument("--env-file", help="Optional path to a simulator .env file.")
    pub.add_argument(
        "--transport",
        choices=("stdout", "memory", "mqtt"),
        default="stdout",
        help="Output transport (default: stdout, offline-safe with no broker).",
    )
    pub.add_argument(
        "--scenario",
        choices=tuple(sorted(SCENARIOS)),
        default=None,
        help="Virtual telemetry scenario (overrides AFES_SIM_SCENARIO).",
    )
    pub.add_argument("--count", type=int, default=None, help="Number of telemetry packets.")
    pub.add_argument(
        "--interval-ms",
        type=int,
        default=None,
        help="Nominal publish interval in milliseconds (overrides AFES_SIM_INTERVAL_MS).",
    )
    pub.add_argument("--seed", type=int, default=None, help="Deterministic RNG seed.")
    pub.add_argument(
        "--fixture-mode",
        action="store_true",
        default=None,
        help="Enable reproducible fixture mode (seed=6, epoch=1794457200000).",
    )
    pub.add_argument("--tenant-id", default=None, help="Override AFES_SIM_TENANT_ID.")
    pub.add_argument("--device-id", default=None, help="Override AFES_SIM_DEVICE_ID.")
    pub.add_argument("--gateway-id", default=None, help="Override AFES_SIM_GATEWAY_ID.")
    pub.add_argument(
        "--output",
        default=None,
        help="Optional output file path when using --transport stdout.",
    )
    sleep_group = pub.add_mutually_exclusive_group()
    sleep_group.add_argument(
        "--real-time",
        action="store_true",
        help="Sleep interval_ms between packets even on offline transports.",
    )
    sleep_group.add_argument(
        "--no-sleep",
        action="store_true",
        help="Do not sleep between packets even when using --transport mqtt.",
    )

    val = sub.add_parser(
        "validate",
        help="Validate JSON or JSONL telemetry payloads against the AFES v2 contract offline.",
    )
    val.add_argument(
        "paths",
        nargs="+",
        help="One or more JSON (.json) or JSON Lines (.jsonl) payload files to validate.",
    )
    val.add_argument(
        "--schema",
        default=str(DEFAULT_SCHEMA_PATH),
        help="Path to the AFES v2 telemetry JSON Schema artifact.",
    )
    val.add_argument(
        "--topic",
        default=None,
        help="Optional MQTT topic string to validate against each payload's device_id.",
    )
    val.add_argument(
        "--allow-stage-b",
        action="store_true",
        help=(
            "Allow simulation.is_simulated=false (only for checking the documented "
            "Stage B contract example; Stage A requires is_simulated=true)."
        ),
    )

    return parser


def _run_publish(
    args: argparse.Namespace,
    *,
    stdout: TextIO,
    stderr: TextIO,
) -> int:
    try:
        env = build_environment(args.env_file)
        cfg = SimulatorConfig.from_env(env).with_overrides(
            scenario=args.scenario,
            count=args.count,
            interval_ms=args.interval_ms,
            seed=args.seed,
            fixture_mode=True if args.fixture_mode else None,
            tenant_id=args.tenant_id,
            device_id=args.device_id,
            gateway_id=args.gateway_id,
        )
    except ConfigError as exc:
        stderr.write(f"{STAGE_A_BANNER} CONFIGURATION ERROR: {exc}\n")
        return 2

    out_handle: TextIO | None = None
    try:
        if args.transport == "stdout":
            if args.output:
                out_path = Path(args.output)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_handle = out_path.open("w", encoding="utf-8", newline="\n")
                transport: Transport = StdoutTransport(stream=out_handle)
            else:
                transport = StdoutTransport(stream=stdout)
        elif args.transport == "memory":
            transport = MemoryTransport()
        else:
            transport = PahoMqttTransport(cfg)

        use_sleep = args.real_time or (args.transport == "mqtt" and not args.no_sleep)
        sleep_fn = time.sleep if use_sleep else None

        publisher = TelemetryPublisher(cfg, transport, sleep_fn=sleep_fn)
        summary = publisher.publish_payloads()
    except (ContractRejectionError, PublishTransportError) as exc:
        stderr.write(f"{STAGE_A_BANNER} PUBLISH ERROR: {exc}\n")
        return 1
    finally:
        if out_handle is not None:
            out_handle.close()

    stderr.write(
        f"{STAGE_A_BANNER} Completed virtual telemetry run "
        f"(NOT physical ESP32-S3 hardware verification): "
        f"transport={summary.transport_name} topic={summary.topic} "
        f"qos={summary.qos} retain={summary.retain} "
        f"scenario={summary.scenario} seed={summary.seed} "
        f"published={summary.count_published}/{summary.count_requested}\n"
    )
    return 0


def _iter_payloads_from_file(path: Path) -> list[tuple[str, object]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        items: list[tuple[str, object]] = []
        for lineno, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped:
                continue
            obj = loads_strict(stripped)
            if isinstance(obj, dict) and "payload" in obj and "stage_label" in obj:
                obj = obj["payload"]
            items.append((f"{path}:{lineno}", obj))
        if not items:
            raise PayloadDecodeError(f"{path}: JSONL file contains no records")
        return items
    return [(str(path), loads_strict(text))]


def _run_validate(
    args: argparse.Namespace,
    *,
    stdout: TextIO,
    stderr: TextIO,
) -> int:
    try:
        schema = load_schema(args.schema)
    except (OSError, PayloadDecodeError, SchemaError) as exc:
        stderr.write(f"{STAGE_A_BANNER} SCHEMA ERROR: {exc}\n")
        return 2

    require_simulated = not args.allow_stage_b
    any_failed = False
    total_checked = 0

    for raw_path in args.paths:
        file_path = Path(raw_path)
        if not file_path.is_file():
            stderr.write(f"{STAGE_A_BANNER} INVALID {file_path}: file not found\n")
            any_failed = True
            continue
        try:
            records = _iter_payloads_from_file(file_path)
        except PayloadDecodeError as exc:
            stderr.write(f"{STAGE_A_BANNER} INVALID {file_path}: {exc}\n")
            any_failed = True
            continue

        for label, payload in records:
            total_checked += 1
            result = validate_telemetry(
                payload,
                require_simulated=require_simulated,
                schema=schema,
            )
            violations = list(result.violations)
            if args.topic is not None:
                topic_res = validate_topic(args.topic, payload)
                violations.extend(topic_res.violations)
            if violations:
                any_failed = True
                details = "; ".join(str(v) for v in violations)
                stderr.write(f"{STAGE_A_BANNER} INVALID {label}: {details}\n")
            else:
                stdout.write(f"{STAGE_A_BANNER} VALID {label}\n")

    if any_failed or total_checked == 0:
        return 1
    return 0


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = sys.stdout if stdout is None else stdout
    err = sys.stderr if stderr is None else stderr
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.command == "publish":
        return _run_publish(args, stdout=out, stderr=err)
    if args.command == "validate":
        return _run_validate(args, stdout=out, stderr=err)
    return 2
