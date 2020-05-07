from python_ne.utils.observer import Observer
import matplotlib.pyplot as plt
import numpy as np
import os


class MatplotlibLogger(Observer):

    def __init__(self):
        self.logged_data = []

    def notify(self, *args, **kwargs):
        data = {
            'generation': kwargs['current_generation'],
            'best_element_fitness': kwargs['best_element_fitness'],
            'time_to_run_generation': kwargs['generation_time'],
            'population_fitness_std': kwargs['population_fitness_std']
        }

        self.logged_data.append(data)

    def save_fitness_chart(self, file_path='', fitness_label='fitness', generation_label='generation',
                           chart_title='generation - fitness'):
        x = [data['generation'] for data in self.logged_data]
        y = [data['best_element_fitness'] for data in self.logged_data]

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.set(xlabel=generation_label, ylabel=fitness_label,
               title=chart_title)
        ax.grid()

        fig.savefig(file_path)

    def save_time_chart(self, file_path, time_label='time (s)', generation_label='generation',
                        chart_title='generation - time'):
        x = [data['generation'] for data in self.logged_data]
        y = [data['time_to_run_generation'] for data in self.logged_data]

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.set(xlabel=generation_label, ylabel=time_label,
               title=chart_title)
        ax.grid()

        fig.savefig(file_path)

    def save_std_chart(self, file_path, std_label='std', generation_label='generation', chart_title='generation - std'):
        x = [data['generation'] for data in self.logged_data]
        y = [data['population_fitness_std'] for data in self.logged_data]

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.set(xlabel=generation_label, ylabel=std_label,
               title=chart_title)
        ax.grid()

        fig.savefig(file_path)
