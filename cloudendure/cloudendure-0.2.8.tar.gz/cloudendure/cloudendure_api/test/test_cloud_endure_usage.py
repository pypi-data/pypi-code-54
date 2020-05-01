# coding: utf-8

"""
    CloudEndure API documentation

    © 2017 CloudEndure All rights reserved  # General Request authentication in CloudEndure's API is done using session cookies. A session cookie is returned upon successful execution of the \"login\" method. This value must then be provided within the request headers of all subsequent API requests.  ## Errors Some errors are not specifically written in every method since they may always return. Those are: 1) 401 (Unauthorized) - for unauthenticated requests. 2) 405 (Method Not Allowed) - for using a method that is not supported (POST instead of GET). 3) 403 (Forbidden) - request is authenticated, but the user is not allowed to access. 4) 422 (Unprocessable Entity) - for invalid input.  ## Formats All strings with date-time format are according to RFC3339.  All strings with \"duration\" format are according to ISO8601. For example, a full day duration can be specified with \"PNNNND\".   # noqa: E501

    OpenAPI spec version: 5
    Contact: https://bit.ly/2T54hSc
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

from cloudendure import cloudendure_api
from cloudendure.cloudendure_api.rest import ApiException
from models.cloud_endure_usage import CloudEndureUsage  # noqa: E501


class TestCloudEndureUsage(unittest.TestCase):
    """CloudEndureUsage unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCloudEndureUsage(self):
        """Test CloudEndureUsage"""
        # FIXME: construct object with mandatory attributes with example values
        # model = cloudendure_api.models.cloud_endure_usage.CloudEndureUsage()  # noqa: E501
        pass


if __name__ == "__main__":
    unittest.main()
