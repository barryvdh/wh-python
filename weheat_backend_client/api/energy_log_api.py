# coding: utf-8

"""
    Weheat Backend

    This is the backend for the Weheat project

    The version of the OpenAPI document: v1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import io
import warnings

from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Dict, List, Optional, Tuple, Union, Any

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from pydantic import Field
from typing_extensions import Annotated
from datetime import datetime

from pydantic import StrictStr

from typing import List, Optional

from weheat_backend_client.models.energy_view_dto import EnergyViewDto

from weheat_backend_client.api_client import ApiClient
from weheat_backend_client.api_response import ApiResponse
from weheat_backend_client.rest import RESTResponseType


class EnergyLogApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def api_v1_energy_logs_heat_pump_id_get(
        self,
        heat_pump_id: Annotated[StrictStr, Field(description="The id of the heat pump")],
        start_time: Annotated[Optional[datetime], Field(description="Start time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)")] = None,
        end_time: Annotated[Optional[datetime], Field(description="End time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)")] = None,
        interval: Annotated[Optional[StrictStr], Field(description="Interval granularity of the log data, allowed intervals: \"Hour\", \"Day\", \"Week\", \"Month\", \"Year\"")] = None,
        x_version: Annotated[Optional[StrictStr], Field(description="Optional version parameter for frontend applications to check if an update / refresh is needed")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> List[EnergyViewDto]:
        """Gets the energy logs of the heat pump in a from start time to end time for a given interval  Correct Intervals include: Hour, Day, Week, Month, Year


        :param heat_pump_id: The id of the heat pump (required)
        :type heat_pump_id: str
        :param start_time: Start time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)
        :type start_time: datetime
        :param end_time: End time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)
        :type end_time: datetime
        :param interval: Interval granularity of the log data, allowed intervals: \"Hour\", \"Day\", \"Week\", \"Month\", \"Year\"
        :type interval: str
        :param x_version: Optional version parameter for frontend applications to check if an update / refresh is needed
        :type x_version: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._api_v1_energy_logs_heat_pump_id_get_serialize(
            heat_pump_id=heat_pump_id,
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            x_version=x_version,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '403': "str",
            '505': None,
            '200': "List[EnergyViewDto]",
            '400': None,
            '500': None,
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def api_v1_energy_logs_heat_pump_id_get_with_http_info(
        self,
        heat_pump_id: Annotated[StrictStr, Field(description="The id of the heat pump")],
        start_time: Annotated[Optional[datetime], Field(description="Start time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)")] = None,
        end_time: Annotated[Optional[datetime], Field(description="End time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)")] = None,
        interval: Annotated[Optional[StrictStr], Field(description="Interval granularity of the log data, allowed intervals: \"Hour\", \"Day\", \"Week\", \"Month\", \"Year\"")] = None,
        x_version: Annotated[Optional[StrictStr], Field(description="Optional version parameter for frontend applications to check if an update / refresh is needed")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[List[EnergyViewDto]]:
        """Gets the energy logs of the heat pump in a from start time to end time for a given interval  Correct Intervals include: Hour, Day, Week, Month, Year


        :param heat_pump_id: The id of the heat pump (required)
        :type heat_pump_id: str
        :param start_time: Start time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)
        :type start_time: datetime
        :param end_time: End time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)
        :type end_time: datetime
        :param interval: Interval granularity of the log data, allowed intervals: \"Hour\", \"Day\", \"Week\", \"Month\", \"Year\"
        :type interval: str
        :param x_version: Optional version parameter for frontend applications to check if an update / refresh is needed
        :type x_version: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._api_v1_energy_logs_heat_pump_id_get_serialize(
            heat_pump_id=heat_pump_id,
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            x_version=x_version,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '403': "str",
            '505': None,
            '200': "List[EnergyViewDto]",
            '400': None,
            '500': None,
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def api_v1_energy_logs_heat_pump_id_get_without_preload_content(
        self,
        heat_pump_id: Annotated[StrictStr, Field(description="The id of the heat pump")],
        start_time: Annotated[Optional[datetime], Field(description="Start time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)")] = None,
        end_time: Annotated[Optional[datetime], Field(description="End time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)")] = None,
        interval: Annotated[Optional[StrictStr], Field(description="Interval granularity of the log data, allowed intervals: \"Hour\", \"Day\", \"Week\", \"Month\", \"Year\"")] = None,
        x_version: Annotated[Optional[StrictStr], Field(description="Optional version parameter for frontend applications to check if an update / refresh is needed")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Gets the energy logs of the heat pump in a from start time to end time for a given interval  Correct Intervals include: Hour, Day, Week, Month, Year


        :param heat_pump_id: The id of the heat pump (required)
        :type heat_pump_id: str
        :param start_time: Start time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)
        :type start_time: datetime
        :param end_time: End time of the interval as a DateTime object in UTC (format: yyyy-MM-dd HH:mm:ss)
        :type end_time: datetime
        :param interval: Interval granularity of the log data, allowed intervals: \"Hour\", \"Day\", \"Week\", \"Month\", \"Year\"
        :type interval: str
        :param x_version: Optional version parameter for frontend applications to check if an update / refresh is needed
        :type x_version: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._api_v1_energy_logs_heat_pump_id_get_serialize(
            heat_pump_id=heat_pump_id,
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            x_version=x_version,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '403': "str",
            '505': None,
            '200': "List[EnergyViewDto]",
            '400': None,
            '500': None,
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _api_v1_energy_logs_heat_pump_id_get_serialize(
        self,
        heat_pump_id,
        start_time,
        end_time,
        interval,
        x_version,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> Tuple:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, str] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if heat_pump_id is not None:
            _path_params['heatPumpId'] = heat_pump_id
        # process the query parameters
        if start_time is not None:
            if isinstance(start_time, datetime):
                _query_params.append(
                    (
                        'startTime',
                        start_time.strftime(
                            self.api_client.configuration.datetime_format
                        )
                    )
                )
            else:
                _query_params.append(('startTime', start_time))
            
        if end_time is not None:
            if isinstance(end_time, datetime):
                _query_params.append(
                    (
                        'endTime',
                        end_time.strftime(
                            self.api_client.configuration.datetime_format
                        )
                    )
                )
            else:
                _query_params.append(('endTime', end_time))
            
        if interval is not None:
            
            _query_params.append(('interval', interval))
            
        # process the header parameters
        if x_version is not None:
            _header_params['x-version'] = x_version
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            [
                'text/plain', 
                'application/json', 
                'text/json'
            ]
        )


        # authentication setting
        _auth_settings: List[str] = [
            'oauth2'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/api/v1/energy-logs/{heatPumpId}',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )


