"""Offline contract and unit test suite for the AFES 2.0 Stage A telemetry simulator."""

from __future__ import annotations

import sys
from pathlib import Path

_PUBLISHER_DIR = str(Path(__file__).resolve().parents[1] / "mqtt-publisher")
if _PUBLISHER_DIR not in sys.path:
    sys.path.insert(0, _PUBLISHER_DIR)
