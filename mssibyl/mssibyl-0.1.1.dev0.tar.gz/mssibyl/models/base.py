#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from mssibyl.datasets.utils import TimeSeriesDataset, PredictDataset
from argparse import ArgumentParser
from sklearn.preprocessing import MinMaxScaler


class BaseModel(pl.LightningModule):
    def __init__(self, model_config):
        super(BaseModel, self).__init__()
        self.hparams = self._build_model_specific_hparams(model_config)
        self.sc = MinMaxScaler(feature_range=(0, 0.5))

        self.target = self.hparams.get("target")
        self.forecast_horizon = self.hparams.get("forecast_horizon")
        self.lookback = self.hparams.get("lookback")
        self.num_features = len(self.hparams.get("external_features")) + 1
        self.hidden_size = self.hparams.get("hidden_size")
        self.bidirectional = False

        if isinstance(self.hparams.get("data"), str):
            self.raw_df = pd.read_csv(self.hparams.get("data"))
        else:
            self.raw_df = self.hparams.get("data")

        self.full_df = self.raw_df.copy()

        self.full_df[self.target] = self.sc.fit_transform(
            self.full_df[[self.target]]
        )

        self.encoder = nn.LSTM(
            input_size=self.num_features,
            hidden_size=self.hidden_size,
            num_layers=1,
            dropout=0.0,
            bidirectional=self.bidirectional,
            batch_first=True,
        )
        self.decoder = nn.LSTM(
            input_size=self.hidden_size,
            hidden_size=self.hidden_size // 4,
            num_layers=1,
            dropout=0.0,
            bidirectional=self.bidirectional,
            batch_first=True,
        )
        self.predictor = nn.Linear(
            in_features=self.hidden_size // 4,
            out_features=self.forecast_horizon,
        )
        self.loss_fn = nn.MSELoss()

    def forward(self, x, batch_size=1):

        output, _ = self.encoder(x)

        output = F.dropout(output, p=0.5, training=True)

        output, state = self.decoder(output)
        output = F.dropout(output, p=0.5, training=True)
        output = self.predictor(state[0].squeeze(0))

        return output

    def prepare_data(self):
        self.history = self.full_df.loc[
            self.full_df[self.target].notnull()
        ].copy()

        prepare_for_future = self.history[-self.lookback :]
        self.future = self.full_df.loc[
            self.full_df[self.target].isnull()
        ].copy()
        full_future = pd.concat([prepare_for_future, self.future]).reset_index(
            drop=True
        )

        split_ratio = 0.2

        threshold = int(len(self.history) * (1 - split_ratio))
        df_train = self.history[:threshold]
        df_valid = self.history[threshold:]
        self.dataset_train = TimeSeriesDataset(df_train, self.hparams)
        self.dataset_train.build()
        self.dataset_val = TimeSeriesDataset(df_valid, self.hparams)
        self.dataset_val.build()
        self.dataset_predict = PredictDataset(full_future, self.hparams)
        # self.dataset_predict = TimeSeriesDataset(full_future, self.hparams)
        # self.dataset_predict.build()

    def train_dataloader(self):
        return DataLoader(self.dataset_train, batch_size=1, num_workers=8)

    def val_dataloader(self):
        return DataLoader(self.dataset_val, batch_size=1, num_workers=8)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

    def training_step(self, train_batch, batch_idx):
        x, y = train_batch
        logits = self.forward(x)
        loss = F.mse_loss(logits, y)
        logs = {"train_loss": loss}
        return {"loss": loss, "log": logs}

    def validation_step(self, valid_batch, batch_idx):
        x, y = valid_batch
        logits = self.forward(x)
        loss = F.mse_loss(logits, y)
        return {"val_loss": loss}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x["val_loss"] for x in outputs]).mean()
        tensorboard_logs = {"val_loss": avg_loss}
        # return {"val_loss": avg_loss, "log": tensorboard_logs}
        return {"val_loss": avg_loss}

    def predict(
        self,
        inference_device=None,
        interval=True,
        num_repeats=5,
        include_history=True,
    ):
        if inference_device is None:
            if next(self.parameters()).is_cuda is True:
                inference_device = "cuda:0"
            else:
                inference_device = "cpu"

        repeated_preds = []
        for e in range(num_repeats):
            preds = []
            for i in range(len(self.dataset_predict)):
                x = self.dataset_predict.pop(i, preds)
                x = x.reshape(-1, self.lookback, self.num_features)
                xx = torch.Tensor(x).to(inference_device)
                pred = self.forward(xx)
                preds.append(pred.item())
            repeated_preds.append(preds)
        avg_preds = np.mean(np.array(repeated_preds), axis=0).reshape(-1)

        if interval is True:
            std_preds = np.std(np.array(repeated_preds), axis=0).reshape(-1)
            lower_bound = avg_preds - 2 * std_preds
            upper_bound = avg_preds + 2 * std_preds

            self.future["upper_bound"] = upper_bound
            self.future["lower_bound"] = lower_bound
            self.future["upper_bound"] = self.sc.inverse_transform(
                self.future[["upper_bound"]]
            )
            self.future["lower_bound"] = self.sc.inverse_transform(
                self.future[["lower_bound"]]
            )

        self.future[self.target] = avg_preds
        self.future[self.target] = self.sc.inverse_transform(
            self.future[[self.target]]
        )
        if include_history is True:
            full_predicted = pd.concat([self.raw_df, self.future])
        else:
            full_predicted = self.future

        return full_predicted

    def _build_model_specific_hparams(self, extra):
        default_hparas = {
            "hidden_size": 256,
            "forecast_horizon": 1,
            "lookback": 5,
            "external_features": [],
        }

        for k, v in extra.items():
            default_hparas[k] = v

        return default_hparas
