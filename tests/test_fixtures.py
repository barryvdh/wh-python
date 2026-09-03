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
from weheat.models.heat_pump_log_view_dto import HeatPumpLogViewDto
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
        ("log_latest_cooling_active.json", RawHeatpumpLogAndIsOnlineDto),
        ("log_latest_cooling_stalled.json", RawHeatpumpLogAndIsOnlineDto),
        ("log_latest_dhw_method_none.json", RawHeatpumpLogAndIsOnlineDto),
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
    assert pump.dhw_control_method is HeatPump.DhwControlMethod.FIXED
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
    # the indoor unit is metered separately, and is not part of that total
    assert pump.energy_in_indoor_unit == pytest.approx(
        426.02554 + 252.08315 + 95.72314 + 245.75871 + 22.127708 + 0.038020276
    )
    assert pump.energy_in_indoor_unit < pump.energy_total


@pytest.mark.parametrize(
    "name",
    [
        "log_aggregated_cooling.json",
        "log_aggregated_dhw.json",
        "log_aggregated_heating_old_firmware.json",
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="the aggregated log model predates the cooling and DHW fields, so it "
    "drops all of them; regenerating the models from the spec fixes this",
)
def test_no_field_is_dropped_from_the_aggregated_log(name):
    """Test the aggregated log model keeps every field the backend sent."""
    payload = load(name)

    assert not dropped_fields(payload, HeatPumpLogViewDto.from_dict(payload).to_dict())


def test_cooling_is_stopped_when_dhw_takes_over():
    """Test the recorded buckets show what stops a cooling cycle.

    The stop reason turns to HeatPumpControl exactly when the heat pump switches
    to DHW, which is what that reason means: another function took priority.
    """
    cooling = load("log_aggregated_cooling.json")
    dhw = load("log_aggregated_dhw.json")

    assert cooling["heatPumpStateCooling"] == 60
    assert cooling["coolingStopReasonNone"] == 60
    assert dhw["heatPumpStateDhw"] == 60
    assert dhw["coolingStopReasonHeatPumpControl"] == 60


def test_older_firmware_reports_the_cooling_fields_as_null():
    """Test the backend sends the cooling fields even for firmware that predates them.

    The fields are present and null rather than missing, which is what lets a
    consumer tell "this heat pump does not report cooling" from "this response
    is from before cooling existed": both look the same, and both mean no cooling.
    """
    payload = load("log_aggregated_heating_old_firmware.json")
    current = load("log_aggregated_cooling.json")

    assert set(payload) == set(current)
    assert payload["hqMessageVersionMin"] is None
    assert current["hqMessageVersionMin"] == 1
    assert all(
        payload[key] is None for key in payload if key.startswith("coolingStartConditions")
    )


def test_a_heat_pump_without_the_cooling_fields_reports_no_cooling():
    """Test a log from firmware without cooling decodes to no cooling at all."""
    pump = HeatPump("https://example.invalid", "heat-pump")
    pump._last_log = RawHeatpumpLogAndIsOnlineDto.model_validate(
        {"heat_pump_id": "heat-pump", "timestamp": "2026-01-01T18:30:00+00:00",
         "interval": 15, "state": 70}
    )

    assert pump.heat_pump_state is HeatPump.State.HEATING
    assert pump.cooling_activity is None
    assert pump.cooling_start_conditions is None
    assert pump.cooling_available_from is None


def test_a_stalled_cooling_run_decodes_the_same_as_a_working_one():
    """Test nothing the heat pump reports about its state tells a stall apart.

    Both records are recorded from the same pump two hours into a cooling run,
    one turning and one stalled. Every state, reason and condition matches; only
    the measurements differ, so a consumer has to look at those to see a stall.
    """
    working = HeatPump("https://example.invalid", "heat-pump")
    working._last_log = RawHeatpumpLogAndIsOnlineDto.from_dict(
        load("log_latest_cooling_active.json")
    )
    stalled = HeatPump("https://example.invalid", "heat-pump")
    stalled._last_log = RawHeatpumpLogAndIsOnlineDto.from_dict(
        load("log_latest_cooling_stalled.json")
    )

    for name in (
        "heat_pump_state",
        "cooling_state",
        "cooling_activity",
        "cooling_pause_reason",
        "cooling_stop_reason",
        "cooling_start_conditions",
    ):
        assert getattr(working, name) == getattr(stalled, name), name

    # only what it measures gives the stall away
    assert working.compressor_rpm == 2100
    assert stalled.compressor_rpm == 0
    assert working.power_output == -4973
    assert stalled.power_output == 0
    assert working.air_outlet_temperature == 23
    assert stalled.air_outlet_temperature == 45.3


def test_the_stop_reason_survives_into_a_running_cooling_cycle():
    """Test the stop reason is why the last cycle ended, not the current state."""
    pump = HeatPump("https://example.invalid", "heat-pump")
    pump._last_log = RawHeatpumpLogAndIsOnlineDto.from_dict(
        load("log_latest_cooling_active.json")
    )

    assert pump.heat_pump_state is HeatPump.State.COOLING
    assert pump.cooling_stop_reason is HeatPump.CoolingStopReason.HEAT_PUMP_CONTROL


def test_a_heat_pump_without_dhw_control_reports_no_target():
    """Test a heat pump with DHW control off reports a target of zero.

    Zero is how it says there is no target, not a target of zero degrees, so a
    consumer has to read it together with the control method.
    """
    pump = HeatPump("https://example.invalid", "heat-pump")
    pump._last_log = RawHeatpumpLogAndIsOnlineDto.from_dict(
        load("log_latest_dhw_method_none.json")
    )

    assert pump.dhw_control_method is HeatPump.DhwControlMethod.NONE
    assert pump.dhw_target_temperature == 0
