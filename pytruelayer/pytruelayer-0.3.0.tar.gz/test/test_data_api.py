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

import truelayer
from truelayer.api.data_api import DataApi  # noqa: E501
from truelayer.rest import ApiException


class TestDataApi(unittest.TestCase):
    """DataApi unit test stubs"""

    def setUp(self):
        self.api = truelayer.api.data_api.DataApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_accounts_by_account_id_balance_get(self):
        """Test case for accounts_by_account_id_balance_get

        """
        pass

    def test_accounts_by_account_id_get(self):
        """Test case for accounts_by_account_id_get

        """
        pass

    def test_accounts_by_account_id_transactions_get(self):
        """Test case for accounts_by_account_id_transactions_get

        """
        pass

    def test_accounts_get(self):
        """Test case for accounts_get

        """
        pass

    def test_cards_by_account_id_balance_get(self):
        """Test case for cards_by_account_id_balance_get

        """
        pass

    def test_cards_by_account_id_get(self):
        """Test case for cards_by_account_id_get

        """
        pass

    def test_cards_by_account_id_transactions_get(self):
        """Test case for cards_by_account_id_transactions_get

        """
        pass

    def test_cards_get(self):
        """Test case for cards_get

        """
        pass

    def test_info_get(self):
        """Test case for info_get

        """
        pass

    def test_me_get(self):
        """Test case for me_get

        """
        pass

    def test_results_by_task_id_get(self):
        """Test case for results_by_task_id_get

        """
        pass


if __name__ == '__main__':
    unittest.main()
