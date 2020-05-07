from python_ne.utils.observer import Observer


class ConsoleLogger(Observer):
    def notify(self, *args, **kwargs):
        print(f'generation={kwargs["current_generation"]}/{kwargs["number_of_generations"]},' +
              f' bestfitness={kwargs["best_element_fitness"]}, std={kwargs["population_fitness_std"]},' +
              f' runtime={kwargs["generation_time"]}')
