class GaNeuralNetwork:

    def __init__(self, model_adapter, neural_network_config=None, create_model=True):
        self.model_adapter = model_adapter
        self.neural_network_config = neural_network_config
        self.fitness = 0
        self.raw_fitness = 0
        self.model = self.create_model() if create_model else None

    def create_model(self):
        model = self.model_adapter()
        for i, layer_config in enumerate(self.neural_network_config):
            if i == 0:
                input_shape, unit_count, activation = layer_config
                model.add_dense_layer(activation=activation, input_shape=input_shape, units=unit_count, )
            else:
                unit_count, activation = layer_config
                model.add_dense_layer(activation=activation, units=unit_count, )
        return model

    def get_output(self, obs):
        return self.model.predict(obs)

    def save(self, file_path):
        self.model.save(file_path)

    def load(self, file_path):
        # load is an static method in the adapter class
        self.model = self.model_adapter.load(file_path)

    def __str__(self):
        return f'fitness = {self.fitness}'
