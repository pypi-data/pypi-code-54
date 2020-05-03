import pandas as pd


class GenericDescriber:
    def __init__(self, df):
        self.df = df

    def describe(self):
        raise NotImplementedError()
