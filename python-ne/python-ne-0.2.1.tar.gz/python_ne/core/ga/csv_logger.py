import csv

from python_ne.utils.observer import Observer


class CsvLogger(Observer):

    def notify(self, *args, **kwargs):
        data = {
            'generation': kwargs['current_generation'],
            'best_element_fitness': kwargs['best_element_fitness'],
            'population_fitness_std': kwargs['population_fitness_std'],
            'time_to_run_generation': kwargs['generation_time']
        }

        self.logged_data.append(data)

    def __init__(self):
        self.logged_data = []

    def save(self, file_path):
        file = open(file_path, 'w+')
        csv_writer = csv.DictWriter(file, fieldnames=self.logged_data[0].keys())

        csv_writer.writeheader()

        for data in self.logged_data:
            csv_writer.writerow(data)

        file.close()
