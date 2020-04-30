# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.models.upload_chunk import UploadChunk  # noqa: E501
from pulpcore.client.pulpcore.rest import ApiException

class TestUploadChunk(unittest.TestCase):
    """UploadChunk unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test UploadChunk
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulpcore.models.upload_chunk.UploadChunk()  # noqa: E501
        if include_optional :
            return UploadChunk(
                file = '0', 
                sha256 = '0', 
                offset = 56, 
                size = 56
            )
        else :
            return UploadChunk(
        )

    def testUploadChunk(self):
        """Test UploadChunk"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
