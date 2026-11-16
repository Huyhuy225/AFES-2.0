# AFES 2.0 Local Gateway (`local-gateway/`)

> **Course Item**: **T08** (Local IoT Gateway + minimal operations CLI & health/status endpoint)
> **GitHub Issue**: [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7)
> **Evidence Policy**: Offline tests and simulator-fed runs must be labelled `SIMULATION`. Physical claims require real ESP32-S3 input (`PHYSICAL HARDWARE`).

## Responsibilities

1. **Ingest & Schema Validation**: Consumes `afes/v2/{tenant_id}/devices/{device_id}/telemetry` and validates against `docs/TELEMETRY_SCHEMA.md` (v2.0) while preserving `simulation.is_simulated`.
2. **Idempotency & Deduplication**: Deduplicates packets by `(device_id, message_id)` using a bounded LRU cache.
3. **Offline Buffering & Ordered Replay**: Buffers telemetry during upstream outage (bounded FIFO) and replays in order upon reconnect.
4. **Authorized Command Routing**: Validates and routes downlink RPC commands (`command/req` -> `command/res`), rejecting unauthorized or unsafe payloads.
5. **Minimal Operations Surface**: Provides a CLI and read-only HTTP health/status endpoint (`127.0.0.1:8080` by default) with zero secret exposure. (Not a T10 custom web dashboard.)

## Quick Start (Offline / Simulation)

Run the unit & integration test suite using only the Python standard library:

```powershell
python -B -m unittest discover -s local-gateway/tests -t . -v
```

Run the CLI health/status check or validate a telemetry fixture:

```powershell
$env:PYTHONPATH="local-gateway;simulation/mqtt-publisher"
python -B -m afes_gateway status
python -B -m afes_gateway validate simulation/test-data/fixtures/valid/stage_a_normal_seed6.json
```

Start the minimal HTTP health/status server (`GET /health`, `GET /status`):

```powershell
$env:PYTHONPATH="local-gateway;simulation/mqtt-publisher"
python -B -m afes_gateway serve --host 127.0.0.1 --port 8080
```
