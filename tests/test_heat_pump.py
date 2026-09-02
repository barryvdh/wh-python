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
        ({"state": 132, "cooling_pause_reason": 0}, HeatPump.CoolingActivity.ACTIVE),
        ({"state": 131, "cooling_pause_reason": 0}, HeatPump.CoolingActivity.STARTING),
        ({"state": 136, "cooling_pause_reason": 0}, HeatPump.CoolingActivity.WATER_CHECK),
        ({"state": 40, "cooling_pause_reason": 0}, HeatPump.CoolingActivity.WAITING),
        ({"state": 40, "cooling_pause_reason": 4}, HeatPump.CoolingActivity.PAUSED),
        (
            {"state": 40, "cooling_pause_reason": 0, "cooling_stop_reason": 1},
            HeatPump.CoolingActivity.STOPPED,
        ),
        # a pause reason only counts while the heat pump is in standby
        ({"state": 70, "cooling_pause_reason": 4}, HeatPump.CoolingActivity.WAITING),
        # a heat pump that does not do cooling reports no cooling fields at all
        ({"state": 70}, None),
    ],
)
def test_cooling_activity(fields, expected):
    """Test the cooling status says what the heat pump is doing, or why it is not."""
    assert heat_pump(**fields).cooling_activity is expected


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (0, HeatPump.CoolingStatus.IDLE),
        (2, HeatPump.CoolingStatus.ACTIVE),
        (4, HeatPump.CoolingStatus.STANDBY),
        (99, None),
    ],
)
def test_cooling_status(status, expected):
    """Test the cooling status the heat pump reports in its log."""
    assert heat_pump(cooling_status=status).cooling_status is expected


def test_cooling_status_when_not_reported():
    """Test a heat pump that does not report a cooling status decodes to nothing."""
    assert heat_pump(state=40).cooling_status is None


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
    ("state", "power_in", "power_out", "expected"),
    [
        # heat into the water is what heating is for, so the ratio is positive
        (70, 500, 2000, 4.0),
        (150, 500, 2000, 4.0),
        # heat out of the water is what cooling is for, so that is positive too
        (132, 521, -2671, pytest.approx(5.126, abs=0.001)),
        # only cooling itself flips: defrosting and the water check take heat out
        # of the water too, but not as the point, so they stay negative
        (90, 500, -1000, -2.0),
        (136, 500, -1000, -2.0),
        # heat moving the wrong way for the state stays visible as a negative
        # ratio, rather than reading as a good one
        (132, 690, 7404, pytest.approx(-10.73, abs=0.01)),
        (70, 500, -500, -1.0),
        # without a state there is no way to tell, so report what was measured
        (None, 500, -500, -1.0),
    ],
)
def test_cop(state, power_in, power_out, expected):
    """Test the coefficient of performance follows the state it was measured in."""
    pump = heat_pump(state=state, cm_mass_power_in=power_in, cm_mass_power_out=power_out)

    assert pump.cop == expected


def test_cop_without_input_power():
    """Test nothing is drawn, so nothing is moved per unit drawn."""
    assert heat_pump(state=40, cm_mass_power_in=0, cm_mass_power_out=0).cop == 0


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


@pytest.mark.parametrize(
    ("code", "expected_name"),
    [(4, HeatPump.CoolingPauseReason.WATER_TEMPERATURE_BELOW_SETPOINT), (99, None)],
)
def test_a_code_is_reported_even_when_it_cannot_be_named(code, expected_name):
    """Test the code is reported whether or not this version can name it.

    That is what lets a consumer tell a heat pump reporting an unknown value
    apart from one not reporting the value at all.
    """
    pump = heat_pump(cooling_pause_reason=code)

    assert pump.cooling_pause_reason_code == code
    assert pump.cooling_pause_reason is expected_name


def test_no_code_is_reported_when_the_field_is_absent():
    """Test a heat pump that does not report the field reports no code either."""
    pump = heat_pump(state=40)

    assert pump.cooling_pause_reason_code is None
    assert pump.heat_pump_state_code == 40


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        (0, HeatPump.DhwControlMethod.NONE),
        (1, HeatPump.DhwControlMethod.FIXED),
        (2, HeatPump.DhwControlMethod.SCHEDULE),
        (3, HeatPump.DhwControlMethod.WEHEAT_INTELLIGENCE),
        (4, HeatPump.DhwControlMethod.BOOST),
        (99, None),
    ],
)
def test_dhw_control_method(code, expected):
    """Test the control method the DHW vessel runs on."""
    pump = heat_pump(dhw_control_method=code)

    assert pump.dhw_control_method is expected
    assert pump.dhw_control_method_code == code
