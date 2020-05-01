import json
from urllib import request
import os
from dataclasses import dataclass
from typing import Dict, List, Union, Callable
import pandas as pd

# define types
Json = Union[List, Dict]
Df = pd.DataFrame


def extract_url(url: str) -> Json:
    """Utility to retrieve json from a url and convert to dict."""
    resp = request.urlopen(url)
    data = resp.read().decode("utf-8")
    json_data = json.loads(data)
    return json_data


@dataclass
class FmpWrapper:
    """A Python3 wrapper for the Financial Modeling Prep API."""

    api_version = "v3"
    api_url = "https://financialmodelingprep.com/api"
    base_url: str = os.path.join(api_url, api_version)
    as_pandas: bool = True

    def __route_return(self, data: Json,
                       f: Callable[[Json], Json] = lambda x: x
                       ) -> Union[Df, Json]:
        if self.as_pandas:
            new_data = f(data)
            return pd.DataFrame(new_data)
        return data

    def profile(self, ticker: str) -> Union[Df, Json]:
        """Retrieve a company's profile."""
        url = os.path.join(self.base_url, "company", "profile", ticker)
        raw_data = extract_url(url)
        return self.__route_return(raw_data)

    def quote(self, tickers: List[str]) -> Union[Df, Json]:
        """Retreive quotes for any number of stock tickers."""
        url = os.path.join(self.base_url, "quote", ",".join(tickers))
        raw_data = extract_url(url)
        return self.__route_return(raw_data)

    def financials(self, ticker: str,
                   type: str,
                   period: str = "annual") -> Union[Df, Json]:
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
            url = os.path.join(self.base_url, "financials",
                               type_map[type], query)
            raw_data = extract_url(url)
            def f(x: Json) -> Json: return x["financials"]
            return self.__route_return(raw_data, f)
        else:
            raise ValueError(f"Type '{type}' is invalid.  Use one of:\
                             {type_map.keys}")

    def price_history(self, ticker: str) -> Union[Df, Json]:
        """Retrieve daily price data."""
        url = os.path.join(self.base_url, "historical-price-full", ticker)
        raw_data = extract_url(url)
        def f(x: Json) -> Json: return x["historical"]
        return self.__route_return(raw_data, f)
