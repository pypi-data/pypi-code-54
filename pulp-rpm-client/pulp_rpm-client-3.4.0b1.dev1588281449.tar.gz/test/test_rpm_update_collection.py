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

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.models.rpm_update_collection import RpmUpdateCollection  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException

class TestRpmUpdateCollection(unittest.TestCase):
    """RpmUpdateCollection unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RpmUpdateCollection
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_rpm.models.rpm_update_collection.RpmUpdateCollection()  # noqa: E501
        if include_optional :
            return RpmUpdateCollection(
                name = '0', 
                shortname = '0', 
                packages = [
                    {
                        'key' : '0'
                        }
                    ]
            )
        else :
            return RpmUpdateCollection(
                name = '0',
                shortname = '0',
        )

    def testRpmUpdateCollection(self):
        """Test RpmUpdateCollection"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
