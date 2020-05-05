from ehr_functions.models.types._base import Model


class SKLearnModel(Model):
    def __init__(self, model, kwargs):
        super().__init__()
        self.model = model(**kwargs)

    def train(self, x, y):
        self.model.fit(x, y)

    def predict(self, x):
        return self.model.predict(x)
