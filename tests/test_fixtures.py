"""Tests that decode recorded API responses.

The fixtures are real responses with identifying fields replaced. They guard
against the generated models silently dropping fields the backend has started
reporting, which the models do because from_dict builds from a fixed key list.
"""
import json
import pathlib

import pytest

from weheat.abstractions.heat_pump import HeatPump
from weheat.models import TotalEnergyAggregate
from weheat.models.raw_heatpump_log_and_is_online_dto import RawHeatpumpLogAndIsOnlineDto
from weheat.models.read_all_heat_pump_dto_paged_response import ReadAllHeatPumpDtoPagedResponse
from weheat.models.read_heat_pump_dto import ReadHeatPumpDto

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def load(name: str) -> dict:
    """Return the recorded response with the given name."""
    return json.loads((FIXTURES / name).read_text())


def dropped_fields(payload: dict, decoded: dict) -> set:
    """Return the keys the model did not keep."""
    return set(payload) - set(decoded)


@pytest.mark.parametrize(
    ("name", "model"),
    [
        ("log_latest_cooling.json", RawHeatpumpLogAndIsOnlineDto),
        ("log_latest_standby.json", RawHeatpumpLogAndIsOnlineDto),
        ("energy_total.json", TotalEnergyAggregate),
        ("heat_pump.json", ReadHeatPumpDto),
    ],
)
def test_no_field_is_dropped(name, model):
    """Test the model keeps every field the backend sent.

    from_dict picks keys one by one, so a field the backend adds is discarded
    without any error until it is added to the model as well.
    """
    payload = load(name)

    assert not dropped_fields(payload, model.from_dict(payload).to_dict())


def test_no_field_is_dropped_from_the_heat_pump_list():
    """Test the paged heat pump list keeps every field the backend sent."""
    payload = load("heat_pumps_list.json")

    decoded = ReadAllHeatPumpDtoPagedResponse.from_dict(payload).to_dict()

    assert not dropped_fields(payload, decoded)
    assert not dropped_fields(payload["data"][0], decoded["data"][0])


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


def test_standby_log():
    """Test a log recorded after cooling was stopped for another function."""
    pump = HeatPump("https://example.invalid", "heat-pump")
    pump._last_log = RawHeatpumpLogAndIsOnlineDto.from_dict(load("log_latest_standby.json"))

    assert pump.heat_pump_state is HeatPump.State.STANDBY
    assert pump.cooling_activity is HeatPump.CoolingActivity.STOPPED
    assert pump.cooling_stop_reason is HeatPump.CoolingStopReason.HEAT_PUMP_CONTROL
    # only the outside air temperature is holding cooling off
    unmet = [name for name, met in pump.cooling_start_conditions.items() if not met]
    assert unmet == ["outside_air_temperature"]
    # the pump is idle, so it reports no flow through either circuit
    assert pump.central_heating_flow_volume == 0
    assert pump.compressor_rpm == 0


def test_energy_total():
    """Test the recorded energy totals add up the way the properties report them."""
    pump = HeatPump("https://example.invalid", "heat-pump")
    pump._energy_total = TotalEnergyAggregate.from_dict(load("energy_total.json"))

    assert pump.energy_in_heating == pytest.approx(5717.358)
    assert pump.energy_in_defrost == pytest.approx(36.181 + 0.045924444)
    # energy removed from the water is reported as a negative amount
    assert pump.energy_out_cooling < 0
    assert pump.energy_total == pytest.approx(
        5717.358 + 2143.2793 + 832.4635 + 103.82725 + 36.181 + 0.045924444
    )
