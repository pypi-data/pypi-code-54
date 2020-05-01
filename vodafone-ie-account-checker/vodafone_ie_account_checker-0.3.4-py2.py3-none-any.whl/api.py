"""Main module."""

import logging
import requests

from lxml import html
from collections import namedtuple
from datetime import datetime

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

XP_USAGE_SINCE = '//*[@id="main"]/div/section/' \
                 'div[2]/section[1]/div/h2/text()'
XP_USAGE_TOTAL = '//*[@id="main"]/div/section/' \
                 'div[2]/section[1]/div/div/div/strong/text()'
XP_ACCOUNT_BALANCE = '//*[@id="main"]/div/section/' \
                     'div[1]/section[1]/div/span/text()'
XP_BUNDLE_NAME = '//*[@id="main"]/div/section/' \
                 'div[2]/section[2]/div/div[1]/div[1]/ul[1]/li/text()'

DEFAULT_FAIR_USAGE_LIMIT_GB = 1000
DATA_KILOBYTES = "kB"
DATA_MEGABYTES = "MB"
DATA_GIGABYTES = "GB"
DATA_TERABYTES = "TB"


class Account:
    """
    Represents a VF Account.
    """

    def __init__(self, username, password, token1, token2,
                 fair_usage_limit=DEFAULT_FAIR_USAGE_LIMIT_GB):
        """
        Defines an vf account.

        :param username: VF Broadband username (email)
        :param password: VF Broadband password
        :param token1: Token 1
        :param token2: Token 2
        :param fair_usage_limit: If your fair usage is
        not 1000 GB, specify it here.
        """
        log.debug("Initialising new VF Account")

        if "@" not in username:
            log.warning("Vodafone Broadband username "
                        "should be an email address.")
        self.logged_in = False
        self.data = None

        self._session = requests.Session()
        self.username = username
        self.password = password

        self.verification_token1 = token1
        self.verification_token2 = token2
        self.fair_usage_limit = fair_usage_limit

    def get_account_overview_request(self):
        """ Do the account overview request and return account tuple """

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://broadband.vodafone.ie',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; '
                          'Intel Mac OS X 10_15_4) '
                          'AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml'
                      ',application/xml;q=0.9,image/webp,'
                      'image/apng,*/*;q=0.8,application/'
                      'signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://broadband.vodafone.ie'
                       '/myaccount/session/login?t=1',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        params = (
            ('t', '1'),
        )

        # log.debug(f"self.verification_token1 {self.verification_token1}")
        # log.debug(f"self.verification_token2 {self.verification_token2}")

        cookies = {
            '__RequestVerificationToken': self.verification_token1,
        }

        data = {
            '__RequestVerificationToken': self.verification_token2,
            'emailAddress': self.username,
            'password': self.password
        }
        response = self._session.post('https://broadband.'
                                      'vodafone.ie/myaccount/session/login',
                                      headers=headers,
                                      cookies=cookies,
                                      params=params,
                                      data=data
                                      )

        # usage since date
        # e.g. ['Since 15 Apr 2020']
        usage_since = self.get_xpath_value(response, XP_USAGE_SINCE)
        # data usage. e.g. ['397.35 GB']
        usage_value_raw = self.get_xpath_value(response, XP_USAGE_TOTAL)
        usage_value, usage_value_unit, usage_percent = \
            self.get_usage_values(usage_value_raw)

        # account due fee. e.g. €60
        account_balance = self.get_xpath_value(response, XP_ACCOUNT_BALANCE)
        # Bundles
        # Gigabit Broadband 300 (eir)
        bundle_name = self.get_xpath_value(response, XP_BUNDLE_NAME)

        if usage_value == "":
            log.warning("Unable to get usage data.")
            # log.warning(response.content)
            self.data = None
        else:
            AccountDetails = namedtuple("AccountDetails",
                                        ["usage_since",
                                         "usage_value",
                                         "usage_value_raw",
                                         "usage_value_unit",
                                         "usage_percent",
                                         "last_updated",
                                         "account_balance",
                                         "bundle_name"])
            account_details = AccountDetails(usage_since,
                                             usage_value,
                                             usage_value_raw,
                                             usage_value_unit,
                                             usage_percent,
                                             datetime.now(),
                                             account_balance,
                                             bundle_name)
            log.debug(account_details)
            self.logged_in = True
            self.data = account_details
            return account_details

        return None

    def get_xpath_value(self, response, path):
        """ Returns first result of xpath
        match, or blank string if not found. """
        tree = html.fromstring(response.content)
        try:
            result = tree.xpath(path)
            if len(result) == 0:
                log.warning(f"xpath not found: {path}")
                return ""
            return result[0]
        except ValueError:
            log.warning(f"xpath not found: {path}")

        return ""

    def is_logged_in(self):
        """Returns true if a successful login has happened"""
        return self.logged_in

    def get_usage_values(self, usage_value_raw):
        """ Get usage values. """
        try:
            usage_value = usage_value_raw.split(' ')[0]
            usage_value_unit = self.get_unit(usage_value_raw.split(' ')[1])
            usage_percent = int((float(usage_value) /
                                 self.fair_usage_limit) * 100)

            return usage_value, usage_value_unit, usage_percent
        except Exception:
            log.error("Unable to calculate usage.")

        return None, None, None

    def get_unit(self, unit_string):
        value = unit_string.upper()
        if value == "KB":
            return DATA_KILOBYTES
        if value == "MB":
            return DATA_MEGABYTES
        if value == "GB":
            return DATA_GIGABYTES
        if value == "TB":
            return DATA_TERABYTES
