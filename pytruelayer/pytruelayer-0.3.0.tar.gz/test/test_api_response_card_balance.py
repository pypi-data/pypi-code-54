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
from truelayer.models.api_response_card_balance import APIResponseCardBalance  # noqa: E501
from truelayer.rest import ApiException

class TestAPIResponseCardBalance(unittest.TestCase):
    """APIResponseCardBalance unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test APIResponseCardBalance
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = truelayer.models.api_response_card_balance.APIResponseCardBalance()  # noqa: E501
        if include_optional :
            return APIResponseCardBalance(
                results = [
                    truelayer.models.card_balance.CardBalance(
                        available = 1.337, 
                        credit_limit = 1.337, 
                        currency = '0', 
                        current = 1.337, 
                        last_statement_balance = 1.337, 
                        last_statement_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        payment_due = 1.337, 
                        payment_due_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        update_timestamp = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ], 
                results_uri = '0', 
                status = 'Queued', 
                task_id = '0'
            )
        else :
            return APIResponseCardBalance(
        )

    def testAPIResponseCardBalance(self):
        """Test APIResponseCardBalance"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
