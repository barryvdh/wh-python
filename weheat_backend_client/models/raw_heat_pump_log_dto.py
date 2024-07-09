# coding: utf-8

"""
    Weheat Backend

    This is the backend for the Weheat project

    The version of the OpenAPI document: v1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Union
from pydantic import BaseModel, StrictBool, StrictFloat, StrictInt, StrictStr
from pydantic import Field
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class RawHeatPumpLogDto(BaseModel):
    """
    Raw heat pump log as given by a heat pump  (Required star states that it will always be there for any roll, otherwise it is filtered for customers)
    """ # noqa: E501
    heat_pump_id: StrictStr = Field(description="Identifier of the Heat Pump", alias="heatPumpId")
    timestamp: datetime = Field(description="Timestamp of when this was logged to the server")
    firmware_revision: Optional[StrictInt] = Field(default=None, description="Version of heat pump logs (should be 1026)", alias="firmwareRevision")
    packet_counter: Optional[StrictInt] = Field(default=None, description="Packet counter of inside the control board", alias="packetCounter")
    unix_time_mcu: Optional[StrictInt] = Field(default=None, description="Unix time inside the control board at the time it send this log", alias="unixTimeMcu")
    state: Optional[StrictInt] = Field(default=None, description="Current heat pump state (which is decoded in the view)")
    rpm_ctrl: Optional[StrictInt] = Field(default=None, description="Current mode of RPM control (which is decoded in the view)", alias="rpmCtrl")
    error: Optional[StrictInt] = Field(default=None, description="Current state of error in the heat pump (which is decoded in the view)")
    error_decoded_dtc_none: Optional[StrictBool] = Field(default=None, description="None state of the error flag which isn't raw for practical timescale purposes (it was bitwise encoded)", alias="errorDecodedDtcNone")
    error_decoded_dtc_continue: Optional[StrictBool] = Field(default=None, description="DTC continue state of the error flag which isn't raw for practical timescale purposes (it was bitwise encoded)", alias="errorDecodedDtcContinue")
    error_decoded_dtc_compressor_off: Optional[StrictBool] = Field(default=None, description="DTC off state of the error flag which isn't raw for practical timescale purposes (it was bitwise encoded)", alias="errorDecodedDtcCompressorOff")
    error_decoded_dtc_defrost_forbidden: Optional[StrictBool] = Field(default=None, description="DTC defrost forbidden state of the error flag which isn't raw for practical timescale purposes (it was bitwise encoded)", alias="errorDecodedDtcDefrostForbidden")
    error_decoded_dtc_request_service: Optional[StrictBool] = Field(default=None, description="DTC request service state of the error flag which isn't raw for practical timescale purposes (it was bitwise encoded)", alias="errorDecodedDtcRequestService")
    error_decoded_dtc_use_heating_curve: Optional[StrictBool] = Field(default=None, description="DTC use heating curve state of the error flag which isn't raw for practical timescale purposes (it was bitwise encoded)", alias="errorDecodedDtcUseHeatingCurve")
    error_decoded_dtc_dhw_forbidden: Optional[StrictBool] = Field(default=None, description="DTC use heating curve state of the error flag which isn't raw for practical timescale purposes (it was bitwise encoded)", alias="errorDecodedDtcDhwForbidden")
    error_decoded_dtc_error: Optional[StrictBool] = Field(default=None, description="DTC use heating curve state of the error flag which isn't raw for practical timescale purposes (it was bitwise encoded)", alias="errorDecodedDtcError")
    error_decoded_dtc_inactive: Optional[StrictBool] = Field(default=None, description="DTC Inactive state of the error flag which isn't raw for practical timescale purposes (it was bitwise encoded)", alias="errorDecodedDtcInactive")
    heatsink: Optional[StrictInt] = Field(default=None, description="Raw state of the where the heat pump is dumping it's heat")
    si5: Optional[StrictInt] = Field(default=None, description="Raw state of the heat pump")
    e80: Optional[StrictInt] = Field(default=None, description="Raw error code state 80 of the heat pump")
    e81: Optional[StrictInt] = Field(default=None, description="Raw error code state 81 of the heat pump")
    e84: Optional[StrictInt] = Field(default=None, description="Raw error code state 84 of the heat pump")
    e85: Optional[StrictInt] = Field(default=None, description="Raw error code state 85 of the heat pump")
    control_bridge_status: Optional[StrictInt] = Field(default=None, description="Raw control bridge status of the heat pump (bitwise encoded)", alias="controlBridgeStatus")
    control_bridge_status_decoded_water_pump: Optional[StrictBool] = Field(default=None, description="Water pump (requested) on/off flag of the control bridge status (0x01)", alias="controlBridgeStatusDecodedWaterPump")
    control_bridge_status_decoded_dhw_valve: Optional[StrictBool] = Field(default=None, description="DhwValve (requested) open/closed flag of the control bridge status (0x02) (DHW Only)", alias="controlBridgeStatusDecodedDhwValve")
    control_bridge_status_decoded_gas_boiler: Optional[StrictBool] = Field(default=None, description="Gas boiler assistance (requested) on/off flag of the control bridge status (0x04) (Hybrid Only)", alias="controlBridgeStatusDecodedGasBoiler")
    control_bridge_status_decoded_electric_heater: Optional[StrictBool] = Field(default=None, description="Electric heater assistance (requested) on/off flag of the control bridge status (0x08) (DHW Only)", alias="controlBridgeStatusDecodedElectricHeater")
    control_bridge_status_decoded_water_pump2: Optional[StrictBool] = Field(default=None, description="Second water pump (requested) on/off flag of the control bridge status (0x010) (DHW Only)", alias="controlBridgeStatusDecodedWaterPump2")
    input_status: Optional[StrictInt] = Field(default=None, description="Raw input status of the heat pump", alias="inputStatus")
    current_control_method: Optional[StrictInt] = Field(default=None, description="Raw current control method state of the heat pump", alias="currentControlMethod")
    signal_strength: Optional[StrictInt] = Field(default=None, description="Signal strength (rssi) reported by the modem of the control board", alias="signalStrength")
    t1: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature T1 (TOP) of the DHW sensors")
    t2: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature T2 (BOTTOM) of the DHW sensors")
    t_spare_ntc: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Spare temperature sensor (for DHW)", alias="tSpareNtc")
    t_board: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature of the control board", alias="tBoard")
    t_air_in: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature of the air going into the heat pump", alias="tAirIn")
    t_air_out: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature of the air going out of the heat pump", alias="tAirOut")
    t_water_in: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature of the water going into the heat pump", alias="tWaterIn")
    t_water_out: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature of the water going out of the heat pump", alias="tWaterOut")
    t_water_house_in: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature of the water going into the building", alias="tWaterHouseIn")
    rpm: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Rpm of the compressor")
    rpm_limiter: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Rpm limit of the compressor", alias="rpmLimiter")
    rpm_limiter_type: Optional[StrictInt] = Field(default=None, description="Type of why the rpm is limited", alias="rpmLimiterType")
    p_compressor_in: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Pressure of the compressor of the side where air goes into the compressor", alias="pCompressorIn")
    p_compressor_out: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Pressure of the compressor of the side where air goes out of the compressor", alias="pCompressorOut")
    p_compressor_in_target: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Target pressure of the compressor of the side where air goes into the compressor", alias="pCompressorInTarget")
    t_inverter: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature of the inverter", alias="tInverter")
    t_compressor_in: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature of the compressor of the side where air goes into the compressor", alias="tCompressorIn")
    t_compressor_out: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature of the compressor of the side where air goes out of the compressor", alias="tCompressorOut")
    t_compressor_in_transient: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature transient of the compressor of the side where air goes into the compressor", alias="tCompressorInTransient")
    t_compressor_out_transient: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature transient of the compressor of the side where air goes out of the compressor", alias="tCompressorOutTransient")
    delta_t_compressor_in_superheat: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Difference in temperature for superheat based on the compressor temperatures", alias="deltaTCompressorInSuperheat")
    compressor_power_low_accuracy: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Power used by the compressor (low accuracy)", alias="compressorPowerLowAccuracy")
    fan: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="State of the fan")
    fan_power: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Power used by the fan", alias="fanPower")
    valve: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Position value of the valve")
    exv_flow_step_gain: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, alias="exvFlowStepGain")
    cm_mass_flow: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Flow of the water going through the heat pump", alias="cmMassFlow")
    cm_mass_power_in: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Power going into the heat pump", alias="cmMassPowerIn")
    cm_mass_power_out: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Power going out of the heat pump (in the form of usable heat)", alias="cmMassPowerOut")
    p_requested: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Power requested by the heat pump", alias="pRequested")
    power_error_integral: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Current value of the power error integral", alias="powerErrorIntegral")
    on_off_thermostat_state: Optional[StrictInt] = Field(default=None, description="State of the on/off thermostat", alias="onOffThermostatState")
    thermostat_status: Optional[StrictInt] = Field(default=None, description="Status of the OpenTherm thermostat", alias="thermostatStatus")
    t_room: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Temperature of the room given by the OpenTherm thermostat", alias="tRoom")
    t_room_target: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Target temperature of the room given by the OpenTherm thermostat", alias="tRoomTarget")
    t_thermostat_setpoint: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Setpoint temperature of the OpenTherm thermostat OR the water setpoint of the heat pump", alias="tThermostatSetpoint")
    ot_boiler_status: Optional[StrictInt] = Field(default=None, description="Status of the OpenTherm boiler", alias="otBoilerStatus")
    ot_boiler_feed_temperature: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Feed temperature of the OpenTherm boiler", alias="otBoilerFeedTemperature")
    ot_boiler_return_temperature: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Return temperature of the OpenTherm boiler", alias="otBoilerReturnTemperature")
    interval: StrictInt = Field(description="Interval for this log in seconds")
    __properties: ClassVar[List[str]] = ["heatPumpId", "timestamp", "firmwareRevision", "packetCounter", "unixTimeMcu", "state", "rpmCtrl", "error", "errorDecodedDtcNone", "errorDecodedDtcContinue", "errorDecodedDtcCompressorOff", "errorDecodedDtcDefrostForbidden", "errorDecodedDtcRequestService", "errorDecodedDtcUseHeatingCurve", "errorDecodedDtcDhwForbidden", "errorDecodedDtcError", "errorDecodedDtcInactive", "heatsink", "si5", "e80", "e81", "e84", "e85", "controlBridgeStatus", "controlBridgeStatusDecodedWaterPump", "controlBridgeStatusDecodedDhwValve", "controlBridgeStatusDecodedGasBoiler", "controlBridgeStatusDecodedElectricHeater", "controlBridgeStatusDecodedWaterPump2", "inputStatus", "currentControlMethod", "signalStrength", "t1", "t2", "tSpareNtc", "tBoard", "tAirIn", "tAirOut", "tWaterIn", "tWaterOut", "tWaterHouseIn", "rpm", "rpmLimiter", "rpmLimiterType", "pCompressorIn", "pCompressorOut", "pCompressorInTarget", "tInverter", "tCompressorIn", "tCompressorOut", "tCompressorInTransient", "tCompressorOutTransient", "deltaTCompressorInSuperheat", "compressorPowerLowAccuracy", "fan", "fanPower", "valve", "exvFlowStepGain", "cmMassFlow", "cmMassPowerIn", "cmMassPowerOut", "pRequested", "powerErrorIntegral", "onOffThermostatState", "thermostatStatus", "tRoom", "tRoomTarget", "tThermostatSetpoint", "otBoilerStatus", "otBoilerFeedTemperature", "otBoilerReturnTemperature", "interval"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of RawHeatPumpLogDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # set to None if firmware_revision (nullable) is None
        # and model_fields_set contains the field
        if self.firmware_revision is None and "firmware_revision" in self.model_fields_set:
            _dict['firmwareRevision'] = None

        # set to None if packet_counter (nullable) is None
        # and model_fields_set contains the field
        if self.packet_counter is None and "packet_counter" in self.model_fields_set:
            _dict['packetCounter'] = None

        # set to None if unix_time_mcu (nullable) is None
        # and model_fields_set contains the field
        if self.unix_time_mcu is None and "unix_time_mcu" in self.model_fields_set:
            _dict['unixTimeMcu'] = None

        # set to None if error (nullable) is None
        # and model_fields_set contains the field
        if self.error is None and "error" in self.model_fields_set:
            _dict['error'] = None

        # set to None if error_decoded_dtc_none (nullable) is None
        # and model_fields_set contains the field
        if self.error_decoded_dtc_none is None and "error_decoded_dtc_none" in self.model_fields_set:
            _dict['errorDecodedDtcNone'] = None

        # set to None if error_decoded_dtc_continue (nullable) is None
        # and model_fields_set contains the field
        if self.error_decoded_dtc_continue is None and "error_decoded_dtc_continue" in self.model_fields_set:
            _dict['errorDecodedDtcContinue'] = None

        # set to None if error_decoded_dtc_compressor_off (nullable) is None
        # and model_fields_set contains the field
        if self.error_decoded_dtc_compressor_off is None and "error_decoded_dtc_compressor_off" in self.model_fields_set:
            _dict['errorDecodedDtcCompressorOff'] = None

        # set to None if error_decoded_dtc_defrost_forbidden (nullable) is None
        # and model_fields_set contains the field
        if self.error_decoded_dtc_defrost_forbidden is None and "error_decoded_dtc_defrost_forbidden" in self.model_fields_set:
            _dict['errorDecodedDtcDefrostForbidden'] = None

        # set to None if error_decoded_dtc_request_service (nullable) is None
        # and model_fields_set contains the field
        if self.error_decoded_dtc_request_service is None and "error_decoded_dtc_request_service" in self.model_fields_set:
            _dict['errorDecodedDtcRequestService'] = None

        # set to None if error_decoded_dtc_use_heating_curve (nullable) is None
        # and model_fields_set contains the field
        if self.error_decoded_dtc_use_heating_curve is None and "error_decoded_dtc_use_heating_curve" in self.model_fields_set:
            _dict['errorDecodedDtcUseHeatingCurve'] = None

        # set to None if error_decoded_dtc_dhw_forbidden (nullable) is None
        # and model_fields_set contains the field
        if self.error_decoded_dtc_dhw_forbidden is None and "error_decoded_dtc_dhw_forbidden" in self.model_fields_set:
            _dict['errorDecodedDtcDhwForbidden'] = None

        # set to None if error_decoded_dtc_error (nullable) is None
        # and model_fields_set contains the field
        if self.error_decoded_dtc_error is None and "error_decoded_dtc_error" in self.model_fields_set:
            _dict['errorDecodedDtcError'] = None

        # set to None if error_decoded_dtc_inactive (nullable) is None
        # and model_fields_set contains the field
        if self.error_decoded_dtc_inactive is None and "error_decoded_dtc_inactive" in self.model_fields_set:
            _dict['errorDecodedDtcInactive'] = None

        # set to None if heatsink (nullable) is None
        # and model_fields_set contains the field
        if self.heatsink is None and "heatsink" in self.model_fields_set:
            _dict['heatsink'] = None

        # set to None if si5 (nullable) is None
        # and model_fields_set contains the field
        if self.si5 is None and "si5" in self.model_fields_set:
            _dict['si5'] = None

        # set to None if e80 (nullable) is None
        # and model_fields_set contains the field
        if self.e80 is None and "e80" in self.model_fields_set:
            _dict['e80'] = None

        # set to None if e81 (nullable) is None
        # and model_fields_set contains the field
        if self.e81 is None and "e81" in self.model_fields_set:
            _dict['e81'] = None

        # set to None if e84 (nullable) is None
        # and model_fields_set contains the field
        if self.e84 is None and "e84" in self.model_fields_set:
            _dict['e84'] = None

        # set to None if e85 (nullable) is None
        # and model_fields_set contains the field
        if self.e85 is None and "e85" in self.model_fields_set:
            _dict['e85'] = None

        # set to None if control_bridge_status (nullable) is None
        # and model_fields_set contains the field
        if self.control_bridge_status is None and "control_bridge_status" in self.model_fields_set:
            _dict['controlBridgeStatus'] = None

        # set to None if control_bridge_status_decoded_water_pump (nullable) is None
        # and model_fields_set contains the field
        if self.control_bridge_status_decoded_water_pump is None and "control_bridge_status_decoded_water_pump" in self.model_fields_set:
            _dict['controlBridgeStatusDecodedWaterPump'] = None

        # set to None if control_bridge_status_decoded_dhw_valve (nullable) is None
        # and model_fields_set contains the field
        if self.control_bridge_status_decoded_dhw_valve is None and "control_bridge_status_decoded_dhw_valve" in self.model_fields_set:
            _dict['controlBridgeStatusDecodedDhwValve'] = None

        # set to None if control_bridge_status_decoded_gas_boiler (nullable) is None
        # and model_fields_set contains the field
        if self.control_bridge_status_decoded_gas_boiler is None and "control_bridge_status_decoded_gas_boiler" in self.model_fields_set:
            _dict['controlBridgeStatusDecodedGasBoiler'] = None

        # set to None if control_bridge_status_decoded_electric_heater (nullable) is None
        # and model_fields_set contains the field
        if self.control_bridge_status_decoded_electric_heater is None and "control_bridge_status_decoded_electric_heater" in self.model_fields_set:
            _dict['controlBridgeStatusDecodedElectricHeater'] = None

        # set to None if control_bridge_status_decoded_water_pump2 (nullable) is None
        # and model_fields_set contains the field
        if self.control_bridge_status_decoded_water_pump2 is None and "control_bridge_status_decoded_water_pump2" in self.model_fields_set:
            _dict['controlBridgeStatusDecodedWaterPump2'] = None

        # set to None if input_status (nullable) is None
        # and model_fields_set contains the field
        if self.input_status is None and "input_status" in self.model_fields_set:
            _dict['inputStatus'] = None

        # set to None if current_control_method (nullable) is None
        # and model_fields_set contains the field
        if self.current_control_method is None and "current_control_method" in self.model_fields_set:
            _dict['currentControlMethod'] = None

        # set to None if signal_strength (nullable) is None
        # and model_fields_set contains the field
        if self.signal_strength is None and "signal_strength" in self.model_fields_set:
            _dict['signalStrength'] = None

        # set to None if t1 (nullable) is None
        # and model_fields_set contains the field
        if self.t1 is None and "t1" in self.model_fields_set:
            _dict['t1'] = None

        # set to None if t2 (nullable) is None
        # and model_fields_set contains the field
        if self.t2 is None and "t2" in self.model_fields_set:
            _dict['t2'] = None

        # set to None if t_spare_ntc (nullable) is None
        # and model_fields_set contains the field
        if self.t_spare_ntc is None and "t_spare_ntc" in self.model_fields_set:
            _dict['tSpareNtc'] = None

        # set to None if t_board (nullable) is None
        # and model_fields_set contains the field
        if self.t_board is None and "t_board" in self.model_fields_set:
            _dict['tBoard'] = None

        # set to None if rpm (nullable) is None
        # and model_fields_set contains the field
        if self.rpm is None and "rpm" in self.model_fields_set:
            _dict['rpm'] = None

        # set to None if rpm_limiter (nullable) is None
        # and model_fields_set contains the field
        if self.rpm_limiter is None and "rpm_limiter" in self.model_fields_set:
            _dict['rpmLimiter'] = None

        # set to None if rpm_limiter_type (nullable) is None
        # and model_fields_set contains the field
        if self.rpm_limiter_type is None and "rpm_limiter_type" in self.model_fields_set:
            _dict['rpmLimiterType'] = None

        # set to None if p_compressor_in (nullable) is None
        # and model_fields_set contains the field
        if self.p_compressor_in is None and "p_compressor_in" in self.model_fields_set:
            _dict['pCompressorIn'] = None

        # set to None if p_compressor_out (nullable) is None
        # and model_fields_set contains the field
        if self.p_compressor_out is None and "p_compressor_out" in self.model_fields_set:
            _dict['pCompressorOut'] = None

        # set to None if p_compressor_in_target (nullable) is None
        # and model_fields_set contains the field
        if self.p_compressor_in_target is None and "p_compressor_in_target" in self.model_fields_set:
            _dict['pCompressorInTarget'] = None

        # set to None if t_inverter (nullable) is None
        # and model_fields_set contains the field
        if self.t_inverter is None and "t_inverter" in self.model_fields_set:
            _dict['tInverter'] = None

        # set to None if t_compressor_in (nullable) is None
        # and model_fields_set contains the field
        if self.t_compressor_in is None and "t_compressor_in" in self.model_fields_set:
            _dict['tCompressorIn'] = None

        # set to None if t_compressor_out (nullable) is None
        # and model_fields_set contains the field
        if self.t_compressor_out is None and "t_compressor_out" in self.model_fields_set:
            _dict['tCompressorOut'] = None

        # set to None if t_compressor_in_transient (nullable) is None
        # and model_fields_set contains the field
        if self.t_compressor_in_transient is None and "t_compressor_in_transient" in self.model_fields_set:
            _dict['tCompressorInTransient'] = None

        # set to None if t_compressor_out_transient (nullable) is None
        # and model_fields_set contains the field
        if self.t_compressor_out_transient is None and "t_compressor_out_transient" in self.model_fields_set:
            _dict['tCompressorOutTransient'] = None

        # set to None if delta_t_compressor_in_superheat (nullable) is None
        # and model_fields_set contains the field
        if self.delta_t_compressor_in_superheat is None and "delta_t_compressor_in_superheat" in self.model_fields_set:
            _dict['deltaTCompressorInSuperheat'] = None

        # set to None if compressor_power_low_accuracy (nullable) is None
        # and model_fields_set contains the field
        if self.compressor_power_low_accuracy is None and "compressor_power_low_accuracy" in self.model_fields_set:
            _dict['compressorPowerLowAccuracy'] = None

        # set to None if fan (nullable) is None
        # and model_fields_set contains the field
        if self.fan is None and "fan" in self.model_fields_set:
            _dict['fan'] = None

        # set to None if fan_power (nullable) is None
        # and model_fields_set contains the field
        if self.fan_power is None and "fan_power" in self.model_fields_set:
            _dict['fanPower'] = None

        # set to None if valve (nullable) is None
        # and model_fields_set contains the field
        if self.valve is None and "valve" in self.model_fields_set:
            _dict['valve'] = None

        # set to None if exv_flow_step_gain (nullable) is None
        # and model_fields_set contains the field
        if self.exv_flow_step_gain is None and "exv_flow_step_gain" in self.model_fields_set:
            _dict['exvFlowStepGain'] = None

        # set to None if cm_mass_flow (nullable) is None
        # and model_fields_set contains the field
        if self.cm_mass_flow is None and "cm_mass_flow" in self.model_fields_set:
            _dict['cmMassFlow'] = None

        # set to None if cm_mass_power_in (nullable) is None
        # and model_fields_set contains the field
        if self.cm_mass_power_in is None and "cm_mass_power_in" in self.model_fields_set:
            _dict['cmMassPowerIn'] = None

        # set to None if cm_mass_power_out (nullable) is None
        # and model_fields_set contains the field
        if self.cm_mass_power_out is None and "cm_mass_power_out" in self.model_fields_set:
            _dict['cmMassPowerOut'] = None

        # set to None if p_requested (nullable) is None
        # and model_fields_set contains the field
        if self.p_requested is None and "p_requested" in self.model_fields_set:
            _dict['pRequested'] = None

        # set to None if power_error_integral (nullable) is None
        # and model_fields_set contains the field
        if self.power_error_integral is None and "power_error_integral" in self.model_fields_set:
            _dict['powerErrorIntegral'] = None

        # set to None if thermostat_status (nullable) is None
        # and model_fields_set contains the field
        if self.thermostat_status is None and "thermostat_status" in self.model_fields_set:
            _dict['thermostatStatus'] = None

        # set to None if t_room (nullable) is None
        # and model_fields_set contains the field
        if self.t_room is None and "t_room" in self.model_fields_set:
            _dict['tRoom'] = None

        # set to None if t_room_target (nullable) is None
        # and model_fields_set contains the field
        if self.t_room_target is None and "t_room_target" in self.model_fields_set:
            _dict['tRoomTarget'] = None

        # set to None if ot_boiler_status (nullable) is None
        # and model_fields_set contains the field
        if self.ot_boiler_status is None and "ot_boiler_status" in self.model_fields_set:
            _dict['otBoilerStatus'] = None

        # set to None if ot_boiler_feed_temperature (nullable) is None
        # and model_fields_set contains the field
        if self.ot_boiler_feed_temperature is None and "ot_boiler_feed_temperature" in self.model_fields_set:
            _dict['otBoilerFeedTemperature'] = None

        # set to None if ot_boiler_return_temperature (nullable) is None
        # and model_fields_set contains the field
        if self.ot_boiler_return_temperature is None and "ot_boiler_return_temperature" in self.model_fields_set:
            _dict['otBoilerReturnTemperature'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of RawHeatPumpLogDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "heatPumpId": obj.get("heatPumpId"),
            "timestamp": obj.get("timestamp"),
            "firmwareRevision": obj.get("firmwareRevision"),
            "packetCounter": obj.get("packetCounter"),
            "unixTimeMcu": obj.get("unixTimeMcu"),
            "state": obj.get("state"),
            "rpmCtrl": obj.get("rpmCtrl"),
            "error": obj.get("error"),
            "errorDecodedDtcNone": obj.get("errorDecodedDtcNone"),
            "errorDecodedDtcContinue": obj.get("errorDecodedDtcContinue"),
            "errorDecodedDtcCompressorOff": obj.get("errorDecodedDtcCompressorOff"),
            "errorDecodedDtcDefrostForbidden": obj.get("errorDecodedDtcDefrostForbidden"),
            "errorDecodedDtcRequestService": obj.get("errorDecodedDtcRequestService"),
            "errorDecodedDtcUseHeatingCurve": obj.get("errorDecodedDtcUseHeatingCurve"),
            "errorDecodedDtcDhwForbidden": obj.get("errorDecodedDtcDhwForbidden"),
            "errorDecodedDtcError": obj.get("errorDecodedDtcError"),
            "errorDecodedDtcInactive": obj.get("errorDecodedDtcInactive"),
            "heatsink": obj.get("heatsink"),
            "si5": obj.get("si5"),
            "e80": obj.get("e80"),
            "e81": obj.get("e81"),
            "e84": obj.get("e84"),
            "e85": obj.get("e85"),
            "controlBridgeStatus": obj.get("controlBridgeStatus"),
            "controlBridgeStatusDecodedWaterPump": obj.get("controlBridgeStatusDecodedWaterPump"),
            "controlBridgeStatusDecodedDhwValve": obj.get("controlBridgeStatusDecodedDhwValve"),
            "controlBridgeStatusDecodedGasBoiler": obj.get("controlBridgeStatusDecodedGasBoiler"),
            "controlBridgeStatusDecodedElectricHeater": obj.get("controlBridgeStatusDecodedElectricHeater"),
            "controlBridgeStatusDecodedWaterPump2": obj.get("controlBridgeStatusDecodedWaterPump2"),
            "inputStatus": obj.get("inputStatus"),
            "currentControlMethod": obj.get("currentControlMethod"),
            "signalStrength": obj.get("signalStrength"),
            "t1": obj.get("t1"),
            "t2": obj.get("t2"),
            "tSpareNtc": obj.get("tSpareNtc"),
            "tBoard": obj.get("tBoard"),
            "tAirIn": obj.get("tAirIn"),
            "tAirOut": obj.get("tAirOut"),
            "tWaterIn": obj.get("tWaterIn"),
            "tWaterOut": obj.get("tWaterOut"),
            "tWaterHouseIn": obj.get("tWaterHouseIn"),
            "rpm": obj.get("rpm"),
            "rpmLimiter": obj.get("rpmLimiter"),
            "rpmLimiterType": obj.get("rpmLimiterType"),
            "pCompressorIn": obj.get("pCompressorIn"),
            "pCompressorOut": obj.get("pCompressorOut"),
            "pCompressorInTarget": obj.get("pCompressorInTarget"),
            "tInverter": obj.get("tInverter"),
            "tCompressorIn": obj.get("tCompressorIn"),
            "tCompressorOut": obj.get("tCompressorOut"),
            "tCompressorInTransient": obj.get("tCompressorInTransient"),
            "tCompressorOutTransient": obj.get("tCompressorOutTransient"),
            "deltaTCompressorInSuperheat": obj.get("deltaTCompressorInSuperheat"),
            "compressorPowerLowAccuracy": obj.get("compressorPowerLowAccuracy"),
            "fan": obj.get("fan"),
            "fanPower": obj.get("fanPower"),
            "valve": obj.get("valve"),
            "exvFlowStepGain": obj.get("exvFlowStepGain"),
            "cmMassFlow": obj.get("cmMassFlow"),
            "cmMassPowerIn": obj.get("cmMassPowerIn"),
            "cmMassPowerOut": obj.get("cmMassPowerOut"),
            "pRequested": obj.get("pRequested"),
            "powerErrorIntegral": obj.get("powerErrorIntegral"),
            "onOffThermostatState": obj.get("onOffThermostatState"),
            "thermostatStatus": obj.get("thermostatStatus"),
            "tRoom": obj.get("tRoom"),
            "tRoomTarget": obj.get("tRoomTarget"),
            "tThermostatSetpoint": obj.get("tThermostatSetpoint"),
            "otBoilerStatus": obj.get("otBoilerStatus"),
            "otBoilerFeedTemperature": obj.get("otBoilerFeedTemperature"),
            "otBoilerReturnTemperature": obj.get("otBoilerReturnTemperature"),
            "interval": obj.get("interval")
        })
        return _obj


