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

from msrest.serialization import Model


class AssetDto(Model):
    """AssetDto.

    :param asset_id:
    :type asset_id: str
    :param name:
    :type name: str
    :param current_version:
    :type current_version: ~_restclient.models.AssetVersionDto
    """

    _attribute_map = {
        'asset_id': {'key': 'assetId', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'current_version': {'key': 'currentVersion', 'type': 'AssetVersionDto'},
    }

    def __init__(self, asset_id=None, name=None, current_version=None):
        super(AssetDto, self).__init__()
        self.asset_id = asset_id
        self.name = name
        self.current_version = current_version
