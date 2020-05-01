import json
from urllib import request
import os
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Union
import pandas as pd


def url_to_dict(url: str) -> Dict[str, Any]:
    """Utility to retrieve json from a url and convert to dict."""
    resp = request.urlopen(url)
    data = resp.read().decode("utf-8")
    json_data = json.loads(data)
    return dict(json_data)


@dataclass
class FinancialModelingPrep:
    """A Python3 wrapper for the Financial Modeling Prep API."""

    api_version = "v3"
    api_url = "https://financialmodelingprep.com/api"
    base_url: str = os.path.join(api_url, api_version)

    def __post_init__(self, as_pandas: bool = True) -> None:
        """
        Initialize class variables.

        :param as_pandas: returns api calls as pandas df if true, else as
        dict.
        """
        self.as_pandas = as_pandas

    def profile(self, ticker: str) -> Dict[str, Any]:
        """Retrieve a company's profile."""
        url = os.path.join(self.base_url, "company", "profile", ticker)
        dict_repr = url_to_dict(url)
        if self.as_pandas:
            return pd.DataFrame(dict_repr)
        return dict_repr

    def quote(self, tickers: List[str]) -> List[Dict[str, Any]]:
        """Retreive quotes for any number of stock tickers."""
        url = os.path.join(self.base_url, "quote", *tickers)
        dict_repr = url_to_dict(url)
        if self.as_pandas:
            return pd.DataFrame(dict_repr)
        return dict_repr

    def financials(self, ticker: str,
                   type: str,
                   period="annual") -> Dict[str, Any]:
        """
        Retrieve a company's financial statements.

        :param type: the type of financial statement to retrieve
        :param period: quarter or annual
        """
        types = ["income-statement", "balance-sheet-statement",
                 "cash-flow-statement"]
        type_map = {t.split("-")[0]: t for t in types}
        if type in type_map.keys():
            query = ticker + "?period=" + period
            url = os.path.join(self.base_url, "financials", type_map.get(type),
                               query)
            dict_repr = url_to_dict(url)
            if self.as_pandas:
                return pd.DataFrame(dict_repr["financials"])
            return dict_repr
        else:
            raise ValueError(f"Type '{type}' is invalid.  Use one of:\
                             {type_map.keys}")

    def price_history(self, ticker: str) -> Union[Dict[str, Any],
                                                  pd.DataFrame]:
        """Retrieve daily price data."""
        url = os.path.join(self.base_url, "historical-price-full", ticker)
        dict_repr = url_to_dict(url)
        if self.as_pandas:
            return pd.DataFrame(dict_repr)
        return dict_repr
