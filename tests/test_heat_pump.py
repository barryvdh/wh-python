"""Unit tests for the decoding the HeatPump abstraction does on a log.

These run without API credentials, unlike the tests in test_ha_api.py.
"""
import pytest

from weheat.abstractions.heat_pump import HeatPump
from weheat.models.raw_heatpump_log_and_is_online_dto import RawHeatpumpLogAndIsOnlineDto

BASE_LOG = {
    "heat_pump_id": "0000-1111-2222-3333",
    "timestamp": "2026-08-31T10:00:00+00:00",
    "interval": 15,
}


def heat_pump(**fields) -> HeatPump:
    """Build a heat pump holding a log with the given fields."""
    pump = HeatPump("https://example.invalid", "0000-1111-2222-3333")
    pump._last_log = RawHeatpumpLogAndIsOnlineDto.model_validate({**BASE_LOG, **fields})
    return pump


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (1, HeatPump.State.OFFLINE),
        (40, HeatPump.State.STANDBY),
        (70, HeatPump.State.HEATING),
        (84, HeatPump.State.DEFROSTING),
        (90, HeatPump.State.DEFROSTING),
        (120, HeatPump.State.DEFROSTING),
        (130, HeatPump.State.COOLING),
        (136, HeatPump.State.WATER_CHECK),
        (137, HeatPump.State.COOLING),
        (138, None),
        (150, HeatPump.State.DHW),
        (200, HeatPump.State.DEFROSTING),
        (239, HeatPump.State.DEFROSTING),
        (240, None),
        (1010, HeatPump.State.UPDATING),
    ],
)
def test_heat_pump_state(state, expected):
    """Test the numeric state maps to the state the heat pump is in."""
    assert heat_pump(state=state).heat_pump_state is expected


@pytest.mark.parametrize(
    ("fields", "expected"),
    [
        ({"state": 132, "cooling_pause_reason": 0}, HeatPump.CoolingStatus.ACTIVE),
        ({"state": 131, "cooling_pause_reason": 0}, HeatPump.CoolingStatus.STARTING),
        ({"state": 136, "cooling_pause_reason": 0}, HeatPump.CoolingStatus.WATER_CHECK),
        ({"state": 40, "cooling_pause_reason": 0}, HeatPump.CoolingStatus.WAITING),
        ({"state": 40, "cooling_pause_reason": 4}, HeatPump.CoolingStatus.PAUSED),
        (
            {"state": 40, "cooling_pause_reason": 0, "cooling_stop_reason": 1},
            HeatPump.CoolingStatus.STOPPED,
        ),
        # a pause reason only counts while the heat pump is in standby
        ({"state": 70, "cooling_pause_reason": 4}, HeatPump.CoolingStatus.WAITING),
        # a heat pump that does not do cooling reports no cooling fields at all
        ({"state": 70}, None),
    ],
)
def test_cooling_status(fields, expected):
    """Test the cooling status says what the heat pump is doing, or why it is not."""
    assert heat_pump(**fields).cooling_status is expected


def test_cooling_start_conditions():
    """Test the start conditions decode to a flag per condition."""
    # every condition met except the outside air temperature
    conditions = heat_pump(cooling_start_conditions=2043).cooling_start_conditions

    assert conditions["outside_air_temperature"] is False
    assert conditions["demand"] is True
    assert sum(conditions.values()) == len(HeatPump.COOLING_START_CONDITION_BITS) - 1


def test_cooling_start_conditions_without_a_log():
    """Test a heat pump that reports no start conditions decodes to nothing."""
    assert heat_pump().cooling_start_conditions is None


@pytest.mark.parametrize(
    ("power_in", "power_out", "expected"),
    [
        (500, 2000, 4.0),
        # while cooling the output power is negative, the ratio stays positive
        (521, -2671, pytest.approx(5.126, abs=0.001)),
        (0, 2000, 0),
    ],
)
def test_cop(power_in, power_out, expected):
    """Test the coefficient of performance is a positive ratio in every state."""
    pump = heat_pump(cm_mass_power_in=power_in, cm_mass_power_out=power_out)

    assert pump.cop == expected


def test_cooling_available_from():
    """Test the restart delay is counted from the last cooling cycle."""
    pump = heat_pump(
        last_cooling_time="2026-08-31T09:00:00+00:00", cooling_exponential_backoff=180
    )

    assert pump.cooling_available_from.isoformat() == "2026-08-31T12:00:00+00:00"


def test_cooling_available_from_before_any_cooling():
    """Test there is no restart delay before the heat pump has ever cooled."""
    assert heat_pump(cooling_exponential_backoff=180).cooling_available_from is None


@pytest.mark.parametrize("code", [99, -1])
def test_unknown_codes_decode_to_nothing(code):
    """Test a code this version does not know does not raise."""
    pump = heat_pump(cooling_pause_reason=code, cooling_stop_reason=code)

    assert pump.cooling_pause_reason is None
    assert pump.cooling_stop_reason is None
