# coding: utf-8

"""
    TrueLayer Resource API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1.0
    Contact: rienafairefr@gmail.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import truelayer
from truelayer.models.cached_api_response_object import CachedAPIResponseObject  # noqa: E501
from truelayer.rest import ApiException

class TestCachedAPIResponseObject(unittest.TestCase):
    """CachedAPIResponseObject unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CachedAPIResponseObject
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = truelayer.models.cached_api_response_object.CachedAPIResponseObject()  # noqa: E501
        if include_optional :
            return CachedAPIResponseObject(
                error = '0', 
                error_description = '0', 
                error_details = {
                    'key' : '0'
                    }, 
                results = [
                    {
                        'key' : '0'
                        }
                    ], 
                results_uri = '0', 
                status = 'Queued', 
                task_id = '0'
            )
        else :
            return CachedAPIResponseObject(
        )

    def testCachedAPIResponseObject(self):
        """Test CachedAPIResponseObject"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
