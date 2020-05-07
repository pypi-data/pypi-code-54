import random


class MutationStrategy:

    def run(self, element, mutation_chance):
        raise NotImplementedError()


class NoMutation(MutationStrategy):

    def run(self, element, mutation_chance):
        pass


class Mutation1(MutationStrategy):

    def run(self, element, mutation_chance):
        for layer in element.model.get_layers():
            weights, bias = layer.get_weights()

            prev_layer_neuron_count, current_layer_neuron_count = weights.shape

            for prev_neuron in range(prev_layer_neuron_count):
                for cur_neuron in range(current_layer_neuron_count):
                    if random.random() < mutation_chance:
                        weights[prev_neuron][cur_neuron] = random.uniform(-1, 1)

            for i in range(len(bias)):
                if random.random() < mutation_chance:
                    bias[i] = random.uniform(-1, 1)

            layer.set_weights((weights, bias))
