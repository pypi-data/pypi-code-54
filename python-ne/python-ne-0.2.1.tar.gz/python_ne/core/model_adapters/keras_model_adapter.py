import keras
import numpy as np
from keras import Sequential
from keras.layers import Dense

from python_ne.core.model_adapters.model_adapter import ModelAdapter
from python_ne.core.model_adapters.keras_dense_layer_adapter import KerasDenseLayerAdapter


class KerasModelAdapter(ModelAdapter):

    @staticmethod
    def load(file_path):
        adapter = KerasModelAdapter()
        adapter.model = keras.models.load_model(file_path)
        return adapter

    def build_model(self):
        return Sequential()

    def add_dense_layer(self, **kwargs):
        self.model.add(Dense(**kwargs))

    def get_weights(self):
        return self.model.get_weights()

    def set_weights(self, weights):
        self.model.set_weights()

    def predict(self, obs):
        return self.model.predict(obs.reshape((1,) + obs.shape))

    def get_layers(self):
        return [KerasDenseLayerAdapter(layer) for layer in self.model.layers]

    def save(self, file_path):
        self.model.save(file_path)

    @staticmethod
    def new_instance():
        return KerasModelAdapter()
