#!/usr/bin/env python
# encoding: utf-8


import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader


class PredictDataset:
    def __init__(self, df, config):
        self.df = df
        self.lookback = config.get("lookback")
        self.target = config.get("target")
        self.external_features = config.get("external_features")
        self.sample_size = len(self.df) - self.lookback

    def __len__(self):
        return self.sample_size

    def pop(self, i, preds):
        kk = (
            self.df[[self.target] + self.external_features]
            .copy()
            .values[i : i + self.lookback, :]
        )
        if preds != []:
            predicted = min(self.lookback, len(preds))
            # kk[-len(preds):, 0] = [3*i for i in range(len(preds))]
            kk[-predicted:, 0] = preds[-self.lookback :]
        kk = kk.astype("float32")
        return kk


class TimeSeriesDataset(Dataset):
    def __init__(self, dataset, config):
        self.df = dataset
        self.external_features = config.get("external_features")
        self.target = config.get("target")
        self.lookback = config.get("lookback")
        self.forecast_horizon = config.get("forecast_horizon")
        self.sample_size = len(self.df) - self.lookback - self.forecast_horizon

    def __len__(self):
        return self.sample_size

    def build(self):
        self.x = []
        self.y = []
        for i in range(0, self.sample_size):
            sample_x = (
                self.df[[self.target] + self.external_features]
                .copy()
                .values[i : i + self.lookback, :]
            )
            sample_y = (
                self.df[self.target]
                .copy()
                .values[
                    i
                    + self.lookback : i
                    + self.lookback
                    + self.forecast_horizon
                ]
            )
            # uniform
            # offset = sample_x[0, 0]
            # sample_x[:, 0] -= offset
            # sample_y[0] -= offset
            self.x.append(sample_x)
            self.y.append(sample_y)
        # self.x = np.asarray(self.x)
        # self.y = np.asarray(self.y)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        # print(type(self.x))
        temp_x = self.x[idx].astype("float32")
        temp_y = self.y[idx].astype("float32")

        # sample = (np.array()self.x[idx], self.y[idx])
        sample = (temp_x, temp_y)
        # print(sample[0].dtype)

        return sample


def make_timeline(df, freq="D", periods=100):
    if ("ds" not in df) or ("y" not in df):
        raise ValueError("xxx")
    history = pd.to_datetime(df["ds"]).sort_values()
    last_date = history.max()

    extend_dates = pd.date_range(
        start=last_date, periods=periods + 1, freq=freq, closed="right"
    )
    extend_df = pd.DataFrame({"ds": extend_dates})
    full_dates = pd.concat([df, extend_df]).reset_index(drop=True)

    return full_dates

    # return pd.DataFrame({"ds": full_dates})


#    df["y"] = pd.to_numeric(df["y"])
#    if np.isinf(df["y"].values).any():
#        raise ValueError("")
#    if df["ds"].dtype == np.int64:
#        df["ds"] = df["ds"].astype(str)
#    df["ds"] = pd.to_datetime(df["ds"])
#    if df["ds"].isnull().any():
#        raise ValueError("xxx")
