#!/usr/bin/env python
# encoding: utf-8

from mssibyl.models import BaseModel
from mssibyl.trainer import BaseTrainer
from mssibyl.datasets.utils import make_timeline

import pandas as pd

df = pd.read_csv("./data.csv")
df.columns = ["ds", "y"]
df = df[:1000]

df_with_future = make_timeline(df, freq="H", periods=300)

args = {
    "lookback": 48,
    "forecast_horizon": 1,
    "data": df_with_future,
    "target": "y",
}

sibyl_model = BaseModel(args)
trainer = BaseTrainer(
    max_epochs=100, gpus=1, show_progress_bar=False, early_stop_callback=True
)
trainer.fit(sibyl_model)
preds = sibyl_model.predict(interval=True, include_history=True)

preds.to_csv("res.csv", index=False)
