#!/usr/bin/env python
# encoding: utf-8

import pytorch_lightning as pl


class BaseTrainer(pl.Trainer):
    def __init__(self, *args, **kargs):
        super(BaseTrainer, self).__init__(*args, **kargs)
