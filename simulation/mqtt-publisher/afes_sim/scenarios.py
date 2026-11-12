"""Stage A virtual telemetry scenarios.

Every scenario below describes SYNTHETIC data produced by a virtual node. The
numeric bands are simulator-local modelling assumptions chosen so that each
scenario is internally coherent; they are NOT sensor calibration data and they
are NOT part of the AFES v2 telemetry contract.

Alarm thresholds referenced here (temperature > 50.0 degC, smoke > 500.0 PPM)
are taken from the approved documentation (docs/TELEMETRY_SCHEMA.md section 4.1
trigger_details example and COURSE_REQUIREMENTS.md T12). The warning-smoke
pre-alarm band (300-500 PPM) is a simulator-local assumption because the
contract does not define a numeric pre-alarm threshold.
"""

from __future__ import annotations

from dataclasses import dataclass

TEMP_ALARM_THRESHOLD_C = 50.0
SMOKE_ALARM_THRESHOLD_PPM = 500.0
SMOKE_PREALARM_FLOOR_PPM = 300.0  # simulator-local assumption, not contract

SCENARIO_ID_PREFIX = "STAGE_A_SIM_"


@dataclass(frozen=True)
class Band:
    """Closed interval that a generated value is clamped into."""

    low: float
    high: float

    def clamp(self, value: float) -> float:
        return max(self.low, min(self.high, value))

    def contains(self, value: float) -> bool:
        return self.low <= value <= self.high


@dataclass(frozen=True)
class Signal:
    """A synthetic signal ramping linearly from start to end with noise."""

    start: float
    end: float
    noise_sigma: float
    band: Band
    decimals: int = 1


@dataclass(frozen=True)
class Scenario:
    key: str
    scenario_id: str
    description: str
    system_state: str
    sensor_health: str
    ai_classification: str
    temperature_c: Signal
    humidity_pct: Signal
    smoke_ppm: Signal
    gas_co_ppm: Signal
    flame_raw_adc: Signal
    fire_risk: Signal
    flame_detected: bool
    buzzer_active: bool
    alarm_led_active: bool
    water_pump_relay_active: bool
    exhaust_fan_active: bool
    override_mode: str


NORMAL = Scenario(
    key="normal",
    scenario_id=SCENARIO_ID_PREFIX + "NORMAL_BASELINE",
    description="Stage A virtual baseline monitoring: ambient room, no smoke, no flame.",
    system_state="NORMAL",
    sensor_health="HEALTHY",
    ai_classification="NORMAL",
    temperature_c=Signal(26.5, 27.5, 0.15, Band(20.0, 35.0)),
    humidity_pct=Signal(60.0, 62.0, 0.4, Band(40.0, 75.0)),
    smoke_ppm=Signal(110.0, 130.0, 2.5, Band(50.0, 200.0)),
    gas_co_ppm=Signal(3.5, 4.5, 0.2, Band(0.0, 9.0)),
    flame_raw_adc=Signal(90.0, 120.0, 6.0, Band(0.0, 400.0), decimals=0),
    fire_risk=Signal(0.01, 0.03, 0.005, Band(0.0, 0.10), decimals=2),
    flame_detected=False,
    buzzer_active=False,
    alarm_led_active=False,
    water_pump_relay_active=False,
    exhaust_fan_active=False,
    override_mode="AUTO",
)

WARNING_SMOKE = Scenario(
    key="warning-smoke",
    scenario_id=SCENARIO_ID_PREFIX + "WARNING_SMOKE",
    description=(
        "Stage A virtual smoke pre-alarm: smoke rising inside the simulator-local "
        "300-500 PPM band, temperature below the 50 degC alarm threshold, no flame."
    ),
    system_state="WARNING",
    sensor_health="HEALTHY",
    ai_classification="SMOKE_SPIKE",
    temperature_c=Signal(29.0, 33.0, 0.2, Band(25.0, 49.9)),
    humidity_pct=Signal(55.0, 52.0, 0.4, Band(35.0, 70.0)),
    smoke_ppm=Signal(320.0, 470.0, 6.0, Band(SMOKE_PREALARM_FLOOR_PPM, 499.9)),
    gas_co_ppm=Signal(8.0, 15.0, 0.5, Band(0.0, 35.0)),
    flame_raw_adc=Signal(150.0, 260.0, 10.0, Band(0.0, 900.0), decimals=0),
    fire_risk=Signal(0.35, 0.60, 0.02, Band(0.30, 0.70), decimals=2),
    flame_detected=False,
    buzzer_active=False,
    alarm_led_active=True,
    water_pump_relay_active=False,
    exhaust_fan_active=True,
    override_mode="AUTO",
)

CRITICAL_FIRE = Scenario(
    key="critical-fire",
    scenario_id=SCENARIO_ID_PREFIX + "CRITICAL_FIRE",
    description=(
        "Stage A virtual confirmed fire: temperature above 50 degC, smoke above "
        "500 PPM, flame detected, local suppression outputs engaged."
    ),
    system_state="CRITICAL",
    sensor_health="HEALTHY",
    ai_classification="FIRE",
    temperature_c=Signal(55.0, 68.0, 0.4, Band(TEMP_ALARM_THRESHOLD_C + 0.1, 90.0)),
    humidity_pct=Signal(40.0, 30.0, 0.5, Band(10.0, 60.0)),
    smoke_ppm=Signal(620.0, 880.0, 12.0, Band(SMOKE_ALARM_THRESHOLD_PPM + 0.1, 2000.0)),
    gas_co_ppm=Signal(40.0, 85.0, 2.0, Band(20.0, 400.0)),
    flame_raw_adc=Signal(3100.0, 3800.0, 40.0, Band(2500.0, 4095.0), decimals=0),
    fire_risk=Signal(0.90, 0.98, 0.01, Band(0.85, 1.0), decimals=2),
    flame_detected=True,
    buzzer_active=True,
    alarm_led_active=True,
    water_pump_relay_active=True,
    exhaust_fan_active=False,
    override_mode="EMERGENCY_LOCK",
)

SCENARIOS: dict[str, Scenario] = {s.key: s for s in (NORMAL, WARNING_SMOKE, CRITICAL_FIRE)}
DEFAULT_SCENARIO = NORMAL.key


def get_scenario(key: str) -> Scenario:
    try:
        return SCENARIOS[key]
    except KeyError:
        valid = ", ".join(sorted(SCENARIOS))
        raise ValueError(f"unknown scenario {key!r}; expected one of: {valid}") from None
