# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.45.02
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class JobsApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def create_screenshot_job(self, **kwargs):
        """
        Create a job to capture a worksheet screenshot at a regular interval
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_screenshot_job(body=body_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param ScreenshotJobInputV1 body: Data to create the job (required)
        :return: JobOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.create_screenshot_job_with_http_info(**kwargs)
        else:
            (data) = self.create_screenshot_job_with_http_info(**kwargs)
            return data

    def create_screenshot_job_with_http_info(self, **kwargs):
        """
        Create a job to capture a worksheet screenshot at a regular interval
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_screenshot_job_with_http_info(body=body_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param ScreenshotJobInputV1 body: Data to create the job (required)
        :return: JobOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_screenshot_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_screenshot_job`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/vnd.seeq.v1+json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/vnd.seeq.v1+json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api('/jobs/screenshot', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='JobOutputV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def delete_job(self, **kwargs):
        """
        Delete a scheduled job and cancel any currently running instance
        Only administrators are permitted to perform this action
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_job(group=group_value, id=id_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str group: Group to which the job belongs (required)
        :param str id: ID of the job to delete (required)
        :return: StatusMessageBase
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.delete_job_with_http_info(**kwargs)
        else:
            (data) = self.delete_job_with_http_info(**kwargs)
            return data

    def delete_job_with_http_info(self, **kwargs):
        """
        Delete a scheduled job and cancel any currently running instance
        Only administrators are permitted to perform this action
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_job_with_http_info(group=group_value, id=id_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str group: Group to which the job belongs (required)
        :param str id: ID of the job to delete (required)
        :return: StatusMessageBase
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['group', 'id']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'group' is set
        if ('group' not in params) or (params['group'] is None):
            raise ValueError("Missing the required parameter `group` when calling `delete_job`")
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_job`")


        collection_formats = {}

        path_params = {}
        if 'group' in params:
            path_params['group'] = params['group']
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/vnd.seeq.v1+json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/vnd.seeq.v1+json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api('/jobs/{group}/{id}', 'DELETE',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='StatusMessageBase',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_jobs(self, **kwargs):
        """
        List of scheduled jobs
        Pagination is enabled for this query. Only administrators are permitted to perform this action
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_jobs(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int offset: The pagination offset, the index of the first job that will be returned in this page of results
        :param int limit: The pagination limit, the total number of jobs that will be returned in this page of results
        :return: GetJobsOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_jobs_with_http_info(**kwargs)
        else:
            (data) = self.get_jobs_with_http_info(**kwargs)
            return data

    def get_jobs_with_http_info(self, **kwargs):
        """
        List of scheduled jobs
        Pagination is enabled for this query. Only administrators are permitted to perform this action
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_jobs_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int offset: The pagination offset, the index of the first job that will be returned in this page of results
        :param int limit: The pagination limit, the total number of jobs that will be returned in this page of results
        :return: GetJobsOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['offset', 'limit']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_jobs" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'limit' in params:
            query_params.append(('limit', params['limit']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/vnd.seeq.v1+json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/vnd.seeq.v1+json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api('/jobs', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='GetJobsOutputV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_screenshot(self, **kwargs):
        """
        A simplified endpoint for fetching a screenshot of a worksheet at a regular interval.
        Does not rely on websockets, but instead expects the consumer to poll this endpoint for the latest image. Returns the binary content of the image directly along with appropriate image headers. Also includes an Expires header that indicates the time the next request should be made. If a period is not supplied, then the image is saved on the server, a URL to the image is returned, and the Expires header is not included
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_screenshot(worksheet_id=worksheet_id_value, width=width_value, height=height_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str document_id: The ID of the Topic Document that is requesting this screenshot
        :param str worksheet_id: The worksheet id to capture (required)
        :param str workstep_id: The workstep id to capture. If not provided the latest for the worksheet will be used
        :param str range_formula: A Seeq formula that is used to determine the date range used for the screenshot. It must produce a capsule and will be passed $now, set to the current time, as an argument. Example: capsule($now - 24h, $now) or capsule(\"2018-05-25T23:40:33.139Z\", \"2018-05-26T23:40:33.139Z\"). If not supplied, then the display range of the source worksheet will be used.
        :param str period: The duration between each screenshot. Example: 5min. If not supplied then the screenshot job will be executed once and the screenshot field of the response will contain the URL of the screenshot instead of Base64-encoded image bytes.
        :param int width: The width of the screenshot (required)
        :param int height: The height of the screenshot (required)
        :param str timezone: The timezone to use for the screenshot. If not provided the timezone of the server will be used
        :param str content_selector: A CSS selector that can be used to capture only a certain page element
        :return: ScreenshotOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_screenshot_with_http_info(**kwargs)
        else:
            (data) = self.get_screenshot_with_http_info(**kwargs)
            return data

    def get_screenshot_with_http_info(self, **kwargs):
        """
        A simplified endpoint for fetching a screenshot of a worksheet at a regular interval.
        Does not rely on websockets, but instead expects the consumer to poll this endpoint for the latest image. Returns the binary content of the image directly along with appropriate image headers. Also includes an Expires header that indicates the time the next request should be made. If a period is not supplied, then the image is saved on the server, a URL to the image is returned, and the Expires header is not included
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_screenshot_with_http_info(worksheet_id=worksheet_id_value, width=width_value, height=height_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str document_id: The ID of the Topic Document that is requesting this screenshot
        :param str worksheet_id: The worksheet id to capture (required)
        :param str workstep_id: The workstep id to capture. If not provided the latest for the worksheet will be used
        :param str range_formula: A Seeq formula that is used to determine the date range used for the screenshot. It must produce a capsule and will be passed $now, set to the current time, as an argument. Example: capsule($now - 24h, $now) or capsule(\"2018-05-25T23:40:33.139Z\", \"2018-05-26T23:40:33.139Z\"). If not supplied, then the display range of the source worksheet will be used.
        :param str period: The duration between each screenshot. Example: 5min. If not supplied then the screenshot job will be executed once and the screenshot field of the response will contain the URL of the screenshot instead of Base64-encoded image bytes.
        :param int width: The width of the screenshot (required)
        :param int height: The height of the screenshot (required)
        :param str timezone: The timezone to use for the screenshot. If not provided the timezone of the server will be used
        :param str content_selector: A CSS selector that can be used to capture only a certain page element
        :return: ScreenshotOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['document_id', 'worksheet_id', 'workstep_id', 'range_formula', 'period', 'width', 'height', 'timezone', 'content_selector']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_screenshot" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'worksheet_id' is set
        if ('worksheet_id' not in params) or (params['worksheet_id'] is None):
            raise ValueError("Missing the required parameter `worksheet_id` when calling `get_screenshot`")
        # verify the required parameter 'width' is set
        if ('width' not in params) or (params['width'] is None):
            raise ValueError("Missing the required parameter `width` when calling `get_screenshot`")
        # verify the required parameter 'height' is set
        if ('height' not in params) or (params['height'] is None):
            raise ValueError("Missing the required parameter `height` when calling `get_screenshot`")


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'document_id' in params:
            query_params.append(('documentId', params['document_id']))
        if 'worksheet_id' in params:
            query_params.append(('worksheetId', params['worksheet_id']))
        if 'workstep_id' in params:
            query_params.append(('workstepId', params['workstep_id']))
        if 'range_formula' in params:
            query_params.append(('rangeFormula', params['range_formula']))
        if 'period' in params:
            query_params.append(('period', params['period']))
        if 'width' in params:
            query_params.append(('width', params['width']))
        if 'height' in params:
            query_params.append(('height', params['height']))
        if 'timezone' in params:
            query_params.append(('timezone', params['timezone']))
        if 'content_selector' in params:
            query_params.append(('contentSelector', params['content_selector']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/vnd.seeq.v1+json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/vnd.seeq.v1+json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api('/jobs/screenshot', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='ScreenshotOutputV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
