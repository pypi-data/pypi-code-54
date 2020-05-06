"""
This example generates some very large objects mainly to test how well they ware handled by visual frontends
"""
# %%
from fn_graph import Composer
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px


def dataframe(dataframe_width, dataframe_length):
    return pd.DataFrame(
        {
            f"dimension_{i}": np.random.random(dataframe_length)
            for i in range(dataframe_width)
        }
    )


def dictionary(dataframe: pd.DataFrame):
    return dataframe.to_dict()


def to_set(dictionary: dict):
    return {f"{k}-{v}" for k, dimension in dictionary.items() for v in dimension}


f = (
    Composer()
    .update_parameters(dataframe_length=100, dataframe_width=10)
    .update(dataframe, dictionary, set=to_set)
)
