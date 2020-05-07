import random

import numpy as np

from python_ne.core.ga import randomly_combine_lists
from python_ne.core.ga.ga_neural_network import GaNeuralNetwork


class CrossoverStrategy:

    def run(self, parent1, parent2):
        raise NotImplementedError()


class NoCrossover(CrossoverStrategy):

    def run(self, parent1, parent2):
        return self.copy_parent(parent1), self.copy_parent(parent2)

    def copy_parent(self, parent):
        child = GaNeuralNetwork(create_model=False, model_adapter=parent.model_adapter,
                                neural_network_config=parent.neural_network_config)
        child.model = parent.model_adapter.new_instance()
        for layer in parent.model.get_layers():

            child.model.add_dense_layer(
                weights=layer.get_weights(),
                input_shape=layer.get_input_shape(),
                units=layer.get_units(),
                activation=layer.get_activation()
            )
        return child


class Crossover1(CrossoverStrategy):

    def run(self, parent1, parent2):
        n_children = 2
        children = []

        for _ in range(n_children):
            child = GaNeuralNetwork(create_model=False, model_adapter=parent1.model_adapter,
                                    neural_network_config=parent1.neural_network_config)
            children.append(child)
            child.model = parent1.model_adapter.new_instance()
            for layer1, layer2 in zip(parent1.model.get_layers(), parent2.model.get_layers()):
                weights1, bias1 = layer1.get_weights()
                weights2, bias2 = layer2.get_weights()

                child_weights = np.zeros(weights1.shape)
                for i in range(weights1.shape[0]):
                    for j in range(weights1.shape[1]):
                        child_weights[i][j] = weights1[i][j] if random.random() < 0.5 else weights2[i][j]

                child_bias = np.zeros(bias1.shape)
                for i in range(bias1.shape[0]):
                    child_bias[i] = bias1[i] if random.random() < 0.5 else bias2[i]

                child.model.add_dense_layer(
                    weights=(child_weights, child_bias),
                    input_shape=layer1.get_input_shape(),
                    units=layer1.get_units(),
                    activation=layer1.get_activation()
                )

        return children


class Crossover2(CrossoverStrategy):

    def run(self, parent1, parent2):
        child1 = GaNeuralNetwork(
            create_model=False,
            model_adapter=parent1.model_adapter,
            neural_network_config=parent1.neural_network_config
        )
        child2 = GaNeuralNetwork(
            create_model=False,
            model_adapter=parent1.model_adapter,
            neural_network_config=parent1.neural_network_config
        )

        child1.model = parent1.model_adapter.new_instance()
        child2.model = parent1.model_adapter.new_instance()

        for parent1_layer, parent2_layer in zip(parent1.model.get_layers(), parent2.model.get_layers()):
            parent1_weights, parent1_bias = parent1_layer.get_weights()
            parent2_weights, parent2_bias = parent2_layer.get_weights()

            prev_layer_neuron_count, current_layer_neuron_count = parent1_weights.shape

            total_weights_count = prev_layer_neuron_count * current_layer_neuron_count

            parent1_weights_flat = parent1_weights.reshape((total_weights_count,))
            parent2_weights_flat = parent2_weights.reshape((total_weights_count,))

            weight_combination1, weight_combination2 = randomly_combine_lists.get_random_lists_combinations(
                parent1_weights_flat, parent2_weights_flat, (prev_layer_neuron_count, current_layer_neuron_count))

            bias_combination_1, bias_combination_2 = randomly_combine_lists \
                .get_random_lists_combinations(parent1_bias, parent2_bias, return_shape=parent1_bias.shape)

            child1.model.add_dense_layer(
                weights=[weight_combination1, bias_combination_1],
                input_shape=parent1_layer.get_input_shape(),
                units=parent1_layer.get_units(),
                activation=parent1_layer.get_activation()
            )
            child2.model.add_dense_layer(
                weights=[weight_combination2, bias_combination_2],
                input_shape=parent1_layer.get_input_shape(),
                units=parent1_layer.get_units(),
                activation=parent1_layer.get_activation()
            )
        return child1, child2


class Crossover3(CrossoverStrategy):

    def run(self, parent1, parent2):
        n_children = 2
        children = []

        for i in range(n_children):
            child = GaNeuralNetwork(
                create_model=False,
                model_adapter=parent1.model_adapter,
                neural_network_config=parent1.neural_network_config
            )

            children.append(child)
            child.model = parent1.model_adapter.new_instance()
            for layers in zip(parent1.model.get_layers(), parent2.model.get_layers()):
                chosen_layer = random.choice(layers)
                child.model.add_dense_layer(
                    units=chosen_layer.get_units(),
                    input_shape=chosen_layer.get_input_shape(),
                    weights=chosen_layer.get_weights(),
                    activation=chosen_layer.get_activation()
                )

        return children


class Crossover4(CrossoverStrategy):

    def run(self, parent1, parent2):
        n_children = 2
        children = []

        fittest_parent = max(parent1, parent2, key=lambda parent: parent.fitness)
        worst_parent = min(parent1, parent2, key=lambda parent: parent.fitness)

        chance = 0.9

        for _ in range(n_children):
            child = GaNeuralNetwork(create_model=False, model_adapter=fittest_parent.model_adapter,
                                    neural_network_config=fittest_parent.neural_network_config)
            children.append(child)
            child.model = fittest_parent.model_adapter.new_instance()
            for best_layer, worst_layer in zip(fittest_parent.model.get_layers(), worst_parent.model.get_layers()):
                best_weights, best_bias = best_layer.get_weights()
                worst_weights, worst_bias = worst_layer.get_weights()

                child_weights = np.zeros(best_weights.shape)
                for i in range(best_weights.shape[0]):
                    for j in range(best_weights.shape[1]):
                        child_weights[i][j] = best_weights[i][j] if random.random() < chance else worst_weights[i][j]

                child_bias = np.zeros(best_bias.shape)
                for i in range(best_bias.shape[0]):
                    child_bias[i] = best_bias[i] if random.random() < chance else worst_bias[i]

                child.model.add_dense_layer(
                    weights=(child_weights, child_bias),
                    input_shape=best_layer.get_input_shape(),
                    units=best_layer.get_units(),
                    activation=best_layer.get_activation()
                )

        return children
