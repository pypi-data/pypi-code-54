# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse

from .. import models


class RunOperations(object):
    """RunOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer

        self.config = config

    def get_child(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, run_id, filter=None, continuation_token=None, orderby=None, sortorder=None, top=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param run_id:
        :type run_id: str
        :param filter:
        :type filter: str
        :param continuation_token:
        :type continuation_token: str
        :param orderby:
        :type orderby: list[str]
        :param sortorder: Possible values include: 'Asc', 'Desc'
        :type sortorder: str
        :param top:
        :type top: int
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PaginatedRunDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.PaginatedRunDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_child.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if filter is not None:
            query_parameters['$filter'] = self._serialize.query("filter", filter, 'str')
        if continuation_token is not None:
            query_parameters['$continuationToken'] = self._serialize.query("continuation_token", continuation_token, 'str')
        if orderby is not None:
            query_parameters['$orderby'] = self._serialize.query("orderby", orderby, '[str]', div=',')
        if sortorder is not None:
            query_parameters['$sortorder'] = self._serialize.query("sortorder", sortorder, 'str')
        if top is not None:
            query_parameters['$top'] = self._serialize.query("top", top, 'int')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('PaginatedRunDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_child.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runs/{runId}/children'}

    def get_token(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, run_id, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param run_id:
        :type run_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: TokenResult or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.TokenResult or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_token.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('TokenResult', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_token.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runs/{runId}/token'}

    def get_details(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, run_id, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param run_id:
        :type run_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: RunDetailsDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.RunDetailsDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_details.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('RunDetailsDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_details.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runs/{runId}/details'}

    def get(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, run_id, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param run_id:
        :type run_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: RunDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.RunDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('RunDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runs/{runId}'}

    def patch(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, run_id, create_run_dto=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param run_id:
        :type run_id: str
        :param create_run_dto:
        :type create_run_dto: ~_restclient.models.CreateRunDto
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: RunDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.RunDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.patch.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if create_run_dto is not None:
            body_content = self._serialize.body(create_run_dto, 'CreateRunDto')
        else:
            body_content = None

        # Construct and send request
        request = self._client.patch(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('RunDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    patch.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runs/{runId}'}

    def batch_add_or_modify(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, request_dto, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param request_dto:
        :type request_dto: ~_restclient.models.BatchAddOrModifyRunRequestDto
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: BatchAddOrModifyRunResultDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.BatchAddOrModifyRunResultDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.batch_add_or_modify.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(request_dto, 'BatchAddOrModifyRunRequestDto')

        # Construct and send request
        request = self._client.patch(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('BatchAddOrModifyRunResultDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    batch_add_or_modify.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/batch/runs'}

    def get_by_query(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, query_params=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param query_params:
        :type query_params: ~_restclient.models.QueryParamsDto
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PaginatedRunDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.PaginatedRunDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_by_query.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if query_params is not None:
            body_content = self._serialize.body(query_params, 'QueryParamsDto')
        else:
            body_content = None

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('PaginatedRunDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_by_query.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runs:query'}

    def list_by_compute(
            self, subscription_id, resource_group_name, workspace_name, compute_name, filter=None, continuation_token=None, top=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param compute_name: Name of the Azure Machine Learning compute.
        :type compute_name: str
        :param filter:
        :type filter: str
        :param continuation_token:
        :type continuation_token: str
        :param top:
        :type top: int
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PaginatedRunDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.PaginatedRunDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.list_by_compute.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'computeName': self._serialize.url("compute_name", compute_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if filter is not None:
            query_parameters['$filter'] = self._serialize.query("filter", filter, 'str')
        if continuation_token is not None:
            query_parameters['$continuationToken'] = self._serialize.query("continuation_token", continuation_token, 'str')
        if top is not None:
            query_parameters['$top'] = self._serialize.query("top", top, 'int')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('PaginatedRunDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    list_by_compute.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/computes/{computeName}/runs'}

    def get_counts(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, filter=None, continuation_token=None, orderby=None, sortorder=None, top=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param filter:
        :type filter: str
        :param continuation_token:
        :type continuation_token: str
        :param orderby:
        :type orderby: list[str]
        :param sortorder: Possible values include: 'Asc', 'Desc'
        :type sortorder: str
        :param top:
        :type top: int
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: RunCountsDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.RunCountsDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_counts.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if filter is not None:
            query_parameters['$filter'] = self._serialize.query("filter", filter, 'str')
        if continuation_token is not None:
            query_parameters['$continuationToken'] = self._serialize.query("continuation_token", continuation_token, 'str')
        if orderby is not None:
            query_parameters['$orderby'] = self._serialize.query("orderby", orderby, '[str]', div=',')
        if sortorder is not None:
            query_parameters['$sortorder'] = self._serialize.query("sortorder", sortorder, 'str')
        if top is not None:
            query_parameters['$top'] = self._serialize.query("top", top, 'int')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('RunCountsDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_counts.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runcounts'}

    def delete_tags(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, run_id, tags, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param run_id:
        :type run_id: str
        :param tags:
        :type tags: list[str]
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: RunDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.RunDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.delete_tags.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(tags, '[str]')

        # Construct and send request
        request = self._client.delete(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('RunDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    delete_tags.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runs/{runId}/tags'}
