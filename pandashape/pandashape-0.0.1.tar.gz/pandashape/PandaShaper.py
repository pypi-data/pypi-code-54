import pandas as pd
from pandashape import Columns
from pandashape.describers.GeneralDescriber import GeneralDescriber
from pandashape.internal.TransformerExecutor import TransformerExecutor


class PandaShaper:
    def __init__(self, df, inplace=False):
        assert(isinstance(df, pd.DataFrame))

        # why does this cause an evaluation of the truth of df?
        # self.df = df if inplace else df.copy(df)
        self.df = df
        if not inplace:
            self.df = df.copy()

    def describe(self, columnDefinitions=None):
        if columnDefinitions is None:
            describer = GeneralDescriber(self.df)
            return describer.describe(self.df)

    def transform(self, columnDefinitions):
        executor = TransformerExecutor()
        newColumns = executor.transform(self.df, columnDefinitions)
        print('new columns!', newColumns)
