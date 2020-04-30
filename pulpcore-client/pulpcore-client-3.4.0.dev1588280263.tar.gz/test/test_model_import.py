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
from pulpcore.client.pulpcore.models.model_import import ModelImport  # noqa: E501
from pulpcore.client.pulpcore.rest import ApiException

class TestModelImport(unittest.TestCase):
    """ModelImport unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ModelImport
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulpcore.models.model_import.ModelImport()  # noqa: E501
        if include_optional :
            return ModelImport(
                pulp_href = '0', 
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                task = '0', 
                params = pulpcore.client.pulpcore.models.params.Params()
            )
        else :
            return ModelImport(
                task = '0',
                params = pulpcore.client.pulpcore.models.params.Params(),
        )

    def testModelImport(self):
        """Test ModelImport"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
