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

import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.models.file_file_distribution import FileFileDistribution  # noqa: E501
from pulpcore.client.pulp_file.rest import ApiException

class TestFileFileDistribution(unittest.TestCase):
    """FileFileDistribution unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test FileFileDistribution
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_file.models.file_file_distribution.FileFileDistribution()  # noqa: E501
        if include_optional :
            return FileFileDistribution(
                pulp_href = '0', 
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                base_path = '0', 
                base_url = '0', 
                content_guard = '0', 
                name = '0', 
                publication = '0'
            )
        else :
            return FileFileDistribution(
                base_path = '0',
                name = '0',
        )

    def testFileFileDistribution(self):
        """Test FileFileDistribution"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
