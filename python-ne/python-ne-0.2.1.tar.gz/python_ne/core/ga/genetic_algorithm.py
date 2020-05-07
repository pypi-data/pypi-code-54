import time

import numpy as np

from python_ne.core.ga import random_probability_selection
from python_ne.core.ga.ga_neural_network import GaNeuralNetwork

from python_ne.utils.observed import Observed


class GeneticAlgorithm(Observed):

    def __init__(self, population_size, selection_percentage, mutation_chance, fitness_threshold,
                 neural_network_config, model_adapter, crossover_strategy, mutation_strategy):
        super(GeneticAlgorithm, self).__init__()
        self.crossover_strategy = crossover_strategy
        self.mutation_strategy = mutation_strategy
        self.population_size = population_size
        self.population = self.create_population(neural_network_config, model_adapter)
        self.number_of_selected_elements = int(len(self.population) * selection_percentage)
        self.mutation_chance = mutation_chance
        self.fitness_threshold = fitness_threshold

    def create_population(self, neural_network_config, model_adapter):
        return [GaNeuralNetwork(model_adapter=model_adapter, neural_network_config=neural_network_config)
                for _ in range(self.population_size)]

    def run(self, number_of_generations, calculate_fitness_callback):
        for generation in range(number_of_generations):
            start_generation_time = time.time()
            self.calculate_fitness(calculate_fitness_callback)
            self.normalize_fitness()
            new_elements = self.crossover()
            self.mutate(new_elements)
            self.recycle(new_elements)
            best_element = self.get_best_element()
            generation_time = time.time() - start_generation_time
            self.notify_observers(
                current_generation=generation + 1,
                number_of_generations=number_of_generations,
                generation_time=generation_time,
                population_fitness_std=np.array([e.raw_fitness for e in self.population]).std(),
                best_element_fitness=best_element.raw_fitness
            )
            if best_element.raw_fitness >= self.fitness_threshold:
                break

    def crossover(self):
        total_fitness = sum([element.fitness for element in self.population])
        selected_elements = random_probability_selection.perform_selection(
            [(e, e.fitness / total_fitness) for e in self.population],
            self.number_of_selected_elements
        )

        selected_elements.sort(key=lambda element: element.fitness, reverse=True)

        new_elements = []

        # iterate by pairs of elements
        for element1, element2 in zip(selected_elements[0::2], selected_elements[1::2]):
            new_elements.extend(self.crossover_strategy.run(element1, element2))

        return new_elements

    def mutate(self, new_elements):
        for element in new_elements:
            self.mutation_strategy.run(element, self.mutation_chance)

    def recycle(self, new_elements):
        self.population.sort(key=lambda element: element.fitness)

        for index, new_element in enumerate(new_elements):
            self.population[index] = new_element

    def calculate_fitness(self, calculate_fitness_callback):
        for element in self.population:
            fitness = calculate_fitness_callback(element)
            element.fitness = fitness
            element.raw_fitness = fitness

    def normalize_fitness(self):
        worst_fitness = min(self.population, key=lambda e: e.fitness).fitness
        for element in self.population:
            element.fitness += abs(worst_fitness)

    def get_best_element(self):
        self.population.sort(key=lambda element: element.fitness)
        return self.population[-1]
