# coding: utf-8

"""
    Onshape REST API

    The Onshape REST API consumed by all clients.  # noqa: E501

    The version of the OpenAPI document: 1.113
    Contact: api-support@onshape.zendesk.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401
import sys  # noqa: F401

# python 2 and python 3 compatibility library
import six

from onshape_client.oas.api_client import ApiClient
from onshape_client.oas.exceptions import ApiTypeError, ApiValueError
from onshape_client.oas.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    int,
    none_type,
    str,
    validate_and_convert_types,
)


class OpenAPIApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __get_open_api(self, **kwargs):
            """OpenAPI spec documentation for the Onshape REST API.  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True
            >>> thread = api.get_open_api(async_req=True)
            >>> result = thread.get()


            Keyword Args:
                excluded_tags (str): If an operation contains an excluded tag, it is not returned from this endpoint.. [optional]
                included_tags (str): Return only operations with tags included in includedTags.. [optional]
                include_deprecated (bool): Include deprecated endpoints.. [optional]
                documentation_status ([str]): Only return endpoints that have the specified document status. Default is to return all the endpoints the user should have access to.. [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int): specifies the index of the server
                    that we want to use.
                    Default is 0.
                async_req (bool): execute request asynchronously

            Returns:
                None
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs["async_req"] = kwargs.get("async_req", False)
            kwargs["_return_http_data_only"] = kwargs.get(
                "_return_http_data_only", True
            )
            kwargs["_preload_content"] = kwargs.get("_preload_content", True)
            kwargs["_request_timeout"] = kwargs.get("_request_timeout", None)
            kwargs["_check_input_type"] = kwargs.get("_check_input_type", True)
            kwargs["_check_return_type"] = kwargs.get("_check_return_type", True)
            kwargs["_host_index"] = kwargs.get("_host_index", 0)
            return self.call_with_http_info(**kwargs)

        self.get_open_api = Endpoint(
            settings={
                "response_type": None,
                "auth": [],
                "endpoint_path": "/api/openapi",
                "operation_id": "get_open_api",
                "http_method": "GET",
                "servers": [],
            },
            params_map={
                "all": [
                    "excluded_tags",
                    "included_tags",
                    "include_deprecated",
                    "documentation_status",
                ],
                "required": [],
                "nullable": [],
                "enum": ["documentation_status",],
                "validation": [],
            },
            root_map={
                "validations": {},
                "allowed_values": {
                    ("documentation_status",): {
                        "DEVELOPMENT": "DEVELOPMENT",
                        "PRODUCTION": "PRODUCTION",
                        "STAGING": "STAGING",
                        "EVP": "EVP",
                        "UNSET": "UNSET",
                        "INTERNAL": "INTERNAL",
                    },
                },
                "openapi_types": {
                    "excluded_tags": (str,),
                    "included_tags": (str,),
                    "include_deprecated": (bool,),
                    "documentation_status": ([str],),
                },
                "attribute_map": {
                    "excluded_tags": "excludedTags",
                    "included_tags": "includedTags",
                    "include_deprecated": "includeDeprecated",
                    "documentation_status": "documentationStatus",
                },
                "location_map": {
                    "excluded_tags": "query",
                    "included_tags": "query",
                    "include_deprecated": "query",
                    "documentation_status": "query",
                },
                "collection_format_map": {"documentation_status": "multi",},
            },
            headers_map={"accept": [], "content_type": [],},
            api_client=api_client,
            callable=__get_open_api,
        )


