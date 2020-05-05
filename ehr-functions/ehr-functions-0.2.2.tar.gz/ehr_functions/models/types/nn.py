# from livelossplot.keras import PlotLossesCallback
from ehr_functions.models.types._base import Model
import numpy as np


class NeuralNetwork(Model):
    def __init__(self, model, epochs=10, batch_size=32, round_output=False, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.epochs = epochs
        self.batch_size = batch_size
        self.round_output = round_output

    def train(self, x, y):
        self.model.fit(x, y, epochs=self.epochs, batch_size=self.batch_size, validation_split=0.2)
        # callbacks=[PlotLossesCallback()])

    def predict(self, x):
        output = self.model.predict(x)
        if self.round_output:
            output = np.round(output)

        return output
