#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser

from sibyldeep.models import BaseModel

from pytorch_lightning import Trainer


import pandas as pd

batch_size = 1
forecast_horizon = 1
lookback = 28
n_epochs = 5

train_true_y = []
train_pred_y = []

df = pd.read_csv("./data.csv")
df.columns = ["ds", "y"]
df["ext"] = 1
df = df[:50]


def train(args):
    sibyl_model = BaseModel(args)
    trainer = Trainer(args)
    trainer.fit(sibyl_model)


if __name__ == "__main__":
    hyper_params_parser = ArgumentParser(description="parser")
    # model level
    hyper_params_parser = BaseModel.add_model_specific_args(hyper_params_parser)

    # trainer level
    hyper_params_parser = Trainer.from_argparse_args(hyper_params_parser)

    hyper_params = hyper_params_parser.parse_args()
    train(hyper_params)
