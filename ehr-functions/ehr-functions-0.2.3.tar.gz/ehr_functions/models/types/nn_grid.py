from keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier
from eli5.sklearn import PermutationImportance
from livelossplot.keras import PlotLossesCallback
from ehr_functions.models.types._base import Model
import numpy as np
import eli5


class NeuralNetworkGrid(Model):
    def __init__(self, model_fn, epochs=10, batch_size=32, round_output=False, **kwargs):
        super().__init__(**kwargs)

        self.model = KerasClassifier(build_fn=model_fn)
        self.epochs = epochs
        self.batch_size = batch_size
        self.round_output = round_output

    def train(self, x, y):
        x, y = self._process_train_data(x, y)
        print(x.shape)
        print(y.shape)
        self.model.fit(x, y, epochs=self.epochs, batch_size=self.batch_size, validation_split=0.2,
                       callbacks=[PlotLossesCallback()])

    def predict(self, x):
        output = self.model.predict(x)
        if self.round_output:
            output = np.round(output)

        return output
