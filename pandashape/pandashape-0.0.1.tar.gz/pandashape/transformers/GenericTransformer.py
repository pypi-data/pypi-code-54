class GenericTransformer:
    def transform(self):
        raise NotImplementedError()

    def transformSeries(self, series):
        raise NotImplementedError()
