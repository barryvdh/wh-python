"""Tests that decode recorded API responses.

The fixtures are real responses with identifying fields replaced. They guard
against the generated models silently dropping fields the backend has started
reporting, which the models do because from_dict builds from a fixed key list.
"""
import json
import pathlib

import pytest

from weheat.abstractions.heat_pump import HeatPump
from weheat.models.raw_heatpump_log_and_is_online_dto import RawHeatpumpLogAndIsOnlineDto

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def load(name: str) -> dict:
    """Return the recorded response with the given name."""
    return json.loads((FIXTURES / name).read_text())


@pytest.mark.parametrize("name", [p.name for p in sorted(FIXTURES.glob("log_*.json"))])
def test_no_log_field_is_dropped(name):
    """Test the log model keeps every field the backend sent.

    from_dict picks keys one by one, so a field the backend adds is discarded
    without any error until it is added to the model as well.
    """
    payload = load(name)

    decoded = RawHeatpumpLogAndIsOnlineDto.from_dict(payload).to_dict()

    assert not set(payload) - set(decoded)


def test_cooling_log():
    """Test a log recorded while the heat pump was cooling."""
    pump = HeatPump("https://example.invalid", "heat-pump")
    pump._last_log = RawHeatpumpLogAndIsOnlineDto.from_dict(load("log_latest_cooling.json"))

    assert pump.heat_pump_state is HeatPump.State.COOLING
    assert pump.cooling_activity is HeatPump.CoolingActivity.ACTIVE
    assert pump.is_online is True
    assert pump.dhw_target_temperature == 55
    # heat is removed from the water while cooling, so the output power is negative
    assert pump.power_output == -2671
    assert pump.cop == pytest.approx(5.126, abs=0.001)
    # every start condition is met except the demand for cooling
    assert pump.cooling_start_conditions["demand"] is False
    assert pump.cooling_pause_reason is HeatPump.CoolingPauseReason.WATER_TEMPERATURE_BELOW_SETPOINT
    # the restart delay is counted in minutes from the last cooling cycle
    assert pump.cooling_available_from.isoformat() == "2026-08-29T11:32:28+00:00"
