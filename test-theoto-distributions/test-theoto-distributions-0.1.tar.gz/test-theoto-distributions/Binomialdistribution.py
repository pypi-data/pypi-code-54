# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:42:41 2020

@author: Tati
"""


import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
                
    """
   
    def __init__(self, prob = 0.5, size = 25):
        self.p = prob
        self.n =  size
        mean = self.calculate_mean()
        stdev = self.calculate_stdev()
        Distribution.__init__(self, mean, stdev)

    def calculate_mean(self):
        return self.p * self.n
    
    def calculate_stdev(self):
        return math.sqrt(self.n*self.p*(1-self.p))
    
    def replace_stats_with_data(self):
        self.n = len(self.data)
        pos_values = [x for x in self.data if x >0]
        self.p = len(pos_values)/self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n
    
    def plot_bar(self):
        plt.hist(self.data)
        plt.xlabel('Results')
        plt.ylabel('Frequency')
        plt.titel('Binomial Distribution')
        plt.show()
    
    def pdf(self, k):
        n = self.n
        p = self.p
        return (math.factorial(n)*(p**k)*((1-p)**(n-k)))/(math.factorial(k)*math.factorial(n-k))
            
    def plot_bar_plf(self):
        
        x = []
        y = []

        # calculate the x values to visualize
        for k in range(self.n + 1):
            x.append(k)
            y.append(self.pdf(k))

        plt.plot(x, y)
        plt.set_title('Binomial Distribution: Probability density function')
        plt.set_ylabel('Density')
        plt.show()

        return x, y

    def __add__(self, other):
        try:
            assert self.p == other.p, 'p values are not equal'
            results = Binomial()
            results.n = self.n + other.n
            results.p = self.p 
            return results
        except AssertionError as error:
            raise Exception('p values are not equal: {} and {}'.format(self.p, other.p))
        
    def __repr__(self):
        return "mean {:.0f}, standard deviation {:.1f}, p {:.1f}, n {:.0f}".format(self.mean, self.stdev, self.p, self.n)
                    