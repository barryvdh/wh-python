"""Weheat heat pump abstraction from the API."""
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, TypeVar, Union, Optional, cast

import aiohttp

from weheat import HeatPumpApi
from weheat.api.energy_log_api import EnergyLogApi
from weheat.api.heat_pump_log_api import HeatPumpLogApi
from weheat.api_client import ApiClient
from weheat.configuration import Configuration
from weheat.models import TotalEnergyAggregate, RawHeatpumpLogAndIsOnlineDto

T = TypeVar("T", bool, int, float)


class HeatPump:
    """Heat pump class representing a heat pump."""

    class State(Enum):
        OFFLINE = auto()
        STANDBY = auto()
        WATER_CHECK = auto()
        HEATING = auto()
        COOLING = auto()
        DHW = auto()
        LEGIONELLA_PREVENTION = auto()
        DEFROSTING = auto()
        SELF_TEST = auto()
        MANUAL_CONTROL = auto()
        UPDATING = auto()

    class CoolingState(Enum):
        IDLE = 130
        STARTING = 131
        ACTIVE = 132
        STOPPING = 133
        STANDBY = 134
        PAUSING = 135
        WATER_CHECK = 136
        STANDBY_RUN_CP = 137

    class CoolingActivity(Enum):
        """What the heat pump is doing about cooling, or why it is not cooling."""

        IDLE = auto()
        STARTING = auto()
        ACTIVE = auto()
        STOPPING = auto()
        STANDBY = auto()
        PAUSING = auto()
        WATER_CHECK = auto()
        STANDBY_RUN_CP = auto()
        PAUSED = auto()
        STOPPED = auto()
        WAITING = auto()

    class CoolingStatus(Enum):
        """The cooling status the heat pump reports in its log."""

        IDLE = 0
        STARTING = 1
        ACTIVE = 2
        STOPPING = 3
        STANDBY = 4

    class CoolingPauseReason(Enum):
        NONE = 0
        ROOM_TEMPERATURE_TOO_LOW = 1
        OUTSIDE_TEMPERATURE_TOO_LOW = 2
        OUTSIDE_COLDER_THAN_WATER_TEMPERATURE = 3
        WATER_TEMPERATURE_BELOW_SETPOINT = 4
        HEAT_PUMP_CONTROL = 5
        WATER_TEMPERATURE_BELOW_DEWPOINT = 6
        CONTACT_BLOCKED = 7
        DEMAND = 8

    class ControlMethod(Enum):
        NONE = 0
        HEATING_CURVE = 1
        ON_OFF_THERMOSTAT = 2
        BASE_OPEN_THERM = 3
        SMART_OPEN_THERM = 4
        CLOUD_THERMOSTAT = 5
        MANUAL_POWER = 6
        AUTO_INPUT_SELECT = 7
        MANUAL_SETPOINT = 8

    class CoolingStopReason(Enum):
        NONE = 0
        DTC = 1
        CONTROL_METHOD = 2
        NO_INDOOR_UNIT_COMMUNICATION = 3
        HEAT_PUMP_CONTROL = 4
        COOLING_CONTROL = 5
        CONTACT_SWITCH_OVER = 6
        THERMOSTAT_DISABLED = 7

    # The numeric states the heat pump reports while cooling, and while defrosting.
    DEFROST_STATES = frozenset({84, 90, 100, 110, 120, *range(200, 240)})
    COOLING_STATES = frozenset(state.value for state in CoolingState)

    # Bit masks of the conditions that must all be met before cooling can start.
    COOLING_START_CONDITION_BITS = {
        "control_method": 1,
        "dtc": 2,
        "outside_air_temperature": 4,
        "inside_temperature": 8,
        "indoor_unit_connected": 16,
        "water_to_air": 32,
        "demand": 64,
        "water_temperature": 128,
        "contact_not_blocked": 256,
        "exponential_backoff": 512,
        "heat_cool_delay": 1024,
    }

    def __init__(self, api_url: str, uuid: str, client_session: aiohttp.ClientSession | None = None) -> None:
        self._api_url = api_url
        self._uuid = uuid
        self._last_log: Union[RawHeatpumpLogAndIsOnlineDto, None] = None
        self._energy_total: Union[TotalEnergyAggregate, None] = None
        self._nominal_max_power: Union[float, None] = None
        self._client = client_session

    async def async_get_status(self, access_token: str) -> None:
        """Updates the heat pump instance with data from the API."""
        await self.async_get_logs(access_token)
        await self.async_get_energy(access_token)

    async def async_get_logs(self, access_token: str) -> None:
        """Updates the heat pump instance with data from the API."""
        try:
            config = Configuration(host=self._api_url, access_token=access_token, client_session=self._client)

            async with ApiClient(configuration=config) as client:
                # Set the max power once
                if self._nominal_max_power is None:
                    response = await HeatPumpApi(client).api_v1_heat_pumps_heat_pump_id_get_with_http_info(
                        heat_pump_id=self._uuid)

                    if response.status_code == 200:
                        self._set_nominal_max_power_for_model(response.data.model)

                response = await HeatPumpLogApi(
                    client
                ).api_v1_heat_pumps_heat_pump_id_logs_latest_get_with_http_info(
                    heat_pump_id=self._uuid)

                if response.status_code == 200:
                    self._last_log = response.data


        except Exception as e:
            self._last_log = None
            raise e

    async def async_get_energy(self, access_token: str) -> None:
        """Updates the heat pump instance with data from the API."""
        try:
            config = Configuration(host=self._api_url, access_token=access_token, client_session=self._client)

            async with ApiClient(configuration=config) as client:
                response = await EnergyLogApi(client).total_heat_pump_id_get_with_http_info(heat_pump_id=self._uuid)

                if response.status_code == 200:
                    # aggregate the energy consumption
                    self._energy_total = response.data

        except Exception as e:
            self._energy_total = None
            raise e

    def _if_available_and_valid(self, key: str) -> Optional[T]:
        """Return the value from the last logged value if available and not -1. None otherwise."""
        value = self._if_available(key)
        if value is not None and value != -1:
            return value
        return None

    def _if_available(self, key: str) -> Optional[T]:
        """Returns the value from the last logged value if available. None otherwise."""
        if self._last_log is not None and hasattr(self._last_log, key):
            return cast(T, getattr(self._last_log, key))
        return None

    def _set_nominal_max_power_for_model(self, model_id: int) -> None:
        # These numbers are the rpm at 100% power in the portal
        # RPM can go above 100% if the limit is increased in the portal.
        # except for the Flint, that cannot go above 100%.
        if model_id == 1:
            # BB60
            self._nominal_max_power = 5520
        elif 2 <= model_id <= 4:
            # SP60
            self._nominal_max_power = 5520
        elif model_id == 5:
            # Flint
            self._nominal_max_power = 5400
        else:
            # BB80
            self._nominal_max_power = 4500

    def __str__(self) -> str:
        return f"WeheatHeatPump(uuid={self._uuid}, last update={self._if_available('timestamp')})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def heat_pump_state_code(self) -> Union[int, None]:
        """The raw state the heat pump reports, named by heat_pump_state."""
        return self._if_available("state")

    @property
    def current_control_method_code(self) -> Union[int, None]:
        """The raw control method the heat pump reports, named by current_control_method."""
        return self._if_available("current_control_method")

    @property
    def cooling_pause_reason_code(self) -> Union[int, None]:
        """The raw pause reason the heat pump reports, named by cooling_pause_reason."""
        return self._if_available("cooling_pause_reason")

    @property
    def cooling_stop_reason_code(self) -> Union[int, None]:
        """The raw stop reason the heat pump reports, named by cooling_stop_reason."""
        return self._if_available("cooling_stop_reason")

    @property
    def raw_content(self) -> Optional[dict]:
        raw = {}
        if self._last_log:
            raw.update(vars(self._last_log))
        if self._energy_total:
            raw.update(vars(self._energy_total))
        return raw or None

    @property
    def is_online(self) -> Union[bool, None]:
        """Whether the heat pump was still reporting to the backend at the time of the last log."""
        return self._if_available("is_online")

    @property
    def water_inlet_temperature(self) -> Union[float, None]:
        """The heat pump water inlet temperature."""
        return self._if_available("t_water_in")

    @property
    def water_outlet_temperature(self) -> Union[float, None]:
        """The heat pump water outlet temperature."""
        return self._if_available("t_water_out")

    @property
    def water_house_in_temperature(self) -> Union[float, None]:
        """The water house in temperature."""
        return self._if_available("t_water_house_in")

    @property
    def air_inlet_temperature(self) -> Union[float, None]:
        """The heat pump air inlet temperature."""
        return self._if_available("t_air_in")

    @property
    def air_outlet_temperature(self) -> Union[float, None]:
        """The heat pump air outlet temperature."""
        return self._if_available("t_air_out")

    @property
    def thermostat_water_setpoint(self) -> Union[float, None]:
        """The  thermostat water setpoint."""
        return self._if_available("t_thermostat_setpoint")

    @property
    def thermostat_room_temperature(self) -> Union[float, None]:
        """The thermostat current room temperature."""
        return self._if_available_and_valid("t_room")

    @property
    def thermostat_room_temperature_setpoint(self) -> Union[float, None]:
        """The thermostat room temperature setpoint."""
        return self._if_available_and_valid("t_room_target")

    @property
    def thermostat_on_off_state(self) -> Union[bool, None]:
        """The thermostat on/off state."""
        return self._if_available("on_off_thermostat_state")

    @property
    def power_input(self) -> Union[float, None]:
        """The heat pumps power input."""
        return self._if_available("cm_mass_power_in")

    @property
    def power_output(self) -> Union[float, None]:
        """The heat pumps hydraulic output power."""
        return self._if_available("cm_mass_power_out")

    @property
    def dhw_top_temperature(self) -> Union[float, None]:
        """The DHW vessel top temperature."""
        return self._if_available("t1")

    @property
    def dhw_bottom_temperature(self) -> Union[float, None]:
        """The DHW vessel bottom temperature."""
        return self._if_available("t2")

    @property
    def dhw_target_temperature(self) -> Union[float, None]:
        """The DHW vessel target temperature."""
        return self._if_available_and_valid("dhw_target_temperature")

    @property
    def cop(self) -> Union[float, None]:
        """
        Returns the coefficient of performance of the heat pump.
        Note that this is calculated from a singular log entry and might not be accurate when the
        heat pump is changing its output power or switching states
        """
        input = self.power_input
        output = self.power_output
        # When either is not available, the calculation cannot be made.
        if input is None or output is None:
            return None

        if input > 0:
            # While cooling or defrosting the output power is negative, as heat is removed from
            # the water. The amount of energy moved per unit of input is still a positive ratio.
            return abs(output) / input

        return 0

    @property
    def indoor_unit_water_pump_state(self) -> Union[bool, None]:
        """Decoded water pump state."""
        return self._if_available("control_bridge_status_decoded_water_pump")

    @property
    def indoor_unit_auxiliary_pump_state(self) -> Union[bool, None]:
        """Decoded auxiliary pump state."""
        return self._if_available("control_bridge_status_decoded_water_pump2")

    @property
    def indoor_unit_dhw_valve_or_pump_state(self) -> Union[bool, None]:
        """Decoded DHW valve or pump state."""
        return self._if_available("control_bridge_status_decoded_dhw_valve")

    @property
    def indoor_unit_gas_boiler_state(self) -> Union[bool, None]:
        """Decoded gas boiler state."""
        return self._if_available("control_bridge_status_decoded_gas_boiler")

    @property
    def indoor_unit_electric_heater_state(self) -> Union[bool, None]:
        """Decoded electric heater state."""
        return self._if_available("control_bridge_status_decoded_electric_heater")

    @property
    def compressor_percentage(self) -> Union[int, None]:
        current_rpm = self._if_available("rpm")
        if self._nominal_max_power is not None and current_rpm is not None:
            # calculate percentage of rpm
            return int((100 / self._nominal_max_power) * current_rpm)
        return None

    @property
    def compressor_rpm(self) -> Union[float, None]:
        """Compressor RPM."""
        return self._if_available("rpm")

    @property
    def heat_pump_state(self) -> Union[State, None]:
        """The heat pump state."""
        numeric_state = self._if_available("state")
        if numeric_state is None:
            return None

        if numeric_state == 1:
            return self.State.OFFLINE
        if numeric_state == 40:
            return self.State.STANDBY
        elif numeric_state == 70:
            return self.State.HEATING
        elif numeric_state == self.CoolingState.WATER_CHECK.value:
            return self.State.WATER_CHECK
        elif numeric_state in self.COOLING_STATES:
            return self.State.COOLING
        elif numeric_state == 150:
            return self.State.DHW
        elif numeric_state == 160:
            return self.State.LEGIONELLA_PREVENTION
        elif numeric_state == 170:
            return self.State.SELF_TEST
        elif numeric_state == 180:
            return self.State.MANUAL_CONTROL
        elif numeric_state == 1010:
            return self.State.UPDATING
        elif numeric_state in self.DEFROST_STATES:
            return self.State.DEFROSTING
        return None

    @property
    def last_cooling_time(self) -> Union[datetime, None]:
        """The last completed cooling cycle, which the restart delay is counted from.

        This is not updated while a cooling cycle is running, so during cooling it still
        refers to the cycle before it.
        """
        return cast(Optional[datetime], self._if_available("last_cooling_time"))

    @property
    def current_control_method(self) -> Union["HeatPump.ControlMethod", None]:
        """The control method the heat pump is currently running on."""
        value = self._if_available("current_control_method")
        if value is None:
            return None
        try:
            return self.ControlMethod(value)
        except ValueError:
            # The backend may report methods this version does not know about yet.
            return None

    @property
    def cooling_state(self) -> Union["HeatPump.CoolingState", None]:
        """The cooling sub state, only set while the heat pump is in a cooling state."""
        value = self._if_available("state")
        if value is None:
            return None
        try:
            return self.CoolingState(value)
        except ValueError:
            return None

    @property
    def cooling_status(self) -> Union["HeatPump.CoolingStatus", None]:
        """The cooling status the heat pump reports, if it reports one."""
        value = self._if_available("cooling_status")
        if value is None:
            return None
        try:
            return self.CoolingStatus(value)
        except ValueError:
            # The backend may report a status this version does not know about yet.
            return None

    @property
    def cooling_activity(self) -> Union["HeatPump.CoolingActivity", None]:
        """What the heat pump is doing about cooling, or why it is not cooling.

        The heat pump only reports a cooling state during a cooling cycle, so
        outside one this reports whether cooling is paused, stopped, or waiting
        for its start conditions. None when the heat pump does not do cooling.
        """
        cooling_state = self.cooling_state
        if cooling_state is not None:
            return self.CoolingActivity[cooling_state.name]
        if self._if_available("cooling_pause_reason") is None:
            return None
        if self.heat_pump_state is self.State.STANDBY:
            if self.cooling_pause_reason not in (None, self.CoolingPauseReason.NONE):
                return self.CoolingActivity.PAUSED
            if self.cooling_stop_reason not in (None, self.CoolingStopReason.NONE):
                return self.CoolingActivity.STOPPED
        return self.CoolingActivity.WAITING

    @property
    def cooling_pause_reason(self) -> Union["HeatPump.CoolingPauseReason", None]:
        """The reason cooling is currently held off."""
        value = self._if_available("cooling_pause_reason")
        if value is None:
            return None
        try:
            return self.CoolingPauseReason(value)
        except ValueError:
            # The backend may report reasons this version does not know about yet.
            return None

    @property
    def cooling_stop_reason(self) -> Union["HeatPump.CoolingStopReason", None]:
        """The reason the last cooling cycle was stopped."""
        value = self._if_available("cooling_stop_reason")
        if value is None:
            return None
        try:
            return self.CoolingStopReason(value)
        except ValueError:
            # The backend may report reasons this version does not know about yet.
            return None

    @property
    def cooling_backoff(self) -> Union[int, None]:
        """The minutes to wait after a cooling cycle before cooling may start again."""
        return self._if_available("cooling_exponential_backoff")

    @property
    def cooling_available_from(self) -> Union[datetime, None]:
        """The moment the wait time after the last cooling cycle expires."""
        last_cooling_time = self.last_cooling_time
        if last_cooling_time is None:
            return None
        return last_cooling_time + timedelta(minutes=self.cooling_backoff or 0)

    @property
    def cooling_start_conditions(self) -> Union[Dict[str, bool], None]:
        """Each condition for starting cooling, and whether it is currently met."""
        value = self._if_available("cooling_start_conditions")
        if value is None:
            return None
        return {
            name: bool(value & bit)
            for name, bit in self.COOLING_START_CONDITION_BITS.items()
        }

    @staticmethod
    def _pwm_to_volume(pwm: float, max: float) -> Union[float, None]:
        """Calculate PWM to Volume in m3/h based on the max available volume"""

        # 0 or > 75 are abnormal states. 255 = Off
        if pwm < 1 or pwm > 75:
            return None

        # 2 = standby
        if pwm <= 5:
            return 0

        # 5-75 is linear from 0 to max
        return ((pwm - 5) / 70) * max

    @property
    def dhw_flow_volume(self) -> Union[float, None]:
        """The DHW Flow in m3/h."""
        pwm = pwm = self._if_available("dhw_flow")
        if pwm is None:
            return None

        return self._pwm_to_volume(pwm, max=2.1)

    @property
    def central_heating_flow_volume(self) -> Union[float, None]:
        """The Central Heating Flow in m3/h."""
        pwm = pwm = self._if_available("central_heating_flow")
        if pwm is None:
            return None

        return self._pwm_to_volume(pwm, max=2.1)

    @property
    def energy_in_heating(self) -> Union[float, None]:
        """The total used energy in heating mode."""
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_ein_heating)

    @property
    def energy_in_dhw(self) -> Union[float, None]:
        """The total used energy in DHW mode."""
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_ein_dhw)

    @property
    def energy_in_defrost(self) -> Union[float, None]:
        """The total used energy in defrost modes."""
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_ein_heating_defrost + self._energy_total.total_ein_dhw_defrost)

    @property
    def energy_in_defrost_dhw(self) -> Union[float, None]:
        """The total used energy in defrost from DHW mode."""
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_ein_dhw_defrost)

    @property
    def energy_in_defrost_ch(self) -> Union[float, None]:
        """The total used energy in defrost from CH mode."""
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_ein_heating_defrost)

    @property
    def energy_in_cooling(self) -> Union[float, None]:
        """The total used energy in cooling mode."""
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_ein_cooling)

    @property
    def energy_in_standby(self) -> Union[float, None]:
        """The total used energy in standby mode."""
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_ein_standby)
        
    @property
    def energy_out_heating(self) -> Union[float, None]:
        """The total supplied energy in heating mode."""
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_e_out_heating)

    @property
    def energy_out_dhw(self) -> Union[float, None]:
        """The total supplied energy in DHW mode."""
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_e_out_dhw)

    @property
    def energy_out_defrost(self) -> Union[float, None]:
        """The total supplied energy in defrost modes.
        Note that this energy value is negative as energy is removed from the water.
        """
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_e_out_dhw_defrost + self._energy_total.total_e_out_heating_defrost)

    @property
    def energy_out_defrost_dhw(self) -> Union[float, None]:
        """The total supplied energy in defrost DHW mode.
        Note that this energy value is negative as energy is removed from the water.
        """
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_e_out_dhw_defrost)

    @property
    def energy_out_defrost_ch(self) -> Union[float, None]:
        """The total supplied energy in defrost CH mode.
        Note that this energy value is negative as energy is removed from the water.
        """
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_e_out_heating_defrost)

    @property
    def energy_out_cooling(self) -> Union[float, None]:
        """The total supplied energy in cooling mode.
        Note that this energy value is negative as energy is removed from the water.
        """
        if self._energy_total is None:
            return None
        return float(self._energy_total.total_e_out_cooling)

    @property
    def energy_total(self) -> Union[float, None]:
        """The total used (electrical) energy of the outdoor unit in kWh.

        This does not include the indoor unit, which the heat pump meters
        separately and reports through energy_in_indoor_unit.
        """
        if self._energy_total is None:
            return None
        return float(
            self._energy_total.total_ein_heating + self._energy_total.total_ein_dhw + 
            self._energy_total.total_ein_cooling + self._energy_total.total_ein_standby +
            self._energy_total.total_ein_heating_defrost + self._energy_total.total_ein_dhw_defrost
        )

    @property
    def energy_in_indoor_unit(self) -> Union[float, None]:
        """The total used (electrical) energy of the indoor unit in kWh."""
        if self._energy_total is None:
            return None
        return float(
            self._energy_total.total_ein_iu_heating + self._energy_total.total_ein_iu_dhw +
            self._energy_total.total_ein_iu_cooling + self._energy_total.total_ein_iu_standby +
            self._energy_total.total_ein_iu_heating_defrost +
            self._energy_total.total_ein_iu_dhw_defrost
        )

    @property
    def energy_output(self) -> Union[float, None]:
        """The total useful generated energy for the house in kWh."""
        if self._energy_total is None:
            return None
        return float(
            self._energy_total.total_e_out_heating + self._energy_total.total_e_out_dhw +
            self._energy_total.total_e_out_heating_defrost + self._energy_total.total_e_out_dhw_defrost +
            (-self._energy_total.total_e_out_cooling))