class Endpoint(object):
    def __init__(
        self,
        settings=None,
        params_map=None,
        root_map=None,
        headers_map=None,
        api_client=None,
        callable=None,
    ):
        """Creates an endpoint

        Args:
            settings (dict): see below key value pairs
                'response_type' (tuple/None): response type
                'auth' (list): a list of auth type keys
                'endpoint_path' (str): the endpoint path
                'operation_id' (str): endpoint string identifier
                'http_method' (str): POST/PUT/PATCH/GET etc
                'servers' (list): list of str servers that this endpoint is at
            params_map (dict): see below key value pairs
                'all' (list): list of str endpoint parameter names
                'required' (list): list of required parameter names
                'nullable' (list): list of nullable parameter names
                'enum' (list): list of parameters with enum values
                'validation' (list): list of parameters with validations
            root_map
                'validations' (dict): the dict mapping endpoint parameter tuple
                    paths to their validation dictionaries
                'allowed_values' (dict): the dict mapping endpoint parameter
                    tuple paths to their allowed_values (enum) dictionaries
                'openapi_types' (dict): param_name to openapi type
                'attribute_map' (dict): param_name to camelCase name
                'location_map' (dict): param_name to  'body', 'file', 'form',
                    'header', 'path', 'query'
                collection_format_map (dict): param_name to `csv` etc.
            headers_map (dict): see below key value pairs
                'accept' (list): list of Accept header strings
                'content_type' (list): list of Content-Type header strings
            api_client (ApiClient) api client instance
            callable (function): the function which is invoked when the
                Endpoint is called
        """
        self.settings = settings
        self.params_map = params_map
        self.params_map["all"].extend(
            [
                "async_req",
                "_host_index",
                "_preload_content",
                "_request_timeout",
                "_return_http_data_only",
                "_check_input_type",
                "_check_return_type",
            ]
        )
        self.params_map["nullable"].extend(["_request_timeout"])
        self.validations = root_map["validations"]
        self.allowed_values = root_map["allowed_values"]
        self.openapi_types = root_map["openapi_types"]
        extra_types = {
            "async_req": (bool,),
            "_host_index": (int,),
            "_preload_content": (bool,),
            "_request_timeout": (none_type, int, (int,), [int]),
            "_return_http_data_only": (bool,),
            "_check_input_type": (bool,),
            "_check_return_type": (bool,),
        }
        self.openapi_types.update(extra_types)
        self.attribute_map = root_map["attribute_map"]
        self.location_map = root_map["location_map"]
        self.collection_format_map = root_map["collection_format_map"]
        self.headers_map = headers_map
        self.api_client = api_client
        self.callable = callable

    def __validate_inputs(self, kwargs):
        for param in self.params_map["enum"]:
            if param in kwargs:
                check_allowed_values(self.allowed_values, (param,), kwargs[param])

        for param in self.params_map["validation"]:
            if param in kwargs:
                check_validations(self.validations, (param,), kwargs[param])

        if kwargs["_check_input_type"] is False:
            return

        for key, value in six.iteritems(kwargs):
            fixed_val = validate_and_convert_types(
                value,
                self.openapi_types[key],
                [key],
                False,
                kwargs["_check_input_type"],
                configuration=self.api_client.configuration,
            )
            kwargs[key] = fixed_val

    def __gather_params(self, kwargs):
        params = {
            "body": None,
            "collection_format": {},
            "file": {},
            "form": [],
            "header": {},
            "path": {},
            "query": [],
        }

        for param_name, param_value in six.iteritems(kwargs):
            param_location = self.location_map.get(param_name)
            if param_location is None:
                continue
            if param_location:
                if param_location == "body":
                    params["body"] = param_value
                    continue
                base_name = self.attribute_map[param_name]
                if param_location == "form" and self.openapi_types[param_name] == (
                    file_type,
                ):
                    params["file"][param_name] = [param_value]
                elif param_location == "form" and self.openapi_types[param_name] == (
                    [file_type],
                ):
                    # param_value is already a list
                    params["file"][param_name] = param_value
                elif param_location in {"form", "query"}:
                    param_value_full = (base_name, param_value)
                    params[param_location].append(param_value_full)
                if param_location not in {"form", "query"}:
                    params[param_location][base_name] = param_value
                collection_format = self.collection_format_map.get(param_name)
                if collection_format:
                    params["collection_format"][base_name] = collection_format

        return params

    def __call__(self, *args, **kwargs):
        """ This method is invoked when endpoints are called
        Example:
        pet_api = PetApi()
        pet_api.add_pet  # this is an instance of the class Endpoint
        pet_api.add_pet()  # this invokes pet_api.add_pet.__call__()
        which then invokes the callable functions stored in that endpoint at
        pet_api.add_pet.callable or self.callable in this class
        """
        return self.callable(self, *args, **kwargs)

    def call_with_http_info(self, **kwargs):

        try:
            _host = self.settings["servers"][kwargs["_host_index"]]
        except IndexError:
            if self.settings["servers"]:
                raise ApiValueError(
                    "Invalid host index. Must be 0 <= index < %s"
                    % len(self.settings["servers"])
                )
            _host = None

        for key, value in six.iteritems(kwargs):
            if key not in self.params_map["all"]:
                raise ApiTypeError(
                    "Got an unexpected parameter '%s'"
                    " to method `%s`" % (key, self.settings["operation_id"])
                )
            # only throw this nullable ApiValueError if _check_input_type
            # is False, if _check_input_type==True we catch this case
            # in self.__validate_inputs
            if (
                key not in self.params_map["nullable"]
                and value is None
                and kwargs["_check_input_type"] is False
            ):
                raise ApiValueError(
                    "Value may not be None for non-nullable parameter `%s`"
                    " when calling `%s`" % (key, self.settings["operation_id"])
                )

        for key in self.params_map["required"]:
            if key not in kwargs.keys():
                raise ApiValueError(
                    "Missing the required parameter `%s` when calling "
                    "`%s`" % (key, self.settings["operation_id"])
                )

        self.__validate_inputs(kwargs)

        params = self.__gather_params(kwargs)

        accept_headers_list = self.headers_map["accept"]
        if accept_headers_list:
            params["header"]["Accept"] = self.api_client.select_header_accept(
                accept_headers_list
            )

        content_type_headers_list = self.headers_map["content_type"]
        if content_type_headers_list:
            header_list = self.api_client.select_header_content_type(
                content_type_headers_list
            )
            params["header"]["Content-Type"] = header_list

        return self.api_client.call_api(
            self.settings["endpoint_path"],
            self.settings["http_method"],
            params["path"],
            params["query"],
            params["header"],
            body=params["body"],
            post_params=params["form"],
            files=params["file"],
            response_type=self.settings["response_type"],
            auth_settings=self.settings["auth"],
            async_req=kwargs["async_req"],
            _check_type=kwargs["_check_return_type"],
            _return_http_data_only=kwargs["_return_http_data_only"],
            _preload_content=kwargs["_preload_content"],
            _request_timeout=kwargs["_request_timeout"],
            _host=_host,
            collection_formats=params["collection_format"],
        )
